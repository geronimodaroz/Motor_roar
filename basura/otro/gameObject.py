

import sys
import os #acceso a funciones que te permiten interactuar con el sistema operativo

from tkinter import filedialog # seleccionar archivos por el
import tkinter as tk

#from pygame import *
import pygame
import pygame as pg


# Inicializa Pygame
pygame.init()
pygame.display.set_caption("videogame") # Establecer el título de la ventana

# Configurar la pantalla
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))




# Configurar Tkinter
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal de Tkinter






def image_load():
    # Solicitar al usuario que seleccione un archivo de imagen
    file_paths = filedialog.askopenfilenames(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    images = []
    for i in file_paths:
        images.append(pg.image.load(i))


# esta clase agrega sprites
class gameObject():

    def __init__(self,name = "undefined", position=(0, 0),image_path = "undefined.png"):

        self.name = name
        self.position = position
        self.image = pg.image.load(image_path)


    def image_load(self):
        # Solicitar al usuario que seleccione un archivo de imagen
        file_paths = filedialog.askopenfilenames(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])

        self.images = []
        for i in file_paths:
            self.images.append(pg.image.load(i))
        
        #rect
        img = self.images[0]
        self.rect = img.get_rect(topleft= self.position)

object_1 = gameObject("player",(100,100))
object_1.image_load()

"""# esta clase agrega sprites
class gameObject():
    def __init__(self, position=(0, 0),image_path = "undefined.png"):
        #self.name = name
        #self.image_path = image_path
        self.name_spt = os.listdir(image_path)
        self.image_spr=[]
        #print(image_path)
        #self.image = pg.image.load(self.spt)#.convert_alpha() # convert_alpha identifica la trasparencia
        #self.rect = self.image.get_rect(topleft=position)
        for filename in self.name_spt:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path_spt = os.path.join(image_path, filename) # une la ruta y el nombre
                image = pg.image.load(image_path_spt)#.convert_alpha()
                self.image_spr.append(image)
        #rect
        image1 = self.image_spr[0]
        self.rect = image1.get_rect(topleft=position)"""






#spt_animation_run = gameObject((0,0),"animation_run/")


# Bucle principal del juego
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Aquí puedes agregar la lógica de tu juego y dibujar en la ventana
    



    # Limpia la ventana
    screen.fill((100, 100, 100))


    #screen.blit(spt_animation_run.image_spr[0],(200,200)) # dibujo la imagen

    screen.blit(object_1.images[0],object_1.position)

    # Actualizar la ventana
    pg.display.update()