from utils.game_board import Position, Board

class Piece():
    """
    This class is the parent class to all pieces
    used in the game. 
    
    A piece is minimally expected to:
    1. have a goal position and isAtGoal function
    2. keep track of its previous position, like a linkedlist.
    3. return an array of previous positions in a specified format

    Classes that inherit from Piece are expected to have:
    1. getValidActions -> [(cost, Piece), ...] list of move cost and pieces with updated previous to current
    2. isCompatibleEffect -> bool whether a piece can be placed in a position 
                             with a given effect
    3. getEffects -> (effect, [(x, y), ...] effect and AOE that a piece enacts
    4. toString -> to string
    """

    KING = "K"
    OBSTACLE = "O"
    NOT_FRIENDLY = "X"
    QUEEN = "Q"

    def __init__(self, position, goalPosition = None, previousPiece = None, isFriendly = True):
        self.position: Position = position
        self.goalPosition: Position = goalPosition
        self.previousPiece: Piece = previousPiece
        self.isFriendly: bool = isFriendly
        self.type: str = None

    def isAtGoal(self) -> bool:
        return self.position.isAt(self.goalPosition)

    def getFormattedHistory(self) -> list(tuple((str, str))):
        piece = self
        history = []
        while piece.previousPiece != None:
            history.insert(0, piece.position.getPositionAsAsciiTuple())
            piece = piece.previousPiece
        return history

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        
        return (self.position == other.position
            and self.goalPosition == other.goalPosition
            and self.isFriendly == other.isFriendly
            and self.type == other.type)

    def __hash__(self) -> int:
        # use hash of tuple of attributes to hash

        key = (self.position.getPositionAscii(), 
            self.goalPosition.getPositionAscii(), 
            self.type, 
            self.isFriendly)
        h = hash(key)
        # print(key)
        # print(h)
        return h

    def __str__(self) -> str:
        return self.type + ", " + str(self.position) + ", isFriendly:" + str(self.isFriendly)


class KingPiece(Piece):
    """
    Encapsulates behaviour of the King Piece.
    """
    def __init__(self, position, goalPosition = None, previousPiece = None, isFriendly = True):
        super(KingPiece, self).__init__(position, goalPosition, previousPiece, isFriendly)
        self.type = Piece.KING
        if not self.isFriendly:
            self.type += Piece.NOT_FRIENDLY

    
    def getValidActions(self, board: Board) -> list((int, Piece)): # returns list of KingPiece with previous position
        """
        Returns valid positions King piece can move to, given a board
        and using its (self) current position.

        @param board    game board.
        @return         list of KingPieces with updated previous positions
                        to current position and move cost. King can move 
                        in eight directions.
        """

        validActions = []

        x, y = self.position.getPositionIndices()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                if (xOffset == 0) and (yOffset == 0):
                    continue # ignore itself

                newX = x + xOffset
                newY = y + yOffset

                if (board.isValidPosition(newX, newY) 
                    and board.positionIsEmpty(newX, newY) 
                    and self.isCompatibleEffect(board.getPositionEffect(newX, newY))):
                    
                    newPosition = board.getPosition(newX, newY)
                    newPiece = KingPiece(newPosition, self.goalPosition, self)
                    costToNewPosition = board.getPositionCost(newX, newY)
                    validActions.append((costToNewPosition, newPiece))

        return validActions

    def isCompatibleEffect(self, effect: str) -> bool: # King cannot place at any piece AOE
        """
        Returns true if King piece is compatible with effect.

        @param effect   String variable describing effect.
        @return         False, King cannot be placed in any position with effect.
        """

        return effect == None

    
    def getEffects(self) -> tuple((str, list(tuple((int, int))))):
        """
        Returns area of effect of king piece. 

        @return ("K", [(x, y), ...]) effect and list of (x,y) 
                describing area of effect.
        """
        areaOfEffect = []
        x, y = self.position.getPositionIndices()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                if (xOffset == 0) and (yOffset == 0):
                    continue # ignore itself
                newX = x + xOffset
                newY = y + yOffset
                areaOfEffect.append((newX, newY))
        effect = self.type
        return effect, areaOfEffect

    def toString(self) -> str:
        return self.type


class ObstaclePiece(Piece):
    """
    Encapsulates behaviour of the Obstacle Piece.
    """
    def __init__(self, position, goalPosition = None, previousPiece = None, isFriendly = True):
        super(ObstaclePiece, self).__init__(position, goalPosition, previousPiece, isFriendly)
        self.type = Piece.OBSTACLE
        if not self.isFriendly:
            self.type += Piece.NOT_FRIENDLY

    
    def getValidActions(self, board: Board) -> list((int, Piece)): # returns list of KingPiece with previous position
        """
        Returns valid positions Obstacle piece can move to, given a board
        and using its (self) current position.

        @param board    game board.
        @return         [], empty list. Obstacle cannot move.
        """
        validActions = []

        return validActions

    def isCompatibleEffect(self, effect: str) -> bool: # King cannot place at any piece AOE
        """
        Returns true if Obstacle piece is compatible with effect.

        @param effect   String variable describing effect.
        @return         True, obstacle can be placed anywhere.
        """
        return True

    
    def getEffects(self) -> tuple((str, list(tuple((int, int))))):
        """
        Returns area of effect of Obstacle piece. 

        @return ("O", []), since obstacle has no effect.
        """

        effect = self.type
        areaOfEffect = []

        return effect, areaOfEffect

    def toString(self) -> str:
        return self.type

class QueenPiece(Piece):
    """
    Encapsulates behaviour of the Queen Piece.
    """
    def __init__(self, position, goalPosition = None, previousPiece = None):
        super(QueenPiece, self).__init__(position, goalPosition, previousPiece)
        self.type = Piece.QUEEN
        if not self.isFriendly:
            self.type += Piece.NOT_FRIENDLY
        
    
    def getValidActions(self, board: Board) -> list((int, Piece)): # returns list of KingPiece with previous position
        """
        Returns valid positions piece can move to, given a board
        and using its (self) current position.

        @param board    game board.
        @return         list of (cost, Piece) tuples. Queen can move radially
                        in any direction, any number of steps. 
        """
        validActions = []

        # search radially outwards, terminating in that direction if obstacle met
        


        return validActions

    def isCompatibleEffect(self, effect: str) -> bool: # King cannot place at any piece AOE
        """
        Returns true if piece is compatible with effect.

        @param effect   String variable describing effect.
        @return         
        """
        return 

    
    def getEffects(self) -> tuple((str, list(tuple((int, int))))):
        """
        Returns area of effect of piece. 

        @return 
        """


        return effect, areaOfEffect

    def toString(self) -> str:
        return self.type

