import tkinter as tk
import os
import sys
import time
import traceback
import ctypes
from ctypes import wintypes
import pygame as pg

class TransparentWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")  # Tamaño y posición de la ventana
        self.root.overrideredirect(True)  # Eliminar la barra superior nativa

        # Crear el marco externo con bordes personalizados
        self.border_frame = tk.Frame(self.root, bg='black', bd=5)  # Color del borde externo
        #self.border_frame.place(x=50, y=50, width=500, height=500)
        self.border_frame.pack(fill="both", expand=True)

        # Crear la barra superior personalizada
        self.title_bar = tk.Frame(self.border_frame, bg='black', relief='raised', bd=0)  # Barra superior de color oscuro
        self.title_bar.pack(fill="x")

        # Botón de cerrar en la barra superior
        close_button = tk.Button(self.title_bar, text="Cerrar", command=self.close, bg='red', fg='white')
        close_button.pack(side="right", padx=10, pady=2)

        # Etiqueta para arrastrar la ventana
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.move_window)
        
        # Crear el área central de contenido
        self.content_area = tk.Frame(self.border_frame, bg='gray')
        self.content_area.pack(fill="both", expand=True)
        
        # Inicializar Pygame en un Frame
        self.pygame_frame = tk.Frame(self.content_area, width=800, height=600, bg='blue', highlightthickness=0)
        self.pygame_frame.place(x=0, y=0)  # Colocar el frame en el centro

        # Bind para detectar el movimiento del mouse y cambiar el cursor
        self.border_frame.bind("<Motion>", self.change_cursor_borde)
        self.content_area.bind("<Motion>", self.change_cursor_content_area)


        # Inicializar la ventana de Pygame
        self.root.after(100, self.embed_pygame)
        #self.embed_pygame()

    def embed_pygame(self):
        # Iniciar Pygame
        os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())  # Vincular Pygame con el ID del frame
        #pg.init()
        # Configurar la ventana de Pygame dentro del frame

        # Ejemplo simple de Pygame: Dibujar en la ventana incrustada
        self.running = True
        self.pygame_loop()

    def pygame_loop(self):


        # Inicializar Pygame    
        pg.init()

        # Añadir la ruta al módulo de scripts
        sys.path.append('c:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0.01/src')

        from scripts.fonts import Font
        from Events import event  # eventos

        # Configuración de la pantalla
        width, height = 800, 600
        default_screen_surface = pg.display.set_mode((width, height), pg.NOFRAME)
        #print(default_screen_surface.get_width(),default_screen_surface.get_height())
        
        window_id = pg.display.get_wm_info()["window"]

        #pg.display.set_caption("Roar!!")

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



        while self.running:


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

                    # Dibujar en la ventana de Pygame
                    default_screen_surface.fill((50,50,50))  # Fondo azul

                    #pg.draw.rect(default_screen_surface,(255,0,0),(20,20,200,200))



                    engine_window.draw(event_dict) # engine_screen

                    # # FPS
                    # ----------------------------------------------------------------------------
                    fps_text = Font.surf_font_default(str(int(clock.get_fps())), (250, 250, 250))
                    width  = event_dict["Screen"]["Width"]
                    height = event_dict["Screen"]["Height"]
                    default_screen_surface.blit(fps_text, (width - fps_text.get_width() - 20,height - fps_text.get_height() -15)) # fps
                    # ----------------------------------------------------------------------------

                    # Actualizar la pantalla de Pygame
                    pg.display.update()

                    # Limitar a 60 FPS
                    # ----------------------------------------------------------------------------
                    clock.tick(event_dict["FPS"]["Fixed"])
                    event_dict["FPS"]["Real"] = clock.get_fps()
                    event_dict["FPS"]["delta_time"] = clock.get_time() / 1000 # Calcular tiempo transcurrido
                    # ----------------------------------------------------------------------------

                # Actualizar la ventana de Tkinter
                self.root.update_idletasks()
                self.root.update()



            except Exception as e:
                tb = traceback.format_exc()
                print(tb)




    def change_cursor_content_area(self, event):
        pass
        #self.root.config(cursor="arrow")  # Restablecer el cursor a la flecha normal

    def change_cursor_borde(self, event):
        x, y = event.x, event.y
        width = self.border_frame.winfo_width()
        height = self.border_frame.winfo_height()
        border_width = 5  # El ancho del borde negro
        
        # Cambiar el cursor cuando el ratón está sobre los bordes
        if x <= border_width and y >= height - border_width:
            self.root.config(cursor="bottom_left_corner")  # Esquina inferior izquierda
        elif x >= width - border_width and y >= height - border_width:
            self.root.config(cursor="bottom_right_corner")  # Esquina inferior derecha
        elif x <= border_width:
            self.root.config(cursor="left_side")  # Borde izquierdo
        elif x >= width - border_width:
            self.root.config(cursor="right_side")  # Borde derecho
        elif y >= height - border_width:
            self.root.config(cursor="bottom_side")  # Borde inferior
        else:
            self.root.config(cursor="arrow")  # Restablecer el cursor a la flecha normal

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def move_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def close(self):
        self.running = False  # Cierra el loop de Pygame
        self.root.destroy()  # Cierra la ventana de Tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = TransparentWindow(root)
    root.mainloop()