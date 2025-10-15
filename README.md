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


comando para generar el apk 

"cd /home/raucrow/jc2dev/Whitefly_detector/frontend
flutter build apk --release"


cuando no detecta el telefono

adb devices

Autorizar la depuración USB
adb kill-server && adb start-server