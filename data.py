import pandas as pd
from datetime import date, datetime
import os

STORAGE_FILENAME = 'storage.csv' # caminho até o arquivo de estoque
SALES_PATH = 'sales/' # caminho até a pasta de vendas

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
    def delete(self, id_item):
        '''
        Deletar produto.

        Args:
            id_item: id do produto a ser deletado.
        '''
        self.dataframe = self.dataframe.drop(index=self.get_df_index(id_item))
    
    def find(self, value, column_filter=None):
        items = []
        if column_filter == None: column_filter = [True]*len(self.dataframe.columns)
        for i, item in self.get_dict().items():
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
        '''
        return self.dataframe.loc[self.dataframe['id'] == id_item].index.item()
    
    def get_dict(self): 
        '''
        Pegar dataframe como dicionário.
        returns:
            dicionário com os dados do dataframe.
        '''
        return self.dataframe.to_dict('index')
    
    def get_size(self):
        '''
        Pegar o tamanho do estoque.
        returns:
            valor inteiro referente a quantidade de itens cadastrados.
        '''
        return len(self.dataframe)
    
    @autosave
    def modify(self, id_item, modifications):
        '''
        Modificar algum produto.

        Args:
            id_item: O id do produto a ser modificado.
            modifications: um dicionário em que a 'key' indica a coluna do item e o 'value' o novo valor.
                |-> Dict{nome da coluna: novo valor}
        '''
        for key, value in modifications.items(): 
            if key in ('id', 'nome') and value in self.dataframe[key].tolist():
                raise DataError(f'Produto com "{key}" = "{value}" já está cadastrado.')
            else:
                self.dataframe.at[id_item, key] = value
    
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
        |-> As vendas são salvas por mês.
        |-> Os dados são armazenados em um dataframe do pandas.
        |-> Cada ítem cadastrado deve ter id diferente.
        |-> Colunas:
            |-> id: A principal idendificação da venda (não confundir com o index do dataframe, o id da venda não deve mudar)
            |-> horario: A data e hora em que a venda foi realizada
            |-> produtos: produtos vendidos (formato: produto1-produto2-...; produto = id do produto/quantidade)
            |-> total: Valor total da venda.
            |-> pago: Valor pago pelo cliente.
            |-> formato: Formato de pagamento (dinheiro, cartão de débito, cartão de crédito, ...).
            |-> mod: Alterações no valor final (descondos, acécimos, ...).
    '''
    def __init__(self, path):
        self.path = path
        self.filename = None
        self.update()
    
    @autosave
    def add(self, produtos, total, pago=0, formato='dinheiro', mod=None):
        id_item = 0
        while id_item in self.dataframe['id'].tolist(): id_item += 1
        self.dataframe = self.dataframe.append({
            'id': id_item,
            'horario': datetime.now().strftime('%Y/%m/%d - %H:%M'),
            'produtos':'-'.join(['/'.join(map(str, produto)) for produto in produtos]), 
            'total':total, 
            'pago':pago, 
            'formato':formato,
            'mod':mod
        }, ignore_index=True)
    
    def save(self):
        '''
        Salvar os dados.
        '''
        self.dataframe.to_csv(self.filename, index=False)
    
    def update(self):
        '''
        Atualizar o dataframe.
        '''
        self.filename = os.path.join(self.path, date.today().strftime('%Y-%m') + '.csv')
        try: self.dataframe = pd.read_csv(self.filename)
        except FileNotFoundError:
            self.dataframe = pd.DataFrame(columns=['id', 'horario', 'produtos', 'total', 'pago', 'formato', 'mod'])
            self.save()
            self.update()

def init():
    '''
    Cria variáveis globais para acessar as classes de contole de dados.
    '''
    global storage, sales
    storage = Storage(STORAGE_FILENAME)
    sales = Sales(SALES_PATH)