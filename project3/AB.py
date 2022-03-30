import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:

    PIECES = {
    "King": "K",
    "Queen": "Q",
    "Rook": "R",
    "Bishop": "B",
    "Knight": "N",
    "PAWN": "P",
    "Attack": "!"
    }

    ASCII_OFFSET = ord('a')

    def __init__(self, 
        piece_type : str,
        current_position : tuple,
        player : bool):

        # metadata
        self.piece_type : str  = piece_type
        self.symbol : str = self.PIECES[self.piece_type]

        # functional data
        self.current_position : tuple = current_position
        self.player : bool = player

    def possibleplays(self, board) -> list: # list of (start, stop)
        
        col, row = self.current_position

        # ===== HELPER FUNCTIONS =====

        def kingplays():
            possibleplays = []
            for col_offset in range(-1, 2):
                for row_offset in range(-1, 2):

                    # ignore current position
                    if row_offset == 0 and col_offset == 0:
                        continue
                        
                    # find valid positions
                    new_col = col + col_offset
                    new_row = row + row_offset
                    new_position = (new_col, new_row)

                    # valid position, unoccupied or can attack
                    if (board.positioninboard(new_position)
                        and (not board.positionoccupiedboard(new_position))
                        or board.pieceatposition_differentplayer(new_position, self.player)):
                        possibleplays.append(new_position)

            return possibleplays

        
        def queenplays():
            possibleplays = []

            # go left
            for col_offset in range(1, board.columns):

                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)
                
                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)

                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break
                
            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                if row_offset == 0:
                    continue

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            return possibleplays

        def rookplays():
            possibleplays = []

            # go left
            for col_offset in range(1, board.columns):
                new_col = col - col_offset
                new_row = row
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                 
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go right
            for col_offset in range(1, board.columns):
                new_col = col + col_offset
                new_row = row
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)

                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go up
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row + row_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down
            for row_offset in range(1, board.rows):
                new_col = col 
                new_row = row - row_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            return possibleplays

        def bishopplays():
            possibleplays = []

            # diagonals have a max bound
            max_offset = max(board.rows, board.columns)

            # go up left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)
                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go up right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row + diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down left
            for diagonal_offset in range(1, max_offset):
                new_col = col - diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            # go down right
            for diagonal_offset in range(1, max_offset):
                new_col = col + diagonal_offset
                new_row = row - diagonal_offset
                new_position = (new_col, new_row)

                # valid position, unoccupied or can attack
                if (board.positioninboard(new_position)
                    and (not board.positionoccupiedboard(new_position))
                    or board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
                
                if (board.positioninboard(new_position) 
                    and board.positionoccupied(new_position)):                    
                    break

            return possibleplays
        
        def knightplays():
            possibleplays = []
            offset_1 = [1, -1]
            offset_2 = [2, -2]

            # col offset by 1, row offset by 2
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_1
                    new_row = row + delta_2
                    new_position = (new_col, new_row)

                    # valid position, unoccupied or can attack
                    if (board.positioninboard(new_position)
                        and (not board.positionoccupiedboard(new_position))
                        or board.pieceatposition_differentplayer(new_position, self.player)):
                        possibleplays.append(new_position)


            # col offset by 2, row offset by 1
            for delta_1 in offset_1:
                for delta_2 in offset_2:
                    new_col = col + delta_2
                    new_row = row + delta_1
                    new_position = (new_col, new_row)

                    # valid position, unoccupied or can attack
                    if (board.positioninboard(new_position)
                        and (not board.positionoccupiedboard(new_position))
                        or board.pieceatposition_differentplayer(new_position, self.player)):
                        possibleplays.append(new_position)

            return possibleplays  

        def pawnplays():

            possibleplays = []

            direction = 1 
            if not self.player: # is MIN player, go in negative direction vertically
                direction *= -1

            # attacks
            for col_offset in (-1, 1):
                new_col = col + col_offset
                new_row = row + direction
                new_position = (new_col, new_row)
                if (board.positioninboard(new_position)
                    and board.pieceatposition_differentplayer(new_position, self.player)):
                    possibleplays.append(new_position)
            
            
            # move
            new_col = col
            new_row = row + direction
            new_position = (new_col, new_row)
            if (board.positioninboard(new_position)
                and not board.positionoccupiedboard(new_position)):
                possibleplays.append(new_position)

        
        if self.piece_type == "King":
            return kingplays()
        elif self.piece_type == "Queen":
            return queenplays()
        elif self.piece_type == "Rook":
            return rookplays()
        elif self.piece_type == "Bishop":
            return bishopplays()
        elif self.piece_type == "Knight":
            return knightplays()

        elif self.piece_type == "Rook":
            return pawnplays()
        else:
            # pass
            raise RuntimeError("Unidentified piece type calling Piece.possibleMoves_upTo")
        
    @staticmethod
    def asciituple_to_xy(ascii_position: str) -> tuple((int, int)):
        assert(len(ascii_position) <= 3)
        col, row = ascii_position[0], ascii_position[1:]
        col, row = int(ord(col) - Piece.ASCII_OFFSET), int(row)
        return (col, row)

    @staticmethod
    def xy_to_asciituple(position: tuple((int, int))) -> str:
        col, row = position
        return (chr(col + Piece.ASCII_OFFSET), row)

    def position_as_asciituple(self):
        return Piece.xy_to_asciituple(self.current_position)

    def setposition(self, position: tuple):
        self.current_position = position

    def clearposition(self):
        self.current_position = None

    def __repr__(self) -> str:
        if not self.player:
            return "\033[1;33m" + self.symbol + "\033[0;0m" # red
            
        return "\033[1;32m" + self.symbol + "\033[0;0m" # green

    def __str__(self) -> str:
        return self.symbol


class Board:
    pass

#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    pass

def alphabeta(board : Board, depth : int, alpha, beta, maximisingplayer : bool) -> tuple: # returns starting position of piece to next position

    if depth == 0 or board.isterminal():
        return board.evaluate(depth), None

    bestplay = None
    
    possibleplays = board.getpossiblemoves(maximisingplayer)

    # ===== MAX PLAYER =====
    if maximisingplayer: # == 1
        value = -1
        for play in possibleplays:
            childstate = board.applyplay(play)
            
            # if better than current value, record
            downstreamvalue, _ = alphabeta(childstate, depth - 1, alpha, beta, not maximisingplayer)
            if downstreamvalue > value:
                value = downstreamvalue
                bestplay = play

            alpha = max(alpha, value) # record max so far for every child

            # prune
            if value >= beta: 
                break # beta cutoff, since value propagated up larger than seen so far, min player won't play

    # ===== MIN PLAYER =====
    else:
        value = 2**32
        for play in possibleplays:
            childstate = board.applyplay(play)
            
            # if better than current value, record
            downstreamvalue, _ = alphabeta(childstate, depth - 1, alpha, beta, not maximisingplayer)
            if downstreamvalue < value:
                value = downstreamvalue
                bestplay = play

            beta = min(beta, value) # record max so far for every child

            # prune
            if value <= alpha: 
                break # alpha cutoff, since value propagated up smaller than seen so far, max player won't play

    return value, bestplay
    







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
