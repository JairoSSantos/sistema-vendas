from cashier import CashierApp
from control import *
from mysql.connector import connect
import database
import theme

class LoginApp(ttk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()

        self.style = ttk.Style()
        self.style.theme_create('MyTheme', parent='alt', settings=theme.settings_main)
        self.style.theme_use('MyTheme')

        root = ttk.Frame(self)
        root.pack(padx=20, pady=20)

        ttk.Label(root, text='Senha:').grid(row=1, column=1)
        self.pass_entry = tk.Entry(root, **theme.entry_style)
        self.pass_entry.bind('<Return>', self.check_password)
        self.pass_entry.grid(row=1, column=2, padx=5)
        ttk.Button(root, text='Confirmar', command=self.check_password).grid(row=1, column=3)

        self.login_message = tk.StringVar()
        ttk.Label(root, textvariable=self.login_message).grid(row=2, column=1, columnspan=3)
    
    def check_password(self, event=None):
        with connect(host='localhost', user='root', password=self.pass_entry.get()) as con:
            database.init(con)
            if not database.get_databases('sistema_vendas'):
                self.login_message.set('Criando banco de dados "sistema_vendas"...')
                database.create_database()
            
            for table_name in ('produtos', 'vendas', 'compras'):
                if not database.get_tables(table_name): 
                    database.create_table(table_name)
                    self.login_message.set(f'Criando tabela "{table_name}"...')

            self.destroy()
            #ControlApp(database.Table('produtos'), database.Table('vendas')).mainloop()
            CashierApp(database.Table('produtos'), database.Table('vendas'), database.Table('compras')).mainloop()

if __name__ == '__main__':
    LoginApp().mainloop()