import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
// Nota: Asegúrate de que estos imports existan en tu proyecto
import '../services/api_service.dart';
import '../Widgets/result_card.dart';
import 'history_page.dart';
import 'stats_page.dart';

// Importa para usar Geolocator o otros servicios para datos ambientales (simulado aquí)
import 'dart:math';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ImagePicker _picker = ImagePicker();
  final ApiService _api = ApiService();
  File? _selectedImage;
  bool _isAnalyzing = false;
  Map<String, dynamic>? _result;

  // Nuevas variables para datos ambientales
  double _ambientTemperature = 0.0;
  double _soilPH = 0.0;
  bool _isLoadingEnvironmentData = false;

  @override
  void initState() {
    super.initState();
    _loadEnvironmentData();
  }

  // Función para simular la obtención de datos ambientales (Temperatura y pH)
  // Aquí es donde integrarías la lógica real de tus sensores (Bluetooth/Wi-Fi/etc.)
  Future<void> _loadEnvironmentData() async {
    setState(() => _isLoadingEnvironmentData = true);
    // Simulación de una carga de datos
    await Future.delayed(const Duration(seconds: 1)); 
    
    // Simulación: Temperatura entre 18.0 y 28.0 grados
    final random = Random();
    _ambientTemperature = 18.0 + random.nextDouble() * 10.0; 
    
    // Simulación: pH del suelo entre 5.5 y 7.0 (ideal para café)
    _soilPH = 5.5 + random.nextDouble() * 1.5;

    setState(() => _isLoadingEnvironmentData = false);
  }

  Future<void> _pickImage(ImageSource source) async {
    // ... (Tu lógica existente para seleccionar imagen) ...
    try {
      final XFile? image = await _picker.pickImage(
        source: source,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 80,
      );

      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          _result = null; // Limpiar resultado anterior al seleccionar nueva imagen
        });
      }
    } catch (e) {
      _showError('Error al seleccionar imagen: $e');
    }
  }

  Future<void> _analyzeImage() async {
    if (_selectedImage == null) {
      _showError('Por favor, selecciona una imagen primero.');
      return;
    }

    setState(() => _isAnalyzing = true);
    // Añadir datos ambientales al análisis si es necesario para el backend
    final analysisData = {
      'image': _selectedImage!,
      'temperature': _ambientTemperature.toStringAsFixed(1),
      'ph': _soilPH.toStringAsFixed(1),
    };

    // La función analyzeImage en ApiService debe aceptar esta nueva data
    // Por ejemplo: final result = await _api.analyzeImage(analysisData);
    // Para simplificar, mantendremos la firma original por ahora:
    final result = await _api.analyzeImage(_selectedImage!);

    if (result != null) {
      setState(() {
        _result = result;
        _isAnalyzing = false;
      });
    } else {
      setState(() => _isAnalyzing = false);
      _showError('No se pudo analizar la imagen. Intenta de nuevo.');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detector de Plagas del Café ☕'),
        backgroundColor: Colors.brown.shade700,
        foregroundColor: Colors.white,
        actions: [
          // Botón para recargar los datos ambientales
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _isLoadingEnvironmentData ? null : _loadEnvironmentData,
          ),
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
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. Tarjeta de Datos Ambientales
            _isLoadingEnvironmentData
                ? const Center(child: CircularProgressIndicator())
                : EnvironmentDataCard(
                    temperature: _ambientTemperature,
                    ph: _soilPH,
                  ),
            
            const SizedBox(height: 16),

            // 2. Visualización de Imagen Seleccionada o Placeholder
            _selectedImage == null
                ? const PlaceholderImage()
                : SelectedImageCard(image: _selectedImage!),

            const SizedBox(height: 16),

            // 3. Botón de Análisis
            ElevatedButton.icon(
              onPressed: _isAnalyzing || _selectedImage == null ? null : _analyzeImage,
              icon: _isAnalyzing
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.local_florist), // Icono de análisis más relevante
              label: Text(
                _isAnalyzing
                    ? 'Analizando Hoja...'
                    : (_selectedImage == null
                        ? 'Selecciona una imagen para analizar'
                        : 'Analizar Hoja de Café'),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green.shade700,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                textStyle: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            const SizedBox(height: 16),

            // 4. Resultado del análisis
            if (_result != null) ResultCard(result: _result!),
          ],
        ),
      ),
      // Floating Action Button para Cámara y Galería
      floatingActionButton: SplitFloatingActionButton(
        onCameraPressed: () => _pickImage(ImageSource.camera),
        onGalleryPressed: () => _pickImage(ImageSource.gallery),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

// --- WIDGETS AUXILIARES ---

// Tarjeta para mostrar la Temperatura y el PH
class EnvironmentDataCard extends StatelessWidget {
  final double temperature;
  final double ph;

  const EnvironmentDataCard({
    required this.temperature,
    required this.ph,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildDataItem(
              icon: Icons.thermostat_outlined,
              label: 'Temperatura',
              value: '${temperature.toStringAsFixed(1)} °C',
              color: Colors.red.shade600,
            ),
            Container(width: 1, height: 40, color: Colors.grey.shade300),
            _buildDataItem(
              icon: Icons.science_outlined,
              label: 'pH del Suelo',
              value: ph.toStringAsFixed(1),
              color: Colors.blue.shade600,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDataItem({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Column(
      children: [
        Icon(icon, size: 30, color: color),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}

// Tarjeta que muestra la imagen seleccionada
class SelectedImageCard extends StatelessWidget {
  final File image;
  const SelectedImageCard({required this.image, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      clipBehavior: Clip.antiAlias,
      child: Image.file(
        image,
        fit: BoxFit.cover,
        height: 200,
        width: double.infinity,
      ),
    );
  }
}

// Placeholder cuando no hay imagen seleccionada
class PlaceholderImage extends StatelessWidget {
  const PlaceholderImage({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      decoration: BoxDecoration(
        color: Colors.grey.shade200,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey.shade300),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.image_outlined,
            size: 60,
            color: Colors.grey.shade500,
          ),
          const SizedBox(height: 8),
          Text(
            'Toma o selecciona una foto de la hoja de café',
            style: TextStyle(color: Colors.grey.shade600, fontSize: 16),
          ),
        ],
      ),
    );
  }
}

// Floating Action Button separado para Cámara y Galería
class SplitFloatingActionButton extends StatelessWidget {
  final VoidCallback onCameraPressed;
  final VoidCallback onGalleryPressed;

  const SplitFloatingActionButton({
    required this.onCameraPressed,
    required this.onGalleryPressed,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        FloatingActionButton.extended(
          heroTag: 'camera_fab',
          onPressed: onCameraPressed,
          label: const Text('Cámara'),
          icon: const Icon(Icons.camera_alt),
          backgroundColor: Colors.blue.shade600,
          foregroundColor: Colors.white,
        ),
        const SizedBox(width: 16),
        FloatingActionButton.extended(
          heroTag: 'gallery_fab',
          onPressed: onGalleryPressed,
          label: const Text('Galería'),
          icon: const Icon(Icons.photo_library),
          backgroundColor: Colors.orange.shade600,
          foregroundColor: Colors.white,
        ),
      ],
    );
  }
}