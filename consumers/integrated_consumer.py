"""
Consumer integrado que procesa mensajes y los envía a AWS
Este script combina el consumo de Confluent Cloud con la integración a AWS
"""

import json
import os
import sys
sys.path.append('../aws-integration')

from kafka import KafkaConsumer
from dotenv import load_dotenv
from aws_services import AWSIntegration
import logging
import signal

# Cargar variables de entorno
load_dotenv(dotenv_path='../config/.env')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegratedConsumer:
    def __init__(self, topics: list, group_id: str = "aws-integration-group"):
        """
        Inicializa el consumer integrado con AWS
        
        Args:
            topics (list): Lista de topics a consumir
            group_id (str): ID del grupo de consumidores
        """
        self.bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
        self.api_key = os.getenv('CONFLUENT_API_KEY')
        self.api_secret = os.getenv('CONFLUENT_API_SECRET')
        
        if not all([self.bootstrap_servers, self.api_key, self.api_secret]):
            raise ValueError("Faltan credenciales de Confluent Cloud en .env")
        
        # Configurar consumer de Kafka
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=self.api_key,
            sasl_plain_password=self.api_secret,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )
        
        # Inicializar integración AWS
        self.aws_integration = AWSIntegration()
        
        self.running = True
        self.message_count = 0
        
        logger.info(f"Consumer integrado configurado para topics: {topics}")
    
    def process_message(self, message):
        """
        Procesa un mensaje y lo envía a AWS
        
        Args:
            message: Mensaje de Kafka
        """
        try:
            self.message_count += 1
            
            print(f"\n📨 Mensaje #{self.message_count} recibido:")
            print(f"   Topic: {message.topic}")
            print(f"   Key: {message.key}")
            print(f"   Timestamp: {message.timestamp}")
            print(f"   Value: {json.dumps(message.value, indent=2, ensure_ascii=False)}")
            
            # Procesar según el topic
            if message.topic == 'user-events':
                self.process_user_event(message.value)
            elif message.topic == 'system-logs':
                self.process_system_log(message.value)
            elif message.topic == 'notifications':
                self.process_notification(message.value)
            else:
                # Procesamiento genérico
                self.process_generic_message(message.topic, message.value)
            
            print("✅ Mensaje procesado y enviado a AWS")
            print("-" * 60)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            print(f"❌ Error procesando mensaje: {e}")
    
    def process_user_event(self, event_data):
        """
        Procesa eventos de usuario y los envía a AWS
        
        Args:
            event_data (dict): Datos del evento
        """
        print("🔵 Procesando evento de usuario...")
        
        # Enviar a AWS
        success = self.aws_integration.process_user_event_to_aws(event_data)
        
        if success:
            print("   → Evento almacenado en S3")
            print("   → Log enviado a CloudWatch")
            print("   → Métrica enviada a CloudWatch")
        
        # Lógica de negocio adicional
        event_type = event_data.get('event_type')
        user_id = event_data.get('user_id')
        
        if event_type == 'login':
            print(f"   → Usuario {user_id} ha iniciado sesión")
        elif event_type == 'purchase':
            print(f"   → Usuario {user_id} ha realizado una compra")
            # Aquí podrías actualizar inventario, enviar confirmación, etc.
        elif event_type == 'logout':
            print(f"   → Usuario {user_id} ha cerrado sesión")
    
    def process_system_log(self, log_data):
        """
        Procesa logs del sistema y los envía a AWS
        
        Args:
            log_data (dict): Datos del log
        """
        print("📝 Procesando log del sistema...")
        
        # Enviar a AWS
        success = self.aws_integration.process_system_log_to_aws(log_data)
        
        if success:
            print("   → Log enviado a CloudWatch")
            if log_data.get('level') == 'ERROR':
                print("   → Error almacenado en S3 para análisis")
            print("   → Métrica enviada a CloudWatch")
        
        # Lógica de alerta para errores críticos
        if log_data.get('level') == 'ERROR':
            print("   🚨 ERROR CRÍTICO DETECTADO")
            # Aquí podrías enviar alertas, notificaciones, etc.
    
    def process_notification(self, notification_data):
        """
        Procesa notificaciones
        
        Args:
            notification_data (dict): Datos de la notificación
        """
        print("🔔 Procesando notificación...")
        
        # Almacenar en S3
        self.aws_integration.store_data_in_s3(
            notification_data, 
            f"notifications/{notification_data.get('recipient')}/notification.json"
        )
        
        # Enviar log
        log_message = f"NOTIFICATION: {notification_data.get('title')} to {notification_data.get('recipient')}"
        self.aws_integration.send_to_cloudwatch_logs(log_message, "notifications")
        
        # Enviar métrica
        self.aws_integration.send_metric_to_cloudwatch("NotificationsSent", 1)
        
        print("   → Notificación almacenada en S3")
        print("   → Log enviado a CloudWatch")
        print("   → Métrica actualizada")
    
    def process_generic_message(self, topic, message_data):
        """
        Procesamiento genérico para cualquier mensaje
        
        Args:
            topic (str): Nombre del topic
            message_data (dict): Datos del mensaje
        """
        print(f"📄 Procesando mensaje genérico del topic: {topic}")
        
        # Almacenar en S3
        s3_key = f"generic-messages/{topic}/{message_data.get('timestamp', 'unknown')}.json"
        self.aws_integration.store_data_in_s3(message_data, s3_key)
        
        # Enviar métrica
        self.aws_integration.send_metric_to_cloudwatch(f"Messages_{topic}", 1)
        
        print("   → Mensaje almacenado en S3")
        print("   → Métrica enviada a CloudWatch")
    
    def start_consuming(self):
        """Inicia el consumo de mensajes"""
        logger.info("Iniciando consumer integrado con AWS...")
        print("🚀 Consumer AWS integrado iniciado")
        print("📡 Conectado a Confluent Cloud")
        print("☁️  Conectado a AWS")
        print("Presiona Ctrl+C para detener.")
        print("=" * 60)
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                self.process_message(message)
                
        except KeyboardInterrupt:
            logger.info("Recibida señal de interrupción")
        except Exception as e:
            logger.error(f"Error en el consumer: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Detiene el consumer"""
        self.running = False
        self.consumer.close()
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   Mensajes procesados: {self.message_count}")
        
        logger.info("Consumer integrado detenido")

def signal_handler(signum, frame):
    """Manejador de señales para detener gracefully"""
    print("\n🛑 Deteniendo consumer integrado...")
    global consumer
    if 'consumer' in globals():
        consumer.stop()
    sys.exit(0)

def main():
    """Función principal"""
    global consumer
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Topics a consumir
    topics = [
        os.getenv('TOPIC_USER_EVENTS', 'user-events'),
        os.getenv('TOPIC_SYSTEM_LOGS', 'system-logs'),
        os.getenv('TOPIC_NOTIFICATIONS', 'notifications')
    ]
    
    try:
        # Crear y iniciar consumer
        consumer = IntegratedConsumer(topics, group_id="aws-integration-group")
        consumer.start_consuming()
        
    except Exception as e:
        logger.error(f"Error iniciando consumer: {e}")
        print(f"❌ Error: {e}")
        print("\n💡 Verifica que:")
        print("   1. El archivo .env esté configurado correctamente")
        print("   2. Las credenciales de Confluent Cloud sean válidas")
        print("   3. Las credenciales de AWS sean válidas")
        print("   4. Los topics existan en Confluent Cloud")

if __name__ == "__main__":
    main()
