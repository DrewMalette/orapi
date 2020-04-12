import xml.etree.ElementTree as ET

import pygame

from . import sprite
from . import utilities

class Tileset:

	def __init__(self, width, height):
	
		self.width = height
		self.height = height
					
		self.textures = {}
		
	def update(self, filename, firstgid=1):
	
		textures = load_tileset(filename, self.width, self.height, firstgid)
		self.textures.update(textures)
				
	def __getitem__(self, key=-1):
	
		if key is -1:
			return self.textures
		if key is not -1:
			return self.textures[key]
			
class Terrain(object):

	def __init__(self, filename, engine, scene):

		self.uid = filename
		self.engine = engine
		#self.renderer = self.engine.scene_painter
		self.scene = scene

		tree = ET.parse(self.uid)
		root = tree.getroot()
		
		self.cols = int(root.attrib["width"])
		self.rows = int(root.attrib["height"])
		
		self.tilewidth = int(root.attrib["tilewidth"])
		self.tileheight = int(root.attrib["tileheight"])
		self.tilesize = self.tilewidth # assumes a square tile
		
		self.tileset = Tileset(self.tilewidth, self.tileheight)
		
		self.loot = {}
		self.loot_count = 0
		
		self.layerdata = { "bottom": None,
				           "middle": None,
					  	   "top": None,
					  	   "collide": None
						 }

		self.switches = {}
		self.sprites = {}
		
		for tilesettag in root.iter("tileset"):
			filename = tilesettag.attrib["source"]
			tilestree = ET.parse("content/image/" + filename)
			tilesroot = tilestree.getroot()
			for tileset in tilesroot.iter("tileset"):
				for i in tileset.iter("image"):
					filename = "content/image/" + i.attrib["source"]
					firstgid = tilesettag.attrib["firstgid"]
					self.tileset.update(filename, firstgid) # ummmmmmm....?
					
		for layer in root.iter("layer"):
			for data in layer.iter("data"):
				name = layer.attrib['name']
				rawdata = data.text.split(",")
				cleandata = []
				for tile in rawdata:
					cleandata.append(tile.strip())
				self.layerdata[name] = cleandata
				
		for layer in root.iter("objectgroup"):
			for rect in layer.iter("object"):
				rectattribs = {}
				for v in rect.attrib.keys():
					rectattribs[v] = rect.attrib[v]
				for proptag in rect.iter("properties"):
					for propchild in proptag.iter("property"):
						index = propchild.attrib["name"]
						value = propchild.attrib["value"]
						rectattribs[index] = value
				
				uid = rectattribs["id"]
				col = int(float(rectattribs["x"]) / self.tilewidth)
				row = int(float(rectattribs["y"]) / self.tileheight)
				if rectattribs["type"] == "player":
					if self.engine.player_character is None: # move this to engine
						print("player object is not defined")
						print("exiting")
						pygame.quit()
						exit()
					self.sprites["player"] = self.engine.player_character
					self.sprites["player"].scene = self
					self.sprites["player"].place(col,row)
				elif rectattribs["type"] == "switch":
					x = int(float(rectattribs["x"]) / self.tilewidth) * self.tilewidth
					y = int(float(rectattribs["y"]) / self.tileheight) * self.tileheight
					facing = rectattribs["facing"]
					try:
						c = int(rectattribs["col"])
						r = int(rectattribs["row"])
						self.switches[uid] = [pygame.Rect((x,y,self.tilewidth,self.tileheight)), rectattribs["Filename"], (c,r), facing]
					except:
						#print("defaulting to map defined placement position")
						self.switches[uid] = [pygame.Rect((x,y,self.tilewidth,self.tileheight)), rectattribs["Filename"], None, facing]
				elif rectattribs["type"] == "mob":
					self.sprites[uid] = sprite.Mob("content/image/" + rectattribs["Filename"], rectattribs["name"])
					self.sprites[uid].scene = self
					self.sprites[uid].place(col,row)
				elif rectattribs["type"] == "static":
					filepath = "content/image/" + rectattribs["Filename"]
					name = rectattribs["name"]
					self.sprites[uid] = sprite.Static(filepath, name)
					self.sprites[uid].scene = self
					self.sprites[uid].place(col,row)

	def get_tile(self, layername, col, row):
	
		index = int((row % self.rows) * self.cols + (col % self.cols))
		return self.layerdata[layername][index]
		
	def add_loot(self, filename, x, y):
	
		uid = self.loot_count
		px = x
		py = y - 20
		self.loot[self.loot_count] = sprite.Loot(self, uid, filename, (px,py))
		self.loot_count = (self.loot_count + 1) % 256
		
	def update(self):
	
		for sprite in self.sprites.values():
			sprite.update()
			
		for loot in self.loot.values():
			loot.update()
		
		# TODO put this in player
		for switch in self.switches.values():
			rect = switch[0]
			filename = switch[1]
			if self.engine.player_character.colliderect(rect):
				self.engine.active_state.switch_scene("content/image/"+filename, switch[2], switch[3])
