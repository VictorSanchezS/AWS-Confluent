"""
Consumer básico para Confluent Cloud
Este script consume mensajes de un topic en Confluent Cloud
"""

import json
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
import logging
import signal
import sys

# Cargar variables de entorno
load_dotenv(dotenv_path='../config/.env')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfluentConsumer:
    def __init__(self, topics: list, group_id: str = "default-group"):
        self.bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
        self.api_key = os.getenv('CONFLUENT_API_KEY')
        self.api_secret = os.getenv('CONFLUENT_API_SECRET')
        
        if not all([self.bootstrap_servers, self.api_key, self.api_secret]):
            raise ValueError("Faltan credenciales de Confluent Cloud en .env")
        
        # Configuración del consumer
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
            auto_offset_reset='earliest',  # Leer desde el principio
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )
        
        self.running = True
        logger.info(f"Consumer configurado para topics: {topics}, group: {group_id}")
    
    def process_message(self, message):
        """
        Procesa un mensaje recibido
        
        Args:
            message: Mensaje de Kafka
        """
        try:
            print(f"\n📨 Nuevo mensaje recibido:")
            print(f"   Topic: {message.topic}")
            print(f"   Partition: {message.partition}")
            print(f"   Offset: {message.offset}")
            print(f"   Key: {message.key}")
            print(f"   Timestamp: {message.timestamp}")
            print(f"   Value: {json.dumps(message.value, indent=2, ensure_ascii=False)}")
            print("-" * 50)
            
            # Aquí puedes agregar lógica específica según el topic
            if message.topic == 'user-events':
                self.process_user_event(message.value)
            elif message.topic == 'system-logs':
                self.process_system_log(message.value)
            elif message.topic == 'notifications':
                self.process_notification(message.value)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
    
    def process_user_event(self, event_data):
        """Procesa eventos de usuario"""
        user_id = event_data.get('user_id')
        event_type = event_data.get('event_type')
        
        print(f"🔵 Evento de usuario: {user_id} - {event_type}")
        
        # Ejemplo: almacenar en base de datos, enviar métricas, etc.
        if event_type == 'login':
            print("   → Actualizando última conexión del usuario")
        elif event_type == 'purchase':
            print("   → Procesando compra y actualizando inventario")
    
    def process_system_log(self, log_data):
        """Procesa logs del sistema"""
        level = log_data.get('level')
        service = log_data.get('service')
        message = log_data.get('message')
        
        print(f"📝 Log del sistema [{level}] {service}: {message}")
        
        # Ejemplo: enviar a CloudWatch, filtrar errores críticos, etc.
        if level == 'ERROR':
            print("   → Enviando alerta por error crítico")
    
    def process_notification(self, notification_data):
        """Procesa notificaciones"""
        title = notification_data.get('title')
        recipient = notification_data.get('recipient')
        channel = notification_data.get('channel')
        
        print(f"🔔 Notificación para {recipient} por {channel}: {title}")
        
        # Ejemplo: enviar email, push notification, SMS, etc.
        if channel == 'email':
            print("   → Enviando email")
        elif channel == 'push':
            print("   → Enviando push notification")
    
    def start_consuming(self):
        """Inicia el consumo de mensajes"""
        logger.info("Iniciando consumo de mensajes...")
        print("🚀 Consumer iniciado. Presiona Ctrl+C para detener.")
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
        logger.info("Consumer detenido")

def signal_handler(signum, frame):
    """Manejador de señales para detener gracefully"""
    print("\n🛑 Deteniendo consumer...")
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
    
    # Crear y iniciar consumer
    consumer = ConfluentConsumer(topics, group_id="aws-integration-group")
    consumer.start_consuming()

if __name__ == "__main__":
    main()
