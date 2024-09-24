import os
import sys
import time
import traceback
import ctypes
from ctypes import wintypes
import pygame as pg



def main():

    # Inicializar Pygame    
    pg.init()

    # Añadir la ruta al módulo de scripts
    sys.path.append('c:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0.01/src')

    from scripts.fonts import Font
    from Events import event  # eventos

    # Configuración de la pantalla
    width, height = 800, 600
    default_screen_surface = pg.display.set_mode((width, height), pg.NOFRAME)
    window_id = pg.display.get_wm_info()["window"]

    pg.display.set_caption("Roar!!")

    # Configuración de rutas
    #-----------------------------------------------------------------------------
    motor_game_folder_path = "C:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar"
    # Ruta al escritorio y creación de carpeta
    #-----------------------------------------------------------------------------
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    os.chdir(desktop_path)  # Moverse a la ubicación de la ruta
    if not os.path.exists("Videojuego_00"):  # Verificar existencia de carpeta
        os.mkdir("Videojuego_00")  # Crear carpeta
    game_folder_path = os.path.join(desktop_path, "Videojuego_00")  # Ruta a la carpeta del juego
    # Monitor de archivos en la carpeta del juego
    #-----------------------------------------------------------------------------
    from scripts import detection_archive_delate
    detection_archive_delate.monitorear_carpeta(game_folder_path)

    # # Inicializar el reloj y configurar FPS
    # #-----------------------------------------------------------------------------
    clock = pg.time.Clock()
    fps_text = Font().surf_font_default(str(int(clock.get_fps())), (250, 250, 250))

    # Diccionario de eventos
    #-----------------------------------------------------------------------------
    event_dict = {
        "MotorGameFolderpPath": motor_game_folder_path,
        "GameFolderpPath": game_folder_path,
        "Screen":{"Width":width, "Height":height},
        "FPS": {
            "Fixed": 60,
            "Real": None,
            "delta_time": None
        },
        "Colors": {
            "DarkGrey": (5, 5, 5),
            "IntermediumGrey": (40, 40, 40),
            "LightGrey": (90, 90, 90),
            "GreenFluor": (204, 255, 0)
        },
        "keyPressed": {
            "char": [],
            "Control": [],
            "Modifiers": [],
            "shortcuts": []
        },
        "Mouse": {
            "Motion": False,
            "Position": (0, 0),
            "ClickLeftDown": False,
            "ClickLeftPressed": False,
            "ClickLeftUp": False,
            "Scroll": None,
            "Icon": pg.SYSTEM_CURSOR_ARROW
        },
        "EditableObjects": {
            "selected": [],
            "clickable": []
        },
        "depth_number": -1,
        "Delate_List": [],
    }

    # Inicialización de objetos
    #-----------------------------------------------------------------------------
    depth_number = event_dict["depth_number"]
    #objects_list = []  # Lista de objetos en GameEditor (los objetos deben contener un "rect")

     # engine screen
    #-----------------------------------------------------------------------------
    from objects.engine_window import EngineWindow
    engine_window = EngineWindow(event_dict,default_screen_surface)
    #-----------------------------------------------------------------------------



    # Forzar un evento de teclado
    #-----------------------------------------------------------------------------
    key_event_down = pg.event.Event(pg.KEYDOWN, {"key": pg.K_a, "mod": 0, "unicode": "a", "scancode": 4})
    pg.event.post(key_event_down)




    while True: # Bucle principal

        try: # capturo errores 

            # Solo procesar eventos si hay alguno
            events = pg.event.get()
            if events:

                #Bucle de Eventos
                # ----------------------------------------------------------------------------
                # GESTIONA LOS EVENTOS Y SU REINICIO
                event(events,event_dict)
                # ----------------------------------------------------------------------------

                # Obtener posición del mouse
                # ----------------------------------------------------------------------------
                x,y = event_dict["Mouse"]["Position"]
                # ----------------------------------------------------------------------------
                
                # # Detectar colisión con objetos dentro de la lista objects_list
                # # ----------------------------------------------------------------------------
                if (event_dict["Mouse"]["Motion"] and not event_dict["Mouse"]["ClickLeftPressed"]) or event_dict["Mouse"]["ClickLeftUp"]:
                    # Limpiar la lista de clickeables a partir del índice depth_number+1
                    #event_dict["EditableObjects"]["clickable"] = event_dict["EditableObjects"]["clickable"][:depth_number + 1]
                    # verifica donde esta el mouse y los objetos que colisionan con el 
                    # ----------------------------------------------------------------------------
                    save_clickable_list = event_dict["EditableObjects"]["clickable"].copy()
                    del event_dict["EditableObjects"]["clickable"][depth_number+1:]

                    if engine_window.rect.collidepoint(x, y):
                        engine_window.collision_detector(event_dict)

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

                # # ----------------------------------------------------------------------------
                # # ejecuto objetos de lista selected
                # # ----------------------------------------------------------------------------
                exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= depth_number+1 
                if exists_next_clickable_list:
                    event_dict["EditableObjects"]["clickable"][depth_number+1](event_dict, code = "clickable") 

                exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= depth_number+1 
                if exists_next_selected_list:
                    event_dict["EditableObjects"]["selected"][depth_number+1](event_dict, code = "selected") 
                # ----------------------------------------------------------------------------

                #Draw
                # ----------------------------------------------------------------------------

                #Modificar icono del mouse
                # ----------------------------------------------------------------------------
                if pg.mouse.get_cursor()[0] != event_dict["Mouse"]["Icon"]: # si es distinto, cambio
                    pg.mouse.set_cursor(event_dict["Mouse"]["Icon"])
                # ----------------------------------------------------------------------------
                

                default_screen_surface.fill((50,50,50)) # limpia escena 


                engine_window.draw(event_dict) # engine_screen

                # # FPS
                # ----------------------------------------------------------------------------
                fps_text = Font.surf_font_default(str(int(clock.get_fps())), (250, 250, 250))
                width  = event_dict["Screen"]["Width"]
                height = event_dict["Screen"]["Height"]
                default_screen_surface.blit(fps_text, (width - fps_text.get_width() - 20,height - fps_text.get_height() -15)) # fps
                # ----------------------------------------------------------------------------

                
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




if __name__ == "__main__": # solo se puede ejecutar desde el script, no se puede llamar al metodo main()
    main()