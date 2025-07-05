# Guía Paso a Paso: Configuración desde Cero

## 🎯 Objetivo
Configurar Confluent Cloud con AWS para entender y usar **TOPICS** en streaming de datos.

## 📚 Investigación sobre TOPICS

### ¿Qué son los Topics?
Los **Topics** en Confluent/Kafka son contenedores lógicos donde se almacenan los datos. Piensa en ellos como:
- **Carpetas** donde organizas diferentes tipos de mensajes
- **Canales de comunicación** entre aplicaciones
- **Flujos de datos** específicos por categoría

### Ejemplos de Topics para tu Proyecto
1. `estudiante-actividades` - Actividades de estudiantes
2. `sistema-notificaciones` - Notificaciones del sistema
3. `logs-aplicacion` - Logs de la aplicación
4. `eventos-usuario` - Eventos de interacción del usuario

---

## 🚀 PARTE 1: Configurar Confluent Cloud

### Paso 1: Crear tu Primer Cluster
1. Ve a https://confluent.cloud
2. Haz login con tu cuenta
3. Busca el botón **"Create cluster"** o **"Crear cluster"**
4. Selecciona:
   - **Tipo**: Basic (gratis)
   - **Región**: us-east-1 (misma que AWS)
   - **Nombre**: `mi-primer-cluster`

### Paso 2: Generar API Keys
1. Una vez creado el cluster, ve a **"API Keys"**
2. Haz clic en **"Create key"** o **"+ Add key"**
3. Selecciona **"Global access"**
4. **⚠️ IMPORTANTE**: Copia y guarda:
   - API Key
   - API Secret
   (Los necesitarás para el código)

### Paso 3: Crear Topics
1. En tu cluster, ve a **"Topics"**
2. Haz clic en **"Create topic"** o **"+ Add topic"**
3. Crea estos topics:
   - Nombre: `estudiante-eventos`
   - Particiones: 1 (para empezar)
   - Retention: 7 days

4. Crea otro topic:
   - Nombre: `sistema-logs`
   - Particiones: 1
   - Retention: 7 days

---

## ☁️ PARTE 2: Configurar AWS

### Paso 1: Crear Usuario IAM
1. Ve a AWS Console → IAM
2. Usuarios → **"Agregar usuario"**
3. Nombre: `confluent-integration-user`
4. Tipo de acceso: **"Acceso mediante programación"**
5. Permisos: Agregar políticas existentes:
   - `AmazonS3FullAccess`
   - `CloudWatchFullAccess`
6. **⚠️ IMPORTANTE**: Guarda:
   - Access Key ID
   - Secret Access Key

### Paso 2: Crear Bucket S3
1. Ve a AWS Console → S3
2. **"Crear bucket"**
3. Nombre: `mi-proyecto-confluent-[tu-nombre]` (debe ser único)
4. Región: us-east-1
5. Configuración por defecto

### Paso 3: Crear Log Group en CloudWatch
1. Ve a AWS Console → CloudWatch
2. Logs → Log groups
3. **"Crear grupo de registros"**
4. Nombre: `/confluent/mi-aplicacion`

---

## 💻 PARTE 3: Configurar el Proyecto

### Paso 1: Instalar Dependencias
```powershell
# Ejecutar en PowerShell dentro de tu carpeta del proyecto
pip install kafka-python boto3 python-dotenv
```

### Paso 2: Configurar Variables de Entorno
1. Copia el archivo `config/.env.example` a `config/.env`
2. Edita `config/.env` con tus datos:

```env
# Confluent Cloud (datos de tu cluster)
CONFLUENT_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
CONFLUENT_API_KEY=tu-api-key-aqui
CONFLUENT_API_SECRET=tu-api-secret-aqui

# AWS (datos de tu usuario IAM)
AWS_ACCESS_KEY_ID=tu-access-key-aqui
AWS_SECRET_ACCESS_KEY=tu-secret-key-aqui
AWS_REGION=us-east-1
AWS_S3_BUCKET=mi-proyecto-confluent-[tu-nombre]
AWS_CLOUDWATCH_LOG_GROUP=/confluent/mi-aplicacion

# Topics que creaste
TOPIC_USER_EVENTS=estudiante-eventos
TOPIC_SYSTEM_LOGS=sistema-logs
TOPIC_NOTIFICATIONS=notificaciones
```

---

## 🧪 PARTE 4: Probar la Integración

### Paso 1: Probar Conexiones
```powershell
# Ejecutar el script de pruebas
python test_integration.py
```

### Paso 2: Enviar Datos de Prueba
```powershell
# Ejecutar el producer
python producers/basic_producer.py
```

### Paso 3: Consumir Datos
```powershell
# En otra terminal, ejecutar el consumer
python consumers/integrated_consumer.py
```

---

## 📊 ¿Qué va a pasar?

1. **Producer** enviará mensajes a los topics en Confluent Cloud
2. **Consumer** leerá esos mensajes y los enviará a AWS
3. **S3** almacenará los datos para análisis posterior
4. **CloudWatch** mostrará logs y métricas

---

## 🔍 Para tu Investigación sobre Topics

### Preguntas que puedes responder:
1. **¿Cómo se organizan los datos en un topic?**
2. **¿Qué ventajas tienen las particiones?**
3. **¿Cómo garantizan el orden de los mensajes?**
4. **¿Qué pasa si un consumer se desconecta?**
5. **¿Cómo se escalan los topics?**

### Experimentos que puedes hacer:
1. Crear diferentes tipos de topics
2. Enviar mensajes con diferentes estructuras
3. Probar múltiples consumers
4. Analizar el rendimiento con muchos mensajes

---

## 📝 Notas Importantes

- **Topics son persistentes**: Los datos no se pierden al desconectarse
- **Escalabilidad**: Puedes agregar más particiones después
- **Orden**: Solo se garantiza dentro de cada partición
- **Consumers**: Múltiples aplicaciones pueden leer el mismo topic
- **Retention**: Los datos se mantienen por el tiempo configurado

---

## 🆘 Si algo no funciona:

1. Verifica que las credenciales estén correctas en `.env`
2. Asegúrate de que los topics existan en Confluent Cloud
3. Revisa que el bucket S3 y CloudWatch estén creados
4. Ejecuta `python test_integration.py` para diagnosticar problemas
