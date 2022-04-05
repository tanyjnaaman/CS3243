from AB import *

def test_run():
    config = sys.argv[1]
    gameboard = parse(config)
    list(gameboard.keys()).sort()
    print("Dictionary is:", gameboard)
    board = parse_gameboard(gameboard)
    print(board)
    eval, move = play(board)
    print("Move is", move)
    print("Eval is:", eval)

# test_run()

def test_game():

    # parse and set up 
    config = sys.argv[1]
    gameboard = parse(config)
    list(gameboard.keys()).sort()
    print("Dictionary is:", gameboard)
    board = parse_gameboard(gameboard)
    print(board)

    # play
    print("\nGame start!\n")
    inp = input()
    while inp != "exit":
        # read move
        start, end = list(map(lambda x: (str(x[0]), int(x[1])), inp.split(","))) # take as a1, a2

        # modify dict
        piece = gameboard.pop(start)
        gameboard[end] = piece
        print(f"MIN PLAYER (you) moved {piece} from {start} to {end}.")

        # parse to board and play
        board = parse_gameboard(gameboard)
        print(board)
        eval, move = play(board)
        print("\n In response, MAX PLAYER move is", move)

        # apply MAX player move
        start, end = move
        piece = gameboard.pop(start)
        gameboard[end] = piece
        board = parse_gameboard(gameboard)
        print(gameboard)
        print(board)

        inp = input()


test_game()