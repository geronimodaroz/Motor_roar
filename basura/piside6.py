import sys
import pygame
from PySide6 import QtWidgets, QtCore

# Clase personalizada para la ventana principal de PySide6
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Pygame con PySide6")
        self.setGeometry(100, 100, 800, 600)

        # Crear un layout y un botón
        self.layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton("Cerrar")
        self.button.clicked.connect(self.close_app)

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Configurar la superficie Pygame en un área de PySide
        self.pygame_widget = PygameWidget(self)
        self.layout.addWidget(self.pygame_widget)

    def close_app(self):
        self.close()

# Widget que incrusta Pygame en PySide
class PygameWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 400)

        # Inicializar Pygame
        pygame.init()

        # Crear un temporizador de actualización
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(16)  # Aproximadamente 60 FPS

        # Obtener el identificador de la ventana Qt para integrar Pygame
        self.screen = pygame.display.set_mode((800, 400), pygame.NOFRAME)
        
    def update_pygame(self):
        # Dibujar en Pygame (en este caso, solo un fondo azul y un círculo rojo)
        self.screen.fill((0, 128, 255))  # Fondo azul
        pygame.draw.circle(self.screen, (255, 0, 0), (400, 200), 50)  # Círculo rojo
        pygame.display.update()

    def closeEvent(self, event):
        pygame.quit()

# Función principal
def main():
    app = QtWidgets.QApplication(sys.argv)

    # Crear la ventana principal
    window = MainWindow()
    window.show()

    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
