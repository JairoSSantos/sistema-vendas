import pandas as pd
from random import randint

STORAGE_FILENAME = 'storage.csv' # caminho até o arquivo de estoque

def autosave(function):
    def dec_function(*args, **kwargs):
        function(*args, **kwargs)
        args[0].save()
    return dec_function

class DataError(Exception): # classe de erros
    def __init__(self, message):
        super().__init__(message)

class Storage:
    def __init__(self, filename):
        self.filename = filename
        self.update()
    
    @autosave
    def add(self, nome:str, p_venda:float, p_custo:float, quantidade:int):
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
        index = 0
        while index in self.dataframe['id'].tolist(): index += 1
        self.dataframe = self.dataframe.append({
            'id': index,
            'nome':nome, 
            'p_venda':p_venda, 
            'p_custo':p_custo, 
            'quantidade':quantidade
        }, ignore_index=True)
    
    @autosave
    def delete(self, index):
        '''
        Deletar produto.

        Args:
            index: índice do produto a ser deletado.
        '''
        self.dataframe = self.dataframe.drop(index=index)
    
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
    global storage
    storage = Storage(STORAGE_FILENAME)