import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';
import 'package:mysql1/mysql1.dart';

final loginLabels = {
  'user': 'Usuário',
  'password': 'Senha'
};

final fields = {
  'code': 'Código',
  'name': 'Nome do Produto',
  'cost': 'Preço de Custo',
  'price': 'Preço de Venda',
  'quantity': 'Quantidade'
};

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Must add this line.
  await windowManager.ensureInitialized();

  windowManager.waitUntilReadyToShow(const WindowOptions(), () async {
    await windowManager.show();
    await windowManager.focus();
    await windowManager.maximize();
  });

  runApp(
    MaterialApp(
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 183, 0, 255)),
        useMaterial3: true,
      ),
      home: const LoginApp(),
    )
  );
}

class LoginApp extends StatefulWidget {
  const LoginApp({super.key});

  @override
  State<LoginApp> createState() => _LoginAppState();
}

class _LoginAppState extends State<LoginApp> {

  late Map<String, TextEditingController> _formControllers;

  @override
  void initState() {
    super.initState();

    _formControllers = {
      'user': TextEditingController(text:'root'),
      'password': TextEditingController(),
    };
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      body: Center(
        child: SizedBox(
          width: 600,
          child: Card(
            surfaceTintColor: Theme.of(context).colorScheme.onInverseSurface,
            elevation: 10,
            child: Padding(
              padding: const EdgeInsets.all(50),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  for (final field in _formControllers.entries)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 20),
                    child: TextField(
                      controller: field.value,
                      obscureText: (field.key == 'password'),
                      decoration: InputDecoration(
                        border: const OutlineInputBorder(),
                        labelText: loginLabels[field.key],
                        hintText: field.value.text,
                      ),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () => MySqlConnection.connect(
                      ConnectionSettings(
                        user: _formControllers['user']?.text, 
                        password:_formControllers['password']?.text
                      )
                    ).then(
                      (connection) {
                        Navigator.pushReplacement(
                          context, 
                          MaterialPageRoute(builder: 
                            (context) => StorageApp(connection: connection)
                          )
                        );
                      }
                    ), 
                    child: const Text('Acessar')
                  ),
                ],
              ),
            )
          )
        ),
      )
    );
  }
}

class StorageApp extends StatefulWidget {
  final MySqlConnection connection;

  const StorageApp({super.key, required this.connection});

  @override
  State<StorageApp> createState() => _StorageAppState();
}

class _StorageAppState extends State<StorageApp> {

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Controle de Estoque'),
        leading: IconButton(onPressed: ()=>{}, icon: const Icon(Icons.menu_rounded)),
      ),
      body: Column(
        children: [
          Row(
            children: [
              for (final label in fields.values)
              Flexible(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
                  child: TextFormField(
                    decoration:InputDecoration(
                      border: const OutlineInputBorder(),
                      labelText: label,
                    ),
                  ),
                ),
              )
            ],
          ),
          Card(
            borderOnForeground: false,
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    for (final field in fields.entries)
                    ...[
                      Text(field.value),
                      const VerticalDivider()
                    ]
                  ],
                ),
              ],
            ),
          )
        ],
      )
    );
  }
}
