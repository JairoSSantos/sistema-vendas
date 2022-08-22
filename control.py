import tkinter as tk
from tkinter import ttk
from apps.database import Table
from apps.widgets import StylisedApp
from apps.controller import *

#ARROW_UP = u'\u21EA'

class ControlApp(StylisedApp):
    def __init__(self, storage:Table, sales:Table, purchase:Table, master:tk.Frame=None) -> None:
        # configurando janela principal
        StylisedApp.__init__(self, master)
        self.pack()
        self.master.title('Controle de dados')
        self.master.state('zoomed')

        # definir frame principal
        self.notebook_main = ttk.Notebook(self)

        storage_frame = StorageController(storage, self.notebook_main)
        storage_frame.pack(anchor='w', pady=5, padx=5)
        #sales_frame = SalesController(storage, sales, purchase, self.notebook_main)

        # adicionar abas no notebook
        self.notebook_main.add(storage_frame, text='Estoque')
        #self.notebook_main.add(sales_frame, text='Vendas')
        self.notebook_main.grid(row=0, column=0)

        # atializar as abas
        #storage_frame.update('estoque')
        #sales_frame.update('vendas')