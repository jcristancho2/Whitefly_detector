import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HistoryPage extends StatefulWidget {
  const HistoryPage({super.key});

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  final ApiService _api = ApiService();
  List<dynamic> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    try {
      final history = await _api.getHistory();
      setState(() {
        _history = history;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al cargar historial: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Historial'),
        backgroundColor: Colors.green.shade100,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _history.isEmpty
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.history, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text(
                    'No hay detecciones en el historial',
                    style: TextStyle(fontSize: 18, color: Colors.grey),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Realiza tu primera detección de mosca blanca',
                    style: TextStyle(fontSize: 14, color: Colors.grey),
                  ),
                ],
              ),
            )
          : RefreshIndicator(
              onRefresh: _loadHistory,
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _history.length,
                itemBuilder: (context, index) {
                  final detection = _history[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: _getColorForClass(
                          detection['class'] ?? 'sin_plaga',
                        ),
                        child: Icon(
                          _getIconForClass(detection['class'] ?? 'sin_plaga'),
                          color: Colors.white,
                        ),
                      ),
                      title: Text(
                        _getDisplayName(detection['class'] ?? 'sin_plaga'),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Confianza: ${((detection['confidence'] ?? 0) * 100).toStringAsFixed(1)}%',
                          ),
                          Text(
                            'Fecha: ${detection['timestamp'] ?? 'No disponible'}',
                            style: const TextStyle(fontSize: 12),
                          ),
                        ],
                      ),
                      trailing: Icon(
                        Icons.chevron_right,
                        color: Colors.grey.shade400,
                      ),
                    ),
                  );
                },
              ),
            ),
    );
  }

  Color _getColorForClass(String className) {
    switch (className) {
      case 'sin_plaga':
        return Colors.green;
      case 'infestacion_leve':
        return Colors.orange;
      case 'infestacion_severa':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData _getIconForClass(String className) {
    switch (className) {
      case 'sin_plaga':
        return Icons.check_circle;
      case 'infestacion_leve':
        return Icons.warning;
      case 'infestacion_severa':
        return Icons.error;
      default:
        return Icons.help;
    }
  }

  String _getDisplayName(String className) {
    switch (className) {
      case 'sin_plaga':
        return 'Sin Plaga';
      case 'infestacion_leve':
        return 'Infestación Leve';
      case 'infestacion_severa':
        return 'Infestación Severa';
      default:
        return 'Desconocido';
    }
  }
}
