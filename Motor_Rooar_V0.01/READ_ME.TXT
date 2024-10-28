
# ESTA VERSION FUNCIONA CON PYGAME 2.6.0 !!

ERRORES A AREGLAR:
# ----------------------------------------------------------------------------
* aveces el objeto box_text no borra el texto seleccionado, por alguna razon ! (deja de funcionar la tecla "borrar" a veces)
* se estan borrando y dibujando los elementos en cada bucle de eventos, lo cual es innecesario y consume recursos!
* los colores del proyecto no dependen en todos los objetos de "event_dict" y deberian !
* debo precionar "F5" para adaptar la ventana a los cambios en el area de trabajo del monitor, no es automatico y deberia !
* modificar el tamaño de la ventana de pygame desde sus esquinas inferiores permite achicar la ventana mas de lo debido !
* ventana escroleable (class Window): al minimizar la ventana al minimo y intentar mover la barra inferior de posicion si esta en un borde el mouse no desplaza bien la imagen o su contenido hasta despues de un momento, solo ocurre del lado derecho de la barra inferior
# ----------------------------------------------------------------------------


# Lista de pendientes:

* la variable self.is_editing en box_text (objeto) es necesaria ?

* variable para forzar loop - LISTO

* modificar engine_window en objeto e instancia separar el objeto y crear una instancia que cargue su contenido - LISTO

* configurar ventana para monitores - LISTO (aun que se puede mejorar)

* crear boton de cerrar y minimizar en la ventana del proyecto - LISTO

* ordenar variables y elementos de la ventana "EngineWindow" que deje sin terminar, ademas verificar rutas del icono, deberia tener una ruta local 