# import sys
# from PySide6.QtCore import Qt, QPoint
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PySide6.QtGui import QPainter, QColor

# class TransparentWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Configuración de la ventana
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setGeometry(100, 100, 400, 400)  # Tamaño de la ventana

#         self.is_dragging = False
#         self.drag_start_position = QPoint()

#         # Crear botón de cierre
#         self.close_button = QPushButton('Cerrar', self)
#         self.close_button.setGeometry(10, 10, 60, 30)  # Tamaño y posición del botón
#         self.close_button.clicked.connect(self.close)  # Conectar el botón a la función de cierre

#     def paintEvent(self, event):
#         painter = QPainter(self)
        
#         # Dibujar el fondo (transparente)
#         painter.setBrush(QColor(0, 0, 0, 0))  # Color transparente
#         painter.drawRect(0, 0, self.width(), self.height())

#         # Dibujar los bordes
#         border_color = QColor(255, 0, 0)  # Color del borde (rojo)
#         painter.setPen(border_color)
#         painter.setBrush(QColor(0, 0, 0, 0))  # Fondo transparente
#         painter.drawRect(0, 0, self.width() - 1, self.height() - 1)  # Borde externo
#         painter.drawRect(5, 5, self.width() - 11, self.height() - 11)  # Borde interno

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.is_dragging = True
#             self.drag_start_position = event.globalPosition().toPoint() - self.pos()

#     def mouseMoveEvent(self, event):
#         if self.is_dragging:
#             self.move(event.globalPosition().toPoint() - self.drag_start_position)

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.is_dragging = False

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = TransparentWindow()
#     window.show()
#     sys.exit(app.exec())



import tkinter as tk
import pygame
import os

class TransparentWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600+100+100")  # Tamaño y posición de la ventana
        self.root.overrideredirect(True)  # Eliminar la barra superior nativa
        
        # Crear el marco externo con bordes personalizados
        self.border_frame = tk.Frame(self.root, bg='black', bd=5)  # Color del borde externo
        self.border_frame.pack(fill="both", expand=True)
        
        # Crear la barra superior personalizada
        self.title_bar = tk.Frame(self.border_frame, bg='black', relief='raised', bd=0)  # Barra superior de color oscuro
        self.title_bar.pack(fill="x")

        # Botón de cerrar en la barra superior
        close_button = tk.Button(self.title_bar, text="Cerrar", command=self.close, bg='red', fg='white')
        close_button.pack(side="right", padx=10, pady=2)

        # Etiqueta para arrastrar la ventana
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.move_window)
        
        # Crear el área central de contenido
        self.content_area = tk.Frame(self.border_frame, bg='gray')
        self.content_area.pack(fill="both", expand=True)
        
        # Inicializar Pygame en un Frame
        self.pygame_frame = tk.Frame(self.content_area, width=400, height=400, bg='blue', highlightthickness=0)
        self.pygame_frame.place(x=100, y=100)  # Colocar el frame en el centro
        
        # Inicializar la ventana de Pygame
        self.embed_pygame()

    def embed_pygame(self):
        # Iniciar Pygame
        os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())  # Vincular Pygame con el ID del frame
        pygame.init()

        # Configurar la ventana de Pygame dentro del frame
        self.screen = pygame.display.set_mode((400, 400), pygame.NOFRAME )  # Ventana sin marco y con transparencia

        # Ejemplo simple de Pygame: Dibujar en la ventana incrustada
        self.running = True
        self.pygame_loop()

    def pygame_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Dibujar en la ventana de Pygame
            self.screen.fill((0, 128, 255))  # Fondo azul
            pygame.draw.circle(self.screen, (255, 0, 0), (200, 200), 50)  # Círculo rojo

            # Actualizar la pantalla de Pygame
            pygame.display.update()

            # Actualizar la ventana de Tkinter
            self.root.update_idletasks()
            self.root.update()

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def move_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def close(self):
        self.running = False  # Cierra el loop de Pygame
        self.root.destroy()  # Cierra la ventana de Tkinter


if __name__ == "__main__":
    root = tk.Tk()
    app = TransparentWindow(root)
    root.mainloop()




# import tkinter as tk
# import pygame
# import os

# class TransparentWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.overrideredirect(True)  # Eliminar el marco de la ventana
#         self.root.geometry("600x600+100+100")  # Tamaño y posición de la ventana
#         self.root.wm_attributes("-topmost", True)  # Mantener la ventana siempre encima

#         # Crear un lienzo para dibujar (sin bordes blancos)
#         self.canvas = tk.Canvas(self.root, width=600, height=600, bg='gray', highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)  # Llenar toda la ventana

#         # Dibujar bordes en el lienzo (más gruesos)
#         self.borders = {
#             "left": self.canvas.create_rectangle(0, 0, 10, 600, fill="black", width=0),
#             "right": self.canvas.create_rectangle(590, 0, 600, 600, fill="black", width=0),
#             "top": self.canvas.create_rectangle(0, 0, 600, 10, fill="black", width=0),
#             "bottom": self.canvas.create_rectangle(0, 590, 600, 600, fill="black", width=0)
#         }

#         # Botón de cerrar
#         close_button = tk.Button(self.root, text="Cerrar", command=self.close, bg='red', fg='white')
#         close_button.place(x=10, y=10)  # Posición del botón

#         # Configurar eventos para mover la ventana
#         self.canvas.bind("<ButtonPress-1>", self.start_move)
#         self.canvas.bind("<B1-Motion>", self.move_window)

#         # Inicializar Pygame en un Frame
#         self.pygame_frame = tk.Frame(self.root, width=400, height=400, bg='blue', highlightthickness=0)
#         self.pygame_frame.place(x=100, y=100)  # Colocar el frame en el centro

#         # Inicializar la ventana de Pygame
#         self.embed_pygame()

#     def embed_pygame(self):
#         # Iniciar Pygame
#         os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())  # Vincular Pygame con el ID del frame
#         pygame.init()

#         # Configurar la ventana de Pygame dentro del frame
#         self.screen = pygame.display.set_mode((400, 400), pygame.NOFRAME )  # Ventana sin marco y con transparencia

#         # Ejemplo simple de Pygame: Dibujar en la ventana incrustada
#         self.running = True
#         self.pygame_loop()

#     def pygame_loop(self):
#         while self.running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#             # Dibujar en la ventana de Pygame
#             self.screen.fill((0, 128, 255))  # Fondo azul
#             pygame.draw.circle(self.screen, (255, 0, 0), (200, 200), 50)  # Círculo rojo

#             # Actualizar la pantalla de Pygame
#             pygame.display.update()

#             # Actualizar la ventana de Tkinter
#             self.root.update_idletasks()
#             self.root.update()

#     def start_move(self, event):
#         self.offset_x = event.x
#         self.offset_y = event.y

#     def move_window(self, event):
#         x = self.root.winfo_x() + event.x - self.offset_x
#         y = self.root.winfo_y() + event.y - self.offset_y
#         self.root.geometry(f"+{x}+{y}")

#     def close(self):
#         self.running = False  # Cierra el loop de Pygame
#         self.root.destroy()  # Cierra la ventana de Tkinter


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TransparentWindow(root)
#     root.mainloop()





# import tkinter as tk
# import pygame
# import os

# class TransparentWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.overrideredirect(True)  # Eliminar el marco de la ventana
#         self.root.geometry("600x600+100+100")  # Tamaño y posición de la ventana
#         self.root.wm_attributes("-topmost", True)  # Mantener la ventana siempre encima

#         # Crear un lienzo para dibujar (sin bordes blancos)
#         self.canvas = tk.Canvas(self.root, bg='gray', highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)  # Llenar toda la ventana

#         # Botón de cerrar
#         close_button = tk.Button(self.root, text="Cerrar", command=self.close, bg='red', fg='white')
#         close_button.place(x=10, y=10)  # Posición del botón

#         # Zona de redimensionamiento (parte inferior derecha)
#         self.resize_handle_right = tk.Label(self.root, bg='black', cursor='size_nw_se')
#         self.resize_handle_right.place(relx=1.0, rely=1.0, anchor="se", width=20, height=20)
#         self.resize_handle_right.bind("<B1-Motion>", self.resize_window_right)

#         # Zona de redimensionamiento (parte inferior izquierda)
#         self.resize_handle_left = tk.Label(self.root, bg='black', cursor='size_ne_sw')
#         self.resize_handle_left.place(relx=0.0, rely=1.0, anchor="sw", width=20, height=20)
#         self.resize_handle_left.bind("<B1-Motion>", self.resize_window_left)

#         # Configurar eventos para mover la ventana
#         self.canvas.bind("<ButtonPress-1>", self.start_move)
#         self.canvas.bind("<B1-Motion>", self.move_window)

#         # Inicializar Pygame en un Frame
#         self.pygame_frame = tk.Frame(self.root, width=400, height=400, bg='blue', highlightthickness=0)
#         self.pygame_frame.place(x=100, y=100)  # Colocar el frame en el centro

#         # Inicializar la ventana de Pygame
#         self.embed_pygame()

#     def embed_pygame(self):
#         # Iniciar Pygame
#         os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())  # Vincular Pygame con el ID del frame
#         pygame.init()

#         # Configurar la ventana de Pygame dentro del frame
#         self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(), self.pygame_frame.winfo_height()), pygame.NOFRAME)

#         # Ejemplo simple de Pygame: Dibujar en la ventana incrustada
#         self.running = True
#         self.pygame_loop()

#     def pygame_loop(self):
#         while self.running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#             # Dibujar en la ventana de Pygame
#             self.screen.fill((0, 128, 255))  # Fondo azul
#             pygame.draw.circle(self.screen, (255, 0, 0), (self.pygame_frame.winfo_width() // 2, self.pygame_frame.winfo_height() // 2), 50)  # Círculo rojo

#             # Actualizar la pantalla de Pygame
#             pygame.display.update()

#             # Actualizar la ventana de Tkinter
#             self.root.update_idletasks()
#             self.root.update()

#     def start_move(self, event):
#         self.offset_x = event.x
#         self.offset_y = event.y

#     def move_window(self, event):
#         x = self.root.winfo_x() + event.x - self.offset_x
#         y = self.root.winfo_y() + event.y - self.offset_y
#         self.root.geometry(f"+{x}+{y}")

#     def resize_window_right(self, event):
#         # Redimensionar desde la parte derecha
#         new_width = event.x_root - self.root.winfo_x()
#         new_height = event.y_root - self.root.winfo_y()

#         if new_width >= 200 and new_height >= 200:  # Tamaño mínimo
#             self.root.geometry(f"{new_width}x{new_height}")

#         # Ajustar el tamaño del frame de Pygame
#         self.pygame_frame.config(width=new_width - 100, height=new_height - 100)
#         self.pygame_frame.place(x=50, y=50)  # Centrar el frame de Pygame

#         # Redimensionar la ventana de Pygame
#         self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(), self.pygame_frame.winfo_height()), pygame.NOFRAME)

#     def resize_window_left(self, event):
#         # Redimensionar desde la parte izquierda sin desplazar el borde derecho
#         new_width = self.root.winfo_width() - (event.x_root - self.root.winfo_x())
#         new_height = event.y_root - self.root.winfo_y()

#         if new_width >= 200 and new_height >= 200:  # Tamaño mínimo
#             new_x = event.x_root  # Calcular la nueva posición 'x' de la ventana
#             self.root.geometry(f"{new_width}x{new_height}+{new_x}+{self.root.winfo_y()}")

#         # Ajustar el tamaño del frame de Pygame
#         self.pygame_frame.config(width=new_width - 100, height=new_height - 100)
#         self.pygame_frame.place(x=50, y=50)  # Centrar el frame de Pygame

#         # Redimensionar la ventana de Pygame
#         self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(), self.pygame_frame.winfo_height()), pygame.NOFRAME)

#     def close(self):
#         self.running = False  # Cierra el loop de Pygame
#         self.root.destroy()  # Cierra la ventana de Tkinter


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TransparentWindow(root)
#     root.mainloop()





