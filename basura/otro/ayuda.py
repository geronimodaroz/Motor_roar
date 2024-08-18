import pygame as pg

class ClickHandler:
    def __init__(self, click_delay=300):  # Retardo entre clics en milisegundos
        self.click_count = 0
        self.last_click_time = 0
        self.click_delay = click_delay

    def handle_click(self):
        current_time = pg.time.get_ticks()

        # Si el tiempo desde el último clic es menor que el retardo permitido
        if current_time - self.last_click_time <= self.click_delay:
            self.click_count += 1
        else:
            # Reiniciar la cuenta de clics si se ha superado el intervalo
            self.click_count = 1

        self.last_click_time = current_time

        # Detectar el tipo de clic
        if self.click_count == 2:
            print("Doble clic detectado")
        elif self.click_count == 3:
            print("Triple clic detectado")

# Inicialización de Pygame
pg.init()
screen = pg.display.set_mode((800, 600))
click_handler = ClickHandler()

running = True
while running:
    for event in pg.event.get():
        # Detección del evento de clic izquierdo
        if event.type == pg.QUIT:
            running = False

        # Verificación de si se hizo clic con el botón izquierdo del mouse
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # event.button == 1 indica clic izquierdo
            click_handler.handle_click()

    # Actualización de la pantalla y otros elementos del juego
    screen.fill((0, 0, 0))
    pg.display.flip()

pg.quit()
