
from typing import Literal
from objects.windows import WindowBase

class ObjectsCreator(WindowBase):
    """la ventana encargada de crear los objectos para el proyecto"""
    def __init__(self,event_dict,screen,x:int,y:int,w:int,h:int,curtain_w:int,curtain_h:int,scroll_bar: Literal[0, 1, -1] = 0):
        super().__init__(event_dict, screen, x, y, w, h, curtain_w, curtain_h, scroll_bar)

        # ACA QUE DEPTH NUMBER RECIBE BOX TEXT!!!
        event_dict["depth_number"]+=1

        from objects.box_text import BoxText
        self.box_text = BoxText(event_dict,self.view_surface,20,150,200,20,text="Proyecto_01")

        self.objects_list.append(self.box_text)
        #self.load_objects(self.box_text)
        #super().load_objects(self.box_text)

        event_dict["depth_number"]-=1

    def rects_updates(self, presurface, x=0, y=0, w=0, h=0, force=False):
        super().rects_updates(presurface, x, y, w, h, force)

        if self.objects_list:
            self.box_text.rects_updates( self.view_surface, force = True)

    def edit(self, event_dict,code = None):
        super().edit(event_dict,code)

        
        # mouse x,y con respecto a view_rect
        x = event_dict["Mouse"]["Position"][0] - self.view_rect.x 
        y = event_dict["Mouse"]["Position"][1] - self.view_rect.y
        save_x_y = event_dict["Mouse"]["Position"]
        event_dict["Mouse"]["Position"] = (x,y)

        # ejecuto objetos de lista selected
        #ESTO ESTA MAL!! -- por?
        # ----------------------------------------------------------------------------
        if code == "clickable":
            exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= self.depth_number+1 
            if exists_next_clickable_list:
                event_dict["EditableObjects"]["clickable"][self.depth_number+1](event_dict, code ) 

        if code == "selected":
            
            exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number+1 
            if exists_next_selected_list:
                event_dict["EditableObjects"]["selected"][self.depth_number+1](event_dict, code )
        # ----------------------------------------------------------------------------

        event_dict["Mouse"]["Position"] = save_x_y

    def draw(self, event_dict):
        super().draw(event_dict)

        if self.objects_list:
            for obj in self.objects_list:
                obj.draw(event_dict)
        #self.box_text.draw(event_dict)
        
        # object_creator_window
        #objects_creator_window = WindowBase(event_dict,screen,25,80,300,450,500,500,1)