
import pygame
import sys
import os #acceso a funciones que te permiten interactuar con el sistema operativo

#from pygame import *
import pygame as pg

# Inicializa Pygame
pygame.init()

pygame.display.set_caption("videogame") # Establecer el título de la ventana

# Configurar la pantalla
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))





# esta clase agrega sprites
class gameObject(pg.sprite.Sprite):

    def __init__(self, name="undefined", position=(0, 0),image_path = "undefined.png"):

        super().__init__()

        self.name = name
        #self.position = position
        self.image = pg.image.load(image_path)#.convert_alpha() # convert_alpha identifica la trasparencia
        self.rect = self.image.get_rect(topleft=position)






sprite_group = pg.sprite.Group()
sprite_player = gameObject("player",(100,100),"esqueleto.png") # sprite player
sprite_group.add(sprite_player)




# agregar serie de imagenes
archivos = os.listdir("animation_run/")

for spr in archivos:
    sprite_group.add(gameObject("player",(200,200),f"animation_run/{spr}"))



# Bucle principal del juego
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Aquí puedes agregar la lógica de tu juego y dibujar en la ventana
    
    


    # Limpia la ventana
    screen.fill((100, 100, 100))

    sprite_group.draw(screen)

    # Actualizar la ventana
    pg.display.update()