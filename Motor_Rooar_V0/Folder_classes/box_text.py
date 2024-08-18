import pygame as pg
import sys
import math
import time

import os # crear carpetas, archivos ect..

from Folder_classes.surface_reposition import SurfaceReposition # reposicion de surface
from Folder_classes.utility_classes import ClicksDetector # detector de clicks

class BoxText:
    
    # ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE
    def __init__(self,event_dict,surface,x,y,w,h,rect_color = (20,20,20),text_color = (190,190,190), text_font = pg.font.Font(None, 16), text=""):    
        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # presurface 
        self.presurface = surface
        # Rect
        self.rect = pg.Rect(x,y,w,h)
        self.surface_rect = self.rect
        self.surface = SurfaceReposition.surface_reposition(surface, self.rect, self.surface_rect)
        self.rect_box_color = rect_color
        self.rect_line_color = event_dict["Colors"]["LightGrey"]
        
        # Características del cuadro de texto y la fuente
        self.text = text
        self.text_font = text_font
        self.text_color = text_color
        self.text_surface = self.text_font.render(self.text, True, self.text_color)
        
        
        # cursor
        base_name, extension = os.path.splitext(self.text)
        self.cursor_position = len(base_name)
        cursor_text = self.text[:self.cursor_position]
        self.cursor_surface = self.text_font.render(cursor_text, True, (0, 0, 0))
        self.cursor_show = True  # Mostrar cursor o no
        self.cursor_count = 0  # Contador para controlar la visibilidad del cursor

        # text selected
        self.text_selected_list = []
        self.text_selected_rect = pg.Rect(0,0,0,0)
        self.text_selected_flag = "" # bandera para detectar si la seleccion se hace con doble click o con desplazamiento del mouse


        # Cálculo del desplazamiento del área de texto
        dis = self.text_surface.get_width() - self.cursor_surface.get_width()
        if self.text_surface.get_width() > self.rect.width:
            self.displace_area_x = self.cursor_surface.get_width() - max(self.rect.width / 2, self.rect.width - dis)
        else:
            self.displace_area_x = -self.rect.width / 2 + self.text_surface.get_width() / 2

        # Configuración para la gestión de eventos de teclado
        self.key_timer = time.time()  # Temporizador para calcular el tiempo transcurrido
        self.key_alarm = 0  # Tiempo entre la primera impresión de un carácter y el segundo
        self.key_count = 0  # Contador para diferenciar la impresión del primer carácter del segundo
        self.key_save = None  # Guarda la última tecla presionada

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def pre_edit(self,event_dict, code = None):
        if code == "selected":
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
            self.rect_line_color = event_dict["Colors"]["LightGrey"]
        if code == "clickable" :
            self.rect_box_color = (20,20,20)

    def edit(self, event_dict, code = None): # metodo de edicion
        #-------------------------------------------------------------------------------------
        # if code == "clickable":
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

                    # if event_dict["Mouse"]["ClickLeftDoubleClick"]: # HACER DOBLE CLICK EN EL OBJETO?
                        
                    #     #if not(self.text_selected_list):
                    #     for i in range(1,len(self.text)+1):
                    #         self.text_selected_list.append(i)
                    #     # for num,char in enumerate(self.text):
                    #     #     self.text_selected_list.append(num+1)
                    #     self.text_selected_rect.x = -self.displace_area_x
                    #     self.text_selected_rect.y = 0
                    #     self.text_selected_rect.width = self.text_surface.get_width()
                    #     self.text_selected_rect.height = self.rect.height
                    #     # else:
                    #     #     self.text_selected_list.clear()
                    #     #     self.text_selected_rect = pg.Rect(0,0,0,0)

                    
                    #-------------------------------------------------------------------------------------
                    
                    if event_dict["Mouse"]["ClickLeftDown"]: # si hago click dentro de box_text (coordenadas dentro de box_text)
                        
                        # detecto cuantos clicks se han dado en un intervalo de tiempo (500 ms)
                        clicks = ClicksDetector.detect_double_click()
                        

                        if clicks == 1:
                            print("Clic simple")
                        elif clicks == 2:
                            print("Doble clic")
                        elif clicks == 3:
                            print("Triple clic")
                            
                        #print(self.text_selected_flag)
                        self.text_selected_flag = ""
                        
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
                                    cursor_surface = self.text_font.render(t, True, (0, 0, 0))
                                    if cursor_surface.get_width() >= x_click_in_surface_text:
                                        self.cursor_position = i + 1
                                        break
                            t = self.text[:self.cursor_position]
                            self.cursor_surface = self.text_font.render(t, True, (0, 0, 0))

                        elif clicks == 2:
                            
                            self.text_selected_flag = "double_click"

                            for i in range(1,len(self.text)+1):
                                self.text_selected_list.append(i)
                            # for num,char in enumerate(self.text):
                            #     self.text_selected_list.append(num+1)
                            self.text_selected_rect.x = -self.displace_area_x
                            self.text_selected_rect.y = 0
                            self.text_selected_rect.width = self.text_surface.get_width()
                            self.text_selected_rect.height = self.rect.height




                    elif event_dict["Mouse"]["ClickLeftPressed"] and self.text_selected_flag != "double_click": # si mantengo click dentro de box_text (coordenadas dentro de box_text)

                        # Reset selected
                        #-------------------------------------------------------------------------------------
                        self.text_selected_flag = "pressed_click"
                        self.text_selected_list.clear()
                        self.text_selected_rect = pg.Rect(0,0,0,0)
                        #-------------------------------------------------------------------------------------
                        
                        # Determinar el ancho de los caracteres adyacentes al cursor
                        left_char_w = right_char_w = None

                        if self.text:
                            if self.cursor_position == 0:
                                right_char_w = self.text_font.size(self.text[self.cursor_position])[0]
                            elif self.cursor_position == len(self.text):
                                left_char_w = self.text_font.size(self.text[self.cursor_position - 1])[0]
                            else:
                                left_char_w = self.text_font.size(self.text[self.cursor_position - 1])[0]
                                right_char_w = self.text_font.size(self.text[self.cursor_position])[0]
                            
                        # Verificar la posición del cursor en relación con los caracteres adyacentes
                        if (left_char_w and (x + self.displace_area_x) < self.cursor_surface.get_width() - left_char_w) or \
                        (right_char_w and (x + self.displace_area_x) > self.cursor_surface.get_width() + right_char_w):

                            cursor_displace = -((-self.displace_area_x + self.cursor_surface.get_width()) - x)
                            dis = self.cursor_surface.get_width() + cursor_displace
                            selected_indices = []
                            if self.cursor_position > 0 and cursor_displace < 0:
                                # Calcular índices seleccionados hacia la izquierda
                                for i in range(self.cursor_position - 1, -1, -1):
                                    text_until_i = self.text[:i]
                                    if self.text_font.size(text_until_i)[0] < dis: break
                                    selected_indices.append(self.cursor_position - (self.cursor_position - i) + 1)
                            elif self.cursor_position < len(self.text) and cursor_displace > 0:
                                # Calcular índices seleccionados hacia la derecha
                                for i in range(self.cursor_position, len(self.text)):
                                    text_until_next = self.text[:i + 1]
                                    if self.text_font.size(text_until_next)[0] >= dis: break
                                    selected_indices.append(i + 1)
                            # Calcula x1 y w1 en una sola iteración
                            #-------------------------------------------------------------------------------------
                            x1, w1 = 0, 0
                            text_so_far = ""
                            selection_started = False
                            for num, char in enumerate(self.text):
                                text_so_far += char
                                char_width = self.text_font.size(char)[0]
                                if num + 1 in selected_indices:
                                    if not selection_started:
                                        x1 = self.text_font.size(text_so_far)[0] - char_width
                                        selection_started = True
                                    w1 = self.text_font.size(text_so_far)[0] - x1

                            self.text_selected_rect.x = x1 - self.displace_area_x
                            self.text_selected_rect.y = 0#(self.rect.height - self.text_surface.get_height()) / 2
                            self.text_selected_rect.width = w1
                            self.text_selected_rect.height = self.rect.height#self.text_surface.get_height()

                            if len(selected_indices)>1 and selected_indices[0] > selected_indices[-1]: selected_indices.reverse()

                            self.text_selected_list = selected_indices.copy()

                            #-------------------------------------------------------------------------------------


                        # # Desplazamiento en x
                        # #-------------------------------------------------------------------------------------
                        vel = 3
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
                    key = event_dict["keyPressed"][-1] if event_dict["keyPressed"] else None
                    #-------------------------------------------------------------------------------------
                    # guardando el evento de teclado al precionar tecla
                    #-------------------------------------------------------------------------------------
                    if self.key_save != key: 
                        self.key_count = 0 
                        self.key_alarm = 0 
                        self.key_save = key
                    #-------------------------------------------------------------------------------------
                    if key: # si preciono alguna tecla

                        #posibilidad de editar texto
                        #-------------------------------------------------------------------------------------
                        t = max(self.key_alarm - round(time.time() - self.key_timer,2),0) # tiempo antes de imprimir otro caracter
                        if t<=0: # gestionar la repeticion de caracteres con la telcla presionada
                            Key_down(key) # edito el texto
                            self.key_timer = time.time() # guarda hora actual
                            if self.key_count == 0: self.key_alarm = 0.5
                            else: self.key_alarm = 0.05
                            self.key_count = 1
                        #-------------------------------------------------------------------------------------

                        # actualizar superficies 
                        #-------------------------------------------------------------------------------------
                        # superficie del texto
                        self.text_surface = self.text_font.render(self.text, True, self.text_color)
                        # superficie hasta el cursor
                        t = self.text[:self.cursor_position]
                        self.cursor_surface = self.text_font.render(t, True, (0, 0, 0))
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
                        Key_up()
                
                init2() # inicio2
                #-------------------------------------------------------------------------------------
            #-------------------------------------------------------------------------------------
            def Key_down(key):

                def init():
                    # Manejar la tecla de retroceso (borrar)
                    if key["key"] == pg.K_BACKSPACE:
                        
                        if not self.text_selected_list:  # Si no hay caracteres seleccionados 
                            if self.cursor_position > 0:  # Solo si hay texto para borrar
                                self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                                self.cursor_position -= 1  # Mover el cursor hacia la izquierda
                        else:  # Si hay caracteres seleccionados
                            #_delete_selected_text()
                            _edit_selected_text()

                    # Flecha izquierda
                    elif key["key"] == pg.K_LEFT:
                        if self.cursor_position > 0:
                            self.cursor_position -= 1
                        _reset_selection()

                    # Flecha derecha
                    elif key["key"] == pg.K_RIGHT:
                        if self.cursor_position < len(self.text):
                            self.cursor_position += 1
                        _reset_selection()

                    # Manejar la entrada de caracteres permitidos
                    elif (key["unicode"].isalpha() or
                        key["unicode"].isnumeric() or
                        key["key"] in {pg.K_SPACE, pg.K_UNDERSCORE, pg.K_MINUS, pg.K_PERIOD}):

                        if not self.text_selected_list:
                            # Insertar el nuevo carácter
                            self.text = self.text[:self.cursor_position] + key["unicode"] + self.text[self.cursor_position:]
                            self.cursor_position += 1
                        else:
                            # Reemplazar el texto seleccionado con el nuevo carácter
                            #_replace_selected_text(key["unicode"])
                            _edit_selected_text(key["unicode"])
                    
                def _edit_selected_text(replacement_char=None):
                    """Eliminar o reemplazar el texto seleccionado y ajustar el cursor."""
                    selection_indices = self.text_selected_list
                    if selection_indices:
                        if replacement_char is None:
                            # Eliminar el texto seleccionado
                            self.text = self.text[:(selection_indices[0] - 1)] + self.text[selection_indices[-1]:]
                            self.cursor_position = max(0, selection_indices[0] - 1)
                        else:
                            # Reemplazar el texto seleccionado con el nuevo carácter
                            self.text = self.text[:(selection_indices[0] - 1)] + replacement_char + self.text[selection_indices[-1]:]
                            self.cursor_position = max(0, selection_indices[0] - 1) + 1
                        _reset_selection()

                def _reset_selection():
                    """Resetear la selección de texto y reiniciar el cursor intermitente."""
                    if self.text_selected_list:
                        #self.cursor_position = self.text_selected_list[0]-1 # llevamos el cursor al inicio del cuadro seleccionado 
                        self.text_selected_list.clear()
                        self.text_selected_rect = pg.Rect(0, 0, 0, 0)
                    self.cursor_show = True
                    self.cursor_count = 0
                    
                    
                
                init()
            def Key_up():
                self.key_count = 0
                self.key_alarm = 0
            #-------------------------------------------------------------------------------------
            init() # inicio 


    def draw(self,event_dict): # cambiar a event_dict!

        # coordenadas del box_text
        #-------------------------------------------------------------------------------------
        r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        #-------------------------------------------------------------------------------------
        # box_text
        pg.draw.rect(self.presurface,self.rect_box_color, self.rect)
        pg.draw.rect(self.surface,(70,70,70), self.text_selected_rect) #text_selected
        pg.draw.rect(self.presurface,self.rect_line_color,self.rect,1)

        # if self.cursor_selected_rect:
        #     pg.draw.rect(self.surface,(0,200,0),self.cursor_selected_rect)

        # self.sup_cur_x = max(min(self.sup_cur_x,self.cursor_surface.get_width()),0)

        

        rect = pg.Rect(self.displace_area_x,0,r_w,r_h)
        self.surface.blit(self.text_surface, (0,self.text_surface.get_height()/2),rect)
        #self.surface.blit(self.text_surface, (r_x,r_y+self.text_surface.get_height()/2),rect)

        # rectangulo de edicion de texto  (click izquierdo)
        if self.edit in event_dict["EditableObjects"]["selected"]:
            # rectangulo verde
            #pg.draw.rect(self.presurface, (204,255,0),self.rect,width=1) 

            # Lógica para el cursor intermitente
            self.cursor_count += 1
            if self.cursor_count >= event_dict["FPS"]["Real"]/2:#Cambia el valor según la velocidad deseada del cursor
                self.cursor_show = not self.cursor_show
                self.cursor_count = 0
                
            # Dibuja el cursor intermitente
            if self.cursor_show and not(self.text_selected_list): 
                cursor_x = self.cursor_surface.get_width() - self.displace_area_x
                cursor_y = 3#self.text_y
                cursor_height = self.text_surface.get_height()
                pg.draw.line(self.surface, (220,220,220), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))
