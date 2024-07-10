import pygame as pg
import math
import sys



class BoxTextName:
    # ESTA CLASE CREA UN CUADRO DE TEXTO EDITABLE 
    def __init__(self,event_dict,surface,format,name,x,y,width,height,color_box = (255,255,255),color_text = (220,220,220), font = pg.font.Font(None, 18), text=""):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # BOX_TEXT_NAME : SOLO GESTIONA EL NOMBRE DEL OBJETO BOX_TEXT Y LOS UBICA DENTRO DEL RECT CORRESPONDIENTE
        # BOX_TEXT : GESTIONA LA CAJA DE TEXTO
        # AMBOS FUNCIONAN COMO UNO SOLO !



        self.format = format # si es horizontal o vertical

        # nombre
        self.name = name
        self.name_size = font.size(self.name)   # tamaño del nombre
        self.name_width, self.name_height = self.name_size
        # superficie del nombre (para dibujarlo despues)
        self.name_superface = font.render(self.name, True, color_text)


        # ESTO DEPENDE DEL FORMATO 
        # rectangulo de nombre + texto
        if format == 0: # formato horizontal

            # rect
            x = x 
            y = y 
            w = self.name_width + width
            h = height
            self.rect = pg.Rect(x,y,w,h)

            #box_text (posicion dentro de rect)
            x = self.name_width
            y = 0
            w = width #- self.name_width
            h = height

        elif format == 1: # formato vertical

            #rect
            x = x
            y = y 
            w = width 
            h = self.name_height + height #+ 2
            self.rect = pg.Rect(x,y,w,h)

            #box_text (posicion dentro de rect)
            x = 0
            y = self.name_height #+ 2
            w = width
            h = height


        # posicion de nombre
        if self.format == 0: # formato horizontal
            self.namex = 0
            self.namey = (self.rect.height/2) - (self.name_height/2)
        elif self.format == 1: # formato vertical
            self.namex = (self.rect.width/2)-(self.name_width/2)
            self.namey = 0
        
        # superficie del rect 
        self.surface = surface.subsurface(self.rect)

        from Folder_box_text_name.box_text import BoxText
        self.box_text = BoxText(event_dict,self.surface,x,y,w,h,color_box)


        # guarda opsicion de name y box_text dentro del rect
        # --------------------------------------------------------------------------
        self.save_namey = self.namey
        self.save_box_text_rect_y = self.box_text.rect.y
        # --------------------------------------------------------------------------


        # VARIABLES DE REPOSICION
        # --------------------------------------------------------------------------
        self.save_rect_y = self.rect.y # guardamos posicion y de self.rect
        self.save_rect_height = self.rect.height # guardamos height de self.rect
        # posicion en y de box_sprite_loader arriba y abajo
        self.top_y = 0
        self.down_y = self.rect.height
        # --------------------------------------------------------------------------

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------


    def reposition(self):
        # reposiciono superficie de "box_text" que es igual a la de "box_text_name"
        self.box_text.surface = self.surface
        # reposiciono los elementos de self.rect.y
        # ---------------------------------------------------------------------------------
        self.namey = self.top_y + self.save_namey # name y
        self.box_text.rect.y = self.top_y + self.save_box_text_rect_y # box_text y
        # ---------------------------------------------------------------------------------



    def edit(self, event_dict = None): # metodo de edicion

        save_x_y = event_dict["MouseClickLeft"]

        if event_dict["MouseClickLeft"]:

            x = event_dict["MouseClickLeft"][0] - self.rect.x 
            y = event_dict["MouseClickLeft"][1] - self.rect.y

            event_dict["MouseClickLeft"] = (x,y)


        self.box_text.edit(event_dict)
        
        event_dict["MouseClickLeft"] = save_x_y





    def draw(self,edit):

        
        pg.draw.rect(self.surface, (90,90,90),(0,0,self.rect.width,self.rect.height),width=1) # rectangulo blanquito

        # nombre
        if self.format == 0: # formato horizontal
            self.surface.blit(self.name_superface,(self.namex,self.namey))

        elif self.format == 1: # formato vertical
            self.surface.blit(self.name_superface, (self.namex,self.namey))

        
        # si box_name_text esta siendo editado y ademas box_text_edit esta siendo editado
        self.box_text.draw(edit) # dibujar box_text



