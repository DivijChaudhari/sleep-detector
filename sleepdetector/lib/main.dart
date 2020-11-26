import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:io';
import 'dart:convert';
import 'dart:isolate';
import 'package:sendsms/sendsms.dart';

var address = new InternetAddress('192.168.2.1');
int port = 4210;
String message;
String name;
bool i;
void mssage() async{
  print('1');

  String phoneNumber = "+919105558877";
  String message = "i am feeling sleepy contact me https://maps.google.com/?q=28.895022,76.599212";

  await Sendsms.onGetPermission();

  if (await Sendsms.hasPermission()) {
    await Sendsms.onSendSMS(phoneNumber, message);
  }
}
void foo(var message){

  Future.wait([RawDatagramSocket.bind(InternetAddress.anyIPv4, 0)]).then((values) {
    RawDatagramSocket udpSocket = values[0];
    udpSocket.listen((RawSocketEvent e) async {
      print(e);
      name='not start';
      while(true) {

        udpSocket.send(new Utf8Codec().encode('check'), address, port);
        udpSocket.writeEventsEnabled = false;
        udpSocket.readEventsEnabled = true;
        sleep(const Duration(seconds: 5));
        Datagram dg = udpSocket.receive();
        if (dg != null) {
          message = new String.fromCharCodes(dg.data);
          if(message=='emergency') {
            name = 'emergency';
            print('ddkd');
           i=true;}

          else if(message=='no emergency'){
            name='no';
            print(message);
            i=false;
          }
        }
        udpSocket.readEventsEnabled = false;
      }
      // udpSocket.close();

    });
  });

}
void main() {

  runApp(MyApp());
  try{
    Isolate.spawn(foo,'Hello!!'); }
  catch(e){
  while(true){
    if(i){
      mssage();
    }
    else{
      print('1');
      continue;
    }
  }
  }
}

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'sleep',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'sleep App'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: SafeArea(
        child: ListView(
          children: <Widget>[
            Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Padding(
                    padding: EdgeInsets.all(16.0),
                  ),
                  RaisedButton(
                    onPressed: () async {
                     await mssage();
                    },
                    child: Text('hello'),
                    color: Colors.blue,
                  ),
                ]
            ),
          ],
        ),
      ),
    );
  }
}

