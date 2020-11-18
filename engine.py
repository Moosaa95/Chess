## This is the main chess game engine that implements the rules of the game
## and stores the state of the the chess board, including its pieces and moves


class Game_state():
	
	def __init__(self):
		"""
			The chess board is an 8 X 8 dimensional array (Matrix of 8 rows and 8 columns )
			i.e a list of lists. Each element of the Matrix is a string of two characters 
			representing the chess pieces in the order "type" + "colour"

			light pawn = pl
			dark pawn  = pd

			light knight = nl
			dark knight  = nd
			e.t.c

			empty board square = "  " ---> double empty space

		"""

		self.board = [

			["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
			["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
			["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]]

		self.light_to_move = True # True = light's turn to play; False = dark's turn to play
		self.move_log = []        # keeps a log of all moves made withing a game
		self.track_of_castling = castling(True, True, True, True) 
		self.castling_log = [castling(self.track_of_castling.lks,self.track_of_castling.dks,self.track_of_castling.lqs, self.track_of_castling.dqs)] #keeping track of castling right
		self.light_king_location = (7,4)
		self.dark_king_location = (0, 4)
		
		self.move_piece = {"p":self.get_pawn_moves, "r":self.get_rook_moves, \
						"q":self.get_queen_moves, "k":self.get_king_moves, \
						"b":self.get_bishop_moves, "n":self.get_knight_moves}
	
	
	def squareUnderAttack(self, r, c):
		""" 
		determine if enemy can attack the square r,c
		"""
		self.light_to_move = not self.light_to_move #switch to opponent's turn
		opponent_moves = self.get_possible_moves()[0]
		self.light_to_move = not self.light_to_move #swicth back turn
		for move in opponent_moves:
			if move.end_row == r and move.end_col == c: #square is under attack
				return True
		return False


	def get_pawn_moves(self, r, c, moves):
		"""
			Calculates all possible pawn moves for a given color (light or dark)
			and appends them to a list

			input parameter(s):
			r     --> starting row (int)
			c     --> starting colum (int)
			moves --> possible moves container (list)

			return parameter(s):
			None
		"""

		if self.light_to_move: # light pawns
			if r-1 >= 0 and self.board[r-1][c] == "  ": # one square advance
				moves.append(Move((r, c), (r-1, c), self.board))

				if r == 6 and self.board[r-2][c] == "  ": # two square advance
					moves.append(Move((r, c), (r-2, c), self.board))

			if c-1 >= 0: # left captures
				if r-1 >=0 and self.board[r-1][c-1][1] == "d": # dark piece present
					moves.append(Move((r, c), (r-1, c-1), self.board))

			if c+1 <= len(self.board[0]) - 1: # right captures
				if r-1>= 0  and self.board[r-1][c+1][1] == "d":
					moves.append(Move((r, c), (r-1, c+1), self.board))

		else: # dark pawns

			if r+1 <= 7 and self.board[r+1][c] == "  ": # one square advance
				moves.append(Move((r, c), (r+1, c), self.board))

				if r == 1 and self.board[r+2][c] == "  ": # two square advance
					moves.append(Move((r, c), (r+2, c), self.board))

			if c-1 >= 0: # left captures
				if r+1 <= 7 and self.board[r+1][c-1][1] == "l": # light piece present
					moves.append(Move((r, c), (r+1, c-1), self.board))

			if c+1 <= len(self.board[0]) - 1: # right captures
				if r+1 <= 7 and self.board[r+1][c+1][1] == "l":
					moves.append(Move((r, c), (r+1, c+1), self.board))
					

	def get_bishop_moves(self, r, c, moves):

		"""
			calculates all possible bishop moves for a given colour (light or dark)
			and appends them to a list

			input parameters:
			r     --> starting row (int)
			c     --> starting column (int)
			moves --> posiible moves container (list)

			return parameter(s):
			None
		"""
		directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			for i in range(1, 8):
				end_row = r + d[0] * i
				end_col = c + d[1] * i

				if 0 <= end_row < 8 and 0 <= end_col < 8:
					destination = self.board[end_row][end_col]
					if destination == "  ":
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif destination[1] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else: # friendly piece
						break
				else: # off board
					break
		


	def get_knight_moves(self, r, c, moves):
		directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			end_row = r + d[0]
			end_col = c + d[1]

			if 0 <= end_row < 8 and 0 <= end_col < 8:
				destination = self.board[end_row][end_col]
				if destination[1] == enemy_color or destination == "  ":
					moves.append(Move((r, c), (end_row, end_col), self.board))


	def get_king_moves(self, r, c, moves):
		directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			end_row = r + d[0]
			end_col = c + d[1]

			if 0 <= end_row < 8 and 0<= end_col < 8:
				destination = self.board[end_row][end_col]
				if destination[1] == enemy_color or destination == "  ":
					moves.append(Move((r, c), (end_row, end_col), self.board))


		


	def get_rook_moves(self, r, c, moves):

		directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
		enemy_color = "d" if self.light_to_move else "l"
		
		for d in directions:
			for i in range(1, 8):
				end_row = r + d[0] * i
				end_col = c + d[1] * i

				if 0 <= end_row < 8 and 0 <= end_col <8: # on board
					destination = self.board[end_row][end_col]
					if destination == "  ": # empty
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif destination[1] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else: # freindly piece
						break
				else: # off board
					break
		

	def get_queen_moves(self, r, c, moves):
		self.get_bishop_moves(r, c, moves)
		self.get_rook_moves(r, c, moves)

	
	def make_move(self, move):
		"""
			moves pieces on the board
		"""
		self.board[move.start_row][move.start_col] = "  "
		self.board[move.end_row][move.end_col] = move.piece_moved
		self.move_log.append(move) # log move
		self.light_to_move = not self.light_to_move # next player to move

		#castle move
		if move.is_castle_move:
			if move.end_col - move.start_col == 2:#king side castle move
				self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] #move the rook
				self.board[move.end_row][move.end_col+1] = "  " #delete old rook
			else: #queen side castle move
				self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2] #move the rook
				self.board[move.end_row][move.end_col-2] = "  " #delete old rook
			

		#update castling right
		self.castle_move_update(move)
		self.castling_log.append(castling(self.track_of_castling.lks,self.track_of_castling.dks,self.track_of_castling.lqs, self.track_of_castling.dqs))


	def undo_move(self, look_ahead_mode = False):
		"""
			undoes last move
		"""
		if self.move_log:
			last_move = self.move_log.pop()
			self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
			self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
			self.light_to_move = not self.light_to_move

			print("undoing ->", last_move.get_chess_notation())
		else:
			print("All undone!")
		
		#undo castle move
		if last_move.is_castle_move:
			if last_move.end_col - last_move.start_col == 2: #kingside
				self.board[last_move.end_row][last_move.end_col+1] = self.board[last_move.end_row][last_move.end_col-1]
				self.board[last_move.end_row][last_move.end_col-1] = "  "
			else: #queen side 
				self.board[last_move.end_row][last_move.end_col-2] = self.board[last_move.end_row][last_move.end_col+1]
				self.board[last_move.end_row][last_move.end_col+1] = "  "

		#undo castling
		self.castling_log.pop() #delete the new castle right
		self.track_of_castling = self.castling_log[-1] #set the track to the last castle right on the list
		

	
	def castle_move_update(self, move):
		""" update the castle move rights """
		if move.piece_moved == 'kl':
			self.track_of_castling.lks = False
			self.track_of_castling.lqs = False
		elif move.piece_moved == 'kd':
			self.track_of_castling.dks = False
			self.track_of_castling.dqs = False
		elif move.piece_moved == 'rl':
			if move.start_row == 7:
				if move.start_col == 0: #left rrook
					self.track_of_castling.lqs = False
				elif move.start_col == 7: #right rook
					self.track_of_castling.lks = False
		elif move.piece_moved == 'rd':
			if move.start_row == 0:
				if move.start_col == 0: #left rrook
					self.track_of_castling.dqs = False
				elif move.start_col == 7: #right rook
					self.track_of_castling.dks = False

	def get_valid_moves(self):
		moves = self.get_possible_moves()[0]
		castling_tempo = castling(self.track_of_castling.lks, self.track_of_castling.dks, self.track_of_castling.lqs, self.track_of_castling.dqs)
		if self.light_to_move:
			self.get_castle_moves(self.light_king_location[0], self.light_king_location[1], moves)
		else:
			self.get_castle_moves(self.dark_king_location[0], self.dark_king_location[1], moves)
		
		self.track_of_castling = castling_tempo
		return moves



	def get_possible_moves(self):

		moves = []

		turn = "l" if self.light_to_move else "d"

		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j][1] == turn:
					self.move_piece[self.board[i][j][0]](i, j, moves)

		return moves, turn

	def get_castle_moves(self, r, c, moves):
		""" get all valid castle moves for the king at r,c and add them to the list """
		if self.squareUnderAttack(r,c):
			return #cant castle while in check
		if (self.light_to_move and self.track_of_castling.lks) or (not self.light_to_move and self.track_of_castling.dks):
			self.get_king_side_catle_moves(r,c,moves) 
		if (self.light_to_move and self.track_of_castling.lqs) or (not self.light_to_move and self.track_of_castling.dqs):
			self.get_queen_side_catle_moves(r,c,moves)

	def get_king_side_catle_moves(self, r,c, moves):
		if self.board[r][c+1] == "  " and self.board[r][c+2] == "  ":
			if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
				moves.append(Move((r,c), (r, c+2), self.board, is_castle_move=True))


	def get_queen_side_catle_moves(self, r,c, moves):
		if self.board[r][c-1] == "  " and self.board[r][c-2] == "  " and self.board[r][c-3]:
			if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
				moves.append(Move((r,c),(r, c-2), self.board, is_castle_move=True))
class castling():
	def __init__(self,lks,dks,lqs,dqs):
		self.lks = lks #lks - light king side 
		self.dks = dks #dks - dark king side
		self.lqs = lqs #lqs - light queen side
		self.dqs = dqs #dqs - dark queen side

class Move():

	# map ranks to rows
	ranks_to_rows = {"1":7, "2":6, "3":5, "4":4,
					"5":3, "6":2, "7":1, "8":0}

	# map rows to ranks (revers of ranks to rows)
	rows_to_ranks = {row:rank for rank, row in ranks_to_rows.items()}

	# map files to columns 
	files_to_cols = {"a":0, "b":1, "c":2, "d":3,
					"e":4, "f":5, "g":6, "h":7}

	# map columns to files (revers of files to columns)
	cols_to_files = {col:file for file, col in files_to_cols.items()} 

	def __init__(self, start_sq, end_sq, board, is_castle_move=False):
		"""
			A Move class abstracting all parameters needed
			for moving chess pieces on the board

			input parameter(s):
			start_sq --> (row, column) of piece to be moved (tuple)
			end_square --> (row, column) of move destination on the board (tuple)
			board --> board object referencing current state of the board (class Game_state) 
		"""
		self.start_row = start_sq[0] # row location of piece to be moved
		self.start_col = start_sq[1] # column location of piece to be moved
		self.end_row = end_sq[0] # intended row destination of piece to be moved 
		self.end_col = end_sq[1] # intended column destiantion of piece to e moved
		self.piece_moved = board[self.start_row][self.start_col] # actual piece moved
		self.piece_captured = board[self.end_row][self.end_col] # opponent piece if any on the destination square
		self.is_castle_move = is_castle_move #castle move
	def get_chess_notation(self):
		"""
			creates a live commentary of pieces moved on the chess board during a game

			input parameter(s):
			None

			return parameter(s)
			commentary (string)
		"""
		return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
			"(" + self.piece_captured[0].upper() + " captured!)" if self.piece_captured != "  " else self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + \
			self.get_rank_file(self.end_row, self.end_col)


	def get_rank_file(self, r, c):
		"""
			calls cols_to_file and rows_to_rank attributes

			input parameter(s):
			r --> row to be converted to rank (int)
			c --> column to be converted to file (int)

			return parameter(s):
			"file" + "rank" (str)
		"""
		return self.cols_to_files[c] + self.rows_to_ranks[r]


	def __eq__(self, other):
		"""
			operator overloading for equating two move objects
		"""

		if isinstance(other, Move): # if first (self) and second (other) parameters are both Move objects
			return self.start_row == other.start_row and self.start_col == other.start_col and \
					self.end_row == other.end_row and self.end_col == other.end_col
		else:
			return False


	def __ne__(self, other):
		"""
			"not equals to" --> conventional counterpart to __eq__
		"""
		return self.__eq__(other)


	def __str__(self):
		"""
			operator overloading for printing Move objects
		"""
		return "({}, {}) ({}, {})".format(self.start_row, self.start_col, self.end_row, self.end_col)


