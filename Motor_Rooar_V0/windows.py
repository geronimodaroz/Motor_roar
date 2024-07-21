import pygame as pg
#import sys
from Folder_classes.surface_reposition import SurfaceReposition




class Window:

    def __init__(self,event_dict,screen, x, y, w, h):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Rect
        # ----------------------------------------------------------------------------
        self.screen = screen
        self.rect = pg.rect.Rect(x,y,w,h) # rect
        self.color = (90,90,90) # color
        #self.surface_rect = pg.rect.Rect(x,y,w,h) # surface rect
        #self.surface =  self.screen.subsurface(self.surface_rect) # surface
        # ----------------------------------------------------------------------------
        # scale_modifier
        # ----------------------------------------------------------------------------
        x = self.rect.x#0
        y = self.rect.y#0
        w = self.rect.width
        h = self.rect.height

        self.scale_modifier_rect = pg.rect.Rect(x,y,w,h) # scale_modifier_rect
        #self.scale_modifier_surface_rect = pg.rect.Rect(x,y,w,h) # scale_modifier_surface_rect
        #self.scale_modifier_surface = self.surface.subsurface(self.scale_modifier_surface_rect) # scale_modifier_surface
        self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_right = self.scale_modifier_hit_left = False
        self.scale_modifier_bar = 15
        self.scale_modifier_margin = 3
        #self.scale_modifier_color = (90,90,90)
        # ----------------------------------------------------------------------------
        # view
        # ----------------------------------------------------------------------------
        margin = self.scale_modifier_margin
        bar = self.scale_modifier_bar

        x = self.scale_modifier_rect.x + margin
        y = self.scale_modifier_rect.y + bar
        w = self.scale_modifier_rect.width - (margin*2) 
        h = self.scale_modifier_rect.height - (margin) - bar

        self.view_rect = pg.rect.Rect(x,y,w,h) # view_rect
        self.view_surface_rect = pg.rect.Rect(x,y,w,h) # view_surface_rect
        self.surface_reposition # reposicion de la superficie view
        #self.view_surface = self.screen.subsurface(self.view_surface_rect) # view_surface
        self.view_color = (5,5,5)
    
        # ----------------------------------------------------------------------------
        # scroll_bar
        # ----------------------------------------------------------------------------
        x = self.view_rect.x + self.view_rect.w - 11
        y = self.view_rect.y
        w = 11
        h = self.view_rect.h

        self.scroll_bar_rect = pg.rect.Rect(x,y,w,h) # view_rect
        self.scroll_bar_color =(50,50,50)

        # ----------------------------------------------------------------------------



        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------


    def surface_reposition(self):
        #view
        # ----------------------------------------------------------------------------
        self.view_surface = SurfaceReposition.surface_reposition(self.screen,self.view_rect,self.view_surface_rect)
        # ----------------------------------------------------------------------------
    

    def collision_detector(self,event_dict):
        # INFO:
        # ----------------------------------------------------------------------------
        # ESTE METODO ME INDICA CON QUE SECCION DEL OBJETO "SELF" ESTOY COLISIONANDO Y LO AGREGARA A LA LISTA "CLICKABLE"
        # 1: self.edit
        # 2: self.scale_modifier + variable de seccion "self.hit_scale_modifier_(top,down,left,right)"
        # ----------------------------------------------------------------------------

        #MousePosition - (x,y)
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0] #- self.rect.x
        mouse_y = event_dict["Mouse"]["MousePosition"][1] #- self.rect.y
        # ----------------------------------------------------------------------------

        
        
        # METODO INICIADOR
        def init():


            #Mouse Position Detection
            # ----------------------------------------------------------------------------
            if self.view_rect.collidepoint(mouse_x,mouse_y): # rect (1)

                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # cambio cursor a flecha 

                del event_dict["EditableObjects"]["clickable"][self.depth_number:]
                event_dict["EditableObjects"]["clickable"].append(self.edit)

            elif self.scale_modifier_rect.collidepoint(mouse_x,mouse_y): # rect scale_modifier (2)

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
            #del event_dict["EditableObjects"]["clickable"][self.depth_number:]
            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)
            # ----------------------------------------------------------------------------

            # comprobamos que seccion del "rect_scale_modifier" esta colisionando y Modificamos icono del cursor
            # ----------------------------------------------------------------------------

            margin = self.scale_modifier_margin #margen "5"
            bar = self.scale_modifier_bar

            x = self.scale_modifier_rect.x
            y = self.scale_modifier_rect.y
            w = self.scale_modifier_rect.width
            h = self.scale_modifier_rect.height

            hit_top = mouse_y <= y + bar
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin

            self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False

            # if hit_top and hit_left:
            #     self.scale_modifier_hit_top = self.scale_modifier_hit_left = True
            #     event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            # elif hit_top and hit_right:
            #     self.scale_modifier_hit_top = self.scale_modifier_hit_right = True
            #     event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            if hit_top:
                self.scale_modifier_hit_top = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
            elif hit_down and hit_right:
                self.scale_modifier_hit_down = self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_down and hit_left:
                self.scale_modifier_hit_down = self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down:
                self.scale_modifier_hit_down = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left:
                self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            elif hit_right:
                self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            
            # ----------------------------------------------------------------------------
        
        init() # iniciamos


    


    def scale_modifier(self,event_dict):

        if event_dict["Mouse"]["Motion"]:

            Mouse_motion_x = event_dict["Mouse"]["Motion"][0]
            Mouse_motion_y = event_dict["Mouse"]["Motion"][1]

            limit = 150


            if self.scale_modifier_hit_top: # TOP

                self.rect.x += Mouse_motion_x # rect 
                self.rect.y += Mouse_motion_y
                self.scale_modifier_rect.x += Mouse_motion_x # scale_modifie
                self.scale_modifier_rect.y += Mouse_motion_y
                self.view_rect.x += Mouse_motion_x # view_rect
                self.view_rect.y += Mouse_motion_y
                self.view_surface_rect.x = self.view_rect.x
                self.view_surface_rect.y = self.view_rect.y

            elif self.scale_modifier_hit_down: # DOWN

                if self.rect.height + Mouse_motion_y > limit:

                    self.rect.height += Mouse_motion_y # rect
                    self.scale_modifier_rect.height += Mouse_motion_y # scale_modifier
                    self.view_rect.height += Mouse_motion_y # view_rect
                    self.view_surface_rect.height = self.view_rect.height

            if self.scale_modifier_hit_left: # LEFT

                if self.rect.width - Mouse_motion_x > limit:
                    self.rect.width -= Mouse_motion_x # rect
                    self.scale_modifier_rect.width -= Mouse_motion_x # scale_modifier
                    self.view_rect.width -= Mouse_motion_x # view_rect
                    self.view_surface_rect.width = self.view_rect.width#Mouse_motion_x 

                    self.rect.x += Mouse_motion_x 
                    self.scale_modifier_rect.x += Mouse_motion_x 
                    self.view_rect.x += Mouse_motion_x 
                    self.view_surface_rect.x = self.view_rect.x
                else:
                    margin = self.scale_modifier_margin
                    Mouse_motion_x = limit - self.rect.width
                    
                    self.rect.width = limit # rect
                    self.scale_modifier_rect.width = limit # scale_modifier
                    self.view_rect.width = limit - (margin*2)# view_rect
                    self.view_surface_rect.width = limit - (margin*2) # Mouse_motion_x 

                    self.rect.x -= Mouse_motion_x
                    self.scale_modifier_rect.x -= Mouse_motion_x
                    self.view_rect.x -= Mouse_motion_x
                    self.view_surface_rect.x -= Mouse_motion_x

            elif self.scale_modifier_hit_right: # RIGHT

                if self.rect.width + Mouse_motion_x > limit:

                    self.rect.width += Mouse_motion_x # rect
                    self.scale_modifier_rect.width += Mouse_motion_x # scale_modifier
                    self.view_rect.width += Mouse_motion_x # view_rect
                    self.view_surface_rect.width = self.view_rect.width
            

            
            

            # # scale_modifier
            # # ----------------------------------------------------------------------------
            # x = self.rect.x
            # y = self.rect.y
            # w = self.rect.width
            # h = self.rect.height
            # self.scale_modifier_rect = pg.rect.Rect(x,y,w,h) # scale_modifier_rect
            # # ----------------------------------------------------------------------------
            # # view
            # # ----------------------------------------------------------------------------
            # margin = self.scale_modifier_margin
            # bar = self.scale_modifier_bar
            # x = self.scale_modifier_rect.x + margin
            # y = self.scale_modifier_rect.y + bar
            # w = self.scale_modifier_rect.width - (margin*2)
            # h = self.scale_modifier_rect.height - (margin) - bar
            # self.view_rect = pg.rect.Rect(x,y,w,h) # view_rect
            # self.view_surface_rect = pg.rect.Rect(x,y,w,h) # view_surface_rect
            # # ----------------------------------------------------------------------------
            
            self.surface_reposition # reposicion de la superficie view


        # si click up elimino de lista selected a scale modifier
        if event_dict["Mouse"]["MouseClickLeftUp"]:
            self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False
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

        pg.draw.rect(self.screen,self.color,self.rect,0,10) # rect
        #pg.draw.rect(self.screen,(255,0,0),self.scale_modifier_rect,1) # scale_modifier


        pg.draw.rect(self.screen, self.view_color,self.view_rect,0,10) # view
        #pg.draw.rect(self.screen,(255,0,0),self.view_rect,1) # view

        pg.draw.rect(self.screen,self.scroll_bar_color,self.scroll_bar_rect,0,10,0,-1,0,-1) # scroll_bar 
        

        # self.view_surface.blit(self.image,(0,0))
        # if self.view_rect.x < 0:
        #     self.view_surface.blit(self.image,(self.view_rect.x,0))
        

        




#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------WindowBase-------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------


class WindowBase():

    def __init__(self,event_dict,screen, x, y, w, h):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Rect
        # ----------------------------------------------------------------------------
        self.screen = screen
        self.rect = pg.rect.Rect(x,y,w,h) # rect
        self.color = (90,90,90) # color
        # ----------------------------------------------------------------------------
        # view
        # ----------------------------------------------------------------------------
        margin = 5
        bar = 15

        x = self.rect.x + margin
        y = self.rect.y + margin
        w = self.rect.width - (margin*2)
        h = self.rect.height - (margin*2) 

        self.view_rect = pg.rect.Rect(x,y,w,h) # view_rect
        self.view_surface_rect = pg.rect.Rect(x,y,w,h) # view_surface_rect
        self.surface_reposition # reposicion de la superficie view
        #self.view_surface = self.screen.subsurface(self.view_surface_rect) # view_surface
        self.view_color = (5,5,5)
        

        # ----------------------------------------------------------------------------

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------


    def surface_reposition(self):
        #view
        # ----------------------------------------------------------------------------
        self.view_surface = SurfaceReposition.surface_reposition(self.screen,self.view_rect,self.view_surface_rect)
        # ----------------------------------------------------------------------------
    

    def collision_detector(self,event_dict):
        # INFO:
        # ----------------------------------------------------------------------------
        # ESTE METODO ME INDICA CON QUE SECCION DEL OBJETO "SELF" ESTOY COLISIONANDO Y LO AGREGARA A LA LISTA "CLICKABLE"
        # 1: self.edit
        # ----------------------------------------------------------------------------

        #MousePosition - (x,y)
        # ----------------------------------------------------------------------------
        mouse_x = event_dict["Mouse"]["MousePosition"][0] #- self.rect.x
        mouse_y = event_dict["Mouse"]["MousePosition"][1] #- self.rect.y
        # ----------------------------------------------------------------------------

        
        
        # METODO INICIADOR
        def init():


            #Mouse Position Detection
            # ----------------------------------------------------------------------------
            if self.view_rect.collidepoint(mouse_x,mouse_y): # rect (1)

                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW # cambio cursor a flecha 

                del event_dict["EditableObjects"]["clickable"][self.depth_number:]
                event_dict["EditableObjects"]["clickable"].append(self.edit)

        
        init() # iniciamos


    

    def edit(self,event_dict):
        
        print("edit")



    def draw(self,event_dict):

        pg.draw.rect(self.screen,self.color,self.rect,0,10) # rect

        pg.draw.rect(self.screen, self.view_color,self.view_rect,0,10) # view

        