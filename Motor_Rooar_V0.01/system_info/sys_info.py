import sys
import pygame as pg
import ctypes
from ctypes import wintypes



# SYSINFO DEBE TENER UN BOCLU CONTINUO QUE DETECTE CAMBIOS ENEL SISTEMA INDEPENIENTEMENTE DEL BUCLE DEL PROYECTO?



# Clase para obtener y manejar la información del sistema
class SysInfo:
    """Clase que contiene información sobre el sistema:
       * Tamaño de los monitores
       * Cantidad de monitores
       * Información de la barra de tareas (posición y dimensiones)
       * Actualización automática si alguna de estas propiedades cambia
    """


    @staticmethod
    def get_monitor_count():
        """Obtiene la cantidad de monitores conectados."""
        count = ctypes.c_int(0)  # Variable para contar monitores
        # Definir el callback para la enumeración
        def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
            count.value += 1  # Incrementar el contador
            return 1  # Continuar la enumeración
        MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HMONITOR, wintypes.HDC, wintypes.LPRECT, wintypes.LPARAM)
        # Enumerar los monitores
        ctypes.windll.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
        return count.value
    



    @staticmethod
    def get_monitors_info():
        """Obtiene una lista de los monitores, sus dimenciones y areas de trabajo."""

        # Definición de MONITORINFO
        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT),
                ("dwFlags", wintypes.DWORD)
            ]

        # Función para obtener la lista de monitores conectados
        def _get_monitors_info():
            monitors = []
            def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
                mi = MONITORINFO()
                mi.cbSize = ctypes.sizeof(MONITORINFO)
                ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))
                monitors.append(mi)
                return 1  # Continuar la enumeración
            MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(wintypes.RECT), ctypes.c_int)
            ctypes.windll.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
            return monitors
        

        monitors_list = []

        # Obtener la lista de monitores
        monitors = _get_monitors_info()  # Asumimos que esta función está definida

        for i, monitor in enumerate(monitors):
            
            monitors_list.append({
                            "Number": i,  # Número del monitor
                            "Position": {
                                "X": monitor.rcMonitor.left,
                                "Y": monitor.rcMonitor.top
                                },
                            "Dimensions": { # Ancho y Alto
                                "Width": monitor.rcMonitor.right - monitor.rcMonitor.left,
                                "Height": monitor.rcMonitor.bottom - monitor.rcMonitor.top
                                },  
                            "WorkArea": { # Área de trabajo
                                "X": monitor.rcWork.left,
                                "Y": monitor.rcWork.top,
                                "Width": monitor.rcWork.right - monitor.rcWork.left,
                                "Height": monitor.rcWork.bottom - monitor.rcWork.top
                                }  
                            })
            

        return monitors_list






# Función para obtener la información de la barra de tareas
# def get_taskbar_info():
#     user32 = ctypes.windll.user32
    
#     # Obtener el rectángulo de la barra de tareas
#     rect = RECT()
#     hwnd = user32.FindWindowW("Shell_TrayWnd", None)
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))

#     screen_width = user32.GetSystemMetrics(0)  # Ancho de la pantalla
#     screen_height = user32.GetSystemMetrics(1)  # Alto de la pantalla

#     # Calcular el ancho y alto de la barra de tareas
#     taskbar_x = rect.left
#     taskbar_y = rect.top
#     taskbar_w = rect.right - rect.left
#     taskbar_h = rect.bottom - rect.top

#     # Determinar la posición de la barra de tareas
#     position = ""
#     if rect.top == 0 and taskbar_w == screen_width:  # Barra en la parte superior
#         position = "Top"
#     elif rect.bottom == screen_height and taskbar_w == screen_width:  # Barra en la parte inferior
#         position = "Bottom"
#     elif rect.left == 0 and taskbar_h == screen_height:  # Barra a la izquierda
#         position = "Left"
#     elif rect.right == screen_width and taskbar_h == screen_height:  # Barra a la derecha
#         position = "Right"
#     else:
#         position = "Unknown"

#     # Devolver la posición y tamaño de la barra de tareas
#     return {
#         "position": position,
#         "x": taskbar_x,
#         "y": taskbar_y,
#         "width": taskbar_w,
#         "height": taskbar_h
#     }


# Si la barra de tareas está en este monitor, añadir la información
# if (monitor.rcMonitor.left <= taskbar_info["x"] < monitor.rcMonitor.right) and \
#    (monitor.rcMonitor.top <= taskbar_info["y"] < monitor.rcMonitor.bottom):
#     monitor_info["taskbar"] = {
#         "Position": taskbar_info,
#         "TaskbarDimensions": (taskbar_info["width"], taskbar_info["height"])
#     }