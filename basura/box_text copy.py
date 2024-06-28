import pygame as pg
import sys
import math
import time

import os # crear carpetas, archivos ect..

class BoxText:
    # ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE
    def __init__(self,event_dict,surface,x,y,w,h,color_box = (20,20,20),color_text = (180,180,180), font = pg.font.Font(None, 16), text=""):    
        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        #PreSurface
        self.surface = surface
        # rectangulo de texto
        self.rect = pg.Rect(x,y,w,h)
        #surface
        #self.surface = surface.subsurface(self.rect) #ESTO ES NECESARIOOO????

        # Variables
        # ----------------------------------------------------------------------------
        # caracteristicas del cuadro de texto y la fuente
        self.color_box = color_box
        self.color_text = color_text
        self.font = font
        self.text = text
        # Variables para el cursor intermitente
        self.cursor_show = True # mostrar cursor o no
        self.cursor_count = 0  # Contador para controlar la visibilidad del cursor

        base_name, extension = os.path.splitext(self.text)
        self.cursor_position = len(base_name)
        #self.cursor_position = int(len(self.text)/2) # posiscion del cursor en el texto a la mitad
        t = self.text[:self.cursor_position]
        self.cursor_surface = self.font.render(t, True, (0, 0, 0)) # superficie del cursor en el texto
        self.displace_area_x = 0 # la posicion en x del area que se desplaza por text_surface
        #self.cursor_surface = None#self.font.render(self.text, True, (0, 0, 0)) # superficie del cursor en el texto
        # desplazar el punto x
        self.text_x_displace = 0 # desplazar el punto x del texto cuando el cursor se mueve a izquierda o derecha
        # key_down
        self.key_timer = time.time() # temporizador para calcular el tiempo trascurrido
        self.key_alarm = 0 # tiempo que trascurre entre la primera impresion de un caracter y el segundo
        self.key_count = 0 # contador para diferenciar la impresion del primer caracter del segundo
        self.key_save = None
        # ----------------------------------------------------------------------------


        
        

        
        # coordenadas del box_text
        #-------------------------------------------------------------------------------------
        r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        #-------------------------------------------------------------------------------------
        # Renderiza el texto en una superficie
        self.text_superface = self.font.render(self.text, True, self.color_text)
        # calculando superficie hasta el cursor, de pende de self.cursor_position
        # coordenadas para el texto
        self.text_x = r_x + (r_w - self.text_superface.get_width()) // 2 #- self.text_x_displace
        self.text_y = r_y + (r_h - self.text_superface.get_height()) // 2

        #-------------------------------------------------------------------------------------


        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def reposition(self):
        # coordenadas del box_text
        #-------------------------------------------------------------------------------------
        r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        #-------------------------------------------------------------------------------------
        # Renderiza el texto en una superficie
        """self.text_superface = self.font.render(self.text, True, self.color_text)
        # calculando superficie hasta el cursor, de pende de self.cursor_position
        t = ""
        for i in range(self.cursor_position):
            t += self.text[i]
        self.cursor_surface = self.font.render(t, True, (0, 0, 0))"""
        # modificar "text_x_displace"
        """if self.text_x + self.cursor_surface.get_width() > r_x + r_w:
                self.text_x_displace -= (r_x + r_w) - (self.text_x+ self.cursor_surface.get_width())
        if self.text_x + self.cursor_surface.get_width() < r_x: 
                self.text_x_displace += (self.text_x+  self.cursor_surface.get_width()) - (r_x) """
        # coordenadas para el texto
        self.text_x = r_x + (r_w - self.text_superface.get_width()) // 2 #- self.text_x_displace
        self.text_y = r_y + (r_h - self.text_superface.get_height()) // 2
        #-------------------------------------------------------------------------------------


    def edit(self, event_dict = None): # metodo de edicion

        # Metodos key_down, Key_up
        #-------------------------------------------------------------------------------------
        def Key_down():
            
            # Manejar la tecla de retroceso (borrar)
            if key["key"] == pg.K_BACKSPACE:
                if self.cursor_position > 0:  # Solo si hay texto para borrar
                    # Obtener el carácter a borrar y calcular su ancho
                    delete_char = self.text[self.cursor_position - 1:self.cursor_position]
                    delete_char_rendered = self.font.render(delete_char, True, (0, 0, 0))
                    delete_char_width = delete_char_rendered.get_width()
                    
                    # Ajustar la posición del texto en la GUI
                    if abs(self.text_x_displace) > 5:
                        self.text_x_displace = (abs(self.text_x_displace) - delete_char_width) * math.copysign(1, self.text_x_displace)
                    else:
                        self.text_x_displace = 0
                    
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

        def Key_up():
            self.key_count = 0
            self.key_alarm = 0
        #-------------------------------------------------------------------------------------

        # Comienzo del codigo

        # si hay teclas presionadas seleccionamos la ultima de la lista
        if event_dict["keyPressed"]: key = event_dict["keyPressed"][-1] 
        else: key = None
        # guardando el evento de teclado al precionar tecla
        # si presiono otra tecla mientras haya una presionada se reinicia el contador
        # si dejo de presionar (key_up) los eventtos no coinciden y se reinicia (key_up != None)
        if self.key_save != key: 
            self.key_count = 0 # un contador
            self.key_alarm = 0 # alarma para poder editar el texto
            self.key_save = key


        if key:
            t = max(self.key_alarm - round(time.time() - self.key_timer,2),0) # tiempo antes de imprimir otro caracter
            if t<=0: # gestionar la repeticion de caracteres con la telcla presionada
                Key_down() # edito el texto
                self.key_timer = time.time() # guarda hora actual
                if self.key_count == 0: self.key_alarm = 0.5
                else: self.key_alarm = 0.05
                self.key_count = 1

            # coordenadas del box_text
            #-------------------------------------------------------------------------------------
            r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
            #-------------------------------------------------------------------------------------
            # Renderiza el texto en una superficie
            self.text_superface = self.font.render(self.text, True, self.color_text)
            # calculando superficie hasta el cursor, de pende de self.cursor_position
            t = self.text[:self.cursor_position]
            self.cursor_surface = self.font.render(t, True, (0, 0, 0))
            # modificar "text_x_displace"
            if self.text_x + self.cursor_surface.get_width() > r_x + r_w:
                    self.text_x_displace -= (r_x + r_w) - (self.text_x+ self.cursor_surface.get_width())
            if self.text_x + self.cursor_surface.get_width() < r_x: 
                    self.text_x_displace += (self.text_x+  self.cursor_surface.get_width()) - (r_x) 

            # coordenadas para el texto
            self.text_x = r_x + (r_w - self.text_superface.get_width()) // 2 #- self.text_x_displace
            self.text_y = r_y + (r_h - self.text_superface.get_height()) // 2
            #-------------------------------------------------------------------------------------

        else: # si dejo de presionar una tecla se reinicia
            Key_up()


    def draw(self,event_dict): # cambiar a event_dict!

        # coordenadas del box_text
        #-------------------------------------------------------------------------------------
        r_x, r_y, r_w, r_h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        #-------------------------------------------------------------------------------------


        # Dibuja el cuadro de texto en la pantalla
        pg.draw.rect(self.surface, self.color_box, self.rect)
        #rect gris de las imagenes
        pg.draw.rect(self.surface,(80,80,80),self.rect,1)

        # NO SERIA MEJOR TOMAR LA POSICION DEL CURSOR PARA DEFINIR RECT?
        
        #print(self.cursor_position,self.cursor_surface)
        if self.text_superface.get_width() > r_w:

            # flecha izquierda o derecha
            if self.cursor_surface.get_width() > self.displace_area_x + r_w: # si salgo de r_w por derecha
                self.displace_area_x = self.cursor_surface.get_width() - r_w
            elif self.cursor_surface.get_width() < self.displace_area_x : # si salgo de r_w por izquierda
                self.displace_area_x = self.cursor_surface.get_width()

            # borrar
            if self.displace_area_x + r_w > self.text_superface.get_width():
                self.displace_area_x = self.text_superface.get_width() - r_w

        else:
            self.displace_area_x =   self.text_superface.get_width()/2 -r_w/2

        #self.sup_cur_x = max(min(self.sup_cur_x,self.cursor_surface.get_width()),0)
        rect = pg.Rect(self.displace_area_x,0,r_w,r_h)

        self.surface.blit(self.text_superface, (r_x,r_y+self.text_superface.get_height()/2),rect)

        # rectangulo de edicion de texto  (click izquierdo)
        if self in event_dict["EditPoint"]:
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
                cursor_height = self.text_superface.get_height()
                pg.draw.line(self.surface, (220,220,220), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))
