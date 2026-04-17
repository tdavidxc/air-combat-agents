import tkinter as tk
import math

#with predictive pathing, its the same as direct path, but it needs to guess how many seconds until the missile reaches its target, then predict where the target will be at that time and aim towards there instead.
#this means the missile will need to pass the target's movement info through to the targetting algorithm
class PredictivePath:
    def initialise(self, missile, target_x, target_y):
        self.missile = missile
        self.target_x = target_x
        self.target_y = target_y
        self.target_heading = None #the target's heading is needed here to predict where it will be
        self.target_velocity = None #the target's velocity is also needed to predict where it will be

    def update_target_position(self, x, y):
        self.target_x = x
        self.target_y = y

    #adding a method to update the target's info
    def update_target_info(self, heading, velocity):
        self.target_heading = heading
        self.target_velocity = velocity

    def update(self, delta_time, elapsed_time):

        closest_dx = self.target_x - self.missile.x
        closest_dy = self.target_y - self.missile.y
        closest_dist = closest_dx**2 + closest_dy**2

        #tordial distance calculation
        #https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/
        #need to account for the wrapping around of the environment
        for x_offset in [-1000, 0, 1000]:
            for y_offset in [-1000, 0, 1000]:
                dx = (self.target_x + x_offset) - self.missile.x
                dy = (self.target_y + y_offset) - self.missile.y
                dist = dx**2 + dy**2
                if dist < closest_dist:
                    closest_dist = dist
                    closest_dx = dx
                    closest_dy = dy

        actual_dist = math.sqrt(closest_dist)

        #calculating a rough estimate on how long it will take the missile to get there
        #using the missile's current speed, but making sure not to divide by 0, if stationary
        missile_speed = self.missile.velocity
        if missile_speed < 1:
            missile_speed = 1 #using 1 as a minimum speed to prevent division
        #estimating the time to reach the target
        time_to_target = actual_dist / missile_speed
        #if for some reason we don't know the target's movement info, just aim directly
        if self.target_heading is None or self.target_velocity is None:
            predicted_dx = closest_dx
            predicted_dy = closest_dy
        else: #we know the target's info
            #using radians to calculate the predicted position
            target_rad = math.radians(self.target_heading)
            predicted_target_x = self.target_x + math.sin(target_rad) * self.target_velocity * time_to_target
            predicted_target_y = self.target_y - math.cos(target_rad) * self.target_velocity * time_to_target
            #the x and y are the predicted position using sin and cosing the angle with basic trigonometry
            #now doing the toroidal check again on the predicted position to see if its easier going a different route
            predicted_dx = predicted_target_x - self.missile.x
            predicted_dy = predicted_target_y - self.missile.y
            predicted_dist_squared = predicted_dx**2 + predicted_dy**2
            for x_offset in [-1000, 0, 1000]:
                for y_offset in [-1000, 0, 1000]:
                    dx = (predicted_target_x + x_offset) - self.missile.x
                    dy = (predicted_target_y + y_offset) - self.missile.y
                    dist_squared = dx**2 + dy**2
                    if dist_squared < predicted_dist_squared:
                        predicted_dist_squared = dist_squared
                        predicted_dx = dx
                        predicted_dy = dy

        #now we should have predicted dx and dy being the difference between the missile and the predicted jet position
        #now aiming at the predicted position instead of the actual position like direct_path
        #everything before this is to predict the target position
        target_angle = math.degrees(math.atan2(predicted_dx, -predicted_dy)) #@NOTE: taken from the simpleBot3 file from labs, changed to make 0 north

        #calculate the difference between the current heading and the target angle
        angle_diff = (target_angle - self.missile.get_heading() + 360) % 360
        if angle_diff > 180:
            angle_diff -= 360

        turn_strength = self.missile.get_turn_strength()

        if angle_diff > turn_strength:
            self.missile.turn_rate = min(turn_strength, angle_diff)
        else:
            self.missile.turn_rate = max(-turn_strength, angle_diff)
        
        #turn towards the target, by changing the misisle's turn rate to the negative or positive of its own turn rate depending on direction
        #self.missile.turn_rate = max(-self.missile.get_turn_rate(), min(self.missile.get_turn_strength(), angle_diff / self.missile.get_turn_strength()))

        
        #if fuel is not none, increase acceleration
        if self.missile.fuel > 0:
            self.missile.acceleration = self.missile.get_base_acceleration()
        else:
            #reduce the missiles speed with its drag until it reaches 0, at which point set it to explode
            if self.missile.velocity > 0:
                if self.missile.velocity < 1: #a  threshold to prevent the missile's velocity from getting smaller and smaller and never 0
                    self.missile.velocity = 0
                    self.missile.STATUS = "exploded"
                    self.missile.set_explosion_reason("fuel")

                else:
                    self.missile.velocity *= (1 - self.missile.drag * delta_time) #changing the missile's velocity based on its drag
            else:
                self.missile.acceleration = 0
                self.missile.velocity = 0
                self.missile.fuel = 0
                #potentially adding anti friendly-kill mechanism in the future @NOTE
                self.missile.STATUS = "exploded"
                self.missile.set_explosion_reason("fuel")

        return
    