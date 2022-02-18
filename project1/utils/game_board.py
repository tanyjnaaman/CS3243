"""
A game state should model an instance of the environment 
and be able to do a goal test. 

In this case, we model it with the BoardState class. 

The state models pieces by encapsulating Piece, Obstacle, Opponent 
and Empty objects. 

It also provides the goal test, actions, action cost and transition functions.
"""

from utils.position import Position

               
class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.positions = {(i, j): Position(i, j) for i in range(columns) for j in range(rows)}

    def clearPosition(self, x, y):
        self.positions.get((x, y)).clearPiece()

    def placePiece(self,x: int, y: int, pieceClass, isFriendly = True):
        position = self.positions.get((x, y))
        piece = pieceClass(position, isFriendly)
        position.placePiece(piece)
        effect, areaOfeffect = piece.getEffects()
        for xy in areaOfeffect:
            x, y = xy
            self.positions.get((x,y)).setEffect(effect)

    def positionIsEmpty(self, x: int, y: int):
        return self.positions.get((x, y)).isEmpty()

    def isValidPosition(self, x: int,  y: int) -> bool:
        return not (self.positions.get((x, y)) == None)
    
    def getPositionEffect(self, x: int, y: int) -> str:
        return self.positions.get((x, y)).getEffect()
    
    def getPositionCost(self,x: int, y: int) -> int:
        return self.positions.get((x, y)).getCost()

    def setPositionCost(self, x: int, y: int, cost: int):
        self.positions.get((x, y)).setCost(cost)

    def getPosition(self, x: int, y: int) -> Position:
        return self.positions.get((x, y))

    def toString(self) -> str:
        out = ""
        verticalSeperator = (self.columns + 1) * 2 * " -" + "\n"
        horizontalSeparator = " | "
        for i in range(self.rows):
            out += verticalSeperator
            row = str(i) + horizontalSeparator
            for j in range(self.columns):
                item = self.positions.get((j, i)).toString()
                row += item + horizontalSeparator
            out += row + "\n"
        
        letters = "  " + horizontalSeparator
        for j in range(self.columns):
            letters += Position.convertXtoAscii(j) + horizontalSeparator
        out += verticalSeperator
        out += letters

        return out

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        
        if not(self.rows == other.rows and self.columns == other.columns):
            return False
        
        return self.positions == other.positions

                
class BoardState:
    def __init__(self, board, player, costToState):
        self.board: Board = board
        self.player = player
        self.costToState: int = costToState

    def isGoal(self):
        return self.player.isAtGoal()

    def getValidNeighbourStates(self):

        # get possible positions of player
        possibleCostAndPieces = self.player.getValidActions(self.board)

        # create new piece with updated position for each move
        states = []
        for p in possibleCostAndPieces:

            moveCost = p[0] 
            pieceWithUpdatedPosition = p[1]

            state = BoardState(self.board,
                player = pieceWithUpdatedPosition, 
                costToState = moveCost)

            states.append(state)

        return states

    def getPlayerActionHistory(self):
        return self.player.getFormattedHistory()

    def __hash__(self) -> int:
        # use hash of player, since board is unchanged
        return hash(self.player)

    def __eq__(self, other):
        if not isinstance(other, BoardState):
            return False
         
        return self.player == other.player



class Node:
    def __init__(self, boardState: BoardState, 
        pathCost: float = 0, 
        parent = None, 
        f = lambda state, pathCost: pathCost + state.costToState):
        
        self.parent = parent
        self.state: BoardState = boardState
        self.pathCost: float = pathCost
        self.f = f
        self.evaluation = f(self.state, self.pathCost) # evaluate at instantiation

    def isGoal(self):
        return self.state.isGoal()

    def getValidNeighbours(self): # returns nodes
        nodes = []
        for state in self.state.getValidNeighbourStates():

            # wrap into nodes, add action cost
            node = Node(boardState = state, 
                pathCost = self.pathCost + state.costToState,
                parent = self,
                f = self.f) 

            nodes.append(node)
        return nodes
    
    def getReturnFormat(self, nodesExplored):
        # traverse linkedlist and return nodesExplored
        return self.state.getPlayerActionHistory(), nodesExplored

    def __lt__(self, other):
        return isinstance(other, Node) and (self.evaluation < other.evaluation)
    
    def __gt__(self, other):
        return isinstance(other, Node) and (self.evaluation > other.evaluation)
    
    def __eq__(self, other):
        return isinstance(other, Node) and (self.evaluation == other.evaluation)
        

            
    

