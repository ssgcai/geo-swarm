from AgentState import AgentState
from constants import *
import copy
from geo_utils import *
from math import pi, floor
import random
from scipy.stats import levy


class Agent:
	def __init__(self,agent_id, vertex, type, data=None, config=None, l=L, msg_ct=0, prop_ctr=0):
		self.location = vertex
		self.config = config
		self.state = AgentState(agent_id, vertex, type, data, l, msg_ct, prop_ctr)


	# Look in influence radius for a task with nonzero residual demand
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

	def within_site(self, x, y):
		x_range = (0, M-1)
		y_range = (0, N-1)
		if x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]:
			return True
		return False

	# Get random travel direction (Levy random walk)
	def get_travel_direction(self, new_agent_state):
		if self.state.travel_distance == 0:
			new_agent_state.travel_distance = int(min(self.state.levy_cap, levy.rvs(loc=levy_loc)))
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)

		new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
		new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)

		while not self.within_site(new_location[0], new_location[1]):
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)
			new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
			new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)
		new_agent_state.travel_distance = new_agent_state.travel_distance-1
		return new_direction

	# Used by follower agents; looks at task_info of propagator agent at its vertex, chooses task to move towards with defined probabilities
	def choose_dir_from_propagator(self):
		for agent in self.location.agents:
			if agent.state.type == "Propagator" and sum([x[0] for x in agent.state.data.values()]) > 0:
				probs = []
				for x in list(agent.state.data.keys()):
					dem = agent.state.data[x][0]
					dist = l2_distance(x[0], x[1], self.location.coords()[0], self.location.coords()[1])
					if dist == 0 and dem > 0:
							return get_direction_from_destination(x, self.location.coords())
					elif dist == 0:
						probs.append(0)
					else:
						probs.append(dem / dist**2)
				task = random.choices(list(agent.state.data.keys()), weights=probs, k=1)
				return get_direction_from_destination(task[0], self.location.coords())
		return None

	# Used by propagator agents; share task/demand information (if it is new) with propagator agents in influence radius (1)
	def propagate(self, local_vertex_mapping, comm_buff, max_dist):
		ct = 0

		# Truncate influence radius 2 ('follower' agent) local_vertex_mapping to influence radius 1 ('propagator' agent)
		local_vertex_mapping.pop((0,0))
		to_remove = []
		for i in local_vertex_mapping:
			if abs(i[0]) > 1 or abs(i[1]) > 1:
				to_remove.append(i)
		for j in to_remove:
			local_vertex_mapping.pop(j)

		for v in list(local_vertex_mapping.values()):
			for agent in v.agents:
				if agent.state.type == "Propagator":  # access the propagator agent at each vertex
					ct_tmp = 0
					for t in self.state.data:  # loop through this (self) agent's task/demand data
						if self.state.data[t][1] > 0 and l2_distance(t[0], t[1], agent.location.coords()[0], agent.location.coords()[1]) <= max_dist:
							ct_tmp = 1
							if t not in list(agent.state.data.keys()):
								agent.state.data[t] = (self.state.data[t][0], 0)
							elif agent.state.data[t][0] > self.state.data[t][0]:
								agent.state.data[t] = (self.state.data[t][0], 0)
					ct += ct_tmp  # increment message count each time task_info shared with another agent

		if ct > 0:
			ages = []
			for t in self.state.data:
				ages.append(self.state.data[t][1])
			if min(ages) > comm_buff + 1:  # if this (self) agent already propagated this same exact task_info, do not need to again (no messages sent)
				ct = 0

		return ct


	# Calculate the single round/time step transition for this agent, returning the proposed new vertex state, new agent state, and direction to move
	def generate_transition(self,local_vertex_mapping):
		new_agent_state = copy.copy(self.state)
		if self.state.type == 'Follower':
			# Not headed towards task nor doing a task
			if self.state.committed_task is None and self.state.destination_task is None:
				nearby_task = self.find_nearby_task(local_vertex_mapping)
				if nearby_task is not None:  # If found task nearby, head towards it/do it
					new_agent_state.destination_task = nearby_task
					return self.location.state, new_agent_state, "S"
				else:  # Otherwise, move w prob based on propagator info; if no info at vertex, random walk
					new_direction = self.choose_dir_from_propagator()
					if new_direction is None:
						new_direction = self.get_travel_direction(new_agent_state)
					else:
						new_agent_state.msg_ct += 1  # Had to look at task_info of propagator agent, increment interagent message count
					return self.location.state, new_agent_state, new_direction
			elif self.state.destination_task is not None:  # Headed towards task
				if self.state.destination_task.residual_demand == 0:
					new_agent_state.destination_task = None
					return self.location.state, new_agent_state, "S"
				if self.location.coords() == self.state.destination_task.task_location:  # Arrived at task
					new_agent_state.committed_task = self.state.destination_task
					new_agent_state.destination_task = None
					new_vertex_state = copy.copy(self.location.state)
					new_vertex_state.residual_demand -= 1
					return new_vertex_state, new_agent_state, "S"
				else:  # Still moving towards task
					new_direction = get_direction_from_destination(self.state.destination_task.task_location, self.location.coords())
					new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
					return self.location.state, new_agent_state, new_direction
			else:  # Committed to doing a task, so stay still
				return self.location.state, self.state, "S"
		else:  # type = 'Propagator'
			if self.location.state.is_task:  # if propagator agent on task, get the residual demand
				if self.location.coords() not in self.state.data:
					self.state.data[self.location.coords()] = (self.location.state.residual_demand, 0)
				elif self.state.data[self.location.coords()][0] > self.location.state.residual_demand:
					self.state.data[self.location.coords()] = (self.location.state.residual_demand, 0)

				new_agent_state.prop_ctr += 1
				if new_agent_state.prop_ctr >= self.config.prop_timeout:  # can propagate every prop_timeout rounds
					new_agent_state.msg_ct += self.propagate(local_vertex_mapping, self.config.prop_timeout, self.config.max_prop_rad)
					new_agent_state.prop_ctr = 0
			else:  # otherwise pass your task/demand data to your influence radius
				new_agent_state.prop_ctr += 1
				if new_agent_state.prop_ctr >= self.config.prop_timeout:  # can propagate every prop_timeout rounds
					new_agent_state.msg_ct += self.propagate(local_vertex_mapping, self.config.prop_timeout, self.config.max_prop_rad)
					new_agent_state.prop_ctr = 0
			for t in self.state.data:
				self.state.data[t] = (self.state.data[t][0], self.state.data[t][1] + 1)  # all data points at self have now sat for at least one round
			return self.location.state, new_agent_state, "S"
