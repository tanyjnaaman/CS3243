import re
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

from sys import argv
import random
from copy import deepcopy


class Piece:

    PIECES = {
        "King": "K",
        "Queen": "Q",
        "Rook": "R",
        "Bishop": "B",
        "Knight": "N",
        "Obstacle": "X",
        "Attack": "!"
        }
    
    ASCII_OFFSET = ord('a')

    def __init__(
        self, 
        piece_type: str, 
        current_position: tuple((int, int)), 
        goal_positions: list(tuple((int, int))) = None, 
        is_opponent: bool = True):

        self.piece_type:str  = piece_type
        self.current_position = current_position
        self.goal_positions = goal_positions
        self.is_opponent: bool = is_opponent
        self.symbol: str = self.PIECES[self.piece_type]
    
    def possibleMoves(self, board) -> list(tuple((int, int))):
        
        def kingMoves():
            possibleMoves = []
            for col_offset in range(-1, 2):
                for row_offset in range(-1, 2):

                    # ignore current position
                    if row_offset == 0 and col_offset == 0:
                        continue
                        
                    # find valid positions
                    new_col = col + col_offset
                    new_row = row + row_offset
                    new_position = (new_col, new_row)

                    if (board.isPositionInBoard(new_position)
                        and not board.isPositionOccupied(new_position)):
                        possibleMoves.append(new_position)

            return possibleMoves
        
        def queenMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):

                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves

        def rookMoves():
            possibleMoves = []

            # go left
            for col_offset in range(1, board.columns):
                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves

        def bishopMoves():
            possibleMoves = []

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue
                
                if board.isPositionOccupied(new_position):
                    break

                possibleMoves.append(new_position)

            return possibleMoves
        
        def knightMoves():
            possibleMoves = []
            offset_1 = [1, -1]
            offset_2 = [2, -2]

            # col offset by 1, row offset by 2
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_1
                    new_row = row + delta_2
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position) and 
                        not board.isPositionOccupied(new_position)):
                        possibleMoves.append(new_position)

            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if (board.isPositionInBoard(new_position) and 
                        not board.isPositionOccupied(new_position)):                        
                        possibleMoves.append(new_position)
            
            return possibleMoves

        col, row = self.current_position
        
        if self.piece_type == "King":
            return kingMoves()
        elif self.piece_type == "Queen":
            return queenMoves()
        elif self.piece_type == "Rook":
            return rookMoves()
        elif self.piece_type == "Bishop":
            return bishopMoves()
        elif self.piece_type == "Knight":
            return knightMoves()
        elif self.piece_type == "Obstacle":
            return []
        elif self.piece_type == "Attack":
            raise RuntimeError("Attack piece should not be calling Piece.possibleMoves")
        else:
            raise RuntimeError("Unidentified piece type calling Piece.possibleMoves")

    def possibleAttacks(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces
    
    def possibleMoves_wrapped(self, board):
        possibleMoves = self.possibleMoves(board)
        wrapped = []
        for new_position in possibleMoves:
            wrapped.append(Piece(self.piece_type, new_position, self.goal_positions, self.is_opponent, previousPiece = self))
        return wrapped

    @staticmethod
    def convertAsciiPositionToXy(ascii_position: str) -> tuple((int, int)):
        assert(len(ascii_position) <= 3)
        col, row = ascii_position[0], ascii_position[1:]
        col, row = int(ord(col) - Piece.ASCII_OFFSET), int(row)
        return (col, row)

    @staticmethod
    def convertXyToAsciiTuple(position: tuple((int, int))) -> str:
        col, row = position
        return (chr(col + Piece.ASCII_OFFSET), row)

    def positionToAsciiTuple(self):
        return Piece.convertXyToAsciiTuple(self.current_position)


    def __repr__(self) -> str:
        if self.is_opponent:
            return "\033[1;31m" + self.symbol + "\033[0;0m" # red
        else:
            return "\033[1;32m" + self.symbol + "\033[0;0m" # green

    def __hash__(self) -> int:
        hashcode = hash(self.current_position, self.piece_type) # hash by current position and piece type
        return hashcode 
    
    def __lt__(self, other: object):
        return False # no notion of less or more than

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        
        return self.current_position == other.current_position


class Board:
    def __init__(self, rows: int, columns: int):
        self.rows: int = rows
        self.columns:int  = columns 
        self.pieces_grid: list(list(Piece)) = [[None for x in range(self.columns)] for y in range(self.rows)]
        self.attacks_grid: list(list(int)) = [[0 for x in range(self.columns)] for y in range(self.rows)]
        self.pieces_table: dict = dict()

    def clear_attack_grid(self):
        self.attacks_grid = [[None for x in range(self.columns)] for y in range(self.rows)]

    def getPiece(self, piece_position: tuple((int, int))) -> Piece:
        return self.pieces_table.get(piece_position)

    def addPiece(self, piece: Piece, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = piece
        self.pieces_table[piece_position] = piece

    def addPiece_withAttacks(self, piece: Piece, piece_position: tuple((int, int))):
        # add piece to board

        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        for col, row, attackPiece in piece.possibleAttacks(self):
            self.attacks_grid[row][col] += 1

    def removePiece_withAttacks(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)

        # remove piece from board
        self.removePiece(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row, attackPiece in piece.possibleAttacks(self):
            self.attacks_grid[row][col] -= 1

    def removePiece(self, piece_position: tuple((int, int))):
        col, row = piece_position
        self.pieces_grid[row][col] = None
        self.pieces_table.pop(piece_position)



    def isPositionOccupied(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.pieces_grid[row][col] != None

    def isPositionAttacked(self, position: tuple((int, int))) -> bool:
        col, row = position
        return self.attacks_grid[row][col] != None

    def isPositionInBoard(self, position: tuple((int, int))) -> bool:
        col, row = position
        return (col < self.columns and col >= 0) and (row < self.rows and row >= 0)

    def toDictionary(self) -> dict:
        out = {}
        for y in range(self.rows):
            for x in range(self.columns):
                piece: Piece = self.pieces_grid[y][x]
                if  piece != None:
                    out[Piece.convertXyToAsciiTuple((x, y))] = piece.piece_type
        return out

    def isSolutionTo8Queens(self) -> bool:
        
        count = 0
        overlap = (self.attacks_grid and self.pieces_grid)
        for y in range(self.rows):
                    for x in range(self.columns):
                        position = overlap[y][x]
                        if position != None or position == True:
                            count += 1
        return count == 0

    def getPiecePositions(self) -> list(tuple((int, int))):
        return list(self.pieces_table.keys())
                

    def __repr__(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "

        # print board
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                piece = self.pieces_grid[i][j]
                if piece == None:
                    item = " "
                elif isinstance(piece, str):
                    item = piece
                else:
                    item = repr(piece)
                row += item + horizontalSeparator
            out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        out += verticalSeperator
        out += letters
        out += "\n\n\n"

        # print attacks
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                attack = self.attacks_grid[i][j]
                if self.pieces_grid[i][j] != None:
                    item = repr(piece)
                elif attack != 0:
                    item = "\033[1;31m" + str(attack) + "\033[0;0m" # red
                else:
                    item = str(attack)


                row += item + horizontalSeparator
            out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        out += verticalSeperator
        out += letters

        return out


def parse(file_path: str):

    # read file piped in
    with open(file_path) as f:
        lines = f.readlines()
    
    # ===== game board =====
    rows = int(lines[0][5:])
    columns = int(lines[1][5:])

    # ===== obstacles =====

    # read in obstacles
    obstacles = []
    num_obstacles = int(lines[2][20:])
    if num_obstacles > 0: # has obstacles
        obstacle_positions = lines[3].split(":")[1].strip("\n").split(" ")
        obstacle_positions = list(map(Piece.convertAsciiPositionToXy, obstacle_positions))
        obstacles = [Piece("Obstacle", obstacle_positions[i]) for i in range(num_obstacles)]
    
    # place obstacles on board
    for i in range(num_obstacles):
        obstacle = obstacles[i]
        obstacle_position = obstacle_positions[i]
        board.addPiece(obstacle, obstacle_position)

    # ===== k =====
    k = int(lines[4].split(":")[-1])


    # ===== pieces =====
    # read number of pieces
    line_index = 5
    line = lines[line_index]
    num_pieces = line.split(":")[1].split(" ")
    num_pieces = sum(map(int, num_pieces))
    line_index += 2

    # read in positions of pieces add to list of pieces
    pieces = []
    for i in range(num_pieces):
        line = lines[line_index].strip("[]\n\r")
        piece_type, ascii_position = line.split(",")
        position = Piece.convertAsciiPositionToXy(ascii_position)
        piece = Piece(piece_type, position)
        pieces.append((position, piece))

        # next iteration
        line_index += 1

    
    return rows, columns, pieces, k, num_pieces
    

def evaluation_function(board: Board) -> float:

    def numberInAttackPositions():
        count = 0
        overlap = (board.attacks_grid and board.pieces_grid)
        for y in range(board.rows):
                    for x in range(board.columns):
                        position = overlap[y][x]
                        if position != None or position == True:
                            count += 1
        return count

    value = numberInAttackPositions()

    return value

def successor_generation(board: Board, reservePieces: list) -> tuple((Board, tuple((int, int)))): # only by removing pieces

    def top():

        # initialize
        values = []
        bestPositionToRemove = None
        bestReserveToAddIndex = 0
        bestValue = 9223372036854775807

        # find best to remove
        positions = board.getPiecePositions()
        for p in positions:

            # remove position
            removedPiece = board.getPiece(p)
            board.removePiece_withAttacks(p)

            for i in range(len(reservePieces)):

                pos, piece = reservePieces[i]
                
                # add reserve piece
                board.addPiece_withAttacks(piece, pos)

                # evaluate and rank
                val = evaluation_function(board)
                if val < bestValue:
                    bestValue = val
                    bestPositionToRemove = p
                    bestReserveToAddIndex = i

                # remove reserve piece to restore state
                board.removePiece_withAttacks(pos)



            # add back to restore state
            board.addPiece_withAttacks(removedPiece, p)
        
        # apply best change permanently

        # remove existing, put to reserve
        piece = board.getPiece(bestPositionToRemove)
        board.removePiece_withAttacks(bestPositionToRemove) 
        reservePieces.append((bestPositionToRemove, piece))

        # move from reserve to main board
        pos, piece = reservePieces.pop(bestReserveToAddIndex) 
        board.addPiece_withAttacks(piece, pos)
        

        return board, bestValue, reservePieces

    board, value, newReservePieces = top()
    return board, value, newReservePieces

  

def local_search(board: Board, offBoardPieces: list):

    current = board
    reservePieces = offBoardPieces
    current_value = evaluation_function(board)

    while True:

        # generate successor
        best_successor, value, reservePieces = successor_generation(current, reservePieces)
        print("\nvalue: ", value)

        # see if need to terminate
        if (value >= current_value):
            return board.toDictionary(), board
        else:
            current = best_successor

def random_initialization_search(rows: int, cols: int, n: int, k: int, pieces: list):
    

    print("\n ===== NEW SEARCH =====")
    # deepcopy
    board = Board(rows, cols)

    # random initialization
    indices = [i for i in range(n)]
    random.shuffle(indices)
    indices = indices[:k]

    indices = [2, 4, 11, 13]


    for i in indices:
        pos, piece = pieces[i]
        board.addPiece_withAttacks(piece, pos)

    remainingPieces = []
    for i in range(n):
        if i not in indices:
            remainingPieces.append(pieces[i])
    
    # search
    print(indices)
    print(repr(board))
    # print(remainingPieces)
    return local_search(board, remainingPieces)



def test_run():
    input_filepath = argv[1]
    rows, cols, pieces, k, n = parse(input_filepath)
    print("board dimensions are (rows x cols): ", rows, "x", cols)
    print("k is :", k)
    print("pieces are: \n", pieces)

    # random initialization search
    isGoal = False
    while not isGoal:
        dictionary, board = random_initialization_search(rows ,cols, n, k, pieces)
        isGoal = board.isSolutionTo8Queens()

    print(repr(board))
    print(dictionary)

    
test_run()


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.

    return goalState #Format to be returned


