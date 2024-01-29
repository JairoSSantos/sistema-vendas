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

        login_frame = ttk.Frame(self)
        login_frame.pack(padx=20, pady=20)

        ttk.Label(login_frame, text='Senha:').grid(row=1, column=1)
        self.pass_entry = tk.Entry(login_frame, **theme.entry_style)
        self.pass_entry.bind('<Return>', self.check_password)
        self.pass_entry.grid(row=1, column=2, padx=5)
        ttk.Button(login_frame, text='Confirmar', command=self.check_password).grid(row=1, column=3)

        self.login_message = tk.StringVar()
        self.login_message_label = ttk.Label(login_frame, textvariable=self.login_message)
        self.login_message_label.grid(row=2, column=1, columnspan=3)
        self.login_message_label.grid_remove()

        self.open_frame = ttk.Frame(self)
        self.open_var = tk.StringVar()
        ttk.Button(self.open_frame, text='Controle', width=10,
            command=lambda app='controle': self.open_var.set(app)).pack(padx=10, side=tk.LEFT)
        ttk.Button(self.open_frame, text='Caixa', width=10,
            command=lambda app='caixa': self.open_var.set(app)).pack(padx=10)
    
    def open_app(self):
        self.open_frame.wait_variable(self.open_var)
        self.destroy()
        tables = database.Table('produtos'), database.Table('vendas'), database.Table('compras')
        match self.open_var.get():
            case 'controle': ControlApp(*tables).mainloop()
            case 'caixa': CashierApp(*tables).mainloop()
    
    def check_password(self, event=None):
        with connect(host='localhost', user='root', password=self.pass_entry.get()) as con:
            database.init(con)
            if not database.get_databases('sistema_vendas'):
                self.login_message.set('Criando banco de dados "sistema_vendas"...')
                self.update()
                database.create_database()
            
            for table_name in ('produtos', 'vendas', 'compras'):
                if not database.get_tables(table_name): 
                    self.login_message.set(f'Criando tabela "{table_name}"...')
                    self.login_message_label.grid()
                    self.update()
                    database.create_table(table_name)
                    self.login_message_label.grid_remove()
            
            self.open_frame.pack(pady=10)
            self.open_app()

if __name__ == '__main__':
    LoginApp().mainloop()