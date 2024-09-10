import win32api
import win32con
import win32gui
import ctypes

def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    elif msg == win32con.WM_PAINT:
        # Aquí se dibuja el fondo de la ventana
        hdc, ps = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        hbrush = win32gui.CreateSolidBrush(0x0000FF)  # Azul
        win32gui.FillRect(hdc, rect, hbrush)
        win32gui.DeleteObject(hbrush)
        win32gui.EndPaint(hwnd, ps)
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def create_window():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = wnd_proc
    wc.lpszClassName = 'MyWindowClass'
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, 'My Window', win32con.WS_OVERLAPPEDWINDOW,
                                 win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                 800, 600, 0, 0, wc.hInstance, None)

    # Mostrar la ventana
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hwnd)

    win32gui.PumpMessages()

if __name__ == "__main__":
    create_window()
