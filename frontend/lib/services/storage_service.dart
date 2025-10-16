import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/analysis_result.dart';

class StorageService {
  static const String _historyKey = 'analysis_history';

  Future<List<AnalysisResult>> getHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final historyJson = prefs.getStringList(_historyKey) ?? [];
    return historyJson.map((json) => AnalysisResult.fromJson(jsonDecode(json))).toList();
  }

  Future<void> saveAnalysis(AnalysisResult analysis) async {
    final prefs = await SharedPreferences.getInstance();
    final history = await getHistory();
    history.insert(0, analysis);
    
    // Mantener solo los últimos 50 resultados
    if (history.length > 50) {
      history.removeRange(50, history.length);
    }

    final historyJson = history.map((analysis) => jsonEncode(analysis.toJson())).toList();
    await prefs.setStringList(_historyKey, historyJson);
  }

  Future<void> clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_historyKey);
  }
}