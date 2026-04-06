import tkinter as tk
import math
import random


class DirectPath:
    def initialise(self, missile, target_x, target_y):
        self.missile = missile
        self.target_x = target_x
        self.target_y = target_y

    def update(self, delta_time):
        #calculate the angle to the target
        dx = self.target_x - self.missile.x
        dy = self.target_y - self.missile.y
        target_angle = math.degrees(math.atan2(dy, dx)) #@NOTE: taken from the simpleBot3 file from labs

        #calculate the difference between the current heading and the target angle
        angle_diff = (target_angle - self.missile.get_heading + 360) % 360
        if angle_diff > 180:
            angle_diff -= 360
        
        #turn towards the target, by changing the misisle's turn rate to the negative or positive of its own turn rate depending on direction
        if angle_diff > 0:
            self.missile.turn_rate = self.missile.get_turn_rate()
        else:
            self.missile.turn_rate = -self.missile.get_turn_rate()
        return