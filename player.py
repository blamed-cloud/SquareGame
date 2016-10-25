#!/usr/bin/python
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
