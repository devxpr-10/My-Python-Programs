from math import inf
from objects import Board

def minimax(board: Board, maximizing: bool):
    if (winner := board.state()) != None:
        return winner

    if maximizing:
        best_score = -inf
        for i, j in board.empty_locations():
            board.put((i, j), board.maximizing)
            score = minimax(board, False)
            board.put((i, j), " ")

            best_score = max(score, best_score)
            
        return best_score
    else:
        best_score = inf
        for i, j in board.empty_locations():
            board.put((i, j), board.minimizing)
            score = minimax(board, True)
            board.put((i, j), " ")

            best_score = min(score, best_score)

        return best_score

def best_move(board: Board) -> tuple | None:
    best_score = -inf
    move = None

    for i, j in board.empty_locations():
        board.put((i, j), board.maximizing)

        score = minimax(board, False)

        board.put((i, j), " ")

        if score > best_score:
            best_score  = score
            move = (i, j)

    return move