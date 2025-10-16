import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'dart:io';
import 'dart:math';
import '../services/api_service.dart';
import '../services/theme_service.dart';
import '../services/storage_service.dart';
import '../services/bluetooth_service.dart';
import '../models/analysis_result.dart';
import '../Widgets/result_card.dart';
import 'history_page.dart';
import 'stats_page.dart';
import 'bluetooth_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with TickerProviderStateMixin {
  final ImagePicker _picker = ImagePicker();
  final ApiService _api = ApiService();
  final StorageService _storage = StorageService();

  File? _selectedImage;
  bool _isAnalyzing = false;
  Map<String, dynamic>? _result;

  double _ambientTemperature = 0.0;
  double _soilPH = 0.0;
  bool _isLoadingEnvironmentData = false;

  late AnimationController _fadeController;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _fadeController, curve: Curves.easeInOut),
    );
    _loadEnvironmentData();
    _fadeController.forward();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    super.dispose();
  }

  Future<void> _loadEnvironmentData() async {
    setState(() => _isLoadingEnvironmentData = true);

    final bluetoothService = Provider.of<BluetoothService>(
      context,
      listen: false,
    );

    if (bluetoothService.isConnected) {
      final sensorData = await bluetoothService.getSensorData();
      if (sensorData != null) {
        _ambientTemperature = sensorData['temperature']!;
        _soilPH = sensorData['ph']!;
      }
    } else {
      // Datos simulados si no hay conexión Bluetooth
      await Future.delayed(const Duration(seconds: 1));
      final random = Random();
      _ambientTemperature = 18.0 + random.nextDouble() * 10.0;
      _soilPH = 5.5 + random.nextDouble() * 1.5;
    }

    setState(() => _isLoadingEnvironmentData = false);
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? image = await _picker.pickImage(
        source: source,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );

      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          _result = null;
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

    final result = await _api.analyzeImage(_selectedImage!);

    if (result != null) {
      setState(() {
        _result = result;
        _isAnalyzing = false;
      });

      // Guardar en historial
      final analysisResult = AnalysisResult(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        imagePath: _selectedImage!.path,
        temperature: _ambientTemperature,
        ph: _soilPH,
        result: result,
        timestamp: DateTime.now(),
      );

      await _storage.saveAnalysis(analysisResult);
    } else {
      setState(() => _isAnalyzing = false);
      _showError('No se pudo analizar la imagen. Intenta de nuevo.');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error_outline, color: Colors.white),
            const SizedBox(width: 8),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.red.shade400,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final themeService = Provider.of<ThemeService>(context);
    final bluetoothService = Provider.of<BluetoothService>(context);

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: _buildAppBar(themeService, bluetoothService),
      body: FadeTransition(
        opacity: _fadeAnimation,
        child: _buildResponsiveBody(context, themeService),
      ),
    );
  }

  PreferredSizeWidget _buildAppBar(
    ThemeService themeService,
    BluetoothService bluetoothService,
  ) {
    return AppBar(
      elevation: 0,
      backgroundColor: Colors.transparent,
      flexibleSpace: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: themeService.isDarkMode
                ? [const Color(0xFF1B5E20), const Color(0xFF2E7D32)]
                : [const Color(0xFF6D4C41), const Color(0xFF8D6E63)],
          ),
        ),
      ),
      title: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.local_florist, size: 24),
          ),
          const SizedBox(width: 12),
          const Expanded(
            child: Text(
              'CoffeeGuard Pro',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.5,
              ),
            ),
          ),
        ],
      ),
      foregroundColor: Colors.white,
      actions: [
        _buildAppBarAction(
          bluetoothService.isConnected
              ? Icons.bluetooth_connected
              : Icons.bluetooth,
          () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const BluetoothPage()),
          ),
          bluetoothService.isConnected ? Colors.green : null,
        ),
        _buildAppBarAction(
          themeService.isDarkMode ? Icons.light_mode : Icons.dark_mode,
          themeService.toggleTheme,
        ),
        _buildAppBarAction(
          Icons.refresh,
          _isLoadingEnvironmentData ? null : _loadEnvironmentData,
        ),
        _buildAppBarAction(
          Icons.analytics_outlined,
          () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const StatsPage()),
          ),
        ),
        _buildAppBarAction(
          Icons.history,
          () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const HistoryPage()),
          ),
        ),
      ],
    );
  }

  Widget _buildAppBarAction(
    IconData icon,
    VoidCallback? onPressed, [
    Color? iconColor,
  ]) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      child: IconButton(
        icon: Icon(icon, color: iconColor),
        onPressed: onPressed,
        style: IconButton.styleFrom(
          backgroundColor: Colors.white.withOpacity(0.1),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
    );
  }

  Widget _buildResponsiveBody(BuildContext context, ThemeService themeService) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

    return SingleChildScrollView(
      physics: const BouncingScrollPhysics(),
      child: Center(
        child: Container(
          constraints: BoxConstraints(
            maxWidth: isTablet ? 800 : double.infinity,
          ),
          child: Column(
            children: [
              SizedBox(
                height:
                    AppBar().preferredSize.height +
                    MediaQuery.of(context).padding.top +
                    20,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: isTablet ? 40 : 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    _buildWelcomeSection(themeService),
                    const SizedBox(height: 24),
                    if (isTablet)
                      Row(
                        children: [
                          Expanded(
                            child: _buildEnvironmentSection(themeService),
                          ),
                          const SizedBox(width: 24),
                          Expanded(child: _buildImageSection(themeService)),
                        ],
                      )
                    else ...[
                      _buildEnvironmentSection(themeService),
                      const SizedBox(height: 24),
                      _buildImageSection(themeService),
                    ],
                    const SizedBox(height: 24),
                    _buildAnalysisButton(themeService),
                    const SizedBox(height: 24),
                    if (_result != null) _buildResultSection(themeService),
                    const SizedBox(height: 100),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeSection(ThemeService themeService) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: themeService.isDarkMode
              ? [const Color(0xFF1B5E20), const Color(0xFF2E7D32)]
              : [const Color(0xFF4CAF50), const Color(0xFF66BB6A)],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color:
                (themeService.isDarkMode
                        ? Colors.black
                        : const Color(0xFF4CAF50))
                    .withOpacity(0.3),
            blurRadius: 15,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Icon(Icons.eco, color: Colors.white, size: 28),
          ),
          const SizedBox(width: 16),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '¡Bienvenido!',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'Detecta plagas en tus cultivos de café',
                  style: TextStyle(color: Colors.white70, fontSize: 16),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEnvironmentSection(ThemeService themeService) {
    return Container(
      decoration: BoxDecoration(
        color: themeService.isDarkMode ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(
              themeService.isDarkMode ? 0.3 : 0.05,
            ),
            blurRadius: 20,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF1976D2), Color(0xFF2196F3)],
              ),
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20),
                topRight: Radius.circular(20),
              ),
            ),
            child: Row(
              children: [
                const Icon(Icons.sensors, color: Colors.white, size: 24),
                const SizedBox(width: 12),
                const Text(
                  'Datos Ambientales',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const Spacer(),
                if (_isLoadingEnvironmentData)
                  const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                  ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20),
            child: _isLoadingEnvironmentData
                ? const Center(
                    child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: CircularProgressIndicator(),
                    ),
                  )
                : EnvironmentDataCard(
                    temperature: _ambientTemperature,
                    ph: _soilPH,
                    isDarkMode: themeService.isDarkMode,
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildImageSection(ThemeService themeService) {
    return Container(
      decoration: BoxDecoration(
        color: themeService.isDarkMode ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(
              themeService.isDarkMode ? 0.3 : 0.05,
            ),
            blurRadius: 20,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFFFF7043), Color(0xFFFF8A65)],
              ),
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20),
                topRight: Radius.circular(20),
              ),
            ),
            child: const Row(
              children: [
                Icon(Icons.image_outlined, color: Colors.white, size: 24),
                SizedBox(width: 12),
                Text(
                  'Imagen para Análisis',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                _selectedImage == null
                    ? PlaceholderImage(isDarkMode: themeService.isDarkMode)
                    : SelectedImageCard(image: _selectedImage!),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildCircularButton(
                      Icons.camera_alt,
                      'Cámara',
                      const Color(0xFF2196F3),
                      () => _pickImage(ImageSource.camera),
                    ),
                    _buildCircularButton(
                      Icons.photo_library,
                      'Galería',
                      const Color(0xFFFF9800),
                      () => _pickImage(ImageSource.gallery),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCircularButton(
    IconData icon,
    String label,
    Color color,
    VoidCallback onPressed,
  ) {
    return Column(
      children: [
        FloatingActionButton(
          heroTag: '${label.toLowerCase()}_fab',
          onPressed: onPressed,
          backgroundColor: color,
          foregroundColor: Colors.white,
          elevation: 8,
          child: Icon(icon, size: 28),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
        ),
      ],
    );
  }

  Widget _buildAnalysisButton(ThemeService themeService) {
    return Container(
      decoration: BoxDecoration(
        gradient: _selectedImage != null
            ? LinearGradient(
                colors: themeService.isDarkMode
                    ? [const Color(0xFF1B5E20), const Color(0xFF2E7D32)]
                    : [const Color(0xFF4CAF50), const Color(0xFF66BB6A)],
              )
            : null,
        color: _selectedImage == null
            ? (themeService.isDarkMode
                  ? Colors.grey.shade700
                  : Colors.grey.shade300)
            : null,
        borderRadius: BorderRadius.circular(16),
        boxShadow: _selectedImage != null
            ? [
                BoxShadow(
                  color:
                      (themeService.isDarkMode
                              ? Colors.black
                              : const Color(0xFF4CAF50))
                          .withOpacity(0.4),
                  blurRadius: 15,
                  offset: const Offset(0, 8),
                ),
              ]
            : null,
      ),
      child: ElevatedButton.icon(
        onPressed: _isAnalyzing || _selectedImage == null
            ? null
            : _analyzeImage,
        icon: _isAnalyzing
            ? const SizedBox(
                width: 24,
                height: 24,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                ),
              )
            : const Icon(Icons.psychology, size: 24),
        label: Text(
          _isAnalyzing
              ? 'Analizando imagen...'
              : (_selectedImage == null
                    ? 'Selecciona una imagen'
                    : 'Analizar Imagen'),
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
          ),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.transparent,
          foregroundColor: Colors.white,
          shadowColor: Colors.transparent,
          padding: const EdgeInsets.symmetric(vertical: 18),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
      ),
    );
  }

  Widget _buildResultSection(ThemeService themeService) {
    return Container(
      decoration: BoxDecoration(
        color: themeService.isDarkMode ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(
              themeService.isDarkMode ? 0.3 : 0.05,
            ),
            blurRadius: 20,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF9C27B0), Color(0xFFBA68C8)],
              ),
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20),
                topRight: Radius.circular(20),
              ),
            ),
            child: const Row(
              children: [
                Icon(Icons.analytics, color: Colors.white, size: 24),
                SizedBox(width: 12),
                Text(
                  'Resultado del Análisis',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20),
            child: ResultCard(result: _result!),
          ),
        ],
      ),
    );
  }
}

// Widgets personalizados con efecto de relieve

class EnvironmentDataCard extends StatelessWidget {
  final double temperature;
  final double ph;
  final bool isDarkMode;

  const EnvironmentDataCard({
    required this.temperature,
    required this.ph,
    required this.isDarkMode,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _buildReliefCard(
            icon: Icons.thermostat,
            label: 'Temperatura',
            value: '${temperature.toStringAsFixed(1)}°C',
            color: const Color(0xFFE53935),
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: _buildReliefCard(
            icon: Icons.science,
            label: 'pH del Suelo',
            value: ph.toStringAsFixed(1),
            color: const Color(0xFF1E88E5),
          ),
        ),
      ],
    );
  }

  Widget _buildReliefCard({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDarkMode ? const Color(0xFF2A2A2A) : Colors.grey.shade50,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          // Sombra exterior (más oscura)
          BoxShadow(
            color: isDarkMode ? Colors.black54 : Colors.grey.shade400,
            offset: const Offset(4, 4),
            blurRadius: 8,
          ),
          // Luz interior (más clara)
          BoxShadow(
            color: isDarkMode ? Colors.grey.shade800 : Colors.white,
            offset: const Offset(-2, -2),
            blurRadius: 8,
          ),
        ],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, size: 32, color: color),
          ),
          const SizedBox(height: 12),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: isDarkMode ? Colors.grey.shade400 : Colors.grey.shade600,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }
}

class SelectedImageCard extends StatelessWidget {
  final File image;
  const SelectedImageCard({required this.image, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Stack(
          children: [
            Image.file(
              image,
              fit: BoxFit.cover,
              height: 200,
              width: double.infinity,
            ),
            Positioned(
              top: 12,
              right: 12,
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.6),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.check_circle,
                  color: Colors.white,
                  size: 20,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class PlaceholderImage extends StatelessWidget {
  final bool isDarkMode;
  const PlaceholderImage({required this.isDarkMode, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: isDarkMode
              ? [Colors.grey.shade800, Colors.grey.shade700]
              : [Colors.grey.shade100, Colors.grey.shade200],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDarkMode ? Colors.grey.shade600 : Colors.grey.shade300,
          width: 2,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: isDarkMode ? Colors.grey.shade700 : Colors.grey.shade300,
              shape: BoxShape.circle,
            ),
            child: Icon(
              Icons.add_photo_alternate,
              size: 48,
              color: isDarkMode ? Colors.grey.shade400 : Colors.grey.shade600,
            ),
          ),
          const SizedBox(height: 16),
          Text(
            'Selecciona una imagen',
            style: TextStyle(
              color: isDarkMode ? Colors.grey.shade400 : Colors.grey.shade600,
              fontSize: 18,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Usa los botones de abajo',
            style: TextStyle(
              color: isDarkMode ? Colors.grey.shade500 : Colors.grey.shade500,
              fontSize: 14,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
