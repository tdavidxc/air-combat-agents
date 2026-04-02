#The main file for the air combat agents.
import tkinter as tk
from simulation.simulation import Simulation

def test_simulation():
    #test the simulation by creating a window and canvas
    window = tk.Tk()
    canvas = Simulation.initialise(window, 1000, 1000)
    #test the creation of agents here
    #test the running of the simulation here
    window.mainloop()



if __name__ == "__main__":
    #select the simulation to run here
    test_simulation()