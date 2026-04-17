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
        700,        #y position [lower = higher on the screen]
        90,         #heading
        50,          #velocity (recommended for testing: 50)
        0.0,        #acceleration (recommended for testing: 0.0 | good acceleration = 10.0)
        50,          #turn rate (recommended for testing: 50)
        "friendly",  #type
        200,        #radar range (recommended for testing: 400)
        360         #radar fov (recommended for testing: 360 [means full view])
    )

    jet2 = Jet()
    jet2.initialise(
        2,
        700,
        200,
        270,
        50,
        0.0,
        50,
        "enemy",
        400,
        360
    )

    jet3 = Jet()
    jet3.initialise(
        3,
        200,
        100,
        90,
        50,
        0.0,
        50,
        "enemy",
        400,
        360
    )

    missile1 = Missile()
    missile1.initialise(
        4,          #id
        10.0,      #acceleration (recommended for testing: 10.0)
        150,          #turn strength (recommended for testing: 50+, often 3x aircraft turn rate)
        65,           #explosion radius #for now the pixel size of the explosion png [2x pixel size because of resize] (recommended for testing: greater than detonation distance)
        50,           #detonation distance (recommended for testing: 50)
        5.0,          #fuel (recommended for testing: 5.0)
        1.0,          #fuel rate (recommended for testing: 1.0)
    "direct_path",            #targetting strategy
        "armed",     #status
        jet1,          #jet that the missile is attached to
        "friendly",    #type
        1000,           #radar range (recommended for testing: 400)
        360            #radar fov (recommended for testing: 360 [means full view])
    )

    missile2 = Missile()
    missile2.initialise(
        5,
        10.0,
        150,
        65,
        50,
        5.0,
        1.0,
        "direct_path",
        "armed",
        jet1,
        "friendly",
        400,
        360
    )

    #creating the objects in the canvas
    simulation.create_objects(canvas, [jet1, jet2, jet3, missile1, missile2])
    agents = [jet1, jet2, jet3, missile1, missile2]


    #test the running of the simulation here
    last_time = start_time = time.time()

    
    #TODO: TEMPORARY
    missile1_fired = False
    missile2_fired = False
    


    def after_simulation(log):
        #if simulation log isnt empty, print it
        if log:
            print("Simulation log: \n")
            for entry in log:
                print(entry)
        else:
            print("Simulation log is empty")

    #run the simulation for simulation_length seconds given in each simulation function
    def simulation_loop():
        nonlocal last_time, start_time, missile1_fired, missile2_fired #the nonlocal keyword allows the scope of the last_time to be accessed and modified within all nested functions like Jet

        now = time.time()
        delta_time = now - last_time #time since the last frame in seconds
        elapsed_time = now - start_time
        last_time = now


        #counting seconds in the simulation without multiple repetitive prints in the console, only print every second
        #@NOTE: every second condition
        if int(elapsed_time) % 1 == 0 and int(elapsed_time) != int(elapsed_time - delta_time):
            simulation.set_elapsed_time(elapsed_time)
            print("Elapsed time: " + str(int(elapsed_time)) + " seconds")
            if(missile1 in agents):
                print("--- Missile 1 angle:", missile1.heading, "degrees --- turn rate: ", missile1.turn_rate, "degrees/second", "position: ", missile1.get_position(), " whos radar: ", missile1.get_whos_radar(), " distance to target: ", simulation.get_object_distance(missile1, missile1.target))
            if(missile2 in agents):
                print("--- Missile 2 angle:", missile2.heading, "degrees --- turn rate: ", missile2.turn_rate, "degrees/second", "position: ", missile2.get_position(), " whos radar: ", missile2.get_whos_radar(), " distance to target: ", simulation.get_object_distance(missile2, missile2.target))
            if(jet2 in agents):
                print("--- Enemy jet (jet2) position: ", jet2.get_position(), "heading: ", jet2.heading, "degrees ---")
            if(jet3 in agents):
                print("--- Enemy jet (jet3) position: ", jet3.get_position(), "heading: ", jet3.heading, "degrees ---")

        #simulation stop condition
        if elapsed_time > simulation_length:
            print("Simulation ended after " + str(simulation_length) + " seconds.")
            after_simulation(simulation.get_log()) #print the log of the simulation after it ends
            return
        

        #test missile fire TEMPORARY
        #NOTE temporary
        if not missile1_fired and elapsed_time > 5: #fire the missile after 5 seconds for testing
            missile1.STATUS = "fired"
            missile1.set_target(jet2) #setting the missile's target to the enemy jet for testing
            missile1_fired = True
            simulation.add_log("Missile " + str(missile1.get_id()) + " fired at time: " + str(int(elapsed_time)) + " seconds, targeting Jet " + str(jet2.get_id()))
        if not missile2_fired and elapsed_time > 10: #fire the missile after 10 seconds for testing
            missile2.STATUS = "fired"
            missile2.set_target(jet3) #setting the missile's target to the enemy jet for testing
            missile2.set_target_position(jet3.get_position()) #setting the missile's target position to the enemy jet's position for testing, this is needed because the direct path algorithm needs a target position to work with, and currently the missile only updates its target position when its fired, so we need to set it here for testing
            missile2_fired = True
            simulation.add_log("Missile " + str(missile2.get_id()) + " fired at time: " + str(int(elapsed_time)) + " seconds, targeting Jet " + str(jet3.get_id()))




        #agent loops

        #updating jets radars first
        for agent in list(agents):
            if agent.get_name() == "jet":
                agent.update_targeting(agents)

        #all missiles ask their jet for the target position
        for agent in list(agents):
            if agent.get_name() == "missile" and agent.STATUS == "fired":
                agent.update_target_position(agents)

        #everyone moves
        for agent in list(agents): #after testing, i found that looping over a copy of agents is needed because im removing the agents from the original list before I need them
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