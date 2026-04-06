import tkinter as tk
import math
import random

class Jet:
    #this is a simpler version of the jet class i made just in-case
    def initialise(self, id, x, y, heading, velocity, type):
        self.ID = id
        self.x = x 
        self.y = y 
        self.heading = heading 
        self.velocity = velocity
        self.acceleration = 0
        self.turn_rate = 0
        self.TYPE = type
        self.NAME = "jet"
        self.canvas_id = None

    def initialise(self, id, x, y, heading, velocity, acceleration, turn_rate, type):
        self.ID = id
        self.x = x
        self.y = y
        self.heading = heading
        self.velocity = velocity
        self.acceleration = acceleration
        self.turn_rate = turn_rate
        self.TYPE = type
        self.NAME = "jet"
        self.canvas_id = None

    #@NOTE: delta_time is the time since last frame which is a nonlocal variable passed through from main.py
    def move(self, delta_time):
        #simple movement logic for the jet right now, it moves with the initialised characteristics
        self.velocity += self.acceleration * delta_time
        self.heading += self.turn_rate * delta_time
        self.heading %= 360 #modding with 360 to keep the heading within 360 degrees

        #move in the direction of the heading at the current v
        rad = math.radians(self.heading)
        self.x += math.sin(rad) * self.velocity * delta_time
        self.y -= math.cos(rad) * self.velocity * delta_time
        
        
        #keep the jet within the bounds of the simulation by wrapping around the boundaries
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
    

