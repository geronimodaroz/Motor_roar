import pygame as pg
import sys

# Inicializa Pygame
pg.init()

# Configuración de pantalla
width, height = 800, 600
screen = pg.display.set_mode((width, height), pg.NOFRAME)
pg.display.set_caption("Ventana Sin Bordes con Bordes Redimensionables")

# Configuración de colores
border_color = (255, 0, 0)  # Rojo
border_thickness = 10       # Grosor del borde
background_color = (0, 0, 0)  # Negro

# Variables de control para arrastrar y redimensionar
is_dragging = False
is_resizing = False
resize_direction = None
drag_offset_x, drag_offset_y = 0, 0
min_width, min_height = 100, 100  # Tamaño mínimo de la ventana

def get_resize_direction(mouse_x, mouse_y, width, height, border_thickness):
    """Determina la dirección de redimensionamiento según la posición del ratón."""
    if mouse_x < border_thickness:
        return 'left'
    elif mouse_x > width - border_thickness:
        return 'right'
    elif mouse_y < border_thickness:
        return 'top'
    elif mouse_y > height - border_thickness:
        return 'bottom'
    return None

# Bucle principal
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Comenzar a arrastrar o redimensionar
            if event.button == 1:  # Botón izquierdo del ratón
                mouse_x, mouse_y = event.pos
                resize_direction = get_resize_direction(mouse_x, mouse_y, width, height, border_thickness)
                if resize_direction:
                    is_resizing = True
                else:
                    is_dragging = True
                    drag_offset_x, drag_offset_y = mouse_x, mouse_y
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False
                is_resizing = False
        elif event.type == pg.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if is_dragging:
                # Mueve la ventana mientras se arrastra
                new_x = mouse_x - drag_offset_x
                new_y = mouse_y - drag_offset_y
                pg.display.set_mode((width, height), pg.NOFRAME)
            elif is_resizing:
                # Redimensiona la ventana mientras se arrastra un borde
                if resize_direction == 'right':
                    width = max(min_width, mouse_x)
                elif resize_direction == 'bottom':
                    height = max(min_height, mouse_y)
                elif resize_direction == 'left':
                    delta = mouse_x - drag_offset_x
                    width = max(min_width, width - delta)
                    drag_offset_x = mouse_x
                elif resize_direction == 'top':
                    delta = mouse_y - drag_offset_y
                    height = max(min_height, height - delta)
                    drag_offset_y = mouse_y
                screen = pg.display.set_mode((width, height), pg.NOFRAME)

    # Rellenar el fondo
    screen.fill(background_color)

    # Dibujar los bordes personalizados
    pg.draw.rect(screen, border_color, (0, 0, width, border_thickness))  # Borde superior
    pg.draw.rect(screen, border_color, (0, height - border_thickness, width, border_thickness))  # Borde inferior
    pg.draw.rect(screen, border_color, (0, 0, border_thickness, height))  # Borde izquierdo
    pg.draw.rect(screen, border_color, (width - border_thickness, 0, border_thickness, height))  # Borde derecho

    # Actualizar la pantalla
    pg.display.update()

pg.quit()
sys.exit()
