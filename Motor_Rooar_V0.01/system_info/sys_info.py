import sys
import pygame as pg
import ctypes
from ctypes import wintypes




# Clase para obtener y manejar la información del sistema
class SysInfo:
    """Clase que contiene información sobre el sistema:
       * Tamaño de los monitores
       * Cantidad de monitores
       * Información de la barra de tareas (posición y dimensiones)
       * Actualización automática si alguna de estas propiedades cambia
    """

    # sys_info_dict = {
    #             "Monitors": {
    #                 "Numbers": None,  # Número total de monitores
    #                 "Info": [],  # Lista para almacenar la información de cada monitor
    #                 "WindowInMonitor": None
    #             }
    #         }

    @staticmethod
    def get_system_info():
        """Método estático para obtener la información del sistema sin crear una instancia."""

        # Definir RECT y MONITORINFO para Windows
        class RECT(ctypes.Structure):
            _fields_ = [("left", wintypes.LONG),
                        ("top", wintypes.LONG),
                        ("right", wintypes.LONG),
                        ("bottom", wintypes.LONG)]

        class MONITORINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD),
                        ("rcMonitor", RECT),
                        ("rcWork", RECT),
                        ("dwFlags", wintypes.DWORD)]

        # Función para obtener la lista de monitores conectados
        def _get_monitors_info():
            monitors = []
            def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
                mi = MONITORINFO()
                mi.cbSize = ctypes.sizeof(MONITORINFO)
                ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))
                monitors.append(mi)
                return 1  # Continuar la enumeración
            MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(RECT), ctypes.c_int)
            ctypes.windll.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
            return monitors
        


        # sys_info_dict = {
        #         "Monitors": {
        #             "Numbers": 0,  # Número total de monitores
        #             "Info": []  # Lista para almacenar la información de cada monitor
        #         }
        # }

        monitors_list = []

        # Obtener la lista de monitores
        monitors = _get_monitors_info()  # Asumimos que esta función está definida

        # Rellenar el diccionario con la información de los monitores
        #sys_info_dict["Monitors"]["Numbers"] = len(monitors)

        for i, monitor in enumerate(monitors):
            monitor_info = {
                            "Number": i+1,  # Número del monitor
                            "Position": {
                                "left": monitor.rcMonitor.left,
                                "top": monitor.rcMonitor.top},
                            "Dimensions": (monitor.rcMonitor.right - monitor.rcMonitor.left,
                                        monitor.rcMonitor.bottom - monitor.rcMonitor.top),  # Ancho y Alto
                            "WorkArea": (monitor.rcWork.right - monitor.rcWork.left,
                                        monitor.rcWork.bottom - monitor.rcWork.top)  # Área de trabajo
                            }

            # Añadir la información del monitor al diccionario
            #sys_info_dict["Monitors"]["Info"].append(monitor_info)
            monitors_list.append(monitor_info)

        return monitors_list#sys_info_dict


# Crear instancia de SysInfo
#info = SysInfo()





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