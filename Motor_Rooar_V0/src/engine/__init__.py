import sys
import pygame as pg
import time
import os # crear carpetas, archivos ect..

sys.path.append('c:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0/src')

from Motor_Rooar_V0.src.scripts.clicks_detector import Font # fuentes (string a surface)
import traceback

from Events import event # eventos

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
from scripts import detection_archive_delate
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

    "keyPressed":{"char":     [], 
                    "Control":  [], 
                    "Modifiers":[],
                    "shortcuts":[]},

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
from objects.windows import Window
window = Window(event_dict,screen,350,80,300,450,500,500,1)
objects_list.append(window) # agregamos el objeto window a la lista

from instances.Objects_creator import ObjectsCreator
# # window2
objects_creator_window = ObjectsCreator(event_dict,screen,0,80,300,450,500,500,1)
objects_list.append(objects_creator_window) # agregamos el objeto window a la lista


# FORZAR UN EVENTO DE TECLADO
key_event_down = pg.event.Event(pg.KEYDOWN, {"key": pg.K_a, "mod": 0, "unicode": "a", "scancode": 4})
pg.event.post(key_event_down)