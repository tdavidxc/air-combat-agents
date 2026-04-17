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
    def move(self, delta_time, elapsed_time, agents):
        #updated movement logic is to keep the jet within its individual territory which is split half horizontally in the canvas
        canvas_mid = 500 #the middle of the canvas
        if self.TYPE == "friendly":
            zone_center_y = 250 #the center of the friendly zone
            boundary_min = 0
            boundary_max = 500
        if self.TYPE == "enemy":
            zone_center_y = 750 #the center of the enemy zone
            boundary_min = 500
            boundary_max = 1000
        
        #updating so evasion logic comes before boundary logic
        evasion = self.get_evasion_maneuver(agents, delta_time)
        if evasion is not None:
            self.heading += evasion

        #now applying a weaker boundary correction
        #adding a soft boundary steering to keep the jets within their territory
        elif self.y < boundary_min + 100 or self.y > boundary_max - 100: #checks if near boundary (100 is the boundary margin)
            dy = zone_center_y - self.y
            dx = 0 #we really only want to steer vertically because the sides are looped around

            target_angle = math.degrees(math.atan2(dy, dx))
            raw_difference = (target_angle - self.heading + 360) % 360
            if raw_difference > 180:
                raw_difference -= 360 #converting the angle difference between -180 to 180 for easier calculating
            max_turn = self.turn_rate * delta_time
            self.heading += max(-max_turn, min(max_turn, raw_difference))

        #fallback wandering with a small nudge only, otherwise the jet wandering is too aggressive
        else:
            self.heading += random.uniform(-1, 1) * self.turn_rate * 0.1 * delta_time #no threats, wander normally

        #simple movement logic for the jet right now, it moves with the initialised characteristics
        self.velocity += self.acceleration * delta_time
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
        #not doing y wrapping because I want jets to stay in their territories
        if self.y < 0:
            self.y = 1000
        elif self.y > 1000:
            self.y = 0


    #this method returns the heading depending on what zone its in: too close to a threat = run, in firing range = hold and shoot, far away = approach
    #@NOTE: need to add logic where the jet can only see if its within radar range and fov. Right now, it can evade any threat
    def get_evasion_maneuver(self, agents, delta_time):
        DANGER_RADIUS = 300 #if any enemy is within this radius, its a danger so we run
        ENGAGE_RADIUS = 400 #prefered fighting distance
        MISSILE_DANGER = 500 #if any missile is within this radius, its a danger so we run too

        closest_threat = None
        closest_dist = float('inf') #we want the closest thread distance to be infinity so any threat will be closer than this
        closest_is_missile = False #keeping track of what the closest threat is

        for agent in agents:
            #filtering for enemies only
            if agent.get_type() == self.TYPE:
                continue #doing nothing
            if agent.get_id() == self.ID:
                continue #also doing nothing because its itself

            #anything else is the enemy
            #finding the distance to the target
            dist = math.sqrt(
                (agent.get_position()[0] - self.x) ** 2 +  #the x position
                (agent.get_position()[1] - self.y) ** 2    #the y position
            )

            #missile evasion logic
            if agent.get_name() == "missile" and dist < MISSILE_DANGER:
                if dist < closest_dist:
                    closest_dist = dist
                    closest_threat = agent
                    closest_is_missile = True
            #jet logic to decide whether to run, engage, or approach
            elif agent.get_name() == "jet" and not closest_is_missile and dist < ENGAGE_RADIUS: #no need to redo check
                if dist < closest_dist:
                    closest_dist = dist
                    closest_threat = agent
                    closest_is_missile = False

        #if no threats detected, returning None
        if closest_threat is None:
            return None
        

        #getting target position to decide evasion maneuver
        tx, ty = closest_threat.get_position()
        screen_angle = math.degrees(math.atan2(ty - self.y, tx - self.x))
        angle_to_threat = self.screen_angle_to_heading(screen_angle)

        #@NOTE: this is where you decide how to evade a missile
        if closest_is_missile:
            #turning perpendicular to the missile's trajectory to try and bleed its energy like in real life
            dodge_angle = (angle_to_threat + 90) % 360
            raw_diff = (dodge_angle - self.heading + 360) % 360
            if raw_diff > 180:
                raw_diff -= 360
            max_turn = self.turn_rate * delta_time
            return max(-max_turn, min(max_turn, raw_diff))
        
        #@NOTE: theses are the logics on how to handle other jets
        #if the jet is too close, we need to run away from it
        if closest_dist < DANGER_RADIUS:
            run_angle = (angle_to_threat + 180) % 360
            raw_diff = (run_angle - self.heading + 360) % 360
            if raw_diff > 180:
                raw_diff -= 360
            max_turn = self.turn_rate * delta_time
            return max(-max_turn, min(max_turn, raw_diff))
        #if the jet is at a good distance, hold the distance by orbitting like the default maneouver
        if closest_dist < ENGAGE_RADIUS:
            orbit_angle = (angle_to_threat + 90) % 360 #circling around them
            raw_diff = (orbit_angle - self.heading + 360) % 360
            if raw_diff > 180:
                raw_diff -= 360
            max_turn = self.turn_rate * delta_time
            return max(-max_turn, min(max_turn, raw_diff))
        #if the jet is far away, close in
        raw_diff = (angle_to_threat - self.heading + 360) % 360
        if raw_diff > 180:
            raw_diff -= 360
        max_turn = self.turn_rate * delta_time
        return max(-max_turn, min(max_turn, raw_diff))



    def screen_angle_to_heading(self, screen_angle):
        return (90 - screen_angle) % 360

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
    

