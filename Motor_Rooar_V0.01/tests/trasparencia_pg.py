import pygame
import ctypes
from ctypes import wintypes

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)  # Sin marco y con soporte de transparencia
pygame.display.set_caption("Ventana Transparente con Pygame")

# Función para hacer la ventana transparente
def make_window_transparent():
    hwnd = pygame.display.get_wm_info()["window"]  # Obtener el identificador de la ventana
    # Cambiar el estilo de la ventana para permitir la transparencia
    ctypes.windll.user32.SetWindowLongW(hwnd, -20,  # GWL_EXSTYLE
        ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00080000)  # WS_EX_LAYERED

    # Establecer la transparencia de la ventana
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000001)  # LWA_ALPHA

# Llamar a la función para hacer la ventana transparente
make_window_transparent()

# Bucle principal de la aplicación
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla
    screen.fill((0, 0, 0, 0))  # Rellenar con color transparente

    # Dibujar un rectángulo rojo semi-transparente
    pygame.draw.rect(screen, (255, 0, 0, 128), (100, 100, 200, 150))  # Rojo semi-transparente

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
