
from typing import Literal
from Folder_classes.windows import WindowBase

class ObjectsCreator(WindowBase):

    def __init__(self,event_dict,screen,x:int,y:int,w:int,h:int,curtain_w:int,curtain_h:int,scroll_bar: Literal[0, 1, -1] = 0):
        
        super().__init__(event_dict, screen, x, y, w, h, curtain_w, curtain_h, scroll_bar)

        from Folder_classes.box_text import BoxText
        self.box_text = BoxText(event_dict,self.view_surface,20,100,50,20,text="hola")

        #self.load_objects(self.box_text)

        super().load_objects(self.box_text)




    def edit(self, event_dict,code = None):
        super().edit(event_dict,code)
        
        # mouse x,y con respecto a view_rect
        x = event_dict["Mouse"]["MousePosition"][0] - self.view_rect.x 
        y = event_dict["Mouse"]["MousePosition"][1] - self.view_rect.y
        save_x_y = event_dict["Mouse"]["MousePosition"]
        event_dict["Mouse"]["MousePosition"] = (x,y)

        # ejecuto objetos de lista selected
        # ----------------------------------------------------------------------------
        exists_next_clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= self.depth_number+1 
        if exists_next_clickable_list:
            event_dict["EditableObjects"]["clickable"][self.depth_number+1](event_dict, code = "clickable") 

        exists_next_selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number+1 
        if exists_next_selected_list:
            event_dict["EditableObjects"]["selected"][self.depth_number+1](event_dict, code = "selected")
        # ----------------------------------------------------------------------------

        event_dict["Mouse"]["MousePosition"] = save_x_y

    
    def draw(self, event_dict):
        super().draw(event_dict)

        if self.objects_list:
            for obj in self.objects_list:
                obj.draw(event_dict)
        #self.box_text.draw(event_dict)
        
        # object_creator_window
        #objects_creator_window = WindowBase(event_dict,screen,25,80,300,450,500,500,1)