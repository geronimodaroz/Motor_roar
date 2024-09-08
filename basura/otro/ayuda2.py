import pygame as pg
pg.init()

# Crear una ventana sin decoración
screen = pg.display.set_mode((800, 600), pg.NOFRAME)

# Bucle principal
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Dibujar tu propia barra superior
    pg.draw.rect(screen, (100, 100, 255), (0, 0, 800, 30))  # Barra superior personalizada

    pg.display.update()

pg.quit()
