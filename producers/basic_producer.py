"""
Producer básico para Confluent Cloud
Este script envía mensajes a un topic en Confluent Cloud
"""

import json
import os
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv(dotenv_path='../config/.env')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfluentProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
        self.api_key = os.getenv('CONFLUENT_API_KEY')
        self.api_secret = os.getenv('CONFLUENT_API_SECRET')
        
        if not all([self.bootstrap_servers, self.api_key, self.api_secret]):
            raise ValueError("Faltan credenciales de Confluent Cloud en .env")
        
        # Configuración del producer
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=self.api_key,
            sasl_plain_password=self.api_secret,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )
        
        logger.info("Producer configurado exitosamente")
    
    def send_message(self, topic: str, message: dict, key: str = None):
        """
        Envía un mensaje a un topic específico
        
        Args:
            topic (str): Nombre del topic
            message (dict): Mensaje a enviar
            key (str): Clave del mensaje (opcional)
        """
        try:
            # Agregar timestamp al mensaje
            message['timestamp'] = datetime.now().isoformat()
            
            # Enviar mensaje
            future = self.producer.send(topic, value=message, key=key)
            
            # Esperar confirmación
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Mensaje enviado a {topic}: partition={record_metadata.partition}, offset={record_metadata.offset}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False
    
    def send_user_event(self, user_id: str, event_type: str, data: dict):
        """
        Envía un evento de usuario
        
        Args:
            user_id (str): ID del usuario
            event_type (str): Tipo de evento (login, logout, purchase, etc.)
            data (dict): Datos adicionales del evento
        """
        message = {
            'user_id': user_id,
            'event_type': event_type,
            'data': data
        }
        
        topic = os.getenv('TOPIC_USER_EVENTS', 'user-events')
        return self.send_message(topic, message, key=user_id)
    
    def send_system_log(self, level: str, message: str, service: str):
        """
        Envía un log del sistema
        
        Args:
            level (str): Nivel del log (INFO, WARN, ERROR)
            message (str): Mensaje del log
            service (str): Servicio que genera el log
        """
        log_message = {
            'level': level,
            'message': message,
            'service': service
        }
        
        topic = os.getenv('TOPIC_SYSTEM_LOGS', 'system-logs')
        return self.send_message(topic, log_message, key=service)
    
    def close(self):
        """Cierra el producer"""
        self.producer.close()
        logger.info("Producer cerrado")

def main():
    """Función principal con ejemplos de uso"""
    producer = ConfluentProducer()
    
    try:
        # Ejemplo 1: Evento de usuario
        print("📧 Enviando evento de usuario...")
        success = producer.send_user_event(
            user_id="user_123",
            event_type="login",
            data={"ip": "192.168.1.1", "device": "mobile"}
        )
        
        if success:
            print("✅ Evento de usuario enviado exitosamente")
        
        # Ejemplo 2: Log del sistema
        print("\n📝 Enviando log del sistema...")
        success = producer.send_system_log(
            level="INFO",
            message="Aplicación iniciada correctamente",
            service="auth-service"
        )
        
        if success:
            print("✅ Log del sistema enviado exitosamente")
        
        # Ejemplo 3: Mensaje personalizado
        print("\n🔔 Enviando notificación...")
        notification = {
            "title": "Bienvenido a Confluent",
            "message": "Tu primer mensaje fue enviado exitosamente",
            "recipient": "user_123",
            "channel": "email"
        }
        
        topic = os.getenv('TOPIC_NOTIFICATIONS', 'notifications')
        success = producer.send_message(topic, notification, key="user_123")
        
        if success:
            print("✅ Notificación enviada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
    
    finally:
        producer.close()

if __name__ == "__main__":
    main()
