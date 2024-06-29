import sys
import pygame as pg
from tkinter import filedialog, Tk
import shutil # para copiar archivos en otra carpeta (aparentemente)
import os # crear carpetas, archivos ect..
import pickle # guardar o cargar archivos
import uuid # Generar un sufijo único

from Folder_classes.font import Font # fuentes (string a surface)

from Folder_box_sprite_loader.box_text import BoxText # importo box text



class BoxSpriteLoader:

    def __init__(self,event_dict,surface,x,y,w,h,color):

        # prufundidad del objeto +1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]+=1
        self.depth_number = event_dict["depth_number"]
        # ----------------------------------------------------------------------------

        self.preSurface = surface # superficie sobre la que se dibuja boxSpriteLoader

        # box_sprite_loader
        #---------------------------------------------------------------------------------
        self.rect = pg.Rect(x,y,w,h) # rect de boxSpriteLoader
        self.surface = surface.subsurface(self.rect) # superficie de boxSpriteLoader
        self.color = color # color de fondo de boxSpriteLoader
        #---------------------------------------------------------------------------------

        self.gridx = self.rect.width/3 # tamaño de los cuadros de imagenes en x
        self.gridy = 120   # tamaño de los cuadros de imagenes en y

        self.countx = 0 # cuenta la posicion x desde 0
        self.county = 0 # cuenta la posicion y desde 0

        self.images = [] # guarda una lista [image_surface ,rect , rect.y, name], dentro de self.images

        self.image_select = [] # imagenes seleccionadas
        self.save_image_select = None # guarda posicion de la primer imagen seleccionada 

        # variables de posicion y
        # --------------------------------------------------------------------------
        self.scroll_y = 0 # distancia de scroll dentro de box_sprite_loader
        # --------------------------------------------------------------------------
        # agregamos add "+" a la lista "self.save_images_rect_y"
        add_rect = pg.Rect(0,0,self.gridx,self.gridy)
        self.images.append(["No image", add_rect, add_rect.y,"No name","No Box_text"])
        
        # VARIABLES DE REPOSICION
        # --------------------------------------------------------------------------
        self.save_rect_y = self.rect.y # guardamos posicion y de self.rect
        self.save_rect_height = self.rect.height # guardamos height de self.rect
        # posicion en y de box_sprite_loader arriba y abajo
        self.top_y = 0
        self.down_y = self.rect.height
        # --------------------------------------------------------------------------

        # crea carpeta Images 
        # --------------------------------------------------------------------------
        os.chdir(event_dict["GameFolderpPath"]) # nos mueve a la hubicacion de la ruta
        if not(os.path.exists("Images")): # si no existe carpeta "Images"
            os.mkdir("Images") # crea carpetas "Images"
        self.folder_images_path = os.path.join(event_dict["GameFolderpPath"],"Images") # ubicacion a Images
        # path al motor del juego
        self.motor_game_folder_path = event_dict["MotorGameFolderpPath"] 

        self.load_images(event_dict) # carga archivo pickle de imagenes
        # --------------------------------------------------------------------------

        #self.save_text_edit = "" # para guardar el texto origonal antes de ser editado
        #self.box_text_is_edit = None


        # prufundidad del objeto -1
        # ----------------------------------------------------------------------------
        event_dict["depth_number"]-=1
        # ----------------------------------------------------------------------------





    def load_images(self,event_dict):
        # CARGAR ARCHIVO "PICKLE" !!
        os.chdir(self.folder_images_path) # nos mueve a la hubicacion de la ruta
        self.images.clear() # limpio lista images
        # Abre el archivo pickle 
        # --------------------------------------------------------------------------
        try:
            with open('images_name_list.pickle', 'rb') as archivo:
                # Carga los datos del archivo pickle
                image_names = pickle.load(archivo)
        except:
            print("no hay archivo pickle")
            image_names = []
        # --------------------------------------------------------------------------
        
        # reposiciono imagenes
        # --------------------------------------------------------------------------
        self.countx = 0 # cuenta la posicion x desde 0
        self.county = 0 # cuenta la posicion y desde 0

        for image_name in image_names:
            try:
                image_surface = pg.image.load(image_name) # cargo imagen
            except:
                #SI NO SE ENCUENTRA LA IMAGEN EN LA CARPETA "IMAGES" LA CAMBIAMOS POR "image_not found.jpg"
                not_found_image_path = os.path.join(self.motor_game_folder_path,"Folder_images/Image_not_found.jpeg") 
                shutil.copy(not_found_image_path,self.folder_images_path) # Copiar el archivo a la carpeta destino
                new_imagen_path = os.path.join(self.folder_images_path,"Image_not_found.jpeg")
                os.rename(new_imagen_path,image_name) # renombramos la imagen
                image_surface = pg.image.load(image_name)
            image_surface = pg.transform.scale(image_surface,(self.gridx,self.gridx))

            # rect images
            x = self.gridx*self.countx
            y = self.gridy*self.county
            w = self.gridx
            h = self.gridy
            image_rect = pg.Rect(x,y,w,h)

            save_image_rect_y = image_rect.y

            image_rect.y += self.scroll_y + self.top_y # si hay scroll dentro de box_sprite_loader o colision de self.rect lo agregamos a y

            # box_text
            x = image_rect.x 
            y = image_rect.y + image_rect.h - 20
            w = self.gridx
            h = 20
            #base_name, extension = os.path.splitext(image_name) # nombre base sin la extencion PNG,JPGE ect..
            boxtext = BoxText(event_dict,self.surface,x,y,w,h,text=image_name)

            self.images.append([image_surface, image_rect, save_image_rect_y,image_name,boxtext])
            
            # orden para los cuadrados en filas y columnas
            if self.gridx * (self.countx+1) < self.rect.width:
                self.countx += 1
            else:
                self.countx = 0
                self.county += 1
        # agrego el elemento add al final de la lista "+"
        add_rect = pg.Rect(self.gridx*self.countx, self.gridy*self.county, self.gridx,self.gridy)
        self.images.append(["No image", add_rect, add_rect.y,"No name","No Box_text"])
        add_rect.y += self.scroll_y + self.top_y # si hay scroll dentro de box_sprite_loader o colision de self.rect lo agregamos a y
        # --------------------------------------------------------------------------

        # reposicionar imagenes seleccionadas en caso que haya
        # --------------------------------------------------------------------------
        self.save_image_select = None 
        for i in self.image_select:
            for j in self.images:
                if i[3] == j[3]:
                    pos = self.image_select.index(i)
                    self.image_select[pos] = j
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------



    def reposition(self):
        # reposiciono los elementos de self.rect.y
        # --------------------------------------------------------------------------
        for i in self.images:
            
            # reposicion de y de cada imagen y "+"
            i[1].y = i[2] + self.scroll_y + self.top_y

            # reposicion box_text de cada imagen menos "+"
            if i != self.images[-1]: # si no es "+"
                # reposicionamos surface y rect de box_text
                i[4].surface = self.surface # reposiciono la superficie tambien
                y = i[1].y + i[1].h - 20
                i[4].rect.y = y
                #i[4].reposition()
        # --------------------------------------------------------------------------

    def save_pickle(self):
        # Guardar la lista en un archivo pickle (menos "+")
        #-------------------------------------------------------------------------
        list = []
        for i in self.images[:-1]:
            list.append(i[3])
        with open('images_name_list.pickle','wb') as archive:
            pickle.dump(list,archive)
        #-------------------------------------------------------------------------


    def edit(self,event_dict = None):

        # Teclas presionadas
        # ----------------------------------------------------------------------------
        if event_dict["keyPressed"]: 
            key = event_dict["keyPressed"][-1] # ultima tecla presionada
            if key["key"] == 127: k_sup = True # suprimir
            else: k_sup = False 
            if key["key"] == 1073742049: k_shift = True # Shift
            else: k_shift = False
            if key["key"] == 13: k_enter = True # "Enter"
            else: k_enter = False 
        else: 
            key = False
            k_sup = False
            k_shift = False
            k_enter = False
        # ----------------------------------------------------------------------------



        # SCROLL ---------------------------------------------------------------------
        can_scroll = self.gridy*(self.county+1) > (self.down_y - self.top_y)
        if event_dict["MouseScroll"]!=None and can_scroll:
            dis = 20
            if event_dict["MouseScroll"] == 1:
                if not(self.images[0][1].y + dis < self.top_y): # colicioin arriba
                    self.scroll_y += self.top_y - self.images[0][1].y
                else:
                    self.scroll_y += dis
            elif event_dict["MouseScroll"] == -1:
                if not(self.images[-1][1].y + self.gridy - dis > self.down_y): #colicion abajo
                    self.scroll_y += self.down_y - (self.images[-1][1].y + self.gridy)
                else:
                    self.scroll_y += -dis
            self.reposition()
        # ----------------------------------------------------------------------------




        
        # HAGO CLICK IZQUIERDO
        # ----------------------------------------------------------------------------
        save_x_y = event_dict["MouseClickLeft"] # salvamos posicion del click mouse izquierdo
        if event_dict["MouseClickLeft"]:
            x = event_dict["MouseClickLeft"][0] - self.rect.x 
            y = event_dict["MouseClickLeft"][1] - self.rect.y
            event_dict["MouseClickLeft"] = (x,y) # ahora esto no es necesario


            # AGREGAR IMAGENES - deteccion 0
            # ----------------------------------------------------------------------------
            if self.images[-1][1].collidepoint(x,y):
                
                #borro el ultimo elemento de la lista
                del self.images[-1] # se borra "+"
                # seleccionamos las imagenes de la ruta original en el ordenador
                file_paths = filedialog.askopenfilenames(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
                os.chdir(self.folder_images_path) # nos mueve a la hubicacion de la ruta

                for file_path in file_paths:
                    image_name = os.path.basename(file_path)
                    archive_in_folder = os.path.join(self.folder_images_path,image_name)

                    if os.path.exists(archive_in_folder): 
                        # si existe cambio nombre de la imagen
                        unique_suffix = uuid.uuid4().hex[:6] # Generar un sufijo único
                        base_name, extension = os.path.splitext(image_name)
                        image_name = f"{base_name}_{unique_suffix}{extension}"
                        destination_file_path = os.path.join(self.folder_images_path, image_name)
                        shutil.copy2(file_path,destination_file_path)
                    else:
                        shutil.copy2(file_path,self.folder_images_path)
                        
                    try:
                        
                        image_surface = pg.image.load(image_name)

                        # Cargar cada imagen seleccionada
                        image_surface = pg.transform.scale(image_surface,(self.gridx,self.gridx))

                        # rect images
                        x = self.gridx*self.countx
                        y = self.gridy*self.county
                        w = self.gridx
                        h = self.gridy
                        image_rect = pg.Rect(x,y,w,h)

                        save_image_rect_y = image_rect.y

                        image_rect.y += self.scroll_y + self.top_y # si hay scroll dentro de box_sprite_loader o colision de self.rect lo agregamos a y

                        # box_text
                        x = image_rect.x 
                        y = image_rect.y + image_rect.h - 20
                        w = self.gridx
                        h = 20
                        #base_name, extension = os.path.splitext(image_name) # nombre base sin la extencion PNG,JPGE ect..
                        boxtext = BoxText(event_dict,self.surface,x,y,w,h,text=image_name)

                        self.images.append([image_surface, image_rect, save_image_rect_y,image_name,boxtext])
                        
                        # orden para los cuadrados en filas y columnas
                        if self.gridx * (self.countx+1) < self.rect.width:
                            self.countx += 1
                        else:
                            self.countx = 0
                            self.county += 1
                        
                    except ZeroDivisionError as error:
                        # Manejar la excepción específica
                        print(f"Error: {error}")
                        print("No es una imagen")

                # agrego el elemento add al final de la lista "+"
                add_rect = pg.Rect(self.gridx*self.countx, self.gridy*self.county, self.gridx,self.gridy)
                self.images.append(["No image", add_rect, add_rect.y,"No name","No Box_text"])
                add_rect.y += self.scroll_y + self.top_y # si hay scroll dentro de box_sprite_loader o colision de self.rect lo agregamos a y

                self.save_pickle() # Guardar la lista en un archivo pickle
            #-------------------------------------------------------------------------
            else:
                for image in self.images[:-1]:

                    # SELECTOR DE BOX_TEXT - deteccion 1
                    # ----------------------------------------------------------------------------
                    if image[4].rect.collidepoint(x,y):

                        self.save_image_select = None
                        self.image_select.clear()

                        try:
                            del event_dict["EditPoint"][self.depth_number+1:]
                        except Exception as e:
                            pass
                            #print(f"Error: {e}")
                        event_dict["EditPoint"].append(image[4])
                        #self.box_text_is_edit = image[4] # guardamos en box_text que se esta editando
                        #self.save_text_edit = image[3] # guardo nombre original de la imagen 
                        break
                    # ----------------------------------------------------------------------------



                    # SELECTOR DE IMAGENES - deteccion 2
                    # ----------------------------------------------------------------------------
                    elif image[1].collidepoint(x,y):
                        # seleccion multiple
                        if k_shift: # Shift:
                            if self.image_select and not(image in self.image_select):
                                if not(self.save_image_select):
                                    self.save_image_select = self.image_select[0]
                                self.image_select.clear()
                                position1 = self.images.index(self.save_image_select)
                                position2 = self.images.index(image)
                                if position1 < position2:
                                    for i in self.images[position1:position2+1]:
                                        self.image_select.append(i)
                                elif position1 > position2:
                                    for i in self.images[position2:position1+1]:
                                        self.image_select.append(i)
                                break
                            else:
                                # seleccion simple
                                self.save_image_select = None
                                self.image_select.clear()
                                self.image_select.append(image)
                                break
                        else:
                            # seleccion simple
                            self.save_image_select = None
                            self.image_select.clear()
                            self.image_select.append(image)
                            break
                else: self.image_select.clear()
                    # ----------------------------------------------------------------------------
        
        

        # EJECUTO BOX_TEXT- cambio de nombre imagen
        # ----------------------------------------------------------------------------
        try:
            event_dict["EditPoint"][self.depth_number+1].edit(event_dict) 

            """if k_enter:
                box_text = event_dict["EditPoint"][self.depth_number+1]
                
                for i in self.images:
                    #self.images = [image_surface, image_rect, save_image_rect_y, image_name, boxtext]
                    i[4] = box_text
                    break
                try:
                    text = box_text.text
                    os.chdir(self.folder_images_path) # nos mueve a la hubicacion de la ruta
                    os.rename(i[3],text) # cambio el viejo nombre por el nuevo en la carpeta
                    i[3] = text # cambio el viejo nombre por el nuevo en "self.images"
                except:
                    box_text.text = i[3]
                    print("ya hay un archivo con ese nombre en la carpeta")

                self.save_pickle() # Guardar la lista en un archivo pickle
                del event_dict["EditPoint"][self.depth_number+1:]"""

        except Exception as e:
            pass
            #print(f"Error: {e}")
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        event_dict["MouseClickLeft"] = save_x_y # devolvemos valor original de "event_dict["MouseClickLeft"]", no es necesario
        # ----------------------------------------------------------------------------  



        # ELIMINAR ELEMENTOS
        # ----------------------------------------------------------------------------
        if k_sup: # suprimir
            # si seleccionamos alguna imagen
            if self.image_select:
                # eliminar elementos de la lista self.images
                for i in self.image_select:
                    folder_images_path = os.path.join(event_dict["GameFolderpPath"],"Images") # ruta a Images
                    os.chdir(folder_images_path) # nos mueve a la hubicacion de la ruta
                    try:
                        os.remove(self.images[self.images.index(i)][3]) # elimina la imagen de la carpeta
                    except:
                        print("No se encontro archivo")

                    del self.images[self.images.index(i)] # elimina la imagen de la lista
                self.image_select.clear()

                
                # reacomodar los elementos de la lista self.images
                self.countx= 0
                self.county= 0
                #self.save_images_rect_y.clear() # eliminamos la posicion guardadas de las imagenes
                for i in self.images[:-1]: # recorremos la lista menos el ultimo elemento

                    # reposicion de las imagenes
                    # ----------------------------------------------------------------------------
                    i[1].x = self.gridx*self.countx
                    i[1].y = self.gridy*self.county 
                    # ----------------------------------------------------------------------------
                    
                    i[2] = i[1].y # guardamos posicion base
                    i[1].y += self.scroll_y + self.top_y # agregamos scroll y reposicion

                    # box_text reposicion (x,y)
                    # ----------------------------------------------------------------------------
                    i[4].rect.x = i[1].x
                    i[4].rect.y = i[1].y + i[1].h - 20 
                    i[4].reposition()
                    # ----------------------------------------------------------------------------

                    if self.gridx * (self.countx+1) < self.rect.width:
                        self.countx += 1
                    else:
                        self.countx = 0
                        self.county += 1
                # reposicion de "+"
                self.images[-1][1].x = self.gridx*self.countx
                self.images[-1][1].y = self.gridy*self.county 
                #self.save_images_rect_y.append(self.images[-1][1].y) # guardamos posicion base
                self.images[-1][2] = self.images[-1][1].y # guardamos posicion base
                self.images[-1][1].y += + self.scroll_y + self.top_y # agregamos scroll y reposicion
                

                self.save_pickle() # Guardar la lista en un archivo pickle

                # reposicionamos dependiendo de la posicion de scroll para evitar salida de rango
                #-----------------------------------------------------------------------------
                can_scroll = self.gridy*(self.county+1) > (self.down_y - self.top_y) # si puedo hacer scroll
                max_scroll_down = self.images[-1][1].y + self.gridy < self.down_y # si me salgo del rango maximo del scroll
                if can_scroll and max_scroll_down: # si me salgo del rango maximo y puedo scrolear
                    self.scroll_y += self.down_y - (self.images[-1][1].y + self.gridy) # resto el rango que sobra a scroll
                    self.reposition()

                elif not(can_scroll) and max_scroll_down: # si me salgo del rango maximo y no puedo scrolear
                    self.scroll_y = 0
                    self.reposition()
                #-----------------------------------------------------------------------------

                
        #-----------------------------------------------------------------------------


    def draw(self,event_dict):
        # box_sprite_loader
        #---------------------------------------------------------------------------------
        pg.draw.rect(self.preSurface,self.color,self.rect) # dibujar rectangulo de fondo
        for i in self.images:

            # verifico si el objeto en lista_image es una imagen, si es asi la dibujo
            if isinstance(i[0],pg.surface.Surface):
                # imagen
                self.surface.blit(i[0],i[1]) 
                #rect gris de las imagenes
                pg.draw.rect(self.surface,(80,80,80),i[1],1) 

                i[4].draw(event_dict)

                if i in self.image_select:
                    pg.draw.rect(self.surface,(204,255,0),i[1],1)

                


            elif isinstance(i[0],str): # dibujo "+"
                line = 30
                c = (120,120,120)
                x1 = i[1].x + self.gridx/2 - line/2
                x2 = i[1].x + self.gridx/2 + line/2
                y1 = i[1].y + self.gridy/2 
                pg.draw.line(self.surface,c,(x1,y1),(x2,y1),5)
                x1 = i[1].x + self.gridx/2 
                y1 = i[1].y + self.gridy/2 - line/2
                y2 = i[1].y + self.gridy/2 + line/2
                pg.draw.line(self.surface,c,(x1,y1),(x1,y2),5)

                pg.draw.rect(self.surface,(80,80,80),i[1],1) #rect gris de las imagenes
        #---------------------------------------------------------------------------------
            







