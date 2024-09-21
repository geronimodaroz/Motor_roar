import pygame

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()

    

    # Iterar sobre los códigos de las teclas
    for key in range(len(keys)):
        if keys[key]:  # Si la tecla está presionada
            print(f"La tecla con código {key} está presionada")

    # Limpiar la pantalla
    screen.fill((0, 0, 0))
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
