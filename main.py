import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data

MONTH_NAME = dict(zip(range(1, 13), ['Janeiro', 'Fevereiro', 'Março', 
    'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dasembro']))

MONTH_NUMBER = {name:'0'*(2-len(str(num))) + str(num) for num, name in MONTH_NAME.items()}

colors = [
    '#084C61', # notebook tab
    '#DB3A34', # notebook selected tab, button background
    '#323031', # text
    '#177E89', # entrys
    '#FFE8B9', # treeview
    '#FFC857' # treeview heading
]

fonts = [
    ('calibri', 18),
    ('calibri', 14),
    ('calibri', 12),
    ('calibri', 14, 'bold')
]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Controle de dados')
        self.root.state('zoomed')
        # self.root.geometry(self.root.winfo_geometry())

        self.style = ttk.Style()
        self.style.theme_create('MyTheme', parent='alt', settings={
            'TNotebook':{
                'configure':{'tabposition':'wn', 'background':colors[0]}
            },
            'TNotebook.Tab':{
                'configure':{
                    'background':colors[0], 
                    'padding':[5, 5], 
                    'width':11, 
                    'font':fonts[0], 
                    'foreground':'white'
                },
                'map':{
                    'background':[('selected', colors[1])],
                    'expand':[('selected', [0]*4)]
                }
            },
            'TFrame':{
                'configure':{'background':'white'}
            },
            'TLabel':{
                'configure':{
                    'background':'white', 
                    'foreground':colors[2],
                    'font':fonts[2]
                }
            },
            'TLabelframe':{
                'configure':{
                    'background':'white', 
                    'relief':'solid', 
                    'borderwidth':1, 
                    'bordercolor':colors[2]
                }
            },
            'TLabelframe.Label':{
                'configure':{
                    'background':'white', 
                    'foreground':colors[2],
                    'font':fonts[1]
                }
            },
            'TButton':{
                'configure':{
                    'background':colors[1],
                    'foreground':'white',
                    'font':fonts[3],
                    'anchor':'center'
                }
            },
            'Treeview.Heading':{
                'configure':{
                    'background':colors[5],
                    'foreground':'white',
                    'font':fonts[2]
                }
            }
        })
        self.style.theme_use('MyTheme')
        self.style.layout('Treeview', [
            ('Treeview.field', None),
            ('Treeview.border', {'sticky':'nswe', 'children':[
                ('Treeview.padding', {'sticky':'nswe', 'children': [
                    ('Treeview.treearea', {'sticky': 'nswe'})
                ]})
            ]})
        ])
        self.style.configure('Treeview', background='white', foreground=colors[2])
        self.style.map('Treeview', background=[('selected', colors[0])], foreground=[('selected', 'white')])
        self.style.layout('Vertical.TScrollbar', [
            ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
                ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), 
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), 
                ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'ns'})]})])

        print(self.style.layout('Vertical.TScrollbar'))
        print(self.style.element_options('Vertical.TScrollbar.trough'))

        self.entry_style = {
            'background':'white', 
            'foreground':colors[0], 
            'font':fonts[2], 
            'relief':'flat',
            'border':0,
            'highlightbackground':colors[3],
            'highlightthickness':1
        }

        self.notebook_main = ttk.Notebook(self.root)

        self.frames = {}
        self.vars = {'filtros':{'estoque':None, 'vendas':None}}
        self.entrys = {'estoque':{}, 'vendas':{}}
        self.buttons = {'estoque':{}, 'vendas':{}}
        self.trees = {}
        self.combos = {}

        self.frames['estoque'] = {'main': ttk.Frame(self.notebook_main)}
        self.frames['estoque']['main'].pack(anchor='w', pady=5, padx=5)
        self.frames['estoque']['produto'] = ttk.LabelFrame(self.frames['estoque']['main'], text='Produto')
        self.frames['estoque']['produto'].grid(row=0, column=0, pady=5, padx=5)
        self.frames['estoque']['dados'] = ttk.Frame(self.frames['estoque']['main'])
        self.frames['estoque']['dados'].grid(row=0, column=1, pady=5, padx=5, rowspan=2)
        self.frames['estoque']['detalhes'] = ttk.LabelFrame(self.frames['estoque']['main'], text='Detalhes')
        self.frames['estoque']['detalhes'].grid(row=1, column=0, pady=5, padx=5)
        self.frames['estoque']['pesquisar'] = ttk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['pesquisar'].grid(row=0, column=0, columnspan=2)

        labels_texts = ['Código:', 'Nome:', 'Preço de venda:', 'Preço de custo:', 'Quantidade:', 'Descrição:']
        labels_width = sorted(map(lambda a: len(a), labels_texts))[-1]
        entrys_keys = ['id', 'nome', 'p_venda', 'p_custo', 'quantidade', 'descricao']
        for i, (text, key) in enumerate(zip(labels_texts, entrys_keys)):
            ttk.Label(self.frames['estoque']['produto'], 
                text=text, width=labels_width, anchor='e').grid(row=i, column=0, pady=2, sticky='w', padx=[0, 2])
            entry = tk.Entry(self.frames['estoque']['produto'], **self.entry_style)
            if key in ('p_venda', 'p_custo'): 
                entry.insert(0, 'R$ 0,00')
                entry.bind('<KeyRelease>', (lambda event: self.update('p_venda', event)) if key == 'p_venda' else (lambda event: self.update('p_custo', event)))
            entry.grid(row=i, column=1, padx=[0, 10], sticky='ew')
            self.entrys['estoque'][key] = entry

        button_width = 10
        self.vars['button cadastrar'] = tk.StringVar()
        self.vars['button cadastrar'].set('Cadastrar')
        self.vars['button excluir'] = tk.StringVar()
        self.vars['button excluir'].set('Excluir')
        self.buttons['estoque']['cadastrar'] = ttk.Button(self.frames['estoque']['produto'], 
            textvariable=self.vars['button cadastrar'], width=button_width, command=self.register)
        self.buttons['estoque']['cadastrar'].grid(row=6, column=0, pady=10)
        self.buttons['estoque']['excluir'] = ttk.Button(self.frames['estoque']['produto'], 
            textvariable=self.vars['button excluir'], width=button_width, command=self.delete)
        self.buttons['estoque']['excluir'].grid(row=6, column=1, pady=10)
        self.buttons['estoque']['filtrar'] = ttk.Button(self.frames['estoque']['pesquisar'], 
            text='Filtrar', width=button_width, command= lambda a=0: self.set_filter('estoque'))
        self.buttons['estoque']['filtrar'].grid(row=0, column=2, pady=5, padx=7)

        self.vars['detalhes'] = tk.StringVar()
        self.vars['detalhes'].set('\n'*12)
        ttk.Label(self.frames['estoque']['detalhes'], width=35, #height=12, 
            textvariable=self.vars['detalhes'], justify=tk.LEFT, anchor='w').pack()

        ttk.Label(self.frames['estoque']['pesquisar'], text='Pesquisar:').grid(row=0, column=0, padx=[0, 2])

        self.entrys['estoque']['pesquisar'] = tk.Entry(self.frames['estoque']['pesquisar'], width=70, **self.entry_style)
        self.entrys['estoque']['pesquisar'].bind('<KeyRelease>', lambda event: self.find('estoque'))
        self.entrys['estoque']['pesquisar'].grid(row=0, column=1)

        columns = [
            ['Código', 100],
            ['Nome', 250],
            ['Preço de venda', 150],
            ['Preço de custo', 150],
            ['Quantidade', 100]
        ]

        self.scrollbar = ttk.Scrollbar(self.frames['estoque']['dados'], orient='vertical')
        self.trees['estoque'] = ttk.Treeview(self.frames['estoque']['dados'], columns=list(map(lambda a: a[0], columns)), height=30)
        self.trees['estoque'].column('#0', width=50)
        for key, width in columns:
            self.trees['estoque'].column(key, width=width, anchor='center')
            self.trees['estoque'].heading(key, text=key)
        self.trees['estoque'].bind('<Double-1>', lambda event: self.update('show_produto'))
        self.trees['estoque'].bind('<<TreeviewSelect>>', lambda event: self.update('show_detalhes'))
        self.trees['estoque'].configure(yscroll=self.scrollbar, selectmod='browse')
        self.trees['estoque'].tag_configure(0, background='white')
        self.trees['estoque'].tag_configure(1, background=colors[4])
        self.trees['estoque'].grid(row=1, column=0)
        self.scrollbar.config(command=self.trees['estoque'].yview)
        self.scrollbar.grid(row=1, column=1, sticky=tk.NS)

        self.frames['estoque']['relatório'] = ttk.Frame(self.frames['estoque']['dados'])
        self.frames['estoque']['relatório'].grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.vars['n cadastros'] = tk.StringVar()
        ttk.Label(self.frames['estoque']['relatório'], 
            text='Produtos cadastrados:', width=30, anchor='w', textvariable=self.vars['n cadastros']).pack(side=tk.LEFT)
        self.buttons['estoque']['relatório'] = ttk.Button(self.frames['estoque']['relatório'], text='Relatório')
        self.buttons['estoque']['relatório'].pack(side=tk.RIGHT)

        self.frames['vendas'] = {'main': tk.Frame(self.notebook_main)}
        self.frames['vendas']['main'].pack()
        self.frames['vendas']['dados'] = tk.Frame(self.frames['vendas']['main'])
        self.frames['vendas']['dados'].pack(anchor='w')

        tk.Label(self.frames['vendas']['dados'], text='Data:').pack(side=tk.LEFT)

        self.combos['dia'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=6)
        self.combos['dia'].pack(side=tk.LEFT, padx=2)
        self.combos['mes'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=10)
        self.combos['mes'].pack(side=tk.LEFT, padx=2)
        self.combos['ano'] = ttk.Combobox(self.frames['vendas']['dados'], values=['Todos'], width=6)
        self.combos['ano'].pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.frames['vendas']['dados'], orient='vertical').pack(side=tk.LEFT, fill='y', padx=10)

        tk.Label(self.frames['vendas']['dados'], text='Pesquisar:').pack(side=tk.LEFT)

        self.entrys['vendas']['pesquisar'] = tk.Entry(self.frames['vendas']['dados'])
        self.entrys['vendas']['pesquisar'].bind('<KeyRelease>', lambda event: self.find('vendas'))
        self.entrys['vendas']['pesquisar'].pack(side=tk.LEFT)

        self.buttons['vendas']['filtrar'] = tk.Button(self.frames['vendas']['dados'], 
            text='Filtrar', command=lambda a=0: self.set_filter('vendas'))
        self.buttons['vendas']['filtrar'].pack(side=tk.LEFT)

        columns = [
            ['Id', 80],
            ['Horário da venda', 150],
            ['Produtos', 200],
            ['Total', 100],
            ['Valor pago', 100],
            ['Formato de pagamento', 150]
        ]

        self.trees['vendas'] = ttk.Treeview(self.frames['vendas']['main'], columns=list(map(lambda a: a[0], columns[1:])))
        for i, (key, width) in enumerate(columns):
            if not i: key = '#0'
            self.trees['vendas'].column(key, width=width)
            self.trees['vendas'].heading(key, text=key if i else columns[0][0])
        self.trees['vendas'].pack(anchor='w')

        self.buttons['vendas']['relatorio'] = tk.Button(self.frames['vendas']['main'], text='Relatório')
        self.buttons['vendas']['relatorio'].pack(anchor='w')

        self.notebook_main.add(self.frames['estoque']['main'], text='Estoque')
        self.notebook_main.add(self.frames['vendas']['main'], text='Vendas')
        self.notebook_main.grid(row=0, column=0)

        self.update('estoque')
        self.update('vendas')
    
    def delete(self):
        if self.vars['button excluir'].get() == 'Excluir':
            try: 
                item = self.trees['estoque'].item(self.trees['estoque'].focus())
                id_item = int(item['text'])
            except ValueError: messagebox.showwarning('Erro ao excluir produto!', 'Selecione o produto para excluí-lo.')
            else: 
                if messagebox.askokcancel('Excluir produto.', 'Deseja excluir {}?'.format(item['values'][0])):
                    data.storage.delete(id_item)
        
        elif self.vars['button excluir'].get() == 'Cancelar':
            for item in self.entrys['estoque'].values(): item.delete(0, tk.END)
            self.vars['button cadastrar'].set('Cadastrar')
            self.vars['button excluir'].set('Excluir')
            self.vars['produto selecionado'] = None

        self.update('estoque')
    
    def find(self, key):
        for i in self.trees[key].get_children(): self.trees[key].delete(i)
        item = data.storage if key == 'estoque' else data.sales
        for item in item.find(self.entrys[key]['pesquisar'].get(), self.vars['filtros'][key]):
            self.trees[key].insert('', item['id'], text=item['id'], values=list(item.values())[1:])
        self.root.update()
    
    def register(self):
        try:
            id_item = int(self.entrys['estoque']['id'].get())
            nome = str(self.entrys['estoque']['nome'].get())
            p_venda = float(self.entrys['estoque']['p_venda'].get().lstrip('R$').replace(',', '.'))
            p_custo = float(self.entrys['estoque']['p_custo'].get().lstrip('R$').replace(',', '.'))
            quantidade = self.entrys['estoque']['quantidade'].get()
            if quantidade == '': quantidade = 0
            descricao = str(self.entrys['estoque']['descricao'].get())
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
                    for item in self.entrys['estoque'].values(): item.delete(0, tk.END)
                    self.vars['button cadastrar'].set('Cadastrar')
                    self.vars['button excluir'].set('Excluir')
                    self.vars['produto selecionado'] = None
            
            self.update('estoque')
    
    def set_filter(self, key):
        toplevel = tk.Toplevel()
        toplevel.title('Selecionar filtros')
        toplevel.focus_force()

        tk.Label(toplevel, text='Aplicar filtros:', width=50, anchor='w').pack()

        if key == 'estoque':
            labels = ['Código', 'Nome', 'Preço de venda', 
                'Preço de custo', 'Quantidade', 'Descrição', 'Data de cadastro', 'Data de última modficação']
            ck_vars = []
            for label in labels:
                var = tk.BooleanVar()
                var.set(True)
                tk.Checkbutton(toplevel, text=label, var=var).pack()
                ck_vars.append(var)
        
        elif key == 'vendas':
            labels = ['Id', 'Horário de venda', 'Produtos', 
                'Total', 'Valor pago', 'Formato', 'Modificações']
            ck_vars = []
            for label in labels:
                var = tk.BooleanVar()
                var.set(True)
                tk.Checkbutton(toplevel, text=label, var=var).pack()
                ck_vars.append(var)
        
        def save(): self.vars['filtros'][key] = [v.get() for v in ck_vars]
        tk.Button(toplevel, text='Salvar', command=save).pack()
        tk.Button(toplevel, text='Calcelar', command= lambda a=0: toplevel.destroy()).pack()
        
        toplevel.mainloop()
    
    def update(self, key, event=None):
        if key == 'estoque': # atualizar a aba de estoque em geral
            self.trees[key].delete(*self.trees[key].get_children())
            items = data.storage.get_itemslist()
            for i, item in enumerate(items):
                codigo, nome, p_venda, p_custo, quant = list(item.values())[:5]
                codigo = str(codigo)
                while len(codigo) < 5: codigo = '0'+codigo
                self.trees[key].insert('', 'end', text=i, values=
                    [codigo, nome, f'R$ {p_venda:.2f}', f'R$ {p_custo:.2f}', f'{quant} Un'], tags=[int((i+2)%2 == 0),])
            self.vars['n cadastros'].set(f'Produtos cadastrados: {data.storage.get_size()}')
            self.entrys['estoque']['id'].delete(0, tk.END)
            self.entrys['estoque']['id'].insert(0, str(data.storage.generate_id()))

        elif key == 'show_produto': # mostrar produto
            try: 
                id_item = int(self.trees['estoque'].item(self.trees['estoque'].focus())['values'][0])
            except ValueError: pass
            else:
                self.vars['produto selecionado'] = id_item
                item = data.storage.get_item(id_item)
                for i, entry in enumerate(['id', 'nome', 'p_venda', 'p_custo', 'quantidade', 'descricao']):
                    self.entrys['estoque'][entry].delete(0, tk.END)
                    self.entrys['estoque'][entry].insert(0, item[i])
                self.vars['button cadastrar'].set('Modificar')
                self.vars['button excluir'].set('Cancelar')
        
        elif key == 'show_detalhes':
            item = self.trees['estoque'].item(self.trees['estoque'].focus())
            try: 
                id_item = int(item['values'][0])
            except ValueError: pass
            else:
                codigo, nome, p_venda, p_custo, quant, desc, cad, mod = data.storage.get_item(id_item)
                text = '\n'.join([
                    f'Código: {codigo}',
                    f'Nome: {nome}',
                    f'Preço de venda: {p_venda}',
                    f'Preço de custo: {p_custo}',
                    f'Quantidade: {quant}',
                    f'Descrição: {desc}',
                    f'Data de cadastro: {cad}',
                    f'Data de última modificação: {mod}'
                ])
                self.vars['detalhes'].set(text)
        
        elif key == 'vendas':
            self.update('vendas_arquivo')
            for i in self.trees[key].get_children(): self.trees[key].delete(i)
            for item in data.sales.get_dict().values():
                self.trees[key].insert('', item['id'], text=item['id'], values=list(item.values())[1:])
        
        elif key == 'vendas_arquivo':
            years, months = [], []
            for year, month in map(lambda a: a.rstrip('.csv').split('-'), data.sales.get_files()):
                years.append(year)
                months.append(MONTH_NAME[int(month)])
            self.combos['ano']['values'] = years
            self.combos['ano'].current(0)
            self.combos['mes']['values'] = months
            self.combos['mes'].current(0)
            self.combos['dia'].current(0)

            data.sales.set_file('-'.join([self.combos['ano'].get(), MONTH_NUMBER[self.combos['mes'].get()]+'.csv']))
        
        elif key in ('p_venda', 'p_custo'):
            val = self.entrys['estoque'][key].get()
            if event.keysym != 'BackSpace': self.entrys['estoque'][key].delete(len(val)-1)
            val = [char for char in val.lstrip('R$ 0') if char.isnumeric()]
            while len(val) < 3: val.insert(0, '0')
            val.insert(-2, ',')
            self.entrys['estoque'][key].delete(0, tk.END)
            self.entrys['estoque'][key].insert(0, 'R$ ' + ''.join(val))

        self.root.update()

if __name__ == '__main__':
    data.init()
    root = tk.Tk()
    app = App(root)
    root.mainloop()