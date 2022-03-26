import os
import sys
from enum import Enum
from collections import deque
from queue import PriorityQueue
import time
import math
from copy import deepcopy

# Helper functions to aid in your implementation. Can edit/remove
def toInt(c):
    return ord(c) - 97

def toChar(i):
    return chr(i + 97)

def check(move):
    return toInt(move[0]) >= 0 & toInt(move[0]) < 26 & move[1] >= 0

def isValid(x, y, state):
    return (x >= 0) and (x < state.board.cols) and (y >= 0) and (y < state.board.rows) and (state.table.get(Position(toChar(x), y)) is None)

def isValidConstraint(x, y, board, table):
    return (x >= 0) and (x < board.cols) and (y >= 0) and (y < board.rows) and (table.get(Position(toChar(x), y)) is None)

def clean(s):
    s = s.replace('[', '')
    s = s.replace(']', '')
    return s

def isPiece(piece):
    if not piece.startswith('[') and not piece.endswith(']'):
        return False
    piece = clean(piece)
    arr = piece.split(',')
    try:
        Type[arr[0]]
        return True
    except Exception as err:
        return False
    
# Type of chess piece
class Type(Enum):
    King = 'King'
    Rook = 'Rook'
    Bishop = 'Bishop'
    Queen = 'Queen'
    Knight = 'Knight'
    Pawn = 'Pawn'

# Position of chess piece - x is char and y is int
class Position:
    def __init__(self, x, y):
        self.x = x  # col number in character - horizontal value
        self.y = y  # row number in integer - vertical value
    
    def __str__(self):
        return '(' + self.x + ',' + str(self.y) + ')'
    
    def get(self):
        return self.x, self.y

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return (self.x == other.x) and (self.y == other.y)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

# Representation of a chess piece - its current Position and its Type
class Piece:
    def __init__(self, currentPosition, type):
        self.currentPosition = currentPosition
        self.x = toInt(currentPosition.x)
        self.y = currentPosition.y
        self.type = type
        self.player = "Default"

    def __lt__(self, other):
        return isinstance(other, Piece) and self.x <= other.x
    
    def getPawn(self, board, table):
        xs = []
        

    def getKing(self, board, table):
        xs = []
        if isValidConstraint(self.x - 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 1))
        if isValidConstraint(self.x - 1, self.y, board, table):
            xs.append(Position(toChar(self.x - 1), self.y))
        if isValidConstraint(self.x - 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 1))
        if isValidConstraint(self.x, self.y - 1, board, table):
            xs.append(Position(toChar(self.x), self.y - 1))
        if isValidConstraint(self.x, self.y + 1, board, table):
            xs.append(Position(toChar(self.x), self.y + 1))
        if isValidConstraint(self.x + 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 1))
        if isValidConstraint(self.x + 1, self.y, board, table):
            xs.append(Position(toChar(self.x + 1), self.y))
        if isValidConstraint(self.x + 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 1))
        return xs

    def getKnight(self, board, table):
        xs = []
        if isValidConstraint(self.x - 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y - 1))
        if isValidConstraint(self.x - 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 2))
        if isValidConstraint(self.x + 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y - 1))
        if isValidConstraint(self.x + 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 2))
        if isValidConstraint(self.x - 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y + 1))
        if isValidConstraint(self.x - 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 2))
        if isValidConstraint(self.x + 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 2))
        if isValidConstraint(self.x + 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y + 1))
        return xs

    def getRook(self, board, table):
        xs = []
        temp = self.x
        while temp >= 0:
            xs.append(Position(toChar(temp), self.y))
            temp = temp - 1
        temp = self.x
        while temp < board.cols:
            xs.append(Position(toChar(temp), self.y))
            temp = temp + 1
        temp = self.y
        while temp >= 0:
            xs.append(Position(toChar(self.x), temp))
            temp = temp - 1
        temp = self.y
        while temp < board.rows:
            xs.append(Position(toChar(self.x), temp))
            temp = temp + 1
        return xs

    def getBishop(self, board, table):
        xs = []
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY >= 0:
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY >= 0:
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY < board.rows:
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY + 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY < board.rows:
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY + 1
        return xs

    def getPawn(self, board, table):
        xs = []
        
        

    def getPosition(self):
        return Position(toChar(self.x), self.y)

    def getThreateningConstraints(self, board, table):
        if self.type == Type.King:
            return self.getKing(board, table)
        elif self.type == Type.Rook:
            return self.getRook(board, table)
        elif self.type == Type.Bishop:
            return self.getBishop(board, table)
        elif self.type == Type.Queen:
            return self.getRook(board, table) + self.getBishop(board, table)
        elif self.type == Type.Knight:
            return self.getKnight(board, table)
        else:
            return self.getPawn(board, table)

    def __str__(self):
        return self.type.name + ' at ' + '(' + toChar(self.x) + ',' + str(self.y) + '), ' + self.player

    def rep(self):
        if self.type == Type.King:
            return 'K'
        elif self.type == Type.Rook:
            return 'R'
        elif self.type == Type.Bishop:
            return 'B'
        elif self.type == Type.Queen:
            return 'Q'
        elif self.type == Type.Knight:
            return 'M'
        else:
            return 'P'

# Representation of a chess board - including height and width
class Board:
    def __init__(self, rows, cols):
        self.rows = rows   # refers to the number of rows
        self.cols = cols   # refers to the number of columns
        self.table = []
        arr = []
        for i in range(rows):
            for j in range(cols):
                self.table.append(Position(toChar(j), i))
    
    def __str__(self):
        res = ""
        for row in self.table:
            res = res + str(row) + "\n"
        return res

# Representation of the state of the chess game
class State:
    def __init__(self, filepath):
        # table: store hash value of pieces, board: store access cost,
        # piece: store starting position, goal: store goal
        self.table = {}
        self.valid_moves = {}
        self.valid_capture = {}
        isEnemy = False
        isAlly = False
        count = 1
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                # Get the number of rows
                if line.startswith("Rows"):
                    self.boardRow = int(line.split("Rows:")[1])

                # Get the number of column and initiate chess board
                elif line.startswith("Cols"):
                    self.boardCol = int(line.split("Cols:")[1])
                    self.board = Board(self.boardRow, self.boardCol)
                    self.domain = set(self.board.table)
                
                elif line.startswith("Position of Enemy Pieces:"):
                    isEnemy = True
                    isAlly = False

                elif line.startswith("Starting Position of Pieces"):
                    isEnemy = False
                    isAlly = True

                elif isPiece(line):
                    line = clean(line)
                    arr = line.split(',')
                    pos = Position(arr[1][0], int(arr[1][1:]))
                    curr = Piece(pos, Type[arr[0]])
                    if isEnemy:
                        curr.player = "Black"
                    if isAlly:
                        curr.player = "White"
                    self.table[pos] = curr
                    xs = curr.getThreateningConstraints(self.board, self.table)
                    self.valid_moves[curr] = xs

                line = fp.readline()
                count = count + 1
        self.pieces = []

    def getState(self):
        res = ''
        for i in range(self.board.rows):
            x = '|'
            if i < 10:
                x = '0' + str(i) + x
            else:
                x = str(i) + x
            for j in range(self.board.cols):
                curr = Position(toChar(j), i)
                if curr in self.table:
                    print(self.table.get(curr))
                    x = x + self.table.get(curr).rep() + '|'
                else:
                    x = x + ' |'
            x = x + '\n'
            res = res + x
        res = res + '  |'
        for j in range(self.board.cols):
            res = res + toChar(j) + '|'
        return res + '\n'

    def __str__(self):
        res = ''
        for i in range(self.board.rows):
            x = '|'
            if i < 10:
                x = '0' + str(i) + x
            else:
                x = str(i) + x
            for j in range(self.board.cols):
                curr = Position(toChar(j), i)
                if self.table.get(curr) is not None:
                    print(self.table.get(curr))
                    x = x + self.table.get(curr).rep() + '|'
                else:
                    x = x + ' |'
            x = x + '\n'
            res = res + x
        res = res + '  |'
        for j in range(self.board.cols):
            res = res + toChar(j) + '|'
        return res + '\n'
    
    def getInfo(self):
        print(str(self))
        print('Number of obstacles is ' + str(len(self.obstacles)))
        temp = 'Obstacles are in: '
        for pos in self.obstacles:
            temp = temp + str(pos) + ', '
        print(temp)
        temp = 'All vacant positions: '
        for pos in self.domain:
            temp = temp + str(pos) + ', '
        print(temp)
        for type in self.variables:
            print(type.name, self.variables.get(type))
        

#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    pass



### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    config = sys.argv[1] #Takes in config.txt Optional

    move = (None, None)
    return move #Format to be returned (('a', 0), ('b', 3))

print(State(sys.argv[1]))