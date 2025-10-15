#!/usr/bin/env python3
"""
Script para probar la API de detección de mosca blanca
"""

import requests
import json
from pathlib import Path

def test_api():
    api_url = "http://localhost:8000"
    
    print("🧪 Probando API de detección de mosca blanca...")
    
    # 1. Probar endpoint de salud
    try:
        print("\n1. Probando endpoint de salud...")
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            print("✅ API saludable:", response.json())
        else:
            print("❌ Problema con API:", response.status_code)
            return
    except Exception as e:
        print("❌ Error conectando a API:", e)
        return
    
    # 2. Probar endpoint principal
    try:
        print("\n2. Probando endpoint principal...")
        response = requests.get(f"{api_url}/")
        if response.status_code == 200:
            print("✅ API principal:", response.json())
        else:
            print("❌ Problema con endpoint principal:", response.status_code)
    except Exception as e:
        print("❌ Error en endpoint principal:", e)
    
    # 3. Probar clases disponibles
    try:
        print("\n3. Probando clases disponibles...")
        response = requests.get(f"{api_url}/classes")
        if response.status_code == 200:
            print("✅ Clases disponibles:", response.json())
        else:
            print("❌ Problema obteniendo clases:", response.status_code)
    except Exception as e:
        print("❌ Error obteniendo clases:", e)
    
    # 4. Buscar imágenes para probar
    print("\n4. Buscando imágenes de prueba...")
    dataset_path = Path("../backend/dataset/test")
    
    if dataset_path.exists():
        for class_folder in dataset_path.iterdir():
            if class_folder.is_dir():
                images = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.png")) + list(class_folder.glob("*.jpeg"))
                if images:
                    test_image = images[0]
                    print(f"\n5. Probando detección con imagen: {test_image}")
                    
                    try:
                        with open(test_image, 'rb') as img_file:
                            files = {'file': ('test.jpg', img_file, 'image/jpeg')}
                            response = requests.post(f"{api_url}/detect", files=files)
                            
                        if response.status_code == 200:
                            result = response.json()
                            print("✅ Detección exitosa!")
                            print(f"   Clase: {result['prediction']['class']}")
                            print(f"   Confianza: {result['prediction']['confidence']:.2%}")
                            print(f"   Severidad: {result['prediction']['severity_level']}")
                            print(f"   Recomendaciones: {len(result['recommendations'])} sugerencias")
                        else:
                            print(f"❌ Error en detección: {response.status_code}")
                            print(f"   Respuesta: {response.text}")
                    except Exception as e:
                        print(f"❌ Error procesando imagen: {e}")
                    break
    else:
        print("❌ No se encontró directorio de dataset para pruebas")
        print("   Puedes usar cualquier imagen desde la app Flutter")

if __name__ == "__main__":
    test_api()