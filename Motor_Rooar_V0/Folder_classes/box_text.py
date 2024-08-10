import pygame as pg
import sys
import math
import time

import os # crear carpetas, archivos ect..

from Folder_classes.surface_reposition import SurfaceReposition

class BoxText:
    
    # ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE
    def __init__(self,event_dict,surface,x,y,w,h,rect_color = (20,20,20),text_color = (180,180,180), text_font = pg.font.Font(None, 16), text=""):    
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
        self.rect_color = rect_color
        
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

        # Variables para el cursor intermitente
        self.cursor_show = True  # Mostrar cursor o no
        self.cursor_count = 0  # Contador para controlar la visibilidad del cursor
        self.cursor_area_select = False  # Si seleccionamos algún área dentro del texto
        self.cursor_selected_rect = None

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



    def edit(self, event_dict): # metodo de edicion
        #-------------------------------------------------------------------------------------


        #if event_dict["EditableObjects"]["selected"]:

            def init(): # Comienzo del codigo
                #-------------------------------------------------------------------------------------
                
                if self.rect.collidepoint(event_dict["Mouse"]["MousePosition"]):
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_IBEAM
                #     if pg.mouse.get_cursor()[0] != 1:
                #         pg.mouse.set_cursor(pg.SYSTEM_CURSOR_IBEAM)
                # else:
                #     if pg.mouse.get_cursor()[0] == 1:
                #         pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


                x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
                y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
                event_dict["Mouse"]["MousePosition"] = (x,y)


                def click():# si hago click
                    #-------------------------------------------------------------------------------------
                    #save_x_y = event_dict["MouseClickLeft"]
                    
                    if event_dict["Mouse"]["MouseClickLeftDown"]: # si hago click dentro de box_text (coordenadas dentro de box_text)

                        #if self.cursor_displace_if_click: # ESTO HAY QUE MIRAR SI ES NECESARIO !!!

                        x_click_in_surface_text = self.displace_area_x + x #event_dict["MouseClickLeft"][0]
                        
                        w_text_surface = self.text_surface.get_width()

                        self.cursor_position = 0
                        self.cursor_show = True
                        self.cursor_count = 0

                        #if x_click_in_surface_text > 0:
                        if x_click_in_surface_text >= w_text_surface:
                            self.cursor_position = len(self.text)

                        elif x_click_in_surface_text > 0:
                            for i in range(len(self.text)):
                                t = self.text[:i + 1]
                                cursor_surface = self.text_font.render(t, True, (0, 0, 0))
                                if cursor_surface.get_width() >= x_click_in_surface_text:
                                    self.cursor_position = i + 1
                                    break

                        t = self.text[:self.cursor_position]
                        self.cursor_surface = self.text_font.render(t, True, (0, 0, 0))


                    # if event_dict["Mouse"]["MouseClickLeftPressed"]: # si mantengo click dentro de box_text (coordenadas dentro de box_text)

                    #     # x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
                    #     # y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
                    #     # event_dict["Mouse"]["MousePosition"] = (x,y)

                    #     #x_click_in_surface_text = self.displace_area_x + x

                    #     cursor_displace = -((-self.displace_area_x + self.cursor_surface.get_width()) - event_dict["Mouse"]["MousePosition"][0]) # desplazamiento del mouse desde el cursor


                    #     if self.cursor_position > 0 and cursor_displace < 0:
                    #         dis = self.cursor_surface.get_width() + cursor_displace
                    #         pre_char = ""
                    #         for i in range(self.cursor_position - 1, -1, -1):
                    #             t = self.text[:i]
                    #             sup_width = self.text_font.size(t)[0]
                    #             if sup_width < dis:
                    #                 break
                    #             pre_char += self.text[i]

                    #         # x = self.rect.x
                    #         # y = self.rect.y
                    #         # h = self.rect.height
                            
                    #         #self.cursor_selected_rect = pg.Rect(x+cursor_displace,y,self.cursor_surface.get_width(),h)
                    #         print(pre_char[::-1])

                    #     elif self.cursor_position < len(self.text) and cursor_displace > 0:
                    #         dis = self.cursor_surface.get_width() + cursor_displace
                    #         post_char = ""
                    #         for i in range(self.cursor_position, len(self.text)):
                    #             t = self.text[:i + 1]
                    #             sup_width = self.text_font.size(t)[0]
                    #             if sup_width >= dis:
                    #                 break
                    #             post_char += self.text[i]
                    #         print(post_char)

                    #     #self.cursor_area_select = True

                    #     #self.cursor_displace_if_click = True

                    # #event_dict["MouseClickLeft"] = save_x_y
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
                
                click()
                key_pressed()
                #-------------------------------------------------------------------------------------
                    
            
            #-------------------------------------------------------------------------------------
            def Key_down(key):
                
                # Manejar la tecla de retroceso (borrar)
                if key["key"] == pg.K_BACKSPACE:
                    if self.cursor_position > 0:  # Solo si hay texto para borrar
                        # Actualizar el texto eliminando el carácter borrado
                        self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                        self.cursor_position -= 1  # Mover el cursor hacia la izquierda

                # Flecha izquierda
                elif key["key"] == pg.K_LEFT: 
                    if self.cursor_position > 0: 
                        self.cursor_position -= 1
                    self.cursor_show = True
                    self.cursor_count = 0

                # Flecha derecha
                elif key["key"] == pg.K_RIGHT: 
                    if self.cursor_position < len(self.text): 
                        self.cursor_position += 1
                    self.cursor_show = True
                    self.cursor_count = 0
                    
                # Manejar la entrada de caracteres permitidos
                elif (key["unicode"].isalpha() or
                    key["unicode"].isnumeric() or
                    key["key"] in {pg.K_SPACE, pg.K_UNDERSCORE, pg.K_MINUS, pg.K_PERIOD}):
                    # Actualizar el texto insertando el nuevo carácter
                    self.text = self.text[:self.cursor_position] + key["unicode"] + self.text[self.cursor_position:]
                    self.cursor_position += 1
            #-------------------------------------------------------------------------------------

            
            #-------------------------------------------------------------------------------------
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
        pg.draw.rect(self.presurface, self.rect_color, self.rect)
        pg.draw.rect(self.presurface,(80,80,80),self.rect,1)

        # if self.cursor_selected_rect:
        #     pg.draw.rect(self.surface,(0,200,0),self.cursor_selected_rect)

        #self.sup_cur_x = max(min(self.sup_cur_x,self.cursor_surface.get_width()),0)

        rect = pg.Rect(self.displace_area_x,0,r_w,r_h)
        self.presurface.blit(self.text_surface, (r_x,r_y+self.text_surface.get_height()/2),rect)

        # rectangulo de edicion de texto  (click izquierdo)
        if self.edit in event_dict["EditableObjects"]["selected"]:
            # rectangulo verde
            pg.draw.rect(self.surface, (204,255,0),self.rect,width=1) 

            # Lógica para el cursor intermitente
            self.cursor_count += 1
            if self.cursor_count >= 200:#Cambia el valor según la velocidad deseada del cursor
                self.cursor_show = not self.cursor_show
                self.cursor_count = 0
                
            # Dibuja el cursor intermitente
            if self.cursor_show: 
                cursor_x = r_x + self.cursor_surface.get_width() - self.displace_area_x
                cursor_y = r_y+3#self.text_y
                cursor_height = self.text_surface.get_height()
                pg.draw.line(self.surface, (220,220,220), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))
