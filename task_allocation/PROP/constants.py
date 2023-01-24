INFLUENCE_RADIUS = int(2)
TORUS = False

# Location Parameters
N = 50
M = 50

# Home Location
HOME_LOC = ((23, 25), (23, 25))

# Tasks and Agents
NUM_AGENTS = 100
K = 0.8
TOTAL_DEMAND = int(NUM_AGENTS*K)
EXPECTED_DEMAND_PER_TASK = 5
NUM_TASKS = 16
EXPECTED_DEMAND_PER_TASK = TOTAL_DEMAND/NUM_TASKS
assert(EXPECTED_DEMAND_PER_TASK >= 1)
assert(NUM_TASKS >= 1)

# General Constants
INF = 1000000000

#TAHH
L = 1/90

# Levy Flight Constants
levy_loc = 10
levy_cap = 1/L
