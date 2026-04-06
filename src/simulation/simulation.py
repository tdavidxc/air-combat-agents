import tkinter as tk
import math
import random
from PIL import Image, ImageTk #library used to image manage in tkinter
import time

class Simulation:
    def initialise(self, window, width, height):
        print("Initialising simulation")
        window.resizable(False, False)
        canvas = tk.Canvas(window, width=width, height=height, bg='white')
        canvas.pack()
        self.pil_images = {} #storing original PIL images by object id for modification
        self.current_images = {} 
        return canvas
        
    
    def create_objects(self, canvas, objects):
        for current_object in objects:
            
            #if the object is a jet and is friendly, load the friendly jet png at the location initialised
            if current_object.get_name() == "jet":
                if current_object.get_type() == "friendly":
                    img = Image.open("agents\\models\\friendly_jet.png").resize((60, 60))
                elif current_object.get_type() == "enemy":
                    img = Image.open("agents\\models\\enemy_jet.png").resize((60, 60))
                self.pil_images[current_object.get_id()] = img
                
                rotated = img.rotate(-current_object.get_heading(), expand=True)
                image = ImageTk.PhotoImage(rotated)
                self.current_images[current_object.get_id()] = image

                item_id = canvas.create_image(
                    current_object.get_position()[0], 
                    current_object.get_position()[1], 
                    image=image
                )
                current_object.set_canvas_id(item_id)
                
                print(current_object.get_type() + " " + current_object.get_name() + " spawned at position: ", current_object.get_position(), "with velocity: ", current_object.get_velocity(), "and heading: ", current_object.get_heading())


    def update_objects(self, canvas, objects):
        for current_object in objects:
            if current_object.get_name() == "jet":
                #orientation
                self.rotate_object(canvas, current_object, current_object.get_heading())
                #position
                canvas.coords(current_object.get_canvas_id(), current_object.get_position()[0], current_object.get_position()[1])


            


    def rotate_object(self, canvas, object, angle):
        object.set_heading(angle)
        img = self.pil_images[object.get_id()] # getting the original unrotated image
        rotated = img.rotate(-angle, expand=True) #PIL rotates counter-clockwise so using negative to reverse that
        image = ImageTk.PhotoImage(rotated)
        self.current_images[object.get_id()] = image #keeping the reference alive
        canvas.itemconfig(object.get_canvas_id(), image=image) #updating the canvas item
