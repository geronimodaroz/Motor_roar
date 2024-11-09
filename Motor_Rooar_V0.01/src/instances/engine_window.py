from src.objects.windows import EngineWindow
import pygame as pg


class EngineWindowInstance(EngineWindow):
    """Crea una instancia del objeto "EngineWindow" y coloca objetos dentro"""
    def __init__(self, event_dict, presurface):
        super().__init__(event_dict, presurface)

        event_dict["depth_number"]+=1

        # Crear ventanas y objetos
        from src.objects.windows import Window
        window = Window(event_dict, self.view_surface, 350, 80, 300, 450, 1024, 683, 1)
        self.objects_list.append(window)  # Agregar el objeto window a la lista

        from src.instances.objects_creator import ObjectsCreator
        objects_creator_window = ObjectsCreator(event_dict, self.view_surface, 20, 80, 300, 450, 500, 500, 1)
        self.objects_list.append(objects_creator_window)  # Agregar el objeto creator window a la lista

        event_dict["depth_number"]-=1

    def rects_updates(self, presurface, w=0, h=0, resize=False, force=False):
        super().rects_updates(presurface, w, h, resize, force)

        # recreo los rects de los objetos dentro de engine window
        # ----------------------------------------------------------------------------
        if self.objects_list:
            for obj in self.objects_list:
                obj.rects_updates(self.view_surface, force = True)
        # ----------------------------------------------------------------------------

    def edit(self, event_dict, code=None):
        super().edit(event_dict, code)

        # Delate objects from object_list
        if event_dict["Delate_List"]:
            for obj in event_dict["Delate_List"]:
                if obj in self.objects_list:
                    self.objects_list.remove(obj)
            event_dict["Delate_List"].clear()

    def draw(self, event_dict):
        super().draw(event_dict)

        #pg.draw.rect(self.presurface,self.color,self.view_rect) # dibujo el fondo gris

        if self.objects_list:
            for obj in self.objects_list:
                obj.draw(event_dict)