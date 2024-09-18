import pygame
import ctypes
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Ventana con bordes de colores')

# Obtener el handle de la ventana
hwnd = pygame.display.get_wm_info()['window']

# Definir colores
COLOR_BORDE = 0x0000FF  # Azul en formato RGB

# Función para cambiar el color del borde
def cambiar_color_borde(hwnd, color):
    # Obtener el estilo de la ventana
    estilo = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
    # Cambiar el estilo de la ventana para permitir el cambio de color del borde
    estilo |= 0x00080000  # WS_BORDER
    ctypes.windll.user32.SetWindowLongW(hwnd, -16, estilo)
    # Cambiar el color del borde
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(color)), ctypes.sizeof(ctypes.c_int))

# Cambiar el color del borde de la ventana
cambiar_color_borde(hwnd, COLOR_BORDE)

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rellenar la ventana con un color de fondo
    ventana.fill((255, 255, 255))

    # Actualizar la pantalla
    pygame.display.flip()
