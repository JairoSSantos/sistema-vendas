import 'package:flutter/material.dart';

final fields = {
  'code': 'Código',
  'name': 'Nome do Produto',
  'cost': 'Preço de Custo',
  'price': 'Preço de Venda',
  'quantity': 'Quantidade'
};

void main() {
  runApp(
    MaterialApp(
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 183, 0, 255)),
        useMaterial3: true,
      ),
      home: const StorageApp(title: 'Controle de Estoque'),
    )
  );
}

class StorageApp extends StatefulWidget {
  const StorageApp({super.key, required this.title});
  final String title;

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
        title: Text(widget.title),
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
