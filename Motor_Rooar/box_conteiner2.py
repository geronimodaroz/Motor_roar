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

        self.scale_modifier_check = False # modificador de escala
        self.scale_modifier_rect_top = pg.rect.Rect(x,y-2,w,4) #top



        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def scale_modifier(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0]  
        mouse_y = event_dict["Mouse"]["MousePosition"][1] 
        # ----------------------------------------------------------------------------


        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZENS)



        if event_dict["Mouse"]["MouseClickLeftDown"]:
            self.scale_modifier_check = True
        if event_dict["Mouse"]["MouseClickLeftUp"]:
            self.scale_modifier_check = False

        if self.scale_modifier_check:
            self.rect.y = mouse_y
            self.surface = self.screen.subsurface(self.rect) # superficie






    def edit(self,event_dict):

        # if self.rect.x < event_dict["Mouse"]["MousePosition"][0] < (self.rect.x + self.rect.width):
        #     print("hola")

        #MousePosition
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        mouse_y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        event_dict["Mouse"]["MousePosition"] = (mouse_x,mouse_y)
        # ----------------------------------------------------------------------------
        
        #top_x = (self.rect.x,self.rect.y,self.rect.x + self.rect.width,self.rect.y+2)



    def draw(self,event_dict):

        pg.draw.rect(self.screen, self.color,self.rect) # box_conteiner


        pg.draw.rect(self.screen, (0,200,0),self.scale_modifier_rect_top,1) # box_conteiner

