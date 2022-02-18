from queue import PriorityQueue
from utils.game_board import Node

def bestFirstSearch(initialNode: Node, f = lambda x : 1):

    # initialize
    frontier = PriorityQueue()
    frontier.put(initialNode)
    reached = {initialNode.state.player : initialNode}
    nodesExplored = 0
    newNodes = 0

    # graph search
    while not frontier.empty():
        # increment counter and get new node
        nodesExplored += 1
        if nodesExplored % 100 == 0:
            print(f"explored {nodesExplored} nodes. frontier size is {len(reached)}")
        currentNode = frontier.get()

        # goal test
        if currentNode.isGoal():
            return currentNode.getReturnFormat(nodesExplored)

        # explore    
        else: 
            neighbourNodes = currentNode.getValidNeighbours() # expand
            for neighbour in neighbourNodes:
                state = neighbour.state
                newPathCost = neighbour.pathCost
                if reached.get(state.player) == None:
                    newNodes += 1
                    print(f"new node: {newNodes}")
                    # print(state.player)
                    # print(hash(state.player))
                    # print(reached.get(state.player))
                    reached[state.player] = neighbour
                    # print(reached.get(state.player))
                    frontier.put(neighbour)
                if (newPathCost < reached.get(state.player).pathCost):
                    print(f"cheaper path: {newPathCost} vs {reached.get(state).pathCost}")
                    reached[state.player] = neighbour
                    frontier.put(neighbour)
                    
    return None

