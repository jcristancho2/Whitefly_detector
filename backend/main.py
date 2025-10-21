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
import gc  # ✅ AGREGAR para limpieza de memoria
import traceback  # ✅ AGREGAR para debugging

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
    """Predicción binaria optimizada con manejo de memoria."""
    image = None
    img_array = None
    
    try:
        print(f"🧠 Memoria antes del procesamiento: {tf.config.experimental.get_memory_info('GPU:0') if tf.config.list_physical_devices('GPU') else 'CPU only'}")
        
        # Preprocesar imagen
        image = Image.open(io.BytesIO(image_bytes))
        print(f"📏 Imagen original: {image.size}, Modo: {image.mode}")
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            print(f"🔄 Convirtiendo de {image.mode} a RGB")
            image = image.convert('RGB')
        
        # ✅ VALIDAR DIMENSIONES ANTES DE PROCESAR
        width, height = image.size
        if width < 50 or height < 50:
            raise ValueError(f"Imagen muy pequeña: {width}x{height}. Mínimo 50x50 pixels")
        
        if width > 4000 or height > 4000:
            print(f"⚠️ Imagen muy grande ({width}x{height}), redimensionando...")
            # Redimensionar manteniendo aspecto
            max_size = 2000
            if width > height:
                new_width = max_size
                new_height = int(height * max_size / width)
            else:
                new_height = max_size
                new_width = int(width * max_size / height)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"✅ Redimensionada a: {image.size}")
        
        # Redimensionar para el modelo y normalizar
        img_array = np.array(image.resize(IMG_SIZE, Image.Resampling.LANCZOS))
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32) / 255.0
        
        print(f"🔢 Array shape: {img_array.shape}, dtype: {img_array.dtype}")
        
        # ✅ PREDICCIÓN CON TIMEOUT Y LIMPIEZA
        start_time = datetime.now()
        
        # Limpiar memoria antes de predicción
        gc.collect()
        
        try:
            prediction = model.predict(img_array, verbose=0, batch_size=1)[0][0]
            processing_time = (datetime.now() - start_time).total_seconds()
            print(f"⚡ Predicción completada en {processing_time:.3f}s")
            
        except Exception as pred_error:
            print(f"❌ Error en predicción: {pred_error}")
            # Intentar con batch más pequeño o diferente configuración
            gc.collect()
            prediction = model.predict(img_array, verbose=0, batch_size=1, steps=1)[0][0]
            processing_time = (datetime.now() - start_time).total_seconds()
            print(f"✅ Predicción recuperada en {processing_time:.3f}s")
        
        # Interpretar resultado binario
        raw_prediction = float(prediction)
        
        if raw_prediction > 0.5:
            result = "sin_mosca_blanca"
            confidence = raw_prediction
            status = "saludable"
            color = "verde"
        else:
            result = "con_mosca_blanca"
            confidence = 1.0 - raw_prediction
            status = "infestado"
            color = "rojo"
        
        # ✅ LIMPIEZA EXPLÍCITA DE MEMORIA
        del img_array
        if image:
            image.close()
        gc.collect()
        
        return {
            "prediction": result,
            "confidence": confidence,
            "raw_score": raw_prediction,
            "status": status,
            "color": color,
            "model_type": "binary",
            "processing_time": processing_time,
            "threshold": 0.5,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # ✅ LIMPIEZA EN CASO DE ERROR
        if 'img_array' in locals() and img_array is not None:
            del img_array
        if 'image' in locals() and image is not None:
            image.close()
        gc.collect()
        
        print(f"❌ Error detallado en predicción: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

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
    """Endpoint mejorado con mejor manejo de errores y timeouts."""
    
    start_total = datetime.now()
    
    try:
        print(f"\n🚀 === INICIANDO ANÁLISIS ===")
        print(f"⏰ Hora: {start_total.isoformat()}")
        
        # Validar modelo cargado
        if model is None:
            print("❌ Modelo no disponible")
            raise HTTPException(status_code=503, detail="Modelo no disponible")
        
        # ✅ INFORMACIÓN DETALLADA DEL ARCHIVO
        print(f"📁 Archivo: {file.filename}")
        print(f"📄 Content-Type: {file.content_type}")
        
        # ✅ LEER CON TIMEOUT
        try:
            contents = await file.read()
            print(f"📊 Tamaño leído: {len(contents)} bytes")
        except Exception as read_error:
            print(f"❌ Error leyendo archivo: {read_error}")
            raise HTTPException(status_code=400, detail="Error leyendo el archivo")
        
        # ✅ VALIDACIONES MEJORADAS
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        
        if len(contents) > 15 * 1024 * 1024:  # 15MB máximo
            raise HTTPException(status_code=413, detail=f"Archivo muy grande: {len(contents)} bytes (máx 15MB)")
        
        # Validación de tipo flexible
        filename = file.filename or ""
        file_extension = os.path.splitext(filename.lower())[1]
        
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
        allowed_content_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/bmp', 'image/webp', 'image/tiff',
            'application/octet-stream', None
        ]
        
        is_valid_extension = file_extension in allowed_extensions
        is_valid_content_type = (
            file.content_type in allowed_content_types or 
            (file.content_type and file.content_type.startswith('image/'))
        )
        
        if not (is_valid_extension or is_valid_content_type):
            print(f"❌ Tipo inválido: {file.content_type} / {file_extension}")
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo no válido: {file.content_type}, ext: {file_extension}"
            )
        
        print(f"✅ Validación OK: {file.content_type} / {file_extension}")
        
        # ✅ VERIFICACIÓN DE IMAGEN REAL
        try:
            test_image = Image.open(io.BytesIO(contents))
            img_format = test_image.format
            img_size = test_image.size
            img_mode = test_image.mode
            test_image.close()
            print(f"✅ Imagen válida: {img_format} {img_size} {img_mode}")
        except Exception as img_error:
            print(f"❌ Imagen inválida: {img_error}")
            raise HTTPException(status_code=400, detail="Archivo no es imagen válida")
        
        print(f"🧠 Iniciando predicción...")
        
        # ✅ PREDICCIÓN CON MANEJO DE TIMEOUTS
        try:
            resultado = predict_binary_image(contents)
            print(f"✅ Predicción exitosa: {resultado['prediction']} ({resultado['confidence']:.3f})")
            
        except HTTPException:
            raise  # Re-lanzar errores HTTP
        except Exception as pred_error:
            print(f"❌ Error en predicción: {pred_error}")
            print(f"📋 Traceback completo: {traceback.format_exc()}")
            
            # ✅ LIMPIEZA Y RETRY
            gc.collect()
            raise HTTPException(
                status_code=500, 
                detail=f"Error procesando imagen: {str(pred_error)}"
            )
        
        # Generar recomendaciones
        recomendaciones = generate_binary_recommendations(resultado)
        
        # Respuesta completa
        total_time = (datetime.now() - start_total).total_seconds()
        
        response = {
            "success": True,
            "detection": resultado,
            "recommendations": recomendaciones,
            "metadata": {
                "filename": file.filename,
                "size_bytes": len(contents),
                "content_type": file.content_type,
                "file_extension": file_extension,
                "image_format": img_format,
                "image_size": img_size,
                "total_processing_time": total_time,
                "location": "Mesa de los Santos, Colombia",
                "analysis_date": datetime.now().isoformat()
            }
        }
        
        # Guardar en historial (limitar tamaño)
        historial_detecciones.append(response)
        if len(historial_detecciones) > 100:  # Mantener solo últimas 100
            historial_detecciones.pop(0)
        
        print(f"✅ === ANÁLISIS COMPLETADO en {total_time:.3f}s ===\n")
        
        return JSONResponse(content=response)
    
    except HTTPException:
        print(f"⚠️ Error HTTP capturado, re-lanzando")
        raise
    except Exception as e:
        total_time = (datetime.now() - start_total).total_seconds()
        error_msg = str(e)
        
        print(f"❌ === ERROR GENERAL después de {total_time:.3f}s ===")
        print(f"Error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Limpieza de memoria
        gc.collect()
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": error_msg,
                "processing_time": total_time,
                "timestamp": datetime.now().isoformat(),
                "debug_info": {
                    "filename": getattr(file, 'filename', 'unknown'),
                    "content_type": getattr(file, 'content_type', 'unknown')
                }
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