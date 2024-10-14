import ctypes
from ctypes import wintypes

# Definimos las constantes necesarias
WM_DISPLAYCHANGE = 0x007E  # Mensaje cuando cambia la configuración de pantalla
WM_DESTROY = 0x0002         # Mensaje para cerrar la ventana

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD)
    ]

def get_monitors_info():
    """Obtiene la información actual de los monitores."""
    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        mi = MONITORINFO(cbSize=ctypes.sizeof(MONITORINFO))
        ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))
        monitors.append({
            "MonitorRect": (mi.rcMonitor.left, mi.rcMonitor.top, 
                            mi.rcMonitor.right, mi.rcMonitor.bottom),
            "WorkArea": (mi.rcWork.left, mi.rcWork.top, 
                         mi.rcWork.right, mi.rcWork.bottom)
        })
        return 1  # Continuar la enumeración

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_int, ctypes.c_int, 
        ctypes.POINTER(wintypes.RECT), ctypes.c_int
    )
    ctypes.windll.user32.EnumDisplayMonitors(
        None, None, MonitorEnumProc(callback), 0
    )
    return monitors

# Almacenar la configuración inicial de los monitores
previous_monitors = get_monitors_info()

def detect_changes():
    """Detecta cambios en la configuración de los monitores."""
    global previous_monitors
    new_monitors = get_monitors_info()

    if new_monitors != previous_monitors:
        print("¡Cambio detectado en la configuración de monitores!")
        print("Configuración anterior:", previous_monitors)
        print("Configuración nueva:", new_monitors)
        previous_monitors = new_monitors  # Actualizar la referencia

def win_proc(hwnd, msg, wparam, lparam):
    """Función que maneja los mensajes del sistema."""
    if msg == WM_DISPLAYCHANGE:
        detect_changes()  # Detectar cambios al recibir el evento
    elif msg == WM_DESTROY:
        ctypes.windll.user32.PostQuitMessage(0)
    return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

class WNDCLASS(ctypes.Structure):
    """Clase para definir la ventana oculta."""
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", wintypes.WNDPROC),
        ("cbClsExtra", wintypes.INT),
        ("cbWndExtra", wintypes.INT),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

def create_hidden_window():
    """Crea una ventana oculta para recibir eventos."""
    wc = WNDCLASS()
    WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
    wc.lpfnWndProc = WNDPROC(win_proc)
    wc.lpszClassName = "HiddenWindowClass"
    wc.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)

    class_atom = ctypes.windll.user32.RegisterClassW(ctypes.byref(wc))
    if not class_atom:
        raise ctypes.WinError()

    hwnd = ctypes.windll.user32.CreateWindowExW(
        0, wc.lpszClassName, "Hidden Window", 0,
        0, 0, 0, 0, 0, 0, wc.hInstance, None
    )
    if not hwnd:
        raise ctypes.WinError()
    return hwnd

def message_loop():
    """Bucle de mensajes para mantener la ventana activa."""
    msg = wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    print("Escuchando cambios en la configuración de monitores...")
    hwnd = create_hidden_window()
    message_loop()
