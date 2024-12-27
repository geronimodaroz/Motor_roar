import os  # Crear carpetas, archivos, etc.
import time
#import sys
#import math

import pygame as pg
import pyperclip  # Para hacer Ctrl + C, Ctrl + V

from src.scripts.surface_reposition import SurfaceReposition  # Reposicion de surface
from src.scripts.clicks_detector import ClicksDetector  # Detector de clicks
from src.scripts.fonts import Font  # Para las fuentes


class BoxText:
    """ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE"""
    def __init__(self, event_dict, surface, x, y, w, h, rect_color=(20, 20, 20), text_color=(190, 190, 190), text=""):
        # Profundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"] += 1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Superficie de referencia
        self.presurface = surface
        self.rect_box_color = rect_color

        # Inicializa el rectángulo y sus atributos relacionados
        #self.rect = pg.rect.Rect(0,0,0,0)

        #   DEBERIAMOS GUARDAR LAS DIMENCIONES DEL OBJETO POR SI SE MODIFICA ??

        self.rect = pg.rect.Rect(x,y,w,h)
        self.surface_rect = self.rect
        
        self.surface = SurfaceReposition.surface_reposition(self.presurface, self.rect, self.surface_rect)
        #self.rects_updates(x, y, w, h)

        # Características del cuadro de texto y la fuente
        self.text = text
        self.text_color = text_color
        self.text_surface = Font.surf_font_OpenSans_Medium(self.text, self.text_color)

        # Inicializa el color de la línea del rectángulo
        self.rect_line_color = event_dict["Colors"]["LightGrey"]

        # Configuración del cursor
        base_name, extension = os.path.splitext(self.text)
        self.cursor_position = len(base_name)
        cursor_text = self.text[:self.cursor_position]
        self.cursor_surface = Font.surf_font_OpenSans_Medium(cursor_text, (0, 0, 0))
        self.cursor_show = True  # Mostrar cursor o no
        self.cursor_count = 0  # Contador para controlar la visibilidad del cursor

        # Cálculo del desplazamiento del área de texto
        dis = self.text_surface.get_width() - self.cursor_surface.get_width()
        if self.text_surface.get_width() > self.rect.width:
            self.displace_area_x = self.cursor_surface.get_width() - max(self.rect.width / 2, self.rect.width - dis)
        else:
            self.displace_area_x = -self.rect.width / 2 + self.text_surface.get_width() / 2

        # Signos permitidos
        self.allowed_signs = ["_", "-", ".", ","]

        self.is_editing = False

        # Texto seleccionado
        self.text_selected_list = []
        self.text_selected_rect = pg.Rect(0, 0, 0, 0)
        self.save_displace = 0

        # Configuración para la gestión de eventos de teclado
        self.key_timer = time.time()  # Temporizador para calcular el tiempo transcurrido
        self.key_alarm = 0  # Tiempo entre la primera impresión de un carácter y el segundo
        self.key_count = 0  # Contador para diferenciar la impresión del primer carácter del segundo
        self.key_save = None  # Guarda la última tecla presionada

        # Profundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"] -= 1
        # ----------------------------------------------------------------------------
    #def rects_updates(self, presurface , force = False):
    def rects_updates(self, presurface, x=0, y=0, w=0, h=0 , force = False):
        """Modifica los atributos de los "rects" del objeto, o los reeinicia usarndo "force" """

        if not any([x, y, w, h]) and force == False:
            return
        
        """Inicializa el rectángulo y sus atributos relacionados."""

        # presurface
        # ----------------------------------------------------------------------------
        self.presurface =  presurface
        # ----------------------------------------------------------------------------

        # Rect
        # ----------------------------------------------------------------------------

        # x = self.rect.x
        # y = self.rect.y
        # w = self.rect.width
        # h = self.rect.height

        self.rect.x += x
        self.rect.y += y
        self.rect.width += w
        self.rect.height += h

        # ----------------------------------------------------------------------------
        #self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        #self.rect = pg.rect.Rect(x,y,w,h)
        self.surface_rect = self.rect
        self.surface = SurfaceReposition.surface_reposition(self.presurface, self.rect, self.surface_rect)
        
    def pre_edit(self,event_dict, code = None):
        if code == "selected":
            event_dict["ForceLoop"] = True # fuerza el bucle mientras box_text este activo
            self.is_editing = True # el objeto se esta editando
            self.rect_box_color = (20,20,20)
            self.rect_line_color = event_dict["Colors"]["GreenFluor"]
        if code == "clickable" :
            self.rect_box_color = event_dict["Colors"]["IntermediumGrey"]

    def pos_edit(self,event_dict, code = None):
        # Reset selected
        #-------------------------------------------------------------------------------------
        self.text_selected_list.clear()
        self.text_selected_rect = pg.Rect(0,0,0,0)
        #-------------------------------------------------------------------------------------
        
        if code == "selected":
            event_dict["ForceLoop"] = False # desactiva el forzador de bucle 
            self.is_editing = False # el objeto deja de editarse
            self.rect_line_color = event_dict["Colors"]["LightGrey"]
        if code == "clickable" :
            self.rect_box_color = (20,20,20)

    def edit(self, event_dict, code = None): # metodo de edicion
        """metodo  principal por donde pasa la logica de las interacciones"""
        #-------------------------------------------------------------------------------------
        #if code == "clickable":
        #     self.rect_box_color = event_dict["Colors"]["IntermediumGrey"]

        if code == "selected":
            def init(): # Comienzo del codigo
                #-------------------------------------------------------------------------------------
                def init2():
                    if self.rect.collidepoint(event_dict["Mouse"]["Position"]):
                        event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_IBEAM

                    click()
                    key_pressed()

                def click():# si hago click

                    # mouse x,y con respecto a box text
                    x = event_dict["Mouse"]["Position"][0] - self.rect.x 
                    #y = event_dict["Mouse"]["Position"][1] - self.rect.y

                    #-------------------------------------------------------------------------------------
                    
                    if event_dict["Mouse"]["ClickLeftDown"]: # si hago click dentro de box_text (coordenadas dentro de box_text)
                        
                        # detecto cuantos clicks se han dado en un intervalo de tiempo (500 ms)
                        clicks = ClicksDetector.detect_double_triple_click()
                        
                        if clicks == 1:

                            # Reset selected
                            #-------------------------------------------------------------------------------------
                            self.text_selected_list.clear()
                            self.text_selected_rect = pg.Rect(0,0,0,0)
                            self.cursor_show = True
                            self.cursor_count = 0
                            #-------------------------------------------------------------------------------------

                            x_click_in_surface_text = self.displace_area_x + x 
                            w_text_surface = self.text_surface.get_width()
                            self.cursor_position = 0 # minima posicion del cursor
                            if x_click_in_surface_text >= w_text_surface: # maxima posicion del cursor
                                self.cursor_position = len(self.text)
                            elif x_click_in_surface_text > 0: # posicion del cursor intermedia
                                for i in range(len(self.text)):
                                    t = self.text[:i + 1]
                                    cursor_surface = Font.font_OpenSans_Medium.render(t, True, (0, 0, 0))
                                    if cursor_surface.get_width() >= x_click_in_surface_text:
                                        self.cursor_position = i + 1
                                        break
                            t = self.text[:self.cursor_position]
                            self.cursor_surface = Font.font_OpenSans_Medium.render(t, True, (0, 0, 0))

                        elif clicks == 2:

                            x1, w1 = 0, 0
                            l1, l2 = 1, len(self.text)  # Inicializamos l2 al tamaño total del texto para capturar todo si está al extremo derecho

                            # Buscar el límite izquierdo (hacia atrás desde la posición del cursor)
                            if self.cursor_position > 0:
                                for i in range(self.cursor_position - 1, -1, -1):  # Recorre hacia atrás
                                    if self.text[i] in [" ", "-", ".", "_"]:  # Comparación correcta
                                        text_width, _ = Font.font_OpenSans_Medium.size(self.text[:i + 1])
                                        x1 = text_width
                                        l1 = i + 2  # Ajusta l1 al siguiente carácter después del delimitador
                                        break

                            # Buscar el límite derecho (hacia adelante desde la posición del cursor)
                            for i in range(self.cursor_position, len(self.text)):  # Recorre hacia adelante
                                if self.text[i] in [" ", "-", ".", "_"]:  # Comparación correcta
                                    text_width, _ = Font.font_OpenSans_Medium.size(self.text[:i])
                                    w1 = text_width - x1
                                    l2 = i   # Almacena la posición del delimitador
                                    break
                            else:
                                # Si no se encontró un delimitador hacia adelante, seleccionamos hasta el final del texto
                                text_width, _ = Font.font_OpenSans_Medium.size(self.text)
                                w1 = text_width - x1 # Selecciona hasta el final del texto

                            # Seleccionar el texto entre l1 y l2
                            self.text_selected_list = list(range(l1, l2+1)) # es necesario +1 para dar el ultimo recorrido al bucle
                            # Configurar el rectángulo de selección
                            self.text_selected_rect.x = -self.displace_area_x + x1
                            self.text_selected_rect.y = 0
                            self.text_selected_rect.width = w1  
                            self.text_selected_rect.height = self.rect.height

                        elif clicks == 3:
                            self.text_selected_list = list(range(1, len(self.text) + 1))
                            self.text_selected_rect.x = -self.displace_area_x
                            self.text_selected_rect.y = 0
                            self.text_selected_rect.width = self.text_surface.get_width()
                            self.text_selected_rect.height = self.rect.height


                    elif event_dict["Mouse"]["ClickLeftPressed"]:
                        
                        if event_dict["Mouse"]["Motion"] or self.save_displace != self.displace_area_x:
        
                            # Resetear selección
                            self.text_selected_list.clear()
                            self.text_selected_rect = pg.Rect(0, 0, 0, 0)
                            
                            left_char_w = right_char_w = None

                            # Determinar anchos de los caracteres alrededor del cursor
                            if self.text:
                                if self.cursor_position == 0:
                                    right_char_w = Font.font_OpenSans_Medium.size(self.text[self.cursor_position])[0]
                                elif self.cursor_position == len(self.text):
                                    left_char_w = Font.font_OpenSans_Medium.size(self.text[self.cursor_position - 1])[0]
                                else:
                                    left_char_w = Font.font_OpenSans_Medium.size(self.text[self.cursor_position - 1])[0]
                                    right_char_w = Font.font_OpenSans_Medium.size(self.text[self.cursor_position])[0]

                            # Determinar si el cursor está dentro del área de los caracteres
                            if (left_char_w and (x + self.displace_area_x) < self.cursor_surface.get_width() - left_char_w) or \
                            (right_char_w and (x + self.displace_area_x) > self.cursor_surface.get_width() + right_char_w):
                                cursor_displace = -((-self.displace_area_x + self.cursor_surface.get_width()) - x)
                                dis = self.cursor_surface.get_width() + cursor_displace

                                selected_indices = []
                                if self.cursor_position > 0 and cursor_displace < 0:
                                    # Seleccionar hacia la izquierda
                                    for i in range(self.cursor_position - 1, -1, -1):
                                        text_until_i = self.text[:i]
                                        if Font.font_OpenSans_Medium.size(text_until_i)[0] < dis: break
                                        selected_indices.append(self.cursor_position - (self.cursor_position - i) + 1)
                                elif self.cursor_position < len(self.text) and cursor_displace > 0:
                                    # Seleccionar hacia la derecha
                                    for i in range(self.cursor_position, len(self.text)):
                                        text_until_next = self.text[:i + 1]
                                        if Font.font_OpenSans_Medium.size(text_until_next)[0] >= dis: break
                                        selected_indices.append(i + 1)

                                # Determinar x1 y w1 de una sola pasada
                                x1, w1 = 0, 0
                                text_so_far = ""
                                selection_started = False
                                for num, char in enumerate(self.text):
                                    text_so_far += char
                                    char_width = Font.font_OpenSans_Medium.size(char)[0]
                                    if num + 1 in selected_indices:
                                        if not selection_started:
                                            x1 = Font.font_OpenSans_Medium.size(text_so_far)[0] - char_width
                                            selection_started = True
                                        w1 = Font.font_OpenSans_Medium.size(text_so_far)[0] - x1

                                self.text_selected_rect.x = x1 - self.displace_area_x
                                self.text_selected_rect.y = 0
                                self.text_selected_rect.width = w1
                                self.text_selected_rect.height = self.rect.height

                                if len(selected_indices) > 1 and selected_indices[0] > selected_indices[-1]: 
                                    selected_indices.reverse()
                                self.text_selected_list = selected_indices.copy()
                            

                            # Desplazamiento en x
                            vel = 3
                            self.save_displace = self.displace_area_x # save displace
                            if self.text_surface.get_width() > self.rect.width:
                                if x < 0:
                                    # Desplazar a la izquierda
                                    self.displace_area_x = max(self.displace_area_x - vel, 0)
                                elif x > self.rect.width:
                                    # Desplazar a la derecha
                                    max_displacement = self.text_surface.get_width() - self.rect.width
                                    self.displace_area_x = min(self.displace_area_x + vel, max_displacement)
                            #-------------------------------------------------------------------------------------

                    #-------------------------------------------------------------------------------------
                def key_pressed(): # si preciono una tecla
                     

                    # Si hay teclas presionadas, seleccionamos la última de la lista
                    #-------------------------------------------------------------------------------------
                    modifiers = event_dict["keyPressed"]["Modifiers"]#.copy()
                    shorts = event_dict["keyPressed"]["shortcuts"][-1] if event_dict["keyPressed"]["shortcuts"] else None
                    control = event_dict["keyPressed"]["Control"][-1] if event_dict["keyPressed"]["Control"] else None
                    char = event_dict["keyPressed"]["char"][-1] if event_dict["keyPressed"]["char"] else None

                    key = (char,control,modifiers,shorts)

                    #-------------------------------------------------------------------------------------
                    # guardando el evento de teclado al precionar tecla
                    #-------------------------------------------------------------------------------------
                    if self.key_save != key: 
                        self.key_count = 0 
                        self.key_alarm = 0 
                        self.key_save = key
                    #-------------------------------------------------------------------------------------
                    if char or control or modifiers or shorts: # si preciono alguna tecla

                        #posibilidad de editar texto
                        #-------------------------------------------------------------------------------------
                        t = max(self.key_alarm - round(time.time() - self.key_timer,2),0) # tiempo antes de imprimir otro caracter
                        if t<=0: # gestionar la repeticion de caracteres con la telcla presionada
                            key_down(char,control,modifiers,shorts) # edito el texto
                            self.key_timer = time.time() # guarda hora actual
                            if self.key_count == 0: self.key_alarm = 0.5
                            else: self.key_alarm = 0.05
                            self.key_count = 1
                        #-------------------------------------------------------------------------------------

                        # actualizar superficies 
                        #-------------------------------------------------------------------------------------
                        # superficie del texto
                        self.text_surface = Font.surf_font_OpenSans_Medium(self.text, self.text_color)
                        # superficie hasta el cursor
                        t = self.text[:self.cursor_position]
                        self.cursor_surface = Font.surf_font_OpenSans_Medium(t, (0, 0, 0))
                        #-------------------------------------------------------------------------------------

                        # desplazamiento del area en x
                        #-------------------------------------------------------------------------------------
                        r_w = self.rect.width
                        surf_text_w = self.text_surface.get_width()
                        surf_curs_w = self.cursor_surface.get_width()
                        a_x = self.displace_area_x
                        if surf_text_w > r_w:
                            # flecha izquierda o derecha
                            if surf_curs_w > a_x + r_w: # si salgo de r_w por derecha
                                a_x = surf_curs_w - r_w
                            elif surf_curs_w < a_x : # si salgo de r_w por izquierda
                                a_x = surf_curs_w
                            # borrar
                            if a_x + r_w > surf_text_w:
                                a_x = surf_text_w - r_w
                        else:
                            a_x =   surf_text_w/2 - r_w/2
                        self.displace_area_x = a_x
                        #-------------------------------------------------------------------------------------
                    else: # si dejo de presionar una tecla se reinicia
                        key_up()
                init2() # inicio2
                #-------------------------------------------------------------------------------------
            #-------------------------------------------------------------------------------------
            def key_down(char, control, modifiers, shortcuts):
                def init():

                    # Handle keyboard shortcuts
                    if shortcuts:
                        handle_shortcuts(shortcuts)
                    # Handle control keys
                    elif control:
                        handle_control(control)
                    # Handle character input
                    elif char:
                        handle_character(char)

                #-------------------------------------------------------------------------------------
                def handle_shortcuts(shortcuts):
                    if shortcuts["unicode"] == "\x03":  # Ctrl + C
                        # Copy selected text to clipboard
                        copied_text = ''.join([self.text[i-1] for i in self.text_selected_list])
                        pyperclip.copy(copied_text)
                    elif shortcuts["unicode"] == "\x16":  # Ctrl + V
                        pasted_text = pyperclip.paste()
                        if self.text_selected_list:
                            _replace_selected_text(pasted_text)
                        else:
                            self.text = self.text[:self.cursor_position] + pasted_text + self.text[self.cursor_position:]
                            self.cursor_position += len(pasted_text)

                def handle_control(control):
                    if control['key'] == pg.K_BACKSPACE:
                        if not self.text_selected_list:
                            if self.cursor_position > 0:
                                self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                                self.cursor_position -= 1
                        else:
                            _delete_selected_text()
                        _reset_selection()
                    elif control['key'] == pg.K_LEFT:
                        if self.cursor_position > 0:
                            self.cursor_position -= 1
                        _reset_selection()
                    elif control['key'] == pg.K_RIGHT:
                        if self.cursor_position < len(self.text):
                            self.cursor_position += 1
                        _reset_selection()

                def handle_character(char):
                    if char["unicode"].isalnum() or char["unicode"] in (" ",*self.allowed_signs): # Filtro de caracteres

                        if not self.text_selected_list:
                            self.text = self.text[:self.cursor_position] + char["unicode"] + self.text[self.cursor_position:]
                            self.cursor_position += 1
                        else:
                            _replace_selected_text(char["unicode"])
                #-------------------------------------------------------------------------------------

                def _delete_selected_text():
                    selection_indices = self.text_selected_list
                    if selection_indices:
                        self.text = self.text[:(selection_indices[0] - 1)] + self.text[selection_indices[-1]:]
                        self.cursor_position = max(0, selection_indices[0] - 1)
                    _reset_selection()

                def _replace_selected_text(replacement_text):
                    selection_indices = self.text_selected_list
                    if selection_indices:
                        self.text = self.text[:(selection_indices[0] - 1)] + replacement_text + self.text[selection_indices[-1]:]
                        plus_position = len(replacement_text)
                        self.cursor_position = max(0, selection_indices[0] - 1) + plus_position
                    _reset_selection()

                def _reset_selection():
                    if self.text_selected_list:
                        self.text_selected_list.clear()
                        self.text_selected_rect = pg.Rect(0, 0, 0, 0)
                    self.cursor_show = True
                    self.cursor_count = 0

                # Initialize key handling
                init()

            def key_up():
                self.key_count = 0
                self.key_alarm = 0
            #-------------------------------------------------------------------------------------
            init() # inicio 

    def draw(self,event_dict): 

        # Dibujar el rectángulo del cuadro de texto
        pg.draw.rect(self.presurface, self.rect_box_color, self.rect)
        pg.draw.rect(self.surface, (70, 70, 70), self.text_selected_rect)  # Resaltar texto seleccionado
        pg.draw.rect(self.presurface, self.rect_line_color, self.rect, 1)

        # Coordenadas del cuadro de texto
        # -------------------------------------------------------------------------------------
        r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        rect = pg.Rect(self.displace_area_x, 0, r_w, r_h)
        y = self.rect.height / 2 - self.text_surface.get_height() / 2
        self.surface.blit(self.text_surface, (0, y), rect)
        # -------------------------------------------------------------------------------------

        # Dibujar el rectángulo de edición de texto (si está en modo de edición)
        if self.is_editing:
            # Lógica para el cursor intermitente
            self.cursor_count += 1
            if self.cursor_count >= event_dict["FPS"]["Real"] / 2:  # Cambia el valor según la velocidad deseada del cursor
                self.cursor_show = not self.cursor_show
                self.cursor_count = 0

            # Dibujar el cursor intermitente si no hay texto seleccionado
            if self.cursor_show and not self.text_selected_list:
                cursor_x = self.cursor_surface.get_width() - self.displace_area_x
                cursor_y = 3  # Posición vertical del cursor
                cursor_height = self.text_surface.get_height()
                pg.draw.line(self.surface, (220, 220, 220), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))

