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

class Player(Enum):
    White = 'White'
    Black = 'Black'

# Position of chess piece - x is char and y is int
class Position:
    def __init__(self, x:str, y:int):
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

class Piece:
    def __init__(self, currentPosition:Position, type:Type, player:Player):
        self.currentPosition = currentPosition
        self.x = toInt(currentPosition.x)
        self.y = currentPosition.y
        self.type = type
        self.player = player
        if self.player is Player.White:
            self.other_player = Player.Black
        else:
            self.other_player = Player.White
        # self.value = 0

    def __lt__(self, other):
        return isinstance(other, Piece) and self.x < other.x
    
    def isValidConstraint(self, x, y, board, table):
        target = table.get(Position(toChar(x), y))
        return (x >= 0) and (x < board.cols) and (y >= 0) and (y < board.rows) \
            and (target is None or target.player is self.other_player)
    
    def isValidPawnCapture(self, x, y, board, table):
        target = table.get(Position(toChar(x), y))
        return (x >= 0) and (x < board.cols) and (y >= 0) and (y < board.rows) \
            and (target is not None and target.player is self.other_player)

    def __str__(self):
        return self.player.name + ' ' + self.type.name + ' at ' + '(' + toChar(self.x) + ',' + str(self.y) + ')'

    def character(self):
        return self.type.name, self.player.name

    def valid_move(self, board, table):
        pass

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

class Knight(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.Knight, player)
        self.value = 30

    def valid_move(self, board, table):
        xs = []
        if super().isValidConstraint(self.x - 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y - 1))
        if super().isValidConstraint(self.x - 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 2))
        if super().isValidConstraint(self.x + 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y - 1))
        if super().isValidConstraint(self.x + 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 2))
        if super().isValidConstraint(self.x - 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y + 1))
        if super().isValidConstraint(self.x - 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 2))
        if super().isValidConstraint(self.x + 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 2))
        if super().isValidConstraint(self.x + 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y + 1))
        return xs

        
class Rook(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.Rook, player)
        self.value = 80

    def valid_move(self, board, table):
        xs = []
        temp = self.x - 1
        while temp >= 0:
            pos = Position(toChar(temp), self.y)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                break
            xs.append(pos)
            temp = temp - 1
        temp = self.x + 1
        while temp < board.cols:
            pos = Position(toChar(temp), self.y)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            temp = temp + 1
        temp = self.y - 1
        while temp >= 0:
            pos = Position(toChar(self.x), temp)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            temp = temp - 1
        temp = self.y + 1
        while temp < board.rows:
            pos = Position(toChar(self.x), temp)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            temp = temp + 1
        return xs

class Bishop(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.Bishop, player)
        self.value = 50

    def valid_move(self, board, table):
        xs = []
        tempX = self.x - 1
        tempY = self.y - 1
        while tempX >= 0 and tempY >= 0:
            pos = Position(toChar(tempX), tempY)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            tempX = tempX - 1
            tempY = tempY - 1
        tempX = self.x + 1
        tempY = self.y - 1
        while tempX < board.cols and tempY >= 0:
            pos = Position(toChar(tempX), tempY)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            tempX = tempX + 1
            tempY = tempY - 1
        tempX = self.x - 1
        tempY = self.y + 1
        while tempX >= 0 and tempY < board.rows:
            pos = Position(toChar(tempX), tempY)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            tempX = tempX - 1
            tempY = tempY + 1
        tempX = self.x + 1
        tempY = self.y + 1
        while tempX < board.cols and tempY < board.rows:
            pos = Position(toChar(tempX), tempY)
            if table.get(pos) is not None:
                if table.get(pos).player is self.other_player:    # enemy piece
                    xs.append(pos)
                # break if ally or enemy piece
                break
            xs.append(pos)
            tempX = tempX + 1
            tempY = tempY + 1
        return xs
        
class Queen(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.Queen, player)
        self.position = position
        self.player = player
        self.value = 200

    def valid_move(self, board, table):
        a = Rook(self.position, self.player)
        b = Bishop(self.position, self.player)
        return a.valid_move(board, table) + b.valid_move(board, table)
        
class King(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.King, player)
        self.value = 2000

    def valid_move(self, board, table):
        xs = []
        if super().isValidConstraint(self.x - 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 1))
        if super().isValidConstraint(self.x - 1, self.y, board, table):
            xs.append(Position(toChar(self.x - 1), self.y))
        if super().isValidConstraint(self.x - 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 1))
        if super().isValidConstraint(self.x, self.y - 1, board, table):
            xs.append(Position(toChar(self.x), self.y - 1))
        if super().isValidConstraint(self.x, self.y + 1, board, table):
            xs.append(Position(toChar(self.x), self.y + 1))
        if super().isValidConstraint(self.x + 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 1))
        if super().isValidConstraint(self.x + 1, self.y, board, table):
            xs.append(Position(toChar(self.x + 1), self.y))
        if super().isValidConstraint(self.x + 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 1))
        return xs

        
class Pawn(Piece):
    def __init__(self, position:Position, player:Player):
        super().__init__(position, Type.Pawn, player)
        self.value = 10

    def valid_move(self, board, table):
        xs = []
        if self.player is Player.White:
            if self.y + 1 < board.rows and table.get(Position(toChar(self.x), self.y + 1)) is None:
                xs.append(Position(toChar(self.x), self.y + 1))
            if super().isValidPawnCapture(self.x - 1, self.y + 1, board, table):
                xs.append(Position(toChar(self.x - 1), self.y + 1))
            if super().isValidPawnCapture(self.x + 1, self.y + 1, board, table):
                xs.append(Position(toChar(self.x + 1), self.y + 1))
        
        if self.player is Player.Black: 
            if self.y - 1 >= 0 and table.get(Position(toChar(self.x), self.y - 1)) is None:
                xs.append(Position(toChar(self.x), self.y - 1))
            if super().isValidPawnCapture(self.x - 1, self.y - 1, board, table):
                xs.append(Position(toChar(self.x - 1), self.y - 1))
            if super().isValidPawnCapture(self.x + 1, self.y - 1, board, table):
                xs.append(Position(toChar(self.x + 1), self.y - 1))

        return xs

# Representation of a chess board - including height and width
class Board:
    def __init__(self, rows:int, cols:int):
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

def parse_piece(position:Position, type:Type, isEnemy:bool):
    if isEnemy:
        player = Player.Black
    else:
        player = Player.White
    if type is Type.King:
        return King(position, player)
    elif type is Type.Queen:
        return Queen(position, player)
    elif type is Type.Rook:
        return Rook(position, player)
    elif type is Type.Bishop:
        return Bishop(position, player)
    elif type is Type.Knight:
        return Knight(position, player)
    else:
        return Pawn(position, player)

# Representation of the state of the chess game
class State:
    def __init__(self, filepath=None):
        # table: store hash value of pieces, board: store access cost,
        # piece: store starting position, goal: store goal
        self.gameboard = {}     # gameboard representation as per the question
        self.table = {}         # hash map of position -> piece
        self.valid_moves = {}   # hash map of piece -> valid position it can move to (list of children state?)
        self.threats = {}       # hash map of piece -> other piece threatening it

        isEnemy = False
        count = 1
        if filepath is None:
            return
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                # Get the number of rows
                if line.startswith("Rows"):
                    self.boardRow = int(line.split("Rows:")[1])

                # Get the number of column and initiate chess board
                elif line.startswith("Cols"):
                    self.boardCol = int(line.split("Cols:")[1])
                    self.board = Board(self.boardRow, self.boardCol)    # representation of the chess board (initial)
                
                elif line.startswith("Position of Enemy Pieces:"):
                    isEnemy = True

                elif line.startswith("Starting Position of Pieces"):
                    isEnemy = False

                elif isPiece(line):
                    line = clean(line)
                    arr = line.split(',')
                    pos = Position(arr[1][0], int(arr[1][1:]))
                    curr = parse_piece(pos, Type[arr[0]], isEnemy)
                    self.table[pos] = curr
                    self.gameboard[pos.get()] = curr.character()

                line = fp.readline()
                count = count + 1
        self.get_valid_moves()
        self.value = 0      # value of the state
        self.move = None, None
    
    def init_game(gameboard):
        state = State()
        state.gameboard = gameboard

        keys = list(gameboard.keys())
        state.boardRow = toInt(max(map(lambda x: x[0], gb))) + 1
        state.boardCol = max(map(lambda x: x[1], gb)) + 1
        state.board = Board(5, 5)

        for key in gameboard:
            pos = Position(key[0], key[1])
            val = gameboard.get(key)
            pcs = parse_piece(pos, Type[val[0]], Player[val[1]] is Player.Black)
            state.table[pos] = pcs
        
        state.get_valid_moves()
        return state

    def get_valid_moves(self):
        for pos in self.table:
            pcs = self.table.get(pos)
            # get a list of all valid move a piece can make on the game for each piece
            vm = pcs.valid_move(self.board, self.table)
            self.valid_moves[pcs] = vm
        for piece in self.valid_moves:
            self.threats[piece] = []
        # for each piece, retrieve all valid move and whether there is a piece on that position
        # retrieve the piece on that position, and add the current piece to the enemy list
        for piece in self.valid_moves:
            curr_list = self.valid_moves.get(piece)
            for pos in curr_list:
                pc = self.table.get(pos)
                if pc is not None:
                    self.threats.get(pc).append(piece)
    
    # children state (next state) is defined as moving a piece to another position
    # in the process, enemy piece might be captured
    def get_children(self, piece, next_position):
        next_state = deepcopy(self)
        next_state.valid_moves.clear()      # clear list of valid move
        next_state.threats.clear()          # clear list of threats
        del next_state.table[piece.currentPosition]    # clear current position of the piece

        next_state.table[next_position] = parse_piece(next_position, piece.type, piece.player is Player.Black)
        next_state.move = piece.currentPosition.get(), next_position.get()
        next_state.get_valid_moves()
        return next_state

    # def is_terminal(self):
    #     # state is terminal if when the player is checkmated
    #     xs = list(filter(lambda x: x.type == Type.King and x.player == self.player, self.table.values()))
    #     if len(xs) == 0:
    #         return True
    #     king = xs[0]
    #     return xs

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
    
    def getInfo(self):
        print(str(self))
        for pos in self.table:
            pcs = self.table.get(pos)
            print(pcs)
            temp = "Can move to position or capture pieces at: "
            for x in self.valid_moves.get(pcs):
                temp = temp + str(x) + ', '
            print(temp)
            temp = "Threatened by: "
            for x in self.threats.get(pcs):
                temp = temp + str(x) + ', '
            print(temp)
            print("\n")
        print(self.gameboard)


# hash map of position -> piece in that position (table)
# hash map of piece -> valid position it can move to (valid_moves)
# hash map of piece -> other piece threatening it   (threats)
# board of the chess game
# value of the state (value of max player minus min player)
class Game:
    def __init__(self, state, player):
        self.state = state      # current state of the game
        self.player = player    # current player of the game
        self.parent = None
        self.children = []      # children of the state (next possible moves)
        for pcs in state.valid_moves:
            # consider a current piece on the chess board, retrieve all possible moves
            if pcs.player != player:
                continue
            moves = state.valid_moves.get(pcs)
            # more efficient algorithm should be considered here
            for pos in moves:
                # move the current piece to the position indicated
                next_state = deepcopy(state)
                next_state.valid_moves.clear()      # clear list of valid move
                next_state.threats.clear()          # clear list of threats
                del next_state.table[pcs.currentPosition]    # clear current position of the piece
                next_state.table[pos] = parse_piece(pos, pcs.type, pcs.player is Player.Black)
                next_state.move = pcs.currentPosition.get(), pos.get()
                next_state.get_valid_moves()
                self.children.append(next_state)
    
    def opponent(self):
        if self.player is Player.White:
            return Player.Black
        else:
            return Player.White

    def is_terminal(self):
        # reminder to write terminal state later
        pass

def evaluate(state):
    white_res = 0
    black_res = 0
    for pos in state.table:
        pcs = state.table.get(pos)
        if pcs.player is Player.White:
            white_res = white_res + pcs.value
        else:
            black_res = black_res + pcs.value
    return white_res - black_res

def minimax(state, alpha, beta, isMaxPlayer, depth):
    if depth == 0 or state.is_terminal():
        return state.value
    
    if isMaxPlayer:
        bestVal = - float('inf')
        for s in state.children:
            value = minimax(s, alpha, beta, False, depth - 1)
            bestVal = max(bestVal, value) 
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = float('inf')
        for s in state.children:
            value = minimax(s, alpha, beta, True, depth - 1)
            bestVal = min(bestVal, value) 
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
        return bestVal

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard):
    state = State.init_game(gameboard)
    game = Game(state, Player.White)
    print(game.state)
    for s in game.children:
        print(s)
    # next_state = minimax(state, -float('inf'), float('inf'), True, 4)
    # return state, next_state

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

    move = ab(gameboard)
    return move #Format to be returned (('a', 0), ('b', 3))

start = time.time()
state = State(sys.argv[1])

gb = state.gameboard
ab(gb)
print(time.time() - start)