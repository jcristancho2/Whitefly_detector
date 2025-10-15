import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../services/api_service.dart';
import '../widgets/result_card.dart';
import 'history_page.dart';
import 'stats_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ImagePicker _picker = ImagePicker();
  final ApiService _api = ApiService();
  File? _selectedImage;
  bool _isAnalyzing = false;
  Map<String, dynamic>? _result;

  Future<void> _pickImage(ImageSource source) async {
    final XFile? image = await _picker.pickImage(source: source);
    if (image != null) {
      setState(() {
        _selectedImage = File(image.path);
        _result = null;
      });
    }
  }

  Future<void> _analyzeImage() async {
    if (_selectedImage == null) {
      _showError('Por favor selecciona una imagen primero');
      return;
    }

    setState(() => _isAnalyzing = true);
    final result = await _api.analyzeImage(_selectedImage!);

    if (result != null) {
      setState(() {
        _result = result;
        _isAnalyzing = false;
      });
    } else {
      setState(() => _isAnalyzing = false);
      _showError('No se pudo analizar la imagen');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detector de Mosca Blanca'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const HistoryPage()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.bar_chart),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const StatsPage()),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            if (_selectedImage != null)
              Image.file(_selectedImage!, height: 250, fit: BoxFit.cover),
            const SizedBox(height: 16),
            if (_isAnalyzing)
              const CircularProgressIndicator()
            else
              ElevatedButton.icon(
                onPressed: _analyzeImage,
                icon: const Icon(Icons.analytics),
                label: const Text("Analizar Imagen"),
              ),
            const SizedBox(height: 16),
            if (_result != null) ResultCard(result: _result!),
          ],
        ),
      ),
    );
  }
}
