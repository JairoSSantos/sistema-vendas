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
        tk.Label(self.frames['info'], textvariable=self.vars['total']).grid(row=0, column=0, sticky='w')

        self.vars['arquivo info'] = tk.StringVar()
        self.vars['arquivo info'].set('ID: 00000  Data: 00/00/0000')
        tk.Label(self.frames['info'], textvariable=self.vars['arquivo info'], justify=tk.RIGHT).grid(row=0, column=1)

        self.vars['produto info'] = tk.StringVar()
        self.vars['produto info'].set('<código> <unidades> <nome> <preço>')
        tk.Label(self.frames['info'], 
            textvariable=self.vars['produto info'], justify=tk.LEFT).grid(row=1, column=0, sticky='w')

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
        self.tree.bind('<Delete>', self.delete)
        self.tree.pack()

        self.frames['control'] = tk.Frame(self.root)
        self.frames['control'].pack()

        tk.Label(self.frames['control'], text='Código do produto:').pack(side=tk.LEFT)
        self.entrys['codigo'] = tk.Entry(self.frames['control'])
        self.entrys['codigo'].bind('<Return>', self.verify_code)
        self.entrys['codigo'].pack(side=tk.LEFT)
        self.buttons['confirmar'] = tk.Button(self.frames['control'], text='Confirmar F2')
        self.buttons['confirmar'].pack(side=tk.LEFT)
        self.buttons['cancelar'] = tk.Button(self.frames['control'], text='Cancelar ESC')
        self.buttons['cancelar'].pack(side=tk.LEFT)
        self.buttons['calculadora'] = tk.Button(self.frames['control'], text='Calculadora F3')
        self.buttons['calculadora'].pack(side=tk.LEFT)

        self.root.bind('<F2>', self.confirm)
        self.root.bind('<Escape>', self.cancel)
    
    def cancel(self, event):
        for i in self.tree.get_children(): self.tree.delete(i)

    def confirm(self, event): pass

    def delete(self, event):
        item = self.tree.item(self.tree.focus())['text']
        if item == '': messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
        elif messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][0])): self.tree.delete(int(item))
    
    def verify_code(self, event):
        value = self.entrys['codigo'].get()
        try:quant, value = map(int, value.split('x')) if 'x' in value else [1, int(value)]
        except ValueError: messagebox.showwarning('Formáto inválido.', 'Erro no formato do código.\nDigite corretamente.')
        else:
            try: nome, p_venda = data.storage.get_value(value, 'nome', 'p_venda')
            except Exception as error: messagebox.showwarning('Erro no código.', error)
            else: self.tree.insert('', 'end', text=len(self.tree.get_children()), values=[quant, nome, p_venda, p_venda*quant])
        finally: self.entrys['codigo'].delete(0, tk.END)
        self.root.update()

if __name__ == '__main__':
    data.init()
    root = tk.Tk()
    app = App(root)
    root.mainloop()