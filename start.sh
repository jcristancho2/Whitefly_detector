#!/bin/bash
# start.sh - Script de inicio rápido del sistema

set -e  # Detener en caso de error

echo "🌱 Sistema de Detección de Mosca Blanca"
echo "========================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar requisitos
check_requirements() {
    echo "🔍 Verificando requisitos..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 no está instalado${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python3 encontrado${NC}"
    
    # pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 no está instalado${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ pip3 encontrado${NC}"
    
    echo ""
}

# Función para crear entorno virtual
setup_venv() {
    echo "📦 Configurando entorno virtual..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✅ Entorno virtual creado${NC}"
    else
        echo -e "${YELLOW}⚠️  Entorno virtual ya existe${NC}"
    fi
    
    # Activar entorno virtual
    source venv/bin/activate || source venv/Scripts/activate 2>/dev/null
    
    echo ""
}

# Función para instalar dependencias
install_dependencies() {
    echo "📚 Instalando dependencias..."
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
    echo ""
}

# Función para crear directorios
create_directories() {
    echo "📁 Creando estructura de directorios..."
    
    mkdir -p models logs dataset/train dataset/val dataset/test uploads
    
    # Crear subdirectorios para clases
    for split in train val test; do
        mkdir -p dataset/$split/sin_plaga
        mkdir -p dataset/$split/infestacion_leve
        mkdir -p dataset/$split/infestacion_severa
    done
    
    echo -e "${GREEN}✅ Directorios creados${NC}"
    echo ""
}

# Función para verificar modelo
check_model() {
    echo "🤖 Verificando modelo..."
    
    if [ -f "models/whitefly_detector.h5" ]; then
        echo -e "${GREEN}✅ Modelo encontrado${NC}"
    else
        echo -e "${YELLOW}⚠️  Modelo no encontrado${NC}"
        echo "   Necesitas entrenar el modelo primero:"
        echo "   python train_model.py"
        echo ""
        read -p "   ¿Quieres entrenar ahora? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            python train_model.py
        fi
    fi
    echo ""
}

# Función para verificar dataset
check_dataset() {
    echo "📊 Verificando dataset..."
    
    train_count=$(find dataset/train -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) 2>/dev/null | wc -l)
    
    if [ "$train_count" -eq 0 ]; then
        echo -e "${YELLOW}⚠️  No hay imágenes en el dataset${NC}"
        echo "   Coloca tus imágenes en:"
        echo "   - dataset/train/sin_plaga/"
        echo "   - dataset/train/infestacion_leve/"
        echo "   - dataset/train/infestacion_severa/"
        echo ""
    else
        echo -e "${GREEN}✅ Dataset encontrado: $train_count imágenes${NC}"
    fi
    echo ""
}

# Función para iniciar servidor
start_server() {
    echo "🚀 Iniciando servidor..."
    echo ""
    echo "   API disponible en: http://localhost:8000"
    echo "   Documentación: http://localhost:8000/docs"
    echo ""
    echo "   Presiona Ctrl+C para detener el servidor"
    echo ""
    
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Menú principal
show_menu() {
    echo "¿Qué deseas hacer?"
    echo ""
    echo "1) Configuración inicial completa"
    echo "2) Solo instalar dependencias"
    echo "3) Verificar sistema"
    echo "4) Entrenar modelo"
    echo "5) Iniciar servidor"
    echo "6) Iniciar con Docker"
    echo "7) Salir"
    echo ""
    read -p "Selecciona una opción (1-7): " option
    
    case $option in
        1)
            check_requirements
            setup_venv
            install_dependencies
            create_directories
            check_dataset
            check_model
            echo -e "${GREEN}✅ Configuración completada${NC}"
            echo ""
            read -p "¿Iniciar servidor ahora? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                start_server
            fi
            ;;
        2)
            setup_venv
            install_dependencies
            ;;
        3)
            python utils.py check
            ;;
        4)
            python train_model.py
            ;;
        5)
            start_server
            ;;
        6)
            echo "🐳 Iniciando con Docker..."
            docker-compose up --build
            ;;
        7)
            echo "👋 ¡Hasta luego!"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida${NC}"
            show_menu
            ;;
    esac
}

# Ejecutar menú
show_menu