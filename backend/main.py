# main.py - Backend FastAPI para detección BINARIA de mosca blanca
"""
API REST para el sistema de detección BINARIA de mosca blanca en cultivos hidropónicos.
Versión optimizada para clasificación binaria: con_mosca_blanca vs sin_mosca_blanca
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from datetime import datetime
from typing import List, Dict
import os

app = FastAPI(title="Sistema Detección Mosca Blanca - Binario", version="2.0.0")

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
MODEL_PATH = "models/binary_whitefly_detector_20251021_011427.h5"

# Variable global para el modelo
model = None

def load_binary_model():
    """Cargar modelo binario."""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            print(f"✅ Cargando modelo binario desde: {MODEL_PATH}")
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"✅ Modelo binario cargado exitosamente")
            return True
        else:
            print(f"❌ Error: No se encuentra el modelo en {MODEL_PATH}")
            print("📁 Archivos disponibles en models/:")
            if os.path.exists("models/"):
                for f in os.listdir("models/"):
                    if f.endswith('.h5'):
                        print(f"   - {f}")
            return False
    except Exception as e:
        print(f"❌ Error al cargar modelo: {str(e)}")
        return False

def predict_binary_image(image_bytes: bytes) -> Dict:
    """Predicción binaria optimizada."""
    try:
        # Preprocesar imagen
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar y normalizar
        img_array = np.array(image.resize(IMG_SIZE))
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        # Predicción binaria
        start_time = datetime.now()
        prediction = model.predict(img_array, verbose=0)[0][0]
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Interpretar resultado binario
        if prediction > 0.5:
            result = "sin_mosca_blanca"
            confidence = float(prediction)
            status = "saludable"
            color = "verde"
        else:
            result = "con_mosca_blanca"
            confidence = float(1 - prediction)
            status = "infestado"
            color = "rojo"
        
        return {
            "prediction": result,
            "confidence": confidence,
            "raw_score": float(prediction),
            "status": status,
            "color": color,
            "model_type": "binary",
            "processing_time": processing_time,
            "threshold": 0.5,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción binaria: {str(e)}")

def generate_binary_recommendations(prediction_result: Dict) -> List[str]:
    """Genera recomendaciones para clasificación binaria."""
    result = prediction_result["prediction"]
    confidence = prediction_result["confidence"]
    
    recommendations = []
    
    if result == "sin_mosca_blanca":
        if confidence > 0.9:
            recommendations.extend([
                "✅ EXCELENTE: Cultivo saludable detectado",
                "🔍 Confianza muy alta en el diagnóstico",
                "📋 Mantener rutina de monitoreo preventivo semanal",
                "🌡️ Verificar condiciones ambientales óptimas",
                "💧 Revisar sistema de riego y drenaje"
            ])
        elif confidence > 0.7:
            recommendations.extend([
                "✅ BUENO: Cultivo aparentemente saludable",
                "🔍 Realizar inspección visual de confirmación",
                "📋 Monitoreo preventivo cada 3-4 días",
                "🌱 Verificar estado general de las plantas"
            ])
        else:
            recommendations.extend([
                "⚠️ PRECAUCIÓN: Resultado incierto",
                "🔍 Confianza moderada - revisar manualmente",
                "📸 Tomar nueva foto con mejor iluminación",
                "👁️ Inspección visual detallada recomendada"
            ])
    
    else:  # con_mosca_blanca
        if confidence > 0.9:
            recommendations.extend([
                "🚨 ALERTA ALTA: Infestación de mosca blanca detectada",
                "⚡ Acción inmediata requerida",
                "🔒 Aislar plantas afectadas inmediatamente",
                "💊 Aplicar tratamiento: aceite de neem (2ml/L) + jabón potásico (5ml/L)",
                "🪤 Instalar trampas amarillas adhesivas",
                "🌊 Lavar hojas con agua a presión moderada",
                "🔄 Control biológico: considerar Encarsia formosa",
                "📅 Monitoreo diario obligatorio",
                "🌡️ Mejorar ventilación del área de cultivo"
            ])
        elif confidence > 0.7:
            recommendations.extend([
                "⚠️ ADVERTENCIA: Posible presencia de mosca blanca",
                "🔍 Verificar con inspección visual detallada",
                "🪤 Instalar trampas amarillas como medida preventiva",
                "💧 Aplicar jabón potásico preventivo (3ml/L)",
                "📋 Aumentar frecuencia de monitoreo a cada 2 días",
                "👥 Revisar plantas adyacentes"
            ])
        else:
            recommendations.extend([
                "🤔 DUDOSO: Posible detección de mosca blanca",
                "📸 Tomar nuevas fotos desde diferentes ángulos",
                "🔍 Inspección visual cuidadosa requerida",
                "📋 Monitoreo preventivo aumentado"
            ])
    
    # Recomendaciones generales
    recommendations.extend([
        "",
        "📊 CONDICIONES ÓPTIMAS:",
        "🌡️ Temperatura: 18-24°C",
        "💧 Humedad relativa: 50-70%",
        "⚗️ pH solución nutritiva: 5.5-6.5",
        "💨 Ventilación adecuada esencial"
    ])
    
    return recommendations

# Cargar modelo al iniciar
load_binary_model()

# Almacenamiento en memoria
historial_detecciones = []

@app.get("/")
async def root():
    """Información de la API binaria."""
    return {
        "nombre": "API Detección Binaria Mosca Blanca",
        "version": "2.0.0",
        "tipo": "Clasificación Binaria",
        "clases": ["sin_mosca_blanca", "con_mosca_blanca"],
        "autor": "Kevin Mateo Santiago Salas",
        "universidad": "Universidad de Investigación y Desarrollo",
        "modelo_activo": MODEL_PATH.split('/')[-1] if model else "No cargado"
    }

@app.get("/health")
async def health_check():
    """Verificar salud del sistema."""
    return {
        "status": "healthy" if model else "unhealthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "timestamp": datetime.now().isoformat(),
        "type": "binary_classification"
    }

@app.post("/api/detectar")
async def detectar_plaga_binaria(file: UploadFile = File(...)):
    """
    Endpoint principal para detección BINARIA de mosca blanca.
    
    Args:
        file: Archivo de imagen (JPG, PNG, JPEG)
    
    Returns:
        JSON con resultado binario y recomendaciones
    """
    try:
        # Validar modelo cargado
        if model is None:
            raise HTTPException(status_code=503, detail="Modelo no disponible")
        
        # ✅ MEJORAR VALIDACIÓN DE TIPO DE ARCHIVO
        print(f"🔍 DEBUG: Archivo recibido - {file.filename}")
        print(f"🔍 DEBUG: Content-Type - {file.content_type}")
        
        # Leer contenido
        contents = await file.read()
        print(f"🔍 DEBUG: Tamaño - {len(contents)} bytes")
        
        # ✅ VALIDACIÓN MEJORADA - Verificar por extensión Y content-type
        filename = file.filename or ""
        file_extension = os.path.splitext(filename.lower())[1]
        
        # Extensiones permitidas
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        # Content-types permitidos (incluyendo casos problemáticos de Flutter)
        allowed_content_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/bmp', 'image/webp', 'application/octet-stream'
        ]
        
        # ✅ VALIDACIÓN FLEXIBLE - Permitir si extensión O content-type es válido
        is_valid_extension = file_extension in allowed_extensions
        is_valid_content_type = (
            file.content_type in allowed_content_types or 
            (file.content_type and file.content_type.startswith('image/'))
        )
        
        if not (is_valid_extension or is_valid_content_type):
            print(f"❌ Archivo rechazado: {file.content_type} / {file_extension}")
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no válido. Content-Type: {file.content_type}, Extensión: {file_extension}"
            )
        
        print(f"✅ Archivo aceptado: {file.content_type} / {file_extension}")
        
        # ✅ VALIDACIÓN ADICIONAL - Verificar que es imagen real usando PIL
        try:
            # Intentar abrir con PIL para confirmar que es imagen
            test_image = Image.open(io.BytesIO(contents))
            test_image.verify()  # Verificar que es imagen válida
            print(f"✅ Imagen válida confirmada: {test_image.format} {test_image.size}")
        except Exception as img_error:
            print(f"❌ No es imagen válida: {img_error}")
            raise HTTPException(status_code=400, detail="El archivo no es una imagen válida")
        
        # Resetear posición del archivo después de verify()
        contents_for_processing = contents  # Ya tenemos los bytes
        
        # Validar tamaño
        if len(contents) > 10 * 1024 * 1024:  # 10MB máximo
            raise HTTPException(status_code=413, detail="Imagen muy grande (máx 10MB)")
        
        print(f"🚀 Procesando imagen con modelo binario...")
        
        # Realizar predicción binaria
        resultado = predict_binary_image(contents_for_processing)
        
        # Generar recomendaciones
        recomendaciones = generate_binary_recommendations(resultado)
        
        # Respuesta completa
        response = {
            "success": True,
            "detection": resultado,
            "recommendations": recomendaciones,
            "metadata": {
                "filename": file.filename,
                "size_bytes": len(contents),
                "content_type": file.content_type,
                "file_extension": file_extension,
                "location": "Mesa de los Santos, Colombia",
                "analysis_date": datetime.now().isoformat()
            }
        }
        
        # Guardar en historial
        historial_detecciones.append(response)
        
        print(f"✅ Análisis completado: {resultado['prediction']} (confianza: {resultado['confidence']:.2f})")
        
        return JSONResponse(content=response)
    
    except HTTPException:
        # Re-lanzar HTTPExceptions (errores de validación)
        raise
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/historial")
async def obtener_historial(limite: int = 20):
    """Historial de detecciones binarias."""
    return {
        "total": len(historial_detecciones),
        "detections": historial_detecciones[-limite:] if historial_detecciones else []
    }

@app.get("/api/estadisticas")
async def obtener_estadisticas_binarias():
    """Estadísticas para clasificación binaria."""
    if not historial_detecciones:
        return {"message": "No hay datos suficientes"}
    
    total = len(historial_detecciones)
    sin_plaga = sum(1 for d in historial_detecciones 
                   if d["detection"]["prediction"] == "sin_mosca_blanca")
    con_plaga = total - sin_plaga
    
    # Confianza promedio
    confianzas = [d["detection"]["confidence"] for d in historial_detecciones]
    confianza_promedio = sum(confianzas) / len(confianzas)
    
    return {
        "total_analysis": total,
        "binary_distribution": {
            "sin_mosca_blanca": sin_plaga,
            "con_mosca_blanca": con_plaga
        },
        "percentages": {
            "healthy": round(sin_plaga/total*100, 2),
            "infested": round(con_plaga/total*100, 2)
        },
        "average_confidence": round(confianza_promedio, 4),
        "model_performance": "binary_classification"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)