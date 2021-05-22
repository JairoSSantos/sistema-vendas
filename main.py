import tkinter as tk
from tkinter import ttk
import data

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Controle de dados')
        # self.root.state('zoomed')

        ttk.Style().configure('TNotebook', tabposition='wn')
        self.notebook_main = ttk.Notebook(self.root)

        self.frame_estoque_main = tk.Frame(self.notebook_main)
        self.frame_estoque_main.pack()

        self.frame_estoque_00 = tk.LabelFrame(self.frame_estoque_main, text='Produto', relief=tk.GROOVE)
        self.frame_estoque_00.pack()

        self.label_estoque_00 = tk.Label(self.frame_estoque_00, text='Nome:')
        self.label_estoque_00.grid(row=0, column=0)
        self.entry_estoque_00 = tk.Entry(self.frame_estoque_00)
        self.entry_estoque_00.grid(row=0, column=1)

        self.label_estoque_01 = tk.Label(self.frame_estoque_00, text='Preço de venda:')
        self.label_estoque_01.grid(row=0, column=4)
        self.entry_estoque_01 = tk.Entry(self.frame_estoque_00)
        self.entry_estoque_01.grid(row=0, column=5)

        self.label_estoque_02 = tk.Label(self.frame_estoque_00, text='Preço de custo:')
        self.label_estoque_02.grid(row=0, column=6)
        self.entry_estoque_02 = tk.Entry(self.frame_estoque_00)
        self.entry_estoque_02.grid(row=0, column=7)

        self.label_estoque_03 = tk.Label(self.frame_estoque_00, text='Quantidade:')
        self.label_estoque_03.grid(row=0, column=2)
        self.entry_estoque_03 = tk.Entry(self.frame_estoque_00)
        self.entry_estoque_03.grid(row=0, column=3)

        self.table_estoque = ttk.Treeview(self.frame_estoque_main, 
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
        self.table_estoque.pack()

        self.frame_vendas_main = tk.Frame(self.notebook_main)
        self.frame_vendas_main.pack()

        self.notebook_main.add(self.frame_estoque_main, text='Estoque')
        self.notebook_main.add(self.frame_vendas_main, text='Vendas')
        self.notebook_main.grid(row=0, column=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()