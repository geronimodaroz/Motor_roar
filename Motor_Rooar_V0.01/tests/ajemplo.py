import cv2
import numpy as np

# Crear una ventana de OpenCV a pantalla completa
cv2.namedWindow("Pantalla", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pantalla", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Bucle para mostrar gráficos
while True:
    # Crear una imagen en negro
    image = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Dibujar gráficos
    cv2.line(image, (100, 100), (200, 200), (255, 0, 0), 5)  # Línea azul
    cv2.circle(image, (300, 300), 50, (0, 255, 0), -1)       # Círculo verde

    # Mostrar la imagen
    cv2.imshow("Pantalla", image)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar ventanas
cv2.destroyAllWindows()


