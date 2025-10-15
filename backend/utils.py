# utils.py - Scripts de utilidad para el proyecto
"""
Funciones auxiliares para preparación de datos, validación y análisis.
"""

import os
import shutil
from pathlib import Path
import numpy as np
import cv2
from PIL import Image
import json
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class DatasetPreparator:
    """Clase para preparar y organizar el dataset."""
    
    def __init__(self, source_dir: str, output_dir: str = 'dataset'):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        
    def organize_from_roboflow(self, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
        """
        Organiza imágenes exportadas de Roboflow en la estructura requerida.
        
        Args:
            train_ratio: Porcentaje para entrenamiento
            val_ratio: Porcentaje para validación
            test_ratio: Porcentaje para prueba
        """
        print("📁 Organizando dataset desde Roboflow...")
        
        # Crear directorios
        for split in ['train', 'val', 'test']:
            for clase in ['sin_plaga', 'infestacion_leve', 'infestacion_severa']:
                (self.output_dir / split / clase).mkdir(parents=True, exist_ok=True)
        
        # Procesar cada clase
        for clase in ['sin_plaga', 'infestacion_leve', 'infestacion_severa']:
            source_class_dir = self.source_dir / clase
            
            if not source_class_dir.exists():
                print(f"⚠️  Advertencia: No se encontró {source_class_dir}")
                continue
            
            # Obtener todas las imágenes
            images = list(source_class_dir.glob('*.jpg')) + \
                    list(source_class_dir.glob('*.jpeg')) + \
                    list(source_class_dir.glob('*.png'))
            
            if len(images) == 0:
                print(f"⚠️  No hay imágenes en {clase}")
                continue
            
            # Dividir dataset
            train_imgs, temp_imgs = train_test_split(
                images, 
                test_size=(val_ratio + test_ratio),
                random_state=42
            )
            
            val_imgs, test_imgs = train_test_split(
                temp_imgs,
                test_size=test_ratio/(val_ratio + test_ratio),
                random_state=42
            )
            
            # Copiar archivos
            for img in train_imgs:
                shutil.copy(img, self.output_dir / 'train' / clase / img.name)
            
            for img in val_imgs:
                shutil.copy(img, self.output_dir / 'val' / clase / img.name)
            
            for img in test_imgs:
                shutil.copy(img, self.output_dir / 'test' / clase / img.name)
            
            print(f"✅ {clase}: {len(train_imgs)} train, {len(val_imgs)} val, {len(test_imgs)} test")
        
        print("\n✨ Dataset organizado exitosamente")
    
    def validate_dataset(self):
        """Valida la estructura y calidad del dataset."""
        print("\n🔍 Validando dataset...")
        
        report = {
            'total_images': 0,
            'splits': {},
            'classes': {},
            'image_sizes': [],
            'issues': []
        }
        
        for split in ['train', 'val', 'test']:
            split_dir = self.output_dir / split
            
            if not split_dir.exists():
                report['issues'].append(f"Falta directorio: {split}")
                continue
            
            split_count = 0
            
            for clase in ['sin_plaga', 'infestacion_leve', 'infestacion_severa']:
                class_dir = split_dir / clase
                
                if not class_dir.exists():
                    report['issues'].append(f"Falta directorio: {split}/{clase}")
                    continue
                
                # Contar imágenes
                images = list(class_dir.glob('*.jpg')) + \
                        list(class_dir.glob('*.jpeg')) + \
                        list(class_dir.glob('*.png'))
                
                count = len(images)
                split_count += count
                
                if clase not in report['classes']:
                    report['classes'][clase] = 0
                report['classes'][clase] += count
                
                # Validar calidad de imágenes
                for img_path in images[:10]:  # Muestra de 10
                    try:
                        img = Image.open(img_path)
                        report['image_sizes'].append(img.size)
                        
                        # Verificar que no esté corrupta
                        img.verify()
                    except Exception as e:
                        report['issues'].append(f"Imagen corrupta: {img_path}")
            
            report['splits'][split] = split_count
            report['total_images'] += split_count
        
        # Imprimir reporte
        print("\n📊 Reporte del Dataset:")
        print(f"   Total de imágenes: {report['total_images']}")
        print(f"\n   Por división:")
        for split, count in report['splits'].items():
            print(f"      {split}: {count} imágenes")
        
        print(f"\n   Por clase:")
        for clase, count in report['classes'].items():
            percentage = (count / report['total_images'] * 100) if report['total_images'] > 0 else 0
            print(f"      {clase}: {count} ({percentage:.1f}%)")
        
        if report['image_sizes']:
            sizes = np.array(report['image_sizes'])
            print(f"\n   Tamaños de imagen:")
            print(f"      Promedio: {sizes.mean(axis=0).astype(int)}")
            print(f"      Mínimo: {sizes.min(axis=0)}")
            print(f"      Máximo: {sizes.max(axis=0)}")
        
        if report['issues']:
            print(f"\n⚠️  Problemas encontrados:")
            for issue in report['issues']:
                print(f"      - {issue}")
        else:
            print(f"\n✅ No se encontraron problemas")
        
        return report
    
    def augment_dataset(self, target_per_class: int = 500):
        """
        Aumenta el dataset aplicando transformaciones si hay pocas imágenes.
        """
        print(f"\n🔄 Aumentando dataset a {target_per_class} imágenes por clase...")
        
        import albumentations as A
        
        # Definir transformaciones
        transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.Rotate(limit=40, p=0.7),
            A.RandomBrightnessContrast(p=0.5),
            A.GaussNoise(p=0.3),
            A.Blur(blur_limit=3, p=0.3),
        ])
        
        for split in ['train']:  # Solo aumentar entrenamiento
            for clase in ['sin_plaga', 'infestacion_leve', 'infestacion_severa']:
                class_dir = self.output_dir / split / clase
                
                if not class_dir.exists():
                    continue
                
                images = list(class_dir.glob('*.jpg')) + \
                        list(class_dir.glob('*.jpeg')) + \
                        list(class_dir.glob('*.png'))
                
                current_count = len(images)
                
                if current_count >= target_per_class:
                    print(f"✅ {clase}: Ya tiene suficientes imágenes ({current_count})")
                    continue
                
                needed = target_per_class - current_count
                print(f"🔄 {clase}: Generando {needed} imágenes adicionales...")
                
                # Generar imágenes aumentadas
                generated = 0
                while generated < needed:
                    for img_path in images:
                        if generated >= needed:
                            break
                        
                        # Cargar imagen
                        image = cv2.imread(str(img_path))
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Aplicar transformación
                        transformed = transform(image=image)
                        augmented_img = transformed['image']
                        
                        # Guardar
                        output_path = class_dir / f"aug_{generated}_{img_path.name}"
                        augmented_img_bgr = cv2.cvtColor(augmented_img, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(str(output_path), augmented_img_bgr)
                        
                        generated += 1
                
                print(f"✅ {clase}: {current_count + generated} imágenes totales")

class ModelAnalyzer:
    """Analiza y visualiza el rendimiento del modelo."""
    
    def __init__(self, model_path: str):
        from tensorflow import keras
        self.model = keras.models.load_model(model_path)
        self.class_names = ['sin_plaga', 'infestacion_leve', 'infestacion_severa']
    
    def predict_image(self, image_path: str) -> Dict:
        """Predice una sola imagen y retorna resultados detallados."""
        from tensorflow.keras.preprocessing.image import load_img, img_to_array
        
        # Cargar y preprocesar
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predecir
        predictions = self.model.predict(img_array, verbose=0)[0]
        
        # Crear resultado
        result = {
            'predicted_class': self.class_names[np.argmax(predictions)],
            'confidence': float(np.max(predictions)),
            'probabilities': {
                name: float(prob) 
                for name, prob in zip(self.class_names, predictions)
            }
        }
        
        return result
    
    def analyze_test_set(self, test_dir: str):
        """Analiza el conjunto de prueba completo."""
        from sklearn.metrics import classification_report, confusion_matrix
        import seaborn as sns
        
        print("\n📊 Analizando conjunto de prueba...")
        
        y_true = []
        y_pred = []
        
        for i, clase in enumerate(self.class_names):
            class_dir = Path(test_dir) / clase
            
            if not class_dir.exists():
                continue
            
            images = list(class_dir.glob('*.jpg')) + \
                    list(class_dir.glob('*.jpeg')) + \
                    list(class_dir.glob('*.png'))
            
            for img_path in images:
                result = self.predict_image(str(img_path))
                y_true.append(i)
                y_pred.append(self.class_names.index(result['predicted_class']))
        
        # Reporte de clasificación
        print("\n📈 Reporte de Clasificación:")
        print(classification_report(
            y_true, 
            y_pred, 
            target_names=self.class_names,
            digits=4
        ))
        
        # Matriz de confusión
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names
        )
        plt.title('Matriz de Confusión')
        plt.ylabel('Verdadero')
        plt.xlabel('Predicho')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300)
        print("\n💾 Matriz de confusión guardada: confusion_matrix.png")
        plt.show()

def check_system_requirements():
    """Verifica que el sistema tenga todos los requisitos."""
    print("🔍 Verificando requisitos del sistema...\n")
    
    requirements = {
        'Python': True,
        'TensorFlow': False,
        'OpenCV': False,
        'FastAPI': False,
        'Pillow': False
    }
    
    # Verificar Python
    import sys
    python_version = sys.version_info
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Verificar paquetes
    try:
        import tensorflow as tf
        requirements['TensorFlow'] = True
        print(f"✅ TensorFlow {tf.__version__}")
    except ImportError:
        print("❌ TensorFlow no instalado")
    
    try:
        import cv2
        requirements['OpenCV'] = True
        print(f"✅ OpenCV {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV no instalado")
    
    try:
        import fastapi
        requirements['FastAPI'] = True
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI no instalado")
    
    try:
        from PIL import Image
        requirements['Pillow'] = True
        print(f"✅ Pillow instalado")
    except ImportError:
        print("❌ Pillow no instalado")
    
    # GPU
    print("\n🎮 GPU:")
    try:
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                print(f"✅ GPU detectada: {gpu.name}")
        else:
            print("⚠️  No se detectó GPU (usará CPU)")
    except:
        print("❓ No se pudo verificar GPU")
    
    # Verificar espacio en disco
    import psutil
    disk = psutil.disk_usage('.')
    free_gb = disk.free / (1024**3)
    print(f"\n💾 Espacio libre: {free_gb:.2f} GB")
    
    if free_gb < 5:
        print("⚠️  Advertencia: Poco espacio en disco")
    
    # Resumen
    print("\n" + "="*50)
    if all(requirements.values()):
        print("✅ Todos los requisitos están instalados")
    else:
        print("⚠️  Faltan dependencias. Ejecuta:")
        print("   pip install -r requirements.txt")
    print("="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python utils.py check          - Verificar requisitos")
        print("  python utils.py organize <dir> - Organizar dataset")
        print("  python utils.py validate       - Validar dataset")
        print("  python utils.py analyze <model>- Analizar modelo")
    else:
        command = sys.argv[1]
        
        if command == "check":
            check_system_requirements()
        
        elif command == "organize" and len(sys.argv) > 2:
            preparator = DatasetPreparator(sys.argv[2])
            preparator.organize_from_roboflow()
        
        elif command == "validate":
            preparator = DatasetPreparator('.')
            preparator.validate_dataset()
        
        elif command == "analyze" and len(sys.argv) > 2:
            analyzer = ModelAnalyzer(sys.argv[2])
            analyzer.analyze_test_set('dataset/test')
        
        else:
            print("❌ Comando no reconocido")