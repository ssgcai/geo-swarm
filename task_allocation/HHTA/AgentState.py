import random
from constants import L, P_commit, P_explore, message_rate

class AgentState:
	# Home, Exploring, Recruiting, Committed
	core_states = ["Home", "Exploring", "Recruiting", "Committed"]

	def __init__(self, agent_id, vertex, l=L, p_commit = P_commit, p_explore=P_explore, message_rate=message_rate):
		self.reset(agent_id, vertex, l, p_commit, p_explore, message_rate)

	def reset(self, agent_id, vertex, l, p_commit, p_explore, message_rate):
		# Initial Parameters
		if random.random() < p_explore:
			self.core_state = "Exploring"
		else:
			self.core_state = "Home"
		self.id = agent_id
		self.L = l
		self.P_commit = p_commit
		self.P_explore = p_explore
		self.message_rate = message_rate

		#Random Walk Parameters
		self.angle = 0
		self.starting_point = (vertex.x, vertex.y)
		self.travel_distance = 0
		self.levy_cap = 1/l

		#Destination Travel Parameters
		self.destination_task = None
		self.home_destination = None

		#Recruitment
		self.recruitment_task = None

		#Commitment
		self.committed_task = None

		#Count messaging
		self.message_count = 0
