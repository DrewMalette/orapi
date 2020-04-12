# media/input, mechanics, file handling

# i'm moving into an era where i'm replacing if statements
#  with boolean multiplication (where possible)
# tl;dr i'm replacing conditionals with boolean based calculations

from .mob import base_update

class Scene:

	def __init__(self, uid, game, terrain=None):
	
		self.uid = uid
		self.game = game
		self.terrain = terrain
		
		self.mobs = {}
		self.live_mobs = {}
		
		self.buildings = {}
		self.furniture = {}
		self.loot = {}

	def add_mob(self, mob):
	
		self.mobs[mob.name] = mob
		
	def update(self):
	
		for mob in self.live_mobs.values():
			base_update(mob)
