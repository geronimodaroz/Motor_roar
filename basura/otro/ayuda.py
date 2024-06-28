import os
import shutil
import uuid

def copiar_archivo_con_nombre_unico(archivo_origen, carpeta_destino):
    nombre_archivo = os.path.basename(archivo_origen)
    nombre_base, extension = os.path.splitext(nombre_archivo)
    
    # Generar un sufijo único para el nombre del archivo
    sufijo_unico = uuid.uuid4().hex[:6]  # Por ejemplo, se usan los primeros 6 caracteres del identificador único
    
    # Construir el nombre del archivo de destino único
    nuevo_nombre_archivo = f"{nombre_base}_{sufijo_unico}{extension}"
    ruta_archivo_destino = os.path.join(carpeta_destino, nuevo_nombre_archivo)
    
    shutil.copy2(archivo_origen, ruta_archivo_destino)
    print(f"El archivo {nombre_archivo} ha sido copiado a la carpeta {carpeta_destino} como {nuevo_nombre_archivo}.")

# Ejemplo de uso
archivo_origen = "C:/Users/gerod/OneDrive/Escritorio/hola/texto.TXT"
carpeta_destino = "C:/Users/gerod/OneDrive/Escritorio/hola/2"

copiar_archivo_con_nombre_unico(archivo_origen, carpeta_destino)
