from ast import Raise
from copy import deepcopy
from operator import is_
import sys
import random


### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.


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
        domain: set = set(), 
        is_opponent: bool = True):

        self.piece_type:str  = piece_type
        self.current_position = current_position
        self.is_opponent: bool = is_opponent
        self.symbol: str = self.PIECES[self.piece_type]
        self.domain: set = domain

    def removeFromDomain(self, position: tuple((int, int))):
        self.domain.remove(position)
    
    def getDomainSize(self):
        return len(self.domain)
    
    def possibleMoves_upTo(self, board) -> list(tuple((int, int))):
        
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

                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)
                        if (board.isPositionInBoard(new_position) 
                            and board.isPositionOccupied(new_position)):
                            break

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
                
                possibleMoves.append(new_position)
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

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

                possibleMoves.append(new_position)
                 
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

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

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

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
                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)

                    if (board.isPositionInBoard(new_position) 
                        and board.isPositionOccupied(new_position)):                    
                        break

            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if board.isPositionInBoard(new_position):                        
                        possibleMoves.append(new_position)
                    
                    if (board.isPositionInBoard(new_position) 
                        and board.isPositionOccupied(new_position)):                    
                        break
            
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
            pass
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves_upTo")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_upTo")

    def possibleMoves_passThrough(self, board) -> list(tuple((int, int))):
        
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

                    if (board.isPositionInBoard(new_position)):
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
                
                possibleMoves.append(new_position)

                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

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

                possibleMoves.append(new_position)

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

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

                possibleMoves.append(new_position)
                

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)


            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

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

                possibleMoves.append(new_position)

            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)
                
                if (board.isPositionInBoard(new_position) 
                    and board.isPositionOccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

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

                possibleMoves.append(new_position)

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

                possibleMoves.append(new_position)


            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                if not board.isPositionInBoard(new_position):
                    continue

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
                    if (board.isPositionInBoard(new_position)):
                        possibleMoves.append(new_position)


            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)
                    if board.isPositionInBoard(new_position):                        
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
            pass
            # raise RuntimeError("Attack piece should not be calling Piece.possibleMoves_passThrough")
        else:
            pass
            # raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_passThrough")

    def possibleAttacks(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves_upTo(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces

    def possibleAttacks_passThrough(self, board) -> list:
        attackPieces = []
        for col, row in self.possibleMoves_passThrough(board):
            attackPieces.append((col, row, Piece("Attack", (col, row), is_opponent = True)))
        return attackPieces
    

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

    def getSequenceOfValues(self, board) -> list(tuple((int, int))):

        def random_sequence():
            values = list(self.domain)
            indices = [i for i in range(len(values))]
            random.shuffle(indices)
            sequence = [values[i] for i in indices]

            return sequence

        def random_filtered_sequence():
            values = list(self.domain)
            indices = [i for i in range(len(values))]
            random.shuffle(indices)
            sequence = []
            for i in indices:
                pos = values[i]
                if not (board.isPositionOccupied(pos) or board.isPositionAttacked(pos)):
                    sequence.append(pos)
            
            return sequence

        def fixed_sequence():
            return list(self.domain)

        def fixed_filtered_sequence():
            values = list(self.domain)
            sequence = []
            for i in values:
                if not (board.isPositionOccupied(i) or board.isPositionAttacked(i)):
                    sequence.append(i)
            
            return sequence
        
        sequence = fixed_filtered_sequence()

        return sequence

    def updateDomainBasedOn(self, board):
        new_domain: set = set()
        for pos in self.domain:
            if not (board.isPositionOccupied(pos) or board.isPositionAttacked(pos)):
                new_domain.add(pos)
        self.domain = new_domain
        return new_domain



    def __repr__(self) -> str:
        if self.is_opponent:
            return "\033[1;31m" + self.symbol + "\033[0;0m" # red
        else:
            return "\033[1;32m" + self.symbol + "\033[0;0m" # green

    def __str__(self) -> str:
        return self.symbol

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
        for col, row, _ in piece.possibleAttacks(self):
            self.attacks_grid[row][col] += 1

    def addPiece_withAttacks_passThrough(self, piece: Piece, piece_position: tuple((int, int))):
        # add piece to board

        self.addPiece(piece, piece_position)
        
        # update position with "Attack"
        for col, row, _ in piece.possibleAttacks_passThrough(self):
            self.attacks_grid[row][col] += 1

    def removePiece_withAttacks(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)

        # remove piece from board
        self.removePiece(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row, _ in piece.possibleAttacks(self):
            self.attacks_grid[row][col] -= 1

    def removePiece_withAttacks_passThrough(self, piece_position: tuple((int, int))):

        # get piece
        piece: Piece = self.pieces_table.get(piece_position)

        # remove piece from board
        self.removePiece(piece_position)
        
        # update position with "Attack" by reducing count
        for col, row, _ in piece.possibleAttacks_passThrough(self):
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
        return self.attacks_grid[row][col] != 0
    
    def numberSafePositions(self) -> int:
        positions = [(x, y) for x in range(self.columns) for y in range(self.rows)]
        count = 0
        for p in positions:
            if not (self.isPositionOccupied(p) or self.isPositionAttacked(p)):    
                count += 1
        return count 

    def isPositionInBoard(self, position: tuple((int, int))) -> bool:
        col, row = position
        return (col < self.columns and col >= 0) and (row < self.rows and row >= 0)

    def toDictionary(self) -> dict:
        out = {}
        for y in range(self.rows):
            for x in range(self.columns):
                piece: Piece = self.pieces_grid[y][x]
                if  piece != None and piece.symbol != "X":
                    out[Piece.convertXyToAsciiTuple((x, y))] = piece.piece_type
        return out

    def isSolutionTo8Queens(self) -> bool:
        
        count = self.positionsUnderAttack()
        return count == 0

    def positionsUnderAttack(self)-> int:
        count = 0
        positions = self.getPiecePositions()
        
        for pos in positions:
            piece: Piece = self.getPiece(pos)
            if piece.symbol == "X":
                continue
            x, y = pos
            if self.attacks_grid[y][x]:
                count += 1
        return count

    def getPiecePositions(self) -> list(tuple((int, int))):
        return list(self.pieces_table.keys())
                

    def __repr__(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "
   
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += chr(j + Piece.ASCII_OFFSET) + horizontalSeparator

        # print attacks
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                attack = self.attacks_grid[i][j]
                piece = self.pieces_grid[i][j]
                if piece != None:
                    item = repr(piece) 
                    if attack == 0:
                        item = "\033[1;32m" + str(piece) + "\033[0;0m"
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

    def isConsistent(self, position: tuple, piece:Piece):

        initialPositionsUnderAttack = self.positionsUnderAttack()
        canPlace = not (self.isPositionOccupied(position) or self.isPositionAttacked(position))

        if not canPlace:
            return False

        # place piece
        piece.current_position = position
        self.addPiece_withAttacks_passThrough(piece, position)

        # count and check
        othersNotAffected = self.positionsUnderAttack() == initialPositionsUnderAttack
        
        # undo placement
        self.removePiece_withAttacks_passThrough(position)

        # return judgement
        return canPlace and othersNotAffected


class CSP:

    def __init__(self, initial_assignment: Board, pieces: list):

        # intiialize
        self.assignment: Board = initial_assignment
        self.pieces: list(Piece) = deepcopy(pieces)
        self.unassigned_pieces: list(Piece) = deepcopy(pieces)
        self.depth = 0
        self.count = 0
    
    def backtracking_search(self):

        # print("\n ===== NEW CALL TO backtracking_search() =====")
        # if solution, return
        if self.assignment.isSolutionTo8Queens() and len(self.unassigned_pieces) == 0:
            return self.assignment.toDictionary(), self.assignment

        # if not solution, get variable to assign, and sequence of values to try assigning
        piece_variable: Piece = CSP.selectByPopUnassignedVariable(self.unassigned_pieces)
        values = piece_variable.getSequenceOfValues(self.assignment)
        
        for position in values:
            if self.assignment.isConsistent(position, piece_variable):
                
                # add piece
                self.assignment.addPiece_withAttacks_passThrough(piece_variable, position)
                # print("assigned ", piece_variable, " to ", position)
                # print(self.assignment)
                # print("variables left: ", len(self.unassigned_pieces), ", ", self.unassigned_pieces)
                self.count += 1
                # print("assignments tried = ", self.count)

                # inference and recursion
                is_viable = self.infer(self.unassigned_pieces)

                if is_viable:
                    self.depth += 1
                    self.infer(self.unassigned_pieces, modify = True)
                    result = self.backtracking_search() # recursive call
                    if result != (False, False): # if valid result found at base of recursion, return
                        return result
                    else: #failed, backtrack
                        # print("\n===== BACKTRACKING =====")
                        self.unassigned_pieces = deepcopy(self.pieces[self.depth:len(self.pieces)])
                        # print("updated unassigned pieces to: ", self.unassigned_pieces)
                        self.depth -=1 
                    
                # else undo assignment
                self.assignment.removePiece_withAttacks_passThrough(position)
                # print("\nnot viable, undoing assignment!")
                # print(self.assignment)
                # print("variables left: ", self.unassigned_pieces)
                # print("\n")

        
        return False, False # return false if no viable found 

    
    def infer(self, unassigned_pieces: list,  modify = False):
        
        def forward_checking():

            # look through remaining unassigned variables and eliminate illegal values
            for p in self.unassigned_pieces:
                piece: Piece = p
                if not modify:
                    piece: Piece = deepcopy(p)

                piece.updateDomainBasedOn(self.assignment)
                if piece.getDomainSize() == 0:
                    return False
                
            return True

        def heuristic_asMany():
            safePositions = self.assignment.numberSafePositions()
            piecesLeft = len(unassigned_pieces)
            if piecesLeft > safePositions:
                # print("safe positions is ", safePositions, " but pieces left is ", piecesLeft)
                return False
            return True
            
        if not heuristic_asMany():
            return False

        inference = forward_checking()
    
        return inference


    
    def selectByPopUnassignedVariable(pieces: list) -> Piece:

        PIECES_VALUE = {
                "King": 8,
                "Queen": 26,
                "Rook": 10,
                "Bishop": 13,
                "Knight": 8,
                "Obstacle": "X",
                "Attack": "!"
                }

        def minimum_remaining_values():
            pieces.sort(key = lambda p : p.getDomainSize())
            return pieces.pop(0)

        def by_piece_type():
            pieces.sort(key = lambda p : PIECES_VALUE[p.piece_type])
            return pieces.pop(0)

        def MRV_then_piece_type():
            pieces.sort(key = lambda p : (p.getDomainSize(), PIECES_VALUE[p.piece_type]))
            return pieces.pop(0)

        def piece_type_then_MRV():
            pieces.sort(key = lambda p : (PIECES_VALUE[p.piece_type], p.getDomainSize()))
            return pieces.pop(0)

        selected_piece = MRV_then_piece_type()

        return selected_piece 



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
        obstacles = [(obstacle_positions[i], 
                        Piece("Obstacle", obstacle_positions[i])) for i in range(num_obstacles)]

    # add obstacles
    board = Board(rows, columns)
    for i in obstacles:
        pos = i[0]
        obs = i[1]
        board.addPiece(obs, pos)

    # ===== pieces =====
    # read number of pieces
    line_index = 4
    line = lines[line_index]
    num_pieces = list(map(int, line.split(":")[1].split(" ")))

    # create a piece with domain for each piece
    pieces = []
    domain = [(x, y) for x in range(columns) for y in range(rows)]
    for piece_type in range(len(num_pieces)):
        if piece_type == 0:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("King", None, deepcopy(domain)))
        elif piece_type == 1:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Queen", None, deepcopy(domain)))                
        elif piece_type == 2:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Bishop", None, deepcopy(domain)))
        elif piece_type == 3:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Rook", None, deepcopy(domain)))
        elif piece_type == 4:
            for i in range(num_pieces[piece_type]):
                pieces.append(Piece("Knight", None, deepcopy(domain)))
        else:
            Raise("Wrong type?")


    return pieces, board
        

def test_run():

    # parse
    print("===== TEST RUN =====")
    
    input_filepath = sys.argv[1]
    pieces, board = parse(input_filepath)
    print("board is: \n", board)
    print("pieces are: \n", pieces)

    # initialize CSP
    csp = CSP(board, pieces)

    # CSP backtracking search
    dictionary, board = csp.backtracking_search()

    print("\nSOLUTION!")
    print(repr(board))
    print(dictionary)
    print("===========")

import time

times = []
n = 10
for i in range(n):
    start = time.time()
    test_run()
    end = time.time()
    times.append(end - start)

import statistics
avg = sum(times)/n
stdev = statistics.stdev(times)

print("\ntook ", avg, "s on average\n")
print("stdev was ", stdev)
    

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    
    # parse
    testfile = sys.argv[1]
    pieces, board = parse(testfile)

    # initialize CSP
    csp = CSP(board, pieces)

    # CSP backtracking search
    dictionary, board = csp.backtracking_search()

    return dictionary #Format to be returned

"""
Idea: 
1. each variable is a piece, and the domain is all locations on the board
2. the constraints are such that a piece cannot take up an occupied position or a position under attack. 

We can model an assignment as a given board state. We can model domains as an additional attribute of the 
Piece class. 
"""

# print(run_CSP())