# media/input, mechanics, file handling

# i'm moving into an era where i'm replacing if statements
#  with boolean multiplication (where possible)
# tl;dr i'm replacing conditionals with boolean based calculations
# create the object within the Game object?
# create a Dialogue box then access it?
# then they need uids again

from .mob import base_update

class Scene:

	def __init__(self, uid, game, terrain=None):
	
		self.uid = uid
		self.game = game
		self.terrain = terrain
		
		self.par_state = self.game.states["gameplay"]
		
		self.mobs = {}
		self.live_mobs = {}
		
		self.buildings = {}
		self.furniture = {}
		self.loot = {}
		
		#self.segment = ""
		#self.segments = {}
		self.segment = ""
		self.segments = {"ExpoDump": scene1_expo_dump, "Wait4Za": wait_for_pizza }

	def add_mob(self, mob):
	
		self.mobs[mob.name] = mob
		
	def update(self):
	
		#self.segments[self.segment](self)
	
		for mob in self.live_mobs.values():	base_update(mob)
			
# scene segments are functions and always pass scene as an argument
def scene1_expo_dump(scene): # "ExpoDump"

	scene.game.ui["Dialogue1"].update()
	scene.game.ui["Dialogue2"].update()
	scene.game.ui["Dialogue3"].update()
	scene.game.ui["PizzaSelect"].update()
	
	if scene.game.ui["Dialogue3"]._returned:
		# start pizza guy timer
		scene.segment = "Wait4Za"
		
	# TODO don't you have to blit some stuff at this point?
	# terrain_renderer.render()
		
def wait_for_pizza(scene):

	c = scene.game.controller
		
	move_mob(scene.game.player, 1 * c.x_axis, 1 * c.y_axis) # TODO show where move_mob comes from
	
	if c.exit == 1:	self.sub_state = "fade_out"; self.game.fader.fade_out()
		
	
