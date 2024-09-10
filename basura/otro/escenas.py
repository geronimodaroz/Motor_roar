import sys
import sdl2
import sdl2.ext

def run():
    # Inicializar SDL
    sdl2.ext.init()

    # Crear una ventana SDL sin decoración
    window = sdl2.SDL_CreateWindow(
        b"Ventana sin Barra Superior",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        800, 600,
        sdl2.SDL_WINDOW_BORDERLESS  # Sin bordes y sin barra de título
    )

    if not window:
        print(f"Error al crear la ventana: {sdl2.SDL_GetError().decode('utf-8')}")
        return

    # Crear un contexto de renderizado
    renderer = sdl2.SDL_CreateRenderer(window, -1, 0)

    running = True
    while running:
        # Manejar eventos
        events = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(events):
            if events.type == sdl2.SDL_QUIT:
                running = False
            elif events.type == sdl2.SDL_KEYDOWN:
                if events.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False

        # Limpiar la pantalla con un color de fondo (negro)
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(renderer)

        # Dibujar bordes personalizados
        border_color = sdl2.SDL_Color(255, 0, 0, 255)  # Color rojo
        draw_borders(renderer, 800, 600, border_color)

        # Actualizar la pantalla
        sdl2.SDL_RenderPresent(renderer)

    # Destruir ventana y cerrar SDL
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.ext.quit()
    sys.exit(0)


def draw_borders(renderer, width, height, color):
    """Función para dibujar bordes personalizados alrededor de la ventana."""
    sdl2.SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a)

    # Dibujar bordes (grosor de 10 píxeles)
    sdl2.SDL_RenderDrawLine(renderer, 0, 0, width, 0)         # Borde superior
    sdl2.SDL_RenderDrawLine(renderer, 0, 0, 0, height)        # Borde izquierdo
    sdl2.SDL_RenderDrawLine(renderer, width - 1, 0, width - 1, height)  # Borde derecho
    sdl2.SDL_RenderDrawLine(renderer, 0, height - 1, width, height - 1)  # Borde inferior


if __name__ == "__main__":
    run()
