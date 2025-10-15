# 🌱 Sistema de Detección de Mosca Blanca

Sistema inteligente para la detección automática de infestaciones de mosca blanca en cultivos usando visión por computadora y redes neuronales convolucionales.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Configuración del Backend](#configuración-del-backend)
- [Configuración del Frontend](#configuración-del-frontend)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 📖 Descripción

Este proyecto utiliza técnicas de machine learning para detectar y clasificar infestaciones de mosca blanca en cultivos agrícolas. El sistema puede identificar tres estados diferentes:

- 🟢 **Sin plaga**: Planta saludable
- 🟡 **Infestación leve**: Presencia mínima de mosca blanca
- 🔴 **Infestación severa**: Alta concentración de mosca blanca

## ✨ Características

- 🤖 **IA Avanzada**: Modelo basado en MobileNetV2 con transfer learning
- 📱 **Aplicación Móvil**: Frontend desarrollado en Flutter
- 🚀 **API REST**: Backend en FastAPI con documentación automática
- 📊 **Análisis en Tiempo Real**: Procesamiento rápido de imágenes
- 🎯 **Alta Precisión**: Modelo entrenado con técnicas de data augmentation
- 📈 **Métricas Detalladas**: Logging y monitoreo del rendimiento
- 🐳 **Docker Support**: Contenedorización para fácil despliegue

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Flutter App    │◄──►│  FastAPI        │◄──►│  TensorFlow     │
│  (Frontend)     │    │  (Backend)      │    │  Model          │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 💻 Requisitos del Sistema

### Requisitos Generales
- **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Linux (Ubuntu 18.04+)
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Almacenamiento**: 5GB de espacio libre
- **Internet**: Conexión estable para descargar dependencias

### Backend (Python)
- **Python**: 3.9 - 3.13
- **pip**: Incluido con Python
- **Entorno virtual**: Recomendado (venv o conda)

### Frontend (Flutter)
- **Flutter SDK**: 3.8.1+
- **Dart SDK**: 3.8.1+
- **Android Studio** (para desarrollo Android)
- **Xcode** (para desarrollo iOS, solo macOS)

## 🚀 Instalación

### Método Rápido (Recomendado)

El proyecto incluye scripts de instalación automática:

#### En Linux/macOS:
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/whitefly-detector.git
cd whitefly-detector

# Dar permisos de ejecución
chmod +x start.sh

# Ejecutar instalación completa
./start.sh
```

#### En Windows:
```cmd
# Clonar el repositorio
git clone https://github.com/tu-usuario/whitefly-detector.git
cd whitefly-detector

# Ejecutar instalación completa
start.bat
```

### Instalación Manual

Si prefieres instalar manualmente o necesitas más control:

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/whitefly-detector.git
cd whitefly-detector
```

#### 2. Configurar Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurar Frontend
```bash
cd frontend

# Instalar dependencias de Flutter
flutter pub get

# Verificar instalación
flutter doctor
```

## ⚙️ Configuración del Backend

### 1. Estructura de Directorios

El script de instalación crea automáticamente la estructura necesaria, pero si instalas manualmente:

```bash
cd backend

# Crear directorios necesarios
mkdir -p models logs uploads
mkdir -p dataset/{train,val,test}/{sin_plaga,infestacion_leve,infestacion_severa}
```

### 2. Variables de Entorno

Crea un archivo `.env` en el directorio `backend/`:

```bash
# backend/.env
DEBUG=True
MODEL_PATH=models/whitefly_detector.h5
UPLOAD_DIR=uploads
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png
```

### 3. Preparar Dataset (Opcional)

Si quieres entrenar tu propio modelo:

```bash
# Organizar imágenes en la estructura:
dataset/
├── train/
│   ├── sin_plaga/          # Imágenes de plantas sanas
│   ├── infestacion_leve/   # Imágenes con infestación leve
│   └── infestacion_severa/ # Imágenes con infestación severa
├── val/
│   ├── sin_plaga/
│   ├── infestacion_leve/
│   └── infestacion_severa/
└── test/
    ├── sin_plaga/
    ├── infestacion_leve/
    └── infestacion_severa/
```

### 4. Entrenar Modelo (Opcional)

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Entrenar modelo
python train_model.py
```

### 5. Iniciar Backend

```bash
# Desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

El backend estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 📱 Configuración del Frontend

### 1. Verificar Instalación de Flutter

```bash
flutter doctor
```

Asegúrate de que todos los checks estén en ✅ verde.

### 2. Configurar Conexión con Backend

Edita el archivo de configuración para apuntar a tu backend:

```dart
// lib/config/api_config.dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000';  // Para desarrollo local
  // static const String baseUrl = 'http://TU_SERVIDOR:8000';  // Para producción
  
  static const String detectEndpoint = '/detect';
  static const int timeoutSeconds = 30;
}
```

### 3. Instalar Dependencias

```bash
cd frontend
flutter pub get
```

### 4. Ejecutar la Aplicación

#### Para Desarrollo Web:
```bash
flutter run -d web-server --web-port 3000
```

#### Para Android:
```bash
# Conectar dispositivo Android o iniciar emulador
flutter devices

# Ejecutar en dispositivo
flutter run
```

#### Para iOS (solo macOS):
```bash
# Abrir simulador iOS
open -a Simulator

# Ejecutar en simulador
flutter run
```

#### Para Desktop:
```bash
# Windows
flutter run -d windows

# macOS
flutter run -d macos

# Linux
flutter run -d linux
```

## 🎯 Uso

### 1. Iniciar el Sistema Completo

#### Usando Scripts de Inicio:
```bash
# Linux/macOS
./start.sh

# Windows
start.bat
```

Selecciona la opción 5 para iniciar el servidor backend.

#### Manualmente:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/macOS
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
flutter run -d web-server --web-port 3000
```

### 2. Probar la API

#### Usando curl:
```bash
# Subir imagen para análisis
curl -X POST "http://localhost:8000/detect" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@ruta/a/tu/imagen.jpg"
```

#### Usando la documentación interactiva:
Visita http://localhost:8000/docs

### 3. Usar la Aplicación

1. Abre la aplicación en tu dispositivo/navegador
2. Toca el botón de cámara o selecciona una imagen
3. Espera el análisis automático
4. Revisa los resultados y recomendaciones

## 📡 API Endpoints

### POST `/detect`
Analiza una imagen para detectar infestación de mosca blanca.

**Parámetros:**
- `file`: Imagen en formato JPG, JPEG o PNG (máx. 10MB)

**Respuesta:**
```json
{
  "prediction": "infestacion_leve",
  "confidence": 0.85,
  "probabilities": {
    "sin_plaga": 0.05,
    "infestacion_leve": 0.85,
    "infestacion_severa": 0.10
  },
  "processing_time": 1.23,
  "timestamp": "2024-01-15T10:30:00Z",
  "recommendations": [
    "Implementar monitoreo regular",
    "Considerar tratamiento preventivo"
  ]
}
```

### GET `/health`
Verifica el estado del servicio.

### GET `/model/info`
Obtiene información sobre el modelo actual.

## 🧠 Entrenamiento del Modelo

### 1. Preparar Dataset

```bash
# Estructura requerida:
dataset/
├── train/ (70% de los datos)
├── val/   (20% de los datos)
└── test/  (10% de los datos)
```

### 2. Configurar Entrenamiento

Edita `backend/train_model.py` para ajustar hiperparámetros:

```python
# Configuración de entrenamiento
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
```

### 3. Ejecutar Entrenamiento

```bash
cd backend
python train_model.py
```

### 4. Monitorear Progreso

Los logs y métricas se guardan en:
- `logs/training_YYYYMMDD_HHMMSS.log`
- `logs/tensorboard/` (visualizar con TensorBoard)

## 🐳 Docker (Opcional)

### Construcción y Ejecución

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build

# Solo backend
docker build -t whitefly-backend ./backend
docker run -p 8000:8000 whitefly-backend

# Solo frontend
docker build -t whitefly-frontend ./frontend
docker run -p 3000:3000 whitefly-frontend
```

## 📁 Estructura del Proyecto

```
whitefly-detector/
├── 📄 README.md
├── 🚀 start.sh / start.bat
├── 🐳 docker-compose.yml
├── 📊 backend/
│   ├── 🔧 main.py              # API principal
│   ├── 🧠 train_model.py       # Entrenamiento del modelo
│   ├── 🛠️ utils.py             # Utilidades
│   ├── 📦 requirements.txt     # Dependencias Python
│   ├── 🗂️ dataset/            # Datos de entrenamiento
│   ├── 🤖 models/             # Modelos entrenados
│   └── 📋 logs/               # Archivos de log
├── 📱 frontend/
│   ├── 🎯 lib/                # Código fuente Flutter
│   ├── 🤖 android/            # Configuración Android
│   ├── 🍎 ios/                # Configuración iOS
│   ├── 🖥️ web/                # Recursos web
│   └── 📦 pubspec.yaml        # Dependencias Flutter
└── 📚 docs/
    └── 📖 PROYECTO MODIFICADO.docx
```

## 🔧 Solución de Problemas

### Problemas Comunes

#### Backend no inicia:
```bash
# Verificar Python
python --version

# Verificar dependencias
pip list

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### Frontend no compila:
```bash
# Limpiar cache
flutter clean
flutter pub get

# Verificar configuración
flutter doctor
```

#### Modelo no encontrado:
```bash
# Verificar si existe el modelo
ls -la backend/models/

# Entrenar nuevo modelo
cd backend && python train_model.py
```

### Logs y Debugging

- **Backend logs**: `backend/logs/`
- **Frontend logs**: Consola del navegador/IDE
- **API logs**: Terminal donde corre uvicorn

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- TensorFlow y Keras por las herramientas de ML
- Flutter por el framework móvil
- FastAPI por el framework web
- La comunidad open source por las librerías utilizadas

---

**💡 Tip**: Para soporte técnico, abre un issue en GitHub o consulta la documentación de la API en `/docs`.


```bash
============================================================
🌱 SISTEMA DE DETECCIÓN DE MOSCA BLANCA - ENTRENAMIENTO
============================================================
Found 1680 images belonging to 3 classes.
Found 1506 images belonging to 3 classes.
Found 846 images belonging to 3 classes.

📊 Distribución del dataset:
   Entrenamiento: 1680 imágenes
   Validación: 1506 imágenes
   Prueba: 846 imágenes

🏷️  Clases: {'infestacion_leve': 0, 'infestacion_severa': 1, 'sin_plaga': 2}
2025-10-15 16:51:10.236627: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (303)

✅ Modelo construido exitosamente
📝 Total de parámetros: 3,086,659
Model: "functional"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                  ┃ Output Shape              ┃         Param # ┃ Connected to               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ input_layer (InputLayer)      │ (None, 224, 224, 3)       │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ Conv1 (Conv2D)                │ (None, 112, 112, 32)      │             864 │ input_layer[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ bn_Conv1 (BatchNormalization) │ (None, 112, 112, 32)      │             128 │ Conv1[0][0]                │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ Conv1_relu (ReLU)             │ (None, 112, 112, 32)      │               0 │ bn_Conv1[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ expanded_conv_depthwise       │ (None, 112, 112, 32)      │             288 │ Conv1_relu[0][0]           │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ expanded_conv_depthwise_BN    │ (None, 112, 112, 32)      │             128 │ expanded_conv_depthwise[0… │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ expanded_conv_depthwise_relu  │ (None, 112, 112, 32)      │               0 │ expanded_conv_depthwise_B… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ expanded_conv_project         │ (None, 112, 112, 16)      │             512 │ expanded_conv_depthwise_r… │
│ (Conv2D)                      │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ expanded_conv_project_BN      │ (None, 112, 112, 16)      │              64 │ expanded_conv_project[0][… │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_expand (Conv2D)       │ (None, 112, 112, 96)      │           1,536 │ expanded_conv_project_BN[… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_expand_BN             │ (None, 112, 112, 96)      │             384 │ block_1_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_expand_relu (ReLU)    │ (None, 112, 112, 96)      │               0 │ block_1_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_pad (ZeroPadding2D)   │ (None, 113, 113, 96)      │               0 │ block_1_expand_relu[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_depthwise             │ (None, 56, 56, 96)        │             864 │ block_1_pad[0][0]          │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_depthwise_BN          │ (None, 56, 56, 96)        │             384 │ block_1_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_depthwise_relu (ReLU) │ (None, 56, 56, 96)        │               0 │ block_1_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_project (Conv2D)      │ (None, 56, 56, 24)        │           2,304 │ block_1_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_1_project_BN            │ (None, 56, 56, 24)        │              96 │ block_1_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_expand (Conv2D)       │ (None, 56, 56, 144)       │           3,456 │ block_1_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_expand_BN             │ (None, 56, 56, 144)       │             576 │ block_2_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_expand_relu (ReLU)    │ (None, 56, 56, 144)       │               0 │ block_2_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_depthwise             │ (None, 56, 56, 144)       │           1,296 │ block_2_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_depthwise_BN          │ (None, 56, 56, 144)       │             576 │ block_2_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_depthwise_relu (ReLU) │ (None, 56, 56, 144)       │               0 │ block_2_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_project (Conv2D)      │ (None, 56, 56, 24)        │           3,456 │ block_2_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_project_BN            │ (None, 56, 56, 24)        │              96 │ block_2_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_2_add (Add)             │ (None, 56, 56, 24)        │               0 │ block_1_project_BN[0][0],  │
│                               │                           │                 │ block_2_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_expand (Conv2D)       │ (None, 56, 56, 144)       │           3,456 │ block_2_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_expand_BN             │ (None, 56, 56, 144)       │             576 │ block_3_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_expand_relu (ReLU)    │ (None, 56, 56, 144)       │               0 │ block_3_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_pad (ZeroPadding2D)   │ (None, 57, 57, 144)       │               0 │ block_3_expand_relu[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_depthwise             │ (None, 28, 28, 144)       │           1,296 │ block_3_pad[0][0]          │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_depthwise_BN          │ (None, 28, 28, 144)       │             576 │ block_3_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_depthwise_relu (ReLU) │ (None, 28, 28, 144)       │               0 │ block_3_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_project (Conv2D)      │ (None, 28, 28, 32)        │           4,608 │ block_3_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_3_project_BN            │ (None, 28, 28, 32)        │             128 │ block_3_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_expand (Conv2D)       │ (None, 28, 28, 192)       │           6,144 │ block_3_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_expand_BN             │ (None, 28, 28, 192)       │             768 │ block_4_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_expand_relu (ReLU)    │ (None, 28, 28, 192)       │               0 │ block_4_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_depthwise             │ (None, 28, 28, 192)       │           1,728 │ block_4_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_depthwise_BN          │ (None, 28, 28, 192)       │             768 │ block_4_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_depthwise_relu (ReLU) │ (None, 28, 28, 192)       │               0 │ block_4_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_project (Conv2D)      │ (None, 28, 28, 32)        │           6,144 │ block_4_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_project_BN            │ (None, 28, 28, 32)        │             128 │ block_4_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_4_add (Add)             │ (None, 28, 28, 32)        │               0 │ block_3_project_BN[0][0],  │
│                               │                           │                 │ block_4_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_expand (Conv2D)       │ (None, 28, 28, 192)       │           6,144 │ block_4_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_expand_BN             │ (None, 28, 28, 192)       │             768 │ block_5_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_expand_relu (ReLU)    │ (None, 28, 28, 192)       │               0 │ block_5_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_depthwise             │ (None, 28, 28, 192)       │           1,728 │ block_5_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_depthwise_BN          │ (None, 28, 28, 192)       │             768 │ block_5_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_depthwise_relu (ReLU) │ (None, 28, 28, 192)       │               0 │ block_5_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_project (Conv2D)      │ (None, 28, 28, 32)        │           6,144 │ block_5_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_project_BN            │ (None, 28, 28, 32)        │             128 │ block_5_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_5_add (Add)             │ (None, 28, 28, 32)        │               0 │ block_4_add[0][0],         │
│                               │                           │                 │ block_5_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_expand (Conv2D)       │ (None, 28, 28, 192)       │           6,144 │ block_5_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_expand_BN             │ (None, 28, 28, 192)       │             768 │ block_6_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_expand_relu (ReLU)    │ (None, 28, 28, 192)       │               0 │ block_6_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_pad (ZeroPadding2D)   │ (None, 29, 29, 192)       │               0 │ block_6_expand_relu[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_depthwise             │ (None, 14, 14, 192)       │           1,728 │ block_6_pad[0][0]          │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_depthwise_BN          │ (None, 14, 14, 192)       │             768 │ block_6_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_depthwise_relu (ReLU) │ (None, 14, 14, 192)       │               0 │ block_6_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_project (Conv2D)      │ (None, 14, 14, 64)        │          12,288 │ block_6_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_6_project_BN            │ (None, 14, 14, 64)        │             256 │ block_6_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_expand (Conv2D)       │ (None, 14, 14, 384)       │          24,576 │ block_6_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_expand_BN             │ (None, 14, 14, 384)       │           1,536 │ block_7_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_expand_relu (ReLU)    │ (None, 14, 14, 384)       │               0 │ block_7_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_depthwise             │ (None, 14, 14, 384)       │           3,456 │ block_7_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_depthwise_BN          │ (None, 14, 14, 384)       │           1,536 │ block_7_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_depthwise_relu (ReLU) │ (None, 14, 14, 384)       │               0 │ block_7_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_project (Conv2D)      │ (None, 14, 14, 64)        │          24,576 │ block_7_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_project_BN            │ (None, 14, 14, 64)        │             256 │ block_7_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_7_add (Add)             │ (None, 14, 14, 64)        │               0 │ block_6_project_BN[0][0],  │
│                               │                           │                 │ block_7_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_expand (Conv2D)       │ (None, 14, 14, 384)       │          24,576 │ block_7_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_expand_BN             │ (None, 14, 14, 384)       │           1,536 │ block_8_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_expand_relu (ReLU)    │ (None, 14, 14, 384)       │               0 │ block_8_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_depthwise             │ (None, 14, 14, 384)       │           3,456 │ block_8_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_depthwise_BN          │ (None, 14, 14, 384)       │           1,536 │ block_8_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_depthwise_relu (ReLU) │ (None, 14, 14, 384)       │               0 │ block_8_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_project (Conv2D)      │ (None, 14, 14, 64)        │          24,576 │ block_8_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_project_BN            │ (None, 14, 14, 64)        │             256 │ block_8_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_8_add (Add)             │ (None, 14, 14, 64)        │               0 │ block_7_add[0][0],         │
│                               │                           │                 │ block_8_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_expand (Conv2D)       │ (None, 14, 14, 384)       │          24,576 │ block_8_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_expand_BN             │ (None, 14, 14, 384)       │           1,536 │ block_9_expand[0][0]       │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_expand_relu (ReLU)    │ (None, 14, 14, 384)       │               0 │ block_9_expand_BN[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_depthwise             │ (None, 14, 14, 384)       │           3,456 │ block_9_expand_relu[0][0]  │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_depthwise_BN          │ (None, 14, 14, 384)       │           1,536 │ block_9_depthwise[0][0]    │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_depthwise_relu (ReLU) │ (None, 14, 14, 384)       │               0 │ block_9_depthwise_BN[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_project (Conv2D)      │ (None, 14, 14, 64)        │          24,576 │ block_9_depthwise_relu[0]… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_project_BN            │ (None, 14, 14, 64)        │             256 │ block_9_project[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_9_add (Add)             │ (None, 14, 14, 64)        │               0 │ block_8_add[0][0],         │
│                               │                           │                 │ block_9_project_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_expand (Conv2D)      │ (None, 14, 14, 384)       │          24,576 │ block_9_add[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_expand_BN            │ (None, 14, 14, 384)       │           1,536 │ block_10_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_expand_relu (ReLU)   │ (None, 14, 14, 384)       │               0 │ block_10_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_depthwise            │ (None, 14, 14, 384)       │           3,456 │ block_10_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_depthwise_BN         │ (None, 14, 14, 384)       │           1,536 │ block_10_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_depthwise_relu       │ (None, 14, 14, 384)       │               0 │ block_10_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_project (Conv2D)     │ (None, 14, 14, 96)        │          36,864 │ block_10_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_10_project_BN           │ (None, 14, 14, 96)        │             384 │ block_10_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_expand (Conv2D)      │ (None, 14, 14, 576)       │          55,296 │ block_10_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_expand_BN            │ (None, 14, 14, 576)       │           2,304 │ block_11_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_expand_relu (ReLU)   │ (None, 14, 14, 576)       │               0 │ block_11_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_depthwise            │ (None, 14, 14, 576)       │           5,184 │ block_11_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_depthwise_BN         │ (None, 14, 14, 576)       │           2,304 │ block_11_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_depthwise_relu       │ (None, 14, 14, 576)       │               0 │ block_11_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_project (Conv2D)     │ (None, 14, 14, 96)        │          55,296 │ block_11_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_project_BN           │ (None, 14, 14, 96)        │             384 │ block_11_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_11_add (Add)            │ (None, 14, 14, 96)        │               0 │ block_10_project_BN[0][0], │
│                               │                           │                 │ block_11_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_expand (Conv2D)      │ (None, 14, 14, 576)       │          55,296 │ block_11_add[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_expand_BN            │ (None, 14, 14, 576)       │           2,304 │ block_12_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_expand_relu (ReLU)   │ (None, 14, 14, 576)       │               0 │ block_12_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_depthwise            │ (None, 14, 14, 576)       │           5,184 │ block_12_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_depthwise_BN         │ (None, 14, 14, 576)       │           2,304 │ block_12_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_depthwise_relu       │ (None, 14, 14, 576)       │               0 │ block_12_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_project (Conv2D)     │ (None, 14, 14, 96)        │          55,296 │ block_12_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_project_BN           │ (None, 14, 14, 96)        │             384 │ block_12_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_12_add (Add)            │ (None, 14, 14, 96)        │               0 │ block_11_add[0][0],        │
│                               │                           │                 │ block_12_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_expand (Conv2D)      │ (None, 14, 14, 576)       │          55,296 │ block_12_add[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_expand_BN            │ (None, 14, 14, 576)       │           2,304 │ block_13_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_expand_relu (ReLU)   │ (None, 14, 14, 576)       │               0 │ block_13_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_pad (ZeroPadding2D)  │ (None, 15, 15, 576)       │               0 │ block_13_expand_relu[0][0] │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_depthwise            │ (None, 7, 7, 576)         │           5,184 │ block_13_pad[0][0]         │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_depthwise_BN         │ (None, 7, 7, 576)         │           2,304 │ block_13_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_depthwise_relu       │ (None, 7, 7, 576)         │               0 │ block_13_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_project (Conv2D)     │ (None, 7, 7, 160)         │          92,160 │ block_13_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_13_project_BN           │ (None, 7, 7, 160)         │             640 │ block_13_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_expand (Conv2D)      │ (None, 7, 7, 960)         │         153,600 │ block_13_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_expand_BN            │ (None, 7, 7, 960)         │           3,840 │ block_14_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_expand_relu (ReLU)   │ (None, 7, 7, 960)         │               0 │ block_14_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_depthwise            │ (None, 7, 7, 960)         │           8,640 │ block_14_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_depthwise_BN         │ (None, 7, 7, 960)         │           3,840 │ block_14_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_depthwise_relu       │ (None, 7, 7, 960)         │               0 │ block_14_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_project (Conv2D)     │ (None, 7, 7, 160)         │         153,600 │ block_14_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_project_BN           │ (None, 7, 7, 160)         │             640 │ block_14_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_14_add (Add)            │ (None, 7, 7, 160)         │               0 │ block_13_project_BN[0][0], │
│                               │                           │                 │ block_14_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_expand (Conv2D)      │ (None, 7, 7, 960)         │         153,600 │ block_14_add[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_expand_BN            │ (None, 7, 7, 960)         │           3,840 │ block_15_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_expand_relu (ReLU)   │ (None, 7, 7, 960)         │               0 │ block_15_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_depthwise            │ (None, 7, 7, 960)         │           8,640 │ block_15_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_depthwise_BN         │ (None, 7, 7, 960)         │           3,840 │ block_15_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_depthwise_relu       │ (None, 7, 7, 960)         │               0 │ block_15_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_project (Conv2D)     │ (None, 7, 7, 160)         │         153,600 │ block_15_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_project_BN           │ (None, 7, 7, 160)         │             640 │ block_15_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_15_add (Add)            │ (None, 7, 7, 160)         │               0 │ block_14_add[0][0],        │
│                               │                           │                 │ block_15_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_expand (Conv2D)      │ (None, 7, 7, 960)         │         153,600 │ block_15_add[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_expand_BN            │ (None, 7, 7, 960)         │           3,840 │ block_16_expand[0][0]      │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_expand_relu (ReLU)   │ (None, 7, 7, 960)         │               0 │ block_16_expand_BN[0][0]   │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_depthwise            │ (None, 7, 7, 960)         │           8,640 │ block_16_expand_relu[0][0] │
│ (DepthwiseConv2D)             │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_depthwise_BN         │ (None, 7, 7, 960)         │           3,840 │ block_16_depthwise[0][0]   │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_depthwise_relu       │ (None, 7, 7, 960)         │               0 │ block_16_depthwise_BN[0][… │
│ (ReLU)                        │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_project (Conv2D)     │ (None, 7, 7, 320)         │         307,200 │ block_16_depthwise_relu[0… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ block_16_project_BN           │ (None, 7, 7, 320)         │           1,280 │ block_16_project[0][0]     │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ Conv_1 (Conv2D)               │ (None, 7, 7, 1280)        │         409,600 │ block_16_project_BN[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ Conv_1_bn                     │ (None, 7, 7, 1280)        │           5,120 │ Conv_1[0][0]               │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ out_relu (ReLU)               │ (None, 7, 7, 1280)        │               0 │ Conv_1_bn[0][0]            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ global_average_pooling2d      │ (None, 1280)              │               0 │ out_relu[0][0]             │
│ (GlobalAveragePooling2D)      │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ batch_normalization           │ (None, 1280)              │           5,120 │ global_average_pooling2d[… │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense (Dense)                 │ (None, 512)               │         655,872 │ batch_normalization[0][0]  │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dropout (Dropout)             │ (None, 512)               │               0 │ dense[0][0]                │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ batch_normalization_1         │ (None, 512)               │           2,048 │ dropout[0][0]              │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense_1 (Dense)               │ (None, 256)               │         131,328 │ batch_normalization_1[0][… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dropout_1 (Dropout)           │ (None, 256)               │               0 │ dense_1[0][0]              │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ batch_normalization_2         │ (None, 256)               │           1,024 │ dropout_1[0][0]            │
│ (BatchNormalization)          │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense_2 (Dense)               │ (None, 128)               │          32,896 │ batch_normalization_2[0][… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dropout_2 (Dropout)           │ (None, 128)               │               0 │ dense_2[0][0]              │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ output (Dense)                │ (None, 3)                 │             387 │ dropout_2[0][0]            │
└───────────────────────────────┴───────────────────────────┴─────────────────┴────────────────────────────┘
 Total params: 3,086,659 (11.77 MB)
 Trainable params: 2,350,979 (8.97 MB)
 Non-trainable params: 735,680 (2.81 MB)
```


comando para generar el apk 

"cd /home/raucrow/jc2dev/Whitefly_detector/frontend
flutter build apk --release"


cuando no detecta el telefono

adb devices

Autorizar la depuración USB
adb kill-server && adb start-server


entorno del back

source venv/bin/activate 
uvicorn main:app --reload --host 0.0.0.0 --port 8000