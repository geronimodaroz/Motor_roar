import pygame
import pygame.gfxdraw
import sys

# Inicializar Pygame
pygame.init()

# Configurar pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rectángulo con Bordes Redondeados y Transparencia")

# Colores
background_color = (0, 0, 0)
rect_color = (255, 0, 0, 128)  # Rojo con 50% de transparencia

# Función para dibujar un rectángulo con bordes redondeados
def draw_rounded_rect(surface, rect, color, radius):
    x, y, w, h = rect
    pygame.gfxdraw.aacircle(surface, x + radius, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + radius, radius, color)
    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + radius, radius, color)
    pygame.gfxdraw.aacircle(surface, x + radius, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + h - radius - 1, radius, color)
    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)
    pygame.gfxdraw.box(surface, (x + radius, y, w - 2 * radius, h), color)
    pygame.gfxdraw.box(surface, (x, y + radius, w, h - 2 * radius), color)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rellenar la pantalla con el color de fondo
    screen.fill(background_color)

    # Dibujar el rectángulo con bordes redondeados y transparencia
    draw_rounded_rect(screen, (300, 225, 200, 150), rect_color, 20)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
