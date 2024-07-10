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
        self.rect = pg.rect.Rect(x,y,w,h) # rect
        self.surface = self.screen.subsurface(self.rect) # superficie
        self.color = color

        # modificar escala
        # ----------------------------------------------------------------------------
        self.margin_scale_modifier = 5
        margin = self.margin_scale_modifier
        self.scale_modifier_rect = pg.rect.Rect(x-5,y-5,w+10,h+10) # modifier rect
        #self.scale_modifier_check = False # modificador de escala
        # ----------------------------------------------------------------------------



        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------
    
    def collision_detector(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0]  
        mouse_y = event_dict["Mouse"]["MousePosition"][1] 
        # ----------------------------------------------------------------------------

        #Mouse Position Detection
        # ----------------------------------------------------------------------------
        if self.rect.collidepoint(mouse_x,mouse_y): #rect
            event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # cambio cursor a flecha 
            
            # if event_dict["Mouse"]["MouseClickLeftDown"]: # click down
            #     del event_dict["EditPoint"][self.depth_number:]
            #     event_dict["EditPoint"].append(self.edit)

        elif self.scale_modifier_rect.collidepoint(mouse_x,mouse_y): # modifier rect

            # if event_dict["Mouse"]["MouseClickLeftDown"]: # click down
            #     del event_dict["EditPoint"][self.depth_number:]
            #     event_dict["EditPoint"].append(self.scale_modifier)


            margin = self.margin_scale_modifier #margen "5"

            x = self.scale_modifier_rect.x
            y = self.scale_modifier_rect.y
            w = self.scale_modifier_rect.width
            h = self.scale_modifier_rect.height

            hit_top = mouse_y <= y + margin
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin

            if hit_top and hit_left or hit_down and hit_right: # top,left o down,right
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top and hit_right or hit_down and hit_left: # top,right o down,left
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_top or hit_down: # top, down
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left or mouse_x >= hit_right: # left, right
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
        # ----------------------------------------------------------------------------
        


    def scale_modifier(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0]  
        mouse_y = event_dict["Mouse"]["MousePosition"][1] 
        # ----------------------------------------------------------------------------

        print("scale_modifier")








    def edit(self,event_dict):


        #MousePosition in the object
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        mouse_y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        event_dict["Mouse"]["MousePosition"] = (mouse_x,mouse_y)
        # ----------------------------------------------------------------------------
        print(event_dict["Mouse"]["MousePosition"])



    def draw(self,event_dict):

        pg.draw.rect(self.screen, self.color,self.rect) # box_conteiner


        pg.draw.rect(self.screen, (0,200,0),self.scale_modifier_rect,1) # box_conteiner

