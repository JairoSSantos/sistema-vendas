from apps.widgets import *
from apps.database import Table
from apps.theme import COLORS
#from tkinter import ttk
from tkinter import messagebox
#from tkinter import simpledialog
import traceback

def br_currency(value:float):
    return f'R$ {value:.2f}'.replace('.', ',')

# table_info = (tag, heading, col_width, formatting)
TABLE_INFO = {
    'estoque':(
        ('id', 'Código', 100, int),
        ('nome', 'Nome do Produto', 250, str),
        ('p_venda', 'Preço de Venda', 150, br_currency),
        ('p_custo', 'Preço de Custo', 150, br_currency),
        ('quantidade', 'Quantidade', 120, int)
    ),
}

class StorageController(ttk.Frame):
    def __init__(self, storage:Table, master):
        ttk.Frame.__init__(self, master)

        self.storage = storage

        self.frames = {}
        self.vars = {} # variáveis
        self.entrys = {} # entradas
        self.formatting = {} # formatação dos dados que serão inseridos nas tabelas

        # definir frames da aba estoque
        #self.frames['form'] = ttk.LabelFrame(self, text='Produto')
        #self.frames['form'].grid(row=0, column=0, pady=5, padx=5, sticky='nsew')
        self.frames['dados'] = ttk.Frame(self)
        self.frames['dados'].grid(row=0, column=1, pady=5, padx=5, rowspan=2)
        self.frames['detalhes'] = ttk.LabelFrame(self, text='Detalhes')
        self.frames['detalhes'].grid(row=1, column=0, pady=5, padx=5, sticky='nsew')
        self.frames['pesquisar'] = ttk.Frame(self.frames['dados'])
        self.frames['pesquisar'].pack()
        self.frames['tree'] = ttk.Frame(self.frames['dados'])
        self.frames['tree'].pack(fill='x')
        self.frames['relatório'] = ttk.Frame(self.frames['dados'])
        self.frames['relatório'].pack(fill='x', pady=10)

        self.form = Form(self, text='Produto')
        self.form.grid(row=0, column=0, pady=5, padx=5, sticky='nsew')
        for i, (col, text, _, _) in enumerate(TABLE_INFO['estoque']):
            ttk.Label(self.form, text= text + ':', width=15, anchor='e').grid(row=i, column=0, pady=2, sticky='w', padx=(0, 2))
            self.form[col] = (MoneyEntry if 'p_' in col else StylisedEntry)(self.form, validate='key')
            self.form[col].grid(row=i, column=1, padx=[0, 10], sticky='ew')
        self.form['id']['validatecommand'] = self.form['quantidade']['validatecommand'] = (self.form.register(lambda char: char.isnumeric()), '%S')
        self.form['quantidade'].bind('<Double-Button-1>', self.update)

        # descrição
        ttk.Label(self.form, text='Descrição:', width=15, anchor='e').grid(row=5, column=0, sticky='nw', padx=[0, 2])
        entry = StylisedText(self.form, width=10, height=5)
        entry.grid(row=5, column=1, padx=[0, 10], sticky='ew', pady=2)
        self.form['descricao'] = entry

        # butões da aba estoque
        for i, (name, command) in enumerate([('registrar', self.register), ('excluir', self.delete)]):
            key = f'button-{name}'
            self.vars[key] = tk.StringVar(value=name[0].upper() + name[1:])
            ttk.Button(self.form, textvariable=self.vars[key], command=command).grid(row=6, column=i, pady=10)

        #definir widgets para visualizar detalhes do produto
        self.vars['detalhes'] = tk.StringVar()
        self.vars['detalhes'].set('\n'*15)
        ttk.Label(self.frames['detalhes'], width=35, #height=12, 
            textvariable=self.vars['detalhes'], justify=tk.LEFT, anchor='w').pack()

        # definir widgets para pesquisar produto
        ttk.Label(self.frames['pesquisar'], text='Pesquisar:').grid(row=0, column=0, padx=[0, 2])
        self.find_entry = StylisedEntry(self.frames['pesquisar'], width=70)
        self.find_entry.bind('<KeyPress>', self.find)
        self.find_entry.grid(row=0, column=1)

        # definir treeview do estowue
        self.tree = Treeview(
            master=self.frames['tree'], 
            table_info=TABLE_INFO['estoque'],
            bindings=(('<Double-1>', self.update),
                      ('<<TreeviewSelect>>', self.update)),
            height=29
        )
        self.tree.pack(side=tk.LEFT)

        # definir widgets do relatório
        self.vars['n-cadastros'] = tk.StringVar()
        ttk.Label(self.frames['relatório'], 
            text='Produtos cadastrados:', width=30, anchor='w', textvariable=self.vars['n-cadastros']).pack(side=tk.LEFT)
        ttk.Button(self.frames['relatório'], text='Relatório').pack(side=tk.RIGHT)
        
        #self.bind_class('Entry', '<Return>', self.update)
        self.form.clear()
        self.tree.update_items(self.storage.select(order=self.tree.orderby.get()))
    
    def delete(self) -> None:
        '''
        Deletar/Modificar produto que esteja selecionado.
        '''
        match self.vars['button-excluir'].get():
            case 'Excluir':
                try: 
                    item = self.tree.get_focus()
                    id_item = int(item['values'][0])
                except ValueError: 
                    messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
                else: 
                    if messagebox.askokcancel('Excluir produto', 'Deseja excluir {} - {}?'.format(*item['values'][:2])):
                        self.storage.delete(where=f'id={id_item}')
                self.tree.update_items(self.storage.select(order=self.tree.orderby.get()))

            case 'Cancelar':
                self.vars['button-registrar'].set('Registrar')
                self.vars['button-excluir'].set('Excluir')
                self.vars['produto-selecionado'] = None
                self.tree.update_items(self.storage.select(order=self.tree.orderby.get()))
                self.form.clear()
    
    def find(self):
        '''
        Pesquisar nos dados o valor da entrada.
        '''
        try:
            like = '"%{}%"'.format(self.find_entry.get())
            self.tree.update(self.storage.select(
                where= '({})'.format(' or '.join([f'{col[0]} like {like}' for col in self.storage.get_columns()])),
                **({'order by': self.vars['ordem']} if self.vars['ordem'] else {})
            ))
        except Exception as error:
            messagebox.showerror(f'Erro: {error}', traceback.format_exc())
    
    def register(self):
        '''
        Registrar/modificar produto.
        '''
        key = self.vars['button-registrar'].get()
        try:
            kwargs = self.form.get()
            print(kwargs)
            match key:
                case 'Registrar':
                    self.storage.insert_into(**kwargs)
        
                case 'Modificar':
                    self.storage.update(set_=kwargs, where='id = {}'.format(self.vars['produto-selecionado']))
                    self.vars['button-registrar'].set('Registrar')
                    self.vars['button-excluir'].set('Excluir')
                    self.vars['produto-selecionado'] = None
        except Exception as error:
            messagebox.showerror(f'Erro ao {key.lower()} produto!', error)
        else:
            self.form.clear()
            self.tree.update_items(self.storage.select(order=self.tree.orderby.get()))
    
    def update(self, event:tk.Event=None):
        '''
        Atualizar aplicação.
        '''
        match event.widget:
            case self.tree:
                try: 
                    id_item = int(self.tree.get_focus()['values'][0])
                except: pass
                else:
                    codigo, nome, p_venda, p_custo, quant, desc = self.storage.select(where=f'id = {id_item}')[0]
                    codigo, desc = str(codigo), str(desc)
                    while len(str(codigo)) < 5: codigo = '0' + codigo
                    fal_rows = 10 - len(desc.split('\n'))
                    text = '\n'.join([
                        f'Código: {codigo}',
                        f'Nome: {nome}',
                        f'Preço de venda: R$ {br_currency(p_venda)}',
                        f'Preço de custo: R$ {br_currency(p_custo)}',
                        f'Quantidade: {quant}',
                        f'Descrição: {desc}',
                        '\n'*fal_rows,
                    ])
                    self.vars['detalhes'].set(text)

                    self.vars['produto-selecionado'] = id_item
                    item = self.storage.select(where=f'id={id_item}')[0]
                    for i, (entry, val) in enumerate(zip(self.entrys.values(), item)): 
                        try: f = TABLE_INFO['estoque'][i][3] # tente obter a formatação
                        except IndexError: entry.set(val) # se não houver, apenas selecione o valor
                        else: entry.set(f(val)) # se houver, aplique a formatação
                    self.vars['button-registrar'].set('Modificar')
                    self.vars['button-excluir'].set('Cancelar')

'''
class SalesController(tk.Frame):
    def __init__(self, sales:Table, purchase:Table, master:tk.Frame=None) -> None:
        tk.Frame.__init__(master)
        self.pack()

        self.sales = sales
        self.purchase = purchase

        self.frames = {} # frames
        self.vars = {} # variáveis
        self.entrys = {} # entradas
        self.combos = {}

        # definir frames de vendas
        self.frames['dados'] = ttk.Frame(self)
        self.frames['dados'].pack(fill='x', padx=10)
        self.frames['tree'] = ttk.Frame(self)
        self.frames['tree'].pack(fill='x', padx=10)
        self.frames['rodape'] = ttk.Frame(self)
        self.frames['rodape'].pack(fill='x', padx=10)

        # definir widgets para selecionar arquivo de vendas
        ttk.Label(self.frames['dados'], text='Data:').pack(side=tk.LEFT)
        self.combos['dia'] = ttk.Combobox(self.frames['dados'], values=['Todos'], width=5, state='readonly', justify='center')
        self.combos['dia'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_dia'))
        self.combos['dia'].pack(side=tk.LEFT)
        ttk.Label(self.frames['dados'], text='/').pack(side=tk.LEFT)
        self.combos['mes'] = ttk.Combobox(self.frames['dados'], values=['Todos'], width=5, state='readonly', justify='center')
        self.combos['mes'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_mes'))
        self.combos['mes'].pack(side=tk.LEFT)
        ttk.Label(self.frames['dados'], text='/').pack(side=tk.LEFT)
        self.combos['ano'] = ttk.Combobox(self.frames['dados'], values=['Todos'], width=7, state='readonly', justify='center')
        self.combos['ano'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_ano'))
        self.combos['ano'].pack(side=tk.LEFT)

        ttk.Separator(self.frames['dados'], orient='vertical').pack(side=tk.LEFT, padx=10, fill='y', pady=5)

        # definir widgets para pesquisar vendas
        ttk.Label(self.frames['dados'], text='Pesquisar:').pack(side=tk.LEFT, padx=[0, 2])
        self.find_entry = tk.Entry(self.frames['dados'], width=70, **theme.entry_style)
        self.find_entry.bind('<KeyPress>', lambda event: self.find('vendas'))
        self.find_entry.pack(side=tk.LEFT, padx=[10])

        # definir treeview das vendas
        columns = [
            ('Id', 50), ('Horário', 80),
            ('Total', 150), ('Valor pago', 150),
            ('Troco', 150), ('Extra', 200),
            ('Formato de pagamento', 200)
        ]
        self.scrollbar_vendas = ttk.Scrollbar(self.frames['tree'], orient='vertical')
        self.tree = ttk.Treeview(self.frames['tree'], columns=list(map(lambda a: a[0], columns)), height=30)
        self.tree.column('#0', width=0)
        for i, (key, width) in enumerate(columns):
            self.tree.column(key, width=width, anchor='center')
            self.tree.heading(key, text=key)
        self.tree.tag_configure(0, background=theme.colors[4])
        self.tree.tag_configure(1, background='white')
        self.tree.configure(yscroll=self.scrollbar_vendas.set)
        self.scrollbar_vendas.config(command=self.tree.yview)
        self.tree.pack(side=tk.LEFT, fill='x')
        self.scrollbar_vendas.pack(side=tk.LEFT, fill='y')
        self.formatting = lambda id_item, horario, total, pago, extra, formato:(
            id_item,
            horario, 
            f'R$ {total:.2f}'.replace('.', ','), 
            f'R$ {pago:.2f}'.replace('.', ','), 
            f'R$ {(pago-total):.2f}'.replace('.', ','),
            extra,
            formato
        )

        # definir widgets do relatório de vendas
        ttk.Button(self.frames['dados'], text='Relatório').pack(side=tk.LEFT)
    
    def tree_update(self, items):
        self.tree.delete(*self.tree.get_children())
        height = self.tree.cget('height') - 1
        ncols = len(self.tree.cget('columns'))
        i = 0
        for i, item in enumerate(items): 
            self.tree.insert('', 'end', values=self.formatting(*item[:ncols]), tags=int((i+2)%2 == 0))
        while i < height:
            i += 1
            self.tree.insert('', 'end', values=['']*ncols, tags=int((i+2)%2 == 0))
    
    def update(self, key:str, event:tk.Event=None) -> None:
        match key:
            case 'vendas':
                self.tree_update('vendas', self.sales.select())
'''