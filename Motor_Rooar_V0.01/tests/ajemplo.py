import ctypes
from ctypes import wintypes

# Funciones de la API de Windows
user32 = ctypes.windll.user32

# Estructura para almacenar la información del rectángulo
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]

def get_taskbar_info():
    # Obtener el handle de la barra de tareas
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    rect = RECT()
    
    # Obtener el rectángulo de la barra de tareas
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    
    # Calcular el ancho y alto de la barra de tareas
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    
    # Obtener dimensiones de la pantalla
    screen_width = user32.GetSystemMetrics(0)  # Ancho
    screen_height = user32.GetSystemMetrics(1)  # Alto

    # Determinar la posición de la barra de tareas
    position = ""
    
    # Verificar la posición en relación a los bordes de la pantalla
    if height < 100:  # Si la altura es menor a 100, podría ser Top o Bottom
        if rect.top == 0:
            position = "Top"
        elif rect.bottom == screen_height:
            position = "Bottom"
    elif width < 100:  # Si el ancho es menor a 100, podría ser Left o Right
        if rect.left == 0:
            position = "Left"
        elif rect.right == screen_width:
            position = "Right"
    else:
        # Detectar si está anclada a la derecha o izquierda
        if rect.left > screen_width / 2:
            position = "Right"
        elif rect.right < screen_width / 2:
            position = "Left"
        else:
            position = "Could not determine the position"
    
    # Devolver la posición, dimensiones y coordenadas
    return {
        "position": position,
        "dimensions": (width, height),
        "coordinates": (rect.left, rect.top)
    }

# Llamada a la función
taskbar_info = get_taskbar_info()
print("Position of the taskbar:", taskbar_info["position"])
print("Dimensions of the taskbar:", taskbar_info["dimensions"])
print("Coordinates of the taskbar:", taskbar_info["coordinates"])
