import sys
import pygame as pg
import time
import os # crear carpetas, archivos ect..

from Folder_classes.utility_classes import Font # fuentes (string a surface)
import traceback

# Inicializar Pygame
pg.init()

# Configurar la pantalla
width, height = 800, 600
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption("Roar!!")



# path to the Motor Roar
#-----------------------------------------------------------------------------
motor_game_folder_path = "C:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar"
#-----------------------------------------------------------------------------



# ruta al escritorio y creo carpeta
#C:\Users\Usuario\Desktop
#-----------------------------------------------------------------------------
desktop_path = os.path.join(os.path.expanduser('~'),'Desktop')

os.chdir(desktop_path) # nos mueve a la hubicacion de la ruta
if not(os.path.exists("Videojuego_00")): # existe carpeta
    os.mkdir("Videojuego_00") # crea carpetas

game_folder_path = os.path.join(desktop_path,"Videojuego_00") # ruta a la carpeta del juego
#-----------------------------------------------------------------------------



# observer para la carpeta del juego "Videojuego_00"
# --------------------------------------------------------------------------
from Folder_classes import detection_archive_delate
detection_archive_delate.monitorear_carpeta(game_folder_path)
# --------------------------------------------------------------------------


# FPS
# --------------------------------------------------------------------------
# Inicializar el reloj
clock = pg.time.Clock()
fps_text = Font().surf_font(str(int(clock.get_fps())), (250, 250, 250))
# --------------------------------------------------------------------------



# diccionario de eventos
#-----------------------------------------------------------------------------
# Diccionario de eventos
event_dict = {
    "MotorGameFolderpPath": motor_game_folder_path,
    "GameFolderpPath": game_folder_path,
    #"screen":{"width":width, "height":height},
    "FPS":{"Fixed":60,
           "Real":None,
           "delta_time":None},
    "Colors":{"DarkGrey":(5, 5, 5),
              "IntermediumGrey":(40, 40, 40),
              "LightGrey":(90, 90, 90),
              "GreenFluor":(204,255,0)},
    #"keyPressed": [],

    "keyPressed":{"char": [], 
                  "Control": [], 
                  "Modifiers":[]},

    # "keyPressed":{"chars": {"Char":[],
    #                         "Number":[],
    #                         "Signs":[]}, 
    #               "Control": [], 
    #               "Modifiers":[]},

    "Mouse":{"Motion":False,
             "Position":(0,0),
             "ClickLeftDown": False,
             "ClickLeftPressed": False,
             "ClickLeftUp": False,
             "Scroll": None,
             "Icon":pg.SYSTEM_CURSOR_ARROW},
    "EditableObjects": {"selected":[],
                        "clickable":[]},
    "depth_number": -1,
    "Delate_List" : [],
}
#-----------------------------------------------------------------------------



depth_number = event_dict["depth_number"]

objects_list = [] # lista de objetos en GameEditor(los objetos deben contener un "rect")


# window2
from Folder_classes.windows import Window
window = Window(event_dict,screen,350,80,300,450,500,500,1)
objects_list.append(window) # agregamos el objeto window a la lista

from Objects_creator import ObjectsCreator
# # window2
objects_creator_window = ObjectsCreator(event_dict,screen,0,80,300,450,500,500,1)
objects_list.append(objects_creator_window) # agregamos el objeto window a la lista




# Crear un diccionario de modificadores
MODIFIERS = {
    pg.KMOD_NONE: "No Modifiers", # No hay modificadores activos.
    pg.KMOD_LSHIFT: "Left Shift", # Shift izquierdo.
    pg.KMOD_RSHIFT: "Right Shift",# Shift derecho.
    pg.KMOD_LCTRL: "Left Ctrl",   # Control izquierdo
    pg.KMOD_RCTRL: "Right Ctrl",  # Control derecho.
    pg.KMOD_LALT: "Left Alt",     # Alt izquierdo.
    pg.KMOD_RALT: "Right Alt",    # Alt derecho.
    #pg.KMOD_LMETA: "Left Meta",   # Meta izquierdo. En algunos sistemas, esta es la tecla de Windows
    #pg.KMOD_RMETA: "Right Meta",  # Meta derecho. En algunos sistemas, esta es la tecla de Windows
    pg.KMOD_NUM: "Num Lock",      # Teclado numérico activado
    pg.KMOD_CAPS: "Caps Lock",    # Bloqueo de mayúsculas activado.
    pg.KMOD_MODE: "Mode"          # Modificador de modo. Este es un modificador adicional utilizado en algunos teclados y sistemas, menos común que los anteriores.
}
def update_modifiers():
    mods = pg.key.get_mods()
    event_dict["keyPressed"]["Modifiers"].clear()
    for mod_code, mod_name in MODIFIERS.items():
        if mods & mod_code:
            event_dict["keyPressed"]["Modifiers"].append(mod_name)



MODIFIER_KEYS = {
    pg.K_LSHIFT, pg.K_RSHIFT, pg.K_LCTRL, pg.K_RCTRL,
    pg.K_LALT, pg.K_RALT, pg.K_LMETA, pg.K_RMETA,
    pg.K_CAPSLOCK, pg.K_NUMLOCK, pg.K_SCROLLOCK, pg.K_MODE
}

# allowed_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
#                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
#                 # 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
#                 # 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
#                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]

allowed_char = {"lower":['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],

                "upper":['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],

                "number":['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',],

                "signs":['_', '-', '.', ',', '!', '?', '@' , '#' , '$' , '%', '^', '&', '*', '(', ')',
                         '[', ']', '{', '}', ';', ':', '\'', '\"', '\\', '/', '|', '<', '>', '=', '+']
                }


shift_chars = ["!", "\"", "#", "$", "%", "&", "/", "(", ")", "=", "°", "?", "¡", "]", "¨", "[", ";", ":", "_", ">", "*", "@", "{", "}", "|", "~", "^",
               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

no_shift_chars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "|", "'", "¿", "}", "´", "{", ",", ".", "-", "<", "+",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]



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


import pygame as pg

# Mapeo de teclas a caracteres sin Shift
# KEY_MAP = {
#     pg.K_a: 'a', pg.K_b: 'b', pg.K_c: 'c', pg.K_d: 'd', pg.K_e: 'e',
#     pg.K_f: 'f', pg.K_g: 'g', pg.K_h: 'h', pg.K_i: 'i', pg.K_j: 'j',
#     pg.K_k: 'k', pg.K_l: 'l', pg.K_m: 'm', pg.K_n: 'n', pg.K_o: 'o',
#     pg.K_p: 'p', pg.K_q: 'q', pg.K_r: 'r', pg.K_s: 's', pg.K_t: 't',
#     pg.K_u: 'u', pg.K_v: 'v', pg.K_w: 'w', pg.K_x: 'x', pg.K_y: 'y',
#     pg.K_z: 'z',
#     pg.K_0: '0', pg.K_1: '1', pg.K_2: '2', pg.K_3: '3', pg.K_4: '4',
#     pg.K_5: '5', pg.K_6: '6', pg.K_7: '7', pg.K_8: '8', pg.K_9: '9',
#     pg.K_SPACE: ' ', pg.K_RETURN: '\n', pg.K_BACKSPACE: 'Backspace',
#     pg.K_TAB: 'Tab', pg.K_ESCAPE: 'Escape', pg.K_MINUS: '-', pg.K_EQUALS: '=',
#     pg.K_LEFTBRACKET: '[', pg.K_RIGHTBRACKET: ']', pg.K_BACKSLASH: '\\',
#     pg.K_SEMICOLON: ';', pg.K_QUOTE: '\'', pg.K_BACKQUOTE: '`',
#     pg.K_COMMA: ',', pg.K_PERIOD: '.', pg.K_SLASH: '/',
#     pg.K_CAPSLOCK: 'Caps Lock', pg.K_F1: 'F1', pg.K_F2: 'F2',
#     225: 'AltGr', 33: '!', 30: 'a', 23: 'h', 11: '0', 10: '9', 5: '4', 17: 'w'
# }
KEY_MAP = {
    4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i',
    13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q',
    21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
    29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7',
    37: '8', 38: '9', 39: '0', 44: " ", 45: '\'',46: '¿', 47: '´', 48: '+', 49: '}', 51: 'ñ',
    52: '{', 53: '|', 54: ',', 55: '.', 56: '-' ,100: '<'
}

KEY_MAP_MAYUS = {
    4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I',
    13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q',
    21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
    29: 'Z', 30: '!', 31: '"', 32: '#', 33: '$', 34: '%', 35: '&', 36: '/',
    37: '()', 38: ')', 39: '=', 44: " ", 45: '?', 46: '¡', 47: '¨', 48: '*', 49: ']', 51: 'Ñ',
    52: '[]', 53: '°', 54: ';', 55: ':', 56: '_', 100: '>'
}

numeric_keypad = {89: '1', 90: '2', 91: '3', 92: '4', 93: '5', 94: '6', 95: '7',
                  96: '8', 97: '9', 98: '0', 100: '<',84: '/', 85: '*', 86: '-',
                  87: '+', 99: '.'}

modifier_key = {
    57: 'Caps Lock',          # Bloqueo de mayúsculas
    83: 'Bloq Num',           # Bloqueo de teclado numerico
    225: 'Left Shift',        # Shift izquierdo
    224: 'Left Ctrl',         # Control izquierdo
    227: 'Left Meta',         # Meta izquierdo (en algunos sistemas, tecla de Windows)
    226: 'Left Alt',          # Alt izquierdo
    228: 'Right Ctrl',        # Control derecho
    229: 'Right Shift',       # Shift derecho
    230: 'AltGr',             # AltGr
    101: 'Right Meta'         # Meta derecho
}

control_key = {
    40: 'Enter',      # Tecla Enter
    42: 'Delete',     # Tecla Suprimir
    41: 'Escape',     # Tecla Escape
    88: 'Intro',      # Tecla Intro
    76: 'Suprimir',   # Tecla Suprimir
    43: 'Tabulador'   # Tecla Tabulador
}

key_events_alpha = [
    # Mod: 1 --> necesita Shift - Mod:0 --> No necesita Shift
    {'unicode': 'a', 'key': 97, 'mod': 0, 'scancode': 4},
    {'unicode': 'b', 'key': 98, 'mod': 0, 'scancode': 5},
    {'unicode': 'c', 'key': 99, 'mod': 0, 'scancode': 6},
    {'unicode': 'd', 'key': 100, 'mod': 0, 'scancode': 7},
    {'unicode': 'e', 'key': 101, 'mod': 0, 'scancode': 8},
    {'unicode': 'f', 'key': 102, 'mod': 0, 'scancode': 9},
    {'unicode': 'g', 'key': 103, 'mod': 0, 'scancode': 10},
    {'unicode': 'h', 'key': 104, 'mod': 0, 'scancode': 11},
    {'unicode': 'i', 'key': 105, 'mod': 0, 'scancode': 12},
    {'unicode': 'j', 'key': 106, 'mod': 0, 'scancode': 13},
    {'unicode': 'k', 'key': 107, 'mod': 0, 'scancode': 14},
    {'unicode': 'l', 'key': 108, 'mod': 0, 'scancode': 15},
    {'unicode': 'm', 'key': 109, 'mod': 0, 'scancode': 16},
    {'unicode': 'n', 'key': 110, 'mod': 0, 'scancode': 17},
    {'unicode': 'o', 'key': 111, 'mod': 0, 'scancode': 18},
    {'unicode': 'p', 'key': 112, 'mod': 0, 'scancode': 19},
    {'unicode': 'q', 'key': 113, 'mod': 0, 'scancode': 20},
    {'unicode': 'r', 'key': 114, 'mod': 0, 'scancode': 21},
    {'unicode': 's', 'key': 115, 'mod': 0, 'scancode': 22},
    {'unicode': 't', 'key': 116, 'mod': 0, 'scancode': 23},
    {'unicode': 'u', 'key': 117, 'mod': 0, 'scancode': 24},
    {'unicode': 'v', 'key': 118, 'mod': 0, 'scancode': 25},
    {'unicode': 'w', 'key': 119, 'mod': 0, 'scancode': 26},
    {'unicode': 'x', 'key': 120, 'mod': 0, 'scancode': 27},
    {'unicode': 'y', 'key': 121, 'mod': 0, 'scancode': 28},
    {'unicode': 'z', 'key': 122, 'mod': 0, 'scancode': 29},
    {'unicode': 'ñ', 'key': 241, 'mod': 0, 'scancode': 51},

    {'unicode': '0', 'key': 48, 'mod': 0, 'scancode': 39},
    {'unicode': '1', 'key': 49, 'mod': 0, 'scancode': 30},
    {'unicode': '2', 'key': 50, 'mod': 0, 'scancode': 31},
    {'unicode': '3', 'key': 51, 'mod': 0, 'scancode': 32},
    {'unicode': '4', 'key': 52, 'mod': 0, 'scancode': 33},
    {'unicode': '5', 'key': 53, 'mod': 0, 'scancode': 34},
    {'unicode': '6', 'key': 54, 'mod': 0, 'scancode': 35},
    {'unicode': '7', 'key': 55, 'mod': 0, 'scancode': 36},
    {'unicode': '8', 'key': 56, 'mod': 0, 'scancode': 37},
    {'unicode': '9', 'key': 57, 'mod': 0, 'scancode': 38},

    {'unicode': "'", 'key': 39, 'mod': 0, 'scancode': 45},
    {'unicode': '-', 'key': 45, 'mod': 0, 'scancode': 56},
    {'unicode': '´', 'key': 43, 'mod': 0, 'scancode': 48},
    {'unicode': ',', 'key': 44, 'mod': 0, 'scancode': 54},
    {'unicode': '.', 'key': 46, 'mod': 0, 'scancode': 55},
    {'unicode': '¿', 'key': 191, 'mod': 0, 'scancode': 46},
    {'unicode': '', 'key': 180, 'mod': 0, 'scancode': 47},
    {'unicode': '{', 'key': 123, 'mod': 0, 'scancode': 52},
    {'unicode': '|', 'key': 124, 'mod': 0, 'scancode': 53},
    {'unicode': '}', 'key': 125, 'mod': 0, 'scancode': 49},
    {'unicode': '<', 'key': 60, 'mod': 0, 'scancode': 100},
    
    {'unicode': 'A', 'key': 97, 'mod': 1, 'scancode': 4},
    {'unicode': 'B', 'key': 98, 'mod': 1, 'scancode': 5},
    {'unicode': 'C', 'key': 99, 'mod': 1, 'scancode': 6},
    {'unicode': 'D', 'key': 100, 'mod': 1, 'scancode': 7},
    {'unicode': 'E', 'key': 101, 'mod': 1, 'scancode': 8},
    {'unicode': 'F', 'key': 102, 'mod': 1, 'scancode': 9},
    {'unicode': 'G', 'key': 103, 'mod': 1, 'scancode': 10},
    {'unicode': 'H', 'key': 104, 'mod': 1, 'scancode': 11},
    {'unicode': 'I', 'key': 105, 'mod': 1, 'scancode': 12},
    {'unicode': 'J', 'key': 106, 'mod': 1, 'scancode': 13},
    {'unicode': 'K', 'key': 107, 'mod': 1, 'scancode': 14},
    {'unicode': 'L', 'key': 108, 'mod': 1, 'scancode': 15},
    {'unicode': 'M', 'key': 109, 'mod': 1, 'scancode': 16},
    {'unicode': 'N', 'key': 110, 'mod': 1, 'scancode': 17},
    {'unicode': 'Ñ', 'key': 241, 'mod': 1, 'scancode': 51},
    {'unicode': 'O', 'key': 111, 'mod': 1, 'scancode': 18},
    {'unicode': 'P', 'key': 112, 'mod': 1, 'scancode': 19},
    {'unicode': 'Q', 'key': 113, 'mod': 1, 'scancode': 20},
    {'unicode': 'R', 'key': 114, 'mod': 1, 'scancode': 21},
    {'unicode': 'S', 'key': 115, 'mod': 1, 'scancode': 22},
    {'unicode': 'T', 'key': 116, 'mod': 1, 'scancode': 23},
    {'unicode': 'U', 'key': 117, 'mod': 1, 'scancode': 24},
    {'unicode': 'V', 'key': 118, 'mod': 1, 'scancode': 25},
    {'unicode': 'W', 'key': 119, 'mod': 1, 'scancode': 26},
    {'unicode': 'X', 'key': 120, 'mod': 1, 'scancode': 27},
    {'unicode': 'Y', 'key': 121, 'mod': 1, 'scancode': 28},
    {'unicode': 'Z', 'key': 122, 'mod': 1, 'scancode': 29},

    {'unicode': '!', 'key': 49, 'mod': 1, 'scancode': 30},
    {'unicode': '"', 'key': 50, 'mod': 1, 'scancode': 31},
    {'unicode': '#', 'key': 51, 'mod': 1, 'scancode': 32},
    {'unicode': '$', 'key': 52, 'mod': 1, 'scancode': 33},
    {'unicode': '%', 'key': 53, 'mod': 1, 'scancode': 34},
    {'unicode': '&', 'key': 54, 'mod': 1, 'scancode': 35},
    {'unicode': '/', 'key': 55, 'mod': 1, 'scancode': 36},
    {'unicode': '(', 'key': 56, 'mod': 1, 'scancode': 37},
    {'unicode': ')', 'key': 57, 'mod': 1, 'scancode': 38},
    {'unicode': '=', 'key': 48, 'mod': 1, 'scancode': 39},
    {'unicode': '¨', 'key': 43, 'mod': 1, 'scancode': 48},
    {'unicode': '', 'key': 180, 'mod': 1, 'scancode': 47},
    {'unicode': '>', 'key': 60, 'mod': 1, 'scancode': 100},
    {'unicode': '_', 'key': 45, 'mod': 1, 'scancode': 56},
    {'unicode': ':', 'key': 46, 'mod': 1, 'scancode': 55},
    {'unicode': ';', 'key': 44, 'mod': 1, 'scancode': 54},
    {'unicode': '[', 'key': 123, 'mod': 1, 'scancode': 52},
    {'unicode': ']', 'key': 125, 'mod': 1, 'scancode': 49},
    {'unicode': '¡', 'key': 191, 'mod': 1, 'scancode': 46},
    {'unicode': '?', 'key': 39, 'mod': 1, 'scancode': 45},
    {'unicode': '°', 'key': 124, 'mod': 1, 'scancode': 53}, 

    {'unicode': '\x08', 'key': 8, 'mod': 0, 'scancode': 42},  # Backspace
    {'unicode': '\x1b', 'key': 27, 'mod': 0, 'scancode': 41}, # Escape
    {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 40},   # Enter
    {'unicode': '\t', 'key': 9, 'mod': 0, 'scancode': 43},    # Tab
    {'unicode': ' ', 'key': 32, 'mod': 0, 'scancode': 44},    # Space
    {'unicode': '', 'key': 1073741904, 'mod': 0, 'scancode': 80}, # Left Arrow
    {'unicode': '', 'key': 1073741903, 'mod': 0, 'scancode': 79}, # Right Arrow
    {'unicode': '', 'key': 1073741906, 'mod': 0, 'scancode': 82}, # Up Arrow
    {'unicode': '', 'key': 1073741905, 'mod': 0, 'scancode': 81}  # Down Arrow
]

# Mod: es el estado de las teclas modificadoras EJ: (Bloq Mayus)8192 + (Bloq Num)4096 = 12288

key_events_special = { # MODIFICADORES
    "left Shift":  {'unicode': '', 'key': 1073742049, 'mod': 1,   'scancode': 225},
    "right Shift": {'unicode': '', 'key': 1073742053, 'mod': 2,   'scancode': 229},
    "left Ctrl":   {'unicode': '', 'key': 1073742048, 'mod': 64,  'scancode': 224},
    "right Ctrl":  {'unicode': '', 'key': 1073742052, 'mod': 128, 'scancode': 228},
    "left Meta":   {'unicode': '', 'key': 1073742050, 'mod': 256, 'scancode': 226},
    "Alt Gr":      {'unicode': '', 'key': 1073742054, 'mod': 576, 'scancode': 230}, # mod = 512 + 64 - (left Ctrl + right Alt)
    "left Alt":    {'unicode': '', 'key': 1073742051, 'mod': 1024,'scancode': 227},
    "Bloq Num":    {'unicode': '', 'key': 1073741907, 'mod': 4096, 'scancode': 83},
    "Bloq Mayus":  {'unicode': '', 'key': 1073741881, 'mod': 8192, 'scancode': 57},
    "Bloq Despl":  {'unicode': '', 'key': 1073741895, 'mod': 32768,'scancode': 71} 
    }






def update_key_state():
    keys = pg.key.get_pressed()
    def get_key_name(key_code):
        """Devuelve el nombre o carácter asociado con un código de tecla."""
        return KEY_MAP.get(key_code, 'Unknown Key')
    pressed_keys = {key: get_key_name(key) for key, pressed in enumerate(keys) if pressed}
    return pressed_keys

#def update_key_state():
#    keys = pg.key.get_pressed()
#    return {key: KEY_MAP.get(key, 'Unknown Key') for key, pressed in enumerate(keys) if pressed}



# Bucle principal
while True:

    try: # capturo errores 

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

                # pressed_keys = update_key_state()
                # for key_code in pressed_keys:
                #     print(f"Key Code: {key_code}, Key Name: {pressed_keys[key_code]}")
                print(event)
                
                # Depuración de códigos de teclas no mapeados
                #if event.key not in KEY_MAP:
                #    print(f"Unmapped Key Code: {event.key}")
                

                # Obtener los modificadores activos
                if event.key in MODIFIER_KEYS: # modificadores

                    event_dict["keyPressed"]["Modifiers"].append(event.key)

                elif event.key in allowed_control_keys:

                    event_dict["keyPressed"]["Control"].append(event.key)

                elif event.unicode in allowed_char["lower"]: 

                    event_dict["keyPressed"]["char"].append({"unicode": event.unicode})

            elif event.type == pg.KEYUP:  # Tecla hacia arriba

                if event.key in MODIFIER_KEYS: # modificadores

                    event_dict["keyPressed"]["Modifiers"].remove(event.key)

                elif event.key in allowed_control_keys:

                    event_dict["keyPressed"]["Control"].remove(event.key)

                elif event.unicode in allowed_char["lower"]: 
                    
                    event_info = {"unicode": event.unicode}

                    i = event_dict["keyPressed"]["char"].index(event_info)
                    del event_dict["keyPressed"]["char"][i]
            
            


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

        #print(event_dict["keyPressed"]["Modifiers"])
        pressed_keys = update_key_state()
        i = []
        for key_code in pressed_keys:
            i.append(pressed_keys[key_code])
            #print(f"Key Code: {key_code}, Key Name: {pressed_keys[key_code]}")
        #print(i)

        # Obtener posición del mouse
        # ----------------------------------------------------------------------------
        x,y = event_dict["Mouse"]["Position"]
        # ----------------------------------------------------------------------------
        

        # Detectar colisión con objetos dentro de la lista objects_list
        # ----------------------------------------------------------------------------
        if (event_dict["Mouse"]["Motion"] and not event_dict["Mouse"]["ClickLeftPressed"]) or event_dict["Mouse"]["ClickLeftUp"]:
            # Limpiar la lista de clickeables a partir del índice depth_number+1
            #event_dict["EditableObjects"]["clickable"] = event_dict["EditableObjects"]["clickable"][:depth_number + 1]
            # verifica donde esta el mouse y los objetos que colisionan con el 
            # ----------------------------------------------------------------------------
            save_clickable_list = event_dict["EditableObjects"]["clickable"].copy()
            del event_dict["EditableObjects"]["clickable"][depth_number+1:]
            # Detectar colisión con objetos
            for obj in objects_list:
                if obj.rect.collidepoint(x, y):
                    obj.collision_detector(event_dict)
                    if event_dict["EditableObjects"]["clickable"]: break
            # ----------------------------------------------------------------------------
            # si el mouse cambio de objetos ejecuto cambios pre o pos de los objetos en las listas 
            # ----------------------------------------------------------------------------
            if save_clickable_list != event_dict["EditableObjects"]["clickable"]:

                def pre_pos_methods(list, prefix, event_dict, code):
                    """Ejecuta métodos con el prefijo dado para cada objeto en la lista."""
                    for obj_func in list:
                        if not(obj_func in event_dict["EditableObjects"]["selected"]): # si es "selected" no entrar a "clickable"
                            try:
                                obj = obj_func.__self__  # desvincula el objeto 
                                func = obj_func.__func__  # desvincula el método
                                method_name = f"{prefix}{func.__name__}"
                                method_to_call = getattr(obj, method_name, None)
                                if callable(method_to_call):
                                    method_to_call(event_dict, code)
                            except Exception as e:
                                print(e)

                # Ejecutar métodos pos_ para objetos clickados
                pre_pos_methods(save_clickable_list,"pos_", event_dict, code = "clickable")
                # Ejecutar métodos pre_ para objetos clickados
                pre_pos_methods(event_dict["EditableObjects"]["clickable"],"pre_", event_dict, code = "clickable")
            # ----------------------------------------------------------------------------
        # ----------------------------------------------------------------------------
        # Si se hace clic izquierdo, copiar lista clickeable a lista seleccionada
        # ----------------------------------------------------------------------------
        elif event_dict["Mouse"]["ClickLeftDown"]:
            if event_dict["EditableObjects"]["selected"] != event_dict["EditableObjects"]["clickable"]:
                def pre_pos_methods(list, prefix, event_dict, code):

                    """Ejecuta métodos con el prefijo dado para cada objeto en la lista."""
                    for obj_func in list:
                        try:
                            obj = obj_func.__self__  # desvincula el objeto 
                            func = obj_func.__func__  # desvincula el método
                            method_name = f"{prefix}{func.__name__}"
                            method_to_call = getattr(obj, method_name, None)
                            if callable(method_to_call):
                                method_to_call(event_dict, code)
                        except Exception as e:
                            print(e)
                # Ejecutar métodos pos_ para objetos seleccionados

                pre_pos_methods(event_dict["EditableObjects"]["selected"],"pos_", event_dict, code = "selected")
                # Actualizar listas de seleccionados y clickeables
                event_dict["EditableObjects"]["selected"] = event_dict["EditableObjects"]["clickable"].copy()
                event_dict["EditableObjects"]["clickable"].clear()
                # Ejecutar métodos pre_ para objetos seleccionados
                pre_pos_methods(event_dict["EditableObjects"]["selected"],"pre_", event_dict, code = "selected")
        # ----------------------------------------------------------------------------

            
        # ----------------------------------------------------------------------------
        # ejecuto objetos de lista selected
        # ----------------------------------------------------------------------------
        exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= depth_number+1 
        if exists_next_clickable_list:
            event_dict["EditableObjects"]["clickable"][depth_number+1](event_dict, code = "clickable") 

        exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= depth_number+1 
        if exists_next_selected_list:
            event_dict["EditableObjects"]["selected"][depth_number+1](event_dict, code = "selected") 

        # ----------------------------------------------------------------------------


        #print(event_dict["EditableObjects"]["clickable"])
        #print(event_dict["EditableObjects"]["selected"])
        #print(event_dict["Delate_List"])
        #print(object_list)


        # Delate objects from object_list
        if event_dict["Delate_List"]:
            for obj in event_dict["Delate_List"]:
                if obj in objects_list:
                    objects_list.remove(obj)
            event_dict["Delate_List"].clear()
        #Draw
        # ----------------------------------------------------------------------------

        #Modificar icono del mouse
        # ----------------------------------------------------------------------------
        if pg.mouse.get_cursor()[0] != event_dict["Mouse"]["Icon"]: # si es distinto, cambio
            pg.mouse.set_cursor(event_dict["Mouse"]["Icon"])
        # ----------------------------------------------------------------------------
        
        # Dibuja el fondo
        screen.fill((50,50,50)) # limpia escena 

        # FPS
        # ----------------------------------------------------------------------------
        fps_text = Font().surf_font(str(int(clock.get_fps())), (250, 250, 250))
        screen.blit(fps_text, (width - fps_text.get_width() - 15,height - fps_text.get_height() -10)) # fps
        # ----------------------------------------------------------------------------
        
        #TRATAR DE DIBUJAR SOLO UNA VEZ Y ACTUALIZAR!!
        if objects_list:
            for obj in objects_list:
                obj.draw(event_dict)


        # Actualiza la pantalla
        pg.display.flip()
        # ----------------------------------------------------------------------------

        # Limitar a 60 FPS
        # ----------------------------------------------------------------------------
        clock.tick(event_dict["FPS"]["Fixed"])
        event_dict["FPS"]["Real"] = clock.get_fps()
        event_dict["FPS"]["delta_time"] = clock.get_time() / 1000 # Calcular tiempo transcurrido
        # ----------------------------------------------------------------------------


    except Exception as e:
        #print(f"Error: {e}")
        # Capturar y mostrar el traceback
        tb = traceback.format_exc()
        print(tb)
