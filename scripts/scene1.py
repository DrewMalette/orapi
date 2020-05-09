import sys
sys.path.append("../")
from orapi import move_mob

# scene segments are functions and always pass scene as an argument
def scene1_expo_dump(scene): # "ExpoDump"

	#if scene.game.ui["dialoguebox"]._returned: scene.segment = "Wait4Za"
	# start pizza guy timer
	#scene.segment = "Wait4Za"
	
	c = scene.game.controller			
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
		
	scene.game.ui["dialoguebox"].update()
		
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()
		
def wait_for_pizza(scene):

	c = scene.game.controller		
	move_mob(scene.game.player, 1 * c.x_axis, 1 * c.y_axis) # TODO show where move_mob comes from
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
	
	scene.game.terrain_renderer.update()	
	
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()

_locals = locals()

