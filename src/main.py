#The main file for the air combat agents.
import os
import tkinter as tk
from simulation.simulation import Simulation
from agents.jet import Jet
from agents.missile import Missile
import time

def test_simulation():
    #test the simulation by creating a window and canvas
    simulation = Simulation()
    window = tk.Tk()
    canvas = simulation.initialise(window, 1000, 1000)
    #test the creation of agents here
    #standard jet test
    jet1 = Jet()
    #example jets
    jet1.initialise(
        1,          #id
        500,        #x position
        500,        #y position
        90,         #heading
        50,          #velocity (recommended for testing: 50)
        0.0,        #acceleration (recommended for testing: 0.0 | good acceleration = 10.0)
        50,          #turn rate (recommended for testing: 50)
        "friendly"  #type
    )

    jet2 = Jet()
    jet2.initialise(
        2,
        300,
        700,
        270,
        50,
        0.0,
        50,
        "enemy"
    )

    missile1 = Missile()
    missile1.initialise(
        3,          #id
        10.0,      #acceleration (recommended for testing: 10.0)
        0,          #turn rate (recommended for testing: 100)
        50,           #explosion radius
        30,           #detonation distance
        5.0,          #fuel (recommended for testing: 5.0)
        1.0,          #fuel rate (recommended for testing: 1.0)
    "direct_path",            #targetting strategy
        "armed",     #status
        jet1,          #jet that the missile is attached to
        "friendly"    #type
    )

    #creating the objects in the canvas
    simulation.create_objects(canvas, [jet1, jet2, missile1])
    agents = [jet1, jet2, missile1]


    #test the running of the simulation here
    last_time = time.time()

    def simulation_loop():
        nonlocal last_time #the nonlocal keyword allows the scope of the last_time to be accessed and modified within all nested functions like Jet
        now = time.time()
        delta_time = now - last_time #time since the last frame in seconds
        last_time = now

        for agent in agents:
            agent.move(delta_time) #move the agent based on its own individual movement logic

        simulation.update_objects(canvas, agents)
        window.after(16, simulation_loop) #schedules the next frame after 16 milliseconds, which is approx. 60fps @NOTE: this code was taken from a tutorial on how to make game loops in tkinter


    window.after(16, simulation_loop)
    window.mainloop() #starting the tkinter main loop to display the window and canvas



if __name__ == "__main__":
    #setting the working directory to the src folder
    os.chdir("C:\\Users\\tom24\\Documents\\University\\Yr3\\Designing Intelligent Agents\\Coursework\\air-combat-agents\\src")
    #select the simulation to run here
    test_simulation()