import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20

def create_simple_model():
    """Crear un modelo más simple y robusto"""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # Congelar el modelo base
    
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 clases
    ])
    
    return model

def main():
    print("🔄 Creando modelo simple...")
    
    # Crear generadores más simples
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Generadores de entrenamiento y validación
    train_generator = datagen.flow_from_directory(
        'dataset/train',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = datagen.flow_from_directory(
        'dataset/train',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"📊 Clases detectadas: {train_generator.class_indices}")
    print(f"📊 Muestras de entrenamiento: {train_generator.samples}")
    print(f"📊 Muestras de validación: {val_generator.samples}")
    
    # Crear modelo
    model = create_simple_model()
    
    # Compilar
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Entrenar SIN class_weight primero
    print("🚀 Entrenando modelo simple...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        verbose=1
    )
    
    # Guardar modelo
    model.save('models/simple_whitefly_detector.h5')
    print("✅ Modelo guardado como simple_whitefly_detector.h5")
    
    # Evaluar en test set
    test_generator = ImageDataGenerator(rescale=1./255).flow_from_directory(
        'dataset/test',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    # Predicciones
    predictions = model.predict(test_generator)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes
    
    # Matriz de confusión
    cm = confusion_matrix(true_classes, predicted_classes)
    print("\n📊 Matriz de Confusión:")
    print(cm)
    
    # Reporte de clasificación
    class_names = list(test_generator.class_indices.keys())
    print(f"\n📊 Clases: {class_names}")
    print("\n📈 Reporte de Clasificación:")
    print(classification_report(true_classes, predicted_classes, target_names=class_names))
    
    # Probar predicción individual
    print("\n🧪 Probando predicción individual...")
    test_image_path = 'dataset/test/infestacion_leve/2014-09-16-13-11-07-004_9307_IJFR_jpg.rf.97a69b9f5ea4b474eb17fec117d0b781.jpg'
    
    if os.path.exists(test_image_path):
        # Cargar y procesar imagen
        img = tf.keras.preprocessing.image.load_img(test_image_path, target_size=IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        # Predicción
        pred = model.predict(img_array)
        predicted_class = np.argmax(pred[0])
        confidence = pred[0][predicted_class]
        
        print(f"🔍 Imagen de prueba: {test_image_path}")
        print(f"🎯 Predicción: {class_names[predicted_class]} (confianza: {confidence:.2%})")
        print(f"📊 Probabilidades: {dict(zip(class_names, pred[0]))}")

if __name__ == "__main__":
    main()