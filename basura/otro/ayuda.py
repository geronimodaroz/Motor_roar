import pygame as pg

# Inicializar Pygame
pg.init()

# Crear una fuente
font = pg.font.Font(None, 36)

# Texto de ejemplo
text = "Prueba de textoiasfbiaushiaushdauishdaisuhdashud9asdh9asha89sgd89wbfijdshfisdfsd"

# Calcular el ancho sumando los anchos de los caracteres individuales
prueba_w = sum(font.size(char)[0] for char in text)

# Renderizar el texto completo y obtener el ancho de la superficie
prueba_w_sup_text = font.render(text, True, (0, 0, 0))

# Mostrar los anchos calculados
print(f"Ancho calculado: {prueba_w}")
print(f"Ancho renderizado: {prueba_w_sup_text.get_width()}")
