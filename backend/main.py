# main.py - Backend FastAPI para detección de mosca blanca
"""
API REST para el sistema de detección de mosca blanca en cultivos hidropónicos.
Incluye endpoints para análisis de imágenes, entrenamiento y estadísticas.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
from PIL import Image
import io
from datetime import datetime
from typing import List, Dict
import json
import os

app = FastAPI(title="Sistema Detección Mosca Blanca", version="1.0.0")

# Configurar CORS para Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración global
IMG_SIZE = (224, 224)
MODEL_PATH = "models/whitefly_detector.h5"
CONFIDENCE_THRESHOLD = 0.7

class WhiteflyDetector:
    """Detector de mosca blanca usando CNN."""
    
    def __init__(self):
        self.model = None
        self.load_or_create_model()
    
    def create_model(self):
        """Crea un modelo CNN basado en MobileNetV2."""
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*IMG_SIZE, 3)
        )
        
        # Congelar las capas base
        base_model.trainable = False
        
        # Agregar capas personalizadas
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.3)(x)
        
        # Capa de salida: 3 clases (sin_plaga, infestacion_leve, infestacion_severa)
        predictions = Dense(3, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def load_or_create_model(self):
        """Carga el modelo entrenado o crea uno nuevo."""
        if os.path.exists(MODEL_PATH):
            print(f"Cargando modelo desde {MODEL_PATH}")
            self.model = keras.models.load_model(MODEL_PATH)
        else:
            print("Creando nuevo modelo...")
            self.model = self.create_model()
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Preprocesa la imagen para el modelo."""
        # Convertir bytes a imagen PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar
        image = image.resize(IMG_SIZE)
        
        # Convertir a array y normalizar
        img_array = img_to_array(image)
        img_array = img_array / 255.0
        
        # Agregar dimensión de batch
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def detect_advanced(self, image_bytes: bytes) -> Dict:
        """
        Detección avanzada con análisis visual complementario.
        Combina CNN con procesamiento de imágenes tradicional.
        """
        # Predicción con CNN
        img_array = self.preprocess_image(image_bytes)
        predictions = self.model.predict(img_array, verbose=0)
        
        # Obtener clase y confianza
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        classes = ['sin_plaga', 'infestacion_leve', 'infestacion_severa']
        detected_class = classes[class_idx]
        
        # Análisis complementario con OpenCV
        image = Image.open(io.BytesIO(image_bytes))
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        additional_analysis = self.analyze_with_opencv(cv_image)
        
        return {
            'clase': detected_class,
            'confianza': confidence,
            'distribuciones': {
                'sin_plaga': float(predictions[0][0]),
                'leve': float(predictions[0][1]),
                'severa': float(predictions[0][2])
            },
            'analisis_visual': additional_analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_with_opencv(self, image: np.ndarray) -> Dict:
        """Análisis complementario con OpenCV."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detectar regiones brillantes (posibles moscas blancas)
        _, binary = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar por tamaño
        valid_contours = [c for c in contours if 15 < cv2.contourArea(c) < 300]
        
        # Analizar distribución
        if len(valid_contours) > 0:
            areas = [cv2.contourArea(c) for c in valid_contours]
            area_promedio = np.mean(areas)
            area_std = np.std(areas)
        else:
            area_promedio = 0
            area_std = 0
        
        return {
            'contornos_detectados': len(valid_contours),
            'area_promedio': float(area_promedio),
            'desviacion_areas': float(area_std),
            'densidad_estimada': len(valid_contours) / (image.shape[0] * image.shape[1]) * 10000
        }
    
    def generate_recommendations(self, detection_result: Dict) -> List[str]:
        """Genera recomendaciones basadas en la detección."""
        clase = detection_result['clase']
        confianza = detection_result['confianza']
        contornos = detection_result['analisis_visual']['contornos_detectados']
        
        recommendations = []
        
        if clase == 'sin_plaga' and confianza > 0.8:
            recommendations.extend([
                "✅ El cultivo se encuentra saludable",
                "Mantener monitoreo preventivo semanal",
                "Revisar condiciones de humedad y temperatura",
                "Verificar sistema de ventilación"
            ])
        
        elif clase == 'infestacion_leve' or (clase == 'sin_plaga' and contornos > 5):
            recommendations.extend([
                "⚠️ Infestación leve detectada",
                "Realizar inspección visual detallada",
                "Aplicar jabón potásico (5ml/L agua) como tratamiento preventivo",
                "Instalar trampas amarillas adhesivas",
                "Aumentar frecuencia de monitoreo a cada 2-3 días",
                "Revisar plantas cercanas"
            ])
        
        elif clase == 'infestacion_severa':
            recommendations.extend([
                "🚨 ALERTA: Infestación severa detectada",
                "Acción inmediata requerida",
                "Aislar plantas afectadas",
                "Aplicar aceite de neem (2ml/L) + jabón potásico (5ml/L)",
                "Considerar control biológico: Encarsia formosa o Eretmocerus eremicus",
                "Lavar hojas con chorro de agua (bajo presión)",
                "Mejorar ventilación del cultivo",
                "Monitoreo diario obligatorio",
                "Evaluar eliminación de plantas severamente afectadas"
            ])
        
        # Recomendaciones generales
        recommendations.append("\n📋 Recomendaciones generales:")
        recommendations.append("- Temperatura óptima: 18-24°C")
        recommendations.append("- Humedad relativa: 50-70%")
        recommendations.append("- pH solución nutritiva: 5.5-6.5")
        
        return recommendations

# Instancia global del detector
detector = WhiteflyDetector()

# Almacenamiento en memoria (en producción usar base de datos)
historial_detecciones = []

@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "nombre": "API Detección Mosca Blanca",
        "version": "1.0.0",
        "autor": "Kevin Mateo Santiago Salas",
        "universidad": "Universidad de Investigación y Desarrollo",
        "descripcion": "Sistema inteligente para detección de plagas en cultivos hidropónicos"
    }

@app.post("/api/detectar")
async def detectar_plaga(file: UploadFile = File(...)):
    """
    Endpoint principal para detectar mosca blanca en una imagen.
    
    Args:
        file: Archivo de imagen (JPG, PNG)
    
    Returns:
        JSON con resultado de detección y recomendaciones
    """
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Leer imagen
        contents = await file.read()
        
        # Realizar detección
        resultado = detector.detect_advanced(contents)
        
        # Generar recomendaciones
        recomendaciones = detector.generate_recommendations(resultado)
        
        # Crear respuesta completa
        response = {
            'exito': True,
            'deteccion': resultado,
            'recomendaciones': recomendaciones,
            'ubicacion': 'Mesa de los Santos, Colombia',
            'clima': 'Cálido',
            'fecha_analisis': datetime.now().isoformat()
        }
        
        # Guardar en historial
        historial_detecciones.append(response)
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en detección: {str(e)}")

@app.get("/api/historial")
async def obtener_historial(limite: int = 10):
    """Obtiene el historial de detecciones."""
    return {
        'total': len(historial_detecciones),
        'detecciones': historial_detecciones[-limite:]
    }

@app.get("/api/estadisticas")
async def obtener_estadisticas():
    """Calcula estadísticas del historial."""
    if not historial_detecciones:
        return {'mensaje': 'No hay datos suficientes'}
    
    total = len(historial_detecciones)
    sin_plaga = sum(1 for d in historial_detecciones if d['deteccion']['clase'] == 'sin_plaga')
    leve = sum(1 for d in historial_detecciones if d['deteccion']['clase'] == 'infestacion_leve')
    severa = sum(1 for d in historial_detecciones if d['deteccion']['clase'] == 'infestacion_severa')
    
    return {
        'total_analisis': total,
        'distribucion': {
            'sin_plaga': sin_plaga,
            'infestacion_leve': leve,
            'infestacion_severa': severa
        },
        'porcentajes': {
            'sin_plaga': round(sin_plaga/total*100, 2),
            'infestacion_leve': round(leve/total*100, 2),
            'infestacion_severa': round(severa/total*100, 2)
        }
    }

@app.get("/api/salud")
async def verificar_salud():
    """Verifica el estado del servicio."""
    return {
        'estado': 'operativo',
        'modelo_cargado': detector.model is not None,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)