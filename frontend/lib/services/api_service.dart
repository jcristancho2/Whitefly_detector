import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://your-api-url.com'; // Cambia por tu URL real

  Future<Map<String, dynamic>?> analyzeImage(File image) async {
    try {
      // Simulación de respuesta mientras configuras tu API real
      await Future.delayed(const Duration(seconds: 2));

      // Respuesta simulada
      return {
        'detection': 'Mosca Blanca',
        'confidence': 0.87,
        'severity': 'Media',
        'recommendations': [
          'Aplicar tratamiento orgánico',
          'Monitorear semanalmente',
          'Mejorar ventilación',
        ],
      };

      // Cuando tengas tu API real, descomenta esto:
      /*
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/analyze'));
      request.files.add(await http.MultipartFile.fromPath('image', image.path));

      var response = await request.send();
      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        return json.decode(responseData);
      }
      return null;
      */
    } catch (e) {
      print('Error en análisis: $e');
      return null;
    }
  }

  Future<Map<String, dynamic>?> getHealthCheck() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/salud'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error al verificar salud del API: $e');
    }
    return null;
  }

  Future<Map<String, dynamic>?> getClasses() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/classes'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error al obtener clases: $e');
    }
    return null;
  }

  // Funciones de compatibilidad (pueden ser implementadas más tarde)
  Future<Map<String, dynamic>?> getStats() async {
    // Por ahora retornamos datos mock
    return {
      'total_detecciones': 0,
      'sin_plaga': 0,
      'infestacion_leve': 0,
      'infestacion_severa': 0,
    };
  }

  Future<List<dynamic>> getHistory() async {
    // Por ahora retornamos lista vacía
    return [];
  }
}
