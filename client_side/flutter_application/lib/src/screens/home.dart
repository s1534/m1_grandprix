import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('temp'),
        backgroundColor: Color(0xff02d39a),
      ),
      body:
          const Center(child: Text('temp画面', style: TextStyle(fontSize: 32.0))),
    );
  }
}
