import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // IP de tu computadora en la red local
  final String baseUrl = 'http://192.168.1.7:8000';
  // Para emulador, usar: 'http://10.0.2.2:8000' (Android) o 'http://localhost:8000'

  Future<Map<String, dynamic>?> analyzeImage(File image) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/detect'));
      request.files.add(await http.MultipartFile.fromPath('file', image.path));
      var response = await request.send();

      if (response.statusCode == 200) {
        var body = await http.Response.fromStream(response);
        return json.decode(body.body);
      }
    } catch (e) {
      print('Error al analizar: $e');
    }
    return null;
  }

  Future<Map<String, dynamic>?> getHealthCheck() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
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
