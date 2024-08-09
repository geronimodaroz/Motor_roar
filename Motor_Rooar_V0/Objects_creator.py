
from typing import Literal
from Folder_classes.windows import WindowBase

class ObjectsCreator(WindowBase):

    def __init__(self,event_dict,screen,x:int,y:int,w:int,h:int,curtain_w:int,curtain_h:int,scroll_bar: Literal[0, 1, -1] = 0):
        
        super().__init__(event_dict, screen, x, y, w, h, curtain_w, curtain_h, scroll_bar)

        from Folder_classes.box_text import BoxText
        self.box_text = BoxText(event_dict,self.view_surface,20,20,50,20,text="hola")

        #self.load_objects(self.box_text)

        super().load_objects(self.box_text)

        

    def collision_detector(self, event_dict):
        super().collision_detector(event_dict)

        # if event_dict["EditableObjects"]["clickable"][self.depth_number] == self.edit:

        #     x = event_dict["Mouse"]["MousePosition"][0] - self.rect.x 
        #     y = event_dict["Mouse"]["MousePosition"][1] - self.rect.y
        #     event_dict["Mouse"]["MousePosition"] = (x,y)

        #     if self.box_text.rect.collidepoint(x,y): # edit

        #         event_dict["EditableObjects"]["clickable"].append(self.box_text.edit)



    def edit(self, event_dict):
        super().edit(event_dict)

        # ejecuto objetos de lista selected
        # ----------------------------------------------------------------------------
        clickable_list = len(event_dict["EditableObjects"]["clickable"])-1 >= self.depth_number+1 
        selected_list = len(event_dict["EditableObjects"]["selected"])-1 >= self.depth_number+1 
        
        if selected_list:
            event_dict["EditableObjects"]["selected"][self.depth_number+1](event_dict)
        elif clickable_list:
            event_dict["EditableObjects"]["clickable"][self.depth_number+1](event_dict)

    

    
    def draw(self, event_dict):
        super().draw(event_dict)

        self.box_text.draw(event_dict)
        
        # object_creator_window
        #objects_creator_window = WindowBase(event_dict,screen,25,80,300,450,500,500,1)