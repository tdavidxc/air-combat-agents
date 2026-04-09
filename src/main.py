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
    simulation_length = 30 #length of simulation in seconds
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
    last_time = start_time = time.time()

    
    #TODO: TEMPORARY
    missile_fired = False
    

    #run the simulation for simulation_length seconds given in each simulation function
    def simulation_loop():
        nonlocal last_time, start_time, missile_fired #the nonlocal keyword allows the scope of the last_time to be accessed and modified within all nested functions like Jet

        now = time.time()
        delta_time = now - last_time #time since the last frame in seconds
        elapsed_time = now - start_time
        last_time = now


        #counting seconds in the simulation without multiple repetitive prints in the console, only print every second
        #@NOTE: every second condition
        if int(elapsed_time) % 1 == 0 and int(elapsed_time) != int(elapsed_time - delta_time):
            print("Elapsed time: " + str(int(elapsed_time)) + " seconds")
            

        #simulation stop condition
        if elapsed_time > simulation_length:
            print("Simulation ended after " + str(simulation_length) + " seconds.")
            return
        

        #test missile fire TEMPORARY
        if not missile_fired and elapsed_time > 5: #fire the missile after 5 seconds for testing
            missile1.STATUS = "fired"
            missile1.set_target(jet2) #setting the missile's target to the enemy jet for testing
            missile_fired = True
            print("Missile " + str(missile1.get_id()) + " fired at time: " + str(int(elapsed_time)) + " seconds, targeting Jet " + str(jet2.get_id()))

        for agent in agents:
            agent.move(delta_time, elapsed_time) #move the agent based on its own individual movement logic

        simulation.update_objects(canvas, agents)
        window.after(16, simulation_loop) #schedules the next frame after 16 milliseconds, which is approx. 60fps @NOTE: this code was taken from a tutorial on how to make game loops in tkinter


    window.after(16, simulation_loop)
    window.mainloop() #starting the tkinter main loop to display the window and canvas



if __name__ == "__main__":
    #setting the working directory to the src folder
    os.chdir("C:\\Users\\tom24\\Documents\\University\\Yr3\\Designing Intelligent Agents\\Coursework\\air-combat-agents\\src")
    #select the simulation to run here
    test_simulation()