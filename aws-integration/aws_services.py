"""
Integración con servicios AWS
Este módulo proporciona funcionalidades para integrar Confluent con AWS
"""

import json
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv(dotenv_path='../config/.env')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSIntegration:
    def __init__(self):
        """Inicializa la integración con AWS"""
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_bucket = os.getenv('AWS_S3_BUCKET')
        self.cloudwatch_log_group = os.getenv('AWS_CLOUDWATCH_LOG_GROUP')
        
        if not all([self.aws_access_key, self.aws_secret_key, self.s3_bucket]):
            raise ValueError("Faltan credenciales de AWS en .env")
        
        # Inicializar clientes AWS
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region
        )
        
        self.cloudwatch_client = boto3.client(
            'logs',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region
        )
        
        self.cloudwatch_metrics = boto3.client(
            'cloudwatch',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region
        )
        
        logger.info("Integración AWS inicializada exitosamente")
    
    def store_data_in_s3(self, data: dict, key: str = None):
        """
        Almacena datos en S3
        
        Args:
            data (dict): Datos a almacenar
            key (str): Clave del objeto en S3
        """
        try:
            if not key:
                timestamp = datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
                key = f"confluent-data/{timestamp}.json"
            
            # Convertir datos a JSON
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            # Subir a S3
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=key,
                Body=json_data,
                ContentType='application/json'
            )
            
            logger.info(f"Datos almacenados en S3: s3://{self.s3_bucket}/{key}")
            return True
            
        except ClientError as e:
            logger.error(f"Error almacenando en S3: {e}")
            return False
    
    def send_to_cloudwatch_logs(self, log_message: str, log_stream: str = None):
        """
        Envía logs a CloudWatch Logs
        
        Args:
            log_message (str): Mensaje de log
            log_stream (str): Stream de logs (opcional)
        """
        try:
            if not log_stream:
                log_stream = f"confluent-stream-{datetime.now().strftime('%Y-%m-%d')}"
            
            # Crear stream si no existe
            try:
                self.cloudwatch_client.create_log_stream(
                    logGroupName=self.cloudwatch_log_group,
                    logStreamName=log_stream
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
            
            # Enviar log
            self.cloudwatch_client.put_log_events(
                logGroupName=self.cloudwatch_log_group,
                logStreamName=log_stream,
                logEvents=[
                    {
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'message': log_message
                    }
                ]
            )
            
            logger.info(f"Log enviado a CloudWatch: {self.cloudwatch_log_group}/{log_stream}")
            return True
            
        except ClientError as e:
            logger.error(f"Error enviando a CloudWatch: {e}")
            return False
    
    def send_metric_to_cloudwatch(self, metric_name: str, value: float, unit: str = 'Count'):
        """
        Envía métricas a CloudWatch
        
        Args:
            metric_name (str): Nombre de la métrica
            value (float): Valor de la métrica
            unit (str): Unidad de medida
        """
        try:
            self.cloudwatch_metrics.put_metric_data(
                Namespace='Confluent/Integration',
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Timestamp': datetime.now()
                    }
                ]
            )
            
            logger.info(f"Métrica enviada a CloudWatch: {metric_name} = {value} {unit}")
            return True
            
        except ClientError as e:
            logger.error(f"Error enviando métrica: {e}")
            return False
    
    def process_user_event_to_aws(self, event_data: dict):
        """
        Procesa eventos de usuario y los envía a AWS
        
        Args:
            event_data (dict): Datos del evento
        """
        try:
            # 1. Almacenar en S3 para análisis posterior
            s3_key = f"user-events/{event_data.get('user_id')}/{datetime.now().strftime('%Y/%m/%d')}/{event_data.get('event_type')}.json"
            self.store_data_in_s3(event_data, s3_key)
            
            # 2. Enviar log a CloudWatch
            log_message = f"USER_EVENT: {event_data.get('user_id')} - {event_data.get('event_type')}"
            self.send_to_cloudwatch_logs(log_message, "user-events")
            
            # 3. Enviar métrica
            self.send_metric_to_cloudwatch(f"UserEvent_{event_data.get('event_type')}", 1)
            
            return True
            
        except Exception as e:
            logger.error(f"Error procesando evento de usuario: {e}")
            return False
    
    def process_system_log_to_aws(self, log_data: dict):
        """
        Procesa logs del sistema y los envía a AWS
        
        Args:
            log_data (dict): Datos del log
        """
        try:
            # 1. Enviar a CloudWatch Logs
            log_message = f"[{log_data.get('level')}] {log_data.get('service')}: {log_data.get('message')}"
            self.send_to_cloudwatch_logs(log_message, f"system-logs-{log_data.get('service')}")
            
            # 2. Si es ERROR, almacenar en S3 para análisis
            if log_data.get('level') == 'ERROR':
                s3_key = f"error-logs/{log_data.get('service')}/{datetime.now().strftime('%Y/%m/%d')}/error.json"
                self.store_data_in_s3(log_data, s3_key)
            
            # 3. Enviar métricas por nivel
            self.send_metric_to_cloudwatch(f"SystemLog_{log_data.get('level')}", 1)
            
            return True
            
        except Exception as e:
            logger.error(f"Error procesando log del sistema: {e}")
            return False
    
    def list_s3_objects(self, prefix: str = ""):
        """
        Lista objetos en S3
        
        Args:
            prefix (str): Prefijo para filtrar objetos
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=prefix
            )
            
            objects = response.get('Contents', [])
            logger.info(f"Encontrados {len(objects)} objetos en S3")
            
            return objects
            
        except ClientError as e:
            logger.error(f"Error listando objetos S3: {e}")
            return []

def main():
    """Función principal con ejemplos de uso"""
    try:
        aws_integration = AWSIntegration()
        
        # Ejemplo 1: Almacenar datos en S3
        print("📦 Almacenando datos en S3...")
        sample_data = {
            "message": "Datos de ejemplo desde Confluent",
            "timestamp": datetime.now().isoformat(),
            "source": "confluent-producer"
        }
        
        success = aws_integration.store_data_in_s3(sample_data)
        if success:
            print("✅ Datos almacenados exitosamente en S3")
        
        # Ejemplo 2: Enviar log a CloudWatch
        print("\n📝 Enviando log a CloudWatch...")
        log_message = "Aplicación de integración AWS-Confluent iniciada"
        success = aws_integration.send_to_cloudwatch_logs(log_message)
        if success:
            print("✅ Log enviado exitosamente a CloudWatch")
        
        # Ejemplo 3: Enviar métrica
        print("\n📊 Enviando métrica a CloudWatch...")
        success = aws_integration.send_metric_to_cloudwatch("TestMetric", 1.0)
        if success:
            print("✅ Métrica enviada exitosamente a CloudWatch")
        
        # Ejemplo 4: Listar objetos en S3
        print("\n📋 Listando objetos en S3...")
        objects = aws_integration.list_s3_objects()
        print(f"Objetos encontrados: {len(objects)}")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")

if __name__ == "__main__":
    main()
