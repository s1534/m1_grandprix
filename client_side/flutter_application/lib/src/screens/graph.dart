import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'dart:typed_data';
import 'home.dart';
import 'package:flutter/services.dart';
import 'package:just_audio/just_audio.dart';
import 'package:audio_session/audio_session.dart';

class LineChartSample2 extends StatefulWidget {
  const LineChartSample2({Key? key}) : super(key: key);

  @override
  _LineChartSample2State createState() => _LineChartSample2State();
}

class _LineChartSample2State extends State<LineChartSample2> {
  late AudioPlayer _player;
  double _currentSliderValue = 1.0;
  bool _changeAudioSource = false;
  String _stateSource = 'アセットを再生';

  List<Color> gradientColors = [
    // const Color(0xff1f005c),
    const Color(0xff02d39a),
    const Color(0xff02d39a),
  ];

  bool showAvg = false;
  bool flag = false;

  int NUM_min = 50;
  int NUM_sec = 15;

  Map<String, dynamic> user = {
    'evals': [0, 20, 40, 60, 80, 100]
  };

  var evals_min = <FlSpot>[
    // FlSpot(0, 3.44),
    // FlSpot(10, 3.44),
    // FlSpot(20, 23),
    // FlSpot(30, 44),
    // FlSpot(40, 55),
    // FlSpot(50, 98),
  ];
  var evals_hour = <FlSpot>[
    // FlSpot(0, 3.44),
    // FlSpot(10, 3.44),
    // FlSpot(20, 23),
    // FlSpot(30, 44),
    // FlSpot(40, 55),
    // FlSpot(50, 98),
  ];

  @override
  void initState() {
    super.initState();
    _setupSession();

    // AudioPlayerの状態を取得
    _player.playbackEventStream.listen((event) {
      switch (event.processingState) {
        case ProcessingState.idle:
          print('オーディオファイルをロードしていないよ');
          break;
        case ProcessingState.loading:
          print('オーディオファイルをロード中だよ');
          break;
        case ProcessingState.buffering:
          print('バッファリング(読み込み)中だよ');
          break;
        case ProcessingState.ready:
          print('再生できるよ');
          break;
        case ProcessingState.completed:
          print('再生終了したよ');
          break;
        default:
          print(event.processingState);
          break;
      }
    });
  }

  Future<void> _setupSession() async {
    _player = AudioPlayer();
    final session = await AudioSession.instance;
    await session.configure(AudioSessionConfiguration.speech());
    await _loadAudioFile();
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  void _takeTurns() {
    late String _changeStateText;
    _changeAudioSource = _changeAudioSource ? false : true; // 真偽値を反転

    _player.stop();
    _loadAudioFile().then((_) {
      if (_changeAudioSource) {
        _changeStateText = 'ストリーミング再生';
      } else {
        _changeStateText = 'アセットを再生';
      }
      setState(() {
        _stateSource = _changeStateText;
      });
    });
  }

  Future<void> _loadAudioFile() async {
    try {
      if (_changeAudioSource) {
        await _player.setUrl(
            'https://s3.amazonaws.com/scifri-episodes/scifri20181123-episode.mp3'); // ストリーミング
      } else {
        await _player.setAsset('assets/audio/yume.mp3'); // アセット(ローカル)のファイル
      }
    } catch (e) {
      print(e);
    }
  }

  Future<void> _callAPI() async {
    var url = Uri.parse(
      'http://18.179.198.146:8080/model',
    );
    var response = await http.get(url);
    if (response.statusCode == 200) {
      // print(response.body);

      setState(() {
        double sum = 0;
        // data = response.statusCode.toString();
        var user = json.decode(response.body);
        evals_min = <FlSpot>[];
        evals_hour = <FlSpot>[];
        for (var i = 0; i < NUM_min; i++) {
          // print(user['evals'][i]);
          evals_min.insert(
              i, FlSpot((i * 10).toDouble(), double.parse(user['evals'][i])));
        }
        for (var i = 0; i < NUM_sec; i++) {
          // print(user['evals'][i]);
          sum += double.parse(user['evals'][i]);
          evals_hour.insert(
              i, FlSpot((i * 10).toDouble(), double.parse(user['evals'][i])));
        }

        double avg = sum / NUM_sec;
        print(user['evals']);
        print(avg);
        if (avg <= 60) {
          flag = true;
        }
      });
    }
    // print('Response status: ${response.statusCode}');
    // print('Response body: ${response.body}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          // Here we take the value from the MyHomePage object that was created by
          // the App.build method, and use it to set our appbar title.
          backgroundColor: Color(0xff02d39a),
          actions: <Widget>[
            IconButton(
                icon: Icon(Icons.autorenew),
                onPressed: () => {
                      _callAPI(),
                      if (flag) {_showMyDialog(), flag = false}
                    }),
          ]),
      // body: RefreshIndicator(
      //   child: LayoutBuilder(
      //     builder: (context, constraints) => SingleChildScrollView(
      //       physics: AlwaysScrollableScrollPhysics(),
      //       child: ConstrainedBox(
      //         constraints: BoxConstraints(minHeight: constraints.maxHeight),
      //         child: SingleChildScrollView(
      //           child: Column(
      //             children: [
      //               graph_template(),
      //               description_card(),
      //               // description_card(),
      //               // description_card(),
      //               // description_card(),
      //             ],
      //           ),
      //         ),
      //       ),
      //     ),
      //   ),
      //   onRefresh: () async {
      //     // スワイプ時に更新したい処理を書く
      //     await _callAPI();
      //   },
      // ),
      body: RefreshIndicator(
        onRefresh: () async {
          await _callAPI();
        },
        child: ListView(children: <Widget>[
          graph_template(),
          description_card(),
        ]),
      ),
    );
  }

  Future<void> _showMyDialog() async {
    return showDialog<void>(
      // `showDialog`メソッドでダイアログを呼び出す!
      context: context, //必須の引数
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        //必須の引数
        return AlertDialog(
          //`showDialog`メソッドの必須の引数であるbuilder:の戻り値としてAlertDialog()を返す！
          title: const Text('集中力が不足しています'),
          content: SingleChildScrollView(
            child: ListBody(
              children: const <Widget>[
                Text('集中力を促進するために音楽を流します'),
                Text('Play music to help you concentrate'),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Approve'),
              onPressed: () {
                // MaterialPageRoute(builder: (context) => HomeScreen());
                Navigator.of(context).pop();
                _playSoundFile();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _showMyDialog_best_concentrate() async {
    return showDialog<void>(
      // `showDialog`メソッドでダイアログを呼び出す!
      context: context, //必須の引数
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        //必須の引数
        return AlertDialog(
          //`showDialog`メソッドの必須の引数であるbuilder:の戻り値としてAlertDialog()を返す！
          title: const Text('集中力が保ててます'),
          content: SingleChildScrollView(
            child: ListBody(
              children: const <Widget>[
                Text('集中できているようなので，音楽を止めますね'),
                Text('Play music to help you concentrate'),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Approve'),
              onPressed: () {
                // MaterialPageRoute(builder: (context) => HomeScreen());
                Navigator.of(context).pop();
                _playSoundFile();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _playSoundFile() async {
    // 再生終了状態の場合、新たなオーディオファイルを定義し再生できる状態にする
    if (_player.processingState == ProcessingState.completed) {
      await _loadAudioFile();
    }

    await _player.setSpeed(_currentSliderValue); // 再生速度を指定
    await _player.play();
  }

  Card description_card2() {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Container(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'testtetst',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              '集中レベルをモニタリングすることで，集中の程度を確認できます．集中力が乱れている場合，適度な休憩をとる必要があります．',
              style: TextStyle(fontSize: 15),
            ),
          ],
        ),
      ),
    );
  }

  Card description_card() {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Container(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '集中レベルモニタリング',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              '集中レベルをモニタリングすることで，集中の程度を確認できます．集中力が乱れている場合，適度な休憩をとる必要があります．',
              style: TextStyle(fontSize: 15),
            ),
          ],
        ),
      ),
    );
  }

  CupertinoAlertDialog _alertBuilderForCupertino() {
    return CupertinoAlertDialog(
      title: Text('Alert'),
      content: Text('This is sample.'),
    );
  }

  Stack graph_template() {
    return Stack(
      children: <Widget>[
        AspectRatio(
          aspectRatio: 1,
          child: Container(
            decoration: const BoxDecoration(
                borderRadius: BorderRadius.all(
                  Radius.circular(0),
                ),
                color: Color(0xffffffff)),
            child: Padding(
              padding: const EdgeInsets.only(
                  right: 18.0, left: 12.0, top: 24, bottom: 12),
              child: LineChart(
                showAvg ? avgData() : mainData(),
              ),
            ),
          ),
        ),
        // SizedBox(
        //   width: 60,
        //   height: 34,
        //   child: TextButton(
        //     onPressed: () {
        //       setState(() {
        //         showAvg = !showAvg;
        //       });
        //     },
        //     child: Text(
        //       'AVG',
        //       style: TextStyle(
        //           fontSize: 12,
        //           color:
        //               showAvg ? Colors.black.withOpacity(0.5) : Colors.black),
        //     ),
        //   ),
        // ),
      ],
    );
  }

  Widget bottomTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      color: Color(0xff67727d),
      fontWeight: FontWeight.bold,
      fontSize: 16,
    );
    Widget text;
    switch (value.toInt()) {
      case 0:
        text = const Text('15分前', style: style);
        break;
      case 160:
        text = const Text('10分前', style: style);
        break;
      case 320:
        text = const Text('5分前', style: style);
        break;
      case 480:
        text = const Text('0分前', style: style);
        break;
      default:
        text = const Text('', style: style);
        break;
    }

    return SideTitleWidget(
      axisSide: meta.axisSide,
      space: 8.0,
      child: text,
    );
  }

  Widget leftTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      color: Color(0xff67727d),
      fontWeight: FontWeight.bold,
      fontSize: 15,
    );
    String text;
    switch (value.toInt()) {
      case 0:
        text = '0%';
        break;
      case 50:
        text = '50%';
        break;
      case 100:
        text = '100%';
        break;
      default:
        return Container();
    }

    return Text(text, style: style, textAlign: TextAlign.left);
  }

  LineChartData mainData() {
    return LineChartData(
      gridData: FlGridData(
        show: true,
        drawVerticalLine: true,
        horizontalInterval: 10,
        verticalInterval: 50,
        getDrawingHorizontalLine: (value) {
          return FlLine(
            color: const Color(0xff37434d),
            strokeWidth: 1,
          );
        },
        getDrawingVerticalLine: (value) {
          return FlLine(
            color: const Color(0xff37434d),
            strokeWidth: 1,
          );
        },
      ),
      titlesData: FlTitlesData(
        show: true,
        rightTitles: AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        topTitles: AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 30,
            interval: 1,
            getTitlesWidget: bottomTitleWidgets,
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            interval: 1,
            getTitlesWidget: leftTitleWidgets,
            reservedSize: 42,
          ),
        ),
      ),
      borderData: FlBorderData(
          show: true,
          border: Border.all(color: const Color(0xff37434d), width: 1)),
      minX: 0,
      maxX: 490,
      minY: 0,
      maxY: 100,
      lineBarsData: [
        LineChartBarData(
          spots: evals_min,
          isCurved: false,
          // color: Color(0xff67727d),
          gradient: LinearGradient(
            colors: gradientColors,
            begin: Alignment.centerLeft,
            end: Alignment.centerRight,
          ),
          barWidth: 5,
          isStrokeCapRound: true,
          dotData: FlDotData(
            show: false,
          ),
          belowBarData: BarAreaData(
            show: true,
            gradient: LinearGradient(
              colors: gradientColors
                  .map((color) => color.withOpacity(0.3))
                  .toList(),
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
            ),
          ),
        ),
      ],
    );
  }

  LineChartData avgData() {
    return LineChartData(
      lineTouchData: LineTouchData(enabled: false),
      gridData: FlGridData(
        show: true,
        drawHorizontalLine: true,
        verticalInterval: 10,
        horizontalInterval: 10,
        getDrawingVerticalLine: (value) {
          return FlLine(
            color: const Color(0xff37434d),
            strokeWidth: 1,
          );
        },
        getDrawingHorizontalLine: (value) {
          return FlLine(
            color: const Color(0xff37434d),
            strokeWidth: 1,
          );
        },
      ),
      titlesData: FlTitlesData(
        show: true,
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 30,
            getTitlesWidget: bottomTitleWidgets,
            interval: 1,
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            getTitlesWidget: leftTitleWidgets,
            reservedSize: 42,
            interval: 1,
          ),
        ),
        topTitles: AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        rightTitles: AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
      ),
      borderData: FlBorderData(
          show: true,
          border: Border.all(color: const Color(0xff37434d), width: 1)),
      minX: 0,
      maxX: 140,
      minY: 0,
      maxY: 110,
      lineBarsData: [
        LineChartBarData(
          spots: evals_hour,
          isCurved: false,
          gradient: LinearGradient(
            colors: [
              ColorTween(begin: gradientColors[0], end: gradientColors[1])
                  .lerp(0.2)!,
              ColorTween(begin: gradientColors[0], end: gradientColors[1])
                  .lerp(0.2)!,
            ],
            begin: Alignment.centerLeft,
            end: Alignment.centerRight,
          ),
          barWidth: 5,
          isStrokeCapRound: true,
          dotData: FlDotData(
            show: false,
          ),
          belowBarData: BarAreaData(
            show: true,
            gradient: LinearGradient(
              colors: [
                ColorTween(begin: gradientColors[0], end: gradientColors[1])
                    .lerp(0.2)!
                    .withOpacity(0.1),
                ColorTween(begin: gradientColors[0], end: gradientColors[1])
                    .lerp(0.2)!
                    .withOpacity(0.1),
              ],
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
            ),
          ),
        ),
      ],
    );
  }

  PieChart aiueo() {
    return PieChart(
      PieChartData(
        startDegreeOffset: 270,
        sections: [
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 2 / 24 * 100,
              titlePositionPercentageOffset: 0.7,
              title: "ゲーム\nテレビ",
              titleStyle: TextStyle(fontSize: 10),
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 1 / 24 * 100,
              titlePositionPercentageOffset: 0.8,
              titleStyle: TextStyle(fontSize: 10),
              title: "寝る\n準備",
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 7 / 24 * 100,
              titlePositionPercentageOffset: 0.5,
              title: "眠",
              titleStyle: TextStyle(fontSize: 10),
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 2 / 24 * 100,
              titleStyle: TextStyle(fontSize: 10),
              titlePositionPercentageOffset: 0.7,
              title: "朝ご飯\nテレビ",
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 4 / 24 * 100,
              title: "?",
              titleStyle: TextStyle(fontSize: 60),
              titlePositionPercentageOffset: 0.7,
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 2 / 24 * 100,
              title: "散歩",
              titleStyle: TextStyle(fontSize: 10),
              titlePositionPercentageOffset: 0.7,
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 1 / 24 * 100,
              title: "晩御飯",
              titleStyle: TextStyle(fontSize: 10),
              titlePositionPercentageOffset: 0.7,
              radius: 160),
          PieChartSectionData(
              borderSide: BorderSide(color: Colors.black, width: 1),
              color: Colors.white,
              value: 5 / 24 * 100,
              title: "家での自由時間\nテレビ\n漫画\nゲーム\nラジオ",
              titleStyle: TextStyle(fontSize: 10),
              titlePositionPercentageOffset: 0.6,
              radius: 160),
        ],
        sectionsSpace: 0,
        centerSpaceRadius: 0,
      ),
    );
  }
}
