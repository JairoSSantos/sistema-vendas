colors = [
    '#084C61', # notebook tab
    '#DB3A34', # notebook selected tab, button background
    '#323031', # text
    '#177E89', # entrys
    '#FFE8B9', # treeview
    '#FFC857' # treeview heading
]

# fonts
fonts = [
    ('calibri', 18),    # 0
    ('calibri', 14),    # 1
    ('calibri', 12),    # 2
    ('calibri', 14, 'bold'),    # 3
    ('calibri', 32),    # 4
    ('calibri', 16),    # 5
    ('calibri', 20)     # 6
]

# configurações do estilo da janela de controle
settings_main = {
    'TNotebook':{
        'configure':{'tabposition':'wn', 'background':colors[0]}
    },
    'TNotebook.Tab':{
        'configure':{
            'background':colors[0], 
            'padding':[5, 5], 
            'width':11, 
            'font':fonts[0], 
            'foreground':'white'
        },
        'map':{
            'background':[('selected', colors[1])],
            'expand':[('selected', [0]*4)]
        }
    },
    'TFrame':{
        'configure':{'background':'white'}
    },
    'TLabel':{
        'configure':{
            'background':'white', 
            'foreground':colors[2],
            'font':fonts[2]
        }
    },
    'TLabelframe':{
        'configure':{
            'background':'white', 
            'relief':'solid', 
            'borderwidth':1, 
            'bordercolor':colors[2]
        }
    },
    'TLabelframe.Label':{
        'configure':{
            'background':'white', 
            'foreground':colors[2],
            'font':fonts[1]
        }
    },
    'TButton':{
        'configure':{
            'background':colors[1],
            'foreground':'white',
            'font':fonts[3],
            'anchor':'center',
            'width':10
        }
    },
    'Treeview':{
        'configure':{
            'background':'white',
            'foreground':colors[2]
        },
        'map':{
            'background':[('selected', colors[0])],
            'foreground':[('selected', 'white')]
        }
    },
    'Treeview.Heading':{
        'configure':{
            'background':colors[5],
            'foreground':'white',
            'font':fonts[2]
        }
    },
    'Vertical.TScrollbar':{
        'configure':{
            'background':colors[1],
            'troughcolor':colors[4], 
            'troughrelief':'flat', 
            'relief':'flat', 
            'arrowcolor':'white'
        }
    },
    'TCombobox':{
        'configure':{
            'font':fonts[0],
            'background':'white',
            'relief':'flat',
            'selectbackground':'while',
            'selectforeground':colors[2],
            'foreground':colors[2]
        }
    },
    'TMenubutton':{
        'configure':{
            'background':colors[1],
            'foreground':'white',
            'font':fonts[3],
            'width':7,
            'anchor':'center',
            'arrowcolor':'white',
        }
    }
}

treeview_layout = [
    ('Treeview.field', None),
    ('Treeview.border', {'sticky':'nswe', 'children':[
        ('Treeview.padding', {'sticky':'nswe', 'children': [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ]})
    ]})
]

vertical_scrollbar_layout = [
    ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':[
        ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
        ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
        ('Vertical.Scrollbar.thumb', {'unit': '1', 'sticky': 'ns', 'children':[
            ('Vertical.Scrollbar.grip', {'sticky': ''})
        ]})
    ]})
]

combobox_layout = [
    ('Combobox.border', {'sticky': 'nswe', 'children': [ 
        ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
            ('Combobox.background', {'sticky': 'nswe', 'children': [
                ('Combobox.textarea', {'sticky': 'nswe'})
            ]})
        ]})
    ]})
]

entry_style = {
    'background':'white', 
    'foreground':colors[0], 
    'font':fonts[2], 
    'relief':'flat',
    'border':0,
    'highlightbackground':colors[3],
    'highlightthickness':1
}
menu_style = {
    'bg':'white',
    'fg':colors[2],
    'selectcolor':colors[3],
    'activebackground':colors[3],
    'activeforeground':'white'
}

# configurações do estilo da janela do caixa
settings_cashier = {
    'TFrame':{
        'configure':{'background':'white'}
    },
    'TLabel':{
        'configure':{
            'background':'white', 
            'foreground':colors[2],
            'font':fonts[2]
        }
    },
    'TButton':{
        'configure':{
            'background':colors[1],
            'foreground':'white',
            'font':fonts[3],
            'anchor':'center',
            'width':10
        }
    },
    'Treeview':{
        'configure':{
            'background':'white',
            'foreground':colors[2],
            'font':fonts[5],
            'rowheight':30
        },
        'map':{
            'background':[('selected', colors[0])],
            'foreground':[('selected', 'white')]
        }
    },
    'Treeview.Heading':{
        'configure':{
            'background':colors[5],
            'foreground':'white',
            'font':fonts[0]
        }
    },
    'Vertical.TScrollbar':{
        'configure':{
            'background':colors[1],
            'troughcolor':colors[4], 
            'troughrelief':'flat', 
            'relief':'flat', 
            'arrowcolor':'white'
        }
    },
    'TMenubutton':{
        'configure':{
            'background':colors[1],
            'foreground':'white',
            'font':fonts[3],
            'width':7,
            'anchor':'center',
            'arrowcolor':'white',
        }
    }
}
labelinfo_style = {
    'bg':colors[3],
    'fg':'white'
}