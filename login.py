from control import *
from mysql.connector import connect
import database

if __name__ == '__main__':
    with connect(host='localhost', user='root', password=input()) as con:
        database.init(con)
        if not database.get_databases('sistema_vendas'):
            print('Criando banco de dados "sistema_vendas"')
            database.create_database()
        
        for table_name in ['produtos', 'vendas', 'compras']:
            if not database.get_tables(table_name): database.create_table(table_name)

        root = tk.Tk()
        ControlApp(root, database.Table('produtos'), database.Table('vendas'))
        root.mainloop()