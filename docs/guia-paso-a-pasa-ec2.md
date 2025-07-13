# Guía Paso a Paso: Ejecutar Producer y Consumer en EC2

## 1. Crear una instancia EC2

1. Ingresa a la consola de AWS y busca "EC2".
2. Haz clic en "Launch Instance".
3. Elige una AMI (Amazon Linux 2, Ubuntu, etc.).
4. Selecciona el tipo de instancia (t2.micro para pruebas).
5. Configura el almacenamiento y red (puedes dejar los valores por defecto).
6. Crea o selecciona un par de llaves (key pair) para acceso SSH.
7. Lanza la instancia.

## 2. Conectarse a la instancia EC2

1. Ve a "Instances" y selecciona tu instancia.
2. Haz clic en "Connect" y sigue las instrucciones para conectarte por SSH.
   - Ejemplo desde terminal:
     ```bash
     ssh -i "tu-key.pem" ec2-user@<ip-publica>
     ```

## 3. Instalar dependencias en EC2

1. Actualiza el sistema:
   ```bash
   sudo yum update -y   # Amazon Linux
   sudo apt update      # Ubuntu
   ```
2. Instala Python 3 y pip:
   ```bash
   sudo yum install python3 -y
   sudo apt install python3-pip -y
   ```
3. Instala las librerías necesarias:
   ```bash
   pip3 install kafka-python boto3 python-dotenv
   ```

## 4. Subir los scripts y el archivo .env

1. Usa SCP, SFTP o copia manualmente los archivos:
   - `basic_producer.py`
   - `basic_consumer.py`
   - `config/.env`
2. Ejemplo con SCP:
   ```bash
   scp -i "tu-key.pem" basic_producer.py ec2-user@<ip-publica>:/home/ec2-user/
   scp -i "tu-key.pem" basic_consumer.py ec2-user@<ip-publica>:/home/ec2-user/
   scp -i "tu-key.pem" .env ec2-user@<ip-publica>:/home/ec2-user/
   ```

## 5. Ejecutar los scripts en EC2

1. En la terminal de la instancia:
   ```bash
   python3 basic_producer.py
   python3 basic_consumer.py
   ```
2. Verifica que los logs y resultados sean correctos.

## 6. (Opcional) Automatizar con systemd o supervisord

Puedes configurar los scripts para que se ejecuten automáticamente al iniciar la instancia.

## 7. Seguridad y recomendaciones

- No compartas tu archivo .env ni tus llaves privadas.
- Usa roles IAM para mayor seguridad si el proyecto escala.
- Monitorea el uso y los logs desde AWS CloudWatch.

---
¡Listo! Ahora tu producer y consumer corren en la nube usando EC2.