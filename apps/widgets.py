import tkinter as tk
from tkinter import ttk
from apps.theme import *
from dataclasses import dataclass

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
    
    def clear(self) -> None:
        self.delete(0, tk.END)
    
    def set(self, value) -> None:
        self.delete(0, tk.END)
        self.insert(0, value)
    
class MoneyEntry(StylisedEntry):
    def __init__(self, *args, **kwargs):
        StylisedEntry.__init__(self, *args, **kwargs)

        self['validate'] = 'key'
        self['validatecommand'] = (self.register(self.on_validate), '%S')
        self.bind('<KeyRelease>', self.formatting)
        self.formatting()
    
    def clear(self):
        self.delete(0, tk.END)
        self.formatting()
    
    def formatting(self, event:tk.Event=None) -> None:
        value = ''.join(filter(lambda char: char.isnumeric(), StylisedEntry.get(self))).lstrip('0')
        #print('formatando', value)
        len_value =  len(value)
        if len_value < 3: value = '0'*(3 - len_value) + value
        self.set('R$ {},{}'.format(value[:-2], value[-2:]))
    
    def get(self) -> float:
        value = StylisedEntry.get(self).lstrip('R$ ').replace(',', '.')
        return float(value) if value else 0
    
    def on_validate(self, S:str) -> bool:
        #print('validando', S)
        if len(S) > 1:
            RS, val = S.split(' ')
            return (RS == 'R$' and val.replace(',', '').isalnum())
        else:
            return S.isnumeric()

class StylisedText(tk.Text):
    def __init__(self, *args, **kwargs):
        kwargs.update(ENTRY)
        tk.Text.__init__(self, *args, **kwargs)
    
    def clear(self) -> None:
        self.delete('0.0', tk.END)
    
    def get(self):
        return tk.Text.get(self, '0.0', tk.END)
    
    def set(self, value) -> None:
        self.clear()
        self.insert('0.0', value)

class Form(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        ttk.LabelFrame.__init__(self, *args, **kwargs)

        self.entrys = {}

    def __getitem__(self, key:str):
        return self.entrys[key]
    
    def __setitem__(self, key:str, value:(StylisedEntry|StylisedText)):
        self.entrys[key] = value
        self.entrys[key].bind('<Return>', self.next)

    def next(self, event:tk.Event):
        entrys_list = list(self.entrys.values())
        try: entrys_list[entrys_list.index(event.widget) + 1].focus()
        except IndexError: pass
    
    def clear(self):
        for item in self.entrys.values(): item.clear()
        #next_id = str(self.storage.get_next_id()[0][0])
        #self.entrys['id'].set('0'*(5 - len(next_id)) + next_id)
    
    def get(self) -> dict:
        return {key:entry.get() for key, entry in self.entrys.items() if entry.get()}

@dataclass
class OrderBy:
    column:str #nome da coluna
    asc:bool=True #se True, a coluna será organizada em ordem ascendente

    def get(self) -> str:
        return 'by {} {}'.format(self.column, 'asc' if self.asc else 'desc')
    
    def get_arrow(self) -> str:
        return ARROW_DOWN if self.asc else ARROW_UP

class Treeview(ttk.Treeview):
    def __init__(self, master, table_info, bindings=(), **kwargs):
        self.table_info = table_info
        self.columns = tuple(map(lambda col: col[0], self.table_info))
        ttk.Treeview.__init__(self, master, columns=self.columns, **kwargs)

        self.orderby = OrderBy(self.columns[0], False)

        self.column('#0', width=0)
        for col, heading, width, _ in self.table_info:
            if col == self.orderby.column: heading += self.orderby.get_arrow()
            self.column(col, width=width, anchor='center')
            self.heading(col, text=heading)

        for event_tag, function in bindings:
            self.bind(event_tag, function)
        self.bind('<<Double-1>>', self.double_click)

        self.height = self.cget('height')
        self.ncols = len(self.table_info)

        self.tag_configure(0, background='white')
        self.tag_configure(1, background=COLORS[4])
        self.scrollbar = ttk.Scrollbar(master, orient='vertical')
        self.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.scrollbar.config(command=self.yview)
    
    def double_click(self, event:tk.Event) -> None:
        if self.identify('region', event.x, event.y) == 'heading':
            self.set_orderby(self.identify('column', event.x, event.y))
    
    def get_focus(self) -> dict:
        return self.item(self.focus())
    
    def set_orderby(self, col_index:str) -> None:
        column = self.column(col_index)
        if column['id'] == self.orderby.column:
            self.orderby.asc = not self.orderby.asc
            self.heading(self.orderby.column,
                text=self.heading(self.orderby.column)['text'][:-1] + self.orderby.get_arrow())
        else:
            self.heading(self.orderby.column, text=self.heading(self.orderby.column)['text'][:-1])
            self.orderby = OrderBy(column['id'])
            self.heading(self.orderby.column,
                text=self.heading(self.orderby.column)['text'] + self.orderby.get_arrow())
    
    def update_items(self, items:(list|tuple)) -> None:
        self.delete(*self.get_children())
        for i, item in enumerate(items):
            self.insert('', 'end', values=[f(value) for value, (_, _, _, f) in zip(item, self.table_info)], tags=i%2)
        i = len(items)
        while i <= self.height:
            self.insert('', 'end', values=['']*self.ncols, tags=i%2)
            i += 1