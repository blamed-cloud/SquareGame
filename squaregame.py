#!/usr/bin/env python
#squaregame.py

import player


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
		
	def is_full(self):
		return self.filled
		
	def is_side_used(self, direction):
		return self.side[direction] != 0
		
	def get_tag(self):
		return self.fill_tag
		
	def num_filled_sides(self):
		return sum(self.side.values())
		
	def link_side(self, other, direction, primary_side = True):
		if direction not in self.links:
			self.links[direction] = other
			self.primary[direction] = primary_side
			other.link_side(self,Square.reverse_side[direction], not primary_side)
			
	def is_side_empty(self, direction):
		return self.side[direction] == 0
		
	def fill_side(self, direction, player_tag):
		filled = self.filled
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
	def __init__(self, n_rows, n_cols, player1, player2, be_quiet = False):
		self.grid = []
		# create empty squares
		for y in range(n_rows):
			row = []
			for x in range(n_cols):
				row += [Square()]
			self.grid += [row]
		# perform linking
		#### consider implimeting back-linking ####
		for y in range(n_rows):
			for x in range(n_cols):
				if x != n_cols - 1:
					self.grid[y][x].link_side(self.grid[y][x+1],"RIGHT")
				if y != n_rows - 1:
					self.grid[y][x].link_side(self.grid[y+1][x],"DOWN")
		self.turn = 0
		self.winner = -1
		self.quiet = be_quiet
		self.players = [None, player1, player2]
		self.rows = n_rows
		self.cols = n_cols
		self.sides = ["UP","RIGHT","DOWN","LEFT"]
		self.escapes = [":w", ":q", ":wq", ":r"]
		self.show_board = not be_quiet
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
				middle_row += sq.primary_print_str("LEFT") + str(sq.get_tag()) + sq.primary_print_str("RIGHT")
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
		
	def check_winner(self):
		win = [0,0,0]
		for y in range(self.rows):
			for x in range(self.cols):
				tag = self.grid[y][x].get_tag()
				if tag == " ":
					return -1
				elif str(tag) == "1":
					win[1] += 1
				elif str(tag) == "2":
					win[2] += 1
		if win[1] > win[2]:
			self.winner = 1
		elif win[1] == win[2]:
			self.winner = 0
		elif win[2] > win[1]:
			self.winner = 2
		return self.winner		
				
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
		return self.winner
				
	def do_turn(self):
		human = self.is_human_turn()
		if human or self.show_board:
			self.opg()
			print "="*(2*self.cols + 1)
#		if not human:
#			if not self.thinking:
#				print "Player" + str(self.get_player_num()) + " (the computer) is thinking..."
#				self.thinking = True

		sq = []
		finished_playing = False
		while not finished_playing:
			if human:
				print "First, choose a square to play on."
				print "enter a number between 0 and " + str(self.rows) + " for the row,"
				print "and then enter a number between 0 and " + str(self.cols) + " for the col."
			sq = self.current_player().choose_square(self)
			if sq in self.escapes:
				self.handle_escape(sq)
			if self.is_valid_sq_pos(sq):
				if not self.grid[sq[0]][sq[1]].is_full():
					if human:
						print "Next, choose a side to play on:"
					direction = self.current_player().choose_side(self)
					if direction in self.escapes:
						self.handle_escape(direction)
					else:
						if not self.grid[sq[0]][sq[1]].is_side_used(direction):
							full = self.grid[sq[0]][sq[1]].fill_side(direction, self.get_player_num())
							if full:
								if self.check_winner() == -1:
									if human:
										print "You filled in a square, so you get to go again."
								else:
									finished_playing = True
							else:
								finished_playing = True
		self.turn += 1
		self.thinking = False

				
#for y in range(1,6):
#	for x in range(1,6):
#		print "y = " + str(y) + "; x = " + str(x)
#		B = Board(y,x)
#		B.opg()
#		print
if __name__ == "__main__":
	num_games = 10000

#	hp = player.Human()
#	B = Board(4,6,hp, player.GreedyAI())
#	B.play()

	p1r = player.RandomAI()
	p2r = player.RandomAI()
	p1g = player.GreedyAI()
	p2g = player.GreedyAI()

	win_counts = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

	for x in range(num_games):
		B = Board(4,4,p1r,p2r, True)
		w = B.play()
		win_counts[0][w] += 1
	
#	for x in range(num_games):
#		B = Board(10,12,p1r,p1g, True)
#		w = B.play()
#		win_counts[1][w] += 1
	
#	for x in range(num_games):
#		B = Board(10,12,p1g,p1r, True)
#		w = B.play()
#		win_counts[2][w] += 1
	
	for x in range(num_games):
		B = Board(10,12,p1g,p2g, True)
		w = B.play()
		win_counts[3][w] += 1

	for x in range(4):
		print win_counts[x]
		for w in win_counts[x]:
			print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
		print




