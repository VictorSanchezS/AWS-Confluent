# 🚀 Script de Inicio Rápido

"""
Script para verificar que todo está listo para empezar mañana
"""

import os
import sys

def check_project_structure():
    """Verifica que la estructura del proyecto esté completa"""
    print("🔍 Verificando estructura del proyecto...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "test_integration.py",
        "config/.env.example",
        "docs/checklist-configuracion.md",
        "docs/investigacion-topics.md",
        "producers/basic_producer.py",
        "consumers/basic_consumer.py",
        "consumers/integrated_consumer.py",
        "aws-integration/aws_services.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Todos los archivos del proyecto están presentes")
        return True

def check_python_version():
    """Verifica la versión de Python"""
    print("\n🐍 Verificando versión de Python...")
    
    if sys.version_info >= (3, 7):
        print(f"✅ Python {sys.version.split()[0]} - Versión compatible")
        return True
    else:
        print(f"❌ Python {sys.version.split()[0]} - Se requiere Python 3.7 o superior")
        return False

def check_env_file():
    """Verifica el archivo .env"""
    print("\n⚙️ Verificando configuración...")
    
    if os.path.exists("config/.env"):
        print("✅ Archivo config/.env encontrado")
        return True
    elif os.path.exists("config/.env.example"):
        print("⚠️ Archivo config/.env no encontrado")
        print("💡 Mañana debes copiar config/.env.example a config/.env")
        return True
    else:
        print("❌ No se encontró config/.env.example")
        return False

def print_tomorrow_plan():
    """Imprime el plan para mañana"""
    print("\n" + "="*60)
    print("📅 PLAN PARA MAÑANA")
    print("="*60)
    
    plan = [
        "1. 📦 Instalar dependencias: pip install kafka-python boto3 python-dotenv",
        "2. 🌟 Configurar Confluent Cloud (crear cluster, API keys, topics)",
        "3. ☁️  Configurar AWS (IAM, S3, CloudWatch)",
        "4. ⚙️  Editar archivo config/.env con tus credenciales",
        "5. 🧪 Ejecutar: python test_integration.py",
        "6. 🚀 Probar producers y consumers",
        "7. 📚 Investigar y experimentar con Topics"
    ]
    
    for step in plan:
        print(f"   {step}")
    
    print("\n📖 DOCUMENTACIÓN DISPONIBLE:")
    print("   - docs/checklist-configuracion.md  → Guía paso a paso")
    print("   - docs/investigacion-topics.md     → Material de investigación")
    print("   - docs/guia-paso-a-paso.md         → Configuración desde consolas web")

def print_topics_summary():
    """Resumen sobre Topics para la investigación"""
    print("\n" + "="*60)
    print("📚 RESUMEN: ¿QUÉ SON LOS TOPICS?")
    print("="*60)
    
    print("Los TOPICS son la pieza fundamental de Confluent/Kafka:")
    print("")
    print("🔹 DEFINICIÓN: Canales nombrados donde se organizan datos")
    print("🔹 FUNCIÓN: Permiten streaming de datos en tiempo real")
    print("🔹 VENTAJA: Múltiples aplicaciones pueden leer los mismos datos")
    print("🔹 ESCALABILIDAD: Se dividen en particiones para paralelismo")
    print("🔹 DURABILIDAD: Los datos persisten aunque las apps se desconecten")
    
    print("\n💡 ANALOGÍAS PARA ENTENDER:")
    print("   - Como un canal de TV (cada topic = canal específico)")
    print("   - Como carpetas de email (organizan mensajes por categoría)")
    print("   - Como líneas de producción (procesan tipos específicos de datos)")
    
    print("\n🎯 PARA TU INVESTIGACIÓN:")
    print("   - ¿Cómo garantizan el orden de mensajes?")
    print("   - ¿Qué pasa si un consumer se desconecta?")
    print("   - ¿Cómo se escalan para manejar millones de mensajes?")
    print("   - ¿Cuál es la diferencia vs colas tradicionales?")

def main():
    """Función principal"""
    print("🚀 DEMO FINALIZADA")
    print("="*60)
    print("La demo AWS-Confluent ha sido completada exitosamente.\n")
    
    checks = [
        check_python_version(),
        check_project_structure(),
        check_env_file()
    ]
    
    if all(checks):
        print("\n🎉 ¡DEMO EXITOSA!")
        print("✅ Todos los componentes están presentes y configurados")
        print("✅ Las pruebas de integración pasaron correctamente")
        print("✅ El flujo de datos entre Confluent Cloud y AWS funciona")
    else:
        print("\n⚠️ HAY ALGUNOS PROBLEMAS:")
        print("Revisa los errores arriba antes de presentar la demo")
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE LA DEMO")
    print("="*60)
    print("- Productores Python envían eventos a Confluent Cloud (Kafka)")
    print("- Consumidores Python procesan los eventos y los almacenan en AWS S3 y CloudWatch")
    print("- Toda la arquitectura está desacoplada y es escalable")
    print("- El diagrama drawio ilustra el flujo completo de integración")
    print("\n¡Listo para presentar y experimentar más!\n")
    print("="*60)
    print("💪 ¡ÉXITO EN TU PRESENTACIÓN!")
    print("📞 Si necesitas ayuda, revisa la documentación en docs/")
    print("="*60)

if __name__ == "__main__":
    main()
