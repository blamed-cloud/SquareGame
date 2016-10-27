#!/usr/bin/env python
#player.py
import PythonLibraries.prgm_lib as prgm_lib
import random

class Player:
	def __init__(self):
		self.human = False
		
	def is_human(self):
		return self.human
		
	def choose_square(self, game):
		pass
		
	def choose_side(self, game):
		pass
		

class Human(Player):
	def __init__(self):
		self.human = True
		
	def choose_square(self, game):
		row = prgm_lib.get_int_escape_codes(game.escapes)
		col = prgm_lib.get_int_escape_codes(game.escapes)
		return [row,col]
		
	def choose_side(self, game):
		return prgm_lib.get_choice_escape_codes(game.sides, game.escapes)

		
class RandomAI(Player):
	def __init__(self):
		self.human = False
		
	def choose_square(self, game):
		return [random.randint(0, game.rows-1), random.randint(0, game.cols-1)]
		
	def choose_side(self, game):
		return game.sides[random.randint(0, len(game.sides)-1)]
		

class GreedyAI(Player):
	num_sides2threshold = {0:1, 1:1, 2:0, 3:2}
	
	def __init__(self):
		self.human = False
		self.chosen_sq = [-1,-1]
		
	def choose_square(self, game):
		pos_sq = [[],[],[]]
		threshold = 0
		for y in range(game.rows):
			for x in range(game.cols):
				filled_sides = game.grid[y][x].num_filled_sides()
				if filled_sides != 4:
					pos_sq[GreedyAI.num_sides2threshold[filled_sides]] += [[y,x]]
		for x in range(3):
			if len(pos_sq[x]) > 0:
				threshold = x
		index = random.randint(0, len(pos_sq[threshold])-1)
		self.chosen_sq = pos_sq[threshold][index] 
		return self.chosen_sq
				
	def choose_side(self, game):
		pos_sides = {"UP": True, "RIGHT": True, "DOWN": True, "LEFT": True}
		y = self.chosen_sq[0]
		x = self.chosen_sq[1]
		sq = game.grid[y][x]
		
		pos_sides = {key:(not sq.is_side_used(key)) for key in pos_sides}
			
#		pos_sides1 = {key:sq.num_filled_sides() for key, value in pos_sides.items() if value}
		pos_sides1 = {}
		for key, value in pos_sides.items():
			if value:
				if key in sq.links:
					pos_sides1[key] = sq.links[key].num_filled_sides
				else:
					pos_sides1[key] = 0

				
		min_v = min(pos_sides1.values())
		
		pos_sides2 = [key for key, value in pos_sides1.items() if value == min_v]
		index = random.randint(0, len(pos_sides2)-1)
		return pos_sides2[index]
