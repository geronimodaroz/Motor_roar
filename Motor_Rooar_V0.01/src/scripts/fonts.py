import pygame as pg


class Font:
    """Contiene las fuentes para el proyecto"""
    # def __init__(self):

    #     # default
    #     self.font_default = pg.font.Font(None, 16)

    #     #self.route_Roboto_Black = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assetsFonts\Roboto-Black.ttf"
    #     #self.route_Roboto_Regular = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assetsFonts\Roboto-Regular.ttf" 

    #     # OpenSans_Medium
    #     self.route_OpenSans_Medium = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0\assets\Fonts\OpenSans-Medium.ttf"
    #     self.font_OpenSans_Medium = pg.font.Font(self.route_OpenSans_Medium, 12)

    # Inicialización de las fuentes como variables de clase
    font_default = pg.font.Font(None, 16)

    route_OpenSans_Medium = r"C:\Users\Usuario\Desktop\Motor_Rooar\Motor_Rooar_V0.01\assets\Fonts\OpenSans-Medium.ttf"
    font_OpenSans_Medium = pg.font.Font(route_OpenSans_Medium, 12)


    @staticmethod
    def surf_font_default(text, color =(180, 180, 180)):
        """ Devuelve la superficie del texto en la fuente default"""
        return Font.font_default.render(text, True, color)

    @staticmethod
    def surf_font_OpenSans_Medium(text, color =(180, 180, 180)):
        """ Devuelve la superficie del texto en la fuente OpenSans_Medium"""
        return Font.font_OpenSans_Medium.render(text, True, color)