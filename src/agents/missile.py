import tkinter as tk
import math
import random
from algorithms.direct_path import DirectPath

class Missile:
    def initialise(self, id, acceleration, turn_strength, explosion_radius, detonation_distance, fuel, fuel_rate, targetting_strategy, status, jet, type):
        self.ID = id
        #these are the same as the jet its attached to
        self.x = jet.get_position()[0]
        self.y = jet.get_position()[1]
        self.heading = jet.get_heading()
        self.velocity = jet.get_velocity()

        self.acceleration = acceleration
        self.turn_rate = 0
        self.TURN_STRENGTH = turn_strength
        self.EXPLOSION_RADIUS = explosion_radius
        self.DETONATION_DISTANCE = detonation_distance
        self.fuel = fuel
        self.FUEL_RATE = fuel_rate
        self.TARGETTING_STRATEGY = targetting_strategy #need to make these strategies
        self.STATUS = status #can be "armed", "fired", "exploded"
        self.jet = jet #the jet object that this missile is attached to, used to get the position and heading of the missile when it is attached to the jet
        self.target = None
        self.JET_ID = jet.get_id() #the id of the jet that this missile is attached to
        self.TYPE = type #can be "friendly" or "enemy"
        self.NAME = "missile"
        self.canvas_id = None
        self.radar = None
        self.drag = 0.5
        self.hit = False #a boolean to see whether the missile hit the target

    #@NOTE: delta_time is the time since last frame which is a nonlocal variable passed through from main.py
    def move(self, delta_time, elapsed_time):

        if self.STATUS == "exploded":
            return #returning early if the missile is exploded so the simulation can handle the rest

        #keeping missile attached to the jet and invisible until its fired
        if self.STATUS == "armed": #if the missile is not in status "fired", it will stay attached to the jet and invisible, so update its position and heading to match the jet
            self.x, self.y = self.jet.get_position()
            self.heading = self.jet.get_heading()
            self.velocity = self.jet.get_velocity()
            self.acceleration = self.jet.get_acceleration()
            return

        #below is just the set movements of the missile (only run if fired, otherwise the missile will stay attached to the jet and invisible)
        if self.STATUS == "fired":
            #update this logic to decide what the missile does when fired (changed depending on targetting strategy @NOTE: to be implemented)
            if self.TARGETTING_STRATEGY == "direct_path":
                #if the directpath hasnt already been initialised @NOTE: might not need to do this
                
                direct_path = DirectPath()
                direct_path.initialise(self, self.target) #initialising the direct path algorithm with the missile and the target position (currently set to the jet's position for testing, but will be changed to the enemy jet's position when implemented)
                direct_path.update(delta_time, elapsed_time) #updating the missile's turn rate based on the direct path algorithm
            #movement logic
            self.velocity += self.acceleration * delta_time
            self.heading += self.turn_rate * delta_time
            self.heading %= 360 #modding with 360 to keep the heading within 360 degrees
            #move in the direction of the heading at the current velocity
            rad = math.radians(self.heading)
            self.x += math.sin(rad) * self.velocity * delta_time
            self.y -= math.cos(rad) * self.velocity * delta_time

            #controlling fuel
            if(self.fuel > 0):
                self.fuel -= self.FUEL_RATE * delta_time

            #vicinity detonation logic
            if self.target is not None:
                target_x, target_y = self.target.get_position()
                distance_to_target = math.sqrt(
                    (target_x - self.x) ** 2 + #x position
                    (target_y - self.y) ** 2   #y position
                )
                if distance_to_target <= self.DETONATION_DISTANCE:
                    self.STATUS = "exploded"
                    self.hit = True



        
        #keep the missile within the bounds of the simulation by wrapping around the boundaries
        if self.x < 0:
            self.x = 1000
        elif self.x > 1000:
            self.x = 0
        if self.y < 0:
            self.y = 1000
        elif self.y > 1000:
            self.y = 0


    

    #getters
    #generalised getter
    def get_info(self):
        return (self.id, self.x, self.y, self.heading, self.velocity, self.acceleration, self.turn_rate)
    #specific getters
    def get_position(self):
        return (self.x, self.y)
    def get_heading(self):
        return self.heading
    def get_velocity(self):
        return self.velocity
    def get_acceleration(self):
        return self.acceleration
    def get_id(self):
        return self.ID
    def get_type(self):
        return self.TYPE
    def get_name(self):
        return self.NAME
    def get_canvas_id(self):
        return self.canvas_id
    def get_turn_rate(self):
        return self.turn_rate
    def get_turn_strength(self):
        return self.TURN_STRENGTH
    def get_explosion_radius(self):
        return self.EXPLOSION_RADIUS
    def get_detonation_distance(self):
        return self.DETONATION_DISTANCE
    def get_fuel(self):
        return self.fuel
    def get_fuel_rate(self):
        return self.FUEL_RATE
    def get_targetting_strategy(self):
        return self.TARGETTING_STRATEGY
    def get_status(self):
        return self.STATUS
    def get_jet(self):
        return self.jet
    def get_radar(self):
        return self.radar
    def get_target(self):
        return self.target
    def get_hit_status(self):
        return self.hit
    
    #setters
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    def set_heading(self, heading):
        self.heading = heading
    def set_velocity(self, velocity):
        self.velocity = velocity
    def set_canvas_id(self, canvas_id):
        self.canvas_id = canvas_id
    def set_turn_rate(self, turn_rate):
        self.turn_rate = turn_rate
    def set_fuel(self, fuel):
        self.fuel = fuel
    def set_status(self, status):
        self.STATUS = status
    def set_target(self, target):
        self.target = target
    def set_radar(self, radar):
        self.radar = radar
