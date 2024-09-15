import pygame as pg
import sys



def modifiers_key_state():
    """Retorna una lista con las teclas modificadoras que están presionadas."""
    mods = pg.key.get_mods()
    return [mod_event for mod_event in key_events_modifier_list if mods & mod_event['mod']]

def key_state(keys, key_event_list):
    """Devuelve una lista con los nombres o caracteres de las teclas presionadas."""
    return [event for key, pressed in enumerate(keys) if pressed for event in key_event_list if event['scancode'] == key]


#def event(event_dict, screen, objects_list):
def event(event_dict,engine_window,default_screen_surface):
    """Gestiona y reinicia los eventos"""

    # Reinicio variables
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


    # Bucle de eventos
    # ----------------------------------------------------------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Detectar redimensionamiento de la ventana
        elif event.type == pg.VIDEORESIZE:
            width, height = event.w, event.h

            event_dict["Screen"]["Width"]  = width
            event_dict["Screen"]["Height"] = height

            engine_window.rect.w = 0
            engine_window.rect.h = 0
            engine_window.rects_updates(default_screen_surface,w=width,h=height,force = True)

            #screen = pg.display.set_mode((width, height), pg.RESIZABLE)
            #print(f"Nuevo tamaño de la ventana: {width}x{height}")    

            #for obj in objects_list:
            #    obj.rects_updates(screen, force = True) # DEBERIAMOS PASAR AQUI LA SUPERFICIE DE LA PANTALLA? (COMO PRESURFACE)
            
        # Eventos de teclas
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:  # Tecla hacia abajo o arriba
            # ----------------------------------------------------------------------------
            #TENER EN CUENTA LAS CARACTERÍSTICAS DEL TECLADO AL MOMENTO DE DETECTAR EVENTOS DE TECLAS
            # ----------------------------------------------------------------------------
            
            # Modifiers 
            # ----------------------------------------------------------------------------
            # ESTO ES SOLO PARA MODIFICADORES: por que mod: es la sumatoria de todas las teclas modificadoras
            event_dict["keyPressed"]["Modifiers"] = modifiers_key_state() # modifiers (key)
            # ----------------------------------------------------------------------------
            keys = pg.key.get_pressed()
            # shortcuts 
            # ----------------------------------------------------------------------------
            Ctrl = any(key["key"] in (pg.K_LCTRL, pg.K_RCTRL) for key in event_dict["keyPressed"]["Modifiers"])
            if Ctrl:
                event_dict["keyPressed"]["shortcuts"] = key_state(keys,key_events_shortcutsr_list)
            # ----------------------------------------------------------------------------
            # Control 
            # ----------------------------------------------------------------------------
            char_list = key_events_control_list.copy()
            # if: Bloq_Num 
            if any(key["key"] == 1073741907 for key in event_dict["keyPressed"]["Modifiers"]): # Bloq Num
                char_list.extend([{'unicode': '\r','key': 1073741912, 'scancode': 88}]) # intro
            event_dict["keyPressed"]["Control"] = key_state(keys,char_list) # control (key)
            # ----------------------------------------------------------------------------
            # Char 
            # ----------------------------------------------------------------------------
            shift = any(key["key"] in (1073742049, 1073742053) for key in event_dict["keyPressed"]["Modifiers"])  # Left Shift, Right Shift
            shift ^= any(key["key"] == 1073741881 for key in event_dict["keyPressed"]["Modifiers"])  # Bloq Mayus: shift != shift
            if shift:  char_list = key_events_upper_char_list.copy()
            else: char_list = key_events_lower_char_list.copy()
            if any(key["key"] == pg.K_NUMLOCK for key in event_dict["keyPressed"]["Modifiers"]): # if: Bloq_Num 
                char_list.extend(key_events_numeric_keypad_list)
            # Verificar que caracteres estan en siendo presionados y lo agrego o quito en orden
            char_list_pressed = key_state(keys,char_list) # char (unicode)
            char = event.unicode
            for dic_char in char_list_pressed:
                if char == dic_char["unicode"]:
                    event_dict["keyPressed"]["char"].append(dic_char)
                    break
            else:
                for dic_char in event_dict["keyPressed"]["char"]:
                    if char == dic_char["unicode"]:
                        event_dict["keyPressed"]["char"].remove(dic_char)
                        break
            # ----------------------------------------------------------------------------


        # Detectar eventos de clic del ratón
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                event_dict["Mouse"]["ClickLeftDown"] = True
                event_dict["Mouse"]["ClickLeftPressed"] = True
        
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                event_dict["Mouse"]["ClickLeftUp"] = True
                event_dict["Mouse"]["ClickLeftPressed"] = False

        # scroll del mouse
        if event.type == pg.MOUSEWHEEL:
            event_dict["Mouse"]["Scroll"] = 1 if event.y > 0 else -1
# ----------------------------------------------------------------------------

key_events_shortcutsr_list = [ # ATAJOS DE TECLADO
    {"unicode": '\x03', "key": 99, "scancode": 6},  # Ctrl + c
    {"unicode": '\x16', "key": 118, "scancode": 25} # Ctrl + v
]

key_events_lower_char_list = [
    {'unicode': ' ', 'key': 32,  'scancode': 44},  # Space
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
    {'unicode': '+', 'key': 43,  'scancode': 48},
    {'unicode': ',', 'key': 44,  'scancode': 54},
    {'unicode': '.', 'key': 46,  'scancode': 55},
    {'unicode': '¿', 'key': 191, 'scancode': 46},
    {'unicode': '´',  'key': 180,'scancode': 47},
    {'unicode': '{', 'key': 123, 'scancode': 52},
    {'unicode': '|', 'key': 124, 'scancode': 53},
    {'unicode': '}', 'key': 125, 'scancode': 49},
    {'unicode': '<', 'key': 60,  'scancode': 100}
]

key_events_upper_char_list = [
    {'unicode': ' ', 'key': 32,  'scancode': 44},  # Space
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
    {'unicode': '*', 'key': 43,  'scancode': 48},
    {'unicode': '¨', 'key': 180, 'scancode': 47},
    {'unicode': '>', 'key': 60,  'scancode': 100},
    {'unicode': '_', 'key': 45,  'scancode': 56},
    {'unicode': ':', 'key': 46,  'scancode': 55},
    {'unicode': ';', 'key': 44,  'scancode': 54},
    {'unicode': '[', 'key': 123, 'scancode': 52},
    {'unicode': ']', 'key': 125, 'scancode': 49},
    {'unicode': '¡', 'key': 191, 'scancode': 46},
    {'unicode': '?', 'key': 39,  'scancode': 45},
    {'unicode': '°', 'key': 124, 'scancode': 53},]

key_events_numeric_keypad_list = [
    {'unicode': '0', 'key': 1073741922, 'scancode': 98},
    {'unicode': '1', 'key': 1073741913, 'scancode': 89},
    {'unicode': '2', 'key': 1073741914, 'scancode': 90},
    {'unicode': '3', 'key': 1073741915, 'scancode': 91},
    {'unicode': '4', 'key': 1073741916, 'scancode': 92},
    {'unicode': '5', 'key': 1073741917, 'scancode': 93},
    {'unicode': '6', 'key': 1073741918, 'scancode': 94},
    {'unicode': '7', 'key': 1073741919, 'scancode': 95},
    {'unicode': '8', 'key': 1073741920, 'scancode': 96},
    {'unicode': '9', 'key': 1073741921, 'scancode': 97},
    {'unicode': '/', 'key': 1073741908, 'scancode': 84},
    {'unicode': '*', 'key': 1073741909, 'scancode': 85},
    {'unicode': '-', 'key': 1073741910, 'scancode': 86},
    {'unicode': '+', 'key': 1073741911, 'scancode': 87},
    {'unicode': '.', 'key': 1073741923, 'scancode': 99},
    #{'unicode': '\r','key': 1073741912, 'scancode': 88},  # Intro
]

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
    #{'unicode': '\r',   'key': 1073741912, 'scancode': 88},  # Intro
    {'unicode': '\t',   'key': 9,          'scancode': 43},  # Tab
    #{'unicode': ' ',    'key': 32,         'scancode': 44},  # Space
    {'unicode': '',     'key': 1073741904, 'scancode': 80},  # Left Arrow
    {'unicode': '',     'key': 1073741903, 'scancode': 79},  # Right Arrow
    {'unicode': '',     'key': 1073741906, 'scancode': 82},  # Up Arrow
    {'unicode': '',     'key': 1073741905, 'scancode': 81},  # Down Arrow
    {'unicode': '\x7f', 'key': 127,        'scancode': 76}   # suprimir
]

# pg_key_list1 = [
#     pg.K_LSHIFT,    # 1073742049, left Shift
#     pg.K_RSHIFT,    # 1073742053, right Shift
#     pg.K_LCTRL,     # 1073742048, left Ctrl
#     pg.K_RCTRL,     # 1073742052, right Ctrl
#     pg.K_LMETA,     # 1073742050, left Meta
#     pg.K_RALT,      # 1073742054, right Alt (Alt Gr)
#     pg.K_LALT,      # 1073742051, left Alt
#     pg.K_NUMLOCK,   # 1073741907, Bloq Num
#     pg.K_CAPSLOCK,  # 1073741881, Bloq Mayus
#     pg.K_SCROLLLOCK # 1073741895, Bloq Despl
# ]

# pg_key_control_list1 = [
#     pg.K_BACKSPACE,  # 8, Backspace
#     pg.K_ESCAPE,     # 27, Escape
#     pg.K_RETURN,     # 13, Enter
#     pg.K_KP_ENTER,   # 1073741912, Intro (teclado numérico)
#     pg.K_TAB,        # 9, Tab
#     pg.K_SPACE,      # 32, Space
#     pg.K_LEFT,       # 1073741904, Left Arrow
#     pg.K_RIGHT,      # 1073741903, Right Arrow
#     pg.K_UP,         # 1073741906, Up Arrow
#     pg.K_DOWN        # 1073741905, Down Arrow
# ]

# pg_key_list1 = [
#     pg.K_a,    # 97
#     pg.K_b,    # 98
#     pg.K_c,    # 99
#     pg.K_d,    # 100
#     pg.K_e,    # 101
#     pg.K_f,    # 102
#     pg.K_g,    # 103
#     pg.K_h,    # 104
#     pg.K_i,    # 105
#     pg.K_j,    # 106
#     pg.K_k,    # 107
#     pg.K_l,    # 108
#     pg.K_m,    # 109
#     pg.K_n,    # 110
#     pg.K_o,    # 111
#     pg.K_p,    # 112
#     pg.K_q,    # 113
#     pg.K_r,    # 114
#     pg.K_s,    # 115
#     pg.K_t,    # 116
#     pg.K_u,    # 117
#     pg.K_v,    # 118
#     pg.K_w,    # 119
#     pg.K_x,    # 120
#     pg.K_y,    # 121
#     pg.K_z,    # 122
#     #pg.K_ñ,    # 241
#     pg.K_0,    # 48
#     pg.K_1,    # 49
#     pg.K_2,    # 50
#     pg.K_3,    # 51
#     pg.K_4,    # 52
#     pg.K_5,    # 53
#     pg.K_6,    # 54
#     pg.K_7,    # 55
#     pg.K_8,    # 56
#     pg.K_9,    # 57
#     pg.K_QUOTE,    # 39
#     pg.K_MINUS,    # 45
#     #pg.K_ACUTE,    # 43 (correspondiente a la tecla '´')
#     pg.K_COMMA,    # 44
#     pg.K_PERIOD,   # 46
#     pg.K_SLASH,    # 191 (correspondiente a la tecla '¿')
#     #pg.K_GRAVE,    # 180 (tecla sin unicode en la lista)
#     #pg.K_LEFTBRACE,    # 123 (correspondiente a la tecla '{')
#     pg.K_BACKSLASH,    # 124 (correspondiente a la tecla '|')
#     #pg.K_RIGHTBRACE,   # 125 (correspondiente a la tecla '}')
#     pg.K_LESS,    # 60 (correspondiente a la tecla '<')
# ]

# pg_key_upper_char_list1 = [
#     pg.K_a,  # 97, A
#     pg.K_b,  # 98, B
#     pg.K_c,  # 99, C
#     pg.K_d,  # 100, D
#     pg.K_e,  # 101, E
#     pg.K_f,  # 102, F
#     pg.K_g,  # 103, G
#     pg.K_h,  # 104, H
#     pg.K_i,  # 105, I
#     pg.K_j,  # 106, J
#     pg.K_k,  # 107, K
#     pg.K_l,  # 108, L
#     pg.K_m,  # 109, M
#     pg.K_n,  # 110, N
#     # pg.K_UNKNOWN para Ñ (no existe pg.K_ñ)
#     pg.K_o,  # 111, O
#     pg.K_p,  # 112, P
#     pg.K_q,  # 113, Q
#     pg.K_r,  # 114, R
#     pg.K_s,  # 115, S
#     pg.K_t,  # 116, T
#     pg.K_u,  # 117, U
#     pg.K_v,  # 118, V
#     pg.K_w,  # 119, W
#     pg.K_x,  # 120, X
#     pg.K_y,  # 121, Y
#     pg.K_z,  # 122, Z
#     pg.K_1,  # 49, !
#     pg.K_2,  # 50, "
#     pg.K_3,  # 51, #
#     pg.K_4,  # 52, $
#     pg.K_5,  # 53, %
#     pg.K_6,  # 54, &
#     pg.K_7,  # 55, /
#     pg.K_8,  # 56, (
#     pg.K_9,  # 57, )
#     pg.K_0,  # 48, =
#     # pg.K_UNKNOWN para ¨ (no existe pg.K correspondiente)
#     # pg.K_UNKNOWN para ´ (no existe pg.K correspondiente)
#     # pg.K_UNKNOWN para > (no existe pg.K correspondiente)
#     # pg.K_MINUS para _ (generalmente - y _ están en la misma tecla)
#     pg.K_PERIOD,  # 46, :
#     pg.K_COMMA,  # 44, ;
#     # pg.K_UNKNOWN para [ (no existe pg.K correspondiente)
#     # pg.K_UNKNOWN para ] (no existe pg.K correspondiente)
#     pg.K_SLASH,  # 191, ¡
#     pg.K_QUOTE,  # 39, ?
#     # pg.K_UNKNOWN para ° (no existe pg.K correspondiente)
# ]
