import sys
import pygame as pg
import time
import os # crear carpetas, archivos ect..

from Folder_classes.font import Font # fuentes (string a surface)
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

# Variables para detectar el doble clic
# --------------------------------------------------------------------------
last_click_time = 0
double_click_interval = 0.5  # Intervalo en segundos permitido para considerar un doble clic
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
    "keyPressed": [],
    "Mouse":{"Motion":False,
             "Position":(0,0),
             "ClickLeftDown": False,
             "ClickLeftPressed": False,
             "ClickLeftUp": False,
             "ClickLeftDoubleClick": False,
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





# Bucle principal
while True:

    try: # capturo errores 

        #Eventos
        # ----------------------------------------------------------------------------
        # Reinicio los eventos
        
        # Mouse motion and mouse position
        if event_dict["Mouse"]["Position"] != pg.mouse.get_pos(): # si el mouse se mueve
            event_dict["Mouse"]["Motion"] = ((pg.mouse.get_pos()[0] - event_dict["Mouse"]["Position"][0]),
                                            (pg.mouse.get_pos()[1] - event_dict["Mouse"]["Position"][1]))
            event_dict["Mouse"]["Position"] = pg.mouse.get_pos()
            event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # reinicio icono del mouse
        else: 
            event_dict["Mouse"]["Motion"] = None

        # Restablecer eventos de clic de ratón
        event_dict["Mouse"]["ClickLeftDown"] = False
        event_dict["Mouse"]["ClickLeftUp"] = False
        event_dict["Mouse"]["ClickLeftDoubleClick"] = False
        # Restableces evento scroll del raton
        event_dict["Mouse"]["Scroll"] = None


        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            # eventos de teclas
            if event.type == pg.KEYDOWN: # tecla hacia abajo
                event_dict["keyPressed"].append({"key":event.key,"unicode":event.unicode})
            elif event.type == pg.KEYUP: # tecla hacia abajo
                i = event_dict["keyPressed"].index({"key":event.key,"unicode":event.unicode})
                del event_dict["keyPressed"][i]
            
            # Detectar eventos de clic del ratón
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    event_dict["Mouse"]["ClickLeftDown"] = True
                    event_dict["Mouse"]["ClickLeftPressed"] = True

                    # doble click
                    # ----------------------------------------------------------------------------
                    # Guardar el tiempo del clic
                    current_time = time.time()
                    # Comparar el tiempo entre clics
                    if current_time - last_click_time <= double_click_interval:
                        event_dict["Mouse"]["ClickLeftDoubleClick"] = True
                    # Actualizar el último tiempo de clic
                    last_click_time = current_time
                    # ----------------------------------------------------------------------------
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del ratón
                    event_dict["Mouse"]["ClickLeftUp"] = True
                    event_dict["Mouse"]["ClickLeftPressed"] = False

            # scroll del mouse
            if event.type == pg.MOUSEWHEEL:
                event_dict["Mouse"]["Scroll"] = 1 if event.y > 0 else -1
        # ----------------------------------------------------------------------------

        # Obtener posición del mouse
        # ----------------------------------------------------------------------------
        x,y = event_dict["Mouse"]["Position"]
        # ----------------------------------------------------------------------------

        # if event_dict["Mouse"]["ClickLeftDoubleClick"]:
        #     print(event_dict["Mouse"]["ClickLeftDoubleClick"])
        
        

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
