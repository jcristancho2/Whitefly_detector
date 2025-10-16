# 🌱 Sistema de Detección de Mosca Blanca

Sistema inteligente para la detección automática de infestaciones de mosca blanca en cultivos usando visión por computadora y redes neuronales convolucionales.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
  - [Arch Linux](#arch-linux)
  - [Windows](#windows)
- [Configuración y Uso](#configuración-y-uso)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Desarrollo y Debugging](#desarrollo-y-debugging)
- [API Endpoints](#api-endpoints)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Solución de Problemas](#solución-de-problemas)

## 📖 Descripción

Este proyecto utiliza técnicas de machine learning para detectar y clasificar infestaciones de mosca blanca en cultivos agrícolas. El sistema puede funcionar en dos modos:

### **Modo Binario (Recomendado):**
- 🟢 **Sin plaga**: Planta saludable
- 🔴 **Con plaga**: Presencia de mosca blanca (cualquier nivel)

### **Modo Multiclase:**
- 🟢 **Sin plaga**: Planta saludable
- 🟡 **Infestación leve**: Presencia mínima de mosca blanca
- 🔴 **Infestación severa**: Alta concentración de mosca blanca

## ✨ Características

- 🤖 **IA Avanzada**: Modelo basado en MobileNetV2 con transfer learning
- 📱 **Aplicación Móvil**: Frontend desarrollado en Flutter
- 🚀 **API REST**: Backend en FastAPI con documentación automática
- 📊 **Análisis en Tiempo Real**: Procesamiento rápido de imágenes
- 🎯 **Alta Precisión**: Modelo entrenado con técnicas de data augmentation
- 📈 **Múltiples Modelos**: Soporte para clasificación binaria y multiclase
- 🔄 **Cross-Platform**: Funciona en Android, iOS, Web y Desktop

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Flutter App    │    │  FastAPI        │    │  TensorFlow     │
│  (Android/iOS)  │◄──►│  Backend        │◄──►│  Model          │
│  - Cámara       │    │  - Procesamiento│    │  - Clasificación│
│  - Galería      │    │  - Validación   │    │  - Predicción   │
│  - Historial    │    │  - API REST     │    │  - Confianza    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 💻 Requisitos del Sistema

### General
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Almacenamiento**: 10GB de espacio libre
- **Internet**: Conexión estable para descargar dependencias

### Backend (Python)
- **Python**: 3.9 - 3.13
- **pip**: Incluido con Python

### Frontend (Flutter)
- **Flutter SDK**: 3.8.1+
- **Dart SDK**: 3.8.1+

### Para Desarrollo Android
- **Android Studio** o **VS Code**
- **Android SDK**
- **Dispositivo Android** con depuración USB habilitada

## 🚀 Instalación

### Arch Linux

#### 1. Preparar el Sistema

```bash
# Actualizar el sistema
sudo pacman -Syu

# Instalar dependencias base
sudo pacman -S git python python-pip python-virtualenv base-devel

# Instalar Flutter (usando yay o paru)
yay -S flutter
# O manualmente:
# sudo pacman -S flutter

# Instalar herramientas de desarrollo Android (opcional)
yay -S android-studio
```

#### 2. Clonar y Configurar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/whitefly-detector.git
cd whitefly-detector

# Hacer el script ejecutable
chmod +x setup_arch.sh

# Ejecutar instalación automática
./setup_arch.sh
```

**Script de instalación automática (`setup_arch.sh`):**

```bash
#!/bin/bash

echo "🌱 INSTALACIÓN DEL SISTEMA DE DETECCIÓN DE MOSCA BLANCA - ARCH LINUX"
echo "=================================================================="

# Configurar Backend
echo "🔧 Configurando Backend..."
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p models logs uploads
mkdir -p dataset/{train,val,test}/{sin_plaga,infestacion_leve,infestacion_severa}
mkdir -p dataset_binary/{train,val,test}/{sin_plaga,con_plaga}

echo "✅ Backend configurado"

# Configurar Frontend
echo "🔧 Configurando Frontend..."
cd ../frontend

# Verificar Flutter
flutter doctor

# Instalar dependencias
flutter pub get

# Limpiar caché por si acaso
flutter clean
flutter pub get

echo "✅ Frontend configurado"

echo "🎉 Instalación completada!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Colocar dataset en backend/dataset/ (opcional)"
echo "2. Entrenar modelo: cd backend && source venv/bin/activate && python train_model.py"
echo "3. Iniciar backend: cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "4. Compilar APK: cd frontend && flutter build apk --release"
```

### Windows

#### 1. Preparar el Sistema

```powershell
# Instalar Chocolatey (si no está instalado)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar dependencias
choco install git python flutter-sdk -y

# Reiniciar terminal para aplicar cambios PATH
```

#### 2. Clonar y Configurar el Proyecto

```powershell
# Clonar el repositorio
git clone https://github.com/tu-usuario/whitefly-detector.git
cd whitefly-detector

# Ejecutar instalación
.\setup_windows.bat
```

**Script de instalación (`setup_windows.bat`):**

```batch
@echo off
echo 🌱 INSTALACIÓN DEL SISTEMA DE DETECCIÓN DE MOSCA BLANCA - WINDOWS
echo ================================================================

echo 🔧 Configurando Backend...
cd backend

:: Crear entorno virtual
python -m venv venv

:: Activar entorno virtual
call venv\Scripts\activate.bat

:: Actualizar pip
python -m pip install --upgrade pip

:: Instalar dependencias
pip install -r requirements.txt

:: Crear directorios
mkdir models logs uploads 2>nul
mkdir dataset\train\sin_plaga dataset\train\infestacion_leve dataset\train\infestacion_severa 2>nul
mkdir dataset\val\sin_plaga dataset\val\infestacion_leve dataset\val\infestacion_severa 2>nul
mkdir dataset\test\sin_plaga dataset\test\infestacion_leve dataset\test\infestacion_severa 2>nul
mkdir dataset_binary\train\sin_plaga dataset_binary\train\con_plaga 2>nul
mkdir dataset_binary\val\sin_plaga dataset_binary\val\con_plaga 2>nul
mkdir dataset_binary\test\sin_plaga dataset_binary\test\con_plaga 2>nul

echo ✅ Backend configurado

echo 🔧 Configurando Frontend...
cd ..\frontend

:: Verificar Flutter
flutter doctor

:: Instalar dependencias
flutter pub get

echo ✅ Frontend configurado

echo 🎉 Instalación completada!
echo.
echo 📝 Próximos pasos:
echo 1. Colocar dataset en backend\dataset\ (opcional)
echo 2. Entrenar modelo: cd backend && venv\Scripts\activate && python train_model.py
echo 3. Iniciar backend: cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo 4. Compilar APK: cd frontend && flutter build apk --release

pause
```

## ⚙️ Configuración y Uso

### 1. Preparar Dataset (Opcional)

Si quieres entrenar tu propio modelo, organiza las imágenes así:

```
backend/dataset/
├── train/ (70% de imágenes)
│   ├── sin_plaga/          # Imágenes de plantas sanas
│   ├── infestacion_leve/   # Imágenes con infestación leve
│   └── infestacion_severa/ # Imágenes con infestación severa
├── val/ (20% de imágenes)
│   ├── sin_plaga/
│   ├── infestacion_leve/
│   └── infestacion_severa/
└── test/ (10% de imágenes)
    ├── sin_plaga/
    ├── infestacion_leve/
    └── infestacion_severa/
```

### 2. Entrenar Modelo

#### Modelo Binario (Recomendado)

```bash
# Arch Linux
cd backend
source venv/bin/activate
python binary_train_optimized.py
```

```powershell
# Windows
cd backend
venv\Scripts\activate
python binary_train_optimized.py
```

**Características del modelo binario:**
- ✅ **Más preciso**: Solo 2 clases reduce confusión
- ✅ **Mejor balance**: ~50%/50% entre clases
- ✅ **Más práctico**: Detecta si hay plaga o no
- ✅ **Mayor accuracy**: Típicamente >95%

#### Modelo Multiclase (3 clases)

```bash
# Arch Linux
cd backend
source venv/bin/activate
python train_model.py
```

```powershell
# Windows
cd backend
venv\Scripts\activate
python train_model.py
```

### 3. Iniciar Backend

```bash
# Arch Linux
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

```powershell
# Windows
cd backend
venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**El backend estará disponible en:**
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Desarrollar App (Opcional)

#### Para desarrollo en tiempo real:

```bash
cd frontend
flutter run
```

#### Para generar APK de producción:

```bash
cd frontend
flutter build apk --release
```

**El APK se generará en:** `frontend/build/app/outputs/flutter-apk/app-release.apk`

### 5. Configurar Dispositivo Android

#### Habilitar depuración USB:

1. **Configuración** → **Acerca del teléfono**
2. Tocar **Número de compilación** 7 veces
3. **Configuración** → **Opciones de desarrollador**
4. Activar **Depuración USB**

#### Verificar conexión:

```bash
# Instalar ADB (si no está)
# Arch Linux:
sudo pacman -S android-tools

# Windows:
choco install adb

# Verificar dispositivos conectados
adb devices

# Si no aparece el dispositivo:
adb kill-server && adb start-server
```

## 🧠 Entrenamiento del Modelo

### Análisis de Dataset

Para verificar la distribución de tu dataset:

```bash
cd backend
source venv/bin/activate  # Linux
# venv\Scripts\activate   # Windows

# Analizar dataset actual
echo "=== ANÁLISIS DEL DATASET ==="
echo "TRAIN:"
echo "  sin_plaga: $(find dataset/train/sin_plaga -name "*.jpg" | wc -l)"
echo "  infestacion_leve: $(find dataset/train/infestacion_leve -name "*.jpg" | wc -l)"
echo "  infestacion_severa: $(find dataset/train/infestacion_severa -name "*.jpg" | wc -l)"
```

### Configuración de Entrenamiento

#### Modelo Binario (`binary_train_optimized.py`)

```python
# Configuración recomendada
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30
TARGET_PER_CLASS = 1400  # Imágenes balanceadas por clase
```

#### Modelo Multiclase (`train_model.py`)

```python
# Configuración con balance de clases
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
# Pesos para balancear clases desbalanceadas
class_weight = {
    0: 1.0,    # infestacion_leve
    1: 5.0,    # infestacion_severa (más peso por menos muestras)
    2: 1.0     # sin_plaga
}
```

### Métricas Esperadas

#### Modelo Binario:
- **Accuracy**: >95%
- **Precision**: >94%
- **Recall**: >94%
- **F1-Score**: >94%

#### Modelo Multiclase:
- **Accuracy**: >90%
- **Precision**: >88%
- **Recall**: >88%
- **F1-Score**: >88%

## 🛠️ Desarrollo y Debugging

### Logs del Sistema

```bash
# Backend logs
tail -f backend/logs/*.log

# Frontend logs (durante desarrollo)
flutter logs
```

### Probar API Manualmente

```bash
# Probar con imagen del dataset
curl -X POST "http://localhost:8000/api/detectar" \
     -F "file=@backend/dataset/test/infestacion_leve/imagen.jpg"

# Respuesta esperada:
{
  "prediction": "con_plaga",
  "confidence": 0.95,
  "processing_time": 1.23,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Actualizar Modelo en Backend

Para usar un modelo recién entrenado:

```python
# En backend/main.py, cambiar la línea:
model = tf.keras.models.load_model('models/binary_whitefly_detector.h5')
# model = tf.keras.models.load_model('models/whitefly_detector.h5')  # Para multiclase
```

Luego reiniciar el backend.

## 📡 API Endpoints

### POST `/api/detectar`
Analiza una imagen para detectar infestación de mosca blanca.

**Parámetros:**
- `file`: Imagen en formato JPG, JPEG o PNG (máx. 10MB)

**Respuesta Binaria:**
```json
{
  "prediction": "con_plaga",
  "confidence": 0.95,
  "processing_time": 1.23,
  "timestamp": "2024-01-15T10:30:00Z",
  "model_type": "binary"
}
```

**Respuesta Multiclase:**
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
  "model_type": "multiclass"
}
```

### GET `/health`
Verifica el estado del servicio.

### GET `/docs`
Documentación interactiva de la API (Swagger UI).

## 📁 Estructura del Proyecto

```
whitefly-detector/
├── 📄 README.md
├── 🛠️ setup_arch.sh          # Script instalación Arch Linux
├── 🛠️ setup_windows.bat      # Script instalación Windows
├── 📊 backend/
│   ├── 🔧 main.py                    # API principal FastAPI
│   ├── 🧠 train_model.py             # Entrenamiento multiclase
│   ├── 🎯 binary_train_optimized.py  # Entrenamiento binario
│   ├── 🔬 simple_train.py            # Modelo simple para debug
│   ├── 🛠️ utils.py                   # Utilidades
│   ├── 📦 requirements.txt           # Dependencias Python
│   ├── 🗂️ dataset/                  # Datos multiclase
│   │   ├── train/{sin_plaga,infestacion_leve,infestacion_severa}/
│   │   ├── val/{sin_plaga,infestacion_leve,infestacion_severa}/
│   │   └── test/{sin_plaga,infestacion_leve,infestacion_severa}/
│   ├── 🗂️ dataset_binary/           # Datos binarios
│   │   ├── train/{sin_plaga,con_plaga}/
│   │   ├── val/{sin_plaga,con_plaga}/
│   │   └── test/{sin_plaga,con_plaga}/
│   ├── 🤖 models/                   # Modelos entrenados
│   │   ├── binary_whitefly_detector.h5      # Modelo binario
│   │   ├── whitefly_detector.h5             # Modelo multiclase
│   │   └── simple_whitefly_detector.h5      # Modelo simple
│   ├── 📋 logs/                     # Archivos de log
│   └── 📁 venv/                     # Entorno virtual Python
├── 📱 frontend/
│   ├── 🎯 lib/                      # Código fuente Flutter
│   │   ├── main.dart                # Punto de entrada
│   │   ├── Pages/                   # Páginas de la app
│   │   ├── services/api_service.dart # Comunicación con backend
│   │   ├── models/                  # Modelos de datos
│   │   └── Widgets/                 # Componentes reutilizables
│   ├── 🤖 android/                  # Configuración Android
│   ├── 🍎 ios/                      # Configuración iOS
│   ├── 🖥️ web/                      # Configuración Web
│   ├── 📦 pubspec.yaml              # Dependencias Flutter
│   └── 🔨 build/app/outputs/flutter-apk/ # APK generado
└── 📚 docs/
    └── 📖 PROYECTO MODIFICADO.docx
```

## 🔧 Solución de Problemas

### Error: Backend no inicia

```bash
# Verificar Python y dependencias
python --version
pip list

# Reinstalar dependencias
cd backend
pip install -r requirements.txt --force-reinstall

# Verificar modelo
ls -la models/
```

### Error: Flutter no compila

```bash
# Limpiar caché
flutter clean
flutter pub get

# Verificar instalación
flutter doctor

# Solucionar problemas específicos
flutter doctor --android-licenses  # Aceptar licencias Android
```

### Error: Dispositivo Android no detectado

```bash
# Verificar ADB
adb devices

# Reiniciar ADB
adb kill-server && adb start-server

# Verificar depuración USB está habilitada
# Configuración → Opciones de desarrollador → Depuración USB
```

### Error: Modelo da predicciones incorrectas

```bash
# Probar con modelo simple
cd backend
source venv/bin/activate
python simple_train.py

# Verificar dataset
echo "Verificando distribución..."
find dataset/train -name "*.jpg" | wc -l

# Reentrenar modelo binario
python binary_train_optimized.py
```

### Error: CUDA no disponible

```bash
# Normal en CPU - el mensaje es solo informativo
# El modelo funcionará perfectamente en CPU
# Para GPU en Arch Linux (opcional):
sudo pacman -S cuda cudnn
```

### Performance Lenta

```bash
# Optimizar batch size
# En train_model.py cambiar:
BATCH_SIZE = 16  # Reducir si hay poco RAM

# Usar modelo más ligero
# Cambiar en train_model.py:
base_model = tf.keras.applications.MobileNetV2(...)  # Ya es ligero
```

## 🚀 Scripts de Inicio Rápido

### Arch Linux

Crear `start_system.sh`:

```bash
#!/bin/bash
echo "🌱 Iniciando Sistema de Detección de Mosca Blanca"

# Terminal 1: Backend
gnome-terminal -- bash -c "cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash"

# Terminal 2: Logs
gnome-terminal -- bash -c "cd backend && tail -f logs/*.log; exec bash"

echo "✅ Sistema iniciado!"
echo "📱 Backend: http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
echo "🔨 Para compilar APK: cd frontend && flutter build apk --release"
```

### Windows

Crear `start_system.bat`:

```batch
@echo off
echo 🌱 Iniciando Sistema de Detección de Mosca Blanca

start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo ✅ Sistema iniciado!
echo 📱 Backend: http://localhost:8000
echo 📖 Docs: http://localhost:8000/docs
echo 🔨 Para compilar APK: cd frontend && flutter build apk --release
pause
```

## 👥 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**💡 Tips Importantes:**

- 🎯 **Usa el modelo binario** para mayor precisión
- 📱 **Habilita depuración USB** en tu dispositivo Android
- 🔄 **Reinicia el backend** después de entrenar un nuevo modelo
- 📊 **Monitorea los logs** para debugging
- 🚀 **Compila APK en release** para mejor performance

**🆘 Soporte:**
- 📖 Documentación de API: http://localhost:8000/docs
- 🐛 Issues: Abre un issue en GitHub
- 💬 Discusiones: Usa las GitHub Discussions

**✨ ¡Tu feedback es valioso para mejorar el sistema!**