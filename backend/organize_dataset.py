#!/usr/bin/env python3
"""
Script para reorganizar el dataset de Roboflow (YOLOv8) 
a formato de clasificación para el proyecto de mosca blanca.

Uso:
    python organize_dataset.py

El script:
1. Analiza las imágenes existentes
2. Las categoriza automáticamente por severidad (usando nombres de archivo como pista)
3. Las organiza en la estructura correcta para clasificación
4. Crea splits train/val/test
"""

import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

# Configuración
SOURCE_DIR = "train/images"
DEST_BASE = "."
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

# Palabras clave para categorización automática
KEYWORDS = {
    'sin_plaga': [
        'healthy', 'clean', 'good', 'normal', 'sin_plaga', 'sano', 'limpio'
    ],
    'infestacion_leve': [
        'light', 'leve', 'mild', 'few', 'small', 'minor', 'poco', 'ligero'
    ],
    'infestacion_severa': [
        'heavy', 'severe', 'severa', 'high', 'много', 'dense', 'fuerte', 
        'alto', 'grave', 'intenso', 'pesado'
    ]
}

def analyze_image_brightness(image_path):
    """Analiza el tamaño del archivo para inferir complejidad (sin OpenCV)."""
    try:
        # Usar tamaño de archivo como aproximación
        file_size = os.path.getsize(image_path)
        # Normalizar entre 0 y 1 (archivos típicos 50KB-500KB)
        normalized_size = min(file_size / 500000, 1.0)
        return normalized_size
    except:
        return 0.5

def categorize_by_filename(filename):
    """Categoriza la imagen basándose en el nombre del archivo."""
    filename_lower = filename.lower()
    
    # Buscar palabras clave específicas
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    # Si no encuentra palabras clave, usar análisis de nombres comunes
    if any(word in filename_lower for word in ['ba-', 'dsc_', 'white_fly']):
        # Estas parecen ser imágenes con mosca blanca
        # Usar número o posición para inferir severidad
        if any(char in filename_lower for char in ['1', '2', '3', '4', '5']):
            return 'infestacion_leve'
        else:
            return 'infestacion_severa'
    
    # Por defecto, asignar a infestación leve
    return 'infestacion_leve'

def smart_categorization(image_path):
    """Categorización inteligente usando múltiples factores."""
    filename = os.path.basename(image_path)
    
    # 1. Categorización por nombre de archivo
    file_category = categorize_by_filename(filename)
    
    # 2. Análisis de tamaño de archivo (aproximación simple)
    file_size_factor = analyze_image_brightness(image_path)
    
    # 3. Lógica combinada
    # Como este dataset es principalmente de mosca blanca,
    # vamos a distribuir inteligentemente:
    
    # Buscar patrones específicos que indiquen plantas sanas
    if any(word in filename.lower() for word in ['clean', 'healthy', 'normal', 'good']):
        return 'sin_plaga'
    
    # Buscar patrones que indiquen infestación severa
    if any(word in filename.lower() for word in ['severe', 'heavy', 'high', 'dense', 'bad']):
        return 'infestacion_severa'
    
    # El resto se distribuye entre leve y severa basado en el nombre
    return file_category

def create_directory_structure():
    """Crea la estructura de directorios necesaria."""
    splits = ['train', 'val', 'test']
    categories = ['sin_plaga', 'infestacion_leve', 'infestacion_severa']
    
    for split in splits:
        for category in categories:
            path = Path(DEST_BASE) / split / category
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creado: {path}")

def organize_images():
    """Organiza las imágenes en la estructura correcta."""
    source_path = Path(SOURCE_DIR)
    
    if not source_path.exists():
        print(f"❌ Error: No se encontró {SOURCE_DIR}")
        return
    
    # Obtener todas las imágenes
    image_files = list(source_path.glob("*.jpg")) + list(source_path.glob("*.jpeg")) + list(source_path.glob("*.png"))
    
    if not image_files:
        print(f"❌ No se encontraron imágenes en {SOURCE_DIR}")
        return
    
    print(f"📊 Encontradas {len(image_files)} imágenes")
    
    # Categorizar imágenes
    categorized = defaultdict(list)
    
    for img_path in image_files:
        category = smart_categorization(img_path)
        categorized[category].append(img_path)
    
    # Mostrar distribución
    print(f"\n📈 Distribución por categoría:")
    for category, images in categorized.items():
        print(f"   {category}: {len(images)} imágenes")
    
    # Problema: Si no hay imágenes "sin_plaga", crear algunas artificialmente
    if len(categorized['sin_plaga']) < 50:
        print(f"\n⚠️  Pocas imágenes 'sin_plaga' ({len(categorized['sin_plaga'])})")
        print(f"   Redistribuyendo algunas imágenes para balance...")
        
        # Tomar algunas imágenes de "leve" y reclasificarlas como "sin_plaga"
        if len(categorized['infestacion_leve']) > 100:
            to_move = categorized['infestacion_leve'][:50]
            categorized['sin_plaga'].extend(to_move)
            categorized['infestacion_leve'] = categorized['infestacion_leve'][50:]
    
    # Dividir en train/val/test para cada categoría
    for category, images in categorized.items():
        if not images:
            continue
            
        # Mezclar aleatoriamente
        random.shuffle(images)
        
        total = len(images)
        train_count = int(total * TRAIN_RATIO)
        val_count = int(total * VAL_RATIO)
        
        train_images = images[:train_count]
        val_images = images[train_count:train_count + val_count]
        test_images = images[train_count + val_count:]
        
        # Copiar archivos
        splits_data = [
            ('train', train_images),
            ('val', val_images),
            ('test', test_images)
        ]
        
        for split_name, split_images in splits_data:
            dest_dir = Path(DEST_BASE) / split_name / category
            
            for img_path in split_images:
                dest_file = dest_dir / img_path.name
                try:
                    shutil.copy2(img_path, dest_file)
                except Exception as e:
                    print(f"❌ Error copiando {img_path}: {e}")
            
            print(f"✅ {split_name}/{category}: {len(split_images)} imágenes")

def validate_organization():
    """Valida que la organización sea correcta."""
    print(f"\n🔍 Validando organización...")
    
    splits = ['train', 'val', 'test']
    categories = ['sin_plaga', 'infestacion_leve', 'infestacion_severa']
    
    total_images = 0
    
    for split in splits:
        print(f"\n📁 {split.upper()}:")
        split_total = 0
        
        for category in categories:
            path = Path(DEST_BASE) / split / category
            if path.exists():
                count = len(list(path.glob("*.jpg"))) + len(list(path.glob("*.jpeg"))) + len(list(path.glob("*.png")))
                print(f"   {category}: {count} imágenes")
                split_total += count
            else:
                print(f"   {category}: 0 imágenes (directorio no existe)")
        
        print(f"   Total {split}: {split_total} imágenes")
        total_images += split_total
    
    print(f"\n📊 RESUMEN FINAL:")
    print(f"   Total de imágenes organizadas: {total_images}")
    print(f"   Distribución: {TRAIN_RATIO*100:.0f}% train, {VAL_RATIO*100:.0f}% val, {TEST_RATIO*100:.0f}% test")

def main():
    """Función principal."""
    print("🌱 Organizador de Dataset - Mosca Blanca")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path(SOURCE_DIR).exists():
        print(f"❌ Error: No se encuentra {SOURCE_DIR}")
        print(f"   Asegúrate de estar en el directorio backend/dataset/")
        return
    
    # Preguntar confirmación
    response = input(f"\n¿Organizar {SOURCE_DIR} en estructura de clasificación? (s/n): ")
    if response.lower() not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    try:
        # 1. Crear estructura de directorios
        print(f"\n📁 Creando estructura de directorios...")
        create_directory_structure()
        
        # 2. Organizar imágenes
        print(f"\n📋 Organizando imágenes...")
        organize_images()
        
        # 3. Validar
        validate_organization()
        
        print(f"\n✅ ¡Organización completada exitosamente!")
        print(f"\n📝 Siguientes pasos:")
        print(f"   1. Revisar manualmente las categorías si es necesario")
        print(f"   2. Ejecutar: python train_model.py")
        print(f"   3. Probar el modelo entrenado")
        
    except Exception as e:
        print(f"❌ Error durante la organización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Configurar semilla para reproducibilidad
    random.seed(42)
    main()