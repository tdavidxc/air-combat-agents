import tkinter as tk
import math
import random

class Simulation:
    def initialise(window, width, height):
        print("Initialising simulation")
        window.resizable(False, False)
        canvas = tk.Canvas(window, width=width, height=height, bg='white')
        canvas.pack()
        return canvas