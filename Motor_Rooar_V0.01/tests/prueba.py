import tkinter as tk
import os
import pygame as pg

class TransparentWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.overrideredirect(True)

        # Crear un marco para contener Pygame
        self.pygame_frame = tk.Frame(self.root, width=800, height=600)
        self.pygame_frame.pack()

        # Botón de cerrar
        close_button = tk.Button(self.root, text="Cerrar", command=self.close, bg='red', fg='white')
        close_button.pack(side="top", padx=10, pady=10)

        # Iniciar Pygame después de que se haya creado el marco
        self.root.after(100, self.embed_pygame)  # Espera un momento para asegurarte de que el marco está listo

    def embed_pygame(self):
        # Inicializar Pygame
        pg.init()

        # Establecer el ID de la ventana de Pygame
        os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())
        self.screen = pg.display.set_mode((800, 600), pg.NOFRAME)

        self.running = True
        self.pygame_loop()

    def pygame_loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
            
            # Lógica de dibujo
            self.screen.fill((0, 0, 0))  # Color de fondo
            pg.display.flip()  # Actualizar la pantalla


        

    def close(self):
        self.running = False
        self.root.destroy()  # Cierra la ventana de Tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = TransparentWindow(root)
    root.mainloop()
