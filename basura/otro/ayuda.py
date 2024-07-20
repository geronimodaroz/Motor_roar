import pygame as pg

# Inicializa Pygame
pg.init()

# Configura la ventana principal
screen_width, screen_height = 800, 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Ventana Principal con Subventana")

# Crea una superficie principal (fondo de la ventana principal)
main_surface = pg.Surface((screen_width, screen_height))
main_surface.fill((200, 200, 200))  # Color gris claro

# Crea una superficie que actúe como una "ventana" dentro de la ventana principal
window_width, window_height = 300, 200
window_surface = pg.Surface((window_width, window_height))
window_surface.fill((100, 100, 255))  # Color azul claro

# Posición de la ventana dentro de la ventana principal
window_x, window_y = 50, 50

# Bucle principal del juego
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Rellena la pantalla principal
    screen.blit(main_surface, (0, 0))

    # Dibuja la ventana dentro de la ventana principal
    screen.blit(window_surface, (window_x, window_y))

    # Actualiza la pantalla
    pg.display.flip()

# Finaliza Pygame
pg.quit()
