import ctypes
from ctypes import wintypes
import sys

WM_DISPLAYCHANGE = 0x007E
WM_SETTINGCHANGE = 0x001A
LRESULT = ctypes.c_long  # Define LRESULT directly using ctypes

class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", wintypes.POINT),
    ]

class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(
            LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

def create_hidden_window():
    WndProcType = ctypes.WINFUNCTYPE(
        LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

    def wnd_proc(hwnd, msg, wparam, lparam):
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        
    wnd_proc_func = WndProcType(wnd_proc)
    
    wc = WNDCLASS()
    wc.lpfnWndProc = wnd_proc_func
    wc.lpszClassName = "MonitorWatcher"
    
    if not ctypes.windll.user32.RegisterClassW(ctypes.byref(wc)):
        raise ctypes.WinError(ctypes.get_last_error())
        
    hwnd = ctypes.windll.user32.CreateWindowExW(
        0, wc.lpszClassName, None, 0, 0, 0, 0, 0, None, None, None, None)
        
    if not hwnd:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return hwnd

def message_loop():
    msg = MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        if msg.message == WM_DISPLAYCHANGE:
            print("Cambio en la configuración de monitores detectado.")
        elif msg.message == WM_SETTINGCHANGE:
            print("Cambio en la configuración del sistema detectado.")
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    hwnd = create_hidden_window()
    print("Esperando cambios en la configuración de monitores...")
    message_loop()
