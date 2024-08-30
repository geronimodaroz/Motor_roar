import pygame as pg

# CONVIERTE STRING EN SURFACE CON ESTA FUENTE "self.font = pg.font.Font(None, 16)"
class Font:
    """Contiene las fuentes para el proyecto"""
    def __init__(self):

        self.font = pg.font.Font(None, 16)

        #self.route_Roboto-Black = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assetsFonts\Roboto-Black.ttf"
        #self.route_Roboto-Regular = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assetsFonts\Roboto-Regular.ttf" 
        self.route_OpenSans-Medium = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assets\Fonts\OpenSans-Medium.ttf" 


    def surf_font(self,text,color = (180,180,180)):
        surf_text = self.font.render(text, True, color)
        return surf_text