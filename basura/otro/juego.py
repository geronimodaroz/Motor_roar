


import pygame
import sys

#from pygame import *
import pygame as pg

# Inicializa Pygame
pygame.init()
pygame.display.set_caption("videogame") # Establecer el título de la ventana
# Definir las dimensiones de la ventana
ventana_ancho = 800
ventana_alto = 600
# Crear la ventana
ventana = pg.display.set_mode((ventana_ancho, ventana_alto))





# Cargar la imagen
imagen = pg.image.load("otro/esqueleto.png")
imagen = pg.transform.scale(imagen,(300,300))


# Obtén el rectángulo de la imagen
imagen_rect = imagen.get_rect()
# Coordenadas de la imagen en la ventana
imagen_rect.center = (ventana_ancho // 2, ventana_alto // 2)

#click_izq = False

# Estado del arrastre
arrastrando = False


# Bucle principal del juego
while True:

    # Limpia la ventana
    ventana.fill((0, 0, 0))


    for event in pg.event.get():
        #print(event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and imagen_rect.collidepoint(event.pos): 
                arrastrando = True
                offset_x, offset_y = event.pos[0] - imagen_rect.x, event.pos[1] - imagen_rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                arrastrando = False

        elif event.type == pygame.MOUSEMOTION:
            if arrastrando:
                imagen_rect.x = event.pos[0] - offset_x
                imagen_rect.y = event.pos[1] - offset_y



    # Aquí puedes agregar la lógica de tu juego y dibujar en la ventana
    


    #mouse_x, mouse_y = pg.mouse.get_pos()




    """# moviendo la imagen
    if imagen_rect.collidepoint(mouse_x,mouse_y):
        #capturando clic izquierdo mouse ([0] -> (true,false,false))
        if pg.mouse.get_pressed()[0]: 
            pg.draw.rect(ventana,(0,255,0), imagen_rect, 2,20)
            if not click_izq:
                click_izq = True
                x = mouse_x - imagen_rect.x
                y = mouse_y - imagen_rect.y

            imagen_rect.x = mouse_x - x
            imagen_rect.y = mouse_y - y
        else:
            click_izq = False"""


    # Dibuja la imagen en la ventana
    ventana.blit(imagen,imagen_rect)
    #dibuja un rectangulo alrrededor
    pg.draw.rect(ventana,(255,255,255), imagen_rect, 2,20)
    # dibujo un punto
    pg.draw.circle(ventana,(255,255,255),imagen_rect.center,1)



    # Actualizar la ventana
    pg.display.update()