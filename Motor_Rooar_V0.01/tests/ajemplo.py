import ctypes
from ctypes import wintypes

# Funciones de la API de Windows
user32 = ctypes.windll.user32

# Obtener dimensiones de la pantalla
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # Ancho y alto

# Estructura para almacenar la información del rectángulo
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]

# Obtener el rectángulo de la barra de tareas
rect = RECT()
user32.GetWindowRect(user32.FindWindowW("Shell_TrayWnd", None), ctypes.byref(rect))

# Calcular dimensiones de la barra de tareas
taskbar_w, taskbar_h = rect.right - rect.left, rect.bottom - rect.top

# Determinar la posición de la barra de tareas basándonos en las coordenadas y los bordes de la pantalla
if rect.top == 0 and taskbar_w == screen_width:  # Barra de tareas en la parte superior
    position = "Top"
elif rect.bottom == screen_height and taskbar_w == screen_width:  # Barra de tareas en la parte inferior
    position = "Bottom"
elif rect.left == 0 and taskbar_h == screen_height:  # Barra de tareas en el lado izquierdo
    position = "Left"
elif rect.right == screen_width and taskbar_h == screen_height:  # Barra de tareas en el lado derecho
    position = "Right"
else:
    position = "Could not determine the position"

# Imprimir la posición de la barra de tareas
print(f"Position of the taskbar: {position}")
