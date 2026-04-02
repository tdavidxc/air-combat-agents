# air-combat-agents

Simulation of autonomous missile agents intercepting aircraft using AI strategies such as A* search, predictive targeting and cooperative behaviour.


Main.py (Entry Point)

- where experiments are run, not the actual simulation logic
- defines the research question
- Can loop over different configurations/algorithms etc.
- Collect performance metrics and outputs results

Simulation.py (Core Loop)

- The actual process/engine of the system
- runs the simulation step by step
- Updates the agents
- Handles interactions
- Almost like the "controller"
- The world model
- Handles the states of the environment
- Stores all entities/jets/environment details
- Provides the information about the state to the agents
- Handles physics basics

  - positions, velocities, distance calculations, sensor simulation, noise/errors etc.

direct_path.py (Algorithm)

- One specific targetting strategy to start off
- Given the missile state and target state
- Returns direction / acceleration / action etc.

missile.py (Agent)

- Stores internal states of the missile agent / characteristics
  - position, velocity
  - fuel
  - sensor ranges
- Calls algorithms like direct_path.py
- Actions include movement and detonation

jet.py (Agent)

- Involves friendly + enemy aircraft
- movement behaviour which can be scrupted randomly or intelligent to be evasive
- States include position, velocity, type (enemy/friendly)
-
