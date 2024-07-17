import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Esto deberia ser general, no solo de una carpeta en particular? 


class _MyHandler(FileSystemEventHandler):
    def on_deleted(self, event): 
        #print(f"evento: {event}")
        if event.is_directory: # si es una carpeta, retorna "nada"
            return
        print(f"Se ha eliminado el archivo: {event.src_path}") # "event.src_path" --> ruta del archivo 

#class Monitor():
def monitorear_carpeta(carpeta):

    #def start():
    event_handler = _MyHandler()
    observer = Observer() # monitorear los cambios en el sistema de archivos
    observer.schedule(event_handler, carpeta, recursive=True) # recursive=True monitores los subdirectorios
    observer.start() # comienzo a monitorear la carpeta 

    """try: # se seguira monitoreando hasta que presionemos "crlt + c"
        while True:# el observador seguira monitoreando la carpeta hasta que se produzca una excepcion "cntl + c"
            time.sleep(1) # espera un segundo antes de volver a iterarse 
    except KeyboardInterrupt: # detener observador si se presiona control + c
        observer.stop() # detiene el observador
    observer.join() # esperar a que el hilo del observador termine su ejecución ??"""

    # Ejemplo de uso
#carpeta_a_monitorear = None#"C:/Users/gerod/OneDrive/Escritorio/hola"
#monitorear_carpeta(carpeta_a_monitorear)