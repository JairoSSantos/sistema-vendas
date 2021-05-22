import pandas as pd
from random import randint

STORAGE_FILENAME = 'storage.csv' # caminho até o arquivo de estoque

def autosave(function):
    def dec_function(self, *args, **kwargs):
        function(self, *args, **kwargs)
        self.save()
    return dec_function

class DataError(Exception): # classe de erros
    def __init__(self, message):
        super().__init__(message)

class Storage:
    '''
    Classe para controlar os dados do estoque.
        |-> Os dados são armazenados em um dataframe do pandas.
        |-> Cada ítem cadastrado deve ter id e nome diferendes.
        |-> Colunas:
            |-> id: A principal idendificação do produto (não confundir com o index do dataframe, o id do produto não deve mudar)
            |-> nome: Nome do produto (não podem haver dois produtos com o mesmo nome)
            |-> p_venda: Preço de venda do produto.
            |-> p_custo: Preço que esse produto custou (este dado irá permitir o cálculo do lucro na venda do produto).
            |-> quantidade: Quantidade do produto em estoque.
            |-> descricao: Uma descrição sobre o produto.
    '''
    def __init__(self, filename):
        self.filename = filename
        self.update()
    
    @autosave
    def add(self, nome, p_venda, p_custo, quantidade=0, descricao=''):
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
        id_item = 0
        while id_item in self.dataframe['id'].tolist(): id_item += 1
        self.dataframe = self.dataframe.append({
            'id': id_item,
            'nome':nome, 
            'p_venda':p_venda, 
            'p_custo':p_custo, 
            'quantidade':quantidade,
            'descricao':descricao
        }, ignore_index=True)
    
    @autosave
    def delete(self, id_item):
        '''
        Deletar produto.

        Args:
            id_item: id do produto a ser deletado.
        '''
        self.dataframe = self.dataframe.drop(index=self.get_df_index(id_item))
    
    def get_df_index(self, id_item):
        '''
        Função para pegar o índice do item no dataframe.
        '''
        return self.dataframe.loc[self.dataframe['id'] == id_item].index.item()
    
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

def init():
    '''
    Cria variáveis globais para acessar as classes de contole de dados.
    '''
    global storage
    storage = Storage(STORAGE_FILENAME)