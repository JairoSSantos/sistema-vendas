import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data

class SalePay:
    def __init__(self):
        self.items = []
        self.date = None
        self.index = None
        self.paid = None

    def add(self, *args): 
        self.items.append(args)
    
    def confirm(self, form): 
        data.sales.add(
            [[int(un), id_item] 
                for id_item, un, name, p_venda, total in self.items], 
            self.get_total(), self.paid, form, self.mods)
    
    def get_change(self):
        return self.paid - self.get_total()

    def get_total(self):
        return sum([item[4] for item in self.items])
    
    def set_paid(self, value): self.paid = value
    
    def new(self, index=0, date='00/00/0000'):
        self.items.clear()
        self.date = date
        self.index = index

class ConfirmApp:
    def __init__(self, root, sale):
        self.root = root
        self.sale = sale
        tk.Label(self.root, text=f'ID: {self.sale.index}  Data: {self.sale.date}').pack()
        tk.Label(self.root, text=f'Total: {self.sale.get_total():.2f} R$').pack()

        self.val_recebido = tk.StringVar()
        self.val_recebido.set('Valor recebido: 00,00 R$')
        tk.Label(self.root, textvariable=self.val_recebido).pack()

        self.troco = tk.StringVar()
        self.troco.set('Troco: 00,00 R$')
        tk.Label(self.root, textvariable=self.troco).pack()

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack()
        tk.Button(buttons_frame, text='Confirmar F2', command=self.confirm).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text='Cancelar ESC', command=self.cancel).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text='Desconto F4', command=self.set_mod).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text='Calculadora F3').pack(side=tk.LEFT)
        self.root.bind('<KeyRelease>', self.payvalue)
        self.root.bind('<F2>', self.confirm)
        self.root.bind('<Escape>', self.cancel)
        self.root.focus_force()
        self.root.mainloop()
    
    def cancel(self):
        if messagebox.showwarning('Cancelar venda', 'Deseja iniciar nova venda?'):
            self.sale.new()
        self.root.destroy()

    def confirm(self):
        self.sale.confirm()
        self.sale.new()
        self.root.destroy()
    
    def payvalue(self, event):
        dec = [int(char) for char in self.val_recebido.get().lstrip('0') if char.isnumeric()]
        try: value = int(event.char)
        except ValueError:
            if event.keysym == 'BackSpace': del dec[-1]
        else: dec.append(value)
        finally:
            while len(dec) < 3: dec.insert(0, 0)
            dec.insert(-2, ',')
            dec = ''.join(map(str, dec))
            val = float(dec.replace(',', '.'))
            self.val_recebido.set(f'Valor recebido: {dec} R$')
            self.troco.set(f'Troco: {self.sale.get_change(val):.2f} R$'.replace('.', ','))

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
            'Código':100,
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
        self.buttons['confirmar'] = tk.Button(self.frames['control'], text='Confirmar F2', command=self.confirm)
        self.buttons['confirmar'].pack(side=tk.LEFT)
        self.buttons['cancelar'] = tk.Button(self.frames['control'], text='Cancelar ESC', command=self.cancel)
        self.buttons['cancelar'].pack(side=tk.LEFT)
        self.buttons['calculadora'] = tk.Button(self.frames['control'], text='Calculadora F3')
        self.buttons['calculadora'].pack(side=tk.LEFT)

        self.root.bind('<F2>', self.confirm)
        self.root.bind('<Escape>', self.cancel)

        self.sale = SalePay()
    
    def cancel(self, event=None):
        self.sale.new()
        self.update()

    def confirm(self, event=None):
        toplevel = ConfirmApp(tk.Toplevel(self.root), self.sale)

    def delete(self, event):
        item = self.tree.item(self.tree.focus())
        try: id_item = int(item['text'])
        except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
        else:
            if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][1])):
                self.sale.items.pop(id_item)
        finally: self.update()
    
    def update(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, item in enumerate(self.sale.items):
            self.tree.insert('', i, text=i, values=item)
        total = self.sale.get_total()
        self.vars['total'].set(f'Total: {total:.2f} R$')
        self.root.update()
    
    def verify_code(self, event):
        value = self.entrys['codigo'].get()
        try: un, value = map(int, value.split('x')) if 'x' in value else [1, int(value)]
        except ValueError: messagebox.showwarning('Formáto inválido.', 'Erro no formato do código.\nDigite corretamente.')
        else:
            try: nome, p_venda = data.storage.get_value(value, 'nome', 'p_venda')
            except Exception as error: messagebox.showwarning('Erro no código.', error)
            else: 
                self.sale.add(value, un, nome, p_venda, p_venda*un)
                self.vars['produto info'].set(f'{value} {un}  {nome}  {p_venda:.2f} R$')
        finally: self.entrys['codigo'].delete(0, tk.END); self.update()

if __name__ == '__main__':
    data.init()
    root = tk.Tk()
    app = App(root)
    root.mainloop()