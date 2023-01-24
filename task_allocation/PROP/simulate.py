import numpy as np
import pandas as pd

graphics_on = True

import csv
from Configuration import Configuration
from constants import TORUS, N, M, NUM_AGENTS, NUM_TASKS, TOTAL_DEMAND, HOME_LOC
if graphics_on:
    import pygame
    from ViewController import ViewController
import multiprocessing as mp
from matplotlib import pyplot as plt
from random import randint
from VertexState import VertexState



def run(params, num_sims):
    N, M, NUM_TASKS, max_prop_rad, prop_timeout = params

    runtimes = []
    for _ in range(num_sims):
        configuration = Configuration(N, M, max_prop_rad, prop_timeout, TORUS)
        home = VertexState(is_home=True)

        for x in range(HOME_LOC[0][0], HOME_LOC[0][1]+1):
            for y in range(HOME_LOC[1][0], HOME_LOC[1][1]+1):
                configuration.vertices[(x,y)].state = VertexState(is_home=True)

        tasks = []
        task_locations = set()
        for i in range(NUM_TASKS):
            task_location = (randint(0,M-1), randint(0,N-1))
            while task_location in task_locations or configuration.vertices[task_location].state.is_home:
                task_location = (randint(0, M-1), randint(0, N-1))

            tasks.append(VertexState(is_task=True, demand=1, task_location=task_location))
            task_locations.add(task_location)

        for i in range(TOTAL_DEMAND-NUM_TASKS):
            task_num = randint(0, NUM_TASKS-1)
            tasks[task_num].demand += 1
            tasks[task_num].residual_demand += 1

        for task_state in tasks:
            configuration.vertices[task_state.task_location].state = task_state

        # Initialize agents
        agent_locations = []
        types = []
        for x in range(M):
            for y in range(N):
                agent_locations.append((x,y))
                types.append("Propagator")
        for i in range(NUM_AGENTS):
            agent_locations.append((randint(HOME_LOC[0][0], HOME_LOC[0][1]), randint(HOME_LOC[1][0], HOME_LOC[1][1])))
            types.append("Follower")

        configuration.add_agents(agent_locations, types)
        if graphics_on:
            vc = ViewController(configuration)
        ct = int(N/2 + M/2)  # Time at start for propagator agents to get to assigned vertex
        tot_rd = NUM_TASKS
        while tot_rd > 0:
            ct+=1
            configuration.transition()

            if graphics_on:
                vc.update()

            tot_rd = 0
            for task in tasks:
                tot_rd += task.residual_demand

        runtimes.append(ct)

        if graphics_on:
            vc.quit()


    return runtimes






if __name__ == "__main__":
    run([50,50,16,25,3], 1)
