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
			
	def is_side_empty(self, direction):
		return self.side[direction] == 0
		
	def fill_side(self, direction, player_tag):
		if self.side[direction] == 0:
			self.side[direction] = 1
			filled = self.check_full(player_tag)
			if direction in self.links:
				self.links[direction].fill_side(Square.reverse_side[direction], player_tag)
		return filled
				
	def primary_print_str(self, direction):
		value = ""
		if self.primary[direction]:
			if self.side[direction] != 0:
				value = Square.vert_or_horiz[direction]
			else:
				value = " "
		return value


class Board:
	def __init__(self, n_rows, n_cols, player1, player2):
		self.grid = []
		# create empty squares
		for y in range(n_rows):
			row = []
			for x in range(n_cols):
				row += [Square()]
			self.grid += [row]
		# perform linking
		for y in range(n_rows):
			for x in range(n_cols):
				if x != n_cols - 1:
					self.grid[y][x].link_side(self.grid[y][x+1],"RIGHT")
				if y != n_rows - 1:
					self.grid[y][x].link_side(self.grid[y+1][x],"DOWN")
		self.turn = 0
		self.winner = -1
		self.quiet = False
		self.players = [None, player1, player2]
		self.rows = n_rows
		self.cols = n_cols
		self.sides = ["UP","RIGHT","DOWN","LEFT"]
		self.escapes = [":w", ":q", ":wq", ":r"]
		self.show_board = True
		self.thinking = False
		
	def get_turn(self):
		return self.turn
		
	def is_human_turn(self):
		return self.players[self.get_player_num()].is_human()
		
	def current_player(self):
		return self.players[self.get_player_num()]
	
	def handle_escape(self, code):
		if code == ":w":
			print "UnemplementedError: saving"
		elif code == ":wq":
			print "UnemplementedError: saving"
			raise SystemExit
		elif code == ":q":
			raise SystemExit
		elif code == ":r":
			pass
	
	def get_player_num(self):
		return (self.turn % 2) + 1
		
	def opg(self):
		for y in range(self.rows):
			top_row = ""
			middle_row = ""
			bottom_row = ""
			for x in range(self.cols):
				sq = self.grid[y][x]
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
				
	def is_valid_sq_pos(self, sq):
		return (sq[0] in range(self.rows)) and (sq[1] in range(self.cols))
				
	def play(self):
#		if self.history:
#			self.save_state(self.game_file)
		while self.winner == -1:
			self.do_turn()
		if not self.quiet:
			self.opg()
			if self.winner != 0:
				print "PLAYER" + str(self.winner) + " IS THE WINNER!!!"
			else:
				print "IT WAS A DRAW!"
				
	def do_turn(self):
		human = self.is_human_turn()
		if human or self.show_board:
			self.opg()
		if not human:
			if not self.thinking:
				print "Player" + str(self.get_player()) + " (the computer) is thinking..."
				self.thinking = True
		if human:
			print "First, choose a square to play on."
			print "enter a number between 0 and " + str(self.rows) + " for the row,"
			print "and then enter a number between 0 and " + str(self.cols) + " for the col."
		sq = []
		finished_getting_sq = False
		finished_playing = False
		while not finished_playing:
			sq = self.current_player().choose_square(self)
			if self.is_valid_sq_pos(sq):
				
#		if self.current_box != -1:
#			if human:
#				print "Current Square to be played in, at location (" + str(self.current_row) + ", " + str(self.current_col) + ")"
#				self.grid[self.current_row][self.current_col].opg()
#				print "Player" + str(self.get_player()) + ", it is your turn to play on this board."
#				print "Please enter a number [0-8] corresponding to the space you would like to play in."
#				print "Of course, with 0 corresponding to the top left:"
#			num = -1
#			finished_getting_num = False
#			finished_playing = False
#			while not finished_playing:
#				num = self.get_num_for_square()
#				y = self.current_row
#				x = self.current_col
#				inner_col = num % 3
#				inner_row = (num - (num % 3))/3
#				turn_descriptor = [[y,x], [inner_row, inner_col]]
#				if self.try_placing_square(num):
#					self.turn += 1
#					finished_playing = True
#					self.thinking = False
#					self.last_moves[self.get_player()-1] = turn_descriptor
#			if self.history:
#				self.save_state(self.game_file)	
#		else:
#			if human:
#				print "Player" + str(self.get_player()) + ", it is your choice which board to play on."
#				print "Please enter a number [0-8] corresponding to the board you would like to play on."
#				print "Of course, with 0 corresponding to the top left:"
#			num = self.get_num_for_box()
#			self.current_box = num
#			self.current_col = num % 3
#			self.current_row = (num - (num % 3))/3
				
for y in range(1,6):
	for x in range(1,6):
		print "y = " + str(y) + "; x = " + str(x)
		B = Board(y,x)
		B.opg()
		print
