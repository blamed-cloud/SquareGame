#!/usr/bin/python
#squaregame.py



class Square:
	reverse_side = {"UP": "DOWN", "RIGHT": "LEFT", "DOWN": "UP", "LEFT": "RIGHT"}
	vert_or_horiz = {"UP": "_", "RIGHT": "|", "DOWN": "_", "LEFT": "|"}
	
	def __init__(self):
		self.side = {"UP": 0, "RIGHT": 0, "DOWN": 0, "LEFT": 0}
		self.primary = {"UP": True, "RIGHT": True, "DOWN": True, "LEFT": True}
		self.links = {}
		self.filled = False
		self.fill_tag = " "
		
	def check_full(self, player_tag):
		if (not self.filled) and (self.side["UP"] != 0) and (self.side["RIGHT"] != 0) and (self.side["DOWN"] != 0) and (self.side["LEFT"] != 0):
			self.filled = True
			self.fill_tag = player_tag
		return self.filled
		
	def get_tag(self):
		return self.fill_tag
		
	def link_side(self, other, direction, primary_side = True):
		if direction not in self.links:
			self.links[direction] = other
			self.primary[direction] = primary_side
			other.link_side(self,Square.reverse_side[direction], not primary_side)
		
	def fill_side(self, direction):
		if self.side[direction] == 0:
			self.side[direction] = 1
			if direction in self.links:
				self.links[direction].fill_side(Square.reverse_side[direction])
				
	def primary_print_str(self, direction):
		value = ""
		if self.primary[direction]:
			if self.side[direction] != 0:
				value = Square.vert_or_horiz[direction]
			else:
				value = " "
		return value


class Board:
	def __init__(self, n_rows, n_cols):
		self.matrix = []
		# create empty squares
		for y in range(n_rows):
			row = []
			for x in range(n_cols):
				row += [Square()]
			self.matrix += [row]
		# perform linking
		for y in range(n_rows):
			for x in range(n_cols):
				if x != n_cols - 1:
					self.matrix[y][x].link_side(self.matrix[y][x+1],"RIGHT")
				if y != n_rows - 1:
					self.matrix[y][x].link_side(self.matrix[y+1][x],"DOWN")
		self.rows = n_rows
		self.cols = n_cols
		
	def opg(self):
		for y in range(self.rows):
			top_row = ""
			middle_row = ""
			bottom_row = ""
			for x in range(self.cols):
				sq = self.matrix[y][x]
				top_row += "." + sq.primary_print_str("UP")
				middle_row += sq.primary_print_str("LEFT") + sq.get_tag() + sq.primary_print_str("RIGHT")
				bottom_row += "." + sq.primary_print_str("DOWN")
			top_row += "."
			bottom_row += "."
			if len(top_row) == 2*self.cols + 1:
				print top_row
			print middle_row
			if len(bottom_row) == 2*self.cols + 1:
				print bottom_row
				
for y in range(1,6):
	for x in range(1,6):
		print "y = " + str(y) + "; x = " + str(x)
		B = Board(y,x)
		B.opg()
		print
