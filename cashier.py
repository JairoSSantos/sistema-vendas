import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Caixa')

        self.frames = {}
        self.vars = {}
        self.entrys = {}
        self.buttons = {}

        self.frames['info'] = tk.Frame(self.root)
        self.frames['info'].pack(fill='x')

        self.vars['total'] = tk.StringVar()
        self.vars['total'].set('Total: 00,00 R$')
        tk.Label(self.frames['info'], textvariable=self.vars['total']).pack(anchor='nw', side=tk.LEFT)

        self.vars['arquivo info'] = tk.StringVar()
        self.vars['arquivo info'].set('ID: 00000  Data: 00/00/0000')
        tk.Label(self.frames['info'], textvariable=self.vars['arquivo info']).pack(anchor='e')

        self.vars['produto info'] = tk.StringVar()
        self.vars['produto info'].set('<código> <unidades> <nome> <preço>')
        tk.Label(self.frames['info'], textvariable=self.vars['produto info']).pack(anchor='sw', side=tk.LEFT)

        columns = {
            'Un':70,
            'Nome do produto':200,
            'Preço unitário':100,
            'Preço total':100
        }

        self.tree = ttk.Treeview(self.root, columns=list(columns.keys()))
        self.tree.column('#0', width=70)
        self.tree.heading('#0', text='Item')
        for name, width in columns.items():
            self.tree.column(name, width=width)
            self.tree.heading(name, text=name)
        self.tree.pack()

        self.frames['control'] = tk.Frame(self.root)
        self.frames['control'].pack()

        tk.Label(self.frames['control'], text='Código do produto:').pack(side=tk.LEFT)
        self.entrys['codigo'] = tk.Entry(self.frames['control'])
        self.entrys['codigo'].pack(side=tk.LEFT)
        self.buttons['confirmar'] = tk.Button(self.frames['control'], text='Confirmar')
        self.buttons['confirmar'].pack(side=tk.LEFT)
        self.buttons['cancelar'] = tk.Button(self.frames['control'], text='Cancelar')
        self.buttons['cancelar'].pack(side=tk.LEFT)
        self.buttons['calculadora'] = tk.Button(self.frames['control'], text='Calculadora')
        self.buttons['calculadora'].pack(side=tk.LEFT)

if __name__ == '__main__':
    data.init()
    root = tk.Tk()
    app = App(root)
    root.mainloop()