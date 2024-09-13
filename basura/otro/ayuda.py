import pygame as pg
import ctypes
from ctypes import wintypes  # Importar wintypes correctamente

# Inicialización de Pygame
pg.init()

# Dimensiones de la ventana
width, height = 800, 600

# Crear una ventana sin bordes ni barra superior
screen = pg.display.set_mode((width, height), pg.NOFRAME)

# Establecer el título y el icono de la ventana (si lo deseas)
pg.display.set_caption("Ventana Movible")

# Obtener el identificador de la ventana de Pygame (solo en Windows)
window_id = pg.display.get_wm_info()["window"]

# Habilitar que la ventana sea movible (solo en Windows)
ctypes.windll.user32.SetWindowLongW(window_id, -16, ctypes.windll.user32.GetWindowLongW(window_id, -16) | 0x00080000)

# Variable de ejecución
running = True

# Control de movimiento de ventana
moving = False
mouse_start_x, mouse_start_y = 0, 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:  # Click izquierdo del ratón
                mouse_start_x, mouse_start_y = event.pos
                if mouse_start_y <= 30:  # Área superior de la ventana (simulación de barra de título)
                    moving = True

                    
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Soltar el click izquierdo
                moving = False
        elif event.type == pg.MOUSEMOTION and moving:
            # Obtener la posición actual del ratón
            mouse_x, mouse_y = pg.mouse.get_pos()
            
            # Calcular la nueva posición de la ventana
            delta_x = mouse_x - mouse_start_x
            delta_y = mouse_y - mouse_start_y
            
            # Obtener la posición actual de la ventana
            rect = wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(window_id, ctypes.byref(rect))

            # Mover la ventana a la nueva posición
            ctypes.windll.user32.MoveWindow(window_id, rect.left + delta_x, rect.top + delta_y, width, height, True)

    # Dibujar la "barra superior" personalizada
    screen.fill((30, 30, 30))  # Fondo de la ventana
    pg.draw.rect(screen, (100, 100, 255), (0, 0, width, 30))  # Barra superior personalizada

    pg.display.update()

pg.quit()
