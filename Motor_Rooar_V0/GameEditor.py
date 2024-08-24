import sys
import pygame as pg
import time
import os # crear carpetas, archivos ect..

from Folder_classes.utility_classes import Font # fuentes (string a surface)
import traceback

from Events import Events # eventos

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


def update_modifiers_key_state(): # MODIFICADORES
    #event_dict["keyPressed"]["Modifiers"].clear()
    list = []
    for valores in key_events_modifier_list:
        mod_valor = valores['mod']
        if pg.key.get_mods() & mod_valor == mod_valor:
            list.append(valores['key'])
            #event_dict["keyPressed"]["Modifiers"].append(valores['key'])
    #print(list)
    return list

def update_control_key_state(): # CONTROL
    keys = pg.key.get_pressed()
    def get_key_name(key_code):
        """Devuelve el nombre o carácter asociado con un código de tecla."""
        for key_event in key_events_control_list:
            if key_event['scancode'] == key_code:
                return key_event['key']
        return 'Unknown Key'
    pressed_keys = {key: get_key_name(key) for key, pressed in enumerate(keys) if pressed}
    #print(pressed_keys)
    return pressed_keys

def update_char_key_state(): # CARACTERES
    keys = pg.key.get_pressed()
    def get_key_name(key_code):
        """Devuelve el nombre o carácter asociado con un código de tecla."""
        for key_event in key_events_lower_char_list:
            if key_event['scancode'] == key_code:
                return key_event['key']
        return 'Unknown Key'
    pressed_keys = {key: get_key_name(key) for key, pressed in enumerate(keys) if pressed}
    return pressed_keys

# def update_char_key_state():
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

                # ESTO ES SOLO PARA MODIFICADORES: por que mod: es la sumatoria de todas las teclas modificadoras
                event_dict["keyPressed"]["Modifiers"] = update_modifiers_key_state() # modifiers
                
                update_control_key_state() # control
                
                
                # Obtener los modificadores activos
                if event.key in MODIFIER_KEYS: # modificadores
                    pass
                    #event_dict["keyPressed"]["Modifiers"].append(event.key)
                elif event.key in allowed_control_keys:
                    pass
                    #event_dict["keyPressed"]["Control"].append(event.key)
                elif event.unicode in allowed_char["lower"]: 
                    event_dict["keyPressed"]["char"].append({"unicode": event.unicode})

            elif event.type == pg.KEYUP:  # Tecla hacia arriba

                # ESTO ES SOLO PARA MODIFICADORES: por que mod: es la sumatoria de todas las teclas modificadoras
                event_dict["keyPressed"]["Modifiers"] = update_modifiers_key_state() # modifiers

                update_control_key_state() # control

                if event.key in MODIFIER_KEYS: # modificadores
                    pass
                    #event_dict["keyPressed"]["Modifiers"].remove(event.key)
                elif event.key in allowed_control_keys:
                    pass
                    #event_dict["keyPressed"]["Control"].remove(event.key)
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
