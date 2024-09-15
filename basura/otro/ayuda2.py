import pygame as pg
import sys
import ctypes

# Inicializa Pygame
pg.init()

# Configuración de pantalla
width, height = 800, 600
screen = pg.display.set_mode((width, height), pg.NOFRAME)  # Ventana sin bordes
pg.display.set_caption("Ventana Sin Bordes con Bordes Redimensionables")

# Configuración de colores
border_color = (255, 0, 0)  # Rojo para los bordes
border_thickness = 10       # Grosor del borde
background_color = (0, 0, 0)  # Negro de fondo

# Variables de control para arrastrar y redimensionar
is_dragging = False
is_resizing = False
resize_direction = None
drag_offset_x, drag_offset_y = 0, 0
window_x, window_y = 100, 100  # Posición inicial de la ventana
min_width, min_height = 100, 100  # Tamaño mínimo de la ventana

# Función para mover la ventana utilizando ctypes en Windows
def move_window(x, y):
    global window_x, window_y
    hwnd = pg.display.get_wm_info()['window']  # Obtener el manejador de la ventana
    ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)
    window_x, window_y = x, y  # Actualizar posición de la ventana

# Determina la dirección de redimensionamiento según la posición del ratón
def get_resize_direction(mouse_x, mouse_y, width, height, border_thickness):
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
                    is_resizing = True  # Iniciar redimensionamiento
                else:
                    is_dragging = True  # Iniciar arrastre
                    drag_offset_x, drag_offset_y = mouse_x, mouse_y
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False
                is_resizing = False
        elif event.type == pg.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if is_dragging:
                # Mueve la ventana mientras se arrastra
                new_x = window_x + (mouse_x - drag_offset_x)
                new_y = window_y + (mouse_y - drag_offset_y)
                move_window(new_x, new_y)  # Usar ctypes para mover la ventana en Windows
            elif is_resizing:
                # Redimensiona la ventana mientras se arrastra un borde
                if resize_direction == 'right':
                    width = max(min_width, mouse_x)
                elif resize_direction == 'bottom':
                    height = max(min_height, mouse_y)
                elif resize_direction == 'left':
                    delta = mouse_x - drag_offset_x
                    new_width = max(min_width, width - delta)
                    if new_width != width:
                        move_window(window_x + delta, window_y)  # Mover para compensar el redimensionamiento
                        width = new_width
                elif resize_direction == 'top':
                    delta = mouse_y - drag_offset_y
                    new_height = max(min_height, height - delta)
                    if new_height != height:
                        move_window(window_x, window_y + delta)  # Mover para compensar
                        height = new_height
                # Actualiza el tamaño de la ventana
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
