import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/theme_service.dart';
import '../services/storage_service.dart';
import '../models/analysis_result.dart';

class StatsPage extends StatefulWidget {
  const StatsPage({super.key});

  @override
  State<StatsPage> createState() => _StatsPageState();
}

class _StatsPageState extends State<StatsPage> {
  final StorageService _storage = StorageService();
  List<AnalysisResult> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    _history = await _storage.getHistory();
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    final themeService = Provider.of<ThemeService>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Estadísticas'),
        backgroundColor: themeService.isDarkMode
            ? const Color(0xFF1E1E1E)
            : Colors.white,
        foregroundColor: themeService.isDarkMode ? Colors.white : Colors.black,
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _history.isEmpty
          ? const Center(
              child: Text(
                'No hay datos para mostrar estadísticas',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            )
          : Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  _buildStatsCard(
                    'Total de Análisis',
                    _history.length.toString(),
                  ),
                  const SizedBox(height: 16),
                  _buildStatsCard(
                    'Temperatura Promedio',
                    '${(_history.map((e) => e.temperature).reduce((a, b) => a + b) / _history.length).toStringAsFixed(1)}°C',
                  ),
                  const SizedBox(height: 16),
                  _buildStatsCard(
                    'pH Promedio',
                    (_history.map((e) => e.ph).reduce((a, b) => a + b) /
                            _history.length)
                        .toStringAsFixed(1),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildStatsCard(String title, String value) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            Text(
              value,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
