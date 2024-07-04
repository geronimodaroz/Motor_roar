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

        

        self.scale_modifier_rect = pg.rect.Rect(x-5,y-5,w+10,h+10) # modifier rect
        #self.scale_modifier_check = False # modificador de escala



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

        if self.rect.collidepoint(mouse_x,mouse_y): #rect
            event_dict["MouseIcon"] = pg.SYSTEM_CURSOR_ARROW

            if event_dict["Mouse"]["MouseClickLeftDown"]:

                event_dict["EditPoint"].append(self)

                #self.edit(event_dict)

        elif self.scale_modifier_rect.collidepoint(mouse_x,mouse_y): # modifier rect
            event_dict["MouseIcon"] = pg.SYSTEM_CURSOR_SIZENS
        
        #return event_dict


    # def scale_modifier(self,event_dict):

    #     #MousePosition
    #     # ----------------------------------------------------------------------------
    #     mouse_x = event_dict["Mouse"]["MousePosition"][0]  
    #     mouse_y = event_dict["Mouse"]["MousePosition"][1] 
    #     # ----------------------------------------------------------------------------


    #     pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZENS)








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

