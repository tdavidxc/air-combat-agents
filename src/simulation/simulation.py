import tkinter as tk
import math
import random
from PIL import Image, ImageTk #library used to image manage in tkinter
import time
import os

class Simulation:
    def initialise(self, window, width, height):
        print("Initialising simulation")
        window.resizable(False, False)
        canvas = tk.Canvas(window, width=width, height=height, highlightthickness=0)
        canvas.pack()

        #splitting the window into two sections to depict friendly and enemy territory -> https://stackoverflow.com/questions/67448917/how-to-change-background-color-for-a-specific-portion-of-window-python-tkinte
        canvas.create_rectangle(0,0, width, height/2, fill="#ff6b6b", outline="") #enemy territory
        canvas.create_rectangle(0,height/2, width, height, fill="#6babff", outline="") #friendly territory

        self.pil_images = {} #storing original PIL images by object id for modification
        self.current_images = {} 
        self.log = [] #storing the log of the simulation (the report of the simulation)
        self.elapsed_time = 0
        self.enemy_datalink = None
        self.friendly_datalink = None
        return canvas
        

    def create_objects(self, canvas, objects):
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'agents', 'models', 'new')

        for current_object in objects:
            
            #if the object is a jet and is friendly, load the friendly jet png at the location initialised
            if current_object.get_name() == "jet":
                if current_object.get_type() == "friendly":
                    img = Image.open(os.path.join(models_dir, 'blue jet w fire.png')).resize((60, 60))
                elif current_object.get_type() == "enemy":
                    img = Image.open(os.path.join(models_dir, 'red jet w fire.png')).resize((60, 60))
            
            #if the object is a missile
            if current_object.get_name() == "missile":
                if current_object.get_type() == "friendly":
                    if current_object.get_acceleration() > 0:
                        img = Image.open(os.path.join(models_dir, 'blue missile ver 2 w fire.png')).resize((4, 20))
                    else:
                        img = Image.open(os.path.join(models_dir, 'blue missile ver 2.png')).resize((4, 20))
                elif current_object.get_type() == "enemy":
                    if current_object.get_acceleration() > 0:
                        img = Image.open(os.path.join(models_dir, 'red missile ver 2 w fire.png')).resize((4, 20))
                    else:
                        img = Image.open(os.path.join(models_dir, 'red missile ver 2.png')).resize((4, 20))
            
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
                    self.animate_explosion(canvas, current_object.get_position(), 300) #animating the explosion with a frame change every 300 milliseconds


    def animate_explosion(self, canvas, position, time_interval):
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'agents', 'models', 'new')

        big_explosion_image    = Image.open(os.path.join(models_dir, 'biggest explosion.png')).resize((100, 100))
        medium_explosion_image = Image.open(os.path.join(models_dir, 'middle child.png')).resize((70, 70))
        small_explosion_image  = Image.open(os.path.join(models_dir, 'smallest explosion.png')).resize((40, 40))
        explosion_images = [big_explosion_image, medium_explosion_image, small_explosion_image]
        explosion_photo_images = [ImageTk.PhotoImage(img) for img in explosion_images]
        explosion_id = canvas.create_image(position[0], position[1], image=explosion_photo_images[0])
        
        #unique keys
        ref_key = "explosion_" + str(id(explosion_id))
        self.current_images[ref_key] = explosion_photo_images

        def animate(index):
            if index < len(explosion_photo_images):
                canvas.itemconfig(explosion_id, image=explosion_photo_images[index])
                canvas.after(time_interval, lambda: animate(index + 1))
            else:
                canvas.delete(explosion_id)
                if ref_key in self.current_images:
                    del self.current_images[ref_key] #the del keyword can be used to remove a key from a dictionary, this is to prevent memory leaks by keeping references to images that are no longer needed
        animate(1) #animate() is then called with the next index to start the animation


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


    def get_object_distance(self, object1, object2):
        #check if they are initialised and exist
        if object1 is None or object2 is None:
            return None
        return math.sqrt(
            (object1.get_position()[0] - object2.get_position()[0]) ** 2 +  #the x position
            (object1.get_position()[1] - object2.get_position()[1]) ** 2    #the y position
        )
    

    #running a simulation without the canvas or tkinter, simply for testing the logic of the simulation
    def run_headless(self, agents, ticks, delta_time, friendly_datalink=None, enemy_datalink=None):
        #counters to track the stats
        interceptions = 0
        friendly_casualties = 0
        friendly_fire_incidents = 0
        interception_times = []
        missiles_out_of_fuel = 0
        total_missiles_fired = 0

        for tick in range(ticks):
            elapsed_time = tick * delta_time #this would be the elapsed time in seconds based on the delta time that's input

            #updating datalink
            if friendly_datalink is not None:
                friendly_datalink.update(agents)
            if enemy_datalink is not None:
                enemy_datalink.update(agents)

            #jets update their radar and pick a target
            for agent in list(agents):
                if agent.get_name() == "jet":
                    agent.update_targeting(agents)

            #each jet tries to fire a missile at its current target
            for agent in list(agents):
                if agent.get_name() == "jet":
                    fired = agent.try_fire_missiles(agents)
                    if fired is not None:
                        total_missiles_fired += 1

            #TODO fired missiles ask jets for updated positions via datalink (basic now, but a direct ask will be used for now, a shared map will be implemented later TODO)
            for agent in list(agents):
                if agent.get_name() == "missile" and agent.STATUS == "fired":
                    agent.update_target_position(agents)

            

            #all agents move
            for agent in list(agents):
                agent.move(delta_time, elapsed_time, agents) #move the agent based on its own individual movement logic

            #check for any missiles that have chosen to explode and check if anything got hit etc.
            for agent in list(agents):
                #skip that isnt an exploded missile
                if agent.get_name() != "missile" or agent.STATUS != "exploded":
                    continue

                #check if the missile exploded because it ran out of fuel or whether it hit something
                if agent.get_explosion_reason() == "fuel":
                    missiles_out_of_fuel += 1

                #if it hit something, check the explosion radius and what was in its radius
                if agent.get_hit_status():
                    jets_hit = []
                    for obj in list(agents):
                        if obj.get_name() != "jet":
                            continue
                        dist = math.sqrt(
                            (obj.get_position()[0] - agent.get_position()[0]) ** 2 +
                            (obj.get_position()[1] - agent.get_position()[1]) ** 2
                        )
                        if dist <= agent.get_explosion_radius():
                            if obj.get_type() != agent.get_type():  # enemy kill
                                interceptions += 1
                                interception_times.append(elapsed_time)
                            else:  # friendly fire
                                friendly_fire_incidents += 1
                            if obj.get_type() == "friendly" and agent.get_type() == "enemy":
                                friendly_casualties += 1
                            jets_hit.append(obj)
                    #remove the jets that were hit
                    for jet in jets_hit:
                        if jet in agents:
                            agents.remove(jet)
                #remove the exploded missile too
                if agent in agents:
                    agents.remove(agent)
            
        #calculating averages and rates when the simulation ends
        avg_time = round(sum(interception_times) / len(interception_times), 2) if interception_times else 0.0
        rate = round((interceptions / max(total_missiles_fired, 1)) * 100, 1)

        return {
            "interceptions"          : interceptions,
            "friendly_casualties"    : friendly_casualties,
            "friendly_fire_incidents": friendly_fire_incidents,
            "interception_rate_pct"  : rate,
            "avg_interception_time_s": avg_time,
            "kills_per_missile"      : round(interceptions / max(total_missiles_fired, 1), 3),
            "missiles_out_of_fuel"   : missiles_out_of_fuel,
            "total_missiles_fired"   : total_missiles_fired,
        }

    #Exact same as run headless but with print statements and calls to update visuals
    #datalinks are set to None by default but can be passed in if it exists
    def run_with_display(self, agents, simulation_length, friendly_datalink=None, enemy_datalink=None):
        import math
        import time
        import os

        DELTA_TIME = 0.016
        total_ticks = int(simulation_length / DELTA_TIME)
 
        # ── open the simulation window ─────────────────────────────────────────
        window = tk.Tk()
        window.title("Planes go Pew Pew")
        canvas = self.initialise(window, 1000, 1000)
 
        # change directory so the image paths inside create_objects() resolve correctly
        # (they use relative paths like "agents\\models\\new\\...")
        original_dir = os.getcwd()
        src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        os.chdir(src_path)
        self.create_objects(canvas, agents)
        os.chdir(original_dir)  # restore working directory
        tick_holder = [0] #using a list to allow modifications inside
 
        def simulation_loop():
            tick = tick_holder[0]

            

            #stop condition
            if tick >= total_ticks:
                print("Simulation ended after " + str(simulation_length) + " seconds.")
                window.destroy()
                return
            
            elapsed_time = tick * DELTA_TIME

            #updating datalink
            if friendly_datalink is not None:
                friendly_datalink.update(agents)
            if enemy_datalink is not None:
                enemy_datalink.update(agents)

            #jets have to pick their targets
            for agent in list(agents):
                if agent.get_name() == "jet":
                    agent.update_targeting(agents)

            #then they have to fire their missiles
            for agent in list(agents):
                if agent.get_name() == "jet":
                    fired = agent.try_fire_missiles(agents)

            #missiles update their target position by asking the jet or their own
            for agent in list(agents):
                if agent.get_name() == "missile" and agent.STATUS == "fired":
                    agent.update_target_position(agents)

            #moving the agents
            for agent in list(agents):
                agent.move(DELTA_TIME, elapsed_time, agents)

            #updating the visuals
            self.update_objects(canvas, agents)

            #the missile explosion check as usual
            for agent in list(agents):
                if agent.get_name() != "missile" or agent.STATUS != "exploded":
                    continue

                if agent.get_explosion_reason() == "fuel":
                    print(f"tick {tick} - missile {agent.get_id()} ran out of fuel and exploded at position: ", agent.get_position())

                if agent.get_hit_status():
                    jets_hit = []
                    for obj in list(agents):
                        if obj.get_name() != "jet":
                            continue
                        dist = math.sqrt(
                            (obj.get_position()[0] - agent.get_position()[0]) ** 2 +
                            (obj.get_position()[1] - agent.get_position()[1]) ** 2
                        )
                        if dist <= agent.get_explosion_radius():
                            if obj.get_type() != agent.get_type():
                                print(f"tick {tick} - Missile {agent.get_id()} hit Jet {obj.get_id()}")
                            else:
                                print(f"tick {tick} - FRIENDLY FIRE - Missile {agent.get_id()} hit own Jet {obj.get_id()}!")
                            jets_hit.append(obj)
                    for jet in jets_hit:
                        if jet in agents:
                            agents.remove(jet)
                if agent in agents:
                    agents.remove(agent)

            tick_holder[0] += 1
            window.after(16, simulation_loop)

 
        # kick off the loop and wait for the window to close before returning
        window.after(16, simulation_loop)
        window.mainloop()