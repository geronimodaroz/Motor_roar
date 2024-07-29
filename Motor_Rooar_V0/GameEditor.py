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


# fuente para el contador de FPS
fps_text = Font().surf_font("")
# Inicializar el contador de fotogramas
fps_counter = 0
start_time = time.time()


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


# diccionario de eventos
#-----------------------------------------------------------------------------
# Diccionario de eventos
event_dict = {
    "MotorGameFolderpPath": motor_game_folder_path,
    "GameFolderpPath": game_folder_path,
    "screen":{"width":width, "height":height},
    "keyPressed": [],
    "Mouse":{"Motion":False,"MousePosition":(0,0),"MouseClickLeftDown": False,"MouseClickLeftPressed": False,"MouseClickLeftUp": False,"Scroll": None,"Icon":pg.SYSTEM_CURSOR_ARROW,},
    "EditableObjects": {"selected":[],"clickable":[]},
    "depth_number": -1
}
#-----------------------------------------------------------------------------

depth_number = event_dict["depth_number"]



object_list = [] # lista de objetos en GameEditor(los objetos deben contener un "rect")



# window2
from windows import Window
window = Window(event_dict,screen,250,80,300,450,-1)
object_list.append(window) # agregamos el objeto window a la lista



# Bucle principal
while True:

    try: # capturo errores 

        # FPS
        # ----------------------------------------------------------------------------
        fps_counter += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= 0.5:
            fps = fps_counter / elapsed_time
            fps_text = Font().surf_font(f"FPS: {fps:.2f}", (250, 250, 250))
            fps_counter = 0
            start_time = time.time()
        # Añadir un pequeño retraso para no consumir demasiados recursos
        time.sleep(0.01) # esto puede ser buena idea
        # ----------------------------------------------------------------------------

        #Eventos
        # ----------------------------------------------------------------------------
        # Reinicio los eventos
        
        # Mouse motion and mouse position
        if event_dict["Mouse"]["MousePosition"] != pg.mouse.get_pos(): # si el mouse se mueve
            event_dict["Mouse"]["Motion"] = ((pg.mouse.get_pos()[0] - event_dict["Mouse"]["MousePosition"][0]),
                                            (pg.mouse.get_pos()[1] - event_dict["Mouse"]["MousePosition"][1]))
            event_dict["Mouse"]["MousePosition"] = pg.mouse.get_pos()
            event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # reinicio icono del mouse
        else: 
            event_dict["Mouse"]["Motion"] = None

        # Restablecer eventos de clic de ratón
        event_dict["Mouse"]["MouseClickLeftDown"] = False
        event_dict["Mouse"]["MouseClickLeftUp"] = False



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
                    #event_dict["MouseClickLeft"] = event.pos
                    event_dict["Mouse"]["MouseClickLeftDown"] = True
                    event_dict["Mouse"]["MouseClickLeftPressed"] = True
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del ratón
                    event_dict["Mouse"]["MouseClickLeftUp"] = True
                    event_dict["Mouse"]["MouseClickLeftPressed"] = False

            # scroll del mouse
            if event.type == pg.MOUSEWHEEL:
                event_dict["Mouse"]["Scroll"] = 1 if event.y > 0 else -1
        # ----------------------------------------------------------------------------

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0] 
        mouse_y = event_dict["Mouse"]["MousePosition"][1] 
        # ----------------------------------------------------------------------------


        # detectamos colision: Mouse Position
        # ----------------------------------------------------------------------------
        # detectamos en cada frama si hay colision con algun objeto dentro de la lista object_list:
        # esto no se puede optimizar de alguna manera?
        if not(event_dict["Mouse"]["MouseClickLeftPressed"]):
            del event_dict["EditableObjects"]["clickable"][depth_number+1:]
            for obj in object_list:
                #obj.collision_detector(event_dict)
                if obj.rect.collidepoint(mouse_x,mouse_y):
                    obj.collision_detector(event_dict)
                if event_dict["EditableObjects"]["clickable"]: break
        # ----------------------------------------------------------------------------
        # si hago click izquierdo copiamos lista clickeable a lista selected
        # ----------------------------------------------------------------------------
        elif event_dict["Mouse"]["MouseClickLeftDown"]:
            event_dict["EditableObjects"]["selected"] = event_dict["EditableObjects"]["clickable"].copy()
            event_dict["EditableObjects"]["clickable"].clear()
        # ----------------------------------------------------------------------------
        # ejecuto objetos de lista selected
        # ----------------------------------------------------------------------------
        selected_in_list = len(event_dict["EditableObjects"]["selected"])-1 >= depth_number+1 
        if selected_in_list:
            event_dict["EditableObjects"]["selected"][depth_number+1](event_dict)
        # ----------------------------------------------------------------------------



        print(event_dict["EditableObjects"]["clickable"])
        #print(event_dict["EditableObjects"]["selected"])


        

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
        screen.blit(fps_text, (width - fps_text.get_width() - 15,height - fps_text.get_height() -10)) # fps

        #TRATAR DE DIBUJAR SOLO UNA VEZ Y ACTUALIZAR!!

        # window
        window.draw(event_dict)
        # Actualiza la pantalla
        pg.display.flip()
        # ----------------------------------------------------------------------------

    except Exception as e:
        #print(f"Error: {e}")
        # Capturar y mostrar el traceback
        tb = traceback.format_exc()
        print(tb)
