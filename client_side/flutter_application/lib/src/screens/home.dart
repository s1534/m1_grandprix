import 'dart:ui';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'tmp.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);
  @override
  _HomeScreen createState() => _HomeScreen();
}

class _HomeScreen extends State<HomeScreen> {
  String data = "aaaaa";
  Future<dynamic> getData() async {
    http.Response response;

    response = await http.get(Uri.parse('http://127.0.0.1:5000/model'));
    // print(response.statusCode);
    // setState(() {
    //     // data = jsonDecode(response.body);
    //     data = response.statusCode.toString();
    //   });

    if (response.statusCode == 200) {
      setState(() {
        // data = jsonDecode(response.body);
        data = "aaaaaaaaaaaaaaaaaaaaaaa";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('temp'),
        backgroundColor: Color(0xff02d39a),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            Text(data),
            ElevatedButton(
              child: const Text('Button'),
              style: ElevatedButton.styleFrom(
                primary: Colors.orange,
                onPrimary: Colors.white,
              ),
              onPressed: () {
                getData();
                // setState(() {
                //   // data = jsonDecode(response.body);
                //   data = "aaaaaaaaaaaaaaaaaaaaaaa";
                // });
                // Navigator.push(
                //   context,
                //   MaterialPageRoute(builder: (context) => NextPage()),
                // );
              },
            ),
          ],
        ),
      ),
    );
  }
}
