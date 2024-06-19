import sys
import pygame as pg

# CONVIERTE STRING EN SURFACE CON ESTA FUENTE "self.font = pg.font.Font(None, 16)"

class Font:

    def __init__(self):

        self.font = pg.font.Font(None, 16)

        #self.color = (180,180,180)

    def surf_font(self,text,color = (180,180,180)):



        surf_text = self.font.render(text, True, color)

        return surf_text
        