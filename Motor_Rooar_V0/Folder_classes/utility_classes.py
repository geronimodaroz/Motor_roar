import sys
import pygame as pg

# CONVIERTE STRING EN SURFACE CON ESTA FUENTE "self.font = pg.font.Font(None, 16)"
class Font:
    """Contiene las fuentes para el proyecto"""
    def __init__(self):
        self.font = pg.font.Font(None, 16)
        #self.color = (180,180,180)

    def surf_font(self,text,color = (180,180,180)):
        surf_text = self.font.render(text, True, color)
        return surf_text
    

 # Deteccion de doble y triple click
class ClicksDetector:
    # se usa dentro de un "if event_dict["Mouse"]["ClickLeftDown"]:" para detectar el click del raton
    click_count = 0
    last_click_time = 0
    click_delay = 500

    @classmethod
    def detect_double_triple_click(cls):
        """Detecta el tipo de clic sin necesidad de instanciar la clase."""
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - cls.last_click_time
        
        cls.click_count = (
            3 if cls.click_count == 2 and elapsed_time <= cls.click_delay else
            2 if cls.click_count == 1 and elapsed_time <= 200 else
            1
        )
        cls.last_click_time = current_time
        return cls.click_count
    
    @classmethod
    def detect_double_click(cls):
        """Detecta el tipo de clic sin necesidad de instanciar la clase."""
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - cls.last_click_time
        
        cls.click_count = (
            2 if cls.click_count == 1 and elapsed_time <= 200 else
            1
        )
        cls.last_click_time = current_time
        return cls.click_count



# class DetectionDoubleTripleClick():

#     def __init__(self):
#         self.click_count = 0
#         self.last_click_time = 0
#         self.click_delay = 500

#     def detection_doble_triple_ckick(self):

#         current_time = pg.time.get_ticks()

#         # Si el tiempo desde el último clic es menor que el retardo permitido
#         if self.click_count == 2 and current_time - self.last_click_time <= self.click_delay:
#             self.click_count = 3

#         elif self.click_count == 1 and current_time - self.last_click_time <= self.click_delay:
#             self.click_count = 2
#         else:
#             # Reiniciar la cuenta de clics si se ha superado el intervalo
#             self.click_count = 1
            
#         self.last_click_time = current_time

#         return self.click_count
        