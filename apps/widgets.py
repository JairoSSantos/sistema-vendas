import tkinter as tk
from tkinter import ttk
from apps.theme import *

class StylisedApp(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.style = ttk.Style()
        try: self.style.theme_use('MyTheme')
        except tk.TclError: 
            self.style.theme_create('MyTheme', parent='alt', settings=SETTINGS_MAIN)
            self.style.theme_use('MyTheme')
        finally:
            self.style.layout('Treeview', TREEVIEW)
            self.style.layout('Vertical.TScrollbar', VERTICAL_SCROLLBAR)
            self.style.layout('TCombobox', COMBOBOX)
    
class StylisedEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        kwargs.update(ENTRY)
        tk.Entry.__init__(self, *args, **kwargs)
    
    def delete_all(self) -> None:
        self.delete(0, tk.END)
    
    def set(self, value) -> None:
        self.delete_all()
        self.insert(0, value)
    
class MoneyEntry(StylisedEntry):
    def __init__(self, *args, **kwargs):
        StylisedEntry.__init__(self, *args, **kwargs)

        self['validate'] = 'key'
        self['validatecommand'] = lambda char: char.isnumeric(), '%S'
        self.bind('<KeyPress>', self.check_entry)
    
    def check_entry(self, event:tk.Event=None):
        value = ''.join(filter(lambda char:char.isnumeric(), self.get())).lstrip('0')
        len_value =  len(value)
        if len_value < 2: value = '0'*(2 - len_value) + value
        self.set('R$ {},{}'.format(value[:-1], value[-1:]))

class StylisedText(tk.Text):
    def __init__(self, *args, **kwargs):
        kwargs.update(ENTRY)
        tk.Text.__init__(self, *args, **kwargs)
    
    def delete_all(self) -> None:
        self.delete('0.0', tk.END)
    
    def set(self, value) -> None:
        self.delete_all()
        self.insert('0.0', value)