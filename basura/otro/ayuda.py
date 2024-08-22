import pygame as pg
import pyperclip

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
screen = pg.display.set_mode((640, 480))
pg.display.set_caption("Copiar y Pegar con Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente
font = pg.font.Font(None, 36)

# Clase de gestión de texto
class TextManager:
    def __init__(self):
        self.text = ""
        self.cursor_position = 0

    def handle_keys(self, event):
        keys = pg.key.get_pressed()

        # Copiar (Ctrl + C)
        if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
            if event.key == pg.K_c:
                self.copy()

        # Pegar (Ctrl + V)
        if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
            if event.key == pg.K_v:
                self.paste()

    def copy(self):
        # Copiar texto al portapapeles del sistema
        pyperclip.copy(self.text)

    def paste(self):
        # Pegar el texto del portapapeles del sistema
        pasted_text = pyperclip.paste()
        self.text = self.text[:self.cursor_position] + pasted_text + self.text[self.cursor_position:]
        self.cursor_position += len(pasted_text)

    def render(self, screen):
        # Renderizar el texto en la pantalla
        screen.fill(WHITE)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (50, 200))
        pg.display.flip()

# Instancia de la clase TextManager
text_manager = TextManager()

# Bucle principal
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            text_manager.handle_keys(event)

    # Renderizar texto en la pantalla
    text_manager.render(screen)

# Cerrar Pygame
pg.quit()
