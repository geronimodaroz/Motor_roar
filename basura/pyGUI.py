import pygame
import pygame_gui

# Inicializar Pygame
pygame.init()

# Crear la pantalla de Pygame
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Ventana con pygame_gui")

# Crear el administrador de UI
ui_manager = pygame_gui.UIManager(window_size)

# Crear un botón y un cuadro de entrada de texto
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 500), (100, 50)),
                                      text='Presioname',
                                      manager=ui_manager)

text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 400), (200, 50)),
                                                 manager=ui_manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0  # Tiempo entre frames (ajusta la velocidad de actualización)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Procesar eventos de la UI
        ui_manager.process_events(event)

        # Verificar si el botón fue presionado
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print(f"Texto ingresado: {text_entry.get_text()}")

    # Actualizar la UI
    ui_manager.update(time_delta)

    # Dibujar en la ventana
    window.fill((0, 0, 0))  # Fondo negro
    ui_manager.draw_ui(window)  # Dibujar la interfaz de usuario

    # Actualizar la pantalla
    pygame.display.update()

# Finalizar Pygame
pygame.quit()
