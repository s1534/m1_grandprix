import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class NextPage extends StatelessWidget {
  void getData() async {
    // http.Response response;

    final response = await http.get(Uri.parse('http://127.0.0.1:5000/model'));
    // print(response.statusCode);
    // setState(() {
    //     // data = jsonDecode(response.body);
    //     data = response.statusCode.toString();
    //   });
    print(response);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('KBOYのFlutter大学'),
      ),
      body: Center(
          child: Column(children: <Widget>[
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
      ])),
    );
  }
}
