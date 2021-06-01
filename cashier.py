import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import data

class SalePay:
    def __init__(self):
        self.items = []
        self.total = 0
        self.paid = 0
        self.mod = 0

    def add(self, codigo, unidades, nome, preco):
        '''
        Adicionar produto à venda.
        
        Args:
            codigo: int; código do produto.
            unidades: int; quantidade vendida.
            nome: string; nome do produto.
            preco: float; preço do produto.
        '''
        self.total += preco*unidades
        self.items.append([codigo, unidades, nome, preco, preco*unidades])
    
    def confirm(self, form): 
        '''
        Confirmar venda.
        '''
        stuff = [] 
        for id_item, un, name, p_venda, total in self.items:
            stuff.append([int(un), int(id_item)])
            data.storage.decrease(int(id_item), int(un))
        data.sales.add(stuff, self.total, self.paid, form, self.mod)
    
    def get_change(self):
        return self.paid - self.total

    def new(self): self.__init__()
    
    def set_mod(self, value): 
        self.mod += value
        self.total *= 1 + self.mod/100

    def set_paid(self, value): self.paid = value
    
class ConfirmApp:
    def __init__(self, root, sale):
        self.root = root
        self.sale = sale

        ID = str(data.sales.get_next_id())
        while len(ID) < 5: ID = '0'+ID
        tk.Label(self.root, text=f'ID: {ID}  Data: {data.sales.get_current_date()}').pack()

        self.form = tk.StringVar()
        self.form.set(f'Formato: Dinheiro')
        tk.Label(self.root, textvariable=self.form).pack()

        self.val_total = tk.StringVar()
        self.val_total.set(f'Total: R$ {self.sale.total:.2f}')
        tk.Label(self.root, textvariable=self.val_total).pack()

        self.val_recebido = tk.StringVar()
        self.val_recebido.set('Valor recebido: R$ 0,00')
        tk.Label(self.root, textvariable=self.val_recebido).pack()

        self.troco = tk.StringVar()
        self.troco.set('Troco: R$ 0,00')
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
        self.root.bind('<F4>', self.set_mod)
        self.root.focus_force()
        self.root.mainloop()
    
    def cancel(self, event=None):
        if messagebox.showwarning('Cancelar venda', 'Deseja iniciar nova venda?'):
            self.sale.new()
        self.root.destroy()

    def confirm(self, event=None):
        self.sale.confirm(self.form.get().split(':')[-1].strip(' ').lower())
        self.sale.new()
        self.root.destroy()
    
    def payvalue(self, event): # valor pago
        # pegar valor da inerface
        dec = []
        for char in self.val_recebido.get():
            if char.isnumeric():
                if char != '0' or (char == '0' and len(dec)): dec.append(char)

        try: value = int(event.char) # pegar valor digitado
        except ValueError: # se valor não for numeral
            key = event.keysym
            if key == 'BackSpace': del dec[-1] # se for backspace então apague o ultimo valor digitado
            elif key in ('Up', 'Down'): 
                nform = ['dinheiro', 'cartão de crédito', 'cartão de débito']
                i = nform.index(self.form.get().split(':')[-1].strip(' ').lower()) + {'Up':1, 'Down':-1}[key]
                if i > len(nform)-1: i = 0
                self.form.set(f'Formato: {nform[i]}')
        else: dec.append(value) # se for um numero adicione no final do texto
        finally:
            while len(dec) < 3: dec.insert(0, 0) # complete a lista com 0
            dec.insert(-2, ',') # adicione a vísgula para as casas decimais
            dec = ''.join(map(str, dec)) # juntar em texto
            self.val_recebido.set(f'Valor recebido: R$ {dec}') # mudar valor na interface
            self.sale.set_paid(float(dec.replace(',', '.'))) # definir valor pago
            self.troco.set(f'Troco: R$ {self.sale.get_change():.2f}'.replace('.', ',')) # mostrar troco na interface
    
    def set_mod(self, event=None):
        try:
            value = float(simpledialog.askstring('Desconto', 
                'Digite o valor em porcentagem (%) do desconto:', parent=self.root).replace(',', '.'))
        except ValueError: 
            messagebox.showwarning('Formato inválido', 'Formato inválido!\nDigite o valor corretamente!', parent=self.root)
            self.set_mod(event)
        else:
            self.sale.set_mod(-value)
            self.val_total.set(f'Total: R$ {self.sale.total:.2f}')
            self.troco.set(f'Troco: R$ {self.sale.get_change():.2f}'.replace('.', ',')) # mostrar troco na interface
            self.root.update()

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
        self.vars['total'].set('Total: 0,00 R$')
        tk.Label(self.frames['info'], textvariable=self.vars['total']).grid(row=0, column=0, sticky='w')

        self.vars['arquivo info'] = tk.StringVar()
        ID = str(data.sales.get_next_id())
        while len(ID) < 5: ID = '0'+ID
        self.vars['arquivo info'].set(f'ID: {ID}  Data: {data.sales.get_current_date()}')
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
        self.update()
    
    def cancel(self, event=None):
        self.sale.new()
        self.update()

    def confirm(self, event=None):
        toplevel = ConfirmApp(tk.Toplevel(self.root), self.sale)
        ID = str(data.sales.get_next_id())
        while len(ID) < 5: ID = '0'+ID
        self.vars['arquivo info'].set(f'ID: {ID}  Data: {data.sales.get_current_date()}')
        self.root.update()

    def delete(self, event):
        item = self.tree.item(self.tree.focus())
        try: index = int(item['text'])
        except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
        else:
            if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][1])):
                self.sale.items.pop(index)
        finally: self.update()
    
    def update(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, item in enumerate(self.sale.items):
            self.tree.insert('', i, text=i, values=item)
        self.vars['total'].set(f'Total: {self.sale.total:.2f} R$')
        self.root.update()
    
    def verify_code(self, event):
        value = self.entrys['codigo'].get()
        try: un, value = map(int, value.split('x')) if 'x' in value else [1, int(value)]
        except ValueError: messagebox.showwarning('Formáto inválido.', 'Erro no formato do código.\nDigite corretamente.')
        else:
            try: nome, p_venda = data.storage.get_value(value, 'nome', 'p_venda')
            except Exception as error: messagebox.showwarning('Erro no código.', error)
            else: 
                self.sale.add(value, un, nome, p_venda)
                self.vars['produto info'].set(f'{value} {un}  {nome}  {p_venda:.2f} R$')
        finally: self.entrys['codigo'].delete(0, tk.END); self.update()

if __name__ == '__main__':
    data.init()
    data.sales.set_current_file()
    root = tk.Tk()
    app = App(root)
    root.mainloop()