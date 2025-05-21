import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';
import 'package:logging/logging.dart';

void main() {
  Logger.root.level = Level.ALL;
  Logger.root.onRecord.listen((record) {
    debugPrint('${record.level.name}: ${record.time}: ${record.message}');
  });

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'BKLG - Dự đoán điểm số bằng AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2969FF),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        fontFamily: 'Fz Poppins',
      ),
      home: const WelcomeScreen(),
    );
  }
}
