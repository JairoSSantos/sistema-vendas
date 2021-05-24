import tkinter as tk
from tkinter import ttk
import data

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Controle de dados')
        # self.root.state('zoomed')
        # self.root.geometry(self.root.winfo_geometry())

        ttk.Style().configure('TNotebook', tabposition='wn')
        self.notebook_main = ttk.Notebook(self.root)

        self.frames = {}
        self.labels = {}
        self.entrys = {'estoque':{}, 'vendas':{}}
        self.buttons = {'estoque':{}, 'vendas':{}}
        self.trees = {}

        self.frames['estoque'] = {'main': tk.Frame(self.notebook_main)}
        self.frames['estoque']['main'].pack(anchor='w', pady=5, padx=5)
        self.frames['estoque']['produto'] = tk.LabelFrame(self.frames['estoque']['main'], text='Produto', relief=tk.GROOVE)
        self.frames['estoque']['produto'].pack(side=tk.LEFT, anchor='n', pady=5, padx=5)
        self.frames['estoque']['dados'] = tk.Frame(self.frames['estoque']['main'])
        self.frames['estoque']['dados'].pack(side=tk.LEFT, anchor='n')
        self.frames['estoque']['pesquisar'] = tk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['pesquisar'].pack(pady=5, padx=5)

        labels_texts = ['Código:', 'Nome:', 'Preço de venda:', 'Preço de custo:', 'Quantidade:', 'Descrição:']
        labels_width = sorted(map(lambda a: len(a), labels_texts))[-1]
        self.labels['estoque'] = []
        for i, text in enumerate(labels_texts):
            label = tk.Label(self.frames['estoque']['produto'], text=text, width=labels_width, anchor='e')
            label.grid(row=i, column=0, pady=2)
            self.labels['estoque'].append(label)

        entrys_keys = ['code', 'nome', 'p_venda', 'p_custo', 'quantidade', 'desc']
        for i, key in enumerate(entrys_keys):
            entry = tk.Entry(self.frames['estoque']['produto'])
            entry.grid(row=i, column=1, padx=[0, 10])
            self.entrys['estoque'][key] = entry

        button_width = 10
        self.buttons['estoque']['cadastrar'] = tk.Button(self.frames['estoque']['produto'], text='Cadastrar', width=button_width)
        self.buttons['estoque']['cadastrar'].grid(row=6, column=0, pady=10)
        self.buttons['estoque']['excluir'] = tk.Button(self.frames['estoque']['produto'], text='Excluir', width=button_width)
        self.buttons['estoque']['excluir'].grid(row=6, column=1, pady=10)
        self.buttons['estoque']['filtrar'] = tk.Button(self.frames['estoque']['pesquisar'], text='Filtrar', width=button_width)
        self.buttons['estoque']['filtrar'].grid(row=0, column=2, pady=5, padx=7)

        label = tk.Label(self.frames['estoque']['pesquisar'], text='Pesquisar:')
        label.grid(row=0, column=0)
        self.labels['estoque'].append(label)

        self.entrys['estoque']['pesquisar'] = tk.Entry(self.frames['estoque']['pesquisar'], width=70)
        self.entrys['estoque']['pesquisar'].grid(row=0, column=1)

        columns = {
            '#0':['Código', 80],
            'nome':['Nome', 250],
            'p_venda':['Preço de venda', 150],
            'p_custo':['Preço de custo', 150],
            'quantidade':['Quantidade', 100]
        }

        self.trees['estoque'] = ttk.Treeview(self.frames['estoque']['dados'], columns=list(columns.keys())[1:])
        for key, (text, width) in columns.items():
            self.trees['estoque'].column(key, width=width)
            self.trees['estoque'].heading(key, text=text)
        self.trees['estoque'].pack()

        self.frames['estoque']['relatório'] = tk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['relatório'].pack(pady=5, padx=5, fill='x')
        self.labels['estoque'].append(tk.Label(self.frames['estoque']['relatório'], text='Produtos cadastrados:', width=30, anchor='w'))
        self.labels['estoque'][-1].pack(side=tk.LEFT)
        self.buttons['estoque']['relatório'] = tk.Button(self.frames['estoque']['relatório'], text='Relatório')
        self.buttons['estoque']['relatório'].pack(side=tk.RIGHT)

        self.frames['vendas'] = {'main': tk.Frame(self.notebook_main)}
        self.frames['vendas']['main'].pack()
        self.frames['vendas']['dados'] = tk.Frame(self.frames['vendas']['main'])
        self.frames['vendas']['dados'].pack()

        self.labels['vendas'] = []
        self.labels['vendas'].append(tk.Label(self.frames['vendas']['dados'], text='Arquivo de vendas:'))
        self.labels['vendas'][-1].pack(side=tk.LEFT)
        self.labels['vendas'].append(tk.Label(self.frames['vendas']['dados'], text='Pesquisar:'))
        self.labels['vendas'][-1].pack(side=tk.LEFT)

        self.entrys['vendas']['pesquisar'] = tk.Entry(self.frames['vendas']['dados'])
        self.entrys['vendas']['pesquisar'].pack(side=tk.LEFT)

        self.buttons['vendas']['filtrar'] = tk.Button(self.frames['vendas']['dados'], text='Filtrar')
        self.buttons['vendas']['filtrar'].pack(side=tk.LEFT)

        columns = {
            '#0':['Id', 80],
            'horario':['Horário da venda', 150],
            'total':['Total', 100],
            'pago':['Valor pago', 100],
            'formato':['Formato de pagamento', 150]
        }

        self.trees['vendas'] = ttk.Treeview(self.frames['vendas']['main'], columns=list(columns.keys())[1:])
        for key, (text, width) in columns.items():
            self.trees['vendas'].column(key, width=width)
            self.trees['vendas'].heading(key, text=text)
        self.trees['vendas'].pack()

        self.notebook_main.add(self.frames['estoque']['main'], text='Estoque')
        self.notebook_main.add(self.frames['vendas']['main'], text='Vendas')
        self.notebook_main.grid(row=0, column=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()