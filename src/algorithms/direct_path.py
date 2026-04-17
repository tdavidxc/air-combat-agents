import tkinter as tk
import math
import random
import time


class DirectPath:
    def initialise(self, missile, target_x, target_y):
        self.missile = missile
        self.target_x = target_x
        self.target_y = target_y

    def update_target_position(self, x, y):
        self.target_x = x
        self.target_y = y

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


        target_angle = math.degrees(math.atan2(closest_dx, -closest_dy)) #@NOTE: taken from the simpleBot3 file from labs, changed to make 0 north

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
    