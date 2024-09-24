import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPalette

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.pressing = False

        # Layout y botones de la barra de título
        layout = QHBoxLayout()
        self.title_label = QLabel("Ventana con Tema Oscuro", self)
        self.title_label.setStyleSheet("color: white; font-size: 16px;")

        # Botón de minimizar
        btn_minimize = QPushButton("-", self)
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.setStyleSheet("background-color: gray; color: white; border: none;")
        btn_minimize.clicked.connect(self.parent().showMinimized)  # Conectar al método de la ventana principal

        # Botón de cerrar
        btn_close = QPushButton("x", self)
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("background-color: red; color: white; border: none;")
        btn_close.clicked.connect(self.parent().close)  # Conectar al método de la ventana principal

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)
        layout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.position().toPoint()  # Reemplaza event.pos() con event.position()
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            # Reemplaza event.pos() con event.position()
            self.window().move(self.window().pos() + event.position().toPoint() - self.start)

    def mouseReleaseEvent(self, event):
        self.pressing = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowFlags(Qt.FramelessWindowHint)  # Eliminar la barra de título nativa
        self.setFixedSize(800, 600)

        # Crear un tema oscuro para la ventana
        self.set_dark_theme()

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Agregar la barra de título personalizada
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Contenido principal
        content = QLabel("Aquí va el contenido de la ventana", self)
        content.setStyleSheet("color: white; font-size: 18px;")
        main_layout.addWidget(content)
        main_layout.addStretch()

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_dark_theme(self):
        """Aplicar un tema oscuro a la ventana"""
        dark_palette = QPalette()

        # Colores personalizados para el tema oscuro
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(dark_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())










# import tkinter as tk

# def create_transparent_overlay():
#     # Crear una ventana sin bordes
#     overlay = tk.Tk()
#     overlay.overrideredirect(True)  # Eliminar bordes y barra de título
#     overlay.geometry("400x400+100+100")  # Tamaño y posición de la ventana
#     overlay.attributes('-alpha', 0.7)  # 70% de opacidad

#     # Eliminar el color de fondo de la ventana
#     overlay.config(bg="green")

#     # Crear un lienzo sin bordes blancos
#     canvas = tk.Canvas(overlay, width=400, height=400, highlightthickness=0, bg="green")
#     canvas.pack(fill="both", expand=True)

#     # Dibujar un rectángulo verde sin bordes visibles
#     canvas.create_rectangle(0, 0, 400, 400, fill="green", outline="")

#     # Actualizar la ventana para que se dibuje correctamente
#     overlay.update()

#     # Destruir la ventana después de 2 segundos
#     overlay.destroy()
# # Llamar a la función para crear la ventana overlay
# create_transparent_overlay()










# import tkinter as tk

# class OverlayApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Ventana Principal")
#         self.root.geometry("400x400")

#         # Botón para mostrar el overlay
#         show_overlay_btn = tk.Button(self.root, text="Mostrar Overlay", command=self.show_overlay)
#         show_overlay_btn.pack(pady=20)

#         # Botón para cerrar la ventana
#         close_btn = tk.Button(self.root, text="Cerrar", command=self.root.quit)
#         close_btn.pack(pady=20)

#         self.overlay = None

#     def show_overlay(self):
#         if self.overlay is None:
#             # Crear una nueva ventana Toplevel
#             self.overlay = tk.Toplevel(self.root)
#             self.overlay.title("Overlay")
#             self.overlay.geometry("400x400+100+100")  # Tamaño y posición
#             self.overlay.overrideredirect(True)  # Sin bordes
#             self.overlay.attributes("-alpha", 0.5)  # Transparente
#             self.overlay.configure(bg='green')  # Color de fondo del overlay

#             # Botón para cerrar el overlay
#             close_overlay_btn = tk.Button(self.overlay, text="Cerrar Overlay", command=self.hide_overlay)
#             close_overlay_btn.pack(pady=20)

#     def hide_overlay(self):
#         if self.overlay:
#             self.overlay.destroy()
#             self.overlay = None

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = OverlayApp(root)
#     root.mainloop()


# import pygame
# import pygetwindow as gw
# import os
# import tkinter as tk

# class BorderOnlyWindow:
#     def __init__(self, root, width, height):
#         self.root = root
#         self.root.geometry(f"{width}x{height}+100+100")  # Tamaño y posición de la ventana
#         self.root.overrideredirect(True)  # Eliminar la barra superior nativa
#         self.root.attributes('-transparentcolor', 'black')  # Hacer que el color negro sea transparente
#         self.root.attributes('-topmost', True)  # Mantener la ventana siempre por encima

#         # Crear el marco con los bordes blancos
#         self.border_frame = tk.Frame(self.root, bg='white', bd=5)  # Bordes blancos
#         self.border_frame.pack(fill="both", expand=True)

#         # Crear un área transparente (negra) en el centro para que no tenga contenido visible
#         self.transparent_area = tk.Frame(self.border_frame, bg='black')
#         self.transparent_area.pack(fill="both", expand=True)

#         # Bind para poder mover la ventana al arrastrarla
#         self.border_frame.bind("<ButtonPress-1>", self.start_move)
#         self.border_frame.bind("<B1-Motion>", self.move_window)

#         # Opción de cerrar la ventana con la tecla "Esc"
#         self.root.bind("<Escape>", lambda event: self.root.destroy())

#     def start_move(self, event):
#         self.offset_x = event.x
#         self.offset_y = event.y

#     def move_window(self, event):
#         x = self.root.winfo_x() + event.x - self.offset_x
#         y = self.root.winfo_y() + event.y - self.offset_y
#         self.root.geometry(f"+{x}+{y}")

# def is_window_minimized(window_title):
#     try:
#         window = gw.getWindowsWithTitle(window_title)[0]  # Obtener la ventana por su título
#         return window.isMinimized  # Devuelve True si la ventana está minimizada
#     except IndexError:
#         return False  # La ventana no se encontró

# if __name__ == "__main__":
#     # Inicializar Pygame
#     pygame.init()
#     width, height = 600, 600
#     pygame.display.set_caption("Mi Ventana de Pygame")  # Título de la ventana de Pygame
#     screen = pygame.display.set_mode((width, height), pygame.NOFRAME)  # Tamaño de la ventana de Pygame

#     # Inicializar la ventana de tkinter
#     root = tk.Tk()
#     app = BorderOnlyWindow(root, width, height)

#     # Vincular la ventana de tkinter con la ventana de Pygame
#     os.environ['SDL_WINDOWID'] = str(root.winfo_id())  # Vincular Pygame con el ID del frame de tkinter

#     # Bucle principal de Pygame
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Rellenar con un color
#         screen.fill((0, 128, 255))  # Color de fondo azul
#         pygame.display.flip()

#         # Comprobar si la ventana de Pygame está minimizada
#         window_title = "Mi Ventana de Pygame"  # Cambia esto al título de tu ventana de Pygame
#         if is_window_minimized(window_title):
#             root.withdraw()  # Oculta la ventana de tkinter
#         else:
#             root.deiconify()  # Muestra la ventana de tkinter

#         # Sincronizar la posición de la ventana de Pygame con la de Tkinter
#         try:
#             window = gw.getWindowsWithTitle(window_title)[0]
#             x = root.winfo_x()
#             y = root.winfo_y()
#             window.moveTo(x, y)  # Ajustar la posición de la ventana de Pygame
#         except IndexError:
#             pass  # Si la ventana no se encuentra, no hacer nada

#         # Actualizar la ventana de tkinter
#         root.update()

#     root.destroy()
#     pygame.quit()









# import tkinter as tk

# class RoundedBorderWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("400x400+100+100")  # Tamaño y posición de la ventana
#         self.root.overrideredirect(True)  # Eliminar la barra superior nativa
#         self.root.attributes('-transparentcolor', 'black')  # Hacer que el color negro sea transparente

#         # Crear un canvas para dibujar los bordes redondeados
#         self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)

#         # Dibujar los bordes redondeados en el canvas
#         self.draw_rounded_rectangle(10, 10, 380, 380, 20, outline_color='white', fill_color='black')

#         # Bind para mover la ventana al arrastrarla
#         self.canvas.bind("<ButtonPress-1>", self.start_move)
#         self.canvas.bind("<B1-Motion>", self.move_window)

#         # Opción de cerrar la ventana con la tecla "Esc"
#         self.root.bind("<Escape>", lambda event: self.root.destroy())

#     def draw_rounded_rectangle(self, x1, y1, x2, y2, radius, outline_color, fill_color):
#         points = [
#             (x1 + radius, y1), (x2 - radius, y1),  # Líneas superiores
#             (x2, y1 + radius), (x2, y2 - radius),  # Líneas derecha
#             (x2 - radius, y2), (x1 + radius, y2),  # Líneas inferiores
#             (x1, y2 - radius), (x1, y1 + radius)   # Líneas izquierda
#         ]
#         self.canvas.create_polygon(points, smooth=True, fill=fill_color, outline=outline_color, width=5)

#         # Esquinas redondeadas
#         self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, style='arc', outline=outline_color, width=5)
#         self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, style='arc', outline=outline_color, width=5)
#         self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style='arc', outline=outline_color, width=5)
#         self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, style='arc', outline=outline_color, width=5)

#     def start_move(self, event):
#         self.offset_x = event.x
#         self.offset_y = event.y

#     def move_window(self, event):
#         x = self.root.winfo_x() + event.x - self.offset_x
#         y = self.root.winfo_y() + event.y - self.offset_y
#         self.root.geometry(f"+{x}+{y}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = RoundedBorderWindow(root)
#     root.mainloop()
