# train_model.py - Entrenamiento del modelo de detección
"""
Script para entrenar el modelo CNN con imágenes etiquetadas de Roboflow.
Soporta data augmentation y validación cruzada.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import json
from sklearn.utils.class_weight import compute_class_weight

# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Rutas (ajustar según tu estructura)
DATA_DIR = 'dataset/'  # Carpeta con subcarpetas: sin_plaga, leve, severa
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'val')
TEST_DIR = os.path.join(DATA_DIR, 'test')
MODEL_DIR = 'models/'

class WhiteflyModelTrainer:
    """Clase para entrenar el modelo de detección."""
    
    def __init__(self):
        self.model = None
        self.history = None
        
    def create_data_generators(self):
        """
        Crea generadores de datos con data augmentation.
        El data augmentation es crucial para mejorar la generalización.
        """
        # Generador para entrenamiento con augmentation agresivo
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=40,
            width_shift_range=0.3,
            height_shift_range=0.3,
            shear_range=0.3,
            zoom_range=0.3,
            horizontal_flip=True,
            vertical_flip=True,
            brightness_range=[0.7, 1.3],
            fill_mode='nearest'
        )
        
        # Generador para validación (solo normalización)
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Cargar imágenes
        train_generator = train_datagen.flow_from_directory(
            TRAIN_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            VAL_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )
        
        test_generator = val_datagen.flow_from_directory(
            TEST_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"\n📊 Distribución del dataset:")
        print(f"   Entrenamiento: {train_generator.samples} imágenes")
        print(f"   Validación: {val_generator.samples} imágenes")
        print(f"   Prueba: {test_generator.samples} imágenes")
        print(f"\n🏷️  Clases: {train_generator.class_indices}")
        
        return train_generator, val_generator, test_generator
    
    def build_model(self):
        """Construye el modelo CNN optimizado."""
        # Cargar modelo base pre-entrenado
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*IMG_SIZE, 3)
        )
        
        # Descongelar las últimas capas para fine-tuning
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        for layer in base_model.layers[-30:]:
            layer.trainable = True
        
        # Construir arquitectura
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = BatchNormalization()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.4)(x)
        x = BatchNormalization()(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.3)(x)
        
        # Capa de salida
        predictions = Dense(3, activation='softmax', name='output')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compilar con métricas relevantes
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall'),
                keras.metrics.AUC(name='auc')
            ]
        )
        
        self.model = model
        print("\n✅ Modelo construido exitosamente")
        print(f"📝 Total de parámetros: {model.count_params():,}")
        
        return model
    
    def create_callbacks(self):
        """Crea callbacks para el entrenamiento."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        callbacks = [
            # Guardar mejor modelo
            ModelCheckpoint(
                filepath=os.path.join(MODEL_DIR, f'best_model_{timestamp}.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            
            # Early stopping
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Reducir learning rate
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            
            # TensorBoard
            TensorBoard(
                log_dir=f'logs/{timestamp}',
                histogram_freq=1,
                write_graph=True
            )
        ]
        
        return callbacks
    
    def train(self, train_gen, val_gen):
        """Entrena el modelo."""
        print("\n🚀 Iniciando entrenamiento...")
        
        # Calcular class_weight para balancear las clases
        # Obtener las etiquetas del generador de entrenamiento
        train_labels = []
        
        # Iterar sobre el generador para obtener todas las etiquetas
        print("📊 Calculando distribución de clases...")
        for i in range(len(train_gen)):
            batch_x, batch_y = train_gen[i]
            # Convertir one-hot a índices de clase
            batch_labels = np.argmax(batch_y, axis=1)
            train_labels.extend(batch_labels)
        
        # Resetear el generador
        train_gen.reset()
        
        train_labels = np.array(train_labels)
        
        # Calcular pesos automáticamente
        class_weights = compute_class_weight(
            'balanced',
            classes=np.unique(train_labels),
            y=train_labels
        )
        
        # Convertir a diccionario
        class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
        
        print(f"📊 Distribución de clases encontrada:")
        unique, counts = np.unique(train_labels, return_counts=True)
        for class_idx, count in zip(unique, counts):
            class_name = ['infestacion_leve', 'infestacion_severa', 'sin_plaga'][class_idx]
            print(f"   Clase {class_idx} ({class_name}): {count} muestras")
        
        print(f"📊 Pesos de clases calculados: {class_weight_dict}")
        
        callbacks = self.create_callbacks()
        
        self.history = self.model.fit(
            train_gen,
            epochs=EPOCHS,
            validation_data=val_gen,
            class_weight=class_weight_dict,  # 🔥 Balance de clases
            callbacks=callbacks,
            verbose=1
        )
        
        print("\n✅ Entrenamiento completado")
        
        return self.history
    
    def evaluate(self, test_gen):
        """Evalúa el modelo en el conjunto de prueba."""
        print("\n📊 Evaluando modelo...")
        
        results = self.model.evaluate(test_gen, verbose=1)
        
        metrics = {
            'loss': results[0],
            'accuracy': results[1],
            'precision': results[2],
            'recall': results[3],
            'auc': results[4]
        }
        
        # Calcular F1-score
        if metrics['precision'] + metrics['recall'] > 0:
            metrics['f1_score'] = 2 * (metrics['precision'] * metrics['recall']) / \
                                   (metrics['precision'] + metrics['recall'])
        else:
            metrics['f1_score'] = 0
        
        print("\n📈 Resultados en conjunto de prueba:")
        for metric, value in metrics.items():
            print(f"   {metric.capitalize()}: {value:.4f}")
        
        return metrics
    
    def plot_training_history(self):
        """Genera gráficas del entrenamiento."""
        if self.history is None:
            print("No hay historial de entrenamiento")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Exactitud del Modelo')
        axes[0, 0].set_xlabel('Época')
        axes[0, 0].set_ylabel('Exactitud')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Pérdida del Modelo')
        axes[0, 1].set_xlabel('Época')
        axes[0, 1].set_ylabel('Pérdida')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(self.history.history['precision'], label='Train')
        axes[1, 0].plot(self.history.history['val_precision'], label='Validation')
        axes[1, 0].set_title('Precisión del Modelo')
        axes[1, 0].set_xlabel('Época')
        axes[1, 0].set_ylabel('Precisión')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(self.history.history['recall'], label='Train')
        axes[1, 1].plot(self.history.history['val_recall'], label='Validation')
        axes[1, 1].set_title('Recall del Modelo')
        axes[1, 1].set_xlabel('Época')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'training_results_{timestamp}.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráficas guardadas: training_results_{timestamp}.png")
        plt.show()
    
    def save_model(self, filename='whitefly_detector.h5'):
        """Guarda el modelo entrenado."""
        filepath = os.path.join(MODEL_DIR, filename)
        self.model.save(filepath)
        print(f"\n💾 Modelo guardado: {filepath}")
        
        # Guardar configuración
        config = {
            'img_size': IMG_SIZE,
            'classes': ['sin_plaga', 'infestacion_leve', 'infestacion_severa'],
            'timestamp': datetime.now().isoformat(),
            'epochs_trained': len(self.history.history['loss']) if self.history else 0
        }
        
        config_path = os.path.join(MODEL_DIR, 'model_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

def main():
    """Función principal de entrenamiento."""
    print("="*60)
    print("🌱 SISTEMA DE DETECCIÓN DE MOSCA BLANCA - ENTRENAMIENTO")
    print("="*60)
    
    # Crear directorios
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Inicializar trainer
    trainer = WhiteflyModelTrainer()
    
    # Crear generadores de datos
    train_gen, val_gen, test_gen = trainer.create_data_generators()
    
    # Construir modelo
    model = trainer.build_model()
    model.summary()
    
    # Entrenar
    trainer.train(train_gen, val_gen)
    
    # Evaluar
    metrics = trainer.evaluate(test_gen)
    
    # Visualizar resultados
    trainer.plot_training_history()
    
    # Guardar modelo
    trainer.save_model()
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60)

if __name__ == "__main__":
    main()