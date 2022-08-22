import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from apps.database import Table
from datetime import date
from apps import theme
import traceback

def update(function):
    def wrapper(app, *args, **kwargs):
        function(app, *args, **kwargs)
        app.update()
    return wrapper

def exception(function):
    def wrapper(app, *args, **kwargs):
        try: function(app, *args, **kwargs)
        except Exception as error: 
            messagebox.showerror(error, traceback.format_exc(), parent=app)
    return wrapper
    
class ConfirmApp(tk.Frame):
    def __init__(self, master, mainapp):
        super().__init__(master=master)
        self.config(bg=theme.colors[0])
        self.pack()
        self.mainapp = mainapp
        self.extra = 0

        today = date.today().strftime('%d/%m/%Y')
        tk.Label(self, text=f'ID: {self.mainapp.ID}  Data: {today}',
            font=theme.fonts[5], bg=theme.colors[5], fg='white').pack(fill='x')

        labelstyle = {'font':theme.fonts[7], 'bg':theme.colors[0], 'fg':'white'}

        self.form = tk.StringVar(value=f'Formato: dinheiro')
        tk.Label(self, textvariable=self.form, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.val_total = tk.StringVar(value=f'Total: R$ {self.mainapp.total:.2f}')
        tk.Label(self, textvariable=self.val_total, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.val_recebido = tk.StringVar(value='Valor recebido: R$ 0,00')
        tk.Label(self, textvariable=self.val_recebido, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.troco = tk.StringVar(value='Troco: R$ 0,00')
        tk.Label(self, textvariable=self.troco, **labelstyle).pack(padx=10, pady=5, anchor='w')

        buttons_frame = tk.Frame(self, bg=theme.colors[0])
        buttons_frame.pack()
        ttk.Button(buttons_frame, text='Confirmar (F2)', command=lambda key='confirm': self.end(key)).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Cancelar (Esc)', command=lambda key='cancel': self.end(key)).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Desconto', command=self.set_mod).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Calculadora').pack(side=tk.LEFT, padx=5, pady=5)
        self.bind('<KeyRelease>', self.payvalue)
        self.bind('<F2>', lambda event: self.end('confirm'))
        self.bind('<Escape>', lambda event: self.end('cancel'))
        self.bind('<F4>', self.set_mod)
    
    def end(self, key):
        try:
            if key == 'cancel' and messagebox.showwarning('Cancelar venda', 'Deseja iniciar nova venda?'):
                self.mainapp.cancel()
            elif key == 'confirm':
                self.mainapp.sales.update(
                    set_= {
                        'horario': date.today().strftime('%Y-%m-%d %H-%M-%S'),
                        'total': self.mainapp.total,
                        'pago': self.val_recebido.get().split(' ')[-1].replace(',', '.'),
                        'extra': self.extra,
                        'formato': self.form.get().split(' ')[-1]
                    },
                    where= f'id = {self.mainapp.ID}'
                )
                for id_produto, un in self.mainapp.purchase.select(
                        expr='id_produto, quantidade',
                        where=f'id_venda={self.mainapp.ID}'
                    ):
                    self.mainapp.storage.update(
                        set_= f'`quantidade` = `quantidade` - "{un}"',
                        where= f'id = {id_produto}'
                    )
                self.mainapp.restart_vars()
        except Exception as error: messagebox.showerror('Erro', error)
        else: 
            self.destroy()
            self.master.destroy()
    
    @update
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
                nform = ('dinheiro', 'cartão de crédito', 'cartão de débito')
                i = nform.index(self.form.get().split(': ')[-1].lower()) + {'Up':1, 'Down':-1}[key]
                if i > len(nform)-1: i = 0
                self.form.set(f'Formato: {nform[i]}')
        else: dec.append(value) # se for um numero adicione no final do texto
        finally:
            while len(dec) < 3: dec.insert(0, 0) # complete a lista com 0
            dec.insert(-2, ',') # adicione a vísgula para as casas decimais
            dec = ''.join(map(str, dec)) # juntar em texto
            val = float(dec.replace(',', '.')) # str para float
            self.val_recebido.set(f'Valor recebido: R$ {dec}') # mudar valor na interface
            self.troco.set(f'Troco: R$ {(val - self.mainapp.total):.2f}'.replace('.', ',')) # mostrar troco na interface
    
    @update # update atribuido ao objeto tk.Frame
    def set_mod(self, event=None):
        try:
            value = float(simpledialog.askstring('Desconto', 
                'Digite o valor em porcentagem (%) do desconto:', parent=self).replace(',', '.'))
        except ValueError: 
            messagebox.showwarning('Formato inválido', 'Formato inválido!\nDigite o valor corretamente!', parent=self)
            self.set_mod(event)
        else:
            self.extra = self.mainapp.total*(1 - value/100)
            self.mainapp.total -= self.extra
            self.val_total.set(f'Total: R$ {self.mainapp.total}'.replace('.', ','))
            self.troco.set(f'Troco: R$ *') # mostrar troco na interface

class CashierApp(ttk.Frame):
    @update
    def __init__(self, storage:Table, sales:Table, purchase:Table, master=None):
        super().__init__(master)
        self.pack()

        self.storage = storage
        self.sales = sales
        self.purchase = purchase

        self.ID = None # estado inicial do caixa

        # configurar janela
        self.master.title('Caixa')
        self.master.state('zoomed')
        self.master.config(background='white')

        # definir estilo da aplicação
        self.style = ttk.Style()
        self.style.theme_create('CashierTheme', parent='alt', settings=theme.settings_cashier)
        self.style.theme_use('CashierTheme')
        self.style.layout('Treeview', theme.treeview_layout)
        self.style.layout('Vertical.TScrollbar', theme.vertical_scrollbar_layout)
        self.style.layout('TCombobox', theme.combobox_layout)

        self.frames = {}
        self.vars = {}

        self.frames['info'] = tk.Frame(self, bg=theme.colors[0])
        self.frames['info'].pack(fill='x')
        self.frames['produtos'] = ttk.Frame(self)
        self.frames['produtos'].pack(fill='x')
        self.frames['control'] = ttk.Frame(self)
        self.frames['control'].pack(fill='x', pady=10)

        f = tk.Frame(self.frames['info'], bg=theme.colors[0])
        f.pack(fill='x')

        self.vars['total'] = tk.StringVar()
        tk.Label(f, textvariable=self.vars['total'],
            font=theme.fonts[4], **theme.labelinfo_style).pack(side=tk.LEFT, anchor='n')

        self.vars['venda info'] = tk.StringVar()
        tk.Label(f, textvariable=self.vars['venda info'],
            font=theme.fonts[5], **theme.labelinfo_style).pack(side=tk.RIGHT, anchor='n')

        self.vars['produto info'] = tk.StringVar()
        tk.Label(self.frames['info'], textvariable=self.vars['produto info'], 
            anchor='w', font=theme.fonts[6], **theme.labelinfo_style).pack(fill='x')

        columns = {
            'Código':150,
            'Nome do produto':300,
            'Un':100,
            'Preço unitário':200,
            'Preço total':200,
            'Extra':200
        }
        self.scrollbar = ttk.Scrollbar(self.frames['produtos'], orient='vertical')
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree = ttk.Treeview(self.frames['produtos'], columns=list(columns.keys()), height=16)
        self.tree.column('#0', width=80)
        self.tree.heading('#0', text='Item')
        for name, width in columns.items():
            self.tree.column(name, width=width, anchor='center')
            self.tree.heading(name, text=name)
        self.tree.bind('<Delete>', self.delete)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.tree.tag_configure(0, background=theme.colors[4])
        self.tree.tag_configure(1, background='white')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()

        ttk.Label(self.frames['control'], text='Código do produto:').pack(side=tk.LEFT)
        self.entry_codigo = tk.Entry(self.frames['control'], width=70, **theme.entry_style)
        self.entry_codigo.bind('<Return>', self.check_code)
        self.entry_codigo.focus_force()
        self.entry_codigo.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.frames['control'], text='Confirmar (F2)', command=self.confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frames['control'], text='Cancelar (Esc)', command=self.cancel).pack(side=tk.LEFT, padx=5)

        self.bind('<F2>', self.confirm)
        self.bind('<Escape>', self.cancel)
        self.restart_vars()
    
    @update
    def cancel(self, event=None):
        self.purchase.delete(where=f'id_venda={self.ID}')
        self.sales.delete(where=f'id={self.ID}')
        self.restart_vars()

    def confirm(self, event=None):
        toplevel = tk.Toplevel()
        toplevel.focus_force()
        ConfirmApp(toplevel, self)
        toplevel.mainloop()
    
    @update
    def check_code(self, event=None):
        value = self.entry_codigo.get()

        if self.ID == None:
            self.sales.insert_into()
            self.ID, = self.sales.get_last_id()[0]
            self.vars['venda info'].set(f'ID: {self.ID}')
        
        try: un, id_item = map(int, value.split('x')) if 'x' in value else [1, int(value)]
        except ValueError: messagebox.showerror('Formáto inválido.', 'Erro no formato do código.\nDigite corretamente.')
        else:
            try: nome, p_venda = self.storage.select(expr='nome, p_venda', where=f'id = {id_item}')[0]
            except Exception as error: messagebox.showerror('Erro ao procurar produto', error)
            else:
                self.purchase.insert_into(
                    id_venda= self.ID,
                    id_produto= id_item,
                    quantidade= un,
                    extra= 0
                )
                while len(str(id_item)) < 5: id_item = '0'+str(id_item)
                self.vars['produto info'].set(f'{id_item} {nome} {un} {p_venda:.2f}'.replace('.', ','))
        finally: 
            self.entry_codigo.delete(0, tk.END)
    
    @update
    def delete(self, event):
        item = self.tree.item(self.tree.focus())
        try: index = int(item['text'])
        except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
        else:
            if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][1])):
                self.cashier.drop(index)
    
    def restart_vars(self):
        self.ID = None
        self.total = 0
        self.vars['venda info'].set('')
        self.vars['total'].set('Total: R$ 0,00')
        self.vars['produto info'].set('')
    
    @exception
    def update(self):
        self.tree.delete(*self.tree.get_children(''))
        height = self.tree.cget('height')
        ncols = len(self.tree.cget('columns'))
        items = self.purchase.select(where=f'id_venda={self.ID}') if self.ID else []
        self.total = 0
        i = 0
        for i, (item, _, id_produto, quantidade, extra) in enumerate(items):
            nome, p_venda = self.storage.select(expr='nome, p_venda', where=f'id={id_produto}')[0]
            self.tree.insert('', 'end', text=item, values=[
                id_produto,
                nome,
                quantidade,
                f'R$ {p_venda:.2f}'.replace('.', ','), 
                f'R$ {p_venda*quantidade:.2f}'.replace('.', ',')
            ], tags=(i+2)%2)
            self.total += p_venda*quantidade + extra
        if self.total: self.vars['total'].set(f'Total: R$ {self.total:2f}'.replace('.', ','))
        while i < height:
            i += 1
            self.tree.insert('', 'end', values=['']*ncols, tags=(i+2)%2)