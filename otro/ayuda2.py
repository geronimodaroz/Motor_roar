import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"Se ha eliminado el archivo: {event.src_path}")

def monitorear_carpeta(carpeta):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, carpeta, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Ejemplo de uso
carpeta_a_monitorear = "C:/Users/gerod/OneDrive/Escritorio/hola"
monitorear_carpeta(carpeta_a_monitorear)
