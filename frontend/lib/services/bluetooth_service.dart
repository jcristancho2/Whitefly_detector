import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'dart:convert';
import 'dart:typed_data';

// Ensure the flutter_bluetooth_serial package is imported for FlutterBluetoothSerial

class BluetoothService extends ChangeNotifier {
  BluetoothConnection? _connection;
  bool _isConnected = false;
  bool _isConnecting = false;
  List<BluetoothDevice> _devices = [];

  bool get isConnected => _isConnected;
  bool get isConnecting => _isConnecting;
  List<BluetoothDevice> get devices => _devices;

  Future<void> scanDevices() async {
    try {
      _devices.clear();
      notifyListeners();

      final bondedDevices = await FlutterBluetoothSerial.instance.getBondedDevices();
      _devices = bondedDevices.where((device) => device.name?.contains('ESP32') == true).toList();
      notifyListeners();
    } catch (e) {
      debugPrint('Error scanning devices: $e');
    }
  }

  Future<bool> connectToDevice(BluetoothDevice device) async {
    try {
      _isConnecting = true;
      notifyListeners();

      _connection = await BluetoothConnection.toAddress(device.address);
      _isConnected = true;
      _isConnecting = false;
      notifyListeners();

      return true;
    } catch (e) {
      _isConnecting = false;
      _isConnected = false;
      notifyListeners();
      debugPrint('Error connecting: $e');
      return false;
    }
  }

  Future<Map<String, double>?> getSensorData() async {
    if (!_isConnected || _connection == null) return null;

    try {
      _connection!.output.add(Uint8List.fromList('GET_DATA\n'.codeUnits));
      await _connection!.output.allSent;

      final data = await _connection!.input!.first;
      final response = String.fromCharCodes(data);
      final json = jsonDecode(response);

      return {
        'temperature': json['temperature']?.toDouble() ?? 0.0,
        'ph': json['ph']?.toDouble() ?? 0.0,
      };
    } catch (e) {
      debugPrint('Error getting sensor data: $e');
      return null;
    }
  }

  void disconnect() {
    _connection?.close();
    _connection = null;
    _isConnected = false;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}