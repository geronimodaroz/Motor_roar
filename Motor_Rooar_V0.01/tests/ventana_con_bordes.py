import sys
import os
import pygame
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer

class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NativeWindow)
        self.setFixedSize(400, 400)
        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        self.init_pygame()

        # Inicialización de variables para el movimiento del círculo
        self.circle_x = 200  # Posición inicial en el eje X
        self.circle_speed = 3  # Velocidad de movimiento del círculo
        self.circle_radius = 50  # Radio del círculo

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400), pygame.NOFRAME | pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_pygame(self):
        self.handle_events()

        # Limpiar la pantalla
        self.screen.fill((0, 128, 255))

        # Actualizar la posición del círculo
        self.circle_x += self.circle_speed

        # Rebotar el círculo al alcanzar los límites
        if self.circle_x + self.circle_radius > 400 or self.circle_x - self.circle_radius < 0:
            self.circle_speed = -self.circle_speed  # Cambiar dirección

        # Dibujar el círculo
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.circle_x), 200), self.circle_radius)
        pygame.display.flip()
        self.clock.tick(60)

    def closeEvent(self, event):
        self.running = False
        pygame.quit()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Eliminar la bandera de estar siempre en primer plano

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Botón de cerrar
        button_close = QPushButton("Cerrar")
        button_close.setFixedSize(80, 30)
        button_close.clicked.connect(self.close)
        button_close.setStyleSheet("background-color: red; color: white; font-size: 12px; border-radius: 5px;")

        # Botón de minimizar
        button_minimize = QPushButton("Minimizar")
        button_minimize.setFixedSize(80, 30)
        button_minimize.clicked.connect(self.showMinimized)
        button_minimize.setStyleSheet("background-color: yellow; color: black; font-size: 12px; border-radius: 5px;")

        # Añadir botones al layout
        button_layout.addWidget(button_minimize)
        button_layout.addWidget(button_close)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.pygame_widget = PygameWidget(self)
        layout.addLayout(button_layout)
        layout.addStretch()
        layout.addWidget(self.pygame_widget, alignment=Qt.AlignCenter)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer para actualizar la ventana de Pygame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pygame_widget.update_pygame)
        self.timer.start(16)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.position().toPoint() - self.offset)

    def changeEvent(self, event):
        super().changeEvent(event)
        # Asegúrate de que el evento esté siendo detectado correctamente
        if event.type() == event.Type.WindowStateChange:
            if self.isMinimized():
                self.pygame_widget.running = False  # Detener Pygame al minimizar
            elif self.isVisible():
                self.pygame_widget.running = True  # Reiniciar Pygame al restaurar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




# import tkinter as tk
# import pygame
# import os

# class TransparentWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("600x600+100+100")  # Tamaño y posición de la ventana
#         self.root.overrideredirect(True)  # Eliminar la barra superior nativa



#         # Crear el marco externo con bordes personalizados
#         self.border_frame = tk.Frame(self.root, bg='black', bd=5)  # Color del borde externo
#         #self.border_frame.place(x=50, y=50, width=500, height=500)
#         self.border_frame.pack(fill="both", expand=True)

#         # Crear la barra superior personalizada
#         self.title_bar = tk.Frame(self.border_frame, bg='black', relief='raised', bd=0)  # Barra superior de color oscuro
#         self.title_bar.pack(fill="x")

#         # Botón de cerrar en la barra superior
#         close_button = tk.Button(self.title_bar, text="Cerrar", command=self.close, bg='red', fg='white')
#         close_button.pack(side="right", padx=10, pady=2)

#         # Etiqueta para arrastrar la ventana
#         self.title_bar.bind("<ButtonPress-1>", self.start_move)
#         self.title_bar.bind("<B1-Motion>", self.move_window)
        
#         # Crear el área central de contenido
#         self.content_area = tk.Frame(self.border_frame, bg='gray')
#         self.content_area.pack(fill="both", expand=True)
        
#         # Inicializar Pygame en un Frame
#         self.pygame_frame = tk.Frame(self.content_area, width=400, height=400, bg='blue', highlightthickness=0)
#         self.pygame_frame.place(x=100, y=100)  # Colocar el frame en el centro

#         # Bind para detectar el movimiento del mouse y cambiar el cursor
#         self.border_frame.bind("<Motion>", self.change_cursor_borde)
#         self.content_area.bind("<Motion>", self.change_cursor_content_area)
#         # Capturar eventos de teclado en Tkinter
#         self.root.bind("<KeyPress>", self.on_key_press)

#         self.dis = 0
#         self.num = 1

#         # Inicializar la ventana de Pygame
#         self.embed_pygame()

#     def embed_pygame(self):
#         # Iniciar Pygame
#         os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())  # Vincular Pygame con el ID del frame
#         pygame.init()

#         # Configurar la ventana de Pygame dentro del frame
#         self.screen = pygame.display.set_mode((400, 400), pygame.NOFRAME)  # Ventana sin marco y con transparencia
        
#         # Intentar forzar el enfoque
#         pygame.event.set_grab(True)  # Forzar la captura de eventos de teclado

#         # Ejemplo simple de Pygame: Dibujar en la ventana incrustada
#         self.running = True
#         self.pygame_loop()

#     def pygame_loop(self):
#         while self.running:
#             pygame.event.set_grab(True)  # Forzar la captura de eventos de teclado
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                 if event.type == pygame.KEYDOWN:
#                     print("tecla")

#             # Dibujar en la ventana de Pygame
#             self.screen.fill((0, 128, 255))  # Fondo azul

#             self.dis += self.num

#             if self.dis > 400: self.num = -1
#             if self.dis < 0: self.num = 1


#             pygame.draw.circle(self.screen, (255, 0, 0), (self.dis, 200), 50)  # Círculo rojo

#             # Actualizar la pantalla de Pygame
#             pygame.display.update()

#             # Actualizar la ventana de Tkinter
#             self.root.update_idletasks()
#             self.root.update()

#     def on_key_press(self, event):
#         print(event.char)

#     def change_cursor_content_area(self, event):
#         self.root.config(cursor="arrow")  # Restablecer el cursor a la flecha normal

#     def change_cursor_borde(self, event):
#         x, y = event.x, event.y
#         width = self.border_frame.winfo_width()
#         height = self.border_frame.winfo_height()
#         border_width = 5  # El ancho del borde negro
        
#         # Cambiar el cursor cuando el ratón está sobre los bordes
#         if x <= border_width and y >= height - border_width:
#             self.root.config(cursor="bottom_left_corner")  # Esquina inferior izquierda
#         elif x >= width - border_width and y >= height - border_width:
#             self.root.config(cursor="bottom_right_corner")  # Esquina inferior derecha
#         elif x <= border_width:
#             self.root.config(cursor="left_side")  # Borde izquierdo
#         elif x >= width - border_width:
#             self.root.config(cursor="right_side")  # Borde derecho
#         elif y >= height - border_width:
#             self.root.config(cursor="bottom_side")  # Borde inferior
#         else:
#             self.root.config(cursor="arrow")  # Restablecer el cursor a la flecha normal

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





