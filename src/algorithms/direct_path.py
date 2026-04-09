import tkinter as tk
import math
import random
import time


class DirectPath:
    def initialise(self, missile, target):
        self.missile = missile
        self.target = target
        self.target_x, self.target_y = None, None

    def update(self, delta_time, elapsed_time):
        #calculate the angle to the target
        self.target_x, self.target_y = self.target.get_position()

        dx = self.target_x - self.missile.x
        dy = self.target_y - self.missile.y
        target_angle = math.degrees(math.atan2(dy, dx)) #@NOTE: taken from the simpleBot3 file from labs

        #calculate the difference between the current heading and the target angle
        angle_diff = (target_angle - self.missile.get_heading() + 360) % 360
        if angle_diff > 180:
            angle_diff -= 360
        
        #turn towards the target, by changing the misisle's turn rate to the negative or positive of its own turn rate depending on direction
        if angle_diff > 0:
            self.missile.turn_rate = self.missile.get_turn_rate()
        else:
            self.missile.turn_rate = -self.missile.get_turn_rate()

        
        #if fuel is not none, increase acceleration
        if self.missile.fuel > 0:
            self.missile.acceleration = self.missile.get_acceleration()
        else:
            #reduce the missiles speed with its drag until it reaches 0, at which point set it to explode
            if self.missile.velocity > 0:
                if self.missile.velocity < 1: #a  threshold to prevent the missile's velocity from getting smaller and smaller and never 0
                    self.missile.velocity = 0
                    self.missile.STATUS = "exploded"

                else:
                    self.missile.velocity *= (1 - self.missile.drag * delta_time) #changing the missile's velocity based on its drag
            else:
                self.missile.acceleration = 0
                self.missile.velocity = 0
                self.missile.fuel = 0
                #potentially adding anti friendly-kill mechanism in the future @NOTE
                self.missile.STATUS = "exploded"

        return
    