
from utils.game_board import Board, Position, BoardState, Node
from utils.pieces import ObstaclePiece, KingPiece

class Parser:
    def __init__(self):
        self.DEFAULT_COST = 1

    def readValueAfterRegex(self, regex: str) -> str: 
        """
        Reads in second argument of string split by regex.
        e.g. Rows:21 -> returns "21"
        """ 
        line = input()
        line = line.split(regex)[1]
        if line == "-":
            return None
        return line

    def readSequenceAfterRegex(self, regex: str, separator: str, line: str = None) -> list: 
        """
        Reads in second argument of string split by regex.
        e.g. Rows:21 -> returns "21"
        """ 
        # read input if none provided
        if line == None:
            line = input()

        # read
        line = line.split(regex)[1:][0]
        if line == "-":
            return []
        line = line.split(separator)
        return line

    def parseTuple(self, line: str, separator: str, brackets: str) -> tuple((str, str)):
        line = line.strip().strip(brackets)
        return line.split(separator)

    def skipLine(self):
        line = input()
        return None

    def read(self) -> Node:

        # read rows, cols, create empty board
        rows = int(self.readValueAfterRegex(":"))
        cols = int(self.readValueAfterRegex(":"))
        board = Board(rows, cols)

        # read in number/positions of obstacles, populate
        numObstacles = int(self.readValueAfterRegex(":"))
        obstaclePositions = self.readSequenceAfterRegex(":", " ")
        for i in obstaclePositions:
            x, y = Position.convertAsciiToXy(i)
            board.placePiece(x, y, ObstaclePiece)

        # read in costs and update
        self.skipLine()
        line = input()
        while "[" in line:            
            # convert and set
            asciiPosition, cost = self.parseTuple(line, ",", "[]")
            x, y = Position.convertAsciiToXy(asciiPosition)
            board.setPositionCost(x, y, float(cost))

            # read new input
            line = input()

        # read in number/positions of enemy pieces, populate
        numEnemy = self.readSequenceAfterRegex(":", " ", line = line)
        enemyPositions = self.readSequenceAfterRegex(":", " ")
        self.skipLine()
        self.skipLine()

        line = input()
        pieceType, asciiPosition = self.parseTuple(line, ",", "[]")
        x, y = Position.convertAsciiToXy(asciiPosition)
        goalPosition = self.readValueAfterRegex(":")
        xGoal, yGoal = Position.convertAsciiToXy(goalPosition)
        player = KingPiece(board.getPosition(x, y), board.getPosition(xGoal, yGoal))

        boardState = BoardState(board, player, 0)
        startNode = Node(boardState)
        print(board.toString())
        return startNode

        

        # read in number/positions of self pieces
        # read in goal positions
        # wrap goal positions into playable pieces, players into states

        # create initial node and state, return initial node







