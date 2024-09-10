import pygame as pg
import ctypes

# Definir la estructura RECT
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

# Inicialización de Pygame
pg.init()

# Dimensiones de la ventana
width, height = 800, 600

# Crear una ventana sin bordes ni barra superior
screen = pg.display.set_mode((width, height), pg.NOFRAME)

# Establecer el título y el icono de la ventana (si lo deseas)
pg.display.set_caption("Ventana Personalizada")

# Obtener el identificador de la ventana de Pygame (solo en Windows)
window_id = pg.display.get_wm_info()["window"]

# Habilitar que la ventana sea movible (solo en Windows)
ctypes.windll.user32.SetWindowLongW(window_id, -16, ctypes.windll.user32.GetWindowLongW(window_id, -16) | 0x00080000)

# Variable de ejecución
running = True

# Control de movimiento de ventana
moving = False
start_x, start_y = 0, 0

# Obtener la posición inicial de la ventana
rect = RECT()
ctypes.windll.user32.GetWindowRect(window_id, ctypes.byref(rect))
window_x, window_y = rect.left, rect.top

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Detectar si el ratón se ha presionado dentro del área de la "barra superior" simulada
            if event.button == 1:
                mx, my = event.pos
                if my <= 30:  # Supongamos que 30 píxeles es el alto de la "barra superior"
                    moving = True
                    start_x, start_y = mx, my
        elif event.type == pg.MOUSEBUTTONUP:
            # Detectar si el ratón se ha soltado
            if event.button == 1:
                moving = False
        elif event.type == pg.MOUSEMOTION and moving:
            # Mover la ventana mientras el ratón se arrastra
            mx, my = pg.mouse.get_pos()
            new_x = window_x + (mx - start_x)
            new_y = window_y + (my - start_y)
            ctypes.windll.user32.MoveWindow(window_id, new_x, new_y, width, height, True)

    # Dibujar la "barra superior" personalizada
    screen.fill((30, 30, 30))  # Fondo de la ventana
    pg.draw.rect(screen, (100, 100, 255), (0, 0, width, 30))  # Barra superior personalizada

    pg.display.update()

pg.quit()
