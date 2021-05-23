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

        self.frames_estoque = {'main': tk.Frame(self.notebook_main)}
        self.frames_estoque['main'].pack(anchor='w', pady=5, padx=5)
        self.frames_estoque['produto'] = tk.LabelFrame(self.frames_estoque['main'], text='Produto', relief=tk.GROOVE)
        self.frames_estoque['produto'].pack(side=tk.LEFT, anchor='n', pady=5, padx=5)
        self.frames_estoque['pesquisar'] = tk.LabelFrame(self.frames_estoque['main'])
        self.frames_estoque['pesquisar'].pack(pady=5, padx=5)

        self.label_estoque_id = tk.Label(self.frames_estoque['produto'], text='Id:')
        self.label_estoque_id.grid(row=0, column=0)
        self.entry_estoque_id = tk.Entry(self.frames_estoque['produto'])
        self.entry_estoque_id.grid(row=0, column=1)

        self.label_estoque_nome = tk.Label(self.frames_estoque['produto'], text='Nome:')
        self.label_estoque_nome.grid(row=1, column=0)
        self.entry_estoque_nome = tk.Entry(self.frames_estoque['produto'])
        self.entry_estoque_nome.grid(row=1, column=1)

        self.label_estoque_pvenda = tk.Label(self.frames_estoque['produto'], text='Preço de venda:')
        self.label_estoque_pvenda.grid(row=2, column=0)
        self.entry_estoque_pvenda = tk.Entry(self.frames_estoque['produto'])
        self.entry_estoque_pvenda.grid(row=2, column=1)

        self.label_estoque_pcusto = tk.Label(self.frames_estoque['produto'], text='Preço de custo:')
        self.label_estoque_pcusto.grid(row=3, column=0)
        self.entry_estoque_pcusto = tk.Entry(self.frames_estoque['produto'])
        self.entry_estoque_pcusto.grid(row=3, column=1)

        self.label_estoque_quant = tk.Label(self.frames_estoque['produto'], text='Quantidade:')
        self.label_estoque_quant.grid(row=4, column=0)
        self.entry_estoque_quant = tk.Entry(self.frames_estoque['produto'])
        self.entry_estoque_quant.grid(row=4, column=1)

        self.button_estoque_cadastrar = tk.Button(self.frames_estoque['produto'], text='Cadastrar')
        self.button_estoque_cadastrar.grid(row=5, column=0, pady=10)

        self.label_estoque_pesq = tk.Label(self.frames_estoque['pesquisar'], text='Pesquisar:')
        self.label_estoque_pesq.grid(row=0, column=0)
        self.entry_estoque_pesq = tk.Entry(self.frames_estoque['pesquisar'], width=100)
        self.entry_estoque_pesq.grid(row=0, column=1)

        self.table_estoque = ttk.Treeview(self.frames_estoque['main'], 
            columns=['Nome', 'Preço de venda', 'Preço de custo', 'Quantidade'])
        self.table_estoque.column('#0', width=80)
        self.table_estoque.column('Nome', width=250)
        self.table_estoque.column('Preço de venda', width=150)
        self.table_estoque.column('Preço de custo', width=150)
        self.table_estoque.column('Quantidade', width=100)
        self.table_estoque.heading('#0', text='id')
        self.table_estoque.heading('Nome', text='Nome')
        self.table_estoque.heading('Preço de venda', text='Preço de venda')
        self.table_estoque.heading('Preço de custo', text='Preço de custo')
        self.table_estoque.heading('Quantidade', text='Quantidade')
        self.table_estoque.pack(side=tk.RIGHT)

        self.frame_vendas_main = tk.Frame(self.notebook_main)
        self.frame_vendas_main.pack()

        self.notebook_main.add(self.frames_estoque['main'], text='Estoque')
        self.notebook_main.add(self.frame_vendas_main, text='Vendas')
        self.notebook_main.grid(row=0, column=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()