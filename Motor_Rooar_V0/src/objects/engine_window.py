import pygame as pg
import ctypes
from ctypes import wintypes  # Importar wintypes correctamente
#from ctypes import wintypes, byref, windll

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
        #self.rects_updates(presurface,x,y,w,h)
        self.color = (120,120,120)
        # ----------------------------------------------------------------------------

        # Inicializar scale_modifier
        # ----------------------------------------------------------------------------
        self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_right = self.scale_modifier_hit_left = False
        self.scale_modifier_bar = 30
        self.scale_modifier_margin = 5
        # ----------------------------------------------------------------------------


        # variables de engine_window 
        # ----------------------------------------------------------------------------
        # ESTO TAL CEZ NO SEA NECESARIO!
        # Obtener el identificador de la ventana de Pygame (solo en Windows)
        self.window_id = pg.display.get_wm_info()["window"]
        # Habilitar que la ventana sea movible (solo en Windows)
        ctypes.windll.user32.SetWindowLongW(self.window_id, -16, ctypes.windll.user32.GetWindowLongW(self.window_id, -16) | 0x00080000)
        #self.moving = False
        self.initial_mouse_x = 0
        self.initial_mouse_y = 0
        self.initial_window_left = 0
        self.initial_window_top = 0
        self.initial_window_width = 0
        self.initial_window_height = 0

        self.window_left = 0
        self.window_top = 0
        self.window_width = 0
        self.window_height = 0

        self.window_right = 0

        self.save_global_mouse_x = 0
        self.save_global_mouse_y = 0

        # Obtener el "device context" (DC) de la pantalla principal
        self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla


        # ----------------------------------------------------------------------------

        self.objects_list = []  # Lista de objetos en GameEditor (los objetos deben contener un "rect")


        # Llamar a rects_updates para inicializar rectángulos
        # ----------------------------------------------------------------------------
        self.rects_updates(presurface,w,h)
        # ----------------------------------------------------------------------------

        


        # Crear ventanas y objetos
        from objects.windows import Window
        window = Window(event_dict, self.view_surface, 350, 80, 300, 450, 1024, 683, 1)
        self.objects_list.append(window)  # Agregar el objeto window a la lista

        from instances.Objects_creator import ObjectsCreator
        objects_creator_window = ObjectsCreator(event_dict, self.view_surface, 20, 80, 300, 450, 500, 500, 1)
        self.objects_list.append(objects_creator_window)  # Agregar el objeto creator window a la lista


        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def rects_updates(self, presurface, w=0, h=0, resize=False, force=False):
        """
        Actualiza las propiedades del rectángulo del objeto.

        Parámetros:
            presurface: Superficie previa (no utilizada directamente en este código).
            x (int): Nueva posición en el eje X (opcional). ES 0, NO DEBE CAMBIARSE!
            y (int): Nueva posición en el eje Y (opcional). ES 0, NO DEBE CAMBIARSE!
            w (int): Nuevo ancho (opcional).
            h (int): Nueva altura (opcional).
            resize (bool): Indica si se debe redimensionar el rectángulo con los valores proporcionados.
            force (bool): Si es True, fuerza la actualización aunque no se cambien x, y, w, h.
        """

        # Si no hay valores para x, y, w, h y no se fuerza la actualización, salir
        if not any([w, h]) and not force:
            return
        
        # presurface 
        # ----------------------------------------------------------------------------
        self.presurface = presurface
        # ----------------------------------------------------------------------------
        
        # Si hay valores de x, y, w, h y resize es True, actualizar las dimensiones del rectángulo
        if resize:
            if w != 0:
                self.rect.w = w
            if h != 0:
                self.rect.h = h
        else:
            # Rect
            # ----------------------------------------------------------------------------
            self.rect.x = 0
            self.rect.y = 0
            self.rect.width += w
            self.rect.height += h
            # ----------------------------------------------------------------------------
        

        # scale_modifier_rect 
        # ----------------------------------------------------------------------------
        self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # ----------------------------------------------------------------------------

        # view_rect 
        # ----------------------------------------------------------------------------
        bar = self.scale_modifier_bar
        margin = self.scale_modifier_margin

        x = margin
        y = bar #margin
        w = self.rect.width - (margin*2)
        h = self.rect.height - (bar) - (margin)

        self.view_rect = pg.rect.Rect(x,y,w,h)
        self.view_surface_rect = self.view_rect.copy()
        
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)
        # ----------------------------------------------------------------------------

        # recreo los rects de los objetos dentro de engine window
        # ----------------------------------------------------------------------------
        if self.objects_list:
            for obj in self.objects_list:
                obj.rects_updates(self.view_surface, force = True)
        # ----------------------------------------------------------------------------

    def collision_detector(self,event_dict):

        # ----------------------------------------------------------------------------
        mouse_x, mouse_y = event_dict["Mouse"]["Position"] # Obtención de la posición del ratón
        # ----------------------------------------------------------------------------

        def init():

            if self.view_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_view_edit()
            elif self.scale_modifier_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_scale_modifier()

        def _comprobation_section_scale_modifier():

            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)

            margin = self.scale_modifier_margin
            bar = self.scale_modifier_bar
            x, y, w, h = self.scale_modifier_rect
            hit_top = mouse_y <= y + bar
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin
            self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False



            # ENTREGA POSICION ACTUAL DEL MOUSE
            # ----------------------------------------------------------------------------
            class POINT(ctypes.Structure):
                _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]
            def get_global_mouse_position():
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                return point.x, point.y
            self.save_global_mouse_x,self.save_global_mouse_y = get_global_mouse_position()
            # ----------------------------------------------------------------------------


            if hit_down and hit_left:
                self.scale_modifier_hit_down = self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down and hit_right:
                self.scale_modifier_hit_down = self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top:
                self.scale_modifier_hit_top = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
            elif hit_down:
                self.scale_modifier_hit_down = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left:
                self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            elif hit_right:
                self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE

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
    
    def scale_modifier(self,event_dict,code = None):

        if code == "clickable":
            pass
        
        if code == "selected":

            class POINT(ctypes.Structure):
                _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

            def get_global_mouse_position():
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                return point.x, point.y
            
            # Detectar el clic izquierdo y activar el movimiento
            if event_dict["Mouse"]["ClickLeftDown"]:
                self.initial_mouse_x, self.initial_mouse_y = get_global_mouse_position()
                rect = wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(self.window_id, ctypes.byref(rect))

                self.window_left = rect.left
                self.window_top = rect.top
                self.window_width = rect.right - rect.left
                self.window_height = rect.bottom - rect.top

            displacement_x,displacement_y = 0,0

            if (self.save_global_mouse_x,self.save_global_mouse_y) != get_global_mouse_position():
                x,y = get_global_mouse_position()
                displacement_x = x - self.save_global_mouse_x
                displacement_y = y - self.save_global_mouse_y
                self.save_global_mouse_x,self.save_global_mouse_y = get_global_mouse_position()


            if self.scale_modifier_hit_top:

                self.window_left += displacement_x
                self.window_top += displacement_y

                x = self.window_left
                y = self.window_top
                w = self.window_width
                h = self.window_height

                #ctypes.windll.user32.MoveWindow(self.window_id,x,y,w,h, True)
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001)  # 0x0001 es la bandera SWP_NOSIZE para no cambiar el tamaño



            elif self.scale_modifier_hit_down:
                
                # Cambiar las dimensiones de la ventana
                self.window_height += displacement_y

                x = self.window_left
                y = self.window_top
                w = self.window_width
                h = max(100, self.window_height)

                # Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Ancho de las líneas del contorno
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar solo las líneas del buffer a la pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)  # Línea superior
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)  # Línea inferior
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)  # Línea izquierda
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)  # Línea derecha

                    # Invalidar las áreas donde se dibujaron las líneas para forzar la actualización
                    if displacement_y != 0:
                        #rect = wintypes.RECT(x, y, x + w, y + h)
                        #ctypes.windll.user32.InvalidateRect(0, ctypes.byref(rect), True)
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    # Liberar la ventana para que vuelva a actualizarse
                    ctypes.windll.user32.LockWindowUpdate(0)
                    # Liberar el DC de la pantalla después de dibujar
                    #ctypes.windll.user32.ReleaseDC(self.window_id, self.hdc)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    # Liberar el contexto de memoria
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                event_dict["Screen"]["Height"] = h

            
            # Modificar el ancho de la ventana hacia la derecha y dibujar líneas
            if self.scale_modifier_hit_right:
                
                # Definir las constantes
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Actualizar el ancho de la ventana
                self.window_width += displacement_x

                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height

                # Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar las líneas al contexto de pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)

                    # Invalidar las áreas para forzar la actualización
                    if displacement_x!=0 and displacement_y==0:
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    ctypes.windll.user32.LockWindowUpdate(0)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                # Actualizar el diccionario de eventos
                event_dict["Screen"]["Width"] = w

            # Modificar el ancho de la ventana hacia la izquierda y dibujar líneas
            elif self.scale_modifier_hit_left:

                # Definir las constantes
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Calculate the new width and ensure it doesn't go below 100
                new_width = self.window_width - displacement_x
                if new_width < 100:
                    # Adjust the displacement to ensure the width is not less than 100
                    displacement_x = self.window_width - 100

                # Actualizar la posición y el ancho de la ventana
                self.window_left += displacement_x
                self.window_width -= displacement_x

                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height
                

                #Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar las líneas al contexto de pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)

                    # Invalidar las áreas para forzar la actualización
                    if displacement_x!=0 and displacement_y==0:
                        #ctypes.windll.user32.InvalidateRect(0, self.window_id, True)
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    ctypes.windll.user32.LockWindowUpdate(0)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                # Actualizar el diccionario de eventos
                event_dict["Screen"]["Width"] = w






            if event_dict["Mouse"]["ClickLeftUp"]:
                #self.window_id = pg.display.get_wm_info()["window"] # esto no es necesario?

                #self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False
                ctypes.windll.user32.MoveWindow(self.window_id, x, y, w, h, True)
                w  = event_dict["Screen"]["Width"]
                h = event_dict["Screen"]["Height"]
                pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                self.window_id = pg.display.get_wm_info()["window"]
                self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                del event_dict["EditableObjects"]["selected"][self.depth_number:]    



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

        #self.view_surface.fill((50,50,50)) # limpia escena 


        pg.draw.rect(self.presurface,self.color,self.view_rect)

        #pg.draw.rect(self.presurface,(255,0,0),self.rect,1)

        #pg.draw.rect(self.presurface,(255,0,0),self.view_rect,1)



        #TRATAR DE DIBUJAR SOLO UNA VEZ Y ACTUALIZAR!!
        if self.objects_list:
            for obj in self.objects_list:
                obj.draw(event_dict)

        



        
