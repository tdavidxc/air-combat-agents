import tkinter as tk
import math
import random

class Jet:
    def initialise(self, id, x, y, heading, velocity, acceleration, turn_rate, type, radar_range, radar_fov):
        self.ID = id
        self.x = x
        self.y = y
        self.heading = heading
        self.velocity = velocity
        self.acceleration = acceleration
        self.turn_rate = turn_rate
        self.TYPE = type #can be "friendly" or "enemy"
        self.NAME = "jet"
        self.canvas_id = None
        self.RADAR_RANGE = radar_range
        self.RADAR_FOV = radar_fov
        self.current_target = None
        self.current_target_last_known_position = None #(x,y) of target
        self.radar_targets = []


    #method that scans for targets within radar range and fov and returns a list of targets that are within the radar range
    #note that even if the target is lost from the radar, the missile is already launched with the target's last known pos. so the missile will still try to use its own radar
    def scan_for_targets(self, agents):
        #scan for targets within the radar range and fov
        targets = []
        for agent in agents:
            if agent.get_id() != self.ID and agent.get_type() != self.TYPE: #checking if the agent is not itself and a friendly aircraft
                #calculating the distance and angle to see if it should be added to the targets array
                difference_x = agent.get_position()[0] - self.x
                difference_y = agent.get_position()[1] - self.y
                distance = math.sqrt(difference_x**2 + difference_y**2) #pythagorean theorem
                angle_to_agent = math.degrees(math.atan2(difference_y, difference_x)) % 360 #atan2 gives the angle in radians between the positive x-axis and the point (difference_x, difference_y)
                angle_difference = (angle_to_agent - self.heading + 360) % 360 #calculating the angle difference between the jet's heading and the angle to the agent
                if distance <= self.RADAR_RANGE and (angle_difference <= self.RADAR_FOV / 2 or angle_difference >= 360 - self.RADAR_FOV / 2): #checking if the agent is within the radar range and fov (both sides of the fov)
                    targets.append(agent)
        return targets
    
    #given a list of targets, select a target to engage with
    def select_target(self, targets):
        #scanning for targets

        #if we have a target, check if its still in the radar range
        if self.current_target is not None:
            if self.current_target in targets:
                return self.current_target
            
        #if we dont have a target or our target is not in our radar range anymore, select a new target from the targets array as a random target for now, but we can select closest etc.
        if targets:
            self.current_target = random.choice(targets)
        else:
            self.current_target = None
        return self.current_target
    
    #this method uses the above 2 to do the scan and update the target position
    def update_targeting(self, agents):
        targets = self.scan_for_targets(agents)
        self.select_target(targets)

        #update the last known pos if we can see the target
        if self.current_target is not None:
            self.current_target_last_known_position = self.current_target.get_position()
        #otherwise, it just keeps the last known position

    #@NOTE: delta_time is the time since last frame which is a nonlocal variable passed through from main.py
    def move(self, delta_time, elapsed_time):
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
    def get_radar_range(self):
        return self.RADAR_RANGE
    def get_radar_fov(self):
        return self.RADAR_FOV
    def get_current_target(self):
        return self.current_target
    def get_radar_targets(self):
        return self.radar_targets
    def get_current_target_last_known_position(self):
        return self.current_target_last_known_position
    
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
    

