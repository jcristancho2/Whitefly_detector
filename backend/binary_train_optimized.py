import os
import shutil
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30

def create_balanced_binary_dataset():
    """Crear dataset binario perfectamente balanceado"""
    print("🔄 CREANDO DATASET BINARIO BALANCEADO")
    print("="*50)
    
    # Eliminar dataset anterior si existe
    if os.path.exists('dataset_binary'):
        shutil.rmtree('dataset_binary')
    
    # Crear estructura
    for split in ['train', 'val', 'test']:
        for class_name in ['sin_plaga', 'con_plaga']:
            os.makedirs(f'dataset_binary/{split}/{class_name}', exist_ok=True)
    
    # Recopilar todas las imágenes
    def get_all_images(base_path, class_name):
        """Obtener todas las imágenes de una clase de todos los splits"""
        all_images = []
        for split in ['train', 'val', 'test']:
            path = f'{base_path}/{split}/{class_name}'
            if os.path.exists(path):
                for img in os.listdir(path):
                    if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                        all_images.append((split, path, img))
        return all_images
    
    # Obtener todas las imágenes sin plaga
    sin_plaga_images = get_all_images('dataset', 'sin_plaga')
    
    # Obtener todas las imágenes con plaga (combinando leve + severa)
    con_plaga_images = []
    for plague_type in ['infestacion_leve', 'infestacion_severa']:
        plague_images = get_all_images('dataset', plague_type)
        for split, path, img in plague_images:
            # Agregar prefijo para evitar conflictos de nombres
            new_name = f"{plague_type}_{img}"
            con_plaga_images.append((split, path, img, new_name))
    
    print(f"📊 Imágenes disponibles:")
    print(f"  Sin Plaga: {len(sin_plaga_images)}")
    print(f"  Con Plaga: {len(con_plaga_images)}")
    
    # Balancear: usar 1400 de cada clase
    target_per_class = 1400
    
    # Mezclar aleatoriamente
    random.shuffle(sin_plaga_images)
    random.shuffle(con_plaga_images)
    
    # Seleccionar 1400 de cada una
    sin_plaga_selected = sin_plaga_images[:target_per_class]
    con_plaga_selected = con_plaga_images[:target_per_class]
    
    print(f"📊 Usando {len(sin_plaga_selected)} + {len(con_plaga_selected)} = {len(sin_plaga_selected) + len(con_plaga_selected)} imágenes")
    
    # Distribución: 70% train, 15% val, 15% test
    def split_data(images):
        train_size = int(len(images) * 0.70)  # 980
        val_size = int(len(images) * 0.15)    # 210
        test_size = len(images) - train_size - val_size  # 210
        
        return {
            'train': images[:train_size],
            'val': images[train_size:train_size + val_size],
            'test': images[train_size + val_size:]
        }
    
    # Dividir datasets
    sin_plaga_splits = split_data(sin_plaga_selected)
    con_plaga_splits = split_data(con_plaga_selected)
    
    # Copiar archivos
    def copy_images(splits, class_name, is_plague=False):
        counts = {}
        for split_name, images in splits.items():
            count = 0
            for item in images:
                if is_plague:
                    split, path, original_name, new_name = item
                    src = os.path.join(path, original_name)
                    dst = f'dataset_binary/{split_name}/{class_name}/{new_name}'
                else:
                    split, path, img_name = item
                    src = os.path.join(path, img_name)
                    dst = f'dataset_binary/{split_name}/{class_name}/{img_name}'
                
                shutil.copy2(src, dst)
                count += 1
            counts[split_name] = count
        return counts
    
    # Copiar imágenes
    sin_plaga_counts = copy_images(sin_plaga_splits, 'sin_plaga', False)
    con_plaga_counts = copy_images(con_plaga_splits, 'con_plaga', True)
    
    print(f"\n✅ DATASET BINARIO CREADO:")
    for split in ['train', 'val', 'test']:
        sp_count = sin_plaga_counts[split]
        cp_count = con_plaga_counts[split]
        total = sp_count + cp_count
        print(f"{split.upper()}:")
        print(f"  sin_plaga: {sp_count}")
        print(f"  con_plaga: {cp_count}")
        print(f"  Total: {total} (Balance: 50%/50% ✅)")
    
    total_final = sum(sin_plaga_counts.values()) + sum(con_plaga_counts.values())
    print(f"\nTOTAL: {total_final} imágenes")
    return True

def create_binary_model():
    """Crear modelo optimizado para clasificación binaria"""
    print("\n🏗️ CONSTRUYENDO MODELO BINARIO")
    
    # Modelo base
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Descongelar últimas capas para fine-tuning
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    # Arquitectura optimizada para binario
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid', name='output')  # Salida binaria
    ])
    
    # Compilar para clasificación binaria
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall'),
            tf.keras.metrics.AUC(name='auc')
        ]
    )
    
    print(f"✅ Modelo binario creado")
    print(f"📝 Parámetros: {model.count_params():,}")
    
    return model

def train_binary_model():
    """Entrenar el modelo binario"""
    print("\n🚀 ENTRENANDO MODELO BINARIO")
    print("="*50)
    
    # Crear generadores
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Cargar datos
    train_gen = train_datagen.flow_from_directory(
        'dataset_binary/train',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',  # Modo binario
        shuffle=True
    )
    
    val_gen = val_datagen.flow_from_directory(
        'dataset_binary/val',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )
    
    test_gen = val_datagen.flow_from_directory(
        'dataset_binary/test',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )
    
    print(f"📊 Clases detectadas: {train_gen.class_indices}")
    print(f"📊 Train: {train_gen.samples} | Val: {val_gen.samples} | Test: {test_gen.samples}")
    
    # Crear modelo
    model = create_binary_model()
    
    # Callbacks
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            f'models/best_binary_model_{timestamp}.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Entrenar
    print(f"🎯 Iniciando entrenamiento por {EPOCHS} épocas...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluar
    print(f"\n📊 EVALUACIÓN FINAL:")
    test_loss, test_acc, test_prec, test_rec, test_auc = model.evaluate(test_gen, verbose=1)
    
    # Calcular F1-Score
    f1_score = 2 * (test_prec * test_rec) / (test_prec + test_rec) if (test_prec + test_rec) > 0 else 0
    
    print(f"\n📈 RESULTADOS FINALES:")
    print(f"   Accuracy: {test_acc:.4f}")
    print(f"   Precision: {test_prec:.4f}")
    print(f"   Recall: {test_rec:.4f}")
    print(f"   F1-Score: {f1_score:.4f}")
    print(f"   AUC: {test_auc:.4f}")
    
    # Matriz de confusión
    predictions = model.predict(test_gen)
    predicted_classes = (predictions > 0.5).astype(int).flatten()
    true_classes = test_gen.classes
    
    cm = confusion_matrix(true_classes, predicted_classes)
    print(f"\n📊 MATRIZ DE CONFUSIÓN:")
    print(f"   [[Sin Plaga, Con Plaga]]")
    print(f"   {cm}")
    
    # Guardar modelo final
    os.makedirs('models', exist_ok=True)
    model.save('models/binary_whitefly_detector.h5')
    print(f"\n💾 Modelo guardado: models/binary_whitefly_detector.h5")
    
    # Gráficas
    plot_training_results(history, timestamp)
    
    # Prueba individual
    test_individual_prediction(model)
    
    return model

def plot_training_results(history, timestamp):
    """Crear gráficas de entrenamiento"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Train')
    axes[0, 0].plot(history.history['val_accuracy'], label='Validation')
    axes[0, 0].set_title('Accuracy - Modelo Binario')
    axes[0, 0].set_xlabel('Época')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Loss
    axes[0, 1].plot(history.history['loss'], label='Train')
    axes[0, 1].plot(history.history['val_loss'], label='Validation')
    axes[0, 1].set_title('Loss - Modelo Binario')
    axes[0, 1].set_xlabel('Época')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Precision
    axes[1, 0].plot(history.history['precision'], label='Train')
    axes[1, 0].plot(history.history['val_precision'], label='Validation')
    axes[1, 0].set_title('Precision - Modelo Binario')
    axes[1, 0].set_xlabel('Época')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Recall
    axes[1, 1].plot(history.history['recall'], label='Train')
    axes[1, 1].plot(history.history['val_recall'], label='Validation')
    axes[1, 1].set_title('Recall - Modelo Binario')
    axes[1, 1].set_xlabel('Época')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(f'binary_training_results_{timestamp}.png', dpi=300, bbox_inches='tight')
    print(f"📊 Gráficas guardadas: binary_training_results_{timestamp}.png")
    plt.show()

def test_individual_prediction(model):
    """Probar predicción individual"""
    print(f"\n🧪 PRUEBA INDIVIDUAL:")
    
    # Buscar una imagen de cada clase
    sin_plaga_path = None
    con_plaga_path = None
    
    if os.path.exists('dataset_binary/test/sin_plaga'):
        sin_plaga_files = os.listdir('dataset_binary/test/sin_plaga')
        if sin_plaga_files:
            sin_plaga_path = f"dataset_binary/test/sin_plaga/{sin_plaga_files[0]}"
    
    if os.path.exists('dataset_binary/test/con_plaga'):
        con_plaga_files = os.listdir('dataset_binary/test/con_plaga')
        if con_plaga_files:
            con_plaga_path = f"dataset_binary/test/con_plaga/{con_plaga_files[0]}"
    
    def predict_image(image_path, expected_class):
        if not os.path.exists(image_path):
            return
        
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        prediction = model.predict(img_array)[0][0]
        predicted_class = "Con Plaga" if prediction > 0.5 else "Sin Plaga"
        confidence = prediction if prediction > 0.5 else 1 - prediction
        
        print(f"🔍 {expected_class}:")
        print(f"   Imagen: {os.path.basename(image_path)}")
        print(f"   Predicción: {predicted_class} (confianza: {confidence:.2%})")
        print(f"   Raw Score: {prediction:.4f}")
    
    if sin_plaga_path:
        predict_image(sin_plaga_path, "Sin Plaga")
    
    if con_plaga_path:
        predict_image(con_plaga_path, "Con Plaga")

def main():
    """Función principal"""
    print("🌱 SISTEMA BINARIO DE DETECCIÓN DE MOSCA BLANCA")
    print("="*60)
    
    # Establecer semilla para reproducibilidad
    random.seed(42)
    tf.random.set_seed(42)
    np.random.seed(42)
    
    # Crear dataset balanceado
    if create_balanced_binary_dataset():
        print("\n✅ Dataset binario creado exitosamente")
        
        # Entrenar modelo
        model = train_binary_model()
        
        print(f"\n🎉 ¡ENTRENAMIENTO COMPLETADO!")
        print(f"💾 Modelo guardado como: models/binary_whitefly_detector.h5")
        print(f"🎯 Sistema listo para detectar: SIN PLAGA vs CON PLAGA")
    
    print("="*60)

if __name__ == "__main__":
    main()