# Guía de Configuración - Confluent Cloud + AWS

## 1. Configuración de Confluent Cloud

### Paso 1: Crear un Cluster
1. Ir a [Confluent Cloud Console](https://confluent.cloud)
2. Crear un nuevo cluster:
   - **Tipo**: Basic (gratis hasta cierto límite)
   - **Región**: Elegir la misma región que tus recursos AWS
   - **Nombre**: `aws-integration-cluster`

### Paso 2: Generar API Keys
1. En el cluster, ir a "API Keys"
2. Crear una nueva API Key:
   - **Scope**: Global access (para empezar)
   - **Descripción**: `aws-integration-key`
3. **⚠️ IMPORTANTE**: Guardar la API Key y Secret en un lugar seguro

### Paso 3: Crear Topics
1. Ir a "Topics" en el cluster
2. Crear topics básicos:
   - `user-events`: Para eventos de usuario
   - `system-logs`: Para logs del sistema
   - `notifications`: Para notificaciones

## 2. Configuración de AWS

### Paso 1: IAM (Identity and Access Management)
1. Crear un usuario IAM para Confluent:
   - Nombre: `confluent-integration-user`
   - Acceso: Programmatic access
   - Políticas: `AmazonS3FullAccess`, `CloudWatchFullAccess`

### Paso 2: S3 Bucket
1. Crear bucket para almacenar datos:
   - Nombre: `confluent-data-lake-[tu-nombre]`
   - Región: Misma que Confluent cluster

### Paso 3: CloudWatch
1. Configurar grupo de logs:
   - Nombre: `/confluent/application-logs`

## 3. Variables de Entorno

Crear archivo `.env` con tus credenciales:

```env
# Confluent Cloud
CONFLUENT_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
CONFLUENT_API_KEY=tu-api-key
CONFLUENT_API_SECRET=tu-api-secret
CONFLUENT_SCHEMA_REGISTRY_URL=https://psrc-xxxxx.us-east-1.aws.confluent.cloud
CONFLUENT_SCHEMA_REGISTRY_API_KEY=tu-sr-api-key
CONFLUENT_SCHEMA_REGISTRY_API_SECRET=tu-sr-api-secret

# AWS
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=confluent-data-lake-[tu-nombre]
```

## 4. Verificación de Configuración

### Verificar Confluent Cloud
```bash
# Usando Confluent CLI
confluent login
confluent environment list
confluent kafka cluster list
```

### Verificar AWS
```bash
# Usando AWS CLI
aws sts get-caller-identity
aws s3 ls
```

## 5. Primeros Pasos

1. **Instalar dependencias**
2. **Configurar variables de entorno**
3. **Ejecutar producer de ejemplo**
4. **Ejecutar consumer de ejemplo**
5. **Verificar datos en Confluent Cloud Console**

## Troubleshooting

### Errores Comunes

1. **Authentication failed**
   - Verificar API Keys
   - Verificar bootstrap servers URL

2. **Topic not found**
   - Verificar que el topic existe
   - Verificar permisos de la API Key

3. **AWS Connection failed**
   - Verificar credenciales AWS
   - Verificar políticas IAM

## Recursos Adicionales

- [Confluent Cloud Quickstart](https://docs.confluent.io/cloud/current/get-started/index.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Kafka Fundamentals](https://developer.confluent.io/learn-kafka/)
