
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

# Escenas
class Escena():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def draw_background(self, color):
        pg.draw.rect(ventana,color,Escena)


Escena = Escena(0,0,ventana_ancho,ventana_alto)



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
    if event.button == 1 and imagen_rect.collidepoint(event.pos):
        global arrastrando
        arrastrando = True


def manejar_evento_soltar_clic():
    global arrastrando
    if arrastrando:
        arrastrando = False

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
    #pg.MOUSEBUTTONDOWN: manejar_evento_clic,
    #pg.MOUSEBUTTONUP: manejar_evento_soltar_clic,
    #pg.MOUSEMOTION: manejar_evento_movimiento_mouse,
    pg.USEREVENT+3: manejar_evento_clic,
    pg.USEREVENT+2: manejar_evento_movimiento_mouse,
    pg.USEREVENT+1: evento_redimensionar,

}

# variables
mouse_position = pg.mouse.get_pos()

# Bucle principal del juego
while True:


    # evento movimiento mouse
    if mouse_position != pg.mouse.get_pos():
        x = mouse_position[0]
        y = mouse_position[1]
        mouse_motion = (pg.mouse.get_pos()[0] - x, pg.mouse.get_pos()[1] - y)
        pg.event.post(pg.event.Event(pg.USEREVENT+2,motion = mouse_motion ))
        mouse_position = pg.mouse.get_pos()


    # evento mouse click
    if pg.mouse.get_pressed() != (0,0,0):
        mouse_click = pg.mouse.get_pressed()
        pg.event.post(pg.event.Event(pg.USEREVENT+3,click = mouse_click ))




    

    # evento personalizado
    if pg.mouse.get_pos()[0] >= ventana_ancho-20:
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

    #dibujamos canvas
    Escena.draw_background((60,60,60))

    # Dibuja la imagen en la ventana
    ventana.blit(imagen,imagen_rect)
    #dibuja un rectangulo alrrededor
    pg.draw.rect(ventana,(255,255,255), imagen_rect, 2,20)
    # dibujo un punto
    pg.draw.circle(ventana,(255,255,255),imagen_rect.center,1)
    



    # Actualizar la ventana
    pg.display.update()