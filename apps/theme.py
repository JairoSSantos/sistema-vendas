COLORS = (
    '#084C61', # notebook tab
    '#DB3A34', # notebook selected tab, button background
    '#323031', # text
    '#177E89', # entrys
    '#FFE8B9', # treeview
    '#FFC857' # treeview heading
)

# FONTS
FONTS = [
    ('calibri', 18),    # 0
    ('calibri', 14),    # 1
    ('calibri', 12),    # 2
    ('calibri', 14, 'bold'),    # 3
    ('calibri', 32),    # 4
    ('calibri', 16),    # 5
    ('calibri', 20),     # 6
    ('calibri', 24)     # 7
]

ARROW_UP = u'\u2B06'
ARROW_DOWN = u'\u2B07'

# configurações do estilo da janela de controle
SETTINGS_MAIN = {
    'TNotebook':{
        'configure':{'tabposition':'wn', 'background':COLORS[0]}
    },
    'TNotebook.Tab':{
        'configure':{
            'background':COLORS[0], 
            'padding':[5, 5], 
            'width':11, 
            'font':FONTS[0], 
            'foreground':'white'
        },
        'map':{
            'background':[('selected', COLORS[1])],
            'expand':[('selected', [0]*4)]
        }
    },
    'TFrame':{
        'configure':{'background':'white'}
    },
    'TLabel':{
        'configure':{
            'background':'white', 
            'foreground':COLORS[2],
            'font':FONTS[2]
        }
    },
    'TLabelframe':{
        'configure':{
            'background':'white', 
            'relief':'solid', 
            'borderwidth':1, 
            'bordercolor':COLORS[2]
        }
    },
    'TLabelframe.Label':{
        'configure':{
            'background':'white', 
            'foreground':COLORS[2],
            'font':FONTS[1]
        }
    },
    'TButton':{
        'configure':{
            'background':COLORS[1],
            'foreground':'white',
            'font':FONTS[3],
            'anchor':'center',
            'width':10
        }
    },
    'Treeview':{
        'configure':{
            'background':'white',
            'foreground':COLORS[2]
        },
        'map':{
            'background':[('selected', COLORS[0])],
            'foreground':[('selected', 'white')]
        }
    },
    'Treeview.Heading':{
        'configure':{
            'background':COLORS[5],
            'foreground':COLORS[0],
            'font':FONTS[2]
        }
    },
    'Vertical.TScrollbar':{
        'configure':{
            'background':COLORS[1],
            'troughcolor':COLORS[4], 
            'troughrelief':'flat', 
            'relief':'flat', 
            'arrowcolor':'white'
        }
    },
    'TCombobox':{
        'configure':{
            'font':FONTS[0],
            'background':'white',
            'relief':'flat',
            'selectbackground':'while',
            'selectforeground':COLORS[2],
            'foreground':COLORS[2]
        }
    },
    'TMenubutton':{
        'configure':{
            'background':COLORS[1],
            'foreground':'white',
            'font':FONTS[3],
            'width':7,
            'anchor':'center',
            'arrowcolor':'white',
        }
    }
}

TREEVIEW = [
    ('Treeview.field', None),
    ('Treeview.border', {'sticky':'nswe', 'children':[
        ('Treeview.padding', {'sticky':'nswe', 'children': [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ]})
    ]})
]

VERTICAL_SCROLLBAR = [
    ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':[
        ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
        ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
        ('Vertical.Scrollbar.thumb', {'unit': '1', 'sticky': 'ns', 'children':[
            ('Vertical.Scrollbar.grip', {'sticky': ''})
        ]})
    ]})
]

COMBOBOX = [
    ('Combobox.border', {'sticky': 'nswe', 'children': [ 
        ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
            ('Combobox.background', {'sticky': 'nswe', 'children': [
                ('Combobox.textarea', {'sticky': 'nswe'})
            ]})
        ]})
    ]})
]

ENTRY = {
    'background':'white', 
    'foreground':COLORS[0], 
    'font':FONTS[2], 
    'relief':'flat',
    'border':0,
    'highlightbackground':COLORS[3],
    'highlightcolor':COLORS[1],
    'highlightthickness':1,
    'selectbackground':COLORS[0],
    'selectforeground':'white'
}
MENU = {
    'bg':'white',
    'fg':COLORS[2],
    'selectcolor':COLORS[3],
    'activebackground':COLORS[3],
    'activeforeground':'white'
}

# configurações do estilo da janela do caixa
SETTINGS_CASHIER = {
    'TFrame':{
        'configure':{'background':'white'}
    },
    'TLabel':{
        'configure':{
            'background':'white', 
            'foreground':COLORS[2],
            'font':FONTS[2]
        }
    },
    'TButton':{
        'configure':{
            'background':COLORS[1],
            'foreground':'white',
            'font':FONTS[3],
            'anchor':'center',
            'width':10
        }
    },
    'Treeview':{
        'configure':{
            'background':'white',
            'foreground':COLORS[2],
            'font':FONTS[2],
            'rowheight':30
        },
        'map':{
            'background':[('selected', COLORS[0])],
            'foreground':[('selected', 'white')]
        }
    },
    'Treeview.Heading':{
        'configure':{
            'background':COLORS[5],
            'foreground':'white',
            'font':FONTS[1]
        }
    },
    'Vertical.TScrollbar':{
        'configure':{
            'background':COLORS[1],
            'troughcolor':COLORS[4], 
            'troughrelief':'flat', 
            'relief':'flat', 
            'arrowcolor':'white'
        }
    },
    'TMenubutton':{
        'configure':{
            'background':COLORS[1],
            'foreground':'white',
            'font':FONTS[3],
            'width':7,
            'anchor':'center',
            'arrowcolor':'white',
        }
    }
}
LABELINFO = {
    'bg':COLORS[0],
    'fg':'white'
}