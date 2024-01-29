import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import date
from database import Table
import theme
import traceback

ARROW_UP = u'\u21EA'

class ControlApp(tk.Frame):
    def __init__(self, storage:Table, sales:Table, purchase:Table, master:tk.Frame=None) -> None:
        # configurando janela principal
        super().__init__(master)
        self.pack()
        self.master.title('Controle de dados')
        self.master.state('zoomed')

        self.storage = storage
        self.storage_columns = tuple(map(lambda item: item[0], self.storage.get_columns()))
        self.storage_tags = ('Código', 'Nome do produto', 'Preço de venda', 'Preço de custo', 'Quantidade')
        self.sales = sales
        self.purchase = purchase

        # definir estilo da aplicação
        self.style = ttk.Style()
        self.style.theme_use('MyTheme')
        self.style.layout('Treeview', theme.treeview_layout)
        self.style.layout('Vertical.TScrollbar', theme.vertical_scrollbar_layout)
        self.style.layout('TCombobox', theme.combobox_layout)

        # definir frame principal
        self.notebook_main = ttk.Notebook(self)

        self.frames = {} # frames
        self.vars = {'ordem':{'estoque':None, 'vendas':None}} # variáveis
        self.entrys = {'estoque':{}, 'vendas':{}} # entradas
        self.trees = {}
        self.combos = {}
        self.formatting = {} # formatação dos dados que serão inseridos nas tabelas

        # definir frames da aba estoque
        self.frames['estoque'] = {'main': ttk.Frame(self.notebook_main)}
        self.frames['estoque']['main'].pack(anchor='w', pady=5, padx=5)
        self.frames['estoque']['produto'] = ttk.LabelFrame(self.frames['estoque']['main'], text='Produto')
        self.frames['estoque']['produto'].grid(row=0, column=0, pady=5, padx=5, sticky='nsew')
        self.frames['estoque']['dados'] = ttk.Frame(self.frames['estoque']['main'])
        self.frames['estoque']['dados'].grid(row=0, column=1, pady=5, padx=5, rowspan=2)
        self.frames['estoque']['detalhes'] = ttk.LabelFrame(self.frames['estoque']['main'], text='Detalhes')
        self.frames['estoque']['detalhes'].grid(row=1, column=0, pady=5, padx=5, sticky='nsew')
        self.frames['estoque']['pesquisar'] = ttk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['pesquisar'].pack()
        self.frames['estoque']['tree'] = ttk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['tree'].pack(fill='x')
        self.frames['estoque']['relatório'] = ttk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['relatório'].pack(fill='x', pady=10)

        # widgets para entrada de dados do estoque
        labels_width = 15
        for i, (col, text) in enumerate(zip(self.storage_columns[:6], self.storage_tags)):
            ttk.Label(self.frames['estoque']['produto'], text= text + ':', 
                width=labels_width, anchor='e').grid(row=i, column=0, pady=2, sticky='w', padx=(0, 2))
            self.entrys['estoque'][col] = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
            self.entrys['estoque'][col].grid(row=i, column=1, padx=[0, 10], sticky='ew')
        self.entrys['estoque']['p_venda'].insert(0, 'R$ 0,00')
        self.entrys['estoque']['p_custo'].insert(0, 'R$ 0,00')
        self.entrys['estoque']['p_venda'].bind('<KeyPress>', lambda event: self.update('p_venda', event))
        self.entrys['estoque']['p_custo'].bind('<KeyPress>', lambda event: self.update('p_custo', event))
        self.entrys['estoque']['quantidade'].bind('<KeyPress>', lambda event: self.update('quantidade', event))
        self.entrys['estoque']['quantidade'].bind('<Double-Button-1>', lambda event: self.update('quantidade', event))

        # descrição
        ttk.Label(
            self.frames['estoque']['produto'], 
            text='Descrição:', 
            width=labels_width, 
            anchor='e'
        ).grid(row=5, column=0, sticky='nw', padx=[0, 2])
        entry = tk.Text(self.frames['estoque']['produto'], width=10, height=5, **theme.entry_style)
        entry.grid(row=5, column=1, padx=[0, 10], sticky='ew', pady=2)
        self.entrys['estoque']['descricao'] = entry

        # butões da aba estoque
        for i, (item, command) in enumerate([('cadastrar', self.register), ('excluir', self.delete)]):
            key = f'button {item}'
            self.vars[key] = tk.StringVar(value=item[0].upper() + item[1:])
            ttk.Button(self.frames['estoque']['produto'],
                textvariable=self.vars[key], command=command).grid(row=6, column=i, pady=10)

        #definir widgets para visualizar detalhes do produto
        self.vars['detalhes'] = tk.StringVar()
        self.vars['detalhes'].set('\n'*16)
        ttk.Label(self.frames['estoque']['detalhes'], width=35, #height=12, 
            textvariable=self.vars['detalhes'], justify=tk.LEFT, anchor='w').pack()

        # definir widgets para pesquisar produto
        ttk.Label(self.frames['estoque']['pesquisar'], text='Pesquisar:').grid(row=0, column=0, padx=[0, 2])
        self.entrys['estoque']['pesquisar'] = tk.Entry(self.frames['estoque']['pesquisar'], width=70, **theme.entry_style)
        self.entrys['estoque']['pesquisar'].bind('<KeyPress>', lambda event: self.find('estoque'))
        self.entrys['estoque']['pesquisar'].grid(row=0, column=1)

        # definir treeview do estowue
        widths = (100, 250, 150, 150, 120)
        self.trees['estoque'] = ttk.Treeview(self.frames['estoque']['tree'], columns=self.storage_columns[:5], height=29)
        self.trees['estoque'].column('#0', width=0)
        for i, width in enumerate(widths):
            self.trees['estoque'].column(self.storage_columns[i], width=width, anchor='center')
            self.trees['estoque'].heading(self.storage_columns[i], text=self.storage_tags[i])
        self.trees['estoque'].bind('<Double-1>', lambda event: self.update('duplo_click', event))
        self.trees['estoque'].bind('<<TreeviewSelect>>', lambda event: self.update('mostrar_detalhes', event))
        self.trees['estoque'].tag_configure(1, background=theme.colors[4])
        self.trees['estoque'].tag_configure(0, background='white')
        self.scrollbar_estoque = ttk.Scrollbar(self.frames['estoque']['tree'], orient='vertical')
        self.trees['estoque'].configure(yscroll=self.scrollbar_estoque.set)
        self.trees['estoque'].pack(side=tk.LEFT)
        self.scrollbar_estoque.pack(side=tk.RIGHT, fill='y')
        self.scrollbar_estoque.config(command=self.trees['estoque'].yview)
        self.formatting['estoque'] = lambda codigo, nome, p_venda, p_custo, quant: [
            '0'*(5 - len(str(codigo))) + str(codigo) if len(str(codigo)) < 5 else str(codigo), 
            nome, 
            f'R$ {p_venda:.2f}'.replace('.', ','), 
            f'R$ {p_custo:.2f}'.replace('.', ','), 
            f'{quant}'
        ]

        # definir widgets do relatório
        self.vars['n cadastros'] = tk.StringVar()
        ttk.Label(self.frames['estoque']['relatório'], 
            text='Produtos cadastrados:', width=30, anchor='w', textvariable=self.vars['n cadastros']).pack(side=tk.LEFT)
        ttk.Button(self.frames['estoque']['relatório'], text='Relatório').pack(side=tk.RIGHT)

        # ===============================================================================================================================

        # definir frames de vendas
        self.frames['vendas'] = {'main': ttk.Frame(self.notebook_main)}
        self.frames['vendas']['main'].pack()
        self.frames['vendas']['dados'] = ttk.Frame(self.frames['vendas']['main'])
        self.frames['vendas']['dados'].pack(fill='x', padx=10)
        self.frames['vendas']['tree'] = ttk.Frame(self.frames['vendas']['main'])
        self.frames['vendas']['tree'].pack(fill='x', padx=10)
        self.frames['vendas']['rodape'] = ttk.Frame(self.frames['vendas']['main'])
        self.frames['vendas']['rodape'].pack(fill='x', padx=10)

        # definir widgets para selecionar arquivo de vendas
        ttk.Label(self.frames['vendas']['dados'], text='Data:').pack(side=tk.LEFT)
        self.combos['dia'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=5, state='readonly', justify='center')
        self.combos['dia'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_dia'))
        self.combos['dia'].pack(side=tk.LEFT)
        ttk.Label(self.frames['vendas']['dados'], text='/').pack(side=tk.LEFT)
        self.combos['mes'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=5, state='readonly', justify='center')
        self.combos['mes'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_mes'))
        self.combos['mes'].pack(side=tk.LEFT)
        ttk.Label(self.frames['vendas']['dados'], text='/').pack(side=tk.LEFT)
        self.combos['ano'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=7, state='readonly', justify='center')
        self.combos['ano'].bind('<<ComboboxSelected>>', lambda event: self.update('vendas_combo_ano'))
        self.combos['ano'].pack(side=tk.LEFT)

        ttk.Separator(self.frames['vendas']['dados'], orient='vertical').pack(side=tk.LEFT, padx=10, fill='y', pady=5)

        # definir widgets para pesquisar vendas
        ttk.Label(self.frames['vendas']['dados'], text='Pesquisar:').pack(side=tk.LEFT, padx=[0, 2])
        self.entrys['vendas']['pesquisar'] = tk.Entry(self.frames['vendas']['dados'], width=70, **theme.entry_style)
        self.entrys['vendas']['pesquisar'].bind('<KeyPress>', lambda event: self.find('vendas'))
        self.entrys['vendas']['pesquisar'].pack(side=tk.LEFT, padx=[10])

        # definir treeview das vendas
        columns = [
            ('Id', 50),
            ('Horário', 80),
            ('Total', 150),
            ('Valor pago', 150),
            ('Troco', 150),
            ('Extra', 200),
            ('Formato de pagamento', 200)
        ]
        self.scrollbar_vendas = ttk.Scrollbar(self.frames['vendas']['tree'], orient='vertical')
        self.trees['vendas'] = ttk.Treeview(self.frames['vendas']['tree'], columns=list(map(lambda a: a[0], columns)), height=30)
        self.trees['vendas'].column('#0', width=0)
        for i, (key, width) in enumerate(columns):
            self.trees['vendas'].column(key, width=width, anchor='center')
            self.trees['vendas'].heading(key, text=key)
        self.trees['vendas'].tag_configure(0, background=theme.colors[4])
        self.trees['vendas'].tag_configure(1, background='white')
        self.trees['vendas'].configure(yscroll=self.scrollbar_vendas.set)
        self.scrollbar_vendas.config(command=self.trees['vendas'].yview)
        self.trees['vendas'].pack(side=tk.LEFT, fill='x')
        self.scrollbar_vendas.pack(side=tk.LEFT, fill='y')
        self.formatting['vendas'] = lambda id_item, horario, total, pago, extra, formato:[
            id_item,
            horario, 
            f'R$ {total:.2f}'.replace('.', ','), 
            f'R$ {pago:.2f}'.replace('.', ','), 
            f'R$ {(pago-total):.2f}'.replace('.', ','),
            extra,
            formato
        ]

        # definir widgets do relatório de vendas
        ttk.Button(self.frames['vendas']['dados'], text='Relatório').pack(side=tk.LEFT)

        # adicionar abas no notebook
        self.notebook_main.add(self.frames['estoque']['main'], text='Estoque')
        self.notebook_main.add(self.frames['vendas']['main'], text='Vendas')
        self.notebook_main.grid(row=0, column=0)

        self.bind_class('Entry', '<Return>', lambda event: self.update('pular_entrada', event))

        # atializar as abas
        self.update('estoque')
        self.update('vendas')
    
    def delete(self):
        '''
        Deletar item que esteja selecionado no treeview dos produtos.
        '''
        if self.vars['button excluir'].get() == 'Excluir':
            try: 
                item = self.trees['estoque'].item(self.trees['estoque'].focus())
                id_item = int(item['values'][0])
            except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
            else: 
                if messagebox.askokcancel('Excluir produto', 'Deseja excluir {} - {}?'.format(*item['values'][:2])):
                    self.storage.delete(where=f'id={id_item}')
        
        elif self.vars['button excluir'].get() == 'Cancelar':
            for item in self.entrys['estoque'].values(): 
                try: item.delete(0, tk.END)
                except: item.delete('0.0', tk.END)
            self.vars['button cadastrar'].set('Cadastrar')
            self.vars['button excluir'].set('Excluir')
            self.vars['produto selecionado'] = None
            self.update('estoque')

        self.update('estoque')
    
    def find(self, key):
        '''
        Pesquisar nos dados o valor da entrada.

        Args:
            key: chave referente aos dados que serão utilizados
                |-> 'estoque': dados do estoque
                |-> 'vendas': dados das vendas
        '''
        try:
            table = self.storage if key == 'estoque' else self.sales
            like = '"%{}%"'.format(self.entrys[key]['pesquisar'].get())
            self.tree_update(key, table.select(
                where= '(' + ' or '.join([f'{col[0]} like {like}' for col in table.get_columns()]) + ')',
                **({'order by': self.vars['ordem'][key]} if self.vars['ordem'][key] else {})
            ))
        except Exception as error: 
            messagebox.showerror(f'Erro: {error}', traceback.format_exc())
    
    def register(self):
        '''
        Registrar/modificar produto.
        '''
        key = self.vars['button cadastrar'].get()
        try:
            id_item = int(self.entrys['estoque']['id'].get())
            nome = str(self.entrys['estoque']['nome'].get())
            p_venda = float(self.entrys['estoque']['p_venda'].get().lstrip('R$').replace(',', '.'))
            p_custo = float(self.entrys['estoque']['p_custo'].get().lstrip('R$').replace(',', '.'))
            quantidade = self.entrys['estoque']['quantidade'].get()
            descricao = str(self.entrys['estoque']['descricao'].get('0.0', tk.END))
            quantidade = 0 if quantidade == '' else int(quantidade)
        except ValueError: 
            messagebox.showerror(f'Erro ao {key.lower()} produto!', 'Preencha os campos corretamente.')
        else:
            today = date.today().strftime('%Y-%m-%d')
            kwargs = {
                'id':id_item, 
                'nome':nome, 
                'p_venda':p_venda, 
                'p_custo':p_custo, 
                'quantidade':quantidade, 
                'descricao':descricao,
                'data_mod':today
            }
            try:
                match key:
                    case 'Cadastrar':
                        self.storage.insert_into(data_cad=today, **kwargs)
                        for item in self.entrys['estoque'].values():
                            try: item.delete(0, tk.END)
                            except: 
                                try: item.delete('1.0', tk.END)
                                except: pass
                        self.entrys['estoque']['p_venda'].insert(0, 'R$ 0,00')
                        self.entrys['estoque']['p_custo'].insert(0, 'R$ 0,00')
            
                    case 'Modificar':
                        self.storage.update(set_=kwargs, where='id = {}'.format(self.vars['produto selecionado']))
                        for item in self.entrys['estoque'].values(): 
                            try: item.delete(0, tk.END)
                            except: item.delete('0.0', tk.END)
                        self.vars['button cadastrar'].set('Cadastrar')
                        self.vars['button excluir'].set('Excluir')
                        self.vars['produto selecionado'] = None
            except Exception as error:
                messagebox.showerror(f'Erro ao {key.lower()} produto!', error)
            
            self.update('estoque')
    
    def tree_update(self, key, items):
        '''
        Atualizar treeview.
        
        Args:
            key: chave referente ao treeview que será atualizado
                |-> 'estoque': dados do estoque
                |-> 'vendas': dados das vendas
            items: lista dos items que serão expostos no treeview, list[dict{}, dict{}, ...]
        '''
        self.trees[key].delete(*self.trees[key].get_children())
        height = self.trees[key].cget('height') - 1
        ncols = len(self.trees[key].cget('columns'))
        i = 0
        for i, item in enumerate(items): 
            self.trees[key].insert('', 'end', values=self.formatting[key](*item[:ncols]), tags=int((i+2)%2 == 0))
        while i < height:
            i += 1
            self.trees[key].insert('', 'end', values=['']*ncols, tags=int((i+2)%2 == 0))
    
    def update(self, key:str, event:tk.Event=None) -> None:
        '''
        Atualizar aplicação.

        Args:
            key: chave referente à parte da aplicação que será atualizado.
                |-> 'estoque': atualizar toda a aba de estoque
                |-> 'pular_entrada': mudar de entrada ao preencher campo de registro
                |-> 'p_venda' ou 'p_custo': verificar entrada dos preços
                |-> 'duplo_click': modificar produto ou ordenar tabela
                |-> 'mostrar_detalhes': mostrar detalhes do produto
                |-> 'vendas': atualizar toda a aba de vendas
        '''
        match key:
            case 'estoque': 
                items = self.storage.select()
                next_id = str(self.storage.get_next_id()[0][0])
                self.tree_update(key, items)
                self.vars['n cadastros'].set(f'Produtos cadastrados: {len(items)}')
                self.entrys['estoque']['id'].delete(0, tk.END)
                self.entrys['estoque']['id'].insert(0, '0'*(5 - len(next_id)) + next_id)
                self.entrys['estoque']['p_venda'].delete(0, tk.END)
                self.entrys['estoque']['p_venda'].insert(0, 'R$ 0,00')
                self.entrys['estoque']['p_custo'].delete(0, tk.END)
                self.entrys['estoque']['p_custo'].insert(0, 'R$ 0,00')

            case 'pular_entrada':
                self.entrys['estoque'][
                    list(self.entrys['estoque'].keys())[
                        list(self.entrys['estoque'].values()).index(event.widget) + 1
                    ]
                ].focus()

            case 'p_venda'|'p_custo':
                val = [char for char in self.entrys['estoque'][key].get().lstrip('R$ 0') if char.isnumeric()]
                val = ['0']*(3 - len(val)) + val
                val.insert(-2, ',')
                self.entrys['estoque'][key].update()
                self.entrys['estoque'][key].delete(0, tk.END)
                self.entrys['estoque'][key].insert(0, 'R$ ' + ''.join(val))

            case 'duplo_click':
                match self.trees['estoque'].identify('region', event.x, event.y):
                    case 'heading': 
                        i = int(self.trees['estoque'].identify('column', event.x, event.y).split('#')[-1])
                        col = self.storage.get_columns()[i][0]
                        order = self.vars['ordem']['estoque']
                        if col in order:
                            self.vars['ordem']['estoque'] = '{} {}'.format(col, str(-int(order.split(' ')[-1])))
                        else:
                            self.vars['ordem']['estoque'] = f'{col} 1'

                    case 'cell': 
                        try: id_item = int(self.trees['estoque'].item(self.trees['estoque'].focus())['values'][0])
                        except ValueError: pass
                        else:
                            self.vars['produto selecionado'] = id_item
                            item = self.storage.select(where=f'id={id_item}')[0][:6]
                            for entry, val in zip(self.entrys['estoque'].values(), self.formatting['estoque'](*item[:5]) + [item[-1]]): 
                                try: 
                                    entry.delete(0, tk.END)
                                    entry.insert(0, val)
                                except: 
                                    entry.delete('0.0', tk.END)
                                    entry.insert('0.0', val)
                            self.vars['button cadastrar'].set('Modificar')
                            self.vars['button excluir'].set('Cancelar')
        
            case 'mostrar_detalhes': 
                item = self.trees['estoque'].item(self.trees['estoque'].focus())
                try: 
                    id_item = int(item['values'][0])
                except ValueError: pass
                else:
                    codigo, nome, p_venda, p_custo, quant, desc, cad, mod = self.storage.select(where=f'id = {id_item}')[0]
                    codigo, desc = str(codigo), str(desc)
                    while len(str(codigo)) < 5: codigo = '0' + codigo
                    fal_rows = 10 - len(desc.split('\n'))
                    text = '\n'.join([
                        f'Código: {codigo}',
                        f'Nome: {nome}',
                        f'Preço de venda: R$ {p_venda:.2f}'.replace('.', ','),
                        f'Preço de custo: R$ {p_custo:.2f}'.replace('.', ','),
                        f'Quantidade: {quant}',
                        f'Descrição: {desc}',
                        '\n'*fal_rows,
                        f'Data de cadastro: {cad}',
                        f'Data de última modificação: {mod}'
                    ])
                    self.vars['detalhes'].set(text)
        
            case 'quantidade':
                if event.type == '3': 
                    val = self.entrys['estoque'][key].get()
                    if event.keysym != 'BackSpace': self.entrys['estoque'][key].delete(len(val)-1)
                    val = ''.join([char for char in val.lstrip('0 ') if char.isnumeric()])

                elif event.type == '4': 
                    val = simpledialog.askstring('+', 'Digite o valor a ser adicionado:')
                    try: val = int(val)
                    except: messagebox.showwarning('Erro', 'Formato inválido.\nVerifique se o valor foi digitado corretamente.')
                    else: 
                        try: val_add = int(self.entrys['estoque'][key].get().lstrip('0 '))
                        except ValueError: val_add = 0
                        val += val_add
                self.entrys['estoque'][key].delete(0, tk.END)
                self.entrys['estoque'][key].insert(0, f'{val}')

            case 'vendas':
                self.tree_update('vendas', self.sales.select())