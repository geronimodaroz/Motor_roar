import pygame as pg

class WindowManager:
    def __init__(self, event_dict, screen):
        self.screen = screen
        self.event_dict = event_dict
        self.width, self.height = self.screen.get_size()
        # Crear tus rects y otros elementos gráficos aquí
        self.initialize_rects()

    def initialize_rects(self):
        # Crea o inicializa los rects con las dimensiones iniciales de la ventana
        self.rect = pg.Rect(10, 10, 200, 50)  # Ejemplo
        # Más inicializaciones de rects aquí según sea necesario

    def handle_resize(self, event):
        """ Maneja el evento de redimensionamiento de la ventana """
        self.width, self.height = event.w, event.h
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)

        # Recalcula las dimensiones y posiciones de los rects
        self.update_rects()

    def update_rects(self):
        """ Recalcula las posiciones y dimensiones de los rects cuando cambia el tamaño de la ventana """
        # Aquí puedes definir cómo ajustar los rects según el nuevo tamaño de la ventana.
        self.rect.width = self.width // 10  # Ejemplo de ajuste dinámico
        self.rect.height = self.height // 10
        # Recalcula otros rects de forma similar

    def draw(self):
        self.screen.fill((0, 0, 0))  # Limpiar la pantalla con un color de fondo
        pg.draw.rect(self.screen, (255, 0, 0), self.rect)  # Dibuja el rectángulo
        pg.display.flip()

# Ejemplo de uso en un bucle principal de pygame
def main():
    pg.init()
    screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
    event_dict = {}  # Inicializa tu diccionario de eventos
    window_manager = WindowManager(event_dict, screen)
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                window_manager.handle_resize(event)

        window_manager.draw()

    pg.quit()

if __name__ == "__main__":
    main()
