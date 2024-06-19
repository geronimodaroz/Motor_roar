import sys
import pygame as pg



class Reposition:

    def __init__(self):
        pass

    def reposition_y(self,obj_father,obj_child,repo_x = 0,repo_y = 0,repo_w = 0,repo_h = 0):

        # Reposicion en Y
        #----------------------------------------------------------------------------------
        # ! PARA ESTA CLASE LAS VARIABLES:
        # save_rect_y
        # save_rect_height 
        # top_y 
        # down_y
        # SON NECESARIAS EN EL OBJ_CHILD !!

        obj_child.save_rect_y += repo_y # guardamos posiscion de y

        s_y = obj_child.save_rect_y # la posicion original del obj hijo en y
        s_h = obj_child.save_rect_height # el h original del objeto hijo

        fathes_h = obj_father.rect.height
        
        # condiciones
        hit_top = s_y < 0 # si colisiono arriba con self.rect
        hit_down = s_y + s_h > fathes_h # si colisiono abajo con fathes_h
        # MODIFICO "obj_child.rect.y" Y "obj_child.rect.height" SEGUN SU COLISION ARRIBA O ABAJO
        #----------------------------------------------------------------------------------
        if hit_top and not(hit_down): # si colisiono arriba y no abajo
            obj_child.rect.y = 0
            if s_y + s_h > 0:
                obj_child.rect.height = s_y + s_h
            else:
                obj_child.rect.height = 0
        elif hit_down and not(hit_top): # si colisiono abajo y no arriba
            if s_y < fathes_h:
                obj_child.rect.height = fathes_h - s_y
            else:
                obj_child.rect.height = 0
            obj_child.rect.y = fathes_h - obj_child.rect.height
        elif hit_down and hit_top: # si colisiono arriba y abajo (esto no va a pasar?)
            obj_child.rect.y = 0
            obj_child.rect.height = fathes_h
        else: # si no colisiono
            obj_child.rect.y = s_y
            obj_child.rect.height = s_h
        #----------------------------------------------------------------------------------


        #----------------------------------------------------------------------------------
        # si colisiono arriba modifico posicion relativa de obj_child.rect.y (s_y)
        # top_y: posicion relativa de obj_child.rect.y
        # down_y: posicion relativa de obj_child.rect.y + obj_child.rect.height
        if hit_top:
            obj_child.top_y = s_y
            obj_child.down_y = s_y + s_h 
        else:
            obj_child.top_y = 0
            obj_child.down_y = s_h 
        #----------------------------------------------------------------------------------

        # reposiciono la superficie del obj_child
        obj_child.surface = obj_father.surface.subsurface(obj_child.rect)

        # reposiscion personal(de cada elemento unico) de objeto hijo
        obj_child.reposition()