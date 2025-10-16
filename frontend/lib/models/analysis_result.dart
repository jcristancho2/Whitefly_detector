class AnalysisResult {
  final String id;
  final String imagePath;
  final double temperature;
  final double ph;
  final Map<String, dynamic> result;
  final DateTime timestamp;

  AnalysisResult({
    required this.id,
    required this.imagePath,
    required this.temperature,
    required this.ph,
    required this.result,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'imagePath': imagePath,
    'temperature': temperature,
    'ph': ph,
    'result': result,
    'timestamp': timestamp.toIso8601String(),
  };

  factory AnalysisResult.fromJson(Map<String, dynamic> json) => AnalysisResult(
    id: json['id'],
    imagePath: json['imagePath'],
    temperature: json['temperature'],
    ph: json['ph'],
    result: json['result'],
    timestamp: DateTime.parse(json['timestamp']),
  );
}
