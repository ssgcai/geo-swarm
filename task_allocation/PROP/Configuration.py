from Agent import Agent
from constants import INFLUENCE_RADIUS
from geo_utils import generate_local_mapping, get_coords_from_movement
import multiprocessing as mp
from res_utils import *
import time
from Vertex import Vertex


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
	max_prop_rad: float
		maximum propagation radius (d_p), the maximum distance from a task at
		which information for that task can still be propagated
	prop_timeout: int
		integer propagation timeout (t_p), propagator agents can propagate task
		information to their influence radius every t_p rounds
	torus: bool
		True if the grid is a torus, False if we are considering
		edge effects
	"""
	def __init__(self, N, M, max_prop_rad, prop_timeout, torus=False):
		# Create all vertices
		self.vertices = {}
		for x in range(M):
			for y in range(N):
				self.vertices[(x, y)] = Vertex(x,y)  # map from coordinates to vertex itself
		self.N = N
		self.M = M
		self.max_prop_rad = max_prop_rad
		self.prop_timeout = prop_timeout
		self.torus = torus
		self.influence_radius = INFLUENCE_RADIUS
		self.agents = {}  # map from id to agent itself

	def add_agents(self, agent_locations, types):
		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, location, types[agent_id], config=self)
			self.agents[agent_id] = agent
			location.agents.add(agent)

	def reset_agent_locations(self, agent_locations, home_nest):
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
				# Get mapping from local coordinates to each neighboring vertex
				local_vertex_mapping = generate_local_mapping(self.vertices[(x,y)], self.influence_radius, self.vertices)
				new_vert_st, new_ag_up = self.delta(local_vertex_mapping)
				global_transitory[(x,y)] = new_vert_st, new_ag_up
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

		# Phase One: Each vertex uses their own transition function to propose a new vertex state, agent state, and direction of motion
		proposed_vertex_states = {}
		proposed_agent_updates = {}

		for agent in vertex.agents:
			proposed_vertex_state, proposed_agent_state, direction = agent.generate_transition(local_vertex_mapping)
			proposed_vertex_states[agent.state.id] = proposed_vertex_state
			proposed_agent_updates[agent.state.id] = AgentTransition(proposed_agent_state, direction)

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

					agent.state = update.state  # Update agent state

					movement_dir = update.direction  # Update agent location

					vertex.agents.remove(agent)  # Erase agent from current location

					# Move agent according to direction
					new_coords = get_coords_from_movement(vertex.x, vertex.y, movement_dir)
					agent.location = self.vertices[new_coords]

					agent.location.agents.add(agent)  # Add agent to updated location

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
