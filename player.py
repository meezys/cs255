import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.

class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune
		self.board = board
		self.gameTree = None

	def makeTree(self,board):
		#TreeNode(None, board).generate()
		self.gameTree = TreeNode(None, board).printPostOrder()

		

	def getMove(self, gameBoard):
		if self.gameTree.boardsEqual(gameBoard):
			max = self.gameTree.getBestMove(True) 
			self.gameTree = max
			return max.choice
		else:
			for child in self.gameTree.children:
				if child.boardsEqual(gameBoard):
					self.gameTree = child
			max = self.gameTree.getBestMove(True)
			self.gameTree = max
		return max.choice

	def getMoveAlphaBeta(self, gameBoard):

		return 0

class TreeNode:

	def __init__(self, value,board, choice = None):
		self.value = value
		self.board = board
		self.children = []
		self.choice = choice
	
	def generate(self, level = 0):
		Player = ["X", "O"]
		self.expandNode(level, Player)
		for child in self.children:
			if child.value == None:
				child.generate(level + 1)

	# given a tree node, generate all its child states
	def expandNode(self, level, player):
		for i in range (0, self.board.numColumns):
			if not self.board.addPiece(i,player[level % 2]):
				continue
			newboard = self.board.copy()
			value = None
			if newboard.checkFull():
				value = 0
			if newboard.checkWin(): 
				value = 1 if level % 2 == 0 else -1
			self.children.append(TreeNode(value, newboard, i))
			self.board.removePiece(i)
	

	# processes the game tree in a depth-first fashion
	def printPostOrder(self, level  = 0):
		player = ["X","O"]
		if self == None:
			return
		if self.value is None:
			self.expandNode(level,player)
			results = []
			for child in self.children:
				results.append(child.printPostOrder(level+1).value)
			self.value = min(results) if level % 2 != 0 else max(results)
		
		return self
	
	def getBestMove(self, Max):
		if Max:
			return max(self.children, key=lambda child: child.value)
		else:
			return min(self.children, key=lambda child: child.value)
	
	def boardsEqual(self, board):
		for row in range (self.board.numColumns):
			for col in range (self.board.numRows):
				if self.board.checkSpace(row, col).value != board.checkSpace(row, col).value:
					return False
		return True