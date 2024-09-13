import pygame as pg
#import sys
#import pygame.gfxdraw
from scripts.surface_reposition import SurfaceReposition

from typing import Literal


class Window:

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
        self.image = pg.image.load('C:/Users/Usuario/Desktop/med.png')


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
        # x = self.save_curtain_rect_x + self.view_decrement_x
        # y = self.save_curtain_rect_y + self.view_decrement_y
        # w = self.curtain_w
        # h = self.curtain_h

        # # if curtain is outside of view, si la cortina se sale de vista
        # if self.save_curtain_rect_x + w < self.view_rect.width and self.save_curtain_rect_x < 0:
        #     x = self.view_rect.width - w + self.view_decrement_x
        #     self.save_curtain_rect_x = self.view_rect.width - w
        # elif self.save_curtain_rect_x > 0:
        #     x = 0 + self.view_decrement_x
        #     self.save_curtain_rect_x = 0
            
        # if self.save_curtain_rect_y + h < self.view_rect.height and self.save_curtain_rect_y < 0:
        #     y = self.view_rect.height - h + self.view_decrement_y
        #     self.save_curtain_rect_y = self.view_rect.height - h
        # elif self.save_curtain_rect_y > 0:
        #     y = 0 + self.view_decrement_y
        #     self.save_curtain_rect_y = 0

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
        # selected
        if code == "selected":
            if event_dict["Mouse"]["ClickLeftUp"]:
                del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def draw(self,event_dict):


        pg.draw.rect(self.presurface,self.rect_color,self.rect,0,10) # rect

        pg.draw.rect(self.presurface,(0,0,0),self.quit_rect,0,10) # quit

        pg.draw.rect(self.presurface, self.view_color,self.view_rect,0,10) # view

        pg.draw.rect(self.view_surface, self.curtain_color,self.curtain_rect) # curtain



        # Dibuja la imagen en la pantalla
        x = self.curtain_rect.x 
        y = self.curtain_rect.y 
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
#----------------------------------------------------------------WindowBase-------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------


class WindowBase():

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
        self.view_surface_rect = self.view_rect.copy()
        self.view_surface = SurfaceReposition.surface_reposition(self.presurface, self.view_rect, self.view_surface_rect)

        self.view_decrement_x = self.view_rect.x if self.view_rect.x < 0 else 0
        self.view_decrement_y = self.view_rect.y if self.view_rect.y < 0 else 0
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

    def load_objects(self,*objects_list):
        """carga los objetos que estaran dentro de la ventana"""
        #self.objects_list = objects_list # cargar objetos
        self.objects_list.extend(objects_list)
        
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
            curtain.y += self.view_decrement_y

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

            if event_dict["Mouse"]["Scroll"]:

                if event_dict["Mouse"]["Scroll"] == 1:
                    mouse_scroll_motion_y = 20
                elif event_dict["Mouse"]["Scroll"] == -1:
                    mouse_scroll_motion_y = -20

                def update_vertical(bar, bar_limit, motion, curtain, view_height):
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

                if self.curtain_rect.height > self.view_rect.height:
                    update_vertical(
                        self.scroll_bar_side_inside_rect,
                        self.scroll_bar_side_rect,
                        mouse_scroll_motion_y,
                        self.curtain_rect, 
                        self.view_rect.height,
                        )
        
        # selected
        # if code == "selected":
        #     if event_dict["Mouse"]["ClickLeftUp"]:
        #         del event_dict["EditableObjects"]["selected"][self.depth_number:]

    def draw(self,event_dict):
        """dibujo windows"""

        pg.draw.rect(self.presurface,self.rect_color,self.rect,0,10) # rect

        pg.draw.rect(self.presurface, self.view_color,self.view_rect,0,10) # view

        #pg.draw.rect(self.view_surface, self.curtain_color,self.curtain_rect) # curtain


        # Dibuja la imagen en la pantalla
        # x = self.curtain_rect.x 
        # y = self.curtain_rect.y 
        # self.view_surface.blit(self.image,(x,y))

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
        