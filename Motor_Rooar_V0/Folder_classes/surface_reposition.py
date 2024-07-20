#import sys
#import pygame as pg



class SurfaceReposition:


    def surface_reposition(surface_base,rect,surface_rect):
            
        # surface_base
        # rect
        # surface_rect
        # surface

        # x
        surface_rect.x = min(max(0,surface_rect.x),surface_base.get_width())

        if rect.x < 0:
            #surface_rect.x = 0
            if rect.x + rect.width > 0:
                if rect.x + rect.width < surface_base.get_width():
                    surface_rect.width = rect.x + rect.width
                else:
                    surface_rect.width = surface_base.get_width()
            else:
                surface_rect.width = 0
        else:
            if rect.x < surface_base.get_width():
                if rect.x + rect.width > surface_base.get_width():
                    surface_rect.width = surface_base.get_width() - rect.x
                else:
                    surface_rect.width = rect.width 
            else:
                surface_rect.width = 0

        # y
        surface_rect.y = min(max(0,surface_rect.y),surface_base.get_height())

        if rect.y < 0:
            if rect.y + rect.height > 0:
                if rect.y + rect.height < surface_base.get_height():
                    surface_rect.height = rect.y + rect.height
                else:
                    surface_rect.height = surface_base.get_height()
            else:
                surface_rect.height = 0
        else:
            if rect.y < surface_base.get_height():
                if rect.y + rect.height > surface_base.get_height():
                    surface_rect.height = surface_base.get_height() - rect.y
                else:
                    surface_rect.height= rect.height
            else:
                surface_rect.height = 0



        surface =  surface_base.subsurface(surface_rect) # rect surface

        return surface