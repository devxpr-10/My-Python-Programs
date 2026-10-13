""" 
Representations:
-1 -> 'O'
0 -> ' '
1 -> 'X'
(Can be modified)

Player -> Minimizing Player
Computer -> Maximizing Player
"""

from brain import * # Ahh... Minimax
import objects

def main():
    board = objects.Board()
    print("Welcome to Tic Tac Toe. Enter 'q' to exit.")
    print(board)    # Print the board
    while True:
        while True:
            loc = input(f"Enter the location to put '{objects.change_nature(board.minimizing)}' in: ").lower()
            if loc == 'q':
                print("Exiting...")
                exit()
            legal, occupied = board.validity(loc)
            if legal and not occupied:
                break
            elif not legal:
                print("Invalid Location! Please enter a valid position.")    
            elif occupied:
                print("This move has already been made. Try again!")
        
        board.put(loc, board.minimizing)

        computer_loc = best_move(board)
        if computer_loc != None: 
            board.put(computer_loc, board.maximizing)
            print(board)    # Print the board
            print(f"Your opponent puts {objects.change_nature(board.maximizing)} at", board.convert_location(computer_loc))

        if board.state() != None:
            break

    print(board)
    match board.state():
        case 1:
            print("COMPUTER HAS WON THE GAME")
        case -1:
            print("YOU HAVE WON THE GAME")
        case 0:
            print("The game was a draw")


if __name__ == '__main__':  # if name is main 
    main()   # call main