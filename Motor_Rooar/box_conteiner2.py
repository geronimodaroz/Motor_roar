import pygame as pg
import sys
from Folder_classes.reposition import Reposition


class BoxConteiner2:

    def __init__(self,event_dict,screen, x, y, w, h, color):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        self.screen = screen
        self.scale_modifier_rect = pg.rect.Rect(x,y,w,h) # rect
        #self.rect = pg.rect.Rect(x,y,w,h) # rect
        self.scale_modifier_surface = self.screen.subsurface(self.scale_modifier_rect) # superficie

        self.hit_scale_modifier_top = False
        self.hit_scale_modifier_down = False
        self.hit_scale_modifier_right = False
        self.hit_scale_modifier_left = False

        self.color = color


        # view
        # ----------------------------------------------------------------------------
        self.margin_scale_modifier = 5
        margin = self.margin_scale_modifier
        #self.scale_modifier_rect = pg.rect.Rect(x-(margin),y-(margin),w+(margin*2),h+(margin*2)) # modifier rect
        self.view_rect = pg.rect.Rect((margin),(margin),w-(margin*2),h-(margin*2)) # modifier rect
        self.view_surface = self.scale_modifier_surface.subsurface(self.view_rect) # superficie
        # ----------------------------------------------------------------------------



        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------
    
    def collision_detector(self,event_dict):

        # INFO:
        # ----------------------------------------------------------------------------
        # ESTE METODO ME INDICA CON QUE SECCION DEL OBJETO "SELF" ESTOY COLISIONANDO Y LO AGREGARA A LA LISTA "CLICKABLE"
        # 1: self.edit
        # 2: self.scale_modifier + variable de seccion "self.hit_scale_modifier_(top,down,left,right)"
        # ----------------------------------------------------------------------------

        #MousePosition - Pantalla principal (x,y)
        # ----------------------------------------------------------------------------
        #mouse_x = event_dict["Mouse"]["MousePosition"][0] - self.scale_modifier_rect.x
        #mouse_y = event_dict["Mouse"]["MousePosition"][1] - self.scale_modifier_rect.y
        # ----------------------------------------------------------------------------

        # METODO INICIADOR
        def init():

            #Mouse Position Detection
            # ----------------------------------------------------------------------------

            #MousePosition - scale_modifier_rect (x,y)
            # ----------------------------------------------------------------------------
            mouse_x = event_dict["Mouse"]["MousePosition"][0] - self.scale_modifier_rect.x
            mouse_y = event_dict["Mouse"]["MousePosition"][1] - self.scale_modifier_rect.y
            # ----------------------------------------------------------------------------

            if self.view_rect.collidepoint(mouse_x,mouse_y): # rect (1)

                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # cambio cursor a flecha 

                del event_dict["EditableObjects"]["clickable"][self.depth_number:]
                event_dict["EditableObjects"]["clickable"].append(self.edit)

            else: #self.scale_modifier_rect.collidepoint(mouse_x,mouse_y): # rect scale_modifier (2)

                # Si existe la profundidad "depth" en la lista "selected"
                exist_depth_in_list_selected = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number
                if exist_depth_in_list_selected:

                    # y el objeto es diferente a self.scale_modifier
                    different_from_self_scale_modifier = event_dict["EditableObjects"]["selected"][self.depth_number] != self.scale_modifier
                    if different_from_self_scale_modifier:
                        # comprobamos que seccion del "rect_scale_modifier" esta colisionando
                        comprobation_section_scale_modifier()
                else:
                    # si no existe esta "depth" en la lista "selected" la creamos
                    comprobation_section_scale_modifier()
            # ----------------------------------------------------------------------------
        
        
        # METODO DE COMPROBACION DE SECCION DEL MODIFICADOR DE ESCALA
        def comprobation_section_scale_modifier():
            
            # eliminamos elementos del "depth" en lista "clickable" si los hubiera y agregamos "self.scale_modifier"
            # ----------------------------------------------------------------------------
            del event_dict["EditableObjects"]["clickable"][self.depth_number:]
            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)
            # ----------------------------------------------------------------------------

            # comprobamos que seccion del "rect_scale_modifier" esta colisionando y Modificamos icono del cursor
            # ----------------------------------------------------------------------------

            #MousePosition - Pantalla principal (x,y) --- ESTO LO PUEDO CAMBIAR !!! A scale_modifier_rect (x,y)
            # ----------------------------------------------------------------------------
            mouse_x = event_dict["Mouse"]["MousePosition"][0] 
            mouse_y = event_dict["Mouse"]["MousePosition"][1] 
            # ----------------------------------------------------------------------------

            margin = self.margin_scale_modifier #margen "5"

            x = self.scale_modifier_rect.x
            y = self.scale_modifier_rect.y
            w = self.scale_modifier_rect.width
            h = self.scale_modifier_rect.height

            hit_top = mouse_y <= y + margin
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin

            self.hit_scale_modifier_top = self.hit_scale_modifier_down = self.hit_scale_modifier_left = self.hit_scale_modifier_right = False

            if hit_top and hit_left:
                self.hit_scale_modifier_top = self.hit_scale_modifier_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_down and hit_right:
                self.hit_scale_modifier_down = self.hit_scale_modifier_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top and hit_right:
                self.hit_scale_modifier_top = self.hit_scale_modifier_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down and hit_left:
                self.hit_scale_modifier_down = self.hit_scale_modifier_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_top:
                self.hit_scale_modifier_top = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_down:
                self.hit_scale_modifier_down = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left:
                self.hit_scale_modifier_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            elif hit_right:
                self.hit_scale_modifier_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            
            # ----------------------------------------------------------------------------
        
        init() # iniciamos

    


    def scale_modifier(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0]  
        mouse_y = event_dict["Mouse"]["MousePosition"][1] 
        # ----------------------------------------------------------------------------

        if event_dict["Mouse"]["Motion"]:

            Mouse_motion_x = event_dict["Mouse"]["Motion"][0]
            Mouse_motion_y = event_dict["Mouse"]["Motion"][1]

            if self.hit_scale_modifier_top: # TOP
                self.view_rect.height -= Mouse_motion_y
                self.scale_modifier_rect.height -= Mouse_motion_y
                #self.view_rect.y += Mouse_motion_y
                self.scale_modifier_rect.y += Mouse_motion_y
            elif self.hit_scale_modifier_down: # DOWN
                self.view_rect.height += Mouse_motion_y
                self.scale_modifier_rect.height += Mouse_motion_y
            if self.hit_scale_modifier_left: # LEFT
                self.view_rect.width -= Mouse_motion_x
                self.scale_modifier_rect.width -= Mouse_motion_x
                #self.view_rect.x += Mouse_motion_x
                self.scale_modifier_rect.x += Mouse_motion_x
            elif self.hit_scale_modifier_right: # RIGHT
                self.view_rect.width += Mouse_motion_x
                self.scale_modifier_rect.width += Mouse_motion_x

            
            self.scale_modifier_surface = self.screen.subsurface(self.scale_modifier_rect) # superficie
            self.view_surface = self.scale_modifier_surface.subsurface(self.view_rect) # superficie

        # si click up elimino de lista selected a scale modifier
        if event_dict["Mouse"]["MouseClickLeftUp"]:
            self.hit_scale_modifier_top = self.hit_scale_modifier_down = self.hit_scale_modifier_left = self.hit_scale_modifier_right = False
            del event_dict["EditableObjects"]["selected"][self.depth_number:]

            

        


    def edit(self,event_dict):


        #MousePosition in the object
        # ----------------------------------------------------------------------------
        #mouse_x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        #mouse_y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        #event_dict["Mouse"]["MousePosition"] = (mouse_x,mouse_y)
        # ----------------------------------------------------------------------------
        print("edit")



    def draw(self,event_dict):

        pg.draw.rect(self.screen, (0,200,0),self.scale_modifier_rect) # box_conteiner
        pg.draw.rect(self.scale_modifier_surface, self.color,self.view_rect) # box_conteiner
        

