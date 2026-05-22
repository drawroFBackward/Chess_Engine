import numpy as np


initialArragement = [5, 3, 3.5, 9, 500, 3.5, 3, 5]

board = np.zeros((8, 8))

# setting up board:
for i in range(8):
    for j in range(8):
        if i == 0:
            board[i, j] = 2 * initialArragement[j]
        if i == 1:
            board[i, j] = 2
        if i == 7:
            board[i, j] = initialArragement[j]
        if i == 6:
            board[i, j] = 1


def check_piece_owner(x):
    if x == 1 or x == 3 or x == 3.5 or x == 5 or x == 9 or x == 500:
        return True  # White
    return False  # Black


def white_score(board):
    score = 0
    for i in range(8):
        for j in range(8):
            if check_piece_owner(board[i, j]):
                score = score + board[i, j]
    return score


def black_score(board):
    score = 0
    for i in range(8):
        for j in range(8):
            if not check_piece_owner(board[i, j]):
                score = score + board[i, j]
    return score / 2


def generate_white_moves(board):
    move = np.zeros((8, 8))
    moves = []
    for i in range(8):
        for j in range(8):
            # pawn moves (screw enpassant)
            if board[i, j] == 1:
                # move 2 steps on first move
                if i == 6 and board[5, j] == 0 and board[4, j] == 0:
                    move[i, j] = -1
                    move[i - 2, j] = 1
                    moves.append(move)
                    move = np.zeros((8, 8))
                # pawn push
                if board[i - 1, j] == 0:
                    move[i, j] = -1
                    if i - 1 == 0:
                        # promote to queen
                        move[i - 1, j] = 9
                        moves.append(move)
                        # promote to knight
                        move[i - 1, j] = 3
                        moves.append(move)
                    else:
                        move[i - 1, j] = 1
                        moves.append(move)
                    move = np.zeros((8, 8))
                # pawn capture 1
                if not (
                    board[i - 1, j + 1] == 0 and check_piece_owner(board[i - 1, j + 1])
                ):
                    move[i, j] = -1
                    if i - 1 == 0:
                        # promote to queen
                        move[i - 1, j + 1] = 9 - board[i - 1, j + 1]
                        moves.append(move)
                        # promote to knight
                        move[i - 1, j + 1] = 3 - board[i - 1, j + 1]
                        moves.append(move)
                    else:
                        move[i - 1, j + 1] = 1 - board[i - 1, j + 1]
                        moves.append(move)
                    move = np.zeros((8, 8))
                # pawn capture 2
                if not (
                    board[i - 1, j - 1] == 0 and check_piece_owner(board[i - 1, j - 1])
                ):
                    move[i, j] = -1
                    if i - 1 == 0:
                        # promote to queen
                        move[i - 1, j - 1] = 9 - board[i - 1, j - 1]
                        moves.append(move)
                        # promote to knight
                        move[i - 1, j - 1] = 3 - board[i - 1, j - 1]
                        moves.append(move)
                    else:
                        move[i - 1, j - 1] = 1 - board[i - 1, j - 1]
                        moves.append(move)
                    move = np.zeros((8, 8))
            # knight moves
            # if board[i,j] == 3:
            # bishop moves
            # rook moves
            # queen moves
            # king moves
    return moves


print(board)
print(white_score(board))
print(black_score(board))
