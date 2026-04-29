#This is the datalink file where agents in the simulation can update what they see
#if two agents of the same team are in the same "datalink info" then they can see each other's info too

import math


class Datalink:
    def __init__(self, team_type):
        self.TYPE = team_type
        #a list of agents it sees in its radar
        self.known_enemies = {}

    def update(self, agents):
        #clear old info
        self.known_enemies = {}

        #go through every friendly jet and add what it can see to the shared pool
        for agent in agents:
            if agent.get_name() != "jet":
                continue
            if agent.get_type() != self.TYPE:
                continue

            #scan what the jet can see
            for other in agents:
                if other.get_type() == self.TYPE:
                    continue #skip friendly agents, only sharing info about enemies
                if other.get_name() == "missile" and other.STATUS == "armed":
                    continue #armed missiles should not be shared because they arent fired yet

                #check if this jet can see this enemy in its radar
                diff_x = other.get_position()[0] - agent.x
                diff_y = other.get_position()[1] - agent.y
                distance = math.sqrt(diff_x**2 + diff_y**2)
                angle_to_other = math.degrees(math.atan2(diff_x, diff_y)) % 360
                angle_diff = (angle_to_other - agent.get_heading() + 360) % 360

                in_range = distance <= agent.get_radar_range()
                in_fov = angle_diff <= agent.get_radar_fov() / 2 or angle_diff >= 360 - agent.get_radar_fov() / 2

                if in_range and in_fov:
                    #add this enemy to the shared pool
                    #we need to overwrite to know the latest position
                    self.known_enemies[other.get_id()] = {
                        "position" : other.get_position(),
                        "heading"  : other.get_heading(),
                        "velocity" : other.get_velocity(),
                        "name"     : other.get_name(),
                        "object"   : other, #reference object to it
                    }
                    
    def get_known_enemies(self):
        return self.known_enemies
    
    def get_known_enemy_jets(self):
        enemy_jets = {}
        for enemy_id, info in self.known_enemies.items():
            if info["name"] == "jet":
                enemy_jets[enemy_id] = info
        return enemy_jets
    
    def get_known_enemy_missiles(self):
        enemy_missiles = {}
        for enemy_id, info in self.known_enemies.items():
            if info["name"] == "missile":
                enemy_missiles[enemy_id] = info
        return enemy_missiles