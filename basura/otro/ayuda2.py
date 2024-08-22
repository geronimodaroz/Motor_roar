import pygame as pg

pg.init()
scancode = 22  # Código de tecla para 'a'
key_name = pg.key.name(scancode)
print(key_name)  # Salida: 'a'
pg.quit()
