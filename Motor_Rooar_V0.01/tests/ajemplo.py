import pygame as pg
import sys

# Inicializar Pygame
pg.init()

# Definir dimensiones de la ventana y superficie
WIDTH, HEIGHT = 800, 600
SURFACE_WIDTH, SURFACE_HEIGHT = 400, 300

# Crear ventana y superficie
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ventana con redibujado optimizado")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Crear la superficie y rellenarla con color azul
surface = pg.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
surface.fill(BLUE)

# Posición de la superficie en la ventana
surface_x = (WIDTH - SURFACE_WIDTH) // 2
surface_y = (HEIGHT - SURFACE_HEIGHT) // 2

# Dimensiones y posición inicial del rectángulo
rect_width, rect_height = 50, 50
rect_x, rect_y = (SURFACE_WIDTH - rect_width) // 2, (SURFACE_HEIGHT - rect_height) // 2

# Variables para el estado de arrastre y posición anterior
dragging = False
prev_rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)

# Crear un objeto para controlar los FPS
clock = pg.time.Clock()

# Dibujar el contenido inicial de la ventana
window.fill(WHITE)
surface.fill(BLUE)
pg.draw.rect(surface, RED, prev_rect)
window.blit(surface, (surface_x, surface_y))
pg.display.flip()

# Bucle principal
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Obtener la posición del clic del mouse
            mouse_x, mouse_y = event.pos

            # Convertir la posición del mouse a coordenadas dentro de la superficie
            local_x, local_y = mouse_x - surface_x, mouse_y - surface_y

            # Comprobar si el clic está dentro del rectángulo
            if prev_rect.collidepoint(local_x, local_y):
                dragging = True  # Activar arrastre
                offset_x = local_x - rect_x
                offset_y = local_y - rect_y

        elif event.type == pg.MOUSEBUTTONUP:
            dragging = False  # Desactivar arrastre al soltar el botón

        elif event.type == pg.MOUSEMOTION:
            
            if dragging:
                # Mover el rectángulo en función de la posición del mouse
                mouse_x, mouse_y = event.pos
                local_x, local_y = mouse_x - surface_x, mouse_y - surface_y

                # Ajustar posición del rectángulo basado en el desplazamiento del clic inicial
                new_rect_x = local_x - offset_x
                new_rect_y = local_y - offset_y

                # Limitar el rectángulo dentro de los bordes de la superficie
                new_rect_x = max(0, min(new_rect_x, SURFACE_WIDTH - rect_width))
                new_rect_y = max(0, min(new_rect_y, SURFACE_HEIGHT - rect_height))

                # Verificar si el rectángulo se movió
                if new_rect_x != rect_x or new_rect_y != rect_y:
                    # Guardar la posición anterior del rectángulo
                    prev_rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)

                    # Actualizar la nueva posición del rectángulo
                    rect_x, rect_y = new_rect_x, new_rect_y
                    current_rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)

                    # Limpiar solo la parte anterior del rectángulo
                    surface.fill(BLUE, prev_rect)

                    # Dibujar el rectángulo en su nueva posición
                    pg.draw.rect(surface, RED, current_rect)

                    # Actualizar solo el área de la ventana que corresponde a la superficie
                    window.blit(surface, (surface_x, surface_y))

                    # Actualizar solo la parte del rectángulo que cambió
                    pg.display.update(pg.Rect(surface_x + prev_rect.x, surface_y + prev_rect.y, rect_width, rect_height))
                    pg.display.update(pg.Rect(surface_x + rect_x, surface_y + rect_y, rect_width, rect_height))

                    # Dibujar un cuadrado verde en las áreas que se actualizan
                    pg.draw.rect(window, GREEN, pg.Rect(surface_x + prev_rect.x, surface_y + prev_rect.y, rect_width, rect_height))
                    pg.draw.rect(window, GREEN, pg.Rect(surface_x + rect_x, surface_y + rect_y, rect_width, rect_height))

    # Limitar los FPS a 60
    clock.tick(60)

    # Actualizar la pantalla
    #pg.display.flip()

# Salir de Pygame
pg.quit()
sys.exit()
