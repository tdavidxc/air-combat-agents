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
        self.log = [] #storing the log of the simulation (the report of the simulation)
        self.elapsed_time = 0
        return canvas
        
    
    def create_objects(self, canvas, objects):
        for current_object in objects:
            
            #if the object is a jet and is friendly, load the friendly jet png at the location initialised
            if current_object.get_name() == "jet":
                if current_object.get_type() == "friendly":
                    img = Image.open("agents\\models\\friendly_jet.png").resize((60, 60))
                elif current_object.get_type() == "enemy":
                    img = Image.open("agents\\models\\enemy_jet.png").resize((60, 60))
            
            #if the object is a missile
            if current_object.get_name() == "missile":
                if current_object.get_type() == "friendly":
                    img = Image.open("agents\\models\\friendly_missile.png").resize((4, 20))
                elif current_object.get_type() == "enemy":
                    img = Image.open("agents\\models\\enemy_missile.png").resize((4, 20))
            
            self.pil_images[current_object.get_id()] = img
                
            rotated = img.rotate(-current_object.get_heading(), expand=True)
            photo = ImageTk.PhotoImage(rotated)
            self.current_images[current_object.get_id()] = photo

            item_id = canvas.create_image(
                current_object.get_position()[0], 
                current_object.get_position()[1], 
                image=self.current_images[current_object.get_id()]
            )
            current_object.set_canvas_id(item_id)
            
            print(current_object.get_type() + " " + current_object.get_name() + " spawned at position: ", current_object.get_position(), "with velocity: ", current_object.get_velocity(), "and heading: ", current_object.get_heading())


    def update_objects(self, canvas, objects):
        for current_object in list(objects):
            if current_object.get_name() == "jet":
                #orientation
                self.rotate_object(canvas, current_object, current_object.get_heading())
                #position
                canvas.coords(current_object.get_canvas_id(), current_object.get_position()[0], current_object.get_position()[1])
            elif current_object.get_name() == "missile":
                #the missile will be attached to the jet and invisible until its fired, so only update the position and orientation if it has been fired
                if current_object.STATUS == "armed":
                    #visibility
                    canvas.itemconfig(current_object.get_canvas_id(), state='hidden')
                    #orientation and position of the jet its attached to
                    jet = next((obj for obj in objects if obj.get_id() == current_object.JET_ID), None)
                    if jet is not None:
                        self.rotate_object(canvas, current_object, jet.get_heading())
                        #position of the jet its attached to
                        canvas.coords(current_object.get_canvas_id(), jet.get_position()[0], jet.get_position()[1])



                elif current_object.STATUS == "fired":
                    #visibility
                    canvas.itemconfig(current_object.get_canvas_id(), state='normal')
                    #orientation
                    self.rotate_object(canvas, current_object, current_object.get_heading())
                    #position
                    canvas.coords(current_object.get_canvas_id(), current_object.get_position()[0], current_object.get_position()[1])

                    

                elif current_object.STATUS == "exploded":
                    if(current_object.explosion_reason == "hit"):
                        print("Missile " + str(current_object.get_id()) + " exploded at position: ", current_object.get_position(), "after hitting its target.")
                    elif(current_object.explosion_reason == "fuel"):
                        print("Missile " + str(current_object.get_id()) + " exploded at position: ", current_object.get_position(), "after running out of fuel.")
                        self.add_log("Missile " + str(current_object.get_id()) + " exploded at position: " + str(current_object.get_position()) + " after running out of fuel.")
                    #visibility
                    canvas.itemconfig(current_object.get_canvas_id(), state='hidden')
                    #potentially add explosion animation in the future @NOTE
                    #deleting the missile object
                    canvas.delete(current_object.get_canvas_id())
                    objects.remove(current_object)
                    
                    

                    #detecting if any jets were within the explosion radius and track which ones were hit for the final report at the end of the simulation
                    jets_exploded = []
                    if current_object.get_name() == "missile" and current_object.get_hit_status() == True: #only if the missile hit a jet
                        for obj in objects:
                            #only if its a jet
                            if obj.get_name() == "jet":
                                #calculating the distance between the explosion and the jet
                                #this is not to do the explosion check, but instead to see whether any damage was done by the explosion
                                distance = math.sqrt(
                                    (obj.get_position()[0] - current_object.get_position()[0]) ** 2 +  #the x position
                                    (obj.get_position()[1] - current_object.get_position()[1]) ** 2    #the y position
                                )
                                if distance <= current_object.EXPLOSION_RADIUS:
                                    print("Jet " + str(obj.get_id()) + " was hit by the explosion of missile " + str(current_object.get_id()) + " at position: ", obj.get_position())
                                    #logging jetx killed jety using missilez at position p
                                    self.add_log("Jet " + str(current_object.get_jet()) + " killed Jet " + str(obj.get_id()) + " using Missile " + str(current_object.get_id()) + " as position: " + str(obj.get_position()))
                                    jets_exploded.append(obj)
                    #removing the jets that were hit
                    for jet in jets_exploded:
                        canvas.delete(jet.get_canvas_id())
                        objects.remove(jet)

                    #display the explosion at agents\\models\\explosion.png for 1 seconds
                    explosion_img = Image.open("agents\\models\\explosion.png").resize((60, 60))
                    explosion_image = ImageTk.PhotoImage(explosion_img)
                    explosion_id = canvas.create_image(
                        current_object.get_position()[0], 
                        current_object.get_position()[1], 
                        image=explosion_image
                    )
                    #keeping the reference alive
                    self.current_images["explosion_" + str(current_object.get_id())] = explosion_image

                    #removing the explosion after 1 second
                    canvas.after(1000, lambda eid=explosion_id: canvas.delete(eid)) #what lambda does is create a function without actually defining it. using eid to make sure multiple explosions dont mean any other explosion functions get trampled on




    def rotate_object(self, canvas, object, angle):
        object.set_heading(angle)
        img = self.pil_images[object.get_id()] # getting the original unrotated image
        rotated = img.rotate(-angle, expand=True) #PIL rotates counter-clockwise so using negative to reverse that
        image = ImageTk.PhotoImage(rotated)
        self.current_images[object.get_id()] = image #keeping the reference alive
        canvas.itemconfig(object.get_canvas_id(), image=image) #updating the canvas item

    def get_log(self):
        return self.log
    
    def add_log(self, entry):
        #adding log with elapsed time
        self.log.append("[" + str(int(self.elapsed_time)) + "s] " + entry)

    def set_elapsed_time(self, elapsed_time):
        self.elapsed_time = elapsed_time