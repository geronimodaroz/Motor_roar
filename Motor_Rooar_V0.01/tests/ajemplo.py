import pygame as pg
import tkinter as tk
import sys

# Inicializa Pygame
pg.init()

# Configuración de la ventana principal de Pygame
window = pg.display.set_mode((800, 600))
pg.display.set_caption("Ventana Principal - Pygame")

background_color = (30, 30, 30)
clock = pg.time.Clock()

def create_tkinter_window():
    """Crea una ventana de Tkinter redimensionable desde las esquinas."""
    root = tk.Tk()
    root.overrideredirect(True)  # Sin barra de título
    root.attributes('-alpha', 0.4)  # Transparencia
    root.geometry("400x300+100+100")  # Tamaño y posición inicial

    # Variables de estado
    resizing = None  # 'left' o 'right'
    start_x = start_y = win_start_width = win_start_height = win_start_x = 0

    def start_resize(event, direction):
        """Inicia el redimensionamiento."""
        nonlocal resizing, start_x, start_y, win_start_width, win_start_height, win_start_x
        resizing = direction
        start_x, start_y = event.x_root, event.y_root
        win_start_width = root.winfo_width()
        win_start_height = root.winfo_height()
        win_start_x = root.winfo_x()

    def do_resize(event):
        """Realiza el redimensionamiento."""
        dx = event.x_root - start_x
        dy = event.y_root - start_y

        if resizing == 'right':
            new_width = max(100, win_start_width + dx)
            new_height = max(100, win_start_height + dy)
            root.geometry(f"{new_width}x{new_height}")
        elif resizing == 'left':
            new_width = max(100, win_start_width - dx)
            new_height = max(100, win_start_height + dy)
            new_x = win_start_x + dx
            root.geometry(f"{new_width}x{new_height}+{new_x}+{root.winfo_y()}")

    def release(event):
        """Termina el redimensionamiento."""
        nonlocal resizing
        resizing = None

    def enter_resize(event):
        """Detecta la esquina para redimensionar."""
        width, height = root.winfo_width(), root.winfo_height()
        if event.x >= width - 10 and event.y >= height - 10:
            root.config(cursor="bottom_right_corner")
            root.bind("<Button-1>", lambda e: start_resize(e, 'right'))
        elif event.x <= 10 and event.y >= height - 10:
            root.config(cursor="bottom_left_corner")
            root.bind("<Button-1>", lambda e: start_resize(e, 'left'))
        else:
            root.config(cursor="arrow")
            root.bind("<Button-1>", lambda e: None)

    # Conexiones de eventos
    root.bind("<B1-Motion>", do_resize)
    root.bind("<ButtonRelease-1>", release)
    root.bind("<Motion>", enter_resize)

    # Botón de cierre
    tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
    root.mainloop()

# Bucle principal de Pygame
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            create_tkinter_window()

    window.fill(background_color)
    pg.display.update()
    clock.tick(60)
