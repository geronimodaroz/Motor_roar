import pygame as pg
import sys

# def modifiers_key_state():
#     """Retorna una lista con las teclas modificadoras que están presionadas."""
#     return [valores['key'] for valores in key_events_modifier_list 
#             if pg.key.get_mods() & valores['mod'] == valores['mod']]

# def control_key_state():
#     """Devuelve una lista con los nombres de las teclas de control presionadas."""
#     return [event['key'] for key, pressed in enumerate(pg.key.get_pressed())
#             if pressed for event in key_events_control_list if event['scancode'] == key]

# def char_key_state():
#     """Devuelve una lista con los eventos de teclas de caracteres presionadas."""
#     return [key_event for key, pressed in enumerate(pg.key.get_pressed()) 
#             if pressed for key_event in key_events_lower_char_list if key_event['scancode'] == key]



def modifiers_key_state(): # MODIFICADORES
    """Retorna una lista con las teclas modificadoras que estan presionadas"""
    list = []
    for valores in key_events_modifier_list:
        mod_valor = valores['mod']
        if pg.key.get_mods() & mod_valor == mod_valor:
            list.append(valores['key'])
    return list

def control_key_state():
    """Devuelve una lista con los nombres de las teclas presionadas."""
    pressed_keys = []
    for key, pressed in enumerate(pg.key.get_pressed()): # los eventos de teclado también dependen de la capacidad del teclado (n-key rollover)
        if pressed:
            key_name = next((event['key'] for event in key_events_control_list if event['scancode'] == key), None)
            if key_name:
                pressed_keys.append(key_name)
    return pressed_keys

def char_key_state(): # CARACTERES
    keys = pg.key.get_pressed()
    pressed_keys = []
    def get_key_name(key_code):
        """Devuelve el nombre o carácter asociado con un código de tecla."""
        for key_event in key_events_lower_char_list:
            if key_event['scancode'] == key_code:
                pressed_keys.append(key_event)
    for key, pressed in enumerate(keys):
        if pressed:
            get_key_name(key)
    return pressed_keys


def event(event_dict):
    #Eventos
    # ----------------------------------------------------------------------------
    event_dict["Mouse"]["Motion"] = None
    event_dict["Mouse"]["ClickLeftDown"] = False
    event_dict["Mouse"]["ClickLeftUp"] = False
    event_dict["Mouse"]["Scroll"] = None

    # Verificar si el mouse se mueve
    current_mouse_pos = pg.mouse.get_pos()
    if event_dict["Mouse"]["Position"] != current_mouse_pos:
        event_dict["Mouse"]["Motion"] = (
            current_mouse_pos[0] - event_dict["Mouse"]["Position"][0],
            current_mouse_pos[1] - event_dict["Mouse"]["Position"][1]
        )
        event_dict["Mouse"]["Position"] = current_mouse_pos
        event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW  # Reinicio icono del mouse

    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        # Eventos de teclas
        elif event.type == pg.KEYDOWN:  # Tecla hacia abajo

            # ESTO ES SOLO PARA MODIFICADORES: por que mod: es la sumatoria de todas las teclas modificadoras
            event_dict["keyPressed"]["Modifiers"] = modifiers_key_state() # modifiers (key)
            
            event_dict["keyPressed"]["Control"] = control_key_state() # control (key)

            event_dict["keyPressed"]["char"] = char_key_state() # char (unicode)
            
            # Obtener los modificadores activos
            if event.key in MODIFIER_KEYS: # modificadores
                pass
                #event_dict["keyPressed"]["Modifiers"].append(event.key)
            elif event.key in allowed_control_keys:
                pass
                #event_dict["keyPressed"]["Control"].append(event.key)
            elif event.unicode in allowed_char["lower"]: 
                pass
                #event_dict["keyPressed"]["char"].append({"unicode": event.unicode})

        elif event.type == pg.KEYUP:  # Tecla hacia arriba

            # ESTO ES SOLO PARA MODIFICADORES: por que mod: es la sumatoria de todas las teclas modificadoras
            event_dict["keyPressed"]["Modifiers"] = modifiers_key_state() # modifiers

            event_dict["keyPressed"]["Control"] = control_key_state() # control

            event_dict["keyPressed"]["char"] = char_key_state() # char

            if event.key in MODIFIER_KEYS: # modificadores
                pass
                #event_dict["keyPressed"]["Modifiers"].remove(event.key)
            elif event.key in allowed_control_keys:
                pass
                #event_dict["keyPressed"]["Control"].remove(event.key)
            elif event.unicode in allowed_char["lower"]: 
                pass
                # event_info = {"unicode": event.unicode}
                # i = event_dict["keyPressed"]["char"].index(event_info)
                # del event_dict["keyPressed"]["char"][i]
        
        


        # Detectar eventos de clic del ratón
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                event_dict["Mouse"]["ClickLeftDown"] = True
                event_dict["Mouse"]["ClickLeftPressed"] = True
        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                event_dict["Mouse"]["ClickLeftUp"] = True
                event_dict["Mouse"]["ClickLeftPressed"] = False

        # scroll del mouse
        if event.type == pg.MOUSEWHEEL:
            event_dict["Mouse"]["Scroll"] = 1 if event.y > 0 else -1
    # ----------------------------------------------------------------------------

MODIFIER_KEYS = {
    pg.K_LSHIFT, pg.K_RSHIFT, pg.K_LCTRL, pg.K_RCTRL,
    pg.K_LALT, pg.K_RALT, pg.K_LMETA, pg.K_RMETA,
    pg.K_CAPSLOCK, pg.K_NUMLOCK, pg.K_SCROLLOCK, pg.K_MODE}

allowed_control_keys = {
                        pg.K_SPACE,       # Espacio
                        pg.K_BACKSPACE,   # Retroceso (Backspace)
                        pg.K_RETURN,      # Enter
                        pg.K_TAB,         # Tabulador
                        pg.K_ESCAPE,      # Escape
                        pg.K_LEFT,        # Flecha izquierda
                        pg.K_RIGHT,       # Flecha derecha
                        pg.K_UP,          # Flecha arriba
                        pg.K_DOWN,        # Flecha abajo
    }
allowed_char = {"lower":['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],

                "upper":['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],

                "number":['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',],

                "signs":['_', '-', '.', ',', '!', '?', '@' , '#' , '$' , '%', '^', '&', '*', '(', ')',
                         '[', ']', '{', '}', ';', ':', '\'', '\"', '\\', '/', '|', '<', '>', '=', '+']
                }


key_events_lower_char_list = [
    {'unicode': 'a', 'key': 97,  'scancode': 4},
    {'unicode': 'b', 'key': 98,  'scancode': 5},
    {'unicode': 'c', 'key': 99,  'scancode': 6},
    {'unicode': 'd', 'key': 100, 'scancode': 7},
    {'unicode': 'e', 'key': 101, 'scancode': 8},
    {'unicode': 'f', 'key': 102, 'scancode': 9},
    {'unicode': 'g', 'key': 103, 'scancode': 10},
    {'unicode': 'h', 'key': 104, 'scancode': 11},
    {'unicode': 'i', 'key': 105, 'scancode': 12},
    {'unicode': 'j', 'key': 106, 'scancode': 13},
    {'unicode': 'k', 'key': 107, 'scancode': 14},
    {'unicode': 'l', 'key': 108, 'scancode': 15},
    {'unicode': 'm', 'key': 109, 'scancode': 16},
    {'unicode': 'n', 'key': 110, 'scancode': 17},
    {'unicode': 'o', 'key': 111, 'scancode': 18},
    {'unicode': 'p', 'key': 112, 'scancode': 19},
    {'unicode': 'q', 'key': 113, 'scancode': 20},
    {'unicode': 'r', 'key': 114, 'scancode': 21},
    {'unicode': 's', 'key': 115, 'scancode': 22},
    {'unicode': 't', 'key': 116, 'scancode': 23},
    {'unicode': 'u', 'key': 117, 'scancode': 24},
    {'unicode': 'v', 'key': 118, 'scancode': 25},
    {'unicode': 'w', 'key': 119, 'scancode': 26},
    {'unicode': 'x', 'key': 120, 'scancode': 27},
    {'unicode': 'y', 'key': 121, 'scancode': 28},
    {'unicode': 'z', 'key': 122, 'scancode': 29},
    {'unicode': 'ñ', 'key': 241, 'scancode': 51},
    {'unicode': '0', 'key': 48,  'scancode': 39},
    {'unicode': '1', 'key': 49,  'scancode': 30},
    {'unicode': '2', 'key': 50,  'scancode': 31},
    {'unicode': '3', 'key': 51,  'scancode': 32},
    {'unicode': '4', 'key': 52,  'scancode': 33},
    {'unicode': '5', 'key': 53,  'scancode': 34},
    {'unicode': '6', 'key': 54,  'scancode': 35},
    {'unicode': '7', 'key': 55,  'scancode': 36},
    {'unicode': '8', 'key': 56,  'scancode': 37},
    {'unicode': '9', 'key': 57,  'scancode': 38},
    {'unicode': "'", 'key': 39,  'scancode': 45},
    {'unicode': '-', 'key': 45,  'scancode': 56},
    {'unicode': '´', 'key': 43,  'scancode': 48},
    {'unicode': ',', 'key': 44,  'scancode': 54},
    {'unicode': '.', 'key': 46,  'scancode': 55},
    {'unicode': '¿', 'key': 191, 'scancode': 46},
    {'unicode': '',  'key': 180, 'scancode': 47},
    {'unicode': '{', 'key': 123, 'scancode': 52},
    {'unicode': '|', 'key': 124, 'scancode': 53},
    {'unicode': '}', 'key': 125, 'scancode': 49},
    {'unicode': '<', 'key': 60,  'scancode': 100},
]


key_events_upper_char_list = [
    {'unicode': 'A', 'key': 97,  'scancode': 4},
    {'unicode': 'B', 'key': 98,  'scancode': 5},
    {'unicode': 'C', 'key': 99,  'scancode': 6},
    {'unicode': 'D', 'key': 100, 'scancode': 7},
    {'unicode': 'E', 'key': 101, 'scancode': 8},
    {'unicode': 'F', 'key': 102, 'scancode': 9},
    {'unicode': 'G', 'key': 103, 'scancode': 10},
    {'unicode': 'H', 'key': 104, 'scancode': 11},
    {'unicode': 'I', 'key': 105, 'scancode': 12},
    {'unicode': 'J', 'key': 106, 'scancode': 13},
    {'unicode': 'K', 'key': 107, 'scancode': 14},
    {'unicode': 'L', 'key': 108, 'scancode': 15},
    {'unicode': 'M', 'key': 109, 'scancode': 16},
    {'unicode': 'N', 'key': 110, 'scancode': 17},
    {'unicode': 'Ñ', 'key': 241, 'scancode': 51},
    {'unicode': 'O', 'key': 111, 'scancode': 18},
    {'unicode': 'P', 'key': 112, 'scancode': 19},
    {'unicode': 'Q', 'key': 113, 'scancode': 20},
    {'unicode': 'R', 'key': 114, 'scancode': 21},
    {'unicode': 'S', 'key': 115, 'scancode': 22},
    {'unicode': 'T', 'key': 116, 'scancode': 23},
    {'unicode': 'U', 'key': 117, 'scancode': 24},
    {'unicode': 'V', 'key': 118, 'scancode': 25},
    {'unicode': 'W', 'key': 119, 'scancode': 26},
    {'unicode': 'X', 'key': 120, 'scancode': 27},
    {'unicode': 'Y', 'key': 121, 'scancode': 28},
    {'unicode': 'Z', 'key': 122, 'scancode': 29},
    {'unicode': '!', 'key': 49,  'scancode': 30},
    {'unicode': '"', 'key': 50,  'scancode': 31},
    {'unicode': '#', 'key': 51,  'scancode': 32},
    {'unicode': '$', 'key': 52,  'scancode': 33},
    {'unicode': '%', 'key': 53,  'scancode': 34},
    {'unicode': '&', 'key': 54,  'scancode': 35},
    {'unicode': '/', 'key': 55,  'scancode': 36},
    {'unicode': '(', 'key': 56,  'scancode': 37},
    {'unicode': ')', 'key': 57,  'scancode': 38},
    {'unicode': '=', 'key': 48,  'scancode': 39},
    {'unicode': '¨', 'key': 43,  'scancode': 48},
    {'unicode': '', 'key': 180,  'scancode': 47},
    {'unicode': '>', 'key': 60,  'scancode': 100},
    {'unicode': '_', 'key': 45,  'scancode': 56},
    {'unicode': ':', 'key': 46,  'scancode': 55},
    {'unicode': ';', 'key': 44,  'scancode': 54},
    {'unicode': '[', 'key': 123, 'scancode': 52},
    {'unicode': ']', 'key': 125, 'scancode': 49},
    {'unicode': '¡', 'key': 191, 'scancode': 46},
    {'unicode': '?', 'key': 39,  'scancode': 45},
    {'unicode': '°', 'key': 124, 'scancode': 53},
]


# Mod: es el estado de las teclas modificadoras EJ: (Bloq Mayus)8192 + (Bloq Num)4096 = 12288




key_events_modifier_list = [  # MODIFICADORES - ('unicode': '')
    {'key': 1073742049, 'mod': 1,   'scancode': 225},  # left Shift
    {'key': 1073742053, 'mod': 2,   'scancode': 229},  # right Shift
    {'key': 1073742048, 'mod': 64,  'scancode': 224},  # left Ctrl
    {'key': 1073742052, 'mod': 128, 'scancode': 228},  # right Ctrl
    {'key': 1073742050, 'mod': 256, 'scancode': 226},  # left Meta
    {'key': 1073742054, 'mod': 576, 'scancode': 230},  # right Alt (Alt Gr)
    {'key': 1073742051, 'mod': 1024,'scancode': 227},  # left Alt
    {'key': 1073741907, 'mod': 4096, 'scancode': 83},  # Bloq Num
    {'key': 1073741881, 'mod': 8192, 'scancode': 57},  # Bloq Mayus
    {'key': 1073741895, 'mod': 32768,'scancode': 71}   # Bloq Despl
]

key_events_control_list = [  # CONTROL - 'mod': 0
    {'unicode': '\x08', 'key': 8,          'scancode': 42},  # Backspace
    {'unicode': '\x1b', 'key': 27,         'scancode': 41},  # Escape
    {'unicode': '\r',   'key': 13,         'scancode': 40},  # Enter
    {'unicode': '\r',   'key': 1073741912, 'scancode': 88},  # Intro
    {'unicode': '\t',   'key': 9,          'scancode': 43},  # Tab
    {'unicode': ' ',    'key': 32,         'scancode': 44},  # Space
    {'unicode': '',     'key': 1073741904, 'scancode': 80},  # Left Arrow
    {'unicode': '',     'key': 1073741903, 'scancode': 79},  # Right Arrow
    {'unicode': '',     'key': 1073741906, 'scancode': 82},  # Up Arrow
    {'unicode': '',     'key': 1073741905, 'scancode': 81}   # Down Arrow
]