#I will try to implement a q-learning algorithm from Reinforcement Learning lecture, slide 41
#it will use bucketing to make the continuous state space more discrete
#and make decisions for individual jets on when to fire their missiles
#based off 3 states: distance from target, whether it has fired, and whether there are any incoming missiles
#3 states should not take too long to train and with correct training and tuning, should be able to avoid some edge cases which might lead to poor policy decisions

#Adapted from: https://github.com/ElliotVilhelm/QLearning -> they have MIT license
# Original Q-learning algorithm: Watkins, C.J.C.H. (1989)
# I had no clue how to implement this from scratch, so helpful tutorials and guides were used
# and from courseworks from ML and HAI interaction modules from previous semesters
# Links to those can be given on request

import random
import json
import os
import math


#Hyperparameters
GAMMA = 0.99
NUM_STATES = 18 #3 for distance, 3 for missiles already in flight (0, 1-2, 3+), 2 for incoming missiles, 2*3*3 = 18
NUM_ACTIONS = 2 #fire or not fire (0 for not fire, 1 for fire)
MIN_EXPLORE_RATE = 0.01 #this is done to never stop fully exploring
MIN_LEARNING_RATE = 0.05


class QLearner:

    def __init__(self):
        #initialising the q table which is number of states x number of actions to all 0s
        #each row is a state and each column is an action to fire
        #using a dictionary to store the q table

        self.q_table = {}
        for state in range(NUM_STATES):
            self.q_table[state] = [0.0, 0.0] #hold_value, fire_value

        self.episode = 0 #each run is an episode so this is a tracker to keep track of that


    #a method to get the current state of the environment, given all the info
    #this method replaces get_box() from the q learning code in the repo, adapted to work for mine
    def get_state(self, distance_to_target, missiles_in_flight, threat_level):
        #the first feature
        if distance_to_target < 200:
            state = 0 #the jet is close to the target
        elif distance_to_target < 500:
            state = 1 #the jet is at a middle distance from target
        else:
            state = 2 #the jet is far

        #the second feature
        if missiles_in_flight == 0:
            state += 0 #no missiles in the air from the jet
        elif missiles_in_flight <= 2:
            state += 3 #1 or 2 missiles in the air
        else:
            state += 6 #3 or more missiles in the air

        #the third feature
        if not threat_level:
            state += 0 #the jet is safe
        else:
            state += 9 #the jet is threatened

        return state

    

    #a method to get the exploration rate which starts high and "decays" over time
    #this method is adapted from update_explode_rate() in ElliotVilhelm's code in the repo mentioned at the top
    def get_explore_rate(self):
        #@TODO


    #a method to get the learning rate which also decays over time
    def get_learning_rate(self):
        #@TODO


    
    #a method to choose an action based on the current state and the q table
    #this is the epsilon-greedy action selection from the lecture
    def choose_action(self, state):
        #@TODO



    #a method to update the q table based on the action taken and the reward received
    #this follows the bellman equation in slide 42 of reinforcementLearning.pwpt
    def update(self, state, action, reward, next_state):
        #@TODO



    #adding a helper method to increment the episode/run count
    def increment_episode(self):
        self.episode += 1

    

    #q table handling methods
    #a method to save and load the q table with json
    def save(self, filepath):
        #@TODO


    def load(self, filepath):
        #@TODO


    

    #method to evaluate the current q table values during evalation
    #(no exploration, just exploitation)
    def get_best_action(self, state):
        #@TODO



    
    #method to print the q table if needed
    def print_q_table(self):
        #@TODO