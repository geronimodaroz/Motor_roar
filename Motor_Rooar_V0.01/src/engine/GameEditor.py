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
    sys.path.append('c:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0.01')

    from system_info.sys_info import SysInfo # informacion del sistema

    from src.scripts.fonts import Font
    from src.engine.Events import event  # eventos

    # Configuración de la pantalla
    width, height = 800, 600
    default_screen_surface = pg.display.set_mode((width, height), pg.NOFRAME)
    window_id = pg.display.get_wm_info()["window"]
    # Carga el ícono (debe ser una imagen pequeña, preferiblemente 32x32)
    icono = pg.image.load('C:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0.01/assets/images/dino-32.png')
    # Establece el ícono de la ventana
    pg.display.set_icon(icono)

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
    from src.scripts import detection_archive_delate
    detection_archive_delate.monitorear_carpeta(game_folder_path)


    # # Inicializar el reloj y configurar FPS
    #-----------------------------------------------------------------------------
    clock = pg.time.Clock()
    fps_text = Font().surf_font_default(str(int(clock.get_fps())), (250, 250, 250))
    #-----------------------------------------------------------------------------


    # Diccionario de eventos
    #-----------------------------------------------------------------------------

    event_dict = {

        "SysInfo": {"Monitors": SysInfo.get_monitors_info()},  

        "MotorGameFolderpPath": motor_game_folder_path,
        "GameFolderpPath": game_folder_path,
        "Screen":{"Width":width, "Height":height},

        "ForceLoop":False,

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
    #-----------------------------------------------------------------------------


    # variables
    #-----------------------------------------------------------------------------
    depth_number = event_dict["depth_number"]
    #-----------------------------------------------------------------------------


     # engine screen
    #-----------------------------------------------------------------------------
    """Ventana del motor"""
    from src.instances.engine_window import EngineWindowInstance
    engine_window = EngineWindowInstance(event_dict,default_screen_surface)
    #-----------------------------------------------------------------------------


    # Forzar un evento de teclado
    #-----------------------------------------------------------------------------
    """Fuerzo un evento de teclado para que se detecten las teclas precionadas"""
    key_event_down = pg.event.Event(pg.KEYDOWN, {"key": pg.K_a, "mod": 0, "unicode": "a", "scancode": 4})
    pg.event.post(key_event_down)
    #-----------------------------------------------------------------------------


    while True: # Bucle principal

        try: # capturo errores 

            # DETECTAR SI HAY CAMBIOS EN LA CONFIGURACION DEL SISTEMA 


            # si detecto un cambio en los monitores
            #-----------------------------------------------------------------------------

            # ESTOY USANDO SysInfo.get_monitors_info() EN CADA FRAME !

            #print(SysInfo.get_monitor_count())

            
            if SysInfo.get_monitor_count() != len(event_dict["SysInfo"]["Monitors"]):

                time.sleep(2) # Esperamos dos segundos a que se configuren los monitores(no es la mejor forma)

                monitors_list = SysInfo.get_monitors_info()

                if len(monitors_list) < len(event_dict["SysInfo"]["Monitors"]):

                    del_monitors_list = [
                        monitor for monitor in event_dict["SysInfo"]["Monitors"]
                        if monitor not in monitors_list
                    ]

                    rect = wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(window_id, ctypes.byref(rect))

                    window_x = rect.left 
                    window_y = rect.top
                    
                    for monitor in del_monitors_list:

                        monitor_x = monitor["WorkArea"]["X"]
                        monitor_y = monitor["WorkArea"]["Y"]
                        monitor_w = monitor["WorkArea"]["Width"]
                        monitor_h = monitor["WorkArea"]["Height"]

                        monitor_rect = pg.rect.Rect(monitor_x,monitor_y,monitor_w,monitor_h)

                        # Comprobar si x,y de la ventana está dentro del monitor
                        if monitor_rect.collidepoint(window_x,window_y):

                            pg.display.set_mode((800, 600), pg.DOUBLEBUF | pg.NOFRAME)
                            window_id = pg.display.get_wm_info()["window"]
                            engine_window.rects_updates(pg.display.get_surface(), w=800,h=600, resize=True)
                            ctypes.windll.user32.SetWindowPos(window_id, None, 20, 20, 0, 0, 0x0001)  # reposiciona la ventana en x,y
                            engine_window.is_maximize = False
                            engine_window.monitor_selected = 0
                            event_dict["Screen"]["Width"] = 800
                            event_dict["Screen"]["Height"] = 600

                
                            
                event_dict["SysInfo"]["Monitors"] = monitors_list

            #-----------------------------------------------------------------------------




            # Solo procesar eventos si hay alguno
            events = pg.event.get()

            # hay bucle si hay evento o si algun objeto activa el forzador de bucle "event_dict["ForceLoop"]""
            if events or event_dict["ForceLoop"]:

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
                # # ejecuto objetos de lista clickable o selected
                # # ----------------------------------------------------------------------------
                exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= depth_number+1 
                if exists_next_clickable_list:
                    event_dict["EditableObjects"]["clickable"][depth_number+1](event_dict, code = "clickable") 

                exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= depth_number+1 
                if exists_next_selected_list:
                    event_dict["EditableObjects"]["selected"][depth_number+1](event_dict, code = "selected") 
                # ----------------------------------------------------------------------------

                #print(event_dict["EditableObjects"]["selected"])

                #Draw
                # ----------------------------------------------------------------------------

                #Modificar icono del mouse
                # ----------------------------------------------------------------------------
                if pg.mouse.get_cursor()[0] != event_dict["Mouse"]["Icon"]: # si es distinto, cambio
                    pg.mouse.set_cursor(event_dict["Mouse"]["Icon"])
                # ----------------------------------------------------------------------------
                

                default_screen_surface.fill((0,0,255)) # limpia escena 


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