class Position:

    ASCII_OFFSET = 97

    def __init__(self, x, y, cost = 1, piece = None):
        self.x: int = x
        self.y: int = y
        self.cost: int = cost
        self.piece = piece # piece or obstacle
        self.effect: str = None

    def getPositionAscii(self) -> str:
        return self.xToAscii() + str(self.y)

    def getPositionAsAsciiTuple(self):
        return (self.xToAscii(), self.y)

    def xToAscii(self):
        return Position.convertXtoAscii(self.x)

    def getPositionIndices(self):
        return (self.x, self.y)

    def convertAsciiToXy(asciiPosition: str) -> tuple((int, int)):
        x, y = asciiPosition[0], asciiPosition[1:]
        x = ord(x) - Position.ASCII_OFFSET
        return int(x), int(y)

    def convertXtoAscii(x: int) -> str:
        return chr(Position.ASCII_OFFSET + x)

    def placePiece(self, piece):
        self.piece = piece

    def clearPiece(self):
        self.piece = None

    def isAt(self, position):
        if position != None:
            return (self.x == position.x) and (self.y == position.y)
        else:
            raise Exception("position is None!")

    def isEmpty(self):
        return self.piece == None

    def getCost(self):
        return self.cost

    def setCost(self, cost: int):
        self.cost = cost

    def setEffect(self, effect: str):
        self.effect = effect

    def getEffect(self):
        return self.effect

    def toString(self):
        if self.piece != None:
            return self.piece.toString()
        
        return " "
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        
        if (self.x != other.x) or (self.y != other.y) or (self.cost != other.cost):
            return False
        
        return (self.piece == other.piece) and (self.effect == other.effect)

    def __str__(self) -> str:
        return self.getPositionAscii()
