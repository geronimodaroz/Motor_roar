import pygame as pg
import ctypes
from ctypes import wintypes


# Definir RECT y MONITORINFO para Windows
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]

    
# Función para detectar si la ventana ha cambiado de monitor
def detect_monitor_change(hwnd,monitors):


    rect = RECT()
    #hwnd = pg.display.get_wm_info()['window']
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    window_left, window_top, window_right, window_bottom = rect.left, rect.top, rect.right, rect.bottom
    
    # Comparar la posición de la ventana con cada monitor
    for monitor in monitors:
        if (window_left >= monitor.rcMonitor.left and window_right <= monitor.rcMonitor.right and
            window_top >= monitor.rcMonitor.top and window_bottom <= monitor.rcMonitor.bottom):
            return monitor.rcMonitor
    return None