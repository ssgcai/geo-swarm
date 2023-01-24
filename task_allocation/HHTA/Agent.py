from AgentState import AgentState
from geo_utils import *
import random
from math import pi, floor
from constants import *
from scipy.stats import levy
import copy

class Agent:
	def __init__(self,agent_id, vertex, l=L):
		self.location = vertex
		self.state = AgentState(agent_id, vertex, l)

	def find_nearby_task(self,local_vertex_mapping):
		ret = None
		min_dist = 10000000000
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			if vertex.state.is_task and vertex.state.residual_demand > 0:
				this_dist = l2_distance(self.location.x, self.location.y, self.location.x+dx, self.location.y+dy)
				if  this_dist < min_dist:
					min_dist = this_dist
					ret = vertex.state
		return ret

	def find_nearby_tasks(self,local_vertex_mapping):
		nearby_tasks = []
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			if vertex.state.is_task and vertex.state.residual_demand > 0:
				nearby_tasks.append(vertex.state)
		return nearby_tasks

	def random_location_in_home(self):
		x_range = HOME_LOC[0]
		y_range = HOME_LOC[1]

		return (random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1]))

	def within_site(self, x, y, site):
		if site == None:
			x_range = (0, M-1)
			y_range = (0, N-1)
		elif site == "home":
			x_range = HOME_LOC[0]
			y_range = HOME_LOC[1]

		if x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]:
			return True
		return False


	def get_travel_direction(self, new_agent_state):
		if self.state.travel_distance == 0:
			new_agent_state.travel_distance = int(min(self.state.levy_cap, levy.rvs(loc=levy_loc))) #Twice the distance to the nest? maybe make this a variable
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)

		new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
		new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)

		bounding_site = None

		while not self.within_site(new_location[0], new_location[1], bounding_site):
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)
			new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
			new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)
		new_agent_state.travel_distance = new_agent_state.travel_distance-1
		return new_direction

	def get_task_info(self, local_vertex_mapping, new_agent_state):
		tasks = []
		for dx, dy in local_vertex_mapping.keys():
			agents = local_vertex_mapping[(dx, dy)].agents
			for agent in agents:
				if agent.state.core_state == "Task" and random.random() < self.state.message_rate:
					agent.state.message_count += 1
					tasks.append(agent.state.recruitment_task)
		if len(tasks) > 0:
			return random.choice(tasks)
		else:
			return None




	def generate_transition(self,local_vertex_mapping):
		s = self.state
		new_agent_state = copy.copy(s)

		if new_agent_state.core_state == "Home":
			# If just converted to home, returning home
			if s.home_destination is not None:
				new_direction = get_direction_from_destination(s.home_destination, (self.location.x, self.location.y))
				new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
				
				if self.within_site(new_location[0], new_location[1], "home"):
					new_agent_state.home_destination = None
					
				return self.location.state, new_agent_state, new_direction

			# Learn about new task
			if s.home_destination is None:
				task_state = copy.copy(self.get_task_info(local_vertex_mapping, new_agent_state))
				if task_state is not None:
					committed_chance = s.P_commit
					if random.random() < committed_chance:
						new_agent_state.core_state = "Committed"
						new_agent_state.destination_task = task_state
						return self.location.state, new_agent_state, "S"
					else:
						new_agent_state.core_state = "Task"
						new_agent_state.recruitment_task = task_state
						return self.location.state, new_agent_state, "S"


			# Chance of converting to exploring
			c = (1-s.P_explore)/(s.P_explore)
			if c != 0:
				explore_chance = s.L/c
			else:
				explore_chance = 1
			if random.random() < explore_chance:
				new_agent_state.core_state = "Exploring"
				return self.location.state, new_agent_state, "S"
			else:
				return self.location.state, new_agent_state, "S"


		elif new_agent_state.core_state == "Exploring":
			# Search for nearby tasks, has a chance of converting to committed
			nearby_tasks = self.find_nearby_tasks(local_vertex_mapping)
			if nearby_tasks != []:
				sum_rd = 0
				weights = []
				for task_state in nearby_tasks:
					sum_rd += task_state.residual_demand
					weights.append(task_state.residual_demand)
				for i in range(len(weights)):
					weights[i] /= sum_rd
				chosen_task = copy.copy(random.choices(population=nearby_tasks, weights=weights)[0])
				task_dist = l2_distance(chosen_task.task_location[0], chosen_task.task_location[1], 25, 25)
				committed_chance = max(s.P_commit, 1/chosen_task.residual_demand)
				if random.random() < committed_chance:
					new_agent_state.core_state = "Committed"
					new_agent_state.destination_task = chosen_task
					return self.location.state, new_agent_state, "S"
				else:
					new_agent_state.core_state = "Task"
					new_agent_state.home_destination = self.random_location_in_home()
					new_agent_state.recruitment_task = chosen_task
					return self.location.state, new_agent_state, "S"

			# Chance of converting to home
			home_chance = s.L 
			if random.random() < home_chance:
				new_agent_state.home_destination = self.random_location_in_home()
				new_agent_state.core_state = "Home"
				return self.location.state, new_agent_state, "S"

			# Keep random walking
			new_direction = self.get_travel_direction(new_agent_state)
			return self.location.state, new_agent_state, new_direction

		elif new_agent_state.core_state == "Task":
			if s.home_destination is not None:
				new_direction = get_direction_from_destination(s.home_destination, (self.location.x, self.location.y))
				new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
				
				if self.within_site(new_location[0], new_location[1], "home"):
					new_agent_state.home_destination = None
					
				return self.location.state, new_agent_state, new_direction

			committed_chance = 1/s.recruitment_task.residual_demand
			if random.random() < committed_chance:
				new_agent_state.core_state = "Committed"
				new_agent_state.destination_task = new_agent_state.recruitment_task
				new_agent_state.recruitment_task = None
				return self.location.state, new_agent_state, "S"

			return self.location.state, new_agent_state, "S"

		elif new_agent_state.core_state == "Committed":
			if s.destination_task is not None:
				if self.location.coords() == s.destination_task.task_location:
					if self.location.state.residual_demand == 0:
						home_chance = s.L 
						new_agent_state.destination_task = None
						new_agent_state.core_state = "Exploring"
						return self.location.state, new_agent_state, "S"
					new_agent_state.committed_task = s.destination_task
					new_agent_state.destination_task = None
					new_vertex_state = copy.copy(self.location.state)
					new_vertex_state.residual_demand = self.location.state.residual_demand-1
					return new_vertex_state, new_agent_state, "S"
				else:
					new_direction = get_direction_from_destination(s.destination_task.task_location, self.location.coords())
					return self.location.state, new_agent_state, new_direction 
			else:
				return self.location.state, new_agent_state, "S"




