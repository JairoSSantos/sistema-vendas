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

        self.labels = {}
        self.entrys = {}
        self.buttons = {}

        self.frames_estoque = {'main': tk.Frame(self.notebook_main)}
        self.frames_estoque['main'].pack(anchor='w', pady=5, padx=5)
        self.frames_estoque['produto'] = tk.LabelFrame(self.frames_estoque['main'], text='Produto', relief=tk.GROOVE)
        self.frames_estoque['produto'].pack(side=tk.LEFT, anchor='n', pady=5, padx=5)
        self.frames_estoque['dados'] = tk.Frame(self.frames_estoque['main'])
        self.frames_estoque['dados'].pack(side=tk.LEFT, anchor='n')
        self.frames_estoque['pesquisar'] = tk.Frame(self.frames_estoque['dados'])
        self.frames_estoque['pesquisar'].pack(pady=5, padx=5)

        labels_texts = ['Código:', 'Nome:', 'Preço de venda:', 'Preço de custo:', 'Quantidade:', 'Descrição:']
        labels_width = sorted(map(lambda a: len(a), labels_texts))[-1]
        self.labels['estoque'] = []
        for i, text in enumerate(labels_texts):
            label = tk.Label(self.frames_estoque['produto'], text=text, width=labels_width, anchor='e')
            label.grid(row=i, column=0, pady=2)
            self.labels['estoque'].append(label)

        entrys_keys = ['code', 'nome', 'p_venda', 'p_custo', 'quantidade', 'desc']
        self.entrys['estoque'] = {}
        for i, key in enumerate(entrys_keys):
            entry = tk.Entry(self.frames_estoque['produto'])
            entry.grid(row=i, column=1, padx=[0, 10])
            self.entrys['estoque'][key] = entry
        
        self.buttons['estoque'] = {}
        button_width = 10
        self.buttons['estoque']['cadastrar'] = tk.Button(self.frames_estoque['produto'], text='Cadastrar', width=button_width)
        self.buttons['estoque']['cadastrar'].grid(row=6, column=0, pady=10)
        self.buttons['estoque']['excluir'] = tk.Button(self.frames_estoque['produto'], text='Excluir', width=button_width)
        self.buttons['estoque']['excluir'].grid(row=6, column=1, pady=10)
        self.buttons['estoque']['filtrar'] = tk.Button(self.frames_estoque['pesquisar'], text='Filtrar', width=button_width)
        self.buttons['estoque']['filtrar'].grid(row=0, column=2, pady=5, padx=7)

        label = tk.Label(self.frames_estoque['pesquisar'], text='Pesquisar:')
        label.grid(row=0, column=0)
        self.labels['estoque'].append(label)

        self.entrys['estoque']['pesquisar'] = tk.Entry(self.frames_estoque['pesquisar'], width=70)
        self.entrys['estoque']['pesquisar'].grid(row=0, column=1)

        self.table_estoque = ttk.Treeview(self.frames_estoque['dados'], 
            columns=['Nome', 'Preço de venda', 'Preço de custo', 'Quantidade'])
        self.table_estoque.column('#0', width=80)
        self.table_estoque.column('Nome', width=250)
        self.table_estoque.column('Preço de venda', width=150)
        self.table_estoque.column('Preço de custo', width=150)
        self.table_estoque.column('Quantidade', width=100)
        self.table_estoque.heading('#0', text='Código')
        self.table_estoque.heading('Nome', text='Nome')
        self.table_estoque.heading('Preço de venda', text='Preço de venda')
        self.table_estoque.heading('Preço de custo', text='Preço de custo')
        self.table_estoque.heading('Quantidade', text='Quantidade')
        self.table_estoque.pack()

        self.frames_estoque['relatório'] = tk.Frame(self.frames_estoque['dados'])
        self.frames_estoque['relatório'].pack(pady=5, padx=5)
        self.labels['estoque'].append(tk.Label(self.frames_estoque['relatório'], text='Produtos cadastrados:', width=30, anchor='w'))
        self.labels['estoque'][-1].pack(side=tk.LEFT)
        self.buttons['estoque']['relatório'] = tk.Button(self.frames_estoque['relatório'], text='Relatório')
        self.buttons['estoque']['relatório'].pack(side=tk.RIGHT)

        self.frame_vendas_main = tk.Frame(self.notebook_main)
        self.frame_vendas_main.pack()

        self.notebook_main.add(self.frames_estoque['main'], text='Estoque')
        self.notebook_main.add(self.frame_vendas_main, text='Vendas')
        self.notebook_main.grid(row=0, column=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()