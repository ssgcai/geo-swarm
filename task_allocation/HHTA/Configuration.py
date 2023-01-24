import multiprocessing as mp
from Agent import Agent
from Vertex import Vertex
from geo_utils import generate_local_mapping, get_coords_from_movement
from res_utils import *
from constants import INFLUENCE_RADIUS
import time

"""
Given a local vertex mapping, generate a proposed new vertex state and
new agent states and directions for each agent in that vertex

Parameters
local_vertex_mapping: dict
	mapping from local coordinates to the vertices at those coordiantes
"""
def delta(params):
	local_vertex_mapping, x, y = params
	print(x,y)
	vertex = local_vertex_mapping[(0,0)]

	if len(vertex.agents) == 0:
		return x, y, vertex.state, {}

	# Phase One: Each vertex uses their own transition function to propose a new
	# vertex state, agent state, and direction of motion
	proposed_vertex_states = {}
	proposed_agent_updates = {}

	for agent in vertex.agents:
		proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping)

		proposed_vertex_states[agent.state.id] = proposed_vertex_state
		proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)


	# Phase Two: Use a resolution rule to handle conflicting proposed vertex states
	new_vertex_state, new_agent_updates = naive_resolution(proposed_vertex_states, proposed_agent_updates)

	# Need x and y for setting the global state for parallel processing
	return x, y, new_vertex_state, new_agent_updates

class Configuration:
	"""
	Initialize the configuration

	Parameters
	agent_locations: list
		list of integers specifying what vertex to initialize each agent in
	N: int
		the height of the configuration
	M: int
		the width of the configuration
	torus: bool
		True if the grid is a torus, False if we are considering
		edge effects
	"""
	def __init__(self, N, M, torus=False, pool = None):
		# Create all vertices
		self.vertices = {}
		for x in range(M):
			for y in range(N):
				self.vertices[(x, y)] = Vertex(x,y)
		self.torus = torus
		self.N = N
		self.M = M
		self.influence_radius = INFLUENCE_RADIUS # make this a class variable later; radius 0 means only self is influenced
		self.agents = {} # map from id to agent itself
		self.pool = pool


	def add_agents(self, agent_locations):

		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, location)
			self.agents[agent_id] = agent
			location.agents.add(agent)

	def reset_agent_locations(self, agent_locations):
		for x in range(self.M):
			for y in range(self.N):
				self.vertices[(x, y)].agents = set()
		for agent_id in range(len(agent_locations)):
			agent = self.agents[agent_id]
			vertex = self.vertices[agent_locations[agent_id]]
			vertex.agents.add(agent)
			agent.location = vertex
	"""
	Generates a global transitory state for the entire configuration
	"""
	def generate_global_transitory(self):
		# Break down into local configurations and generate local transitory configurations for each to create global one
		global_transitory = {}

		for x in range(self.M):
			for y in range(self.N):

				#Get mapping from local coordinates to each neighboring vertex
				local_vertex_mapping = generate_local_mapping(self.vertices[(x,y)], self.influence_radius, self.vertices)

				global_transitory[(x,y)] = self.delta(local_vertex_mapping)

		return global_transitory

	"""
	Given a local vertex mapping, generate a proposed new vertex state and
	new agent states and directions for each agent in that vertex

	Parameters
	local_vertex_mapping: dict
		mapping from local coordinates to the vertices at those coordiantes
	"""
	def delta(self,local_vertex_mapping):
		vertex = local_vertex_mapping[(0,0)]

		if len(vertex.agents) == 0:
			return vertex.state, {}

		# Phase One: Each vertex uses their own transition function to propose a new
		# vertex state, agent state, and direction of motion
		proposed_vertex_states = {}
		proposed_agent_updates = {}

		for agent in vertex.agents:
			proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping)

			proposed_vertex_states[agent.state.id] = proposed_vertex_state
			proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)


		# Phase Two: Use a resolution rule to handle conflicting proposed vertex states
		new_vertex_state, new_agent_updates = task_claiming_resolution(proposed_vertex_states, proposed_agent_updates, vertex)
		return new_vertex_state, new_agent_updates

	"""
	Given the global transitory configuration, update the configuration to the new
	global state
	"""
	def execute_transition(self,global_transitory):
		for x,y in global_transitory.keys():
			vertex = self.vertices[(x,y)]
			new_vertex_state, new_agent_updates = global_transitory[(x,y)]

			# Update vertex state
			vertex.state = new_vertex_state

			# Update agents
			for agent_id in new_agent_updates:
				agent = self.agents[agent_id]
				update = new_agent_updates[agent_id]
				if update != None:
					# Update agent state
					agent.state = update.state

					# Update agent location
					movement_dir = update.direction

					# Erase agent from current location
					vertex.agents.remove(agent)

					# Move agent according to direction
					new_coords = get_coords_from_movement(vertex.x, vertex.y, movement_dir)
					agent.location = self.vertices[new_coords]

					# Add agent to updated location
					agent.location.agents.add(agent)

	"""
	Transition from the current global state into the next one
	"""
	def transition(self):
		global_transitory = self.generate_global_transitory()
		self.execute_transition(global_transitory)

	def all_agents_terminated(self):
		for agent_id in self.agents:
			if not self.agents[agent_id].terminated:
				return False
		return True
