class Config:
    pass

config = Config()

# Establecer múltiples atributos dinámicamente
atributos = {'host': 'localhost', 'port': 8080, 'debug': True}

for clave, valor in atributos.items():
    setattr(config, clave, valor)

# Obtener y mostrar los valores de los atributos
for clave in atributos:
    valor = getattr(config, clave)
    print(f'{clave}: {valor}')
