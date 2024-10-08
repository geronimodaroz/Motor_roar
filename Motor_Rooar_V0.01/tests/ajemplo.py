import pygame as pg
import ctypes
from ctypes import wintypes

# Inicializar Pygame
pg.init()

# Configurar la ventana de Pygame
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)

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

# Función para obtener la posición de la ventana en Windows
def get_window_position(hwnd):
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom

# Función para obtener la lista de monitores conectados
def get_monitors():
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

# Función para detectar si la ventana ha cambiado de monitor
def detect_monitor_change(hwnd, monitors):
    window_left, window_top, window_right, window_bottom = get_window_position(hwnd)
    
    # Comparar la posición de la ventana con cada monitor
    for monitor in monitors:
        if (window_left >= monitor.rcMonitor.left and window_right <= monitor.rcMonitor.right and
            window_top >= monitor.rcMonitor.top and window_bottom <= monitor.rcMonitor.bottom):
            return monitor.rcMonitor
    return None

# Obtener el manejador de la ventana de Pygame
window_handle = pg.display.get_wm_info()['window']

# Obtener los monitores conectados
monitors = get_monitors()

# Bucle principal de Pygame
running = True
current_monitor = None

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        # Detectar si la ventana ha cambiado de monitor
        
        new_monitor = detect_monitor_change(window_handle, monitors)

        if new_monitor and new_monitor != current_monitor:
            current_monitor = new_monitor
            print(f"Ventana movida al monitor: {new_monitor.left}, {new_monitor.top}")

    pg.display.flip()

pg.quit()
