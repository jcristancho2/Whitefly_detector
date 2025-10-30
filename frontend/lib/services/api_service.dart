import 'dart:convert';
import 'dart:io';
import 'dart:async'; // ← AÑADIR ESTE IMPORT para TimeoutException
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  final String baseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';

  /// Test de conexión ANTES de analizar
  Future<bool> testConnectionBeforeAnalysis() async {
    try {
      print('🔗 Verificando conexión antes de analizar...');

      final response = await http
          .get(
            Uri.parse('$baseUrl/health'),
            headers: {'Accept': 'application/json'},
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        print('✅ Backend accesible - Procediendo con análisis');
        return true;
      } else {
        print('❌ Backend no saludable: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ No se puede conectar al backend: $e');
      return false;
    }
  }

  /// Analizar imagen con verificación previa
  Future<Map<String, dynamic>?> analyzeImage(File image) async {
    try {
      print('🚀 INICIANDO ANÁLISIS DE IMAGEN');
      print('📁 Archivo: ${image.path}');
      print('📊 Tamaño: ${await image.length()} bytes');
      print('📡 URL: $baseUrl/api/detectar');

      // ✅ NUEVO: Verificar conexión PRIMERO
      bool canConnect = await testConnectionBeforeAnalysis();
      if (!canConnect) {
        throw Exception(
          'No se puede conectar al servidor en $baseUrl:8000. Verifica que esté corriendo.',
        );
      }

      // ✅ Verificar que el archivo existe
      if (!await image.exists()) {
        throw Exception('El archivo de imagen no existe');
      }

      // ✅ Verificar tamaño de imagen
      int fileSize = await image.length();
      if (fileSize > 10 * 1024 * 1024) {
        throw Exception('Imagen muy grande (${fileSize} bytes). Máximo 10MB');
      }

      print('✅ Archivo válido, enviando al servidor...');

      // ✅ Crear request con headers mejorados
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/api/detectar'),
      );

      // Agregar imagen
      request.files.add(await http.MultipartFile.fromPath('file', image.path));

      // Headers mejorados
      request.headers.addAll({
        'Accept': 'application/json',
        'User-Agent': 'WhiteflyDetectorApp/1.0',
      });

      print('📤 Enviando imagen (${fileSize} bytes)...');

      // ✅ Timeout progresivo con mejor manejo
      var response = await request.send().timeout(
        const Duration(seconds: 20), // Aumentado a 20 segundos
        onTimeout: () {
          print('⏰ TIMEOUT después de 20 segundos');
          throw TimeoutException(
            'El servidor tardó más de 20 segundos en responder. Intenta con una imagen más pequeña.',
            const Duration(seconds: 20),
          );
        },
      );

      print('📥 Respuesta recibida: ${response.statusCode}');

      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        print('📄 Datos recibidos: ${responseData.length} caracteres');

        try {
          var jsonData = json.decode(responseData);
          print('✅ Análisis exitoso: ${jsonData['detection']['prediction']}');
          print('🎯 Confianza: ${jsonData['detection']['confidence']}');

          return _mapBackendResponse(jsonData);
        } catch (jsonError) {
          print('❌ Error decodificando JSON: $jsonError');
          print('📄 Respuesta recibida: $responseData');
          throw Exception('Respuesta inválida del servidor');
        }
      } else {
        var errorData = await response.stream.bytesToString();
        print('❌ Error ${response.statusCode}: $errorData');
        throw Exception(
          'Error del servidor (${response.statusCode}): $errorData',
        );
      }
    } on TimeoutException catch (e) {
      print('⏰ Timeout detectado: $e');
      throw Exception(
        'El servidor tardó demasiado en responder (>20s). Verifica tu conexión WiFi.',
      );
    } on SocketException catch (e) {
      print('🚫 Error de socket: $e');
      throw Exception(
        'Error de red: No se puede conectar al servidor. Verifica que estés en la misma red WiFi.',
      );
    } on FormatException catch (e) {
      print('📄 Error de formato JSON: $e');
      throw Exception('El servidor devolvió datos inválidos.');
    } catch (e) {
      print('❌ Error general: $e');

      String errorMsg = e.toString().toLowerCase();
      if (errorMsg.contains('connection refused')) {
        throw Exception(
          'Servidor no disponible. Verifica que esté corriendo en 192.168.1.7:8000',
        );
      } else if (errorMsg.contains('network is unreachable')) {
        throw Exception('Red no accesible. Verifica tu conexión WiFi');
      } else if (errorMsg.contains('no route to host')) {
        throw Exception(
          'No se puede llegar al servidor. Verifica la IP y que estés en la misma red',
        );
      } else {
        throw Exception('Error de análisis: ${e.toString()}');
      }
    }
  }

  /// Mapear respuesta del backend al formato Flutter
  Map<String, dynamic> _mapBackendResponse(
    Map<String, dynamic> backendResponse,
  ) {
    try {
      var detection = backendResponse['detection'];
      var recommendations = backendResponse['recommendations'];

      String flutterDetection;
      String severity;

      if (detection['prediction'] == 'sin_mosca_blanca') {
        flutterDetection = 'Sin Plaga';
        severity = 'Saludable';
      } else {
        flutterDetection = 'Mosca Blanca';
        severity = _getSeverityFromConfidence(detection['confidence']);
      }

      return {
        'success': true,
        'detection': flutterDetection,
        'confidence': detection['confidence'],
        'severity': severity,
        'status': detection['status'],
        'color': detection['color'],
        'recommendations': recommendations ?? [],
        'processing_time': detection['processing_time'],
        'model_type': detection['model_type'],
        'timestamp': detection['timestamp'],
      };
    } catch (e) {
      print('❌ Error mapeando respuesta: $e');
      return {
        'success': false,
        'error': 'Error procesando respuesta: $e',
        'raw_response': backendResponse,
      };
    }
  }

  String _getSeverityFromConfidence(double confidence) {
    if (confidence >= 0.9) return 'Alta';
    if (confidence >= 0.7) return 'Media';
    return 'Baja';
  }

  /// Verificar salud del backend
  Future<Map<String, dynamic>?> getHealthCheck() async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/health'),
            headers: {'Accept': 'application/json'},
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {'status': 'unhealthy', 'code': response.statusCode};
    } catch (e) {
      return {'status': 'error', 'message': e.toString()};
    }
  }

  /// Obtener estadísticas REALES del backend
  Future<Map<String, dynamic>?> getStats() async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/api/estadisticas'),
            headers: {'Accept': 'application/json'},
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        var stats = json.decode(response.body);
        return {
          'total_detecciones': stats['total_analysis'] ?? 0,
          'sin_plaga': stats['binary_distribution']?['sin_mosca_blanca'] ?? 0,
          'con_plaga': stats['binary_distribution']?['con_mosca_blanca'] ?? 0,
        };
      }
    } catch (e) {
      print('Error estadísticas: $e');
    }
    return {'total_detecciones': 0, 'sin_plaga': 0, 'con_plaga': 0};
  }

  /// Obtener historial REAL del backend
  Future<List<dynamic>> getHistory() async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/api/historial'),
            headers: {'Accept': 'application/json'},
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        var historyData = json.decode(response.body);
        return historyData['detections'] ?? [];
      }
    } catch (e) {
      print('Error historial: $e');
    }
    return [];
  }
}
