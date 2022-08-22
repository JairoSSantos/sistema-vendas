DATABASE = 'sistema_vendas'

TABLES_DEFINITIONS = {
    'produtos': (
        'id int unique auto_increment',
        'nome varchar(30) not null unique',
        'p_venda decimal(7, 2)',
        'p_custo decimal(7, 2)',
        'quantidade mediumint',
        'descricao tinytext',
        'data_cad date',
        'data_mod date',
        'primary key (id)'
    ),

    'vendas':(
        'id int unique auto_increment',
        'horario datetime',
        'total decimal(7, 2) default 0',
        'pago decimal(7, 2) default 0',
        'extra decimal(7, 2) default 0',
        'formato enum("dinheiro", "crédito", "débito") default "dinheiro"',
        'primary key (id)'
    ),

    'compras':(
        'id int unique auto_increment',
        'id_venda int not null',
        'id_produto int not null',
        'quantidade mediumint not null',
        'extra decimal(7, 2) default 0',
        'foreign key (id_venda) references sistema_vendas.vendas(id)',
        'foreign key (id_produto) references sistema_vendas.produtos(id)',
        'primary key (id)'
    )
}

def init(connection):
    global _connection
    _connection = connection

def DDL(function): # Data Definition Language
    global _connection
    def wrapper(*args, **kwargs):
        with _connection.cursor() as cursor:
            cursor.execute(function(*args, **kwargs))
    return wrapper

def DML(function): # Data Manipulation Language
    global _connection
    def wrapper(*args, **kwargs):
        with _connection.cursor() as cursor:
            cursor.execute(function(*args, **kwargs))
            _connection.commit()
    return wrapper

def DQL(function): # Data Query Language
    global _connection
    def wrapper(*args, **kwargs):
        with _connection.cursor() as cursor:
            cursor.execute(function(*args, **kwargs))
            return cursor.fetchall()
    return wrapper

@DDL
def create_database():
    return (
        f'create database if not exists {DATABASE} '
        'default character set utf8 '
        'default collate utf8_general_ci'
    )

@DDL
def create_table(table_key:str) -> str:
    return (
        f'create table if not exists {DATABASE}.{table_key} ('
        + ','.join(TABLES_DEFINITIONS[table_key])
        + ') default charset = utf8'
    )

@DQL
def get_databases(like:str=None) -> str:
    return f'show databases' + (f' like "{like}"' if like else '')

@DQL
def get_tables(like:str=None) -> str:
    return f'show tables from {DATABASE}' + (f' like "{like}"' if like else '')

class Table:
    def __init__(self, table_name:str):
        self.table_name = table_name
        self.name = f'{DATABASE}.{table_name}'
    
    @DML
    def delete(self, **kwargs) -> str:
        return (
            f'delete from {self.name} ' 
            + ' '.join(f'{k} {v}' for k, v in kwargs.items())
        )
    
    @DQL
    def get_columns(self):
        return f'show columns from {self.name}'

    @DQL
    def get_next_id(self) -> str:
        return (
            'select auto_increment '
            'from information_schema.TABLES '
            'where table_schema = "sistema_vendas" '
            f'and table_name = "{self.table_name}"'
        )
    
    @DQL
    def get_last_id(self) -> str:
        return 'select last_insert_id()'
    
    @DML
    def insert_into(self, **kwargs) -> str:
        return 'insert into {name} ({keys}) values ({values})'.format(
            name=self.name,
            keys= ','.join(kwargs.keys()),
            values= ','.join(map(lambda x: f'"{x}"', kwargs.values()))
        )
    
    @DQL
    def select(self, expr:str='*', **kwargs) -> str:
        return (
            f'select {expr} from {self.name} ' 
            + ' '.join(f'{k} {v}' for k, v in kwargs.items())
        )
    
    @DML
    def update(self, set_:(str|dict), **kwargs) -> str:
        '''
        Args:
            set_: commando no formato string ou um dicionário na forma {coluna:valor, ...}
        '''
        return (
            f'update {self.name} '
            + 'set {} '.format(','.join([f'{k} = "{v}"' for k, v in set_.items()]) if type(set_) == dict else set_)
            + ' '.join(f'{k} {v}' for k, v in kwargs.items())
        )