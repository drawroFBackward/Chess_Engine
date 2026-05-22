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
                if j + 1 < 8:
                    if not (
                        board[i - 1, j + 1] == 0 or check_piece_owner(board[i - 1, j + 1])
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
                if j - 1 >= 0:
                    if not (
                        board[i - 1, j - 1] == 0 or check_piece_owner(board[i - 1, j - 1])
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
            if board[i,j] == 3:
                for x,y in [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]:
                    if i+x >= 0 and i+x < 8 and j+y >= 0 and j+y < 8:
                        if board[i+x,j+y] == 0 or not check_piece_owner(board[i+x,j+y]):
                            move[i,j] = -3
                            move[i+x,j+y] = 3 - board[i+x,j+y]
                            moves.append(move)
                            move = np.zeros((8, 8))
            # bishop moves
            if board[i,j] == 3.5:
                for x,y in [[-1,-1],[-1,1],[1,-1],[1,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -3.5
                                move[i+k*x,j+k*y] = 3.5
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif not check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -3.5
                                move[i+k*x,j+k*y] = 3.5 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # rook moves
            if board[i,j] == 5:
                for x,y in [[-1,0],[1,0],[0,-1],[0,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -5
                                move[i+k*x,j+k*y] = 5
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif not check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -5
                                move[i+k*x,j+k*y] = 5 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # queen moves
            if board[i,j] == 9:
                for x,y in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -9
                                move[i+k*x,j+k*y] = 9
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif not check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -9
                                move[i+k*x,j+k*y] = 9 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # king moves
            if board[i,j] == 500:
                for x,y in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                    if i+x >= 0 and i+x < 8 and j+y >= 0 and j+y < 8:
                        if board[i+x,j+y] == 0 or not check_piece_owner(board[i+x,j+y]):
                            move[i,j] = -500
                            move[i+x,j+y] = 500 - board[i+x,j+y]
                            moves.append(move)
                            move = np.zeros((8, 8))
    return moves

def generate_black_moves(board):
    move = np.zeros((8, 8))
    moves = []
    for i in range(8):
        for j in range(8):
            # pawn moves (screw enpassant)
            if board[i, j] == 2:
                # move 2 steps on first move
                if i == 1 and board[2, j] == 0 and board[3, j] == 0:
                    move[i, j] = -2
                    move[i + 2, j] = 2
                    moves.append(move)
                    move = np.zeros((8, 8))
                # pawn push
                if board[i + 1, j] == 0:
                    move[i, j] = -2
                    if i + 1 == 7:
                        # promote to black queen
                        move[i + 1, j] = 18
                        moves.append(move)
                        # promote to black knight
                        move[i + 1, j] = 6
                        moves.append(move)
                    else:
                        move[i + 1, j] = 2
                        moves.append(move)
                    move = np.zeros((8, 8))
                # pawn capture 1
                if j + 1 < 8:
                    if not (
                        board[i + 1, j + 1] == 0 or not check_piece_owner(board[i + 1, j + 1])
                    ):
                        move[i, j] = -2
                        if i + 1 == 7:
                            # promote to black queen
                            move[i + 1, j + 1] = 18 - board[i + 1, j + 1]
                            moves.append(move)
                            # promote to black knight
                            move[i + 1, j + 1] = 6 - board[i + 1, j + 1]
                            moves.append(move)
                        else:
                            move[i + 1, j + 1] = 2 - board[i + 1, j + 1]
                            moves.append(move)
                        move = np.zeros((8, 8))
                # pawn capture 2
                if j - 1 >= 0:
                    if not (
                        board[i + 1, j - 1] == 0 or not check_piece_owner(board[i + 1, j - 1])
                    ):
                        move[i, j] = -2
                        if i + 1 == 7:
                            # promote to black queen
                            move[i + 1, j - 1] = 18 - board[i + 1, j - 1]
                            moves.append(move)
                            # promote to black knight
                            move[i + 1, j - 1] = 6 - board[i + 1, j - 1]
                            moves.append(move)
                        else:
                            move[i + 1, j - 1] = 2 - board[i + 1, j - 1]
                            moves.append(move)
                        move = np.zeros((8, 8))
            # knight moves
            if board[i,j] == 6:
                for x,y in [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]:
                    if i+x >= 0 and i+x < 8 and j+y >= 0 and j+y < 8:
                        if board[i+x,j+y] == 0 or check_piece_owner(board[i+x,j+y]):
                            move[i,j] = -6
                            move[i+x,j+y] = 6 - board[i+x,j+y]
                            moves.append(move)
                            move = np.zeros((8, 8))
            # bishop moves
            if board[i,j] == 6.5:
                for x,y in [[-1,-1],[-1,1],[1,-1],[1,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -6.5
                                move[i+k*x,j+k*y] = 6.5
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -6.5
                                move[i+k*x,j+k*y] = 6.5 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # rook moves
            if board[i,j] == 10:
                for x,y in [[-1,0],[1,0],[0,-1],[0,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -10
                                move[i+k*x,j+k*y] = 10
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -10
                                move[i+k*x,j+k*y] = 10 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # queen moves
            if board[i,j] == 18:
                for x,y in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -18
                                move[i+k*x,j+k*y] = 18
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -18
                                move[i+k*x,j+k*y] = 18 - board[i+k*x,j+k*y]
                                moves.append(move)
                                move = np.zeros((8, 8))
                                break # can't move past capture
                            else:
                                break # own piece blocking
                        else:
                            break # out of bounds
            # king moves
            if board[i,j] == 1000:
                for x,y in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                    if i+x >= 0 and i+x < 8 and j+y >= 0 and j+y < 8:
                        if board[i+x,j+y] == 0 or check_piece_owner(board[i+x,j+y]):
                            move[i,j] = -1000
                            move[i+x,j+y] = 1000 - board[i+x,j+y]
                            moves.append(move)
                            move = np.zeros((8, 8))
    return moves

print(board)
print(generate_black_moves(board))
