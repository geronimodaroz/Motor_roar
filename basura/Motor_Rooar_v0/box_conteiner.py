import pygame as pg
import sys
from Folder_classes.reposition import Reposition


class BoxConteiner:

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

        self.object_list = [] # lista de objetos que contiene Box_conteiner

        # primer cuadro de texto
        from Folder_box_text_name.box_text_name  import BoxTextName
        x = 20#self.width/2 - t_w/2    #la mitad de box_conteiner - la mitad de box_text
        y = 18
        w = 200
        h = 20
        self.box_text_name = BoxTextName(event_dict,self.surface,0," Name: ",x,y,w,h,(35,35,35))
        self.object_list.append(self.box_text_name) # agregamos el objeto a la lsta

        # sprite loader
        from Folder_box_sprite_loader.box_sprite_loader import BoxSpriteLoader
        x = 20
        y = 60
        w = self.w - (x*2) 
        h = 250
        self.box_sprite_loader = BoxSpriteLoader(event_dict,self.surface,x,y,w,h,(35,35,35))
        #self.box_sprite_loader.load_images() # carga archivo pickle de imagenes
        self.object_list.append(self.box_sprite_loader)


        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------






    def edit(self,event_dict):

        #MousePosition
        # ----------------------------------------------------------------------------
        x = event_dict["MousePosition"][0] - self.rect.x 
        y = event_dict["MousePosition"][1] - self.rect.y
        event_dict["MousePosition"] = (x,y)
        #print(event_dict["MousePosition"])
        
        x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        event_dict["Mouse"]["MousePosition"] = (x,y)
        # ----------------------------------------------------------------------------


        # Scroll
        # ----------------------------------------------------------------------------
        # si hago clicl en box_conteiner(self) y hago scroll
        if event_dict["EditPoint"][-1] == self and  event_dict["MouseScroll"]:
            #from classes.reposition import Reposition
            if event_dict["MouseScroll"] == 1:
                for obj in self.object_list:
                    Reposition().reposition_y(self,obj,repo_y=30)
            elif event_dict["MouseScroll"] == -1:
                for obj in self.object_list:
                    Reposition().reposition_y(self,obj,repo_y=-30)
        # ----------------------------------------------------------------------------


        # Click
        # ----------------------------------------------------------------------------
        #save_x_y = event_dict["MouseClickLeft"]
        if event_dict["MouseClickLeft"]:
            x = event_dict["MouseClickLeft"][0] - self.rect.x 
            y = event_dict["MouseClickLeft"][1] - self.rect.y
            event_dict["MouseClickLeft"] = (x,y)
            for obj in self.object_list: # repaso la lista de objectos dentro de box_conteiner
                if obj.rect.collidepoint(x,y):
                    try:
                        del event_dict["EditPoint"][self.depth_number+1:]
                    except Exception as e:
                        pass
                    #print(f"Error: {e}")
                    event_dict["EditPoint"].append(obj)
                    break
            else:
                del event_dict["EditPoint"][self.depth_number+1:]
        # ----------------------------------------------------------------------------


        
        try:
            event_dict["EditPoint"][self.depth_number+1].edit(event_dict)
        except Exception as e:
            pass
            #print(f"Error: {e}")



        #event_dict["MouseClickLeft"] = save_x_y





    def draw(self,event_dict):

        pg.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h)) # box_conteiner

        # si box_conteiner esta siendo editado y ademas box_text_name esta siendo editado
        
        #box_text_name
        self.box_text_name.draw(self.box_text_name in event_dict["EditPoint"]) 

        # box_sprite_loader
        self.box_sprite_loader.draw(event_dict) 
