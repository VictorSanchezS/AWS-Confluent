# 🎨 Guía Detallada para Diagrama en Draw.io

## 📐 **Configuración del Lienzo**

### **Tamaño y Orientación:**
- **Formato**: A4 Horizontal (Landscape)
- **Tamaño**: 297 x 210 mm
- **Márgenes**: 1 cm en todos los lados
- **Grid**: Activado (ayuda a alinear elementos)

---

## 🎨 **Elementos y Formas a Usar**

### **Librería de Íconos:**
1. **AWS Architecture Icons** (buscar "aws" en símbolos)
2. **Microsoft Azure Icons** (para íconos genéricos de cloud)
3. **Cisco Network Icons** (para conectividad)

### **Formas Básicas:**
- **Rectángulos redondeados**: Para servicios principales
- **Rectángulos normales**: Para componentes específicos
- **Círculos**: Para eventos/datos
- **Nubes**: Para servicios cloud
- **Cilindros**: Para bases de datos/storage

---

## 🎨 **Layout del Diagrama (Izquierda a Derecha)**

### **Columna 1: Fuentes de Datos (X: 0-80)**
```
📱 Aplicación Web Estudiantil
   ↓ (flecha gruesa)
👥 Eventos de Usuario
   ↓ (flecha gruesa)
🖥️ Sistema de Gestión Académica
   ↓ (flecha gruesa)
📊 Logs del Sistema
```

**Elementos Draw.io:**
- **Forma**: Rectángulo redondeado
- **Color**: Verde (#4CAF50)
- **Tamaño**: 150x60 px cada uno
- **Espaciado**: 40px entre elementos

### **Columna 2: Producers (X: 100-180)**
```
🐍 Python Producer
   ↓ (flecha)
📤 Kafka Producer API
   ↓ (flecha)
🔄 Data Serialization
```

**Elementos Draw.io:**
- **Forma**: Hexágono
- **Color**: Azul claro (#2196F3)
- **Tamaño**: 120x80 px
- **Función**: Transformación de datos

### **Columna 3: Confluent Cloud (X: 200-360)**
```
🌐 Confluent Cloud
├── 📂 Topic: estudiante-eventos
├── 📂 Topic: sistema-logs
├── 📂 Topic: notificaciones
└── 🔧 Schema Registry
```

**Elementos Draw.io:**
- **Forma Principal**: Nube grande
- **Color**: Naranja (#FF9800)
- **Tamaño**: 200x150 px
- **Sub-elementos**: Rectángulos dentro de la nube
- **Topics**: Rectángulos pequeños (100x30 px)

### **Columna 4: Consumers (X: 380-460)**
```
🐍 Python Consumer
   ↓ (flecha)
📥 Kafka Consumer API
   ↓ (flecha)
🔄 Data Processing
```

**Elementos Draw.io:**
- **Forma**: Hexágono
- **Color**: Morado (#9C27B0)
- **Tamaño**: 120x80 px
- **Función**: Procesamiento de datos

### **Columna 5: AWS Services (X: 480-650)**
```
☁️ AWS
├── 🪣 S3 Bucket (Data Lake)
├── 📊 CloudWatch (Monitoring)
├── 🚨 CloudWatch Alarms
└── 📧 SNS (Notifications)
```

**Elementos Draw.io:**
- **Forma Principal**: Rectángulo con bordes curvos
- **Color**: Azul oscuro (#1976D2)
- **Tamaño**: 200x150 px
- **Íconos AWS**: Usar íconos oficiales AWS
- **Sub-servicios**: Rectángulos pequeños

---

## 🎨 **Tipos de Conexiones**

### **Flechas Principales (Flujo de Datos):**
- **Estilo**: Flecha gruesa
- **Color**: Negro (#000000)
- **Grosor**: 3px
- **Etiqueta**: "Tiempo Real"

### **Flechas Secundarias (Configuración):**
- **Estilo**: Flecha punteada
- **Color**: Gris (#757575)
- **Grosor**: 2px
- **Etiqueta**: "Config"

### **Flechas de Alerta:**
- **Estilo**: Flecha curva
- **Color**: Rojo (#F44336)
- **Grosor**: 2px
- **Etiqueta**: "Alerta"

---

## 🎨 **Colores y Estilos**

### **Paleta de Colores:**
```
🟢 Verde (#4CAF50)    → Fuentes de datos
🔵 Azul claro (#2196F3) → Producers
🟠 Naranja (#FF9800)  → Confluent Cloud
🟣 Morado (#9C27B0)   → Consumers
🔷 Azul oscuro (#1976D2) → AWS Services
🔴 Rojo (#F44336)     → Alertas/Errores
⚫ Negro (#000000)     → Texto y flechas
```

### **Fuentes:**
- **Títulos**: Arial Bold, 14px
- **Subtítulos**: Arial, 12px
- **Etiquetas**: Arial, 10px
- **Descripciones**: Arial, 9px

---

## 🎨 **Paso a Paso en Draw.io**

### **Paso 1: Configuración Inicial**
1. Abrir Draw.io
2. Seleccionar "Create New Diagram"
3. Elegir template "Blank Diagram"
4. Configurar página: Format → Page Setup → A4 Landscape

### **Paso 2: Crear Fuentes de Datos**
1. Insertar rectángulo redondeado
2. Cambiar color a verde (#4CAF50)
3. Agregar texto: "Aplicación Web Estudiantil"
4. Duplicar para otros 3 elementos
5. Alinear verticalmente

### **Paso 3: Crear Confluent Cloud**
1. Insertar forma "Nube" (buscar en símbolos)
2. Cambiar color a naranja (#FF9800)
3. Agregar texto: "Confluent Cloud"
4. Insertar rectángulos pequeños dentro
5. Etiquetar como topics

### **Paso 4: Crear AWS Services**
1. Buscar "AWS" en símbolos
2. Insertar íconos oficiales:
   - AWS S3
   - AWS CloudWatch
   - AWS SNS
3. Agrupar en contenedor azul

### **Paso 5: Conectar con Flechas**
1. Seleccionar herramienta "Connector"
2. Conectar elementos de izquierda a derecha
3. Cambiar estilo de flechas según tipo
4. Agregar etiquetas a conexiones importantes

### **Paso 6: Agregar Detalles**
1. Títulos y subtítulos
2. Leyenda de colores
3. Indicadores de rendimiento
4. Anotaciones importantes

---

## 🎨 **Elementos Específicos a Incluir**

### **Título Principal:**
```
"Arquitectura AWS-Confluent: Streaming de Datos Estudiantiles"
- Fuente: Arial Bold, 18px
- Posición: Centrado en la parte superior
- Color: Negro (#000000)
```

### **Leyenda:**
```
🟢 Fuentes de Datos
🔵 Producers
🟠 Confluent Cloud
🟣 Consumers  
🔷 AWS Services
🔴 Alertas
```

### **Métricas de Rendimiento:**
```
📊 Throughput: 10,000 msgs/sec
⏱️ Latencia: < 5ms
📈 Escalabilidad: Auto-scaling
🛡️ Disponibilidad: 99.9%
```

### **Flujo Numerado:**
```
1️⃣ Generación de Eventos
2️⃣ Producción a Topics
3️⃣ Streaming en Confluent
4️⃣ Consumo y Procesamiento
5️⃣ Almacenamiento en AWS
```

---

## 🎨 **Capas del Diagrama (Layers)**

### **Layer 1: Fondo y Grid**
- Color de fondo: Blanco (#FFFFFF)
- Grid: Visible durante edición

### **Layer 2: Contenedores Principales**
- Nubes y rectángulos grandes
- Agrupaciones de servicios

### **Layer 3: Servicios Específicos**
- Íconos individuales
- Componentes detallados

### **Layer 4: Conexiones**
- Flechas y conectores
- Flujo de datos

### **Layer 5: Texto y Etiquetas**
- Títulos y descripciones
- Anotaciones y métricas

---

## 🎨 **Elementos Opcionales Avanzados**

### **Animaciones (si Draw.io las soporta):**
- Pulso en los puntos de datos
- Movimiento en las flechas
- Highlight de componentes activos

### **Iconografía Adicional:**
- 🔒 Seguridad en conexiones
- ⚡ Velocidad en procesamiento
- 📊 Gráficos de métricas
- 🔄 Símbolos de alta disponibilidad

### **Notas Técnicas:**
- Versiones de software
- Configuraciones específicas
- Limitaciones conocidas
- Requisitos de red

---

## 🎯 **Checklist Final**

### **Antes de Exportar:**
- [ ] Todos los elementos están alineados
- [ ] Colores son consistentes
- [ ] Texto es legible
- [ ] Flechas conectan correctamente
- [ ] Leyenda está completa
- [ ] Título es claro

### **Formatos de Exportación:**
- [ ] PNG (alta resolución) para presentación
- [ ] PDF para documentación
- [ ] SVG para web/edición futura
- [ ] Draw.io (.drawio) para backup

¡Con esta guía tendrás un diagrama profesional y claro! 🚀
