# ✅ CHECKLIST: Configuración AWS-Confluent desde Cero

## 📅 PLAN PARA MAÑANA

### ⏰ Tiempo estimado: 2-3 horas
### 🎯 Objetivo: Tener un sistema completo funcionando para investigar TOPICS

---

## 🔥 PARTE 1: PREPARACIÓN LOCAL (15 minutos)

### ✅ 1.1 Instalar Dependencias Python
```powershell
# Abrir PowerShell en la carpeta del proyecto
cd "c:\Users\USUARIO\OneDrive\Desktop\Ciclo_2025_I\Topicos Avanzados de Ingeneria de Sistemas\A presentar\AWS-Confluent"

# Instalar paquetes necesarios
pip install kafka-python boto3 python-dotenv
```

### ✅ 1.2 Verificar Instalación
```powershell
python -c "import kafka, boto3, dotenv; print('✅ Todas las dependencias instaladas')"
```

---

## 🌟 PARTE 2: CONFIGURAR CONFLUENT CLOUD (45 minutos)

### ✅ 2.1 Crear Cluster
1. **Ir a:** https://confluent.cloud
2. **Login** con tu cuenta
3. **Buscar:** Botón "Create cluster" o "Add cluster"
4. **Seleccionar:**
   - Tipo: **Basic** (gratuito)
   - Cloud: **Amazon Web Services**
   - Región: **us-east-1** (N. Virginia)
   - Nombre: `mi-primer-cluster`
5. **Crear cluster** (toma 5-10 minutos)

### ✅ 2.2 Generar API Keys
1. **Esperar** a que el cluster esté listo
2. **Ir a:** "Data integration" → "API keys"
3. **Click:** "Create key" o "+ Add key"
4. **Seleccionar:** "Global access"
5. **Descripción:** "Integración AWS"
6. **⚠️ IMPORTANTE:** Copiar y guardar:
   - **API Key:** (ejemplo: ABC123DEF456)
   - **API Secret:** (ejemplo: xyz789abc123...)

### ✅ 2.3 Obtener Bootstrap Servers
1. **Ir a:** "Cluster overview" o "Cluster settings"
2. **Buscar:** "Bootstrap server" o "Endpoint"
3. **Copiar:** La URL (ejemplo: pkc-xxxxx.us-east-1.aws.confluent.cloud:9092)

### ✅ 2.4 Crear Topics
1. **Ir a:** "Topics" en el menú lateral
2. **Crear 3 topics:**

   **Topic 1:**
   - Nombre: `estudiante-eventos`
   - Particiones: 1
   - Retention: 7 days
   
   **Topic 2:**
   - Nombre: `sistema-logs`
   - Particiones: 1
   - Retention: 7 days
   
   **Topic 3:**
   - Nombre: `notificaciones`
   - Particiones: 1
   - Retention: 3 days

---

## ☁️ PARTE 3: CONFIGURAR AWS (45 minutos)

### ✅ 3.1 Crear Usuario IAM
1. **Ir a:** https://console.aws.amazon.com
2. **Buscar:** "IAM" en el buscador
3. **Ir a:** Users → "Create user"
4. **Configurar:**
   - User name: `confluent-integration-user`
   - Access type: ✅ "Provide user access to the AWS Management Console"
   - Console password: Autogenerated
   - ✅ "Users must create a new password at next sign-in"
5. **Permissions:**
   - "Attach policies directly"
   - Buscar y seleccionar:
     - `AmazonS3FullAccess`
     - `CloudWatchFullAccess`
6. **Create user**
7. **⚠️ IMPORTANTE:** En la siguiente pantalla, crear "Access Keys":
   - Use case: "Application running outside AWS"
   - Copiar: Access Key ID y Secret Access Key

### ✅ 3.2 Crear Bucket S3
1. **Buscar:** "S3" en la consola AWS
2. **Click:** "Create bucket"
3. **Configurar:**
   - Bucket name: `confluent-data-[tu-nombre]` (ejemplo: confluent-data-victor)
   - Region: **us-east-1**
   - Todo lo demás: configuración por defecto
4. **Create bucket**

### ✅ 3.3 Crear CloudWatch Log Group
1. **Buscar:** "CloudWatch" en la consola AWS
2. **Ir a:** Logs → Log groups
3. **Click:** "Create log group"
4. **Configurar:**
   - Log group name: `/confluent/mi-aplicacion`
   - Retention: 7 days
5. **Create**

---

## 💻 PARTE 4: CONFIGURAR PROYECTO LOCAL (30 minutos)

### ✅ 4.1 Configurar Variables de Entorno
1. **Copiar archivo:**
   ```powershell
   copy config\.env.example config\.env
   ```

2. **Editar config\.env** con tus datos reales:
   ```env
   # Datos de Confluent Cloud (del paso 2)
   CONFLUENT_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
   CONFLUENT_API_KEY=tu-api-key-aqui
   CONFLUENT_API_SECRET=tu-api-secret-aqui
   
   # Datos de AWS (del paso 3)
   AWS_ACCESS_KEY_ID=tu-access-key-aqui
   AWS_SECRET_ACCESS_KEY=tu-secret-key-aqui
   AWS_REGION=us-east-1
   AWS_S3_BUCKET=confluent-data-[tu-nombre]
   AWS_CLOUDWATCH_LOG_GROUP=/confluent/mi-aplicacion
   
   # Topics (del paso 2.4)
   TOPIC_USER_EVENTS=estudiante-eventos
   TOPIC_SYSTEM_LOGS=sistema-logs
   TOPIC_NOTIFICATIONS=notificaciones
   ```

### ✅ 4.2 Probar Conexiones
```powershell
python test_integration.py
```
**Esperado:** Todas las pruebas deben pasar ✅

---

## 🧪 PARTE 5: PROBAR EL SISTEMA (15 minutos)

### ✅ 5.1 Enviar Datos de Prueba
```powershell
python producers/basic_producer.py
```
**Esperado:** Mensajes enviados exitosamente

### ✅ 5.2 Consumir y Procesar Datos
```powershell
# En otra terminal PowerShell
python consumers/integrated_consumer.py
```
**Esperado:** Ver mensajes siendo procesados y enviados a AWS

### ✅ 5.3 Verificar en AWS
1. **S3:** Verificar que se crearon archivos en tu bucket
2. **CloudWatch:** Verificar logs en `/confluent/mi-aplicacion`

---

## 📚 PARTE 6: INVESTIGACIÓN SOBRE TOPICS (tiempo libre)

### ✅ 6.1 Experimentar con Topics
- Enviar diferentes tipos de mensajes
- Observar cómo se organizan los datos
- Probar con múltiples consumers

### ✅ 6.2 Preguntas para tu Investigación
1. **¿Cómo garantizan los topics el orden de los mensajes?**
2. **¿Qué pasa si un consumer se desconecta y se reconecta?**
3. **¿Cómo afectan las particiones al rendimiento?**
4. **¿Cuál es la diferencia entre un topic y una cola tradicional?**
5. **¿Cómo se puede escalar un topic cuando crece el volumen de datos?**

---

## 🆘 TROUBLESHOOTING COMÚN

### Error: "Authentication failed"
- ✅ Verificar API Key y Secret en .env
- ✅ Verificar Bootstrap Servers URL

### Error: "Topic not found"
- ✅ Verificar que los topics existen en Confluent Cloud
- ✅ Verificar nombres exactos en .env

### Error: "AWS Access Denied"
- ✅ Verificar Access Key y Secret Key
- ✅ Verificar que el usuario IAM tiene las políticas correctas

### Error: "Bucket not found"
- ✅ Verificar que el bucket S3 existe
- ✅ Verificar nombre del bucket en .env

---

## 📞 CONTACTOS DE EMERGENCIA

Si algo no funciona:
1. **Revisar:** logs de error en la terminal
2. **Verificar:** que todos los servicios estén creados en las consolas web
3. **Probar:** ejecutar `python test_integration.py` para diagnóstico
4. **Comparar:** tu archivo .env con el .env.example

---

## 🎯 OBJETIVO FINAL

Al terminar tendrás:
- ✅ Un cluster Confluent Cloud funcionando
- ✅ Topics creados y operativos
- ✅ Integración completa con AWS S3 y CloudWatch
- ✅ Código Python que demuestra streaming de datos
- ✅ Material para investigar cómo funcionan los TOPICS

**¡Buena suerte mañana! 🚀**
