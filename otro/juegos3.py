
import pygame
import sys

#from pygame import *
import pygame as pg

# Inicializa Pygame
pygame.init()

pygame.display.set_caption("videogame") # Establecer el título de la ventana


# Configurar la pantalla
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))

    
class gameObject():

    def __init__(self, name="undefined", position=(0, 0)):
        self.name = name
        self.position = position


    def rectangle(self, x, y, width, height):
        # Crea un objeto Rect y lo guarda como atributo
        self.rect = pg.Rect(x, y, width, height)

    def load_image(self, image_path):
        self.image = pg.image.load(image_path)




# Bucle principal del juego
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Aquí puedes agregar la lógica de tu juego y dibujar en la ventana
    
    objet_1 = gameObject("object_1",(100,100))
    objet_1.rectangle(objet_1.position[0],objet_1.position[1],100,100)
    objet_1.load_image("otro/esqueleto.png")

    # Limpia la ventana
    screen.fill((0, 0, 0))


    pg.draw.rect(screen,pg.Color("green"),objet_1.rect)
    screen.blit(objet_1.image,(objet_1.position[0],objet_1.position[1]))


    # Actualizar la ventana
    pg.display.update()