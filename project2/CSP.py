import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

def 

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.

    goalState = search()
    return goalState #Format to be returned

"""
Idea: we want to begin by assigning variables, domains and constraints.

Variables: implicitly modelled by the board
Domains: a new data structure needed to keep track
constraints: implicitly modelled by a check

1. initialization: We can initialize sets of variables, domains and constraints
2. baktracking algorithm 
"""