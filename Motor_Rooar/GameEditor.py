import sys
import pygame as pg
import time
import os # crear carpetas, archivos ect..

from Folder_classes.font import Font # fuentes (string a surface)


# Inicializar Pygame
pg.init()



# Configurar la pantalla
width, height = 1200, 600
screen = pg.display.set_mode((width, height))
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
    "keyPressed": [],
    "MouseClickLeft": (0, 0),
    "MouseScroll": None,
    "EditPoint": []
}
#-----------------------------------------------------------------------------




object_list = [] # lista de objetos en GameEditor(los objetos deben contener un "rect")


# box_conteiner
from box_conteiner import BoxConteiner
box_conteiner = BoxConteiner(event_dict,screen,80,80,300,450,(0,0,0))
object_list.append(box_conteiner) # agregamos el objeto box_conteiner a la lista




# Bucle principal
while True:
    # FPS
    fps_counter += 1
    elapsed_time = time.time() - start_time
    if elapsed_time >= 0.5:
        fps = fps_counter / elapsed_time
        fps_text = Font().surf_font(f"FPS: {fps:.2f}", (250, 250, 250))
        fps_counter = 0
        start_time = time.time()
    # Añadir un pequeño retraso para no consumir demasiados recursos
    #time.sleep(0.01) # esto puede ser buena idea


    # Reinicio los eventos
    event_dict["MouseClickLeft"] = None
    event_dict["MouseScroll"] = None


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

        # click izquierdo sobre la pantalla
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            event_dict["MouseClickLeft"] = event.pos

        # scroll del mouse
        if event.type == pg.MOUSEWHEEL:
            event_dict["MouseScroll"] = 1 if event.y > 0 else -1



    # detectamos colision:
    if event_dict["MouseClickLeft"]:
        for obj in object_list:
            if obj.rect.collidepoint(event_dict["MouseClickLeft"]):
                if event_dict["EditPoint"] and event_dict["EditPoint"][-1] in object_list:
                    event_dict["EditPoint"].pop()

                if obj not in event_dict["EditPoint"]:
                    event_dict["EditPoint"].append(obj)
                break
        else:
            event_dict["EditPoint"].clear()



    if box_conteiner in event_dict["EditPoint"]:
        event_dict = box_conteiner.edit(event_dict)






    # Dibuja el fondo
    screen.fill((128,128,128)) # limpia escena 
    # FPS
    screen.blit(fps_text, (width - fps_text.get_width() - 15,height - fps_text.get_height() -10)) # fps

    # Box_conteiner
    box_conteiner.draw(event_dict)


    # Actualiza la pantalla
    pg.display.flip()
