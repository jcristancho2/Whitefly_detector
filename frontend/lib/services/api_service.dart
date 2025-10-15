import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://localhost:8000';

  Future<Map<String, dynamic>?> analyzeImage(File image) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/detectar'));
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

  Future<Map<String, dynamic>?> getStats() async {
    final response = await http.get(Uri.parse('$baseUrl/api/estadisticas'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    return null;
  }

  Future<List<dynamic>> getHistory() async {
    final response = await http.get(Uri.parse('$baseUrl/api/historial'));
    if (response.statusCode == 200) {
      return json.decode(response.body)['detecciones'];
    }
    return [];
  }
}
