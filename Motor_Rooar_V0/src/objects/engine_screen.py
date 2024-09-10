import pygame as pg

from scripts.surface_reposition import SurfaceReposition

class EngineScreen():

    def __init__(self,presurface):

        #self.presurface = presurface

        self.rect = pg.rect.Rect(0,0,0,0)

        w = presurface.get_width()
        h = presurface.get_height()
        x = 20
        y = 20
        w = w - 40
        h = h - 40

        self.rects_updates(presurface,x,y,w,h)
        # self.rect = pg.rect.Rect(x,y,w,h)
        # self.surface_rect = self.rect.copy()
        # self.surface = SurfaceReposition.surface_reposition(self.presurface,self.rect,self.surface_rect)
        self.color = (120,120,120)


    def rects_updates(self, presurface, x=0, y=0, w=0, h=0 , force = False):

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
        
        self.rect = pg.rect.Rect(x,y,w,h)
        self.surface_rect = self.rect.copy()
        self.surface = SurfaceReposition.surface_reposition(self.presurface,self.rect,self.surface_rect)


       

    def draw(self,event_dict):

        pg.draw.rect(self.presurface,self.color,self.rect)
