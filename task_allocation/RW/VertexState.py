class VertexState:

	def __init__(self, is_task=False, demand=None, task_location=None, is_home = False):
		self.is_task = is_task
		self.is_home = is_home
		self.demand = demand
		self.residual_demand = demand
		self.task_location = task_location
