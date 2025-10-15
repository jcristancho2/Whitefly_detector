import 'package:flutter/material.dart';

class ResultCard extends StatelessWidget {
  final Map<String, dynamic> result;

  const ResultCard({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    final deteccion = result['deteccion'];
    final String clase = deteccion['clase'];
    final double confianza = deteccion['confianza'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(Icons.analytics, size: 48, color: _getColor(clase)),
            Text(
              _getText(clase),
              style: TextStyle(
                color: _getColor(clase),
                fontWeight: FontWeight.bold,
              ),
            ),
            Text("Confianza: ${(confianza * 100).toStringAsFixed(1)}%"),
          ],
        ),
      ),
    );
  }

  Color _getColor(String clase) {
    switch (clase) {
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

  String _getText(String clase) {
    switch (clase) {
      case 'sin_plaga':
        return 'Sin Plaga Detectada';
      case 'infestacion_leve':
        return 'Infestación Leve';
      case 'infestacion_severa':
        return 'Infestación Severa';
      default:
        return 'Desconocido';
    }
  }
}
