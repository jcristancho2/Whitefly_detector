#!/bin/bash

# Script para configurar Flutter desde fuente oficial
echo "🔧 Configurando Flutter desde fuente oficial..."

# Configurar variables de entorno para Flutter oficial
export FLUTTER_HOME="/home/raucrow/flutter"
export PATH="$FLUTTER_HOME/bin:$PATH"
export ANDROID_HOME="/opt/android-sdk"
export ANDROID_SDK_ROOT="/opt/android-sdk"
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"

echo "✅ Variables de entorno configuradas:"
echo "   FLUTTER_HOME: $FLUTTER_HOME"
echo "   ANDROID_HOME: $ANDROID_HOME"
echo "   PATH actualizado con Flutter y Android SDK"

# Verificar Flutter
echo ""
echo "🔍 Verificando instalación de Flutter..."
flutter doctor

echo ""
echo "📱 Dispositivos disponibles:"
flutter devices

echo ""
echo "🚀 Para usar este entorno, ejecuta:"
echo "   source /home/raucrow/jc2dev/Whitefly_detector/setup_flutter_env.sh"
echo "   cd /home/raucrow/jc2dev/Whitefly_detector/frontend"
echo "   flutter run -d R5CY53FR4DX"