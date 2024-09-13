import pygame as pg
import ctypes
from ctypes import wintypes  # Importar wintypes correctamente

from scripts.surface_reposition import SurfaceReposition
#from scripts.fonts import Font

class EngineWindow():

    def __init__(self,event_dict,presurface):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        #self.presurface = presurface

        # Rect
        # ----------------------------------------------------------------------------
        self.rect = pg.rect.Rect(0,0,0,0)
        x = 0 #20
        y = 0 #20
        w = presurface.get_width() #- 40
        h = presurface.get_height() #- 40
        self.rects_updates(presurface,x,y,w,h)
        self.color = (120,120,120)
        # ----------------------------------------------------------------------------


        # variables de engine_window 
        # ----------------------------------------------------------------------------
        # ESTO TAL CEZ NO SEA NECESARIO!
        # Obtener el identificador de la ventana de Pygame (solo en Windows)
        window_id = pg.display.get_wm_info()["window"]
        # Habilitar que la ventana sea movible (solo en Windows)
        ctypes.windll.user32.SetWindowLongW(window_id, -16, ctypes.windll.user32.GetWindowLongW(window_id, -16) | 0x00080000)
        # ----------------------------------------------------------------------------

        
        # ----------------------------------------------------------------------------

        # Inicializar el reloj y configurar FPS
        #-----------------------------------------------------------------------------
        #self.clock = pg.time.Clock()
        #fps_text = Font().surf_font_default(str(int(self.clock.get_fps())), (250, 250, 250))


        self.objects_list = []  # Lista de objetos en GameEditor (los objetos deben contener un "rect")


        # Crear ventanas y objetos
        from objects.windows import Window
        window = Window(event_dict, self.view_surface, 350, 80, 300, 450, 500, 500, 1)
        self.objects_list.append(window)  # Agregar el objeto window a la lista

        from instances.Objects_creator import ObjectsCreator
        objects_creator_window = ObjectsCreator(event_dict, self.view_surface, 20, 80, 300, 450, 500, 500, 1)
        self.objects_list.append(objects_creator_window)  # Agregar el objeto creator window a la lista


        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------


    def rects_updates(self, presurface, x=0, y=0, w=0, h=0 , force = False):

        if not any([x, y, w, h]) and force == False:
            return
        
        # presurface - AQUI PRESURFACE NO ES NECESARIA PERO LA PONGO POR COHERENCIA
        # ----------------------------------------------------------------------------
        self.presurface = presurface
        # ----------------------------------------------------------------------------
        # Rect
        # ----------------------------------------------------------------------------
        self.rect.x += x
        self.rect.y += y
        self.rect.width += w
        self.rect.height += h
        # ----------------------------------------------------------------------------
        
        #self.rect = pg.rect.Rect(x,y,w,h)

        # scale_modifier_rect 
        # ----------------------------------------------------------------------------
        self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # ----------------------------------------------------------------------------

        # view_rect 
        # ----------------------------------------------------------------------------
        margin = 20
        x = margin
        y = margin
        w = self.rect.width - (margin*2)
        h = self.rect.height - (margin*2)
        self.view_rect = pg.rect.Rect(x,y,w,h)
        self.view_surface_rect = self.view_rect.copy()
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)
        # ----------------------------------------------------------------------------

    

    def collision_detector(self,event_dict):

        def init():
        
            # ----------------------------------------------------------------------------
            x,y = event_dict["Mouse"]["Position"] # Obtención de la posición del ratón
            # ----------------------------------------------------------------------------

            if self.view_rect.collidepoint(x, y):

                _comprobation_section_view_edit()

            elif self.scale_modifier_rect.collidepoint(x, y):
                pass



        def _comprobation_section_view_edit():

            event_dict["EditableObjects"]["clickable"].append(self.edit)

            # mouse x,y con respecto a view_rect
            x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
            y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
            save_x_y = event_dict["Mouse"]["Position"]
            event_dict["Mouse"]["Position"] = (x,y)

            # Detectar colisión con objetos
            for obj in self.objects_list:
                if obj.rect.collidepoint(x, y):
                    obj.collision_detector(event_dict)
                    if event_dict["EditableObjects"]["clickable"]: break

            event_dict["Mouse"]["Position"] = save_x_y

            # Detectar colisión con objetos dentro de la lista objects_list
            # ----------------------------------------------------------------------------
            # if (event_dict["Mouse"]["Motion"] and not event_dict["Mouse"]["ClickLeftPressed"]) or event_dict["Mouse"]["ClickLeftUp"]:
            #     # Limpiar la lista de clickeables a partir del índice depth_number+1
            #     #event_dict["EditableObjects"]["clickable"] = event_dict["EditableObjects"]["clickable"][:depth_number + 1]
            #     # verifica donde esta el mouse y los objetos que colisionan con el 
            #     # ----------------------------------------------------------------------------
            #     save_clickable_list = event_dict["EditableObjects"]["clickable"].copy()
            #     del event_dict["EditableObjects"]["clickable"][self.depth_number+1:]

            #     # mouse x,y con respecto a view_rect
            #     x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
            #     y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
            #     save_x_y = event_dict["Mouse"]["Position"]
            #     event_dict["Mouse"]["Position"] = (x,y)

            #     # Detectar colisión con objetos
            #     for obj in self.objects_list:
            #         if obj.rect.collidepoint(x, y):
            #             obj.collision_detector(event_dict)
            #             if event_dict["EditableObjects"]["clickable"]: break

            #     event_dict["Mouse"]["Position"] = save_x_y
                
            #     # ----------------------------------------------------------------------------
            #     # si el mouse cambio de objetos ejecuto cambios pre o pos de los objetos en las listas 
            #     # ----------------------------------------------------------------------------
            #     if save_clickable_list != event_dict["EditableObjects"]["clickable"]:
            #         def pre_pos_methods(list, prefix, event_dict, code):
            #             """Ejecuta métodos con el prefijo dado para cada objeto en la lista."""
            #             for obj_func in list:
            #                 if not(obj_func in event_dict["EditableObjects"]["selected"]): # si es "selected" no entrar a "clickable"
            #                     try:
            #                         obj = obj_func.__self__  # desvincula el objeto 
            #                         func = obj_func.__func__  # desvincula el método
            #                         method_name = f"{prefix}{func.__name__}"
            #                         method_to_call = getattr(obj, method_name, None)
            #                         if callable(method_to_call):
            #                             method_to_call(event_dict, code)
            #                     except Exception as e:
            #                         print(e)
            #         # Ejecutar métodos pos_ para objetos clickados
            #         pre_pos_methods(save_clickable_list,"pos_", event_dict, code = "clickable")
            #         # Ejecutar métodos pre_ para objetos clickados
            #         pre_pos_methods(event_dict["EditableObjects"]["clickable"],"pre_", event_dict, code = "clickable")
            #     # ----------------------------------------------------------------------------

            # # ----------------------------------------------------------------------------
            # # Si se hace clic izquierdo, copiar lista clickeable a lista seleccionada
            # # ----------------------------------------------------------------------------
            # elif event_dict["Mouse"]["ClickLeftDown"] :
            #     if event_dict["EditableObjects"]["selected"] != event_dict["EditableObjects"]["clickable"]:
            #         def pre_pos_methods(list, prefix, event_dict, code):

            #             """Ejecuta métodos con el prefijo dado para cada objeto en la lista."""
            #             for obj_func in list:
            #                 try:
            #                     obj = obj_func.__self__  # desvincula el objeto 
            #                     func = obj_func.__func__  # desvincula el método
            #                     method_name = f"{prefix}{func.__name__}"
            #                     method_to_call = getattr(obj, method_name, None)
            #                     if callable(method_to_call):
            #                         method_to_call(event_dict, code)
            #                 except Exception as e:
            #                     print(e)
            #         # Ejecutar métodos pos_ para objetos seleccionados
            #         pre_pos_methods(event_dict["EditableObjects"]["selected"],"pos_", event_dict, code = "selected")
            #         # Actualizar listas de seleccionados y clickeables
            #         event_dict["EditableObjects"]["selected"] = event_dict["EditableObjects"]["clickable"].copy()
            #         event_dict["EditableObjects"]["clickable"].clear()
            #         # Ejecutar métodos pre_ para objetos seleccionados
            #         pre_pos_methods(event_dict["EditableObjects"]["selected"],"pre_", event_dict, code = "selected")
            
        init()
       

    def edit(self,event_dict,code = None):

        # mouse x,y con respecto a view_rect
        x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
        y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
        save_x_y = event_dict["Mouse"]["Position"]
        event_dict["Mouse"]["Position"] = (x,y)

        # ejecuto objetos de lista selected
        #ESTO ESTA MAL!! -- por?
        # ----------------------------------------------------------------------------
        if code == "clickable":
            exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= self.depth_number+1 
            if exists_next_clickable_list:
                event_dict["EditableObjects"]["clickable"][self.depth_number+1](event_dict, code ) 

        if code == "selected":
            exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number+1 
            if exists_next_selected_list:
                event_dict["EditableObjects"]["selected"][self.depth_number+1](event_dict, code )
        # ----------------------------------------------------------------------------


        event_dict["Mouse"]["Position"] = save_x_y



         # Delate objects from object_list
        if event_dict["Delate_List"]:
            for obj in event_dict["Delate_List"]:
                if obj in self.objects_list:
                    self.objects_list.remove(obj)
            event_dict["Delate_List"].clear()



    def draw(self,event_dict):

        self.view_surface.fill((50,50,50)) # limpia escena 


        pg.draw.rect(self.presurface,self.color,self.view_rect)


        # FPS
        # ----------------------------------------------------------------------------
        # fps_text = Font.surf_font_default(str(int(self.clock.get_fps())), (250, 250, 250))
        # width  = event_dict["screen"]["width"]
        # height = event_dict["screen"]["height"]
        # self.view_surface.blit(fps_text, (width - fps_text.get_width() - 50,height - fps_text.get_height() -50)) # fps
        # # ----------------------------------------------------------------------------

        #TRATAR DE DIBUJAR SOLO UNA VEZ Y ACTUALIZAR!!
        if self.objects_list:
            for obj in self.objects_list:
                obj.draw(event_dict)



        
