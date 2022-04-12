import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from database import Table
import theme
    
class ConfirmApp:
    def __init__(self, root, mainapp):
        self.root = root
        self.root.config(bg=theme.colors[0])
        self.mainapp = mainapp

        tk.Label(self.root, text='ID: *  Data: *', 
            font=theme.fonts[5], bg=theme.colors[5], fg='white').pack(fill='x')

        labelstyle = {'font':theme.fonts[7], 'bg':theme.colors[0], 'fg':'white'}

        self.form = tk.StringVar()
        self.form.set(f'Formato: dinheiro')
        tk.Label(self.root, textvariable=self.form, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.val_total = tk.StringVar()
        self.val_total.set(f'Total: R$ {self.sale.total:.2f}')
        tk.Label(self.root, textvariable=self.val_total, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.val_recebido = tk.StringVar()
        self.val_recebido.set('Valor recebido: R$ 0,00')
        tk.Label(self.root, textvariable=self.val_recebido, **labelstyle).pack(padx=10, pady=5, anchor='w')

        self.troco = tk.StringVar()
        self.troco.set('Troco: R$ 0,00')
        tk.Label(self.root, textvariable=self.troco, **labelstyle).pack(padx=10, pady=5, anchor='w')

        buttons_frame = tk.Frame(self.root, bg=theme.colors[0])
        buttons_frame.pack()
        ttk.Button(buttons_frame, text='Confirmar', command=lambda a=0: self.end('confirm')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Cancelar', command=lambda a=0: self.end('cancel')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Desconto', command=self.set_mod).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text='Calculadora').pack(side=tk.LEFT, padx=5, pady=5)
        self.root.bind('<KeyRelease>', self.payvalue)
        self.root.bind('<F2>', lambda event: self.end('confirm'))
        self.root.bind('<Escape>', lambda event: self.end('cancel'))
        self.root.bind('<F4>', self.set_mod)
    
    def end(self, key):
        if key == 'cancel' and messagebox.showwarning('Cancelar venda', 'Deseja iniciar nova venda?'):
            pass
        elif key == 'confirm':
            pass
        self.mainapp.vars['arquivo info'].set('ID: *  Data: *')
        self.mainapp.vars['produto info'].set('')
        self.mainapp.update()
    
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
            self.troco.set('Troco: R$ *') # mostrar troco na interface
    
    def set_mod(self, event=None):
        try:
            value = float(simpledialog.askstring('Desconto', 
                'Digite o valor em porcentagem (%) do desconto:', parent=self.root).replace(',', '.'))
        except ValueError: 
            messagebox.showwarning('Formato inválido', 'Formato inválido!\nDigite o valor corretamente!', parent=self.root)
            self.set_mod(event)
        else:
            self.val_total.set('Total: R$ *')
            self.troco.set('Troco: R$ *') # mostrar troco na interface
            self.root.update()

class CashierApp(ttk.Frame):
    def __init__(self, storage:Table, sales:Table, purchase:Table, master=None):
        super().__init__(master)
        self.pack()

        self.storage = storage
        self.sales = sales
        self.purchase = purchase

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

        self.frames['info'] = tk.Frame(self, bg=theme.colors[3])
        self.frames['info'].pack(fill='x', padx=20, pady=[5, 10])

        self.frames['info 1'] = tk.Frame(self.frames['info'], bg=theme.colors[3])
        self.frames['info 1'].pack(fill='y', side=tk.LEFT)

        self.vars['total'] = tk.StringVar()
        self.vars['total'].set('Total: 0,00 R$')
        tk.Label(self.frames['info 1'], textvariable=self.vars['total'], anchor='w',
            font=theme.fonts[4], **theme.labelinfo_style).pack(fill='x', padx=10, pady=[10,5])

        self.vars['produto info'] = tk.StringVar()
        tk.Label(self.frames['info 1'], textvariable=self.vars['produto info'], anchor='w',
            font=theme.fonts[6], **theme.labelinfo_style).pack(fill='x', padx=10, pady=[5,10])

        self.vars['arquivo info'] = tk.StringVar()
        self.vars['arquivo info'].set(f'ID: *  Data: *')
        tk.Label(self.frames['info'], textvariable=self.vars['arquivo info'],
            font=theme.fonts[5], **theme.labelinfo_style).pack(anchor='ne', padx=5, pady=5)

        self.frames['produtos'] = ttk.Frame(self)
        self.frames['produtos'].pack()

        columns = {
            'Código':170,
            'Unidades':100,
            'Nome do produto':400,
            'Preço unitário':250,
            'Preço total':250
        }

        self.scrollbar = ttk.Scrollbar(self.frames['produtos'], orient='vertical')
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree = ttk.Treeview(self.frames['produtos'], columns=list(columns.keys()), height=17)
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

        self.frames['control'] = ttk.Frame(self)
        self.frames['control'].pack(fill='x', padx=20, pady=10)

        ttk.Label(self.frames['control'], text='Código do produto:').pack(side=tk.LEFT)
        self.entry_codigo = tk.Entry(self.frames['control'], width=70, **theme.entry_style)
        self.entry_codigo.bind('<Return>', self.verify_code)
        self.entry_codigo.focus_force()
        self.entry_codigo.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frames['control'], text='Confirmar', command=self.confirm).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.frames['control'], text='Cancelar', command=self.cancel).pack(side=tk.RIGHT, padx=5)

        self.bind('<F2>', self.confirm)
        self.bind('<Escape>', self.cancel)

        self.update()
    
    def cancel(self, event=None):
        # self.sale.new()
        self.update()

    def confirm(self, event=None):
        toplevel = tk.Toplevel()
        toplevel.focus_force()
        ConfirmApp(toplevel, self)

    def delete(self, event):
        item = self.tree.item(self.tree.focus())
        try: index = int(item['text'])
        except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
        else:
            if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][1])):
                pass
        finally: self.update()
    
    def update(self):
        self.tree.delete(*self.tree.get_children())
        cont = 17
        for i, item in enumerate(self.sale.items):
            codigo, unidades, nome, p_venda, total = item
            while len(str(codigo)) < 5: codigo = '0' + str(codigo)
            self.tree.insert('', 'end', text=i, values=[codigo, unidades, nome, 
                f'R$ {p_venda:.2f}'.replace('.', ','), f'R$ {total:.2f}'.replace('.', ',')], tags=not (cont)%2)
            cont -= 1
        while cont >= 0:
            self.tree.insert('', 'end', text='', values=['']*5, tags=not (cont)%2)
            cont -= 1
        self.vars['total'].set(f'Total: R$ {self.sale.total:.2f}'.replace('.', ','))
        self.entry_codigo.focus()
        
    
    def verify_code(self, event):
        value = self.entry_codigo.get()
        try: un, value = map(int, value.split('x')) if 'x' in value else [1, int(value)]
        except ValueError: messagebox.showwarning('Formáto inválido.', 'Erro no formato do código.\nDigite corretamente.')
        else:
            try: nome, p_venda = data.storage.get_value(value, 'nome', 'p_venda')
            except Exception as error: messagebox.showwarning('Erro no código.', error)
            else: 
                self.sale.add(value, un, nome, p_venda)
                while len(str(value)) < 5: value = '0'+str(value)
                self.vars['produto info'].set(f'{value};  {un};  {nome};  R$ {p_venda:.2f};  R$ {(p_venda*un):.2f}'.replace('.', ','))
        finally: self.entry_codigo.delete(0, tk.END); self.update()