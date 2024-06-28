
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
#ventana = pg.display.set_mode((ventana_ancho, ventana_alto),pg.RESIZABLE)
ventana = pg.display.set_mode((ventana_ancho, ventana_alto))




# Cargar la imagen
imagen = pg.image.load("otro/esqueleto.png")
imagen = pg.transform.scale(imagen,(300,300))


# Obtén el rectángulo de la imagen
imagen_rect = imagen.get_rect()
# Coordenadas de la imagen en la ventana
imagen_rect.center = (ventana_ancho // 2, ventana_alto // 2)




# Estado del arrastre
arrastrando = False




def manejar_evento_salida():
    pygame.quit()
    sys.exit()


def manejar_evento_clic():

    if pg.mouse.get_pressed()[0]:
        print(event.click)
    if pg.mouse.get_pressed()[1]:
        print(event.click)
    if pg.mouse.get_pressed()[2]:
        print(event.click)


def manejar_evento_movimiento_mouse():
    if arrastrando:
        imagen_rect.x += event.motion[0]
        imagen_rect.y += event.motion[1]




def evento_redimensionar():
    #print("evento_redimensionar")
    pg.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)



eventos = {
    pg.QUIT: manejar_evento_salida,
    #pg.USEREVENT+3: manejar_evento_clic,
    #pg.USEREVENT+2: manejar_evento_movimiento_mouse,
    #pg.USEREVENT+1: evento_redimensionar,

}

# variables
mouse_position = (0,0)
mouse_motion = (0,0)
mouse_click = (False,False,False)


# Bucle principal del juego
while True:


    # evento movimiento mouse
    if mouse_position != pg.mouse.get_pos():

        event_mouse_motion = pg.USEREVENT+1

        x = mouse_position[0]
        y = mouse_position[1]

        mouse_motion = (pg.mouse.get_pos()[0] - x, pg.mouse.get_pos()[1] - y)

        pg.event.post(pg.event.Event(event_mouse_motion,motion = mouse_motion ))

        mouse_position = pg.mouse.get_pos()

    else: mouse_motion = (0,0)



    # evento mouse click
    if pg.mouse.get_pressed() != (0,0,0):

        event_mouse_click = pg.USEREVENT+2

        mouse_click = pg.mouse.get_pressed()

        pg.event.post(pg.event.Event(event_mouse_click,click = mouse_click ))

    else: mouse_click = (False,False,False)
    
    

    # evento personalizado
    if mouse_click[0] >= ventana_ancho-20:
        pg.event.post(pg.event.Event(pg.USEREVENT+1))


    

    lista = []
    for event in pg.event.get():
        eventos.get(event.type, lambda: None)() # llama a todos los eventos
        lista.append(event.type) # agrega todos los eventos a una lista





    if pg.USEREVENT+1 in lista :
        # cambia el icono del mouse
        c=0
    else:
        pg.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    



    # Aquí puedes agregar la lógica de tu juego y dibujar en la ventana
    


    # Limpia la ventana
    ventana.fill((0, 0, 0))


    # Dibuja la imagen en la ventana
    ventana.blit(imagen,imagen_rect)
    #dibuja un rectangulo alrrededor
    pg.draw.rect(ventana,(255,255,255), imagen_rect, 2,20)
    # dibujo un punto
    pg.draw.circle(ventana,(255,255,255),imagen_rect.center,1)
    



    # Actualizar la ventana
    pg.display.update()