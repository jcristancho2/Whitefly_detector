import 'package:flutter/material.dart';

class ResultCard extends StatelessWidget {
  final Map<String, dynamic> result;

  const ResultCard({required this.result, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.bug_report,
                  color: _getSeverityColor(result['severity']),
                  size: 24,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    result['detection'] ?? 'Análisis completado',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (result['confidence'] != null)
              LinearProgressIndicator(
                value: result['confidence'].toDouble(),
                backgroundColor: Colors.grey.shade300,
                valueColor: AlwaysStoppedAnimation<Color>(
                  _getSeverityColor(result['severity']),
                ),
              ),
            const SizedBox(height: 8),
            Text(
              'Confianza: ${((result['confidence'] ?? 0) * 100).toInt()}%',
              style: TextStyle(color: Colors.grey.shade600),
            ),
            if (result['severity'] != null) ...[
              const SizedBox(height: 8),
              Text(
                'Severidad: ${result['severity']}',
                style: TextStyle(
                  color: _getSeverityColor(result['severity']),
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
            if (result['recommendations'] != null) ...[
              const SizedBox(height: 16),
              const Text(
                'Recomendaciones:',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              ...((result['recommendations'] as List).map(
                (rec) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '• ',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      Expanded(child: Text(rec.toString())),
                    ],
                  ),
                ),
              )),
            ],
          ],
        ),
      ),
    );
  }

  Color _getSeverityColor(String? severity) {
    switch (severity?.toLowerCase()) {
      case 'baja':
        return Colors.green;
      case 'media':
        return Colors.orange;
      case 'alta':
        return Colors.red;
      default:
        return Colors.blue;
    }
  }
}
