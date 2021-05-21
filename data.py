import pandas as pd
from random import randint

AUTOSAVE = True # salvamento altomátivo ativado com padrão
STORAGE_FILENAME = 'storage.csv' # caminho até o arquivo de estoque
STORAGE_DATA = None # variável para o dataframe

def init():
    storage_update()

def set_autosave(autosave=True):
    '''
    Definir salvamento automático.
    -> Se True, então sempre que algum dataframe for modificado será salvo.
    '''
    global AUTOSAVE
    AUTOSAVE = autosave

def storage_add(nome:str, p_venda:float, p_custo:float, quantidade:int):
    '''
    Adicionar item ao estoque.

    Args:
        nome: nome do produto (type= str).
        p_venda: preço de venda do produto (type= float).
        p_custo: preço de custo do produto (type= float).
        quantidade: quantidade disponível no estoque (type= int).
    '''
    global STORAGE_DATA, AUTOSAVE
    index = 0
    while index in list(STORAGE_DATA['id']): index += 1
    STORAGE_DATA = STORAGE_DATA.append({
        'id': index,
        'nome':nome, 
        'p_venda':p_venda, 
        'p_custo':p_custo, 
        'quantidade':quantidade
    }, ignore_index=True)
    if AUTOSAVE: storage_save()

def storage_save():
    '''
    Salvar os dados do estoque.
    '''
    global STORAGE_DATA
    STORAGE_DATA.to_csv(STORAGE_FILENAME, index=False)

def storage_update():
    '''
    Atualizar a variável STORAGE_DATA.
    '''
    global STORAGE_DATA
    STORAGE_DATA = pd.read_csv(STORAGE_FILENAME)

init()
for i in range(10):
    pre = randint(10, 20)
    storage_add(f'item {i+1}', pre, pre-2, randint(0, 100))