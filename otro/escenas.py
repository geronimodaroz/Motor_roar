import pygame as pg
import sys

# Inicializar Pygame
pg.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir dimensiones de la ventana
ventana_ancho = 800
ventana_alto = 600

# Crear la ventana
ventana = pg.display.set_mode((ventana_ancho, ventana_alto))
pg.display.set_caption("Ejemplo de Escenas en Pygame")

# Definir las escenas
class EscenaInicio:
    def __init__(self):
        self.fuente = pg.font.Font(None, 36)

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                return "juego"  # Cambiar a la escena de juego

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)
        texto = self.fuente.render("Presiona ESPACIO para comenzar", True, BLANCO)
        pantalla.blit(texto, (ventana_ancho // 4, ventana_alto // 2))

class EscenaJuego:
    def __init__(self):
        self.fuente = pg.font.Font(None, 36)

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return "inicio"  # Cambiar a la escena de inicio

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(BLANCO)
        texto = self.fuente.render("Presiona ESC para volver al inicio", True, NEGRO)
        pantalla.blit(texto, (ventana_ancho // 4, ventana_alto // 2))

# Inicializar las escenas
escena_actual = "inicio"
escena_inicio = EscenaInicio()
escena_juego = EscenaJuego()

# Bucle principal del juego
while True:
    eventos = pg.event.get()

    # Manejar eventos según la escena actual
    if escena_actual == "inicio":
        transicion = escena_inicio.manejar_eventos(eventos)
    elif escena_actual == "juego":
        transicion = escena_juego.manejar_eventos(eventos)

    # Cambiar a la nueva escena si es necesario
    if transicion:
        if transicion == "inicio":
            escena_actual = "inicio"
        elif transicion == "juego":
            escena_actual = "juego"

    # Actualizar y dibujar según la escena actual
    if escena_actual == "inicio":
        escena_inicio.actualizar()
        escena_inicio.dibujar(ventana)
    elif escena_actual == "juego":
        escena_juego.actualizar()
        escena_juego.dibujar(ventana)

    # Actualizar la ventana
    pg.display.flip()
