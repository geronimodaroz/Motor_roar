import pygame as pg
import sys
#import pygame.gfxdraw
import ctypes
from ctypes import wintypes
from src.scripts.surface_reposition import SurfaceReposition
from src.scripts.fonts import Font

from typing import Literal


#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------Window---------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------

class Window:
    """crea una ventana que se puede escalar y cerrar"""
    def __init__(self,event_dict,presurface,x:int,y:int,w:int,h:int,curtain_w:int,curtain_h:int,scroll_bar: Literal[0, 1, -1] = 0):

        if w < 200: w = 200 
        if h < 200: h = 200
        if curtain_w < 200: curtain_w = 200 
        if curtain_h < 200: curtain_h = 200 

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Inicializar propiedades
        self.presurface = presurface
        self.rect = pg.rect.Rect(0,0,0,0)
        self.rect_color = event_dict["Colors"]["LightGrey"]#(90, 90, 90)

        # Inicializar scale_modifier
        self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_right = self.scale_modifier_hit_left = False
        self.scale_modifier_bar = 25
        self.scale_modifier_margin = 4

        # Inicializar view
        self.view_color = event_dict["Colors"]["DarkGrey"]#(5, 5, 5)

        # Inicializar curtain
        self.curtain_w = curtain_w
        self.curtain_h = curtain_h
        self.save_curtain_rect_x = 0
        self.save_curtain_rect_y = 0
        self.curtain_color = (150, 100, 150)

        # Inicializar scroll_bar
        self.scroll_bar = scroll_bar
        if self.scroll_bar != 0:
            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
            self.scroll_bar_color = event_dict["Colors"]["IntermediumGrey"]#(40, 40, 40)
            self.scroll_bar_insid_color = event_dict["Colors"]["LightGrey"]#(90, 90, 90)
            self.scroll_bar_thickness = 10
            self.scroll_bar_margin_low = 1
            self.scroll_bar_margin_high = 10

        # Llamar a rects_updates para inicializar rectángulos
        self.rects_updates(presurface, x, y, w, h)


        # Cargar imagen
        self.image = pg.image.load('C:/Users/Usuario/Desktop/Motor_Rooar/Motor_Rooar_V0.01/assets/images/pygame.jpg')


        #update draw
        self.update_draw_Window = True
        self.update_draw_Window_inside = True

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def rects_updates(self, presurface, x=0, y=0, w=0, h=0, force = False):

        #if x == 0 and y == 0 and w == 0 and h == 0: return
        if not any([x, y, w, h]) and force == False:
            return
        
        # presurface - AQUI PRESURFACE NO ES NECESARIA PERO LA PONGO POR COHERENCIA
        # ----------------------------------------------------------------------------
        self.presurface = presurface
        # ----------------------------------------------------------------------------

        # Rect
        # ----------------------------------------------------------------------------
        self.rect.x += x
        self.rect.y += y
        self.rect.width += w
        self.rect.height += h
        # ----------------------------------------------------------------------------

        # scale_modifier
        # ----------------------------------------------------------------------------
        self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # ----------------------------------------------------------------------------

        # quit
        # ----------------------------------------------------------------------------
        x = self.rect.x + self.rect.w - 25
        y = self.rect.y + 5
        w = 15
        h = 15
        self.quit_rect = pg.rect.Rect(x,y,w,h)
        # ----------------------------------------------------------------------------

        # view
        # ----------------------------------------------------------------------------
        margin = self.scale_modifier_margin
        bar = self.scale_modifier_bar
        self.view_rect = pg.rect.Rect(self.rect.x + margin, self.rect.y + bar, self.rect.width - 2 * margin, self.rect.height - margin - bar)
        self.view_surface_rect = self.view_rect.copy()
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)

        self.view_decrement_x = self.view_rect.x if self.view_rect.x < 0 else 0
        self.view_decrement_y = self.view_rect.y if self.view_rect.y < 0 else 0
        # ----------------------------------------------------------------------------

        # curtain
        # ----------------------------------------------------------------------------
        def _adjust_curtain_position(save_pos, dim, view_dim, view_decrement):
            if save_pos + dim < view_dim and save_pos < 0:
                return view_dim - dim + view_decrement, view_dim - dim
            elif save_pos > 0:
                return 0 + view_decrement, 0
            return save_pos + view_decrement, save_pos

        x, self.save_curtain_rect_x = _adjust_curtain_position(self.save_curtain_rect_x, self.curtain_w, self.view_rect.width, self.view_decrement_x)
        y, self.save_curtain_rect_y = _adjust_curtain_position(self.save_curtain_rect_y, self.curtain_h, self.view_rect.height, self.view_decrement_y)
        w = self.curtain_w
        h = self.curtain_h

        self.curtain_rect = pg.rect.Rect(x,y,w,h)
        # ----------------------------------------------------------------------------

        # scroll_bar
        # ----------------------------------------------------------------------------
        if self.scroll_bar != 0:
            # side
            if self.curtain_rect.height > self.view_rect.height:
                if self.scroll_bar == 1:
                    x = self.view_rect.x + self.view_rect.width - self.scroll_bar_thickness - self.scroll_bar_margin_low
                else:
                    x = self.view_rect.x + self.scroll_bar_margin_low
                y = self.view_rect.y + self.scroll_bar_margin_low + self.scroll_bar_margin_high
                w = self.scroll_bar_thickness
                h = self.view_rect.height - 2 * self.scroll_bar_margin_low - 2 * self.scroll_bar_margin_high
                self.scroll_bar_side_rect = pg.rect.Rect(x, y, w, h)

                # inside
                self.proportion_hight_insid_bar_side = self.view_rect.height / self.curtain_rect.height
                proportion = abs(self.save_curtain_rect_y)/self.curtain_rect.height
                proportion_y_insid_bar_side = self.scroll_bar_side_rect.height * proportion

                self.scroll_bar_side_inside_rect = pg.rect.Rect(
                    self.scroll_bar_side_rect.x,
                    self.scroll_bar_side_rect.y + proportion_y_insid_bar_side,
                    self.scroll_bar_side_rect.width,
                    self.scroll_bar_side_rect.height * self.proportion_hight_insid_bar_side
                )
            else:
                self.scroll_bar_side_rect = pg.rect.Rect(0, 0, 0, 0)
                self.scroll_bar_side_inside_rect = pg.rect.Rect(0, 0, 0, 0)

            # down
            if self.curtain_rect.width > self.view_rect.width:
                x = self.view_rect.x + self.scroll_bar_margin_low + self.scroll_bar_margin_high
                y = self.view_rect.y + self.view_rect.height - self.scroll_bar_thickness - self.scroll_bar_margin_low
                w = self.view_rect.width - 2 * self.scroll_bar_margin_low - 2 * self.scroll_bar_margin_high
                h = self.scroll_bar_thickness
                self.scroll_bar_down_rect = pg.rect.Rect(x, y, w, h)

                # inside
                proportion_width_insid_bar_down = self.view_rect.width / self.curtain_rect.width
                proportion = abs(self.save_curtain_rect_x)/self.curtain_rect.width
                proportion_x_insid_bar_down = self.scroll_bar_down_rect.width * proportion

                self.scroll_bar_down_inside_rect = pg.rect.Rect(
                    self.scroll_bar_down_rect.x + proportion_x_insid_bar_down,
                    self.scroll_bar_down_rect.y,
                    self.scroll_bar_down_rect.width * proportion_width_insid_bar_down,
                    self.scroll_bar_down_rect.height
                )
            else:
                self.scroll_bar_down_rect = pg.rect.Rect(0, 0, 0, 0)
                self.scroll_bar_down_inside_rect = pg.rect.Rect(0, 0, 0, 0)
        # ----------------------------------------------------------------------------

    def collision_detector(self, event_dict):

        mouse_x, mouse_y = event_dict["Mouse"]["Position"] # Obtención de la posición del ratón
        
        def init(): # Inicio del proceso de comprobación
            if self.quit_rect.collidepoint(mouse_x, mouse_y): # quit
                event_dict["EditableObjects"]["clickable"].append(self.delate)
            elif (self.scroll_bar != 0 and (self.scroll_bar_side_rect.collidepoint(mouse_x, mouse_y) or 
                                          self.scroll_bar_down_rect.collidepoint(mouse_x, mouse_y))): # curtain_displace
                comprobation_section_curtain_displace()
            elif self.view_rect.collidepoint(mouse_x, mouse_y): # edit
                event_dict["EditableObjects"]["clickable"].append(self.edit)
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
            elif self.scale_modifier_rect.collidepoint(mouse_x, mouse_y): # scale_modifier
                comprobation_section_scale_modifier()

        def comprobation_section_curtain_displace():

            event_dict["EditableObjects"]["clickable"].append(self.curtain_displace)

            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = False
            self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
            if self.scroll_bar_side_inside_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_side_inside_hit = True
            elif self.scroll_bar_side_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_side_hit = True
            elif self.scroll_bar_down_inside_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_down_inside_hit = True
            elif self.scroll_bar_down_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_down_hit = True
                

        def comprobation_section_scale_modifier():

            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)
            
            margin = self.scale_modifier_margin
            bar = self.scale_modifier_bar
            x, y, w, h = self.scale_modifier_rect
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
            if hit_down and hit_left:
                self.scale_modifier_hit_down = self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down and hit_right:
                self.scale_modifier_hit_down = self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top:
                self.scale_modifier_hit_top = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
            elif hit_down:
                self.scale_modifier_hit_down = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left:
                self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            elif hit_right:
                self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE

        init()

    def delate(self,event_dict, code = None):
        if code == "selected":
            event_dict["Delate_List"].append(self)
            del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def curtain_displace(self,event_dict,code = None):

        def update_vertical(bar, bar_limit, motion, curtain, view_height, is_click):
            if is_click:
                motion = motion - bar.y - (bar.height / 2)
            bar.y += motion
            proportion = view_height / bar.height
            curtain.y = -(bar.y - bar_limit.y) * proportion 
            if bar.y < bar_limit.y or curtain.y > 0:
                bar.y = bar_limit.y
                curtain.y = 0
            elif bar.y + bar.height > bar_limit.y + bar_limit.height or curtain.y + curtain.height < view_height:
                bar.y = bar_limit.y + bar_limit.height - bar.height
                curtain.y = view_height - curtain.height
            self.save_curtain_rect_y = curtain.y # save
            curtain.y += self.view_decrement_y

        def update_horizontal(bar, bar_limit, motion, curtain, view_width, is_click):
            if is_click:
                motion = motion - bar.x - (bar.width / 2)
            bar.x += motion
            proportion = view_width / bar.width
            curtain.x = -(bar.x - bar_limit.x) * proportion
            if bar.x < bar_limit.x or curtain.x > 0:
                bar.x = bar_limit.x
                curtain.x = 0
            elif bar.x + bar.width > bar_limit.x + bar_limit.width or curtain.x + curtain.width < view_width:
                bar.x = bar_limit.x + bar_limit.width - bar.width
                curtain.x = view_width - curtain.width
            self.save_curtain_rect_x = curtain.x # save
            curtain.x += self.view_decrement_x

        # clickeable
        if code == "clickable":

            if event_dict["Mouse"]["Scroll"]:

                if event_dict["Mouse"]["Scroll"] == 1:
                    mouse_scroll_motion_x = 10 
                    mouse_scroll_motion_y = 10
                elif event_dict["Mouse"]["Scroll"] == -1:
                    mouse_scroll_motion_x = -10 
                    mouse_scroll_motion_y = -10

                if self.scroll_bar_side_hit or self.scroll_bar_side_inside_hit:
                    update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_scroll_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        is_click=False
                    )
                elif self.scroll_bar_down_hit or self.scroll_bar_down_inside_hit:
                    update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_scroll_motion_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=False
                    )
            
                self.update_draw_Window_inside = True # update draw inside windows 
                

        # selected
        if code == "selected":

            if event_dict["Mouse"]["ClickLeftDown"]:

                mouse_x, mouse_y = event_dict["Mouse"]["Position"]
                if self.scroll_bar_side_hit:
                    update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_y,
                        self.curtain_rect,
                        self.view_rect.height,
                        is_click=True
                    )
                elif self.scroll_bar_down_hit:
                    update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=True
                    )
                
                self.update_draw_Window_inside = True # update draw inside windows 

            if event_dict["Mouse"]["Motion"]:

                mouse_motion_x, mouse_motion_y = event_dict["Mouse"]["Motion"]
                if self.scroll_bar_side_inside_hit:
                    update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        is_click=False
                    )
                elif self.scroll_bar_down_inside_hit:
                    update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_motion_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=False
                    )
                
                self.update_draw_Window_inside = True # update draw inside windows 

            # si click up elimino de lista selected a scale modifier
            if event_dict["Mouse"]["ClickLeftUp"]:
                #self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
                del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def scale_modifier(self,event_dict, code = None):
        # selected
        if code == "selected":

            if event_dict["Mouse"]["Motion"]:

                Mouse_motion_x, Mouse_motion_y = event_dict["Mouse"]["Motion"]
                limit_min = 150
                limit_max_w = self.curtain_w
                limit_max_h = self.curtain_h

                def limit_motion(motion, current, limit_min, limit_max):
                    if current + motion < limit_min:
                        return limit_min - current
                    if current + motion > limit_max:
                        return limit_max - current
                    return motion
                
                if self.scale_modifier_hit_top:  # TOP
                    self.rects_updates(self.presurface, x=Mouse_motion_x,y=Mouse_motion_y)
                elif self.scale_modifier_hit_down:  # DOWN
                    Mouse_motion_y = limit_motion(Mouse_motion_y, self.view_rect.height, limit_min, limit_max_h)
                    self.rects_updates(self.presurface, h=Mouse_motion_y)
                if self.scale_modifier_hit_left:  # LEFT
                    Mouse_motion_x = limit_motion(-Mouse_motion_x, self.view_rect.width, limit_min, limit_max_w)
                    self.rects_updates(self.presurface, x=-Mouse_motion_x, w=Mouse_motion_x)
                elif self.scale_modifier_hit_right:  # RIGHT
                    Mouse_motion_x = limit_motion(Mouse_motion_x, self.view_rect.width, limit_min, limit_max_w)
                    self.rects_updates(self.presurface, w=Mouse_motion_x)
                
                self.update_draw_Window = True # update_draw
                
            # Reset hit flags on mouse button release
            if event_dict["Mouse"]["ClickLeftUp"]:
                #self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False
                del event_dict["EditableObjects"]["selected"][self.depth_number:]    

    def edit(self,event_dict, code = None):
        # clickeable
        if code == "clickable":

            if event_dict["Mouse"]["Scroll"]:

                if event_dict["Mouse"]["Scroll"] == 1:
                    mouse_scroll_motion_y = 20
                elif event_dict["Mouse"]["Scroll"] == -1:
                    mouse_scroll_motion_y = -20

                def _update_vertical(bar, bar_limit, motion, curtain, view_height):
                    bar.y += motion
                    proportion = view_height / bar.height # ERROR!!!! no div por 0
                    curtain.y = -(bar.y - bar_limit.y) * proportion 
                    if bar.y < bar_limit.y or curtain.y > 0:
                        bar.y = bar_limit.y
                        curtain.y = 0
                    elif bar.y + bar.height > bar_limit.y + bar_limit.height or curtain.y + curtain.height < view_height:
                        bar.y = bar_limit.y + bar_limit.height - bar.height
                        curtain.y = view_height - curtain.height
                    self.save_curtain_rect_y = curtain.y # save
                    curtain.y += self.view_decrement_y

                if self.curtain_rect.height > self.view_rect.height:
                    _update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_scroll_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        )
                
                self.update_draw_Window_inside = True # update draw inside windows 
        # selected
        if code == "selected":
            if event_dict["Mouse"]["ClickLeftUp"]:
                del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def draw(self,event_dict):


        if self.update_draw_Window or True:

            pg.draw.rect(self.presurface,self.rect_color,self.rect,0,10) # rect

            pg.draw.rect(self.presurface,(0,0,0),self.quit_rect,0,10) # quit

            pg.draw.rect(self.presurface, self.view_color,self.view_rect,0,10) # view

            pg.draw.rect(self.view_surface, self.curtain_color,self.curtain_rect) # curtain

            self.update_draw_Window_inside = True
            self.update_draw_Window = False


        
        if self.update_draw_Window_inside:

            # Dibuja la imagen en la pantalla
            x = self.curtain_rect.x 
            y = self.curtain_rect.y 
            self.view_surface.blit(self.image,(x,y))

            x = self.view_rect.x - 4
            y = self.view_rect.y - 4
            w = self.view_rect.w + 8
            h = self.view_rect.h + 8
            pg.draw.rect(self.presurface,event_dict["Colors"]["LightGrey"],(x,y,w,h),4,10,-1,-1,-1,-1) # view

            if self.scroll_bar != 0: # si es 0: scroll_bar no existe 
                # scroll_bar_side_inside
                if self.curtain_rect.height > self.view_rect.height:
                    pg.draw.rect(self.presurface,self.scroll_bar_insid_color,self.scroll_bar_side_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_side_inside_rect
                    pg.draw.rect(self.presurface,self.scroll_bar_color,self.scroll_bar_side_rect,1,10,-1,-1,-1,-1) # scroll_bar_side_rect
                # scroll_bar_down_inside
                if self.curtain_rect.width > self.view_rect.width:
                    pg.draw.rect(self.presurface,self.scroll_bar_insid_color,self.scroll_bar_down_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_down_inside_rect
                    pg.draw.rect(self.presurface,self.scroll_bar_color,self.scroll_bar_down_rect,1,10,-1,-1,-1,-1) # scroll_bar_down_rect
            
        self.update_draw_Window_inside = False

        

#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------WindowBase-------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------

class WindowBase():
    """Crea una ventana que no se puede escalar ni cerrar"""
    def __init__(self,event_dict,presurface,x:int,y:int,w:int,h:int,curtain_w:int,curtain_h:int,scroll_bar: Literal[0, 1, -1] = 0):

        if w < 200: w = 200 
        if h < 200: h = 200
        if curtain_w < 200: curtain_w = 200 
        if curtain_h < 200: curtain_h = 200 

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Inicializar propiedades
        self.presurface = presurface
        self.rect = pg.rect.Rect(0,0,0,0)
        self.rect_color = event_dict["Colors"]["LightGrey"]

        # Inicializar scale_modifier
        self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_right = self.scale_modifier_hit_left = False
        self.scale_modifier_margin = 4

        # Inicializar view
        self.view_color = event_dict["Colors"]["DarkGrey"]

        # Inicializar curtain
        self.curtain_w = curtain_w
        self.curtain_h = curtain_h
        self.save_curtain_rect_x = 0
        self.save_curtain_rect_y = 0
        self.curtain_color = (150, 100, 150)

        # Inicializar scroll_bar
        self.scroll_bar = scroll_bar
        if self.scroll_bar != 0:
            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
            self.scroll_bar_color = event_dict["Colors"]["IntermediumGrey"]
            self.scroll_bar_insid_color = event_dict["Colors"]["LightGrey"]
            self.scroll_bar_thickness = 10
            self.scroll_bar_margin_low = 1
            self.scroll_bar_margin_high = 10

        # objects list
        # ----------------------------------------------------------------------------
        self.objects_list = []
        # ----------------------------------------------------------------------------

        # Llamar a rects_updates para inicializar rectángulos
        self.rects_updates(presurface, x, y, w, h)

        
        # Cargar imagen
        #self.image = pg.image.load('C:/Users/Usuario/Desktop/med.png')

        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------

    def rects_updates(self, presurface, x=0, y=0, w=0, h=0 , force = False):
        """Modifica los atributos de los "rects" del objeto, o los reeinicia usarndo "force" """

        if not any([x, y, w, h]) and force == False:
            return
        
        # presurface - AQUI PRESURFACE NO ES NECESARIA PERO LA PONGO POR COHERENCIA
        # ----------------------------------------------------------------------------
        self.presurface = presurface
        # ----------------------------------------------------------------------------

        # Rect
        # ----------------------------------------------------------------------------
        self.rect.x += x
        self.rect.y += y
        self.rect.width += w
        self.rect.height += h
        # ----------------------------------------------------------------------------

        # scale_modifier
        # ----------------------------------------------------------------------------
        self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # ----------------------------------------------------------------------------

        # view
        # ----------------------------------------------------------------------------
        margin = self.scale_modifier_margin
        self.view_rect = pg.rect.Rect(self.rect.x + margin, self.rect.y + margin, self.rect.width - 2 * margin, self.rect.height - 2 * margin)
        self.view_surface_rect = self.view_rect.copy() # PARA QUE NECESITO ESTO ?? - aca no es necesario por que la ventana no sale de la superficie original, pero si la ventna saliera esto seria necesario
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)

        # self.view_surface_rect y self.view_decrement en este caso no se usan por que la ventana nunca va a salir de la superficie original



        #  SIRVE REALMENTE self.view_decrement ?? - si, sirve si la ventana sale de la superficie original, que en este caso eso no se da 
        #self.view_decrement_x = self.view_rect.x if self.view_rect.x < 0 else 0
        #self.view_decrement_y = self.view_rect.y if self.view_rect.y < 0 else 0


        # ----------------------------------------------------------------------------

        # objects list
        # ----------------------------------------------------------------------------
        #self.objects_list = None
        # ----------------------------------------------------------------------------

        # curtain
        # ----------------------------------------------------------------------------

        def _adjust_curtain_position(save_pos, dim, view_dim, view_decrement):

            if save_pos + dim < view_dim and save_pos < 0:
                return view_dim - dim + view_decrement, view_dim - dim
            
            elif save_pos > 0:
                return 0 + view_decrement, 0
            
            return save_pos + view_decrement, save_pos

        x, self.save_curtain_rect_x = _adjust_curtain_position(self.save_curtain_rect_x, self.curtain_w, self.view_rect.width,0)# self.view_decrement_x)
        y, self.save_curtain_rect_y = _adjust_curtain_position(self.save_curtain_rect_y, self.curtain_h, self.view_rect.height,0)# self.view_decrement_y)
        w = self.curtain_w
        h = self.curtain_h

        self.curtain_rect = pg.rect.Rect(x,y,w,h)
        # ----------------------------------------------------------------------------

        # scroll_bar
        # ----------------------------------------------------------------------------
        if self.scroll_bar != 0:
            # side
            if self.curtain_rect.height > self.view_rect.height:
                if self.scroll_bar == 1:
                    x = self.view_rect.x + self.view_rect.width - self.scroll_bar_thickness - self.scroll_bar_margin_low
                else:
                    x = self.view_rect.x + self.scroll_bar_margin_low
                y = self.view_rect.y + self.scroll_bar_margin_low + self.scroll_bar_margin_high
                w = self.scroll_bar_thickness
                h = self.view_rect.height - 2 * self.scroll_bar_margin_low - 2 * self.scroll_bar_margin_high
                self.scroll_bar_side_rect = pg.rect.Rect(x, y, w, h)

                # inside
                self.proportion_hight_insid_bar_side = self.view_rect.height / self.curtain_rect.height
                proportion = abs(self.save_curtain_rect_y)/self.curtain_rect.height
                proportion_y_insid_bar_side = self.scroll_bar_side_rect.height * proportion

                self.scroll_bar_side_inside_rect = pg.rect.Rect(
                    self.scroll_bar_side_rect.x,
                    self.scroll_bar_side_rect.y + proportion_y_insid_bar_side,
                    self.scroll_bar_side_rect.width,
                    self.scroll_bar_side_rect.height * self.proportion_hight_insid_bar_side
                )
            else:
                self.scroll_bar_side_rect = pg.rect.Rect(0, 0, 0, 0)
                self.scroll_bar_side_inside_rect = pg.rect.Rect(0, 0, 0, 0)

            # down
            if self.curtain_rect.width > self.view_rect.width:
                x = self.view_rect.x + self.scroll_bar_margin_low + self.scroll_bar_margin_high
                y = self.view_rect.y + self.view_rect.height - self.scroll_bar_thickness - self.scroll_bar_margin_low
                w = self.view_rect.width - 2 * self.scroll_bar_margin_low - 2 * self.scroll_bar_margin_high
                h = self.scroll_bar_thickness
                self.scroll_bar_down_rect = pg.rect.Rect(x, y, w, h)

                # inside
                proportion_width_insid_bar_down = self.view_rect.width / self.curtain_rect.width
                proportion = abs(self.save_curtain_rect_x)/self.curtain_rect.width
                proportion_x_insid_bar_down = self.scroll_bar_down_rect.width * proportion

                self.scroll_bar_down_inside_rect = pg.rect.Rect(
                    self.scroll_bar_down_rect.x + proportion_x_insid_bar_down,
                    self.scroll_bar_down_rect.y,
                    self.scroll_bar_down_rect.width * proportion_width_insid_bar_down,
                    self.scroll_bar_down_rect.height
                )
            else:
                self.scroll_bar_down_rect = pg.rect.Rect(0, 0, 0, 0)
                self.scroll_bar_down_inside_rect = pg.rect.Rect(0, 0, 0, 0)
        # ----------------------------------------------------------------------------
# LOAD_OBJECT_NO ESTA ACTIVO
    def load_objects(self,*objects_list):
        pass
        """carga los objetos que estaran dentro de la ventana"""
        #self.objects_list = objects_list # cargar objetos
        #self.objects_list.extend(objects_list)
        
    def collision_detector(self, event_dict):
        """detecta colision con los "rects" del objeto "windows" y con los objetos que contenga dentro, y los agrega a la lista "clickable" """

        mouse_x, mouse_y = event_dict["Mouse"]["Position"] # Obtención de la posición del ratón
        
        def init(): # Inicio del proceso de comprobación

            if (self.scroll_bar != 0 and (self.scroll_bar_side_rect.collidepoint(mouse_x, mouse_y) or 
                                          self.scroll_bar_down_rect.collidepoint(mouse_x, mouse_y))): # curtain_displace
                _comprobation_section_curtain_displace()
            elif self.view_rect.collidepoint(mouse_x, mouse_y): # edit
                _comprobation_section_view_edit()
            # elif self.scale_modifier_rect.collidepoint(mouse_x, mouse_y): # scale_modifier
            #     comprobation_section_scale_modifier()

        def _comprobation_section_view_edit():
            event_dict["EditableObjects"]["clickable"].append(self.edit)
            #event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
            if self.objects_list: # objs

                #x = event_dict["Mouse"]["Position"][0] - self.view_rect.x # mouse x con respecto a view_rect
                #y = event_dict["Mouse"]["Position"][1] - self.view_rect.y # mouse y con respecto a view_rect

                # mouse x,y con respecto a view_rect
                x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
                y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
                save_x_y = event_dict["Mouse"]["Position"]
                event_dict["Mouse"]["Position"] = (x,y)

                for obj in self.objects_list:
                    if obj.rect.collidepoint(x,y): 
                        event_dict["EditableObjects"]["clickable"].append(obj.edit)

                event_dict["Mouse"]["Position"] = save_x_y


        def _comprobation_section_curtain_displace():
            event_dict["EditableObjects"]["clickable"].append(self.curtain_displace)
            self.scroll_bar_side_hit = self.scroll_bar_side_inside_hit = False
            self.scroll_bar_down_hit = self.scroll_bar_down_inside_hit = False
            if self.scroll_bar_side_inside_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_side_inside_hit = True
            elif self.scroll_bar_side_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_side_hit = True
            elif self.scroll_bar_down_inside_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_down_inside_hit = True
            elif self.scroll_bar_down_rect.collidepoint(mouse_x, mouse_y):
                self.scroll_bar_down_hit = True
                
        def comprobation_section_scale_modifier():
            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)
            margin = self.scale_modifier_margin
            x, y, w, h = self.scale_modifier_rect
            hit_top = mouse_y <= y + margin
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin
            self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False
            if hit_top and hit_left:
                self.scale_modifier_hit_top = self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top and hit_right:
                self.scale_modifier_hit_top = self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down and hit_left:
                self.scale_modifier_hit_down = self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
            elif hit_down and hit_right:
                self.scale_modifier_hit_down = self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
            elif hit_top:
                self.scale_modifier_hit_top = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_down:
                self.scale_modifier_hit_down = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
            elif hit_left:
                self.scale_modifier_hit_left = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
            elif hit_right:
                self.scale_modifier_hit_right = True
                event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE

        init()

    def curtain_displace(self,event_dict, code = None):

        def _update_vertical(bar, bar_limit, motion, curtain, view_height, is_click):
            if is_click:
                motion = motion - bar.y - (bar.height / 2)
            bar.y += motion
            proportion = view_height / bar.height
            curtain.y = -(bar.y - bar_limit.y) * proportion 
            if bar.y < bar_limit.y or curtain.y > 0:
                bar.y = bar_limit.y
                curtain.y = 0
            elif bar.y + bar.height > bar_limit.y + bar_limit.height or curtain.y + curtain.height < view_height:
                bar.y = bar_limit.y + bar_limit.height - bar.height
                curtain.y = view_height - curtain.height
            self.save_curtain_rect_y = curtain.y # save
            #curtain.y += self.view_decrement_y

        def _update_horizontal(bar, bar_limit, motion, curtain, view_width, is_click):
            if is_click:
                motion = motion - bar.x - (bar.width / 2)
            bar.x += motion
            proportion = view_width / bar.width
            curtain.x = -(bar.x - bar_limit.x) * proportion
            if bar.x < bar_limit.x or curtain.x > 0:
                bar.x = bar_limit.x
                curtain.x = 0
            elif bar.x + bar.width > bar_limit.x + bar_limit.width or curtain.x + curtain.width < view_width:
                bar.x = bar_limit.x + bar_limit.width - bar.width
                curtain.x = view_width - curtain.width
            self.save_curtain_rect_x = curtain.x # save
            #curtain.x += self.view_decrement_x

        # clickeable
        if code == "clickable":

            if event_dict["Mouse"]["Scroll"]:
                if event_dict["Mouse"]["Scroll"] == 1:
                    mouse_scroll_motion_x = 10 
                    mouse_scroll_motion_y = 10
                elif event_dict["Mouse"]["Scroll"] == -1:
                    mouse_scroll_motion_x = -10 
                    mouse_scroll_motion_y = -10

                if self.scroll_bar_side_hit or self.scroll_bar_side_inside_hit:
                    _update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_scroll_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        is_click=False
                    )
                elif self.scroll_bar_down_hit or self.scroll_bar_down_inside_hit:
                    _update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_scroll_motion_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=False
                    )


        # selected
        if code == "selected":

            if event_dict["Mouse"]["ClickLeftDown"]:
                mouse_x, mouse_y = event_dict["Mouse"]["Position"]
                if self.scroll_bar_side_hit:
                    _update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_y,
                        self.curtain_rect,
                        self.view_rect.height,
                        is_click=True
                    )
                elif self.scroll_bar_down_hit:
                    _update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=True
                    )

            if event_dict["Mouse"]["Motion"]:
                mouse_motion_x, mouse_motion_y = event_dict["Mouse"]["Motion"]
                if self.scroll_bar_side_inside_hit:
                    _update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        is_click=False
                    )
                elif self.scroll_bar_down_inside_hit:
                    _update_horizontal(
                        self.scroll_bar_down_inside_rect,
                        self.scroll_bar_down_rect,
                        mouse_motion_x,
                        self.curtain_rect,
                        self.view_rect.width,
                        is_click=False
                    )

            # si click up elimino de lista selected a scale modifier
            if event_dict["Mouse"]["ClickLeftUp"]:
                del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def scale_modifier(self,event_dict,code = None):

        # selected
        if code == "selected":

            if event_dict["Mouse"]["Motion"]:

                Mouse_motion_x, Mouse_motion_y = event_dict["Mouse"]["Motion"]
                limit_min = 150
                limit_max_w = self.curtain_w
                limit_max_h = self.curtain_h

                def _limit_motion(motion, current, limit_min, limit_max):
                    if current + motion < limit_min:
                        return limit_min - current
                    if current + motion > limit_max:
                        return limit_max - current
                    return motion
                
                if self.scale_modifier_hit_top:  # TOP
                    Mouse_motion_y = _limit_motion(-Mouse_motion_y, self.view_rect.height, limit_min, limit_max_h)
                    self.rects_updates(self.presurface, y=-Mouse_motion_y, h=Mouse_motion_y)
                elif self.scale_modifier_hit_down:  # DOWN
                    Mouse_motion_y = _limit_motion(Mouse_motion_y, self.view_rect.height, limit_min, limit_max_h)
                    self.rects_updates(self.presurface, h=Mouse_motion_y)
                if self.scale_modifier_hit_left:  # LEFT
                    Mouse_motion_x = _limit_motion(-Mouse_motion_x, self.view_rect.width, limit_min, limit_max_w)
                    self.rects_updates(self.presurface, x=-Mouse_motion_x, w=Mouse_motion_x)
                elif self.scale_modifier_hit_right:  # RIGHT
                    Mouse_motion_x = _limit_motion(Mouse_motion_x, self.view_rect.width, limit_min, limit_max_w)
                    self.rects_updates(self.presurface, w=Mouse_motion_x)

            # Reset hit flags on mouse button release
            if event_dict["Mouse"]["ClickLeftUp"]:
                del event_dict["EditableObjects"]["selected"][self.depth_number:]    

    def edit(self,event_dict, code = None):
        """metodo  principal por donde pasa la logica de las interacciones con los objetos dentro de "view" """
        # clickeable
        if code == "clickable":
            
            # Scroll dentro de la ventana 
            if event_dict["Mouse"]["Scroll"]: 

                if event_dict["Mouse"]["Scroll"] == 1:
                    mouse_scroll_motion_y = 20
                elif event_dict["Mouse"]["Scroll"] == -1:
                    mouse_scroll_motion_y = -20

                def update_vertical(bar, bar_limit, motion, curtain, view_height):
                    bar.y += motion
                    proportion = view_height / bar.height
                    curtain.y = -(bar.y - bar_limit.y) * proportion 

                    # revisar estas linas de codigo !!

                    if bar.y < bar_limit.y or curtain.y > 0:
                        bar.y = bar_limit.y
                        curtain.y = 0
                    elif bar.y + bar.height > bar_limit.y + bar_limit.height or curtain.y + curtain.height < view_height:
                        bar.y = bar_limit.y + bar_limit.height - bar.height
                        curtain.y = view_height - curtain.height

                    # hay que actualizar self.view_decrement_y??


                    self.save_curtain_rect_y = curtain.y # save
                    #curtain.y += self.view_decrement_y # aqui self.view_decrement_y es "0" siempre, donde se actualiza esto?

                if self.curtain_rect.height > self.view_rect.height:
                    update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_scroll_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        )
                    
                # AGREGAR AQUI LA EDICION DE POSICION X,Y DE DE LOS OBJETOS DE LA LISTA OBJECT_LIST SI ES QUE HAY OBJETOS??
                #for obj in self.objects_list:
                #    obj.rect.y += mouse_scroll_motion_y
                #    obj.rects_updates(self.view_surface,force= True)
                    
            
                
        
        # selected
        # if code == "selected":
        #     if event_dict["Mouse"]["ClickLeftUp"]:
        #         del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def draw(self,event_dict):
        """dibujo windows"""

        pg.draw.rect(self.presurface,self.rect_color,self.rect,0,10) # rect

        pg.draw.rect(self.presurface, self.view_color,self.view_rect,0,10) # view

        rect = (self.curtain_rect.x + 10,self.curtain_rect.y + 10 ,self.curtain_rect.width - 20,self.curtain_rect.height- 20)
        pg.draw.rect(self.view_surface, self.curtain_color,rect) # curtain


        # Dibuja la imagen en la pantalla
        #x = self.curtain_rect.x 
        #y = self.curtain_rect.y 
        #self.view_surface.blit(self.image,(x,y))

        x = self.view_rect.x - 4
        y = self.view_rect.y - 4
        w = self.view_rect.w + 8
        h = self.view_rect.h + 8
        pg.draw.rect(self.presurface,event_dict["Colors"]["LightGrey"],(x,y,w,h),4,10,-1,-1,-1,-1) # view

        if self.scroll_bar != 0: # si es 0: scroll_bar no existe 
            # scroll_bar_side_inside
            if self.curtain_rect.height > self.view_rect.height:
                pg.draw.rect(self.presurface,self.scroll_bar_insid_color,self.scroll_bar_side_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_side_inside_rect
                pg.draw.rect(self.presurface,self.scroll_bar_color,self.scroll_bar_side_rect,1,10,-1,-1,-1,-1) # scroll_bar_side_rect
            # scroll_bar_down_inside
            if self.curtain_rect.width > self.view_rect.width:
                pg.draw.rect(self.presurface,self.scroll_bar_insid_color,self.scroll_bar_down_inside_rect,0,10,-1,-1,-1,-1) # scroll_bar_down_inside_rect
                pg.draw.rect(self.presurface,self.scroll_bar_color,self.scroll_bar_down_rect,1,10,-1,-1,-1,-1) # scroll_bar_down_rect




#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------EngineWindow-------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------


class EngineWindow():
    """Crea el objeto ventana del proyecto sin ningun objeto en su interior"""
    def __init__(self, event_dict, presurface):

        # Profundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"] += 1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        # Rectángulo de fondo
        # ----------------------------------------------------------------------------
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        self.color = (120, 120, 120)
        self.update_draw_background = True
        self.rect_width = presurface.get_width()
        self.rect_height = presurface.get_height()
        # ----------------------------------------------------------------------------

        # Modificadores de escala
        # ----------------------------------------------------------------------------
        self.scale_modifier_bar = 30
        self.scale_modifier_margin = 5
        self.scale_modifier_hit_top = False
        self.scale_modifier_hit_down = False
        self.scale_modifier_hit_right = False
        self.scale_modifier_hit_left = False
        # ----------------------------------------------------------------------------

        # Icono y texto
        # ----------------------------------------------------------------------------
        self.icon = pg.transform.scale(pg.image.load(r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0.01\assets\images\dino-32.png"), (20, 20))
        self.text = Font.surf_font_OpenSans_Medium("Roar !! - V0.01")
        # ----------------------------------------------------------------------------

        # Botones (Cerrar, Maximizar, Minimizar)
        # ----------------------------------------------------------------------------
        self.close_button_color = (80, 80, 80)
        self.update_draw_close_button = True
        self.maximize_button_color = (80, 80, 80)
        self.minimize_button_color = (80, 80, 80)
        self.is_maximize = False
        self.save_x_y_minimized_window_screen = (0, 0)
        self.save_window_width = 0
        self.save_window_height = 0
        self.monitor_selected = 0
        # ----------------------------------------------------------------------------

        # Variables de la ventana (Engine Window)
        # ----------------------------------------------------------------------------
        self.window_id = pg.display.get_wm_info()["window"]
        self.window_left = 0
        self.window_top = 0
        self.window_width = 0
        self.window_height = 0
        self.save_global_mouse_x = 0
        self.save_global_mouse_y = 0
        # ----------------------------------------------------------------------------

        # Lista de objetos en GameEditor
        # ----------------------------------------------------------------------------
        self.objects_list = []  # Lista de objetos que deben contener un "rect"
        # ----------------------------------------------------------------------------

        # Inicializar rectángulos
        # ----------------------------------------------------------------------------
        self.rects_updates(presurface, self.rect_width, self.rect_height)
        # ----------------------------------------------------------------------------

        # Profundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"] -= 1
        # ----------------------------------------------------------------------------

    def rects_updates(self, presurface, w=0, h=0, resize=False, force=False):
        """
        Actualiza las propiedades del rectángulo del objeto.

        Parámetros:
            presurface: Superficie previa (no utilizada directamente en este código).
            x (int): Nueva posición en el eje X (opcional). ES 0, NO DEBE CAMBIARSE!
            y (int): Nueva posición en el eje Y (opcional). ES 0, NO DEBE CAMBIARSE!
            w (int): Nuevo ancho (opcional).
            h (int): Nueva altura (opcional).
            resize (bool): Indica si se debe redimensionar el rectángulo con los valores proporcionados.
            force (bool): Si es True, fuerza la actualización aunque no se cambien x, y, w, h.
        """
        
        # Si no hay valores para x, y, w, h y no se fuerza la actualización, salir
        if not any([w, h]) and not force:
            return
        
        # presurface 
        # ----------------------------------------------------------------------------
        self.presurface = presurface
        # ----------------------------------------------------------------------------
        
        # Si hay valores de x, y, w, h y resize es True, actualizar las dimensiones del rectángulo
        if resize:
            if w != 0:
                self.rect.w = w
            if h != 0:
                self.rect.h = h
        else:
            # Rect
            # ----------------------------------------------------------------------------
            self.rect.x = 0
            self.rect.y = 0
            self.rect.width += w
            self.rect.height += h
            # ----------------------------------------------------------------------------

        # scale_modifier_rect 
        # ----------------------------------------------------------------------------
        self.scale_modifier_rect = pg.rect.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # ----------------------------------------------------------------------------

        # buttons
        # ----------------------------------------------------------------------------
        # close_button
        button_dimension = 20
        x = self.rect.width - button_dimension - 5
        y = 5
        w = button_dimension
        h = button_dimension
        self.close_button_rect = pg.rect.Rect(x,y,w,h)

        # maximize_button
        x = self.rect.width - button_dimension - 5 - button_dimension - 5 
        y = 5
        w = button_dimension
        h = button_dimension
        self.maximize_button_rect = pg.rect.Rect(x,y,w,h)

        # minimize_button
        x = self.rect.width - button_dimension - 5 - button_dimension - 5 - button_dimension - 5 
        y = 5
        w = button_dimension
        h = button_dimension
        self.minimize_button_rect = pg.rect.Rect(x,y,w,h)
        # ----------------------------------------------------------------------------

        # view_rect 
        # ----------------------------------------------------------------------------
        bar = self.scale_modifier_bar
        margin = self.scale_modifier_margin

        x = self.rect.x + margin
        y = self.rect.y + bar #margin
        w = self.rect.width - (margin*2) 
        h = self.rect.height - (bar) - (margin)

        self.view_rect = pg.rect.Rect(x,y,w,h)
        self.view_surface_rect = self.view_rect.copy()
        
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)
        # ----------------------------------------------------------------------------

        # # recreo los rects de los objetos dentro de engine window
        # # ----------------------------------------------------------------------------
        # if self.objects_list:
        #     for obj in self.objects_list:
        #         obj.rects_updates(self.view_surface, force = True)
        # # ----------------------------------------------------------------------------
    # LOAD_OBJECT_NO ESTA ACTIVO
    def load_objects(self,*objects_list):
        """carga los objetos que estaran dentro de la ventana"""
        #self.objects_list = objects_list # cargar objetos
        pass
        #self.objects_list.extend(objects_list)

    def collision_detector(self,event_dict):

        # ----------------------------------------------------------------------------
        mouse_x, mouse_y = event_dict["Mouse"]["Position"] # Obtención de la posición del ratón
        # ----------------------------------------------------------------------------

        def init():

            if self.view_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_view_edit()
            elif self.close_button_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_close_button()
            elif self.maximize_button_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_maximize_button()
            elif self.minimize_button_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_minimize_button()
            elif self.scale_modifier_rect.collidepoint(mouse_x, mouse_y):
                _comprobation_section_scale_modifier()

        def _comprobation_section_view_edit():

            event_dict["EditableObjects"]["clickable"].append(self.edit)

            # mouse x,y con respecto a view_rect
            x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
            y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
            save_x_y = event_dict["Mouse"]["Position"]
            event_dict["Mouse"]["Position"] = (x,y)

            # Detectar colisión con objetos
            for obj in self.objects_list:
                if obj.rect.collidepoint(x, y):
                    obj.collision_detector(event_dict)
                    if event_dict["EditableObjects"]["clickable"]: break

            event_dict["Mouse"]["Position"] = save_x_y
 
        def _comprobation_section_scale_modifier():

            event_dict["EditableObjects"]["clickable"].append(self.scale_modifier)

            margin = self.scale_modifier_margin
            bar = self.scale_modifier_bar
            x, y, w, h = self.scale_modifier_rect
            hit_top = mouse_y <= y + bar
            hit_down = mouse_y >= y + h - margin
            hit_left = mouse_x <= x + margin
            hit_right = mouse_x >= x + w - margin
            self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False



            # ENTREGA POSICION ACTUAL DEL MOUSE
            # ----------------------------------------------------------------------------
            class POINT(ctypes.Structure):
                _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]
            def get_global_mouse_position():
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                return point.x, point.y
            self.save_global_mouse_x,self.save_global_mouse_y = get_global_mouse_position()
            # ----------------------------------------------------------------------------

            #print(self.is_maximize)

            if self.is_maximize == False: # si no esta maximizado

                if hit_down and hit_left:
                    self.scale_modifier_hit_down = self.scale_modifier_hit_left = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENESW
                elif hit_down and hit_right:
                    self.scale_modifier_hit_down = self.scale_modifier_hit_right = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENWSE
                elif hit_top:
                    self.scale_modifier_hit_top = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW
                elif hit_down:
                    self.scale_modifier_hit_down = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZENS
                elif hit_left:
                    self.scale_modifier_hit_left = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
                elif hit_right:
                    self.scale_modifier_hit_right = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_SIZEWE
                    
            else:

                if hit_top: # si esta maximizado
                    self.scale_modifier_hit_top = True
                    event_dict["Mouse"]["Icon"] = pg.SYSTEM_CURSOR_ARROW

        def _comprobation_section_close_button():
            event_dict["EditableObjects"]["clickable"].append(self.close)

        def _comprobation_section_maximize_button():
            event_dict["EditableObjects"]["clickable"].append(self.maximize)

        def _comprobation_section_minimize_button():
            event_dict["EditableObjects"]["clickable"].append(self.minimize)
            
        init()
    
    def scale_modifier(self,event_dict,code = None):

        if code == "clickable":
            pass
        
        if code == "selected":

            class POINT(ctypes.Structure):
                _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

            def get_global_mouse_position():
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                return point.x, point.y

            # Detectar el clic izquierdo y activar el movimiento
            if event_dict["Mouse"]["ClickLeftDown"]:
                #self.initial_mouse_x, self.initial_mouse_y = get_global_mouse_position()
                rect = wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(self.window_id, ctypes.byref(rect))

                self.window_left = rect.left
                self.window_top = rect.top
                self.window_width = rect.right - rect.left
                self.window_height = rect.bottom - rect.top

            displacement_x, displacement_y = 0, 0
            if (self.save_global_mouse_x, self.save_global_mouse_y) != get_global_mouse_position():
                x, y = get_global_mouse_position()
                displacement_x = x - self.save_global_mouse_x
                displacement_y = y - self.save_global_mouse_y
                self.save_global_mouse_x, self.save_global_mouse_y = get_global_mouse_position()
            
            # Mover la ventana hacia arriba
            if self.scale_modifier_hit_top:

                if displacement_x != 0 or displacement_y != 0:

                    self.window_left += displacement_x
                    self.window_top += displacement_y
                    x = self.window_left
                    y = self.window_top
                    #w = self.window_width
                    #h = self.window_height
                    w = event_dict["Screen"]["Width"]
                    h = event_dict["Screen"]["Height"]

                    # elegimos el monitor seleccionado
                    for m in event_dict["SysInfo"]["Monitors"]:
                        x_monit = m["Position"]["X"]
                        y_monit = m["Position"]["Y"]
                        w_monit = m["Dimensions"]["Width"]
                        h_monit = m["Dimensions"]["Height"]
                        if x_monit < x < x_monit + w_monit and y_monit < y < y_monit + h_monit:
                            self.monitor_selected = m["Number"] # moniotor seleccionado 


                    # si esta maximizada y la muevo se redimenciona y salgo de maximizado
                    if self.is_maximize:
                        """ Si la ventana esta maximizada y la muevo, self.is_maximize = False y deja de estar maximizada se redimenciona a un valor menor """

                        self.is_maximize = False

                        m = self.monitor_selected
                        num = 40

                        x = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["X"] 
                        y = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Y"] 
                        w = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Width"] - num
                        h = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Height"] - num

                        pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                        self.window_id = pg.display.get_wm_info()["window"]
                        self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                        event_dict["Screen"]["Width"] = w
                        event_dict["Screen"]["Height"] = h
                        ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001)  # reposiciona la ventana en x,y

                        window_handle = pg.display.get_wm_info()['window']
                        # Función para obtener la posición de la ventana en Windows
                        def get_window_position(hwnd):
                            rect = ctypes.wintypes.RECT()
                            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                            return rect.left, rect.top
                        self.save_x_y_minimized_window_screen = get_window_position(window_handle)

                        # update_draw
                        self.update_draw_background = True

                    else:
                        ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001)  # reposiciona la ventana en x,y
                    
                    
                    
                    if event_dict["Mouse"]["ClickLeftUp"]:
                        pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                        self.window_id = pg.display.get_wm_info()["window"]
                        self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                        event_dict["Screen"]["Width"] = w
                        event_dict["Screen"]["Height"] = h

            elif self.scale_modifier_hit_down:

                self.window_height += displacement_y
                x = self.window_left
                y = self.window_top
                w = self.window_width
                h = max(100, self.window_height)
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, w, h, 0)


                if event_dict["Mouse"]["ClickLeftUp"]:
                    pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                    self.window_id = pg.display.get_wm_info()["window"]
                    self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                    event_dict["Screen"]["Width"] = w
                    event_dict["Screen"]["Height"] = h

                    # update_draw
                    self.update_draw_background = True

            if self.scale_modifier_hit_right:

                self.window_width += displacement_x
                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, w, h, 0)


                if event_dict["Mouse"]["ClickLeftUp"]:
                    pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                    self.window_id = pg.display.get_wm_info()["window"]
                    self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                    event_dict["Screen"]["Width"] = w
                    event_dict["Screen"]["Height"] = h

                    # update_draw
                    self.update_draw_background = True

            elif self.scale_modifier_hit_left:

                self.window_width -= displacement_x
                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, w, h, 0)

                
                if event_dict["Mouse"]["ClickLeftUp"]:
                    pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                    self.window_id = pg.display.get_wm_info()["window"]
                    self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                    event_dict["Screen"]["Width"] = w
                    event_dict["Screen"]["Height"] = h

                    # update_draw
                    self.update_draw_background = True

            if event_dict["Mouse"]["ClickLeftUp"]:
                del event_dict["EditableObjects"]["selected"][self.depth_number:] 

                
            """if self.scale_modifier_hit_top:

                self.window_left += displacement_x
                self.window_top += displacement_y

                x = self.window_left
                y = self.window_top
                w = self.window_width
                h = self.window_height

                #ctypes.windll.user32.MoveWindow(self.window_id,x,y,w,h, True)
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001)  # 0x0001 es la bandera SWP_NOSIZE para no cambiar el tamaño

            elif self.scale_modifier_hit_down:
                
                # Cambiar las dimensiones de la ventana
                self.window_height += displacement_y

                x = self.window_left
                y = self.window_top
                w = self.window_width
                h = max(100, self.window_height)

                # Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Ancho de las líneas del contorno
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar solo las líneas del buffer a la pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)  # Línea superior
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)  # Línea inferior
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)  # Línea izquierda
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)  # Línea derecha

                    # Invalidar las áreas donde se dibujaron las líneas para forzar la actualización
                    if displacement_y != 0:
                        #rect = wintypes.RECT(x, y, x + w, y + h)
                        #ctypes.windll.user32.InvalidateRect(0, ctypes.byref(rect), True)
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    # Liberar la ventana para que vuelva a actualizarse
                    ctypes.windll.user32.LockWindowUpdate(0)
                    # Liberar el DC de la pantalla después de dibujar
                    #ctypes.windll.user32.ReleaseDC(self.window_id, self.hdc)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    # Liberar el contexto de memoria
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                event_dict["Screen"]["Height"] = h

            
            # Modificar el ancho de la ventana hacia la derecha y dibujar líneas
            if self.scale_modifier_hit_right:
                
                # Definir las constantes
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Actualizar el ancho de la ventana
                self.window_width += displacement_x

                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height

                # Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar las líneas al contexto de pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)

                    # Invalidar las áreas para forzar la actualización
                    if displacement_x!=0 and displacement_y==0:
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    ctypes.windll.user32.LockWindowUpdate(0)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                # Actualizar el diccionario de eventos
                event_dict["Screen"]["Width"] = w

            # Modificar el ancho de la ventana hacia la izquierda y dibujar líneas
            elif self.scale_modifier_hit_left:

                # Definir las constantes
                LINE_WIDTH = 3
                COLOR = 0x00FF0000  # Rojo para mayor visibilidad

                # Calculate the new width and ensure it doesn't go below 100
                new_width = self.window_width - displacement_x
                if new_width < 100:
                    # Adjust the displacement to ensure the width is not less than 100
                    displacement_x = self.window_width - 100

                # Actualizar la posición y el ancho de la ventana
                self.window_left += displacement_x
                self.window_width -= displacement_x

                x = self.window_left
                y = self.window_top
                w = max(100, self.window_width)
                h = self.window_height
                

                #Obtener el contexto de dispositivo (DC) de la pantalla
                self.hdc = ctypes.windll.user32.GetDC(0)  # 0 representa toda la pantalla

                # Crear un contexto de memoria (buffer)
                mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                mem_bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, w, h)
                ctypes.windll.gdi32.SelectObject(mem_dc, mem_bitmap)

                # Usar "LockWindowUpdate" para bloquear la ventana antes de dibujar
                #ctypes.windll.user32.LockWindowUpdate(0)
                ctypes.windll.user32.LockWindowUpdate(self.window_id)

                try:
                    # Dibujar las líneas del contorno en el contexto de memoria
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, w, LINE_WIDTH, COLOR)  # Línea superior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, h - LINE_WIDTH, w, LINE_WIDTH, COLOR)  # Línea inferior
                    ctypes.windll.gdi32.PatBlt(mem_dc, 0, 0, LINE_WIDTH, h, COLOR)  # Línea izquierda
                    ctypes.windll.gdi32.PatBlt(mem_dc, w - LINE_WIDTH, 0, LINE_WIDTH, h, COLOR)  # Línea derecha

                    # Copiar las líneas al contexto de pantalla
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, w, LINE_WIDTH, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y + h - LINE_WIDTH, w, LINE_WIDTH, mem_dc, 0, h - LINE_WIDTH, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x, y, LINE_WIDTH, h, mem_dc, 0, 0, 0x00CC0020)
                    ctypes.windll.gdi32.BitBlt(self.hdc, x + w - LINE_WIDTH, y, LINE_WIDTH, h, mem_dc, w - LINE_WIDTH, 0, 0x00CC0020)

                    # Invalidar las áreas para forzar la actualización
                    if displacement_x!=0 and displacement_y==0:
                        #ctypes.windll.user32.InvalidateRect(0, self.window_id, True)
                        ctypes.windll.user32.InvalidateRect(0, None, True)

                finally:
                    ctypes.windll.user32.LockWindowUpdate(0)
                    ctypes.windll.user32.ReleaseDC(0, self.hdc)
                    ctypes.windll.gdi32.DeleteObject(mem_bitmap)
                    ctypes.windll.gdi32.DeleteDC(mem_dc)

                # Actualizar el diccionario de eventos
                event_dict["Screen"]["Width"] = w

                
            if event_dict["Mouse"]["ClickLeftUp"]:
                
                #self.scale_modifier_hit_top = self.scale_modifier_hit_down = self.scale_modifier_hit_left = self.scale_modifier_hit_right = False
                ctypes.windll.user32.MoveWindow(self.window_id, x, y, w, h, True)
                w  = event_dict["Screen"]["Width"]
                h = event_dict["Screen"]["Height"]
                pg.display.set_mode((w,h), pg.DOUBLEBUF | pg.NOFRAME)
                self.window_id = pg.display.get_wm_info()["window"]
                self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                del event_dict["EditableObjects"]["selected"][self.depth_number:]     
            """

    def edit(self,event_dict,code = None):

        # mouse x,y con respecto a view_rect
        x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
        y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
        save_x_y = event_dict["Mouse"]["Position"]
        event_dict["Mouse"]["Position"] = (x,y)

        # ejecuto objetos de lista selected
        #ESTO ESTA MAL!! -- por?
        # ----------------------------------------------------------------------------
        if code == "clickable":
            exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= self.depth_number+1 
            if exists_next_clickable_list:
                event_dict["EditableObjects"]["clickable"][self.depth_number+1](event_dict, code ) 

        if code == "selected":
            exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number+1 
            if exists_next_selected_list:
                event_dict["EditableObjects"]["selected"][self.depth_number+1](event_dict, code )
        # ----------------------------------------------------------------------------


        event_dict["Mouse"]["Position"] = save_x_y



        #  # Delate objects from object_list
        # if event_dict["Delate_List"]:
        #     for obj in event_dict["Delate_List"]:
        #         if obj in self.objects_list:
        #             self.objects_list.remove(obj)
        #     event_dict["Delate_List"].clear()

    def draw(self,event_dict):

        if self.update_draw_background: # ESTO ESTA MAL! CLAU BACKGRAUND SI ES LA VENTANA DEL PROYECTO

            # rectangulo gris osucoro de la ventana principal 
            # ----------------------------------------------------------------------------
            pg.draw.rect(self.presurface,(50,50,50),self.rect)
            # ----------------------------------------------------------------------------

            # Icono y texto 
            # ----------------------------------------------------------------------------
            self.presurface.blit(self.icon,(5,5)) # icono
            self.presurface.blit(self.text, (30,6)) # texto - nombre del motor
            # ----------------------------------------------------------------------------

            # cruz de cierre

            self.update_draw_close_button = True
            # ----------------------------------------------------------------------------
            # pg.draw.rect(self.presurface,self.close_button_color,self.close_button_rect,0,6) # close
            # color = (120,120,120)
            # num = 6
            # x1 = self.close_button_rect.x + num
            # y1 = self.close_button_rect.y + num
            # x2 = self.close_button_rect.x + self.close_button_rect.width - num
            # y2 = self.close_button_rect.y + self.close_button_rect.height - num
            # pg.draw.line(self.presurface,color,(x1,y1),(x2,y2),3)
            # x1 = self.close_button_rect.x + num
            # y1 = self.close_button_rect.y + self.close_button_rect.height - num
            # x2 = self.close_button_rect.x + self.close_button_rect.width - num
            # y2 = self.close_button_rect.y + num
            # pg.draw.line(self.presurface,color,(x1,y1),(x2,y2),3)
            # ----------------------------------------------------------------------------

            # maximizar 
            # ----------------------------------------------------------------------------
            pg.draw.rect(self.presurface,self.maximize_button_color,self.maximize_button_rect,0,6) # maximize
            color = (120,120,120)
            num = 5
            x = self.maximize_button_rect.x + num
            y = self.maximize_button_rect.y + num 
            w = self.maximize_button_rect.width - num*2
            h = self.maximize_button_rect.height - num*2 
            pg.draw.rect(self.presurface,color,(x,y,w,h),2)
            # ----------------------------------------------------------------------------

            # minimizar
            # ----------------------------------------------------------------------------
            pg.draw.rect(self.presurface,self.minimize_button_color,self.minimize_button_rect,0,6) # minimize
            color = (120,120,120)
            num = 4
            x1 = self.minimize_button_rect.x + num
            y1 = self.minimize_button_rect.y + self.minimize_button_rect.width/2
            x2 = self.minimize_button_rect.x + self.minimize_button_rect.width - num
            y2 = y1#self.minimize_button_rect.y + self.minimize_button_rect.height - self.minimize_button_rect.width/2 - num*2 
            pg.draw.line(self.presurface,color,(x1,y1),(x2,y2),2)
            # ----------------------------------------------------------------------------

            self.update_draw_background = False



        if self.update_draw_close_button :
            
            # cruz de cierre
            # ----------------------------------------------------------------------------
            pg.draw.rect(self.presurface,self.close_button_color,self.close_button_rect,0,6) # close
            color = (120,120,120)
            num = 6
            x1 = self.close_button_rect.x + num
            y1 = self.close_button_rect.y + num
            x2 = self.close_button_rect.x + self.close_button_rect.width - num
            y2 = self.close_button_rect.y + self.close_button_rect.height - num
            pg.draw.line(self.presurface,color,(x1,y1),(x2,y2),3)
            x1 = self.close_button_rect.x + num
            y1 = self.close_button_rect.y + self.close_button_rect.height - num
            x2 = self.close_button_rect.x + self.close_button_rect.width - num
            y2 = self.close_button_rect.y + num
            pg.draw.line(self.presurface,color,(x1,y1),(x2,y2),3)
            # ----------------------------------------------------------------------------
            self.update_draw_close_button = False
        

        # Interior de la ventana 
        # ----------------------------------------------------------------------------
        #pg.draw.rect(self.presurface,self.color,self.view_rect) # dibujo el fondo gris
        # ----------------------------------------------------------------------------  
           
        event_dict["UpdateDrawRect"] = self.rect
        
    def pre_close(self,event_dict, code = None):

        if code == "clickable":

            self.close_button_color = (180,0,0)
            self.update_draw_close_button = True # actualizar boton de ciere

        if code == "selected":
            pass

    def pos_close(self,event_dict, code = None):

        if code == "clickable":

            self.close_button_color = (80, 80, 80)
            self.update_draw_close_button = True # actualizar boton de ciere

        if code == "selected":
            pass

    def close(self,event_dict,code = None):

        #if code == "clickable":
        #    pass

        if code == "selected":
            pg.quit()
            sys.exit()

    def maximize(self,event_dict,code = None):

        if code == "selected":

            if self.is_maximize==False:

                # Obtener el manejador de la ventana
                window_handle = pg.display.get_wm_info()['window']
                # Función para obtener la posición de la ventana en Windows
                def get_window_position(hwnd):
                    rect = ctypes.wintypes.RECT()
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    return rect.left, rect.top
                self.save_x_y_minimized_window_screen = get_window_position(window_handle)

                m = self.monitor_selected

                x = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["X"]
                y = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Y"]
                w = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Width"]
                h = event_dict["SysInfo"]["Monitors"][m]["WorkArea"]["Height"]

                # Establecer la posición y dimensiones de la ventana en Pygame
                pg.display.set_mode((w, h), pg.NOFRAME)
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001) # reposicion de la ventana  
                self.window_id = pg.display.get_wm_info()["window"]
                self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                self.is_maximize = True # la ventana esta maximizada

                # guardamos las dimenciones de la ventana antes de maximizar
                self.save_window_width = event_dict["Screen"]["Width"]
                self.save_window_Height = event_dict["Screen"]["Height"]
                
            else:
                w = self.save_window_width 
                h = self.save_window_Height

                pg.display.set_mode((w, h), pg.NOFRAME)
                self.window_id = pg.display.get_wm_info()["window"]
                self.rects_updates(pg.display.get_surface(), w=w,h=h, resize=True)
                x,y = self.save_x_y_minimized_window_screen
                ctypes.windll.user32.SetWindowPos(self.window_id, None, x, y, 0, 0, 0x0001) # reposicion de la ventana  
                self.is_maximize = False # la ventana esta maximizada
            
            # actualizar la informacion del tamaño de la ventana
            event_dict["Screen"]["Width"] = w
            event_dict["Screen"]["Height"] = h

            # update_draw
            self.update_draw_background = True

            del event_dict["EditableObjects"]["selected"][self.depth_number:] 

    def minimize(self,event_dict,code = None):
        if code == "selected":
            #if event_dict["Mouse"]["ClickLeftDown"]:
            pg.display.iconify()
            del event_dict["EditableObjects"]["selected"][self.depth_number:]  