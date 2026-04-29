#The main file for the air combat agents.
import os
import tkinter as tk
from simulation.simulation import Simulation
from agents.jet import Jet
from agents.missile import Missile
from algorithms.datalink import Datalink
import time
import random

#Team based settings
SIMULATION_LENGTH = 30
SEED = 42

NUM_FRIENDLY_JETS = 3
NUM_MISSILES_PER_FRIENDLY_JET = 3
FRIENDLY_MISSILE_STRATEGY = "direct_path" #options: "direct_path", "predictive_path"
FRIENDLY_DATALINK = True

NUM_ENEMY_JETS = 3
NUM_MISSILES_PER_ENEMY_JET = 3
ENEMY_MISSILE_STRATEGY = "direct_path"
ENEMY_DATALINK = False




def make_jet(id, x, y, type):
    jet = Jet()
    #example jets
    jet.initialise(
        id,          #id
        x,          #x position
        y,          #y position [lower = higher on the screen]
        90, #starting heading
        150, #initial velocity
        0.0,        #acceleration (recommended for testing: 0.0 | good acceleration = 10.0)
        50,          #turn rate (recommended for testing: 50)
        type,  #type: "friendly" or "enemy"
        300,        #radar range (recommended for testing: 1500)
        120         #radar fov (recommended for testing: 360 [means full view])
    )
    return jet

def make_missile(id, jet, strategy):
    missile = Missile()
    missile.initialise(
        id,          #id
        10.0,          #acceleration (recommended for testing: 10.0)
        150,           #turn strength (recommended for testing: 50+, often 3x aircraft turn rate)
        65,           #explosion radius #for now the pixel size of the explosion png [2x pixel size because of resize] (recommended for testing: greater than detonation distance)
        50,           #detonation distance (recommended for testing: 50)
        0.0,          #fuel (recommended for testing: 5.0)
        1.0,          #fuel rate (recommended for testing: 1.0)
        strategy,            #targetting strategy [can be: "direct_path", "predictive_path"]
        "armed",     #status: "armed" or "fired"
        jet,          #jet that the missile is attached to
        jet.get_type(),    #type: "friendly" or "enemy"
        150,           #radar range (recommended for testing: 1500)
        60            #radar fov (recommended for testing: 360 [means full view])
    )
    return missile





#building the agents
def build_agents(friendly_datalink, enemy_datalink):
    agents = []
    agent_id = 0
    #creating datalinks if enabled
    

    #friendly jets and their missiles
    for _ in range(NUM_FRIENDLY_JETS):
        jet = make_jet(agent_id, random.randint(100, 900), random.randint(500, 900), "friendly")
        if FRIENDLY_DATALINK:
            jet.set_datalink(friendly_datalink)
        agents.append(jet)
        agent_id += 1
        for _ in range(NUM_MISSILES_PER_FRIENDLY_JET):
            missile = make_missile(agent_id, jet, FRIENDLY_MISSILE_STRATEGY)
            agents.append(missile)
            agent_id += 1

    #enemy jets and their missiles
    for _ in range(NUM_ENEMY_JETS):
        jet = make_jet(agent_id, random.randint(100, 900), random.randint(100, 499), "enemy")
        if ENEMY_DATALINK:
            jet.set_datalink(enemy_datalink)
        agents.append(jet)
        agent_id += 1
        for _ in range(NUM_MISSILES_PER_ENEMY_JET):
            missile = make_missile(agent_id, jet, ENEMY_MISSILE_STRATEGY)
            agents.append(missile)
            agent_id += 1

    

    return agents




#the simulation loop, this time handling in seconds instead of ticks
def run():
    #test the simulation by creating a window and canvas
    random.seed(SEED)
    simulation = Simulation()

    #datalink
    if FRIENDLY_DATALINK:
        friendly_datalink = Datalink("friendly")
    else:
        friendly_datalink = None
    if ENEMY_DATALINK:
        enemy_datalink = Datalink("enemy")
    else:
        enemy_datalink = None

    agents = build_agents(friendly_datalink, enemy_datalink)
    #creating the objects in the canvas
    simulation.run_with_display(agents, SIMULATION_LENGTH, friendly_datalink, enemy_datalink)

if __name__ == "__main__":
    #setting the working directory to the src folder
    os.chdir("C:\\Users\\tom24\\Documents\\University\\Yr3\\Designing Intelligent Agents\\Coursework\\air-combat-agents\\src")
    #select the simulation to run here
    run()