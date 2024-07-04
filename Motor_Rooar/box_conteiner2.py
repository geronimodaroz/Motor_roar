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
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = color
        self.rect = pg.rect.Rect(x,y,w,h) # rect de box_conteiner
        self.surface = screen.subsurface(self.rect) # superficie de box_conteiner

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------



    def edit(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        
        x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        event_dict["Mouse"]["MousePosition"] = (x,y)
        # ----------------------------------------------------------------------------



    def draw(self,event_dict):

        pg.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h)) # box_conteiner

