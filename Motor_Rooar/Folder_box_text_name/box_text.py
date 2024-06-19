import pygame as pg
import sys
import math
import time





class BoxText:
    # ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE 
    def __init__(self,surface,x,y,width,height,color_box = (255,255,255),color_text = (220,220,220), font = pg.font.Font(None, 18), text=""):
        
        # NO requiere otra surface

        #superficie
        self.surface = surface

        # rectangulo de texto
        self.rect = pg.Rect(x,y,width,height)

        # caracteristicas del cuadro de texto y la fuente
        self.color_box = color_box
        self.color_text = color_text
        self.font = font
        self.text = text

        # Variables para el cursor intermitente
        self.cursor_show = True # mostrar cursor o no
        self.cursor_timer = 0  # Contador para controlar la visibilidad del cursor
        self.cursor_position = 0 # posiscion del cursor en el texto
        self.cursor_superface = self.font.render("", True, (0, 0, 0)) # superficie del cursor en el texto

        # desplazar el punto x
        self.text_x_displace = 0 # desplazar el punto x del texto cuando el cursor se mueve a izquierda o derecha

        # key_down
        self.key_timer = time.time() # temporizador para calcular el tiempo trascurrido
        self.key_step = 0 # tiempo que trascurre entre la primera impresion de un caracter y el segundo
        self.key_count = 0 # contador para diferenciar la impresion del primer caracter del segundo
        self.key_save = None


        # editamos el bloque de texto o no
        #self.box_text_edit=False



    def edit(self, event_dict = None): # metodo de edicion

        # event_dict: pasa una lista con los eventos

        # Metodos key_down, Key_up
        #-------------------------------------------------------------------------------------
        def Key_down():
            if key["key"] == pg.K_BACKSPACE:
            
                if self.cursor_position > 0: # siempre que haya texto
                    # modifico el valor de "self.text_x_displace" para volver al centro de GUI_rectangle
                    delate_char = self.text[self.cursor_position-1:self.cursor_position]
                    delate_char = self.font.render(delate_char, True, (0, 0, 0))

                    if abs(self.text_x_displace) > 5: self.text_x_displace = (abs(self.text_x_displace) - delate_char.get_width()) * math.copysign(1,self.text_x_displace)
                    else: self.text_x_displace = 0

                    # guardo el nuevo texto antes de posicion_cursor y despues de posicion_cuersor +1
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position-1 +1:]
                    self.cursor_position -= 1 # restamos uno en la posicion del cursor

            elif key["key"] == pg.K_LEFT:

                # Flecha izquierda
                if self.cursor_position > 0: self.cursor_position -= 1
            elif key["key"] == pg.K_RIGHT:

                # Flecha derecha
                if self.cursor_position < len(self.text): self.cursor_position += 1
                
            else:
                # LOS SIMBOLOR PERMITIDOS:
                # key["key"] == pg.K_SPACE   # espacio
                # key["key"] == pg.K_UNDERSCORE # guin bajo
                # key["key"] == pg.K_MINUS # guin bajo
                # key["key"] == pg.K_PERIOD # punto
                    
                if key["unicode"].isalpha() or key["unicode"].isnumeric() or key["key"] == pg.K_SPACE or key["key"] == pg.K_UNDERSCORE or key["key"] == pg.K_MINUS or key["key"] == pg.K_PERIOD:

                    self.text = self.text[:self.cursor_position ] + key["unicode"] + self.text[self.cursor_position :]
                    self.cursor_position += 1
        def Key_up():
            self.key_count = 0
            self.key_step = 0
        #-------------------------------------------------------------------------------------

        # Comienzo del codigo

        # si hay teclas presionadas seleccionamos la ultima de la lista
        key = event_dict["keyPressed"] # lista de teclas presionadas
        if key : # si hay teclas presionadas, seleccionamos la ultima
            key = key[-1]
        else:
            key = None

        # guardando el evento de teclado al precionar tecla
        # si presiono otra tecla mientras haya una presionada se reinicia el contador
        # si dejo de presionar (key_up) los eventtos no coinciden y se reinicia (key_up != None)
        if self.key_save != key: 
            self.key_count = 0
            self.key_step = 0
        self.key_save = key

        # gestionar la repeticion de caracteres con la telcla presionada
        if key:

            t = max(self.key_step - round(time.time() - self.key_timer,2),0) # tiempo antes de imprimir otro caracter
            if t<=0:
                Key_down() # edito el texto
                self.key_timer = time.time()
                if self.key_count == 0: self.key_step = 0.5
                if self.key_count >= 1: self.key_step = 0.05
                self.key_count = 1
        else: # si dejo de presionar una tecla se reinicia
            Key_up()

        return event_dict




    def draw(self,edit):

        # coordenadas del box_text
        #-------------------------------------------------------------------------------------
        t_x = self.rect.x
        t_y = self.rect.y
        t_w = self.rect.width
        t_h = self.rect.height
        #-------------------------------------------------------------------------------------

        # Renderiza el texto en una superficie
        text_superface = self.font.render(self.text, True, self.color_text)

        # coordenadas para el texto
        text_x = t_x + (t_w - text_superface.get_width()) // 2 - self.text_x_displace
        text_y = t_y + (t_h - text_superface.get_height()) // 2

        # calculando superficie hasta el cursor 
        t = ""
        for i in range(self.cursor_position):
            t += self.text[i]
        self.cursor_superface = self.font.render(t, True, (0, 0, 0))

        # modificar "text_x_displace"
        if text_x + self.cursor_superface.get_width() > t_x + t_w:
                self.text_x_displace -= (t_x + t_w) - (text_x+ self.cursor_superface.get_width())
        if text_x + self.cursor_superface.get_width() < t_x: 
                self.text_x_displace += (text_x+  self.cursor_superface.get_width()) - (t_x) 




        # dibujos
                
        # Dibuja el cuadro de texto en la pantalla
        pg.draw.rect(self.surface, self.color_box, self.rect)
        # rect: la parte del texto que se muestra dentro de text_rect

        # NO SERIA MEJOR TOMAR LA POSICION DEL CURSOR PARA DEFINIR RECT?
        rect = pg.Rect(t_x - (text_x),0,t_w,t_h) # vamos bien por aca!
        self.surface.blit(text_superface, (t_x, text_y),rect)
        
        # rectangulo blanquito
        pg.draw.rect(self.surface, (90,90,90), self.rect,width=1) 

        # rectangulo de edicion de texto  (click izquierdo)
        if edit:

            # rectangulo verde
            pg.draw.rect(self.surface, (204,255,0),self.rect,width=1) 

            # Lógica para el cursor intermitente
            self.cursor_timer += 1
            if self.cursor_timer >= 320:#Cambia el valor según la velocidad deseada del cursor
                self.cursor_show = not self.cursor_show
                self.cursor_timer = 0

            # Dibuja el cursor intermitente
            if self.cursor_show:
                t = ""
                for i in range(self.cursor_position):
                    t += self.text[i]
                self.cursor_surface = self.font.render(t, True, (0, 0, 0))
                cursor_x = text_x+ self.cursor_surface.get_width()
                cursor_y = text_y
                cursor_height = text_superface.get_height()
                c = 220
                pg.draw.line(self.surface, (c,c,c), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))

        

        """# ayuda 

        # texto
        x,y = text_x,text_y + text_superface.get_height()
        x_end = x + text_superface.get_width()
        y_end = y 
        pg.draw.line(self.surface, (255, 0, 0), (x,y), (x_end,y_end))

        # cursor
        x,y = text_x,text_y + text_superface.get_height()+5
        x_end = x + self.cursor_superface.get_width()
        y_end = y 
        pg.draw.line(self.surface, (0, 155, 0), (x,y), (x_end,y_end))

        # x
        x,y = 0,text_y + text_superface.get_height()-15
        x_end = x + text_x
        y_end = y 
        pg.draw.line(self.surface, (0, 0, 255), (x,y), (x_end,y_end))

        # mov
        x,y = self.x + self.width/2,text_y + text_superface.get_height()-20
        x_end = x - text_x_displace
        y_end = y 
        pg.draw.line(self.surface, (200, 0, 0), (x,y), (x_end,y_end))

        x=text_x+  self.cursor_superface.get_width()
        pg.draw.line(self.surface, (200, 0, 0), (x,100), (x,100))"""