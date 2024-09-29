
import sys
import pygame as pg
import ctypes
from ctypes import wintypes
from screeninfo import get_monitors


class SysInfo():

    """Contiene informacion sobre el equipo donde se ejecuta la aplicacion
        * Tamaño del monito
        * Cantidad de minitores
        * donde se ejecutara el proyecto
        * posicion de la barra de tareas y sus dimenciones
        * caracteristicas especiales de la barra de tarea (por ejemplo su ocultamiento)
        * actualizacion automatica de alguna de las funciones anteriores si cambiaran
    """

    def __init__(self):

        # Obtiene la lista de monitores (aquí debes implementar la función get_monitors())

        monitores = get_monitors()  # Asegúrate de definir esta función
        # Itera sobre los monitores y muestra sus dimensiones
        for monitor in monitores:
            print(f"Monitor: {monitor.name} - Ancho: {monitor.width}, Alto: {monitor.height}")

        # DETECTAR CANTIDAD DE MONITORES


        # Funciones de la API de Windows
        user32 = ctypes.windll.user32

        # Dimenciones de la pantalla
        #-----------------------------------------------------------------------------
        screen_width = user32.GetSystemMetrics(0)  # Ancho
        screen_height = user32.GetSystemMetrics(1)  # Alto
        #-----------------------------------------------------------------------------

        # Dimenciones y posicion de barra de tareas
        #-----------------------------------------------------------------------------
        # Estructura para almacenar la información del rectángulo
        class RECT(ctypes.Structure):
            _fields_ = [("left", wintypes.LONG),
                        ("top", wintypes.LONG),
                        ("right", wintypes.LONG),
                        ("bottom", wintypes.LONG)]
        # Obtener el rectángulo de la barra de tareas
        hwnd = user32.FindWindowW("Shell_TrayWnd", None)
        rect = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))

        # Calcula el ancho y alto de la barra de tareas
        taskbar_x = rect.left
        taskbar_y = rect.top
        taskbar_w = rect.right - rect.left
        taskbar_h = rect.bottom - rect.top

        # Determinar la posición de la barra de tareas
        position = ""
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
        #-----------------------------------------------------------------------------

    
#info = SysInfo()

#info.__init__()