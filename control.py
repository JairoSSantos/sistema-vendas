import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import data
import theme

class App:
    def __init__(self, root):
        # configurando janela principal
        self.root = root
        self.root.title('Controle de dados')
        self.root.state('zoomed')

        # definir estilo da aplicação
        self.style = ttk.Style()
        self.style.theme_create('MyTheme', parent='alt', settings=theme.settings_main)
        self.style.theme_use('MyTheme')
        self.style.layout('Treeview', theme.treeview_layout)
        self.style.layout('Vertical.TScrollbar', theme.vertical_scrollbar_layout)
        self.style.layout('TCombobox', theme.combobox_layout)

        # definir frame principal
        self.notebook_main = ttk.Notebook(self.root)

        self.frames = {} # frames
        self.vars = {'filtros':{'estoque':[], 'vendas':[]}} # variáveis
        self.entrys = {'estoque':{}, 'vendas':{}} # entradas
        self.trees = {}
        self.combos = {}

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

        # código
        ttk.Label(self.frames['estoque']['produto'], text='Código:', width=labels_width, anchor='e').grid(row=0, column=0, pady=2, sticky='w', padx=[0, 2])
        entry = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
        entry.grid(row=0, column=1, padx=[0, 10], sticky='ew')
        entry.bind('<Return>', lambda event: self.entrys['estoque']['nome'].focus())
        self.entrys['estoque']['id'] = entry

        # nome
        ttk.Label(self.frames['estoque']['produto'], text='Nome:', width=labels_width, anchor='e').grid(row=1, column=0, pady=2, sticky='w', padx=[0, 2])
        entry = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
        entry.grid(row=1, column=1, padx=[0, 10], sticky='ew')
        entry.bind('<Return>', lambda event: self.entrys['estoque']['p_venda'].focus())
        self.entrys['estoque']['nome'] = entry

        # preço de venda
        ttk.Label(self.frames['estoque']['produto'], text='Preço de venda:', width=labels_width, anchor='e').grid(row=2, column=0, pady=2, sticky='w', padx=[0, 2])
        entry = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
        entry.insert(0, 'R$ 0,00')
        entry.bind('<KeyRelease>', lambda event: self.update('p_venda', event))
        entry.grid(row=2, column=1, padx=[0, 10], sticky='ew')
        entry.bind('<Return>', lambda event: self.entrys['estoque']['p_custo'].focus())
        self.entrys['estoque']['p_venda'] = entry

        # preço de custo
        ttk.Label(self.frames['estoque']['produto'], text='Preço de custo:', width=labels_width, anchor='e').grid(row=3, column=0, pady=2, sticky='w', padx=[0, 2])
        entry = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
        entry.insert(0, 'R$ 0,00')
        entry.bind('<KeyRelease>', lambda event: self.update('p_custo', event))
        entry.grid(row=3, column=1, padx=[0, 10], sticky='ew')
        entry.bind('<Return>', lambda event: self.entrys['estoque']['quantidade'].focus())
        self.entrys['estoque']['p_custo'] = entry

        # quantidade
        ttk.Label(self.frames['estoque']['produto'], text='Quantidade:', width=labels_width, anchor='e').grid(row=4, column=0, pady=2, sticky='w', padx=[0, 2])
        entry = tk.Entry(self.frames['estoque']['produto'], **theme.entry_style)
        entry.grid(row=4, column=1, padx=[0, 10], sticky='ew')
        entry.bind('<Double-Button-1>', lambda event: self.update('quantidade', event))
        entry.bind('<KeyRelease>', lambda event: self.update('quantidade', event))
        entry.bind('<Return>', lambda event: self.entrys['estoque']['descricao'].focus())
        self.entrys['estoque']['quantidade'] = entry

        # descrição
        ttk.Label(self.frames['estoque']['produto'], text='Descrição:', 
            width=labels_width, anchor='e').grid(row=5, column=0, sticky='nw', padx=[0, 2])
        entry = tk.Text(self.frames['estoque']['produto'], width=10, height=5, **theme.entry_style)
        entry.grid(row=5, column=1, padx=[0, 10], sticky='ew', pady=2)
        self.entrys['estoque']['descricao'] = entry

        # butões da aba estoque
        self.vars['button cadastrar'] = tk.StringVar()
        self.vars['button cadastrar'].set('Cadastrar')
        self.vars['button excluir'] = tk.StringVar()
        self.vars['button excluir'].set('Excluir')
        ttk.Button(self.frames['estoque']['produto'], textvariable=self.vars['button cadastrar'], command=self.register).grid(row=6, column=0, pady=10)
        ttk.Button(self.frames['estoque']['produto'], textvariable=self.vars['button excluir'], command=self.delete).grid(row=6, column=1, pady=10)

        # filtrar dados
        self.menu_estoque = ttk.Menubutton(self.frames['estoque']['pesquisar'], text='Filtrar')
        self.menu_estoque.menu = tk.Menu(self.menu_estoque, tearoff=1, **theme.menu_style)
        self.menu_estoque['menu'] = self.menu_estoque.menu
        self.vars['filtros']['estoque'] = []
        for key in ['código', 'Nome', 'Preço de venda', 'Preço de custo', 
            'Quantidade', 'Descrição', 'Data de cadastro', 'Data de modificação']:
            var = tk.IntVar()
            var.set(0)
            self.menu_estoque.menu.add_checkbutton(label=key, variable=var)
            self.vars['filtros']['estoque'].append(var)
        self.menu_estoque.grid(row=0, column=2, pady=5, padx=7)

        #definir widgets para visualizar detalhes do produto
        self.vars['detalhes'] = tk.StringVar()
        self.vars['detalhes'].set('\n'*17)
        ttk.Label(self.frames['estoque']['detalhes'], width=35, #height=12, 
            textvariable=self.vars['detalhes'], justify=tk.LEFT, anchor='w').pack()

        # definir widgets para pesquisar produto
        ttk.Label(self.frames['estoque']['pesquisar'], text='Pesquisar:').grid(row=0, column=0, padx=[0, 2])
        self.entrys['estoque']['pesquisar'] = tk.Entry(self.frames['estoque']['pesquisar'], width=70, **theme.entry_style)
        self.entrys['estoque']['pesquisar'].bind('<KeyRelease>', lambda event: self.find('estoque'))
        self.entrys['estoque']['pesquisar'].grid(row=0, column=1)

        # definir treeview do estowue
        columns = [
            ['Código', 100],
            ['Nome', 250],
            ['Preço de venda', 150],
            ['Preço de custo', 150],
            ['Quantidade', 100]
        ]
        self.scrollbar_estoque = ttk.Scrollbar(self.frames['estoque']['tree'], orient='vertical')
        self.trees['estoque'] = ttk.Treeview(self.frames['estoque']['tree'], columns=list(map(lambda a: a[0], columns)), height=30)
        self.trees['estoque'].column('#0', width=50)
        for key, width in columns:
            self.trees['estoque'].column(key, width=width, anchor='center')
            self.trees['estoque'].heading(key, text=key)
        self.trees['estoque'].bind('<Double-1>', lambda event: self.update('show_produto'))
        self.trees['estoque'].bind('<<TreeviewSelect>>', lambda event: self.update('show_detalhes'))
        self.trees['estoque'].configure(yscroll=self.scrollbar_estoque.set)
        self.trees['estoque'].tag_configure(0, background=theme.colors[4])
        self.trees['estoque'].tag_configure(1, background='white')
        self.trees['estoque'].pack(side=tk.LEFT)
        self.scrollbar_estoque.pack(side=tk.RIGHT, fill='y')
        self.scrollbar_estoque.config(command=self.trees['estoque'].yview)

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
        self.entrys['vendas']['pesquisar'].bind('<KeyRelease>', lambda event: self.find('vendas'))
        self.entrys['vendas']['pesquisar'].pack(side=tk.LEFT, padx=[10])

        # filtrar dados
        self.menu_vendas = ttk.Menubutton(self.frames['vendas']['dados'], text='Filtrar')
        self.menu_vendas.menu = tk.Menu(self.menu_vendas, tearoff=1, **theme.menu_style)
        self.menu_vendas['menu'] = self.menu_vendas.menu
        self.vars['filtros']['vendas'] = []
        for key in ['Id', 'Horário', 'Produtos', 'Total', 'Valor pago', 'Troco', 'Formato da venda', 'Modificação']:
            var = tk.IntVar()
            var.set(0)
            self.menu_vendas.menu.add_checkbutton(label=key, variable=var)
            self.vars['filtros']['vendas'].append(var)
        self.menu_vendas.pack(side=tk.LEFT, padx=7, pady=5)

        # definir treeview das vendas
        columns = [
            ['Horário', 80],
            ['Produtos', 320],
            ['Total', 150],
            ['Valor pago', 150],
            ['Troco', 150],
            ['Formato de pagamento', 200]
        ]
        self.scrollbar_vendas = ttk.Scrollbar(self.frames['vendas']['tree'], orient='vertical')
        self.trees['vendas'] = ttk.Treeview(self.frames['vendas']['tree'], columns=list(map(lambda a: a[0], columns)), height=30)
        self.trees['vendas'].column('#0', width=50, anchor='center')
        self.trees['vendas'].heading('#0', text='Id')
        for i, (key, width) in enumerate(columns):
            self.trees['vendas'].column(key, width=width, anchor='center')
            self.trees['vendas'].heading(key, text=key)
        self.trees['vendas'].column('Produtos', anchor='w')
        self.trees['vendas'].tag_configure(0, background=theme.colors[4])
        self.trees['vendas'].tag_configure(1, background='white')
        self.trees['vendas'].configure(yscroll=self.scrollbar_vendas.set)
        self.scrollbar_vendas.config(command=self.trees['vendas'].yview)
        self.trees['vendas'].pack(side=tk.LEFT, fill='x')
        self.scrollbar_vendas.pack(side=tk.LEFT, fill='y')

        # definir widgets do relatório de vendas
        ttk.Button(self.frames['vendas']['dados'], text='Relatório').pack(side=tk.LEFT)

        # adicionar abas no notebook
        self.notebook_main.add(self.frames['estoque']['main'], text='Estoque')
        self.notebook_main.add(self.frames['vendas']['main'], text='Vendas')
        self.notebook_main.grid(row=0, column=0)

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
                id_item = int(item['text'])
            except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
            else: 
                if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][0])):
                    data.storage.delete(id_item)
        
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
        filtro = list(map(lambda a: a.get(), self.vars['filtros'][key]))
        if not sum(filtro): filtro = None
        self.tree_update(key, (data.storage if key == 'estoque' else data.sales).find(
            self.entrys[key]['pesquisar'].get(), # pegar valor de entrada
            filtro # pegar os valores variáveis das checkbox de filtragem
        ))
    
    def register(self):
        '''
        Registrar produto.
        '''
        try:
            id_item = int(self.entrys['estoque']['id'].get())
            nome = str(self.entrys['estoque']['nome'].get())
            p_venda = float(self.entrys['estoque']['p_venda'].get().lstrip('R$').replace(',', '.'))
            p_custo = float(self.entrys['estoque']['p_custo'].get().lstrip('R$').replace(',', '.'))
            quantidade = self.entrys['estoque']['quantidade'].get()
            if quantidade == '': quantidade = 0
            descricao = str(self.entrys['estoque']['descricao'].get('0.0', tk.END))
        except ValueError: messagebox.showwarning('Erro ao cadastrar produto!', 'Preencha os campos corretamente.')
        else:
            if self.vars['button cadastrar'].get() == 'Cadastrar':
                try: data.storage.add(id_item, nome, p_venda, p_custo, quantidade, descricao)
                except Exception as error: messagebox.showwarning('Erro ao cadastrar produto!', error)
                else:
                    for item in self.entrys['estoque'].values(): item.delete(0, tk.END)
                    self.entrys['estoque']['p_venda'].insert(0, 'R$ 0,00')
                    self.entrys['estoque']['p_custo'].insert(0, 'R$ 0,00')
        
            elif self.vars['button cadastrar'].get() == 'Modificar':
                try: data.storage.modify(self.vars['produto selecionado'], {'id':id_item, 'nome':nome, 
                        'p_venda':p_venda, 'p_custo':p_custo, 'quantidade':quantidade, 'descricao':descricao})
                except Exception as error: messagebox.showwarning('Erro ao cadastrar produto!', error)
                else:
                    for item in self.entrys['estoque'].values(): 
                        try: item.delete(0, tk.END)
                        except: item.delete('0.0', tk.END)
                    self.vars['button cadastrar'].set('Cadastrar')
                    self.vars['button excluir'].set('Excluir')
                    self.vars['produto selecionado'] = None
            
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
        if key == 'estoque':
            self.trees[key].delete(*self.trees[key].get_children())
            cont = 0
            for i, item in enumerate(items):
                codigo, nome, p_venda, p_custo, quant = list(item.values())[:5]
                codigo = str(codigo)
                while len(codigo) < 5: codigo = '0'+codigo
                self.trees[key].insert('', 'end', text=i, values=[codigo, nome,
                    f'R$ {p_venda:.2f}'.replace('.', ','), f'R$ {p_custo:.2f}'.replace('.', ','), f'{quant} Un'], 
                    tags=int((i+2)%2 == 0))
                cont = i
            if len(items) < 30:
                for j in range(30-len(items)):
                    self.trees[key].insert('', 'end', text='', values=['']*5, tags=int((cont+j+1)%2 == 0))

        if key == 'vendas':
            self.trees[key].delete(*self.trees[key].get_children())
            cont = 0
            for i, item in enumerate(items):
                index, horario, produtos, total, pago, formato, mod = list(item.values())
                text = []
                produtos = produtos.split('-') if '-' in produtos else [produtos]
                for produto in produtos:
                    id_item, quant = produto.split('/')
                    nome = data.storage.get_value(int(id_item), 'nome')
                    if len(text) > 3: 
                        text.append('...')
                        break
                    else: text.append(nome)
                text = ', '.join(text)
                index = str(index)
                while len(index) < 5: index = '0'+index
                if not pago: pago = total
                self.trees[key].insert('', 'end', text=index, values=[horario, text, 
                    f'R$ {total:.2f}'.replace('.', ','), 
                    f'R$ {pago:.2f}'.replace('.', ','), 
                    f'R$ {(pago-total):.2f}'.replace('.', ','),
                    formato],  
                    tags=int((i+2)%2 == 0))
                cont = i
            if len(items) < 30:
                for j in range(30-len(items)):
                    self.trees[key].insert('', 'end', text='', values=['']*6, tags=int((cont+j+1)%2 == 0))

        self.root.update()
    
    def update(self, key, event=None):
        '''
        Atualizar aplicação.

        Args:
            key: chave referente à parte da aplicação que será atualizado.
                |-> 'estoque': atualizar toda a aba de estoque
                |-> 'show_produto': modificar produto
                |-> 'show_detalhes': mostrar detalhes do produto
                |-> 'vendas': atualizar toda a aba de vendas
                |-> 'vendas_verificar_arquivos': verificar arquivos de vendas e atualizar as datas
                |-> 'p_venda' ou 'p_custo': verificar entrada dos preços
        '''
        if key == 'estoque': # atualizar a aba de estoque em geral
            self.tree_update(key, data.storage.get_itemslist())
            self.vars['n cadastros'].set(f'Produtos cadastrados: {data.storage.get_size()}')
            self.entrys['estoque']['id'].delete(0, tk.END)
            self.entrys['estoque']['id'].insert(0, str(data.storage.generate_id()))
            self.entrys['estoque']['p_venda'].delete(0, tk.END)
            self.entrys['estoque']['p_venda'].insert(0, 'R$ 0,00')
            self.entrys['estoque']['p_custo'].delete(0, tk.END)
            self.entrys['estoque']['p_custo'].insert(0, 'R$ 0,00')

        elif key == 'show_produto': # mostrar produto para modificar
            try: id_item = int(self.trees['estoque'].item(self.trees['estoque'].focus())['values'][0])
            except ValueError: pass
            else:
                self.vars['produto selecionado'] = id_item
                codigo, nome, p_venda, p_custo, quant, desc = data.storage.get_item(id_item)[:6]
                for entry in self.entrys['estoque'].values(): 
                    try: entry.delete(0, tk.END)
                    except: entry.delete('0.0', tk.END)
                self.entrys['estoque']['id'].insert(0, codigo)
                self.entrys['estoque']['nome'].insert(0, nome)
                self.entrys['estoque']['p_venda'].insert(0, f'R$ {p_venda:.2f}'.replace('.', ','))
                self.entrys['estoque']['p_custo'].insert(0, f'R$ {p_custo:.2f}'.replace('.', ','))
                self.entrys['estoque']['quantidade'].insert(0, quant)
                self.entrys['estoque']['descricao'].insert('0.0', desc)
                self.vars['button cadastrar'].set('Modificar')
                self.vars['button excluir'].set('Cancelar')
        
        elif key == 'show_detalhes': # mostrar detalhes do produto
            item = self.trees['estoque'].item(self.trees['estoque'].focus())
            try: 
                id_item = int(item['values'][0])
            except ValueError: pass
            else:
                codigo, nome, p_venda, p_custo, quant, desc, cad, mod = data.storage.get_item(id_item)
                while len(str(codigo)) < 5: codigo = '0'+str(codigo)
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
        
        elif key in ('p_venda', 'p_custo'): # verificar a entrada dos preços
            val = self.entrys['estoque'][key].get()
            if event.keysym != 'BackSpace': self.entrys['estoque'][key].delete(len(val)-1)
            val = [char for char in val.lstrip('R$ 0') if char.isnumeric()]
            while len(val) < 3: val.insert(0, '0')
            val.insert(-2, ',')
            self.entrys['estoque'][key].delete(0, tk.END)
            self.entrys['estoque'][key].insert(0, 'R$ ' + ''.join(val))
        
        elif key == 'quantidade':
            if event.type == '3': # keyrelease
                val = self.entrys['estoque'][key].get()
                if event.keysym != 'BackSpace': self.entrys['estoque'][key].delete(len(val)-1)
                val = ''.join([char for char in val.lstrip('0 ') if char.isnumeric()])
            elif event.type == '4': # double-button-1
                val = simpledialog.askstring('+', 'Digite o valor a ser adicionado:')
                try: val = int(val)
                except: messagebox.showwarning('Erro', 'Formato inválido.\nVerifique se o valor foi digitado corretamente.')
                else: 
                    try: val_add = int(self.entrys['estoque'][key].get().lstrip('0 '))
                    except ValueError: val_add = 0
                    val += val_add
            self.entrys['estoque'][key].delete(0, tk.END)
            self.entrys['estoque'][key].insert(0, f'{val}')

        elif key == 'vendas': # atualizar aba de vendas em geral
            self.update('vendas_verificar_arquivos')
        
        elif key == 'vendas_verificar_arquivos': # atualizar arquivos de vendas
            dates = {}
            for filename in data.sales.get_files():
                year, month, day = filename.rstrip('.csv').split('-')
                if year in dates.keys():
                    if month in dates[year].keys(): dates[year][month].append(day)
                    else: dates[year][month] = [day]
                else: dates[year] = {month:[day]}
            self.vars['dates'] = dates
            self.combos['ano']['values'] = list(dates.keys()) + ['----']
            self.combos['ano'].current(len(dates.keys())-1)
            self.update('vendas_combo_ano')
            self.update('vendas_combo_mes')
            self.update('vendas_combo_dia')
        
        elif key == 'vendas_combo_ano':
            year = self.combos['ano'].get()
            if year == '----':
                pass
            else:
                self.combos['mes']['values'] = list(self.vars['dates'][year].keys()) + ['--']
                self.combos['mes'].current(len(self.vars['dates'][year].keys())-1)
        
        elif key == 'vendas_combo_mes':
            year = self.combos['ano'].get()
            month = self.combos['mes'].get()
            if month == '--':
                pass
            else:
                self.combos['dia']['values'] = self.vars['dates'][year][month] + ['--']
                self.combos['dia'].current(len(self.vars['dates'][year][month])-1)
        
        elif key == 'vendas_combo_dia':
            year = self.combos['ano'].get()
            month = self.combos['mes'].get()
            day = self.combos['dia'].get()
            if day == '--':
                pass
            else:
                data.sales.set_file(f'{year}-{month}-{day}.csv')
                self.tree_update('vendas', data.sales.get_itemslist())

        self.root.update()

if __name__ == '__main__':
    data.init()
    root = tk.Tk()
    app = App(root)
    root.mainloop()