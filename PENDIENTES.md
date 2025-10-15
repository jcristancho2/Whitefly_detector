# 📋 Lista de Pendientes - Sistema de Detección de Mosca Blanca

**Fecha de Análisis**: 14 de Octubre, 2025  
**Estado General**: ⚠️ **PROYECTO NO FUNCIONAL** - Requiere trabajo significativo

---

## 🚨 **PROBLEMAS CRÍTICOS**

### ❌ **Backend - API Principal Vacía**
- **Estado**: 🔴 **CRÍTICO**
- **Problema**: El archivo `backend/main.py` solo contiene un comentario "#API PRINCIPAL"
- **Impacto**: Sin API, el sistema no funciona
- **Acción Requerida**:
  - [ ] Implementar FastAPI completa con endpoints de detección
  - [ ] Crear endpoint `/detect` para análisis de imágenes
  - [ ] Implementar manejo de archivos y validación
  - [ ] Agregar endpoints de salud (`/health`) y información del modelo (`/model/info`)

### ❌ **Modelo de IA Ausente**
- **Estado**: 🔴 **CRÍTICO**
- **Problema**: Carpeta `backend/models/` está vacía
- **Impacto**: No hay modelo para hacer predicciones
- **Acción Requerida**:
  - [ ] Entrenar modelo usando `train_model.py` (requiere dataset)
  - [ ] Obtener dataset de imágenes etiquetadas
  - [ ] Generar modelo `whitefly_detector.h5`

### ❌ **Dataset Vacío**
- **Estado**: 🔴 **CRÍTICO**
- **Problema**: Todas las carpetas de dataset están vacías
- **Impacto**: No se puede entrenar el modelo
- **Acción Requerida**:
  - [ ] Recolectar imágenes de plantas con y sin mosca blanca
  - [ ] Organizar en carpetas: `sin_plaga/`, `infestacion_leve/`, `infestacion_severa/`
  - [ ] Mínimo 100-200 imágenes por categoría

---

## ⚠️ **PROBLEMAS IMPORTANTES**

### 🟡 **Frontend - Dependencias Faltantes**
- **Estado**: 🟡 **ALTO**
- **Problema**: `pubspec.yaml` no incluye dependencias necesarias
- **Dependencias Faltantes**:
  - [ ] `image_picker: ^1.0.4` (selección de imágenes)
  - [ ] `http: ^1.1.0` (comunicación con API)
  - [ ] `path_provider: ^2.1.1` (manejo de archivos)
- **Acción**: Actualizar `pubspec.yaml` y ejecutar `flutter pub get`

### 🟡 **API Endpoints Incorrectos**
- **Estado**: 🟡 **ALTO**
- **Problema**: Frontend llama a endpoints que no existen
- **Endpoints Problemáticos**:
  - `/api/detectar` (debería ser `/detect`)
  - `/api/estadisticas` (no implementado)
  - `/api/historial` (no implementado)
- **Acción**: Sincronizar URLs entre frontend y backend

### 🟡 **Configuración para APK Android**
- **Estado**: 🟡 **MEDIO**
- **Problema**: No está configurado para generar APK de producción
- **Acción**: Configurar firma de aplicación y build settings para Android

---

## 🔧 **TAREAS DE DESARROLLO**

### **Backend (Python/FastAPI)**

#### 1. **Implementar API Principal** 🔴
```python
# Tareas para backend/main.py:
- [ ] Configurar FastAPI app
- [ ] Implementar endpoint POST /detect
- [ ] Cargar modelo TensorFlow/Keras
- [ ] Procesar imágenes con OpenCV/PIL
- [ ] Validar tipos de archivo (jpg, png)
- [ ] Manejar errores y excepciones
- [ ] Configurar CORS para frontend
- [ ] Implementar logging
```

#### 2. **Completar Utilidades** 🟡
```python
# Archivo utils.py (parcialmente implementado):
- [ ] Función para cargar modelo
- [ ] Preprocesamiento de imágenes
- [ ] Validación de archivos
- [ ] Sistema de logs mejorado
- [ ] Configuración desde variables de entorno
```

#### 3. **Sistema de Base de Datos** 🟢
```python
# Opcional pero recomendado:
- [ ] Integrar SQLAlchemy
- [ ] Crear tablas para historial
- [ ] Guardar resultados de detección
- [ ] Sistema de estadísticas
```

### **Frontend (Flutter/Dart)**

#### 1. **Completar Dependencias** 🔴
```yaml
# Actualizar pubspec.yaml:
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.8
  image_picker: ^1.0.4      # ← AGREGAR
  http: ^1.1.0              # ← AGREGAR
  path_provider: ^2.1.1     # ← AGREGAR
  shared_preferences: ^2.2.2 # ← AGREGAR
  permission_handler: ^11.0.1 # ← AGREGAR (para permisos de cámara)
```

#### 2. **Corregir API Service** 🟡
```dart
# Actualizar lib/services/api_service.dart:
- [ ] Cambiar endpoints a /detect, /health, etc.
- [ ] Manejar timeouts
- [ ] Implementar retry logic
- [ ] Mejorar manejo de errores
- [ ] Configurar URL base para producción vs desarrollo
```

#### 3. **Implementar Funcionalidades Faltantes** 🟡
```dart
# Páginas por completar:
- [ ] history_page.dart - mostrar historial de análisis
- [ ] stats_page.dart - estadísticas de detecciones
- [ ] Navegación entre páginas
- [ ] Persistencia local de datos
```

#### 4. **Configuración Android APK** 🔴
```gradle
# Configurar android/app/build.gradle:
- [ ] Configurar applicationId único
- [ ] Agregar permisos de cámara e internet
- [ ] Configurar keystore para firma
- [ ] Optimizar para release
- [ ] Configurar ProGuard/R8
- [ ] Configurar ícono de la app
```

#### 5. **Preparar APK de Producción** 🟡
```bash
# Comandos para generar APK:
- [ ] flutter build apk --release
- [ ] flutter build appbundle --release (para Google Play)
- [ ] Probar APK en dispositivos reales
- [ ] Configurar auto-signing
```

### **Despliegue y Distribución**

#### 1. **Configuración del Backend para Producción** 🟡
```python
# Opciones de despliegue del backend:
- [ ] Servidor VPS (DigitalOcean, Linode, AWS EC2)
- [ ] Servicios serverless (Vercel, Railway, Render)
- [ ] Hosting compartido con soporte Python
- [ ] Configurar dominio y SSL
- [ ] Variables de entorno de producción
```

#### 2. **Generación de APK Android** 🔴
```bash
# Proceso completo para APK:
- [ ] Configurar keystore de firma
- [ ] Configurar build.gradle para release
- [ ] Optimizar assets y dependencias
- [ ] Generar APK firmada
- [ ] Probar en dispositivos reales
- [ ] Documentar proceso de instalación manual
```

#### 3. **Distribución de la App** �
```
# Opciones de distribución:
- [ ] APK directa (instalación manual)
- [ ] Google Play Store (requiere cuenta desarrollador)
- [ ] Tiendas alternativas (F-Droid, Amazon Appstore)
- [ ] Distribución interna/empresarial
```

---

## 🎯 **PLAN DE IMPLEMENTACIÓN RECOMENDADO**

### **Fase 1: Funcionalidad Básica** (1-2 semanas)
1. ✅ **Obtener Dataset**
   - Recolectar/descargar imágenes de plantas
   - Organizar en estructura correcta
   
2. ✅ **Entrenar Modelo**
   - Ejecutar `train_model.py`
   - Validar precisión del modelo
   
3. ✅ **Implementar API Básica**
   - Crear endpoint `/detect`
   - Cargar modelo en memoria
   - Procesar imágenes

### **Fase 2: Integración Frontend** (1 semana)
4. ✅ **Corregir Dependencias Flutter**
   - Actualizar `pubspec.yaml`
   - Sincronizar endpoints
   
5. ✅ **Pruebas de Integración**
   - Probar flujo completo
   - Corregir errores de comunicación

### **Fase 3: APK y Distribución** (1-2 semanas)
6. ✅ **Configurar APK de Producción**
   - Configurar keystore de firma
   - Optimizar build para release
   
7. ✅ **Desplegar Backend**
   - Elegir servicio de hosting
   - Configurar dominio y SSL

### **Fase 4: Testing y Optimización** (1 semana)
8. ✅ **Pruebas Completas**
   - Probar APK en dispositivos reales
   - Validar flujo completo
   
9. ✅ **Documentación Final**
   - Manual de instalación
   - Guía de uso

---

## 📊 **RESUMEN DE ESTADO**

| Componente | Estado | Funcional | Acción Requerida |
|------------|--------|-----------|------------------|
| **Backend API** | 🔴 | No | Implementar desde cero |
| **Modelo IA** | 🔴 | No | Entrenar con dataset |
| **Dataset** | 🔴 | No | Recolectar imágenes |
| **Frontend Flutter** | 🟡 | Parcial | Agregar dependencias |
| **Integración** | 🔴 | No | Sincronizar endpoints |
| **Configuración APK** | 🔴 | No | Configurar para producción |
| **Scripts de inicio** | 🟢 | Sí | Funcionales |
| **Documentación** | 🟢 | Sí | README completo |

---

## 🎯 **PRIORIDADES INMEDIATAS**

### **🔥 URGENTE (Hacer AHORA)**
1. **Obtener dataset de imágenes** - Sin esto, nada funciona
2. **Implementar `backend/main.py`** - API principal
3. **Agregar dependencias Flutter** - Frontend no compila

### **⚡ IMPORTANTE (Esta semana)**
4. **Entrenar modelo de IA** - Una vez que tengas el dataset
5. **Sincronizar endpoints** - Frontend y backend deben coincidir
6. **Pruebas básicas** - Verificar que todo se conecta

### **📈 MEJORAS (Próximas semanas)**
7. **Configurar APK de producción**
8. **Base de datos para historial**
9. **Interfaz mejorada**
10. **Optimizaciones de rendimiento**
11. **Despliegue del backend**

---

## � **CONFIGURACIÓN ESPECÍFICA PARA APK ANDROID**

### **🔧 Preparación del Entorno Android**

#### 1. **Verificar Instalación Android**
```bash
# Verificar que tienes todo configurado:
flutter doctor

# Debe mostrar ✅ en:
# - Flutter SDK
# - Android toolchain
# - Android Studio
# - Connected device (opcional)
```

#### 2. **Configurar Permisos en Android** 🔴
```xml
<!-- En android/app/src/main/AndroidManifest.xml agregar: -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

#### 3. **Configurar build.gradle para Producción** 🔴
```gradle
// En android/app/build.gradle:
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.tuempresa.whitefly_detector"  // ← CAMBIAR
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
}
```

#### 4. **Crear Keystore para Firma** 🔴
```bash
# Crear keystore (hacer una sola vez):
keytool -genkey -v -keystore ~/whitefly-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias whitefly

# Crear archivo key.properties en android/:
storePassword=TU_PASSWORD_AQUI
keyPassword=TU_PASSWORD_AQUI  
keyAlias=whitefly
storeFile=/ruta/completa/a/whitefly-key.jks
```

#### 5. **Configurar Ícono de la App** 🟡
```yaml
# En pubspec.yaml agregar:
flutter_icons:
  android: true
  image_path: "assets/icon/icon.png"  # Crear esta imagen 1024x1024
  
# Luego ejecutar:
# flutter packages pub run flutter_launcher_icons:main
```

### **🚀 Proceso de Generación de APK**

#### **Comandos para Generar APK** 🔴
```bash
# 1. Limpiar proyecto
flutter clean
flutter pub get

# 2. Generar APK de release
flutter build apk --release

# 3. APK estará en: build/app/outputs/flutter-apk/app-release.apk

# 4. Para generar APK más pequeña (recomendado):
flutter build apk --split-per-abi --release

# 5. Para App Bundle (Google Play):
flutter build appbundle --release
```

#### **Configuración de URLs para Producción** 🔴
```dart
// En lib/services/api_service.dart:
class ApiConfig {
  // Para desarrollo:
  static const String devUrl = 'http://10.0.2.2:8000';  // Android emulator
  static const String devLocalUrl = 'http://localhost:8000';
  
  // Para producción:
  static const String prodUrl = 'https://tu-dominio.com';  // ← CAMBIAR
  
  static String get baseUrl {
    // Automáticamente detectar si es debug o release
    const bool isProduction = bool.fromEnvironment('dart.vm.product');
    return isProduction ? prodUrl : devUrl;
  }
}
```

### **🌐 Opciones de Despliegue del Backend (Sin Docker)**

#### **Opción 1: Servicios Cloud Simples** 🟢 **RECOMENDADO**
```bash
# Railway.app (Fácil y gratuito):
1. Crear cuenta en railway.app
2. Conectar repositorio GitHub
3. Railway detecta automáticamente Python
4. Variables de entorno en dashboard
5. URL automática: https://tu-app.railway.app

# Render.com (Alternativa gratuita):
1. Crear cuenta en render.com  
2. Conectar repositorio
3. Configurar como "Web Service"
4. Python environment detectado automáticamente
```

#### **Opción 2: VPS Tradicional** 🟡
```bash
# En servidor Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip nginx

# Instalar dependencias del proyecto
pip3 install -r requirements.txt

# Configurar nginx como proxy reverso
# Usar supervisor para mantener la app corriendo
```

#### **Opción 3: Serverless** 🟡
```bash
# Vercel (requiere adaptar FastAPI):
# - Crear vercel.json
# - Adaptar para funciones serverless

# Google Cloud Functions
# AWS Lambda
```

### **📦 Distribución de la APK**

#### **Instalación Manual** 🟢 **MÁS FÁCIL**
```
1. Generar APK firmada
2. Subir APK a Google Drive/Dropbox
3. Compartir link de descarga
4. Usuario descarga e instala manualmente
5. Activar "Fuentes desconocidas" en Android
```

#### **Google Play Store** 🟡 **MÁS PROFESIONAL**
```
Requisitos:
- Cuenta Google Play Developer ($25 USD una vez)
- App Bundle firmada
- Política de privacidad
- Capturas de pantalla
- Descripción de la app
- Proceso de revisión (1-3 días)
```

#### **Distribución Interna/Empresarial** 🟢
```
- Firebase App Distribution (gratuito)
- TestFlight (solo iOS)
- APK directo por email/web
- Sistema de gestión de dispositivos móviles (MDM)
```

---

## �💡 **RECOMENDACIONES SOBRE DOCKER**

### **¿Por qué NO usar Docker en este caso?**

1. **✅ VENTAJAS de NO usar Docker:**
   - **Más simple**: Menos complejidad para un proyecto pequeño
   - **Deployment directo**: Servicios como Railway/Render son más fáciles
   - **Menos recursos**: No necesitas conocer Docker
   - **Debug más fácil**: Menos capas de abstracción

2. **❌ DESVENTAJAS de NO usar Docker:**
   - Menos consistencia entre entornos
   - Más difícil escalar horizontalmente
   - Dependencia del sistema operativo del servidor

### **🎯 MI RECOMENDACIÓN:**

**Para tu caso específico: NO uses Docker**, porque:

- Es tu primer proyecto de este tipo
- Railway/Render manejan el deployment automáticamente
- Puedes agregar Docker más adelante si lo necesitas
- Te enfocarás en la funcionalidad, no en infraestructura

### **🚀 Plan de Deployment Recomendado:**

1. **Backend**: Railway.app o Render.com (gratuito, fácil)
2. **Frontend**: APK directa para distribución manual
3. **Base de datos**: SQLite local en el backend (simple)
4. **Dominio**: Subdominio gratuito del servicio cloud

---

### **Dataset Recomendado**
- **Mínimo**: 150 imágenes por categoría (450 total)
- **Recomendado**: 500+ imágenes por categoría
- **Formato**: JPG/PNG, 224x224 píxeles mínimo
- **Fuentes**: Roboflow, Kaggle, o captura propia

### **Recursos de Desarrollo**
- **Backend**: Python 3.9+, FastAPI, TensorFlow 2.x
- **Frontend**: Flutter 3.8+, Dart 3.8+
- **Herramientas**: VS Code, Postman para API testing
- **Hardware**: GPU recomendada para entrenamiento

---

**🎯 OBJETIVO**: Tener un MVP funcional en 2-3 semanas con detección básica de mosca blanca.

**📞 CONTACTO**: Para dudas técnicas, revisar documentación de FastAPI, Flutter y TensorFlow.