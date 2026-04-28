# This file handles running experiments and collecting results.
# Run this file directly to open the simulation configuration UI.
# Location: air-combat-agents/experiments/experimenter.py

import sys
import os
import random
from src.simulation.simulation import Simulation
from src.agents.jet import Jet
from src.agents.missile import Missile


# the src folder needs to be on the path so imports inside missile.py, jet.py etc. work correctly
# experimenter.py lives in experiments/, src/ is one level up then into src/
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import csv
from datetime import datetime


#results folder
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

#Experimenter settings that need to be set before running the experimetn
NUM_RUNS = 10
TICKS_PER_SIM = 3000 #how many ticks each sim runs for (recommended: )
DELTA_TIME = 0.016 #1/60 = 0.016 to simulate 60 "frames" per second if needed
SEED = 42 #not needed right now, but when needed for randomness and reproducibility

#friendly team
F_NUM_JETS = 1
F_NUM_MISSILES_PER_JET = 5
F_STRATEGY = "direct_path" #options: "direct_path", "predictive_path"
F_DATALINK = False #Not implemented yet
#enemy team
E_NUM_JETS = 3
E_NUM_MISSILES_PER_JET = 5
E_STRATEGY = "predictive_path"
E_DATALINK = False #Not implemented yet

#builds the actual agents based on the above settings from the individual object classes
#change the individual agent characteristics here as needed
def build_agents(self, seed, f_num_jets, f_num_missiles, f_strategy, f_datalink,
                                e_num_jets, e_num_missiles, e_strategy, e_datalink):


    random.seed(seed)
    agents   = []
    agent_id = 1

    # ── friendly jets ──────────────────────────────────────────────────────
    friendly_jets = []
    for _ in range(f_num_jets): #looping through the number of jets without actually having a pointer
        jet = Jet()
        jet.initialise(
            agent_id,
            x            = random.randint(100, 900),
            y            = random.randint(500, 900),  # bottom half = friendly territory
            heading      = random.randint(0, 359),
            velocity     = 50,
            acceleration = 0.0,
            turn_rate    = 50,
            type         = "friendly",
            radar_range  = 1500,  # large enough to always detect across the map
            radar_fov    = 360,
        )
        friendly_jets.append(jet)
        agents.append(jet)
        agent_id += 1

    # ── enemy jets ─────────────────────────────────────────────────────────
    enemy_jets = []
    for _ in range(e_num_jets):
        jet = Jet()
        jet.initialise(
            agent_id,
            x            = random.randint(100, 900),
            y            = random.randint(100, 499),  # top half = enemy territory
            heading      = random.randint(0, 359),
            velocity     = 50,
            acceleration = 0.0,
            turn_rate    = 50,
            type         = "enemy",
            radar_range  = 1500,
            radar_fov    = 360,
        )
        enemy_jets.append(jet)
        agents.append(jet)
        agent_id += 1

    # ── friendly missiles (armed and attached to their jet) ────────────────
    for jet in friendly_jets:
        for _ in range(f_num_missiles):
            missile = Missile()
            missile.initialise(
                agent_id,
                acceleration        = 10.0,
                turn_strength       = 150,
                explosion_radius    = 65,
                detonation_distance = 50,
                fuel                = 10.0,
                fuel_rate           = 1.0,
                targetting_strategy = f_strategy,
                status              = "armed",
                jet                 = jet,
                type                = "friendly",
                radar_range         = 1500,
                radar_fov           = 360,
            )
            agents.append(missile)
            agent_id += 1

    # ── enemy missiles ─────────────────────────────────────────────────────
    for jet in enemy_jets:
        for _ in range(e_num_missiles):
            missile = Missile()
            missile.initialise(
                agent_id,
                acceleration        = 10.0,
                turn_strength       = 150,
                explosion_radius    = 65,
                detonation_distance = 50,
                fuel                = 10.0,
                fuel_rate           = 1.0,
                targetting_strategy = e_strategy,
                status              = "armed",
                jet                 = jet,
                type                = "enemy",
                radar_range         = 1500,
                radar_fov           = 360,
            )
            agents.append(missile)
            agent_id += 1

    return agents


#What gets called to do a single experiment (useful for doing multiple)
def run_single_simulation(self, agents, ticks, delta_time):
    sim = Simulation()
    #running a "Headless" sim which doesnt show the tkinter application
    results = sim.run_headless(agents, ticks, delta_time)
    return results


#saving the results to the csv
def save_results(self, all_results, f_strategy, e_strategy):
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"results_{f_strategy}_vs_{e_strategy}_{timestamp}.csv"
    filepath  = os.path.join(RESULTS_FOLDER, filename)
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
            writer.writeheader()
            writer.writerows(all_results)
        self.log(f"> Saved: {filepath}")
    except Exception as e:
        self.log(f"> [ERROR] Could not save: {e}")



def main():
    print("______________________________")
    print("Starting Experiment")
    print("Experiment Number:"+ str(1))
    print("Friendly Settings: " + str(F_NUM_JETS) + " jets, " + str(F_NUM_MISSILES_PER_JET) + " missiles per jet, " + str(F_STRATEGY) + " strategy, datalink: " + str(F_DATALINK))
    print("Enemy Settings: " + str(E_NUM_JETS) + " jets, " + str(E_NUM_MISSILES_PER_JET) + " missiles per jet, " + str(E_STRATEGY) + " strategy, datalink: " + str(E_DATALINK))
    print("Total runs: " + str(NUM_RUNS))
    print("Ticks per sim: " + str(TICKS_PER_SIM))
    print("______________________________")

    total_results = []
    
    for i in range(NUM_RUNS):
        print("Simulation " + str(i+1) + "/" + str(NUM_RUNS))
        
        #using a different seed for each run, but based on the initial seed so they arent the same
        agents = build_agents(SEED + i, F_NUM_JETS, F_NUM_MISSILES_PER_JET, F_STRATEGY, F_DATALINK,
                                    E_NUM_JETS, E_NUM_MISSILES_PER_JET, E_STRATEGY, E_DATALINK
        )
        results = run_single_simulation(agents, TICKS_PER_SIM, DELTA_TIME)
        results["run_index"] = i + 1
        total_results.append(results)

        print(f"  interceptions    : {results['interceptions']}")
        print(f"  friendly fire    : {results['friendly_fire_incidents']}")
        print(f"  interception rate: {results['interception_rate_pct']}%")
        print(f"  avg intercept t  : {results['avg_interception_time_s']}s")
        print(f"  fuel outs        : {results['missiles_out_of_fuel']}")

    #averages across all runs
    n = len(total_results)
    def avg(key):
        return round(sum(r[key] for r in total_results) / n, 2)

    print("\n" + "=" * 50)
    print(f"DONE - {n} run(s) completed")
    print(f"  Avg interceptions : {avg('interceptions')}")
    print(f"  Avg friendly fire : {avg('friendly_fire_incidents')}")
    print(f"  Avg intercept rate: {avg('interception_rate_pct')}%")
    print(f"  Avg intercept time: {avg('avg_interception_time_s')}s")
    print(f"  Avg fuel outs     : {avg('missiles_out_of_fuel')}")
    print("=" * 50)

    save_results(total_results, F_STRATEGY, E_STRATEGY)
        

if __name__ == "__main__":
    main()