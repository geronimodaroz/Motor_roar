import tkinter as tk

def show_overlay():
    overlay = tk.Toplevel(root)  # Crear una nueva ventana
    overlay.title("Overlay")
    overlay.geometry("200x100")
    overlay.attributes('-topmost', True)  # Mantenerlo encima
    overlay.overrideredirect(True)  # Quitar bordes
    overlay_label = tk.Label(overlay, text="Este es un overlay")
    overlay_label.pack(pady=20)
    overlay.bind("<Button-1>", lambda e: overlay.destroy())  # Cerrar al hacer clic

# Crear ventana principal
root = tk.Tk()
root.geometry("400x300")

button = tk.Button(root, text="Mostrar Overlay", command=show_overlay)
button.pack(pady=20)

root.mainloop()
