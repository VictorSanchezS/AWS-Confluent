"""
Script de prueba completo para validar la integración AWS-Confluent
Ejecuta productores y consumidores de ejemplo para verificar que todo funciona
"""

import os
import sys
import time
import threading
import json
from datetime import datetime

# Agregar rutas al path
sys.path.append('producers')
sys.path.append('consumers')
sys.path.append('aws-integration')

from dotenv import load_dotenv
from basic_producer import ConfluentProducer
from aws_services import AWSIntegration

# Cargar variables de entorno
load_dotenv(dotenv_path='config/.env')

class TestRunner:
    def __init__(self):
        """Inicializa el runner de pruebas"""
        self.producer = None
        self.aws_integration = None
        self.test_results = []
        self.topic_name = os.getenv("KAFKA_TOPIC", "demo-topic")
    
    def setup(self):
        """Configura los componentes para las pruebas"""
        print("🔧 Configurando componentes para las pruebas...")
        
        try:
            # Inicializar producer
            self.producer = ConfluentProducer(self.topic_name)
            print("✅ Producer de Confluent inicializado")
            
            # Inicializar AWS
            self.aws_integration = AWSIntegration()
            print("✅ Integración AWS inicializada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en la configuración: {e}")
            return False
    
    def test_confluent_connection(self):
        """Prueba la conexión a Confluent Cloud"""
        print("\n🧪 Probando conexión a Confluent Cloud...")
        
        try:
            # Enviar mensaje de prueba
            test_message = {
                "test": True,
                "message": "Prueba de conexión a Confluent Cloud",
                "timestamp": datetime.now().isoformat()
            }
            
            success = self.producer.send_message(self.topic_name, test_message, "test-key")
            
            if success:
                print("✅ Conexión a Confluent Cloud exitosa")
                self.test_results.append(("Confluent Connection", "PASS"))
                return True
            else:
                print("❌ Fallo en la conexión a Confluent Cloud")
                self.test_results.append(("Confluent Connection", "FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ Error probando Confluent: {e}")
            self.test_results.append(("Confluent Connection", "ERROR"))
            return False
    
    def test_aws_s3(self):
        """Prueba la conexión a AWS S3"""
        print("\n🧪 Probando conexión a AWS S3...")
        
        try:
            # Datos de prueba
            test_data = {
                "test": True,
                "message": "Prueba de conexión a AWS S3",
                "timestamp": datetime.now().isoformat()
            }
            
            # Almacenar en S3
            success = self.aws_integration.store_data_in_s3(
                test_data, 
                f"test/connection-test-{int(time.time())}.json"
            )
            
            if success:
                print("✅ Conexión a AWS S3 exitosa")
                self.test_results.append(("AWS S3", "PASS"))
                return True
            else:
                print("❌ Fallo en la conexión a AWS S3")
                self.test_results.append(("AWS S3", "FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ Error probando AWS S3: {e}")
            self.test_results.append(("AWS S3", "ERROR"))
            return False
    
    def test_aws_cloudwatch(self):
        """Prueba la conexión a AWS CloudWatch"""
        print("\n🧪 Probando conexión a AWS CloudWatch...")
        
        try:
            # Enviar log de prueba
            test_log = f"Prueba de conexión a CloudWatch - {datetime.now().isoformat()}"
            success_logs = self.aws_integration.send_to_cloudwatch_logs(test_log, "test-stream")
            
            # Enviar métrica de prueba
            success_metrics = self.aws_integration.send_metric_to_cloudwatch("TestConnection", 1.0)
            
            if success_logs and success_metrics:
                print("✅ Conexión a AWS CloudWatch exitosa")
                self.test_results.append(("AWS CloudWatch", "PASS"))
                return True
            else:
                print("❌ Fallo en la conexión a AWS CloudWatch")
                self.test_results.append(("AWS CloudWatch", "FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ Error probando AWS CloudWatch: {e}")
            self.test_results.append(("AWS CloudWatch", "ERROR"))
            return False
    
    def test_end_to_end_flow(self):
        """Prueba el flujo completo: Confluent -> AWS"""
        print("\n🧪 Probando flujo end-to-end...")
        
        try:
            # 1. Enviar evento de usuario
            user_event = {
                "user_id": "test_user_123",
                "event_type": "test_login",
                "data": {
                    "ip": "127.0.0.1",
                    "device": "test",
                    "browser": "test-browser"
                }
            }
            
            success1 = self.producer.send_user_event(
                user_event["user_id"],
                user_event["event_type"],
                user_event["data"]
            )
            
            if not success1:
                print("❌ Fallo enviando evento de usuario")
                self.test_results.append(("End-to-End Flow", "FAIL"))
                return False
            
            # 2. Procesar con AWS
            # Simulamos lo que haría el consumer
            success2 = self.aws_integration.process_user_event_to_aws(user_event)
            
            if not success2:
                print("❌ Fallo procesando en AWS")
                self.test_results.append(("End-to-End Flow", "FAIL"))
                return False
            
            # 3. Enviar log del sistema
            log_data = {
                "level": "INFO",
                "service": "test-service",
                "message": "Prueba de log del sistema",
                "timestamp": datetime.now().isoformat()
            }
            
            success3 = self.producer.send_system_log(
                log_data["level"],
                log_data["message"],
                log_data["service"]
            )
            
            success4 = self.aws_integration.process_system_log_to_aws(log_data)
            
            if success3 and success4:
                print("✅ Flujo end-to-end exitoso")
                self.test_results.append(("End-to-End Flow", "PASS"))
                return True
            else:
                print("❌ Fallo en el flujo end-to-end")
                self.test_results.append(("End-to-End Flow", "FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ Error en flujo end-to-end: {e}")
            self.test_results.append(("End-to-End Flow", "ERROR"))
            return False
    
    def run_performance_test(self):
        """Ejecuta una prueba de rendimiento básica"""
        print("\n🧪 Ejecutando prueba de rendimiento...")
        
        try:
            message_count = 10
            start_time = time.time()
            
            for i in range(message_count):
                test_message = {
                    "id": i,
                    "message": f"Mensaje de prueba #{i}",
                    "timestamp": datetime.now().isoformat()
                }
                
                self.producer.send_message(self.topic_name, test_message, f"perf-test-{i}")
                
                if i % 5 == 0:
                    print(f"   Enviados {i+1}/{message_count} mensajes...")
            
            end_time = time.time()
            duration = end_time - start_time
            rate = message_count / duration
            
            print(f"✅ Prueba de rendimiento completada:")
            print(f"   Mensajes: {message_count}")
            print(f"   Tiempo: {duration:.2f} segundos")
            print(f"   Tasa: {rate:.2f} mensajes/segundo")
            
            self.test_results.append(("Performance Test", "PASS"))
            return True
            
        except Exception as e:
            print(f"❌ Error en prueba de rendimiento: {e}")
            self.test_results.append(("Performance Test", "ERROR"))
            return False
    
    def print_summary(self):
        """Imprime un resumen de los resultados"""
        print("\n" + "="*60)
        print("📊 RESUMEN DE PRUEBAS")
        print("="*60)
        
        passed = 0
        failed = 0
        errors = 0
        
        for test_name, result in self.test_results:
            status_icon = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
            print(f"{status_icon} {test_name}: {result}")
            
            if result == "PASS":
                passed += 1
            elif result == "FAIL":
                failed += 1
            else:
                errors += 1
        
        print(f"\n📈 Resultados:")
        print(f"   ✅ Exitosas: {passed}")
        print(f"   ❌ Fallidas: {failed}")
        print(f"   ⚠️  Errores: {errors}")
        print(f"   📊 Total: {len(self.test_results)}")
        
        if failed == 0 and errors == 0:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            print("Tu integración AWS-Confluent está funcionando correctamente.")
        else:
            print("\n⚠️  Algunas pruebas fallaron.")
            print("Revisa la configuración y las credenciales.")
    
    def cleanup(self):
        """Limpia los recursos"""
        print("\n🧹 Limpiando recursos...")
        
        if self.producer:
            self.producer.close()
        
        print("✅ Limpieza completada")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN AWS-CONFLUENT")
        print("="*60)
        print("🔎 Estado actual de variables AWS:")
        print(f"   AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
        print(f"   AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY')}")
        print(f"   AWS_REGION: {os.getenv('AWS_REGION')}")
        print(f"   AWS_S3_BUCKET: {os.getenv('AWS_S3_BUCKET')}")
        print(f"   AWS_CLOUDWATCH_LOG_GROUP: {os.getenv('AWS_CLOUDWATCH_LOG_GROUP')}")
        
        if not self.setup():
            print("❌ Fallo en la configuración inicial. Abortando pruebas.")
            return
        
        try:
            # Ejecutar pruebas
            self.test_confluent_connection()
            time.sleep(1)
            
            self.test_aws_s3()
            time.sleep(1)
            
            self.test_aws_cloudwatch()
            time.sleep(1)
            
            self.test_end_to_end_flow()
            time.sleep(1)
            
            self.run_performance_test()
            
        finally:
            self.cleanup()
            self.print_summary()

def main():
    """Función principal"""
    # Verificar que el archivo .env existe
    if not os.path.exists('config/.env'):
        print("❌ Archivo config/.env no encontrado")
        print("💡 Copia config/.env.example a config/.env y completa las credenciales")
        return
    
    # Ejecutar pruebas
    test_runner = TestRunner()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()
