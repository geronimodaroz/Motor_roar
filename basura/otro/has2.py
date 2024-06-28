import pygame
import sys
import time

class Font:
    def __init__(self):
        self.font = pygame.font.Font(None, 16)
        #self.color = (180,180,180)
    def surf_font(self,text,color = (180,180,180)):
        surf_text = self.font.render(text, True, color)
        return surf_text

# Inicializa Pygame
pygame.init()

# Establece el tamaño de la pantalla
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# Establece el título de la ventana
pygame.display.set_caption("Mi Juego")

# Color de fondo (gris)
background_color = (128, 128, 128)

# Bandera para verificar si se ha realizado el dibujo inicial
initial_draw_done = False


# fuente para el contador de FPS
fps_text = Font().surf_font("")
# Inicializar el contador de fotogramas
fps_counter = 0
start_time = time.time()

# Bucle principal del juego
running = True
while running:
    
    # FPS
    fps_counter += 1
    elapsed_time = time.time() - start_time
    if elapsed_time >= 0.5:
        fps = fps_counter / elapsed_time
        fps_text = Font().surf_font(f"FPS: {fps:.2f}", (250, 250, 250))
        fps_counter = 0
        start_time = time.time()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rellena la pantalla con el color de fondo
    screen.fill(background_color)
    
    # Dibuja algo solo una vez
    if not initial_draw_done:
        
        
        pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)  # Dibuja un círculo rojo
        pygame.display.flip()
        initial_draw_done = True
    
    # FPS
    screen.blit(fps_text, (800 - fps_text.get_width() - 15,600 - fps_text.get_height() -10)) # fps
    rect = (800-100,600-100,100,100)
    pygame.display.update(rect)

    # Aquí iría el dibujo continuo, si es necesario
    # Por ejemplo, dibujar objetos que se mueven, actualizan, etc.

    # Actualiza la pantalla
    #ygame.display.flip()

# Cierra Pygame
pygame.quit()
sys.exit()
