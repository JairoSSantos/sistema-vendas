import pandas as pd
from datetime import date, datetime
import os

STORAGE_FILENAME = 'data/storage.csv' # caminho até o arquivo de estoque
SALES_PATH = 'data/sales/' # caminho até a pasta de vendas

def autosave(function):
    def dec_function(itself, *args, **kwargs):
        y = function(itself, *args, **kwargs)
        itself.save()
        if y: return y
    return dec_function

class DataError(Exception): # classe de erros
    def __init__(self, message):
        super().__init__(message)

class Storage:
    '''
    Classe para controlar os dados do estoque.
        |-> Os dados são armazenados em um dataframe do pandas.
        |-> Cada ítem cadastrado deve ter id e nome único.
        |-> Colunas:
            |-> id: A principal idendificação do produto (não confundir com o index do dataframe, o id do produto não deve mudar)
            |-> nome: Nome do produto (não podem haver dois produtos com o mesmo nome)
            |-> p_venda: Preço de venda do produto.
            |-> p_custo: Preço que esse produto custou (este dado irá permitir o cálculo do lucro na venda do produto).
            |-> quantidade: Quantidade do produto em estoque.
            |-> descricao: Uma descrição sobre o produto.
            |-> data_cadastro: Data em que o item foi cadastrado.
            |-> data_mod: Data da úlitima modificação do produto.
    '''
    def __init__(self, filename):
        self.filename = filename
        self.update()
    
    @autosave
    def add(self, id_item, nome, p_venda, p_custo, quantidade, descricao):
        '''
        Adicionar item ao estoque.

        Args:
            nome: nome do produto (type= str).
            p_venda: preço de venda do produto (type= float).
            p_custo: preço de custo do produto (type= float).
            quantidade: quantidade disponível no estoque (type= int).
        '''
        if nome in self.dataframe['nome'].tolist():
            raise DataError('Nome já cadastrado.')
        elif nome == '':
            raise DataError('Nome não informado.')
        if id_item in self.dataframe['id'].tolist():
            raise DataError('Código já cadastrado.')
        today = date.today().strftime('%d/%m/%Y')
        self.dataframe = self.dataframe.append({
            'id': id_item,
            'nome':nome, 
            'p_venda':p_venda, 
            'p_custo':p_custo, 
            'quantidade':quantidade,
            'descricao':descricao,
            'data_cadastro':today,
            'data_mod':today
        }, ignore_index=True)
    
    @autosave
    def decrease(self, id_item, amount):
        '''
        Diminuir quantidade do item.

        Args:
            id_item: código do item.
            amount: quantidade que sera removida.
        '''
        value = self.dataframe.at[self.get_df_index(id_item), 'quantidade']
        self.dataframe.at[self.get_df_index(id_item), 'quantidade'] = value - amount
    
    @autosave
    def delete(self, id_item):
        '''
        Deletar produto.

        Args:
            id_item: id do produto a ser deletado.
        '''
        self.dataframe = self.dataframe.drop(index=self.get_df_index(id_item))
    
    def find(self, value, column_filter=None):
        '''
        Encontrar item no dataframe.

        Args:
            value: valor que deseja ser encontrado.
            column_filter: lista indicando em quais columas do dataframe deve-se procurar o valor (list[bool, bool, ...]).
        
        Returns:
            lista dos itens encontrados.
            formato -> list[dict{}]
        '''
        items = []
        if column_filter == None: column_filter = [True]*len(self.dataframe.columns)
        for i, item in self.dataframe.to_dict('index').items():
            if not item in items:
                for column, verify in zip(self.dataframe.columns, column_filter):
                    if verify and str(value) in str(self.dataframe.at[i, column]):
                        items.append(item)
                        break
        return items
    
    def generate_id(self):
        '''
        Gerar novo código.
        returns:
            int
        '''
        id_item = 0
        while id_item in self.dataframe['id'].tolist(): id_item += 1
        return id_item
    
    def get_df_index(self, id_item):
        '''
        Função para pegar o índice do item no dataframe.

        Args:
            id_item: id do ítem.
        '''
        if not id_item in self.dataframe['id'].tolist():
            raise DataError('Produto não cadastrado!')
        else:
            return self.dataframe.loc[self.dataframe['id'] == id_item].index.item()
    
    def get_itemslist(self): 
        '''
        Pegar dataframe como lista de dicionarios, cada dicionario sendo um ítem.
        returns:
            lista com os dados do dataframe.
        '''
        return list(self.dataframe.to_dict('index').values())
    
    def get_item(self, id_item):
        '''
        Pegar todos os valores de id_item.
        returns:
            lista com todos os valores.
        '''
        return self.dataframe.loc[self.get_df_index(id_item)].tolist()
    
    def get_size(self):
        '''
        Pegar o tamanho do estoque.
        returns:
            valor inteiro referente a quantidade de itens cadastrados.
        '''
        return len(self.dataframe)
    
    def get_value(self, id_item, *columns):
        '''
        Acessar valor no dataframe.

        Args:
            id_item: O id do produto.
            columns: Nome das colunas.
        '''
        if len(columns) == 1: return self.dataframe.at[self.get_df_index(id_item), columns[0]]
        else: return [self.dataframe.at[self.get_df_index(id_item), column] for column in columns]
    
    @autosave
    def increase(self, id_item, amount):
        '''
        Aumentar quantidade do item.

        Args:
            id_item: código do item.
            amount: quantidade que sera acrescentada.
        '''
        value = self.dataframe.at[self.get_df_index(id_item), 'quantidade']
        self.dataframe.at[self.get_df_index(id_item), 'quantidade'] = value + amount
    
    @autosave
    def modify(self, id_item, modifications):
        '''
        Modificar algum produto.

        Args:
            id_item: O id do produto a ser modificado.
            modifications: um dicionário em que a 'key' indica a coluna do item e o 'value' o novo valor.
                |-> Dict{nome da coluna: novo valor}
        '''
        mod = False
        df_id = self.get_df_index(id_item)
        for key, value in modifications.items(): 
            if value != self.dataframe.at[df_id, key]:
                if key in ('id', 'nome') and value in self.dataframe[key].tolist():
                    raise DataError(f'Produto com "{key}" = "{value}" já está cadastrado.')
                elif key in ('data_cadastro', 'data_mod'):
                    raise DataError(f'O valor de "{key}" não pode ser alterado!')
                else: 
                    self.dataframe.at[df_id, key] = value
                    mod = True
        if mod: self.dataframe.at[df_id, 'data_mod'] = date.today().strftime('%d/%m/%Y')
    
    def save(self):
        '''
        Salvar os dados.
        '''
        self.dataframe.to_csv(self.filename, index=False)
    
    def update(self):
        '''
        Atualizar o dataframe.
        '''
        self.dataframe = pd.read_csv(self.filename)

class Sales:
    '''
    Classe para controlar os dados das vendas.
        |-> As vendas são salvas por dia.
        |-> Os dados são armazenados em um dataframe do pandas.
        |-> Cada ítem cadastrado deve ter id diferente.
        |-> Colunas:
            |-> id: A principal idendificação da venda (não confundir com o index do dataframe, o id da venda não deve mudar)
            |-> horario: A hora em que a venda foi realizada
            |-> produtos: produtos vendidos (formato: produto1-produto2-...; produto = id do produto/quantidade)
            |-> total: Valor total da venda.
            |-> pago: Valor pago pelo cliente.
            |-> formato: Formato de pagamento (dinheiro, cartão de débito, cartão de crédito, ...).
            |-> mod: Alterações no valor final (descondos, acécimos, ...).
    '''
    def __init__(self, path):
        self.path = path
        self.filename = None
        self.storage = Storage(STORAGE_FILENAME)
        self.update()
    
    @autosave
    def add(self, produtos, pago=0, formato='dinheiro', mod=0):
        '''
        Adicionar item à venda.

        Args:
            produtos: produtos que foram vendidos (formato: [[id do produto, quantidade], [id do produto, quantidade], ...]).
            pago: valor pago pelo cliente.
            formato: formato de venda (dinheiro, cartão de crédito, cartão de débito, ...).
            mod: alguma alteração no valor final (em %).
        '''
        produtos_text = []
        total = 0
        for id_item, quantidade in produtos:
            total += self.storage.get_value(id_item, 'p_venda') * quantidade
            produtos_text.append(f'{id_item}/{quantidade}')
        total *= 1 + mod/100
        self.dataframe = self.dataframe.append({
            'id': self.get_next_id(),
            'horario': datetime.now().strftime('%H:%M'),
            'produtos': '-'.join(produtos_text), 
            'total':total, 
            'pago':pago, 
            'formato':formato,
            'mod':mod
        }, ignore_index=True)
    
    def find(self, value, column_filter=None):
        '''
        Encontrar item no dataframe.

        Args:
            value: valor que deseja ser encontrado.
            column_filter: lista indicando em quais columas do dataframe deve-se procurar o valor (list[bool, bool, ...]).
        
        Returns:
            lista dos itens encontrados.
            formato -> list[dict{}]
        '''
        items = []
        value = str(value)
        if column_filter == None: column_filter = [True]*len(self.dataframe.columns)
        for i, item in self.get_dict().items():
            if not item in items:
                for column, verify in zip(self.dataframe.columns, column_filter):
                    av_value = self.produtos_form(self.dataframe.at[i, column], 'str0') if column == 'produtos' else str(self.dataframe.at[i, column])
                    if verify and value in av_value:
                        items.append(item)
                        break
        return items
    
    def get_current_date(self):
        '''
        Pegar data atual.
        '''
        return datetime.now().strftime('%Y/%m/%d')
    
    def get_dict(self):
        '''
        Pegar dataframe como dicionário.
        returns:
            dicionário com os dados do dataframe.
        '''
        return self.dataframe.to_dict('index')
    
    def get_files(self):
        '''
        Pegar arquivos salvos.

        Returns:
            lista dos arquivos de vendas.
        '''
        return os.listdir(self.path)
    
    def get_itemslist(self): 
        '''
        Pegar dataframe como lista de dicionarios, cada dicionario sendo um ítem.
        returns:
            lista com os dados do dataframe.
        '''
        return list(self.dataframe.to_dict('index').values())
    
    def get_next_id(self):
        '''
        Pegar id da próxima venda.
        '''
        id_item = 0
        while id_item in self.dataframe['id'].tolist(): id_item += 1
        return id_item
    
    def produtos_form(self, df_produtos, utype, **kwargs):
        '''
        Formatar dados de produtos vendidos pelo nome do produto.

        Args:
            df_produtos: produtos no formato salvo.
            utype: formato de saída
                |-> str0: 'nome_1/quantidade_1-nome_2/quantidade_2-...'
                |-> str1: 'nome_1; nome_2...'
        '''
        if utype == 'str0':
            text = []
            df_produtos = df_produtos.split('-') if '-' in df_produtos else [df_produtos]
            for produto in df_produtos:
                id_item, quant = produto.split('/')
                nome = self.storage.get_value(int(id_item), 'nome')
                text.append(f'{nome}/{quant}')
            return '-'.join(text)
        
        elif utype == 'str1':
            text = []
            df_produtos = df_produtos.split('-') if '-' in df_produtos else [df_produtos]
            for produto in df_produtos:
                id_item, quant = produto.split('/')
                nome = self.storage.get_value(int(id_item), 'nome')
                text.append(nome)
            return '; '.join(text)
    
    def save(self):
        '''
        Salvar os dados.
        '''
        self.dataframe.to_csv(self.filename, index=False)
    
    def set_file(self, name):
        '''
        Definir arquivo.

        Args:
            name: nome do arquivo (formato: "ano-mês-dia.csv").
        '''
        if not name in self.get_files():
            raise DataError(f'Arquivo "{name}" não existe!')
        else: 
            self.filename = os.path.join(self.path, name)
            self.update()
    
    def set_current_file(self):
        '''
        Selecionar o arquivo de vendas atual.
        '''
        name = date.today().strftime('%Y-%m-%d') + '.csv'
        self.filename = os.path.join(self.path, name)
        if not name in self.get_files():
            self.dataframe = pd.DataFrame(columns=['id', 'horario', 'produtos', 'total', 'pago', 'formato', 'mod'])
            self.save()
        else: self.update()
    
    def update(self):
        '''
        Atualizar o dataframe.
        '''
        if not self.filename: self.set_current_file()
        try: self.dataframe = pd.read_csv(self.filename)
        except FileNotFoundError:
            raise DataError('Arquivo não encontrado!')

def init():
    '''
    Cria variáveis globais para acessar as classes de contole de dados.
    '''
    global storage, sales
    storage = Storage(STORAGE_FILENAME)
    sales = Sales(SALES_PATH)