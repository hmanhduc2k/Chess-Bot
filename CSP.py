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
    return (x >= 0) and (x < board.cols) and (y >= 0) and (y < board.rows) and (table.get(Position(toChar(x), y)) is None or table.get(Position(toChar(x), y)).type is not Type.Obstacle)

def isObstacle(x, y, table):
    return table.get(Position(toChar(x), y)) is not None and table.get(Position(toChar(x), y)).type is Type.Obstacle

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
    Obstacle = 'Obstacle'

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

    def __lt__(self, other):
        return isinstance(other, Piece) and self.x <= other.x

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
        while temp >= 0 and not isObstacle(temp, self.y, table):
            xs.append(Position(toChar(temp), self.y))
            temp = temp - 1
        temp = self.x
        while temp < board.cols and not isObstacle(temp, self.y, table):
            xs.append(Position(toChar(temp), self.y))
            temp = temp + 1
        temp = self.y
        while temp >= 0 and not isObstacle(self.x, temp, table):
            xs.append(Position(toChar(self.x), temp))
            temp = temp - 1
        temp = self.y
        while temp < board.rows and not isObstacle(self.x, temp, table):
            xs.append(Position(toChar(self.x), temp))
            temp = temp + 1
        return xs

    def getBishop(self, board, table):
        xs = []
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY >= 0 and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY >= 0 and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY < board.rows and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY + 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY < board.rows and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY + 1
        return xs

    def setPosition(self, position):
        self.currentPosition = position
        self.x = toInt(currentPosition.x)
        self.y = currentPosition.y

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
            return []

    def getAdjacent(self, state):
        xs = []
        if isValid(self.x - 1, self.y - 1, state):
            xs.append(Position(toChar(self.x - 1), self.y - 1))
        if isValid(self.x - 1, self.y, state):
            xs.append(Position(toChar(self.x - 1), self.y))
        if isValid(self.x - 1, self.y + 1, state):
            xs.append(Position(toChar(self.x - 1), self.y + 1))
        if isValid(self.x, self.y - 1, state):
            xs.append(Position(toChar(self.x), self.y - 1))
        if isValid(self.x, self.y + 1, state):
            xs.append(Position(toChar(self.x), self.y + 1))
        if isValid(self.x + 1, self.y - 1, state):
            xs.append(Position(toChar(self.x + 1), self.y - 1))
        if isValid(self.x + 1, self.y, state):
            xs.append(Position(toChar(self.x + 1), self.y))
        if isValid(self.x + 1, self.y + 1, state):
            xs.append(Position(toChar(self.x + 1), self.y + 1))
        return xs

    def __str__(self):
        return self.type.name + ' at ' + '(' + toChar(self.x) + ',' + str(self.y) + ')'

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
            return 'O'

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
        self.table['viable'] = True     # table assignment is possible
        self.obstacles = []
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

                # Get and add all obstacle to the chess table
                elif line.startswith("Position of Obstacles"):
                    line = line.split("Position of Obstacles (space between):")[1]
                    if '\n' in line:
                        line = line.replace('\n', '')
                    if line == '-':
                        continue
                    obstacles = line.split(" ")
                    for obstacle in obstacles:
                        if len(obstacle) < 2:
                            continue
                        pos = Position(obstacle[0], int(obstacle[1:]))
                        curr = Piece(pos, Type.Obstacle)
                        self.table[pos] = curr
                        self.obstacles.append(pos)
                        self.domain.remove(pos)

                elif line.startswith('Number of King, Queen, Bishop, Rook, Knight (space between):'):
                    line = line.split("Number of King, Queen, Bishop, Rook, Knight (space between):")[1]
                    arr = line.split(" ")
                    self.variables = {}
                    self.variables[Type.King] = int(arr[0])
                    self.variables[Type.Queen] = int(arr[1])
                    self.variables[Type.Bishop] = int(arr[2])
                    self.variables[Type.Rook] = int(arr[3])
                    self.variables[Type.Knight] = int(arr[4])
                    
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
                    x = x + self.table.get(curr).rep() + '|'
                else:
                    x = x + ' |'
            x = x + '\n'
            res = res + x
        res = res + '  |'
        for j in range(self.board.cols):
            res = res + toChar(j) + '|'
        return res + '\n'

    def isComplete(self):
        for type in self.variables:
            if self.variables.get(type) > 0:
                return False
        return True

    def total(self):
        count = 0
        for type in self.variables:
            count = count + self.variables.get(type)
        return count
    
    def prune(self, variable):
        if variable.type == Type.King:
            self.kings = self.kings - 1
        elif variable.type == Type.Knight:
            self.knights = self.knights - 1
        elif variable.type == Type.Bishop:
            self.bishops = self.bishops - 1
        elif variable.type == Type.Rook:
            self.rooks = self.rooks - 1
        elif variable.type == Type.Queen:
            self.queens = self.queens - 1

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
                    x = x + self.table.get(curr).rep() + '|'
                else:
                    x = x + ' |'
            x = x + '\n'
            res = res + x
        res = res + '  |'
        for j in range(self.board.cols):
            res = res + toChar(j) + '|'
        return res + '\n'
    
    # def getInfo(self):
    #     print(str(self))
    #     print('Number of obstacles is ' + str(len(self.obstacles)))
    #     temp = 'Obstacles are in: '
    #     for pos in self.obstacles:
    #         temp = temp + str(pos) + ', '
    #     print(temp)
    #     temp = 'All vacant positions: '
    #     for pos in self.domain:
    #         temp = temp + str(pos) + ', '
    #     print(temp)
    #     for type in self.variables:
    #         print(type.name, self.variables.get(type))
        
def select_unassigned_variables(state):
    if state.variables.get(Type.Queen) > 0:
        return Type.Queen
    elif state.variables.get(Type.Rook) > 0:
        return Type.Rook
    elif state.variables.get(Type.Bishop) > 0:
        return Type.Bishop
    elif state.variables.get(Type.Knight) > 0:
        return Type.Knight
    elif state.variables.get(Type.King) > 0:
        return Type.King

# def inference(state):
#     return len(state.domain) >= state.getUnassigned()

# domain: list of all possible positions on the chess board
# pieces: list of pieces assigned
# table: current assignment done (position -> piece)
def backtrack(state):
    if state.isComplete():
        # assignment is complete
        # print(state.getState())
        return state.table
    
    # select unassigned type for variable construct
    type = select_unassigned_variables(state)

    # iterate through each value (position) in the domain list
    for value in state.domain:

        # construct the variable by assigning it to the position value
        variable = Piece(value, type)

        # get the threaten constraint of the variable
        constraints = variable.getThreateningConstraints(state.board, state.table)

        # check whether the constraint is compatible with exisiting pieces
        c = len(set(constraints) & set(state.pieces))

        if c <= 0:   # variable is consistent with assignment, not threatening existing pieces
            # create a new state
            new_state = deepcopy(state)

            new_state.table[value] = variable       # assign position to the chess piece
            constraints.append(value)
            new_state.domain = new_state.domain - set(constraints)      # reduce size of domain by removing threatening constraints
            new_state.variables[variable.type] = new_state.variables.get(variable.type) - 1   # reduce number of available piece
            new_state.pieces.append(value)      # add position of occupied piece for later comparison

            # print(len(new_state.domain))
            # print(new_state.getState())
            
            # forward checking the feasibility of assignment
            if len(new_state.domain) >= new_state.total():
                result = backtrack(new_state)   # continue the assignment recursively
                if result['viable']:            # result is not a failure
                    return result
    # return failure instead
    state.table['viable'] = False
    return state.table


def search(state):
    # state.getInfo()
    timeout = time.time() + 8
    # terminated = False
    data = backtrack(state)

    res = {}
    del data['viable']
    for pos in data:
        if data.get(pos).type is not Type.Obstacle:
            res[pos.x, pos.y] = data.get(pos).type.name
    return res


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    state = State(testfile)

    goalState = search(state)
    return goalState #Format to be returned

# start = time.time()
# print(run_CSP())
# print(time.time() - start)