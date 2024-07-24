import pygame as pg
#import sys
#import pygame.gfxdraw
from Folder_classes.surface_reposition import SurfaceReposition




class Window:

    def __init__(self,event_dict,screen, x, y, w, h, scroll_bar = 0):

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
        # scale_modifier
        # ----------------------------------------------------------------------------
        x = self.rect.x
        y = self.rect.y
        w = self.rect.width
        h = self.rect.height

        self.scale_modifier_rect = pg.rect.Rect(x,y,w,h) # scale_modifier_rect
        self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_right = self.scale_modifier_hit_left = False
        self.scale_modifier_bar = 15
        self.scale_modifier_margin = 3
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
        #self.view_surface = self.screen.subsurface(self.view_surface_rect) # view_surface
        self.view_surface = SurfaceReposition.surface_reposition(self.screen,self.view_rect,self.view_surface_rect)
        #self.surface_reposition # reposicion de la superficie view
        self.view_color = (5,5,5)

        # ----------------------------------------------------------------------------
        # curtain
        # ----------------------------------------------------------------------------
        if self.view_rect.x < 0:
            x = self.view_rect.x
        else:
            x = 0 
        if self.view_rect.y < 0:
            y = self.view_rect.y
        else:
            y = 0 
        w = self.view_rect.width 
        h = 500 
        self.curtain_color = (150,100,150)
        self.curtain_rect = pg.rect.Rect(x,y,w,h)
        self.curtain_surface_rect = pg.rect.Rect(x,y,w,h)
        #self.curtain_surface = self.view_surface.subsurface(self.curtain_rect)
        self.curtain_surface = SurfaceReposition.surface_reposition(self.view_surface,self.curtain_rect,self.curtain_surface_rect)
        # ----------------------------------------------------------------------------
        # scroll_bar
        # ----------------------------------------------------------------------------
        self.scroll_bar = scroll_bar

        if self.scroll_bar != 0: # si es 0: no existe scroll_bar

            self.scroll_bar_side_hit = False
            self.scroll_bar_side_inside_hit = False
            self.scroll_bar_down_hit = False
            self.scroll_bar_down_inside_hit = False

            self.scroll_bar_color = (40,40,40)
            self.scroll_bar_insid_color = (90,90,90)
            # self.scroll_bar_thickness = 10
            # self.margin_low = 2
            # self.margin_high = 10
            scroll_bar_thickness = 10
            margin_low = 2
            margin_high = 10

            # side
            if self.curtain_rect.height > self.view_rect.height:
                if self.scroll_bar == 1:
                    # right
                    x = self.view_rect.x + self.view_rect.width - scroll_bar_thickness - margin_low
                    y = self.view_rect.y + margin_low + margin_high 
                    w = scroll_bar_thickness 
                    h = self.view_rect.h  - (margin_low*2) - (margin_high*2)
                elif self.scroll_bar == -1:
                    # left 
                    x = self.view_rect.x + margin_low
                    y = self.view_rect.y + margin_low + margin_high 
                    w = scroll_bar_thickness 
                    h = self.view_rect.h  - (margin_low*2) - (margin_high*2)
                self.scroll_bar_side_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_side
                # calculo de proporcion en barra lateral interior
                proportion_hight_insid_bar_side = self.view_rect.height / self.curtain_rect.height
                if self.view_rect.y < 0:
                    proportion_y_insid_bar_side = self.curtain_rect.y - self.view_rect.y
                else:
                    proportion_y_insid_bar_side = self.curtain_rect.y
                x = self.scroll_bar_side_rect.x
                y = self.scroll_bar_side_rect.y - proportion_y_insid_bar_side
                w = self.scroll_bar_side_rect.width
                h = self.scroll_bar_side_rect.height * proportion_hight_insid_bar_side
                self.scroll_bar_side_inside_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_side_inside
            else:
                self.scroll_bar_side_rect = pg.rect.Rect(0,0,0,0) # scroll_bar_side
                self.scroll_bar_side_inside_rect = pg.rect.Rect(0,0,0,0) # scroll_bar_side_inside

            # down
            if self.curtain_rect.width > self.view_rect.width:
                x = self.view_rect.x + margin_low + margin_high
                y = self.view_rect.y + self.view_rect.height - scroll_bar_thickness - margin_low
                w = self.view_rect.width - (margin_low*2) - (margin_high*2)
                h = scroll_bar_thickness
                self.scroll_bar_down_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_down
                # calculo de proporcion en barra inferior interior
                proportion_width_insid_bar_down = self.view_rect.width / self.curtain_rect.width
                if self.view_rect.x < 0:
                    proportion_x_insid_bar_down = self.curtain_rect.x - self.view_rect.x
                else:
                    proportion_x_insid_bar_down = self.curtain_rect.x
                x = self.scroll_bar_down_rect.x - proportion_x_insid_bar_down
                y = self.scroll_bar_down_rect.y
                w = self.scroll_bar_down_rect.width * proportion_width_insid_bar_down
                h = self.scroll_bar_down_rect.height
                self.scroll_bar_down_inside_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_down_inside
            else:
                self.scroll_bar_down_rect = pg.rect.Rect(0,0,0,0) # scroll_bar_down
                self.scroll_bar_down_inside_rect = pg.rect.Rect(0,0,0,0) # scroll_bar_down_inside
            # ----------------------------------------------------------------------------

        self.prueba_r = pg.rect.Rect(750,150,50,100)
        self.prueba_s = self.screen.subsurface(self.prueba_r)

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def rects_repositions(self,x = 0,y = 0,w = 0,h = 0):

        # Rect
        # ----------------------------------------------------------------------------
        self.rect.x += x
        self.rect.y += y
        self.rect.width += w
        self.rect.height += h
        # ----------------------------------------------------------------------------
        # scale_modifier
        # ----------------------------------------------------------------------------
        x = self.rect.x
        y = self.rect.y
        w = self.rect.width
        h = self.rect.height

        self.scale_modifier_rect = pg.rect.Rect(x,y,w,h) # scale_modifier_rect
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
        #self.view_surface = self.screen.subsurface(self.view_surface_rect) # view_surface
        self.view_surface = SurfaceReposition.surface_reposition(self.screen,self.view_rect,self.view_surface_rect)
        #self.surface_reposition # reposicion de la superficie view


        # crear posicion relativa de view_rect!!!


        # ----------------------------------------------------------------------------
        # curtain
        # ----------------------------------------------------------------------------
        if self.view_rect.x < 0:
            x = self.view_rect.x
        else:
            x = 0 
        if self.view_rect.y < 0:
            y = self.view_rect.y
        else:
            y = 0 
        w = self.curtain_rect.width#self.view_rect.width - 40
        h = self.curtain_rect.height#self.view_rect.height - 40
        self.curtain_rect = pg.rect.Rect(x,y,w,h)
        self.curtain_surface_rect = pg.rect.Rect(x,y,w,h)
        #self.curtain_surface = self.view_surface.subsurface(self.curtain_rect)
        self.curtain_surface = SurfaceReposition.surface_reposition(self.view_surface,self.curtain_rect,self.curtain_surface_rect)
        # ----------------------------------------------------------------------------
        # scroll_bar
        # ----------------------------------------------------------------------------

        if self.scroll_bar != 0: # si es 0: no existe scroll_bar
        
            scroll_bar_thickness = 10
            margin_low = 2
            margin_high = 10

            # side
            if self.curtain_rect.height > self.view_rect.height:
                if self.scroll_bar == 1:
                    # right
                    x = self.view_rect.x + self.view_rect.width - scroll_bar_thickness - margin_low
                    y = self.view_rect.y + margin_low + margin_high 
                    w = scroll_bar_thickness 
                    h = self.view_rect.h  - (margin_low*2) - (margin_high*2)
                elif self.scroll_bar == -1:
                    # left 
                    x = self.view_rect.x + margin_low
                    y = self.view_rect.y + margin_low + margin_high 
                    w = scroll_bar_thickness 
                    h = self.view_rect.h  - (margin_low*2) - (margin_high*2)
                self.scroll_bar_side_rect = pg.rect.Rect(x,y,w,h) # view_rect
                # calculo de proporcion en barra lateral interior
                proportion_hight_insid_bar_side = self.view_rect.height / self.curtain_rect.height
                if self.view_rect.y < 0:
                    proportion_y_insid_bar_side = self.curtain_rect.y - self.view_rect.y
                else:
                    proportion_y_insid_bar_side = self.curtain_rect.y
                x = self.scroll_bar_side_rect.x
                y = self.scroll_bar_side_rect.y - proportion_y_insid_bar_side
                w = self.scroll_bar_side_rect.width
                h = self.scroll_bar_side_rect.height * proportion_hight_insid_bar_side
                self.scroll_bar_side_inside_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_side_inside

            # down
            if self.curtain_rect.width > self.view_rect.width:
                x = self.view_rect.x + margin_low + margin_high
                y = self.view_rect.y + self.view_rect.height - scroll_bar_thickness - margin_low
                w = self.view_rect.width - (margin_low*2) - (margin_high*2)
                h = scroll_bar_thickness
                self.scroll_bar_down_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_down_inside
                # calculo de proporcion en barra inferior interior
                proportion_width_insid_bar_down = self.view_rect.width / self.curtain_rect.width
                if self.view_rect.x < 0:
                    proportion_x_insid_bar_down = self.curtain_rect.x - self.view_rect.x
                else:
                    proportion_x_insid_bar_down = self.curtain_rect.x

                x = self.scroll_bar_down_rect.x - proportion_x_insid_bar_down
                y = self.scroll_bar_down_rect.y
                w = self.scroll_bar_down_rect.width * proportion_width_insid_bar_down
                h = self.scroll_bar_down_rect.height
                self.scroll_bar_down_inside_rect = pg.rect.Rect(x,y,w,h) # scroll_bar_down_inside
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
            if self.scroll_bar_side_rect.collidepoint(mouse_x,mouse_y) or self.scroll_bar_down_rect.collidepoint(mouse_x,mouse_y):

                
                # Si existe la profundidad "depth" en la lista "selected"
                exist_depth_in_list_selected = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number
                if exist_depth_in_list_selected:

                    # y el objeto es diferente a self.scale_modifier
                    different_from_self_scale_modifier = event_dict["EditableObjects"]["selected"][self.depth_number] != self.scale_modifier
                    if different_from_self_scale_modifier:
                        # comprobamos que seccion del "rect_scale_modifier" esta colisionando
                        comprobation_section_curtain_displace()
                        #event_dict["EditableObjects"]["clickable"].append(self.curtain_displace)
                else:
                    # si no existe esta "depth" en la lista "selected" la creamos
                    comprobation_section_curtain_displace()
                    #event_dict["EditableObjects"]["clickable"].append(self.curtain_displace)

                # if self.scroll_bar_side_rect.collidepoint(mouse_x,mouse_y):
                #     print("side_bar")
                #     pass
                # elif self.scroll_bar_down_rect.collidepoint(mouse_x,mouse_y):
                #     print("down_bar")
                #     pass

            elif self.view_rect.collidepoint(mouse_x,mouse_y): # rect (1)

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
        
        def comprobation_section_curtain_displace():

            event_dict["EditableObjects"]["clickable"].append(self.curtain_displace)

            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False

            if self.scroll_bar_side_rect.collidepoint(mouse_x,mouse_y):
                self.scroll_bar_side_hit = True
                if self.scroll_bar_side_inside_rect.collidepoint(mouse_x,mouse_y):
                    self.scroll_bar_side_inside_hit = True

            elif self.scroll_bar_down_rect.collidepoint(mouse_x,mouse_y):
                self.scroll_bar_down_hit = True
                if self.scroll_bar_down_inside_rect.collidepoint(mouse_x,mouse_y):
                    self.scroll_bar_down_inside_hit = True
        

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

    def curtain_displace(self,event_dict):


        if event_dict["Mouse"]["Motion"]:

            Mouse_motion_x = event_dict["Mouse"]["Motion"][0]
            Mouse_motion_y = event_dict["Mouse"]["Motion"][1]

            if self.scroll_bar_side_inside_hit:

                self.scroll_bar_side_inside_rect.y += Mouse_motion_y

                if self.scroll_bar_side_inside_rect.y < self.scroll_bar_side_rect.y:
                    Mouse_motion_y = 0 
                    self.scroll_bar_side_inside_rect.y = self.scroll_bar_side_rect.y
                elif self.scroll_bar_side_inside_rect.y + self.scroll_bar_side_inside_rect.height > self.scroll_bar_side_rect.y + self.scroll_bar_side_rect.height:
                     Mouse_motion_y = 0 
                     self.scroll_bar_side_inside_rect.y = self.scroll_bar_side_rect.y + self.scroll_bar_side_rect.height - self.scroll_bar_side_inside_rect.height

                self.curtain_rect.y -= Mouse_motion_y
                self.curtain_surface_rect.y = self.curtain_rect.y
                self.curtain_surface = SurfaceReposition.surface_reposition(self.view_surface,self.curtain_rect,self.curtain_surface_rect)

            elif self.scroll_bar_down_inside_hit:

                self.scroll_bar_down_inside_rect.x += Mouse_motion_x

                if self.scroll_bar_down_inside_rect.x < self.scroll_bar_down_rect.x:
                    Mouse_motion_x = 0 
                    self.scroll_bar_down_inside_rect.x = self.scroll_bar_down_rect.x
                elif self.scroll_bar_down_inside_rect.x + self.scroll_bar_down_inside_rect.width > self.scroll_bar_down_rect.x + self.scroll_bar_down_rect.width:
                     Mouse_motion_x = 0 
                     self.scroll_bar_down_inside_rect.x = self.scroll_bar_down_rect.x + self.scroll_bar_down_rect.width - self.scroll_bar_down_inside_rect.width
                
                self.curtain_rect.x -= Mouse_motion_x
                self.curtain_surface_rect.x = self.curtain_rect.x
                self.curtain_surface = SurfaceReposition.surface_reposition(self.view_surface,self.curtain_rect,self.curtain_surface_rect)



        # si click up elimino de lista selected a scale modifier
        if event_dict["Mouse"]["MouseClickLeftUp"]:

            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
            del event_dict["EditableObjects"]["selected"][self.depth_number:]



    def scale_modifier(self,event_dict):

        if event_dict["Mouse"]["Motion"]:

            Mouse_motion_x = event_dict["Mouse"]["Motion"][0]
            Mouse_motion_y = event_dict["Mouse"]["Motion"][1]

            limit = 150

            if self.scale_modifier_hit_top: # TOP
                self.rects_repositions(Mouse_motion_x,Mouse_motion_y)
            elif self.scale_modifier_hit_down: # DOWN
                if self.rect.height + Mouse_motion_y > limit:
                    self.rects_repositions(h = Mouse_motion_y)
                else:
                    Mouse_motion_y = self.rect.height - limit 
                    self.rects_repositions(h = -Mouse_motion_y)
            if self.scale_modifier_hit_left: # LEFT
                if self.rect.width - Mouse_motion_x > limit:
                    self.rects_repositions(x = Mouse_motion_x,w = -Mouse_motion_x)
                else:
                    Mouse_motion_x = self.rect.width -limit 
                    self.rects_repositions(x = Mouse_motion_x, w = -Mouse_motion_x)
            elif self.scale_modifier_hit_right: # RIGHT
                if self.rect.width + Mouse_motion_x > limit:
                    self.rects_repositions(w = Mouse_motion_x)
                else:
                    Mouse_motion_x = self.rect.width - limit 
                    self.rects_repositions(w = -Mouse_motion_x)

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

        #self.prueba_r.x += 1
        #self.prueba_s = self.screen.subsurface(self.prueba_r)
        

        self.curtain_rect.x += 1
        self.curtain_surface_rect.x = self.curtain_rect.x
        #self.curtain_surface = self.view_surface.subsurface(self.curtain_rect)
        self.curtain_surface = SurfaceReposition.surface_reposition(self.view_surface,self.curtain_rect,self.curtain_surface_rect)
        #print("edit")



    def draw(self,event_dict):

        pg.draw.rect(self.screen,self.color,self.prueba_r,0,10) # rect

        pg.draw.rect(self.screen,self.color,self.rect,0,10) # rect
        #pg.draw.rect(self.screen,(255,0,0),self.scale_modifier_rect,1) # scale_modifier


        pg.draw.rect(self.screen, self.view_color,self.view_rect,0,10) # view
        pg.draw.rect(self.screen,(0,0,255),self.view_surface_rect) # view_surface

        pg.draw.rect(self.view_surface, self.curtain_color,self.curtain_rect) # curtain
        pg.draw.rect(self.view_surface,(255,0,0),self.curtain_surface_rect,1) # curtain
        #pg.draw.rect(self.screen,(255,0,0),self.view_rect,1) # view

        if self.scroll_bar != 0: # si es 0: scroll_bar no existe 
            # scroll_bar_side_inside
            if self.curtain_rect.height > self.view_rect.height:
                pg.draw.rect(self.screen,self.scroll_bar_insid_color,self.scroll_bar_side_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_side_inside_rect
                pg.draw.rect(self.screen,self.scroll_bar_color,self.scroll_bar_side_rect,1,10,-1,-1,-1,-1) # scroll_bar_side_rect
            # scroll_bar_down_inside
            if self.curtain_rect.width > self.view_rect.width:
                pg.draw.rect(self.screen,self.scroll_bar_insid_color,self.scroll_bar_down_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_down_inside_rect
                pg.draw.rect(self.screen,self.scroll_bar_color,self.scroll_bar_down_rect,1,10,-1,-1,-1,-1) # scroll_bar_down_rect
        

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

        