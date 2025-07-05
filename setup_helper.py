"""
Script para obtener información de configuración de Confluent Cloud
Te ayuda a encontrar los datos que necesitas en la consola web
"""

import json
from datetime import datetime

def print_configuration_guide():
    """Imprime una guía para obtener la configuración desde las consolas web"""
    
    print("🔧 GUÍA DE CONFIGURACIÓN - CONFLUENT CLOUD + AWS")
    print("=" * 60)
    
    print("\n📋 DATOS QUE NECESITAS RECOPILAR:")
    print("-" * 40)
    
    # Confluent Cloud
    print("\n🌟 CONFLUENT CLOUD:")
    print("   Ve a: https://confluent.cloud")
    print("   1. Bootstrap Servers:")
    print("      📍 Ubicación: Cluster Settings → Endpoint")
    print("      📋 Formato: pkc-xxxxx.us-east-1.aws.confluent.cloud:9092")
    print("      💾 Variable: CONFLUENT_BOOTSTRAP_SERVERS")
    
    print("\n   2. API Key y Secret:")
    print("      📍 Ubicación: Data integration → API keys")
    print("      📋 Crear nueva key con 'Global access'")
    print("      💾 Variables: CONFLUENT_API_KEY, CONFLUENT_API_SECRET")
    
    print("\n   3. Schema Registry (opcional):")
    print("      📍 Ubicación: Schema Registry → Settings")
    print("      📋 Formato: https://psrc-xxxxx.us-east-1.aws.confluent.cloud")
    print("      💾 Variable: CONFLUENT_SCHEMA_REGISTRY_URL")
    
    # AWS
    print("\n☁️  AWS:")
    print("   Ve a: https://console.aws.amazon.com")
    print("   1. IAM - Crear usuario:")
    print("      📍 Ubicación: IAM → Users → Add user")
    print("      📋 Nombre: confluent-integration-user")
    print("      📋 Access type: Programmatic access")
    print("      📋 Políticas: AmazonS3FullAccess, CloudWatchFullAccess")
    print("      💾 Variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
    
    print("\n   2. S3 - Crear bucket:")
    print("      📍 Ubicación: S3 → Create bucket")
    print("      📋 Nombre: confluent-data-[tu-nombre] (único globalmente)")
    print("      📋 Región: us-east-1")
    print("      💾 Variable: AWS_S3_BUCKET")
    
    print("\n   3. CloudWatch - Crear log group:")
    print("      📍 Ubicación: CloudWatch → Logs → Log groups")
    print("      📋 Nombre: /confluent/mi-aplicacion")
    print("      💾 Variable: AWS_CLOUDWATCH_LOG_GROUP")

def generate_env_template():
    """Genera un template del archivo .env con instrucciones"""
    
    template = """# ==============================================
# CONFIGURACIÓN AWS-CONFLUENT
# ==============================================

# PASO 1: Ve a https://confluent.cloud
# Cluster Settings → Endpoint
CONFLUENT_BOOTSTRAP_SERVERS=pkc-XXXXX.us-east-1.aws.confluent.cloud:9092

# Data integration → API keys → Create key
CONFLUENT_API_KEY=XXXXXXXXXXXXXXXX
CONFLUENT_API_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Schema Registry → Settings (opcional)
CONFLUENT_SCHEMA_REGISTRY_URL=https://psrc-XXXXX.us-east-1.aws.confluent.cloud
CONFLUENT_SCHEMA_REGISTRY_API_KEY=XXXXXXXXXXXXXXXX
CONFLUENT_SCHEMA_REGISTRY_API_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# PASO 2: Ve a https://console.aws.amazon.com
# IAM → Users → Add user → Programmatic access
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AWS_REGION=us-east-1

# S3 → Create bucket (nombre único)
AWS_S3_BUCKET=confluent-data-tu-nombre-aqui

# CloudWatch → Logs → Log groups
AWS_CLOUDWATCH_LOG_GROUP=/confluent/mi-aplicacion

# ==============================================
# TOPICS A CREAR EN CONFLUENT CLOUD
# ==============================================
# Ve a: Tu cluster → Topics → Add topic

TOPIC_USER_EVENTS=estudiante-eventos
TOPIC_SYSTEM_LOGS=sistema-logs
TOPIC_NOTIFICATIONS=notificaciones

# ==============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==============================================
APP_NAME=aws-confluent-integration
LOG_LEVEL=INFO"""

    return template

def create_topics_guide():
    """Guía específica para crear topics"""
    
    print("\n📝 GUÍA PARA CREAR TOPICS EN CONFLUENT CLOUD:")
    print("-" * 50)
    
    topics_info = [
        {
            "name": "estudiante-eventos",
            "description": "Eventos relacionados con estudiantes",
            "partitions": 1,
            "retention": "7 days",
            "examples": ["login", "logout", "submit_assignment", "view_grade"]
        },
        {
            "name": "sistema-logs",
            "description": "Logs del sistema y errores",
            "partitions": 1,
            "retention": "7 days",
            "examples": ["application_start", "error_occurred", "warning", "info"]
        },
        {
            "name": "notificaciones",
            "description": "Notificaciones para usuarios",
            "partitions": 1,
            "retention": "3 days",
            "examples": ["email_notification", "push_notification", "sms"]
        }
    ]
    
    for i, topic in enumerate(topics_info, 1):
        print(f"\n{i}. Topic: {topic['name']}")
        print(f"   📝 Descripción: {topic['description']}")
        print(f"   🔧 Particiones: {topic['partitions']}")
        print(f"   ⏰ Retención: {topic['retention']}")
        print(f"   💡 Ejemplos de mensajes: {', '.join(topic['examples'])}")

def print_next_steps():
    """Imprime los próximos pasos a seguir"""
    
    print("\n\n🚀 PRÓXIMOS PASOS:")
    print("-" * 20)
    print("1. 📝 Recopila toda la información de las consolas web")
    print("2. 📄 Edita el archivo config/.env con tus datos")
    print("3. 🧪 Ejecuta: python test_integration.py")
    print("4. 📤 Ejecuta: python producers/basic_producer.py")
    print("5. 📥 Ejecuta: python consumers/integrated_consumer.py")
    print("6. 📊 Revisa los datos en AWS S3 y CloudWatch")

def main():
    """Función principal"""
    print_configuration_guide()
    
    # Crear archivo .env personalizado
    print("\n💾 Creando archivo de configuración personalizado...")
    env_content = generate_env_template()
    
    with open('config/.env.personal', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Archivo creado: config/.env.personal")
    print("📝 Edita este archivo con tus datos y luego renómbralo a .env")
    
    create_topics_guide()
    print_next_steps()
    
    print("\n" + "=" * 60)
    print("🎯 OBJETIVO DE INVESTIGACIÓN SOBRE TOPICS:")
    print("Los topics son la base del streaming de datos.")
    print("Permiten organizar, escalar y procesar datos en tiempo real.")
    print("Tu investigación debe cubrir:")
    print("- ¿Cómo funcionan internamente?")
    print("- ¿Qué ventajas ofrecen?")
    print("- ¿Cómo se usan en aplicaciones reales?")
    print("=" * 60)

if __name__ == "__main__":
    main()
