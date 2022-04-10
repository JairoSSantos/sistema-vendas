
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
        f'create database if not exists sistema_vendas '
        'default character set utf8 '
        'default collate utf8_general_ci'
    )

@DDL
def create_table(table_name:str) -> str:
    match table_name:
        case 'compras':
            return (
                'create table if not exists sistema_vendas.compras ('
                'id_vendas int not null,'
                'id_produto int not null,'
                'quantidade mediumint,'
                'extra text,'
                'foreign key (id_vendas) references sistema_vendas.vendas(id),'
                'foreign key (id_produto) references sistema_vendas.produtos(id)'
                ') default charset = utf8'
            )

        case 'produtos':
            return (
                'create table if not exists sistema_vendas.produtos ('
                'id int unique auto_increment,'
                'nome varchar(30) not null unique,'
                'p_venda decimal(7, 2),'
                'p_custo decimal(7, 2),'
                'quantidade mediumint,'
                'descricao tinytext,'
                'data_cad date,'
                'data_mod date,'
                'primary key (id)'
                ') default charset = utf8'
            )
        
        case 'vendas':
            return (
                'create table if not exists sistema_vendas.vendas ('
                'id int unique auto_increment,'
                'horario datetime,'
                'total decimal(7, 2),'
                'pago decimal(7, 2),'
                'extra text,'
                'primary key (id)'
                ') default charset = utf8'
            )

@DQL
def get_databases(like:str=None) -> str:
    return f'show databases' + (f' like "{like}"' if like else '')

@DQL
def get_tables(like:str=None) -> str:
    return 'show tables from sistema_vendas' + (f' like "{like}"' if like else '')


class Table:
    def __init__(self, name:str):
        self.name = name
    
    @DML
    def delete(self, index:int) -> str:
        return f'delete from sistema_vendas.{self.name} where id = {index}'

    @DQL
    def get(self, where:str=None) -> str:
        return (
            f'select * from sistema_vendas.{self.name}'
            + (f' where {where}' if where else '')
        )

    @DQL
    def get_next_id(self) -> str:
        return (
            'select auto_increment '
            'from information_schema.TABLES '
            'where table_schema = "sistema_vendas" '
            f'and table_name = "{self.name}"'
        )

    @DML
    def modify(self): pass

    @DML
    def insert_into(self, **kwargs) -> str:
        return 'insert into sistema_vendas.{name} ({keys}) values ({values})'.format(
            name=self.name,
            keys= ','.join(kwargs.keys()),
            values= ','.join(map(lambda x: f'"{x}"', kwargs.values()))
        )
    
    @DQL
    def search(self, value, filter_cols:str, cols:str='*') -> str:
        return (
            f'SELECT {cols} MATCH({filter_cols}) '
            f'AGAINST ({value}) AS relevance '
            f'WHERE MATCH({filter_cols}) '
            f'AGAINST {value} ORDER BY relevance DESC LIMIT 0,10'
        )