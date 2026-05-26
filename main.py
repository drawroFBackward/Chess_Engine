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

def evaluate_board(board):
    return white_score(board) - black_score(board)

# castling rights
white_king_has_moved = False
black_king_has_moved = False
white_kingside_rook_has_moved = False
white_queenside_rook_has_moved = False
black_kingside_rook_has_moved = False
black_queenside_rook_has_moved = False

def is_square_attacked_by_black(board, x, y):
    # check if square (x,y) is attacked by any black piece
    # check for pawn attacks
    if x > 0:
        if y > 0:
            if board[x - 1, y - 1] == 2:
                return True
        if y < 7:
            if board[x - 1, y + 1] == 2:
                return True
    # check for knight attacks
    for dx, dy in [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]:
        if x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
            if board[x + dx, y + dy] == 6:
                return True
    # check for bishop/queen attacks
    for dx, dy in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
        for k in range(1, 8):
            if x + k * dx >= 0 and x + k * dx < 8 and y + k * dy >= 0 and y + k * dy < 8:
                if board[x + k * dx, y + k * dy] == 0:
                    continue
                elif board[x + k * dx, y + k * dy] == 7 or board[x + k * dx, y + k * dy] == 18:
                    return True
                else:
                    break
            else:
                break
    # check for rook/queen attacks
    for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        for k in range(1, 8):
            if x + k * dx >= 0 and x + k * dx < 8 and y + k * dy >= 0 and y + k * dy < 8:
                if board[x + k * dx, y + k * dy] == 0:
                    continue
                elif board[x + k * dx, y + k * dy] == 10 or board[x + k * dx, y + k * dy] == 18:
                    return True
                else:
                    break
            else:
                break
    # check for king attacks
    for dx, dy in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        if x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
            if board[x + dx, y + dy] == 1000:
                return True
    return False

def is_square_attacked_by_white(board, x, y):
    # check if square (x,y) is attacked by any white piece
    # check for pawn attacks
    if x < 7:
        if y > 0:
            if board[x + 1, y - 1] == 1:
                return True
        if y < 7:
            if board[x + 1, y + 1] == 1:
                return True
    # check for knight attacks
    for dx, dy in [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]:
        if x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
            if board[x + dx, y + dy] == 3:
                return True
    # check for bishop/queen attacks
    for dx, dy in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
        for k in range(1, 8):
            if x + k * dx >= 0 and x + k * dx < 8 and y + k * dy >= 0 and y + k * dy < 8:
                if board[x + k * dx, y + k * dy] == 0:
                    continue
                elif board[x + k * dx, y + k * dy] == 3.5 or board[x + k * dx, y + k * dy] == 9:
                    return True
                else:
                    break
            else:
                break
    # check for rook/queen attacks
    for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        for k in range(1, 8):
            if x + k * dx >= 0 and x + k * dx < 8 and y + k * dy >= 0 and y + k * dy < 8:
                if board[x + k * dx, y + k * dy] == 0:
                    continue
                elif board[x + k * dx, y + k * dy] == 5 or board[x + k * dx, y + k * dy] == 9:
                    return True
                else:
                    break
            else:
                break
    # check for king attacks
    for dx, dy in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        if x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
            if board[x + dx, y + dy] == 500:
                return True
    return False

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
            # castling moves
            if board[i, j] == 500:
                # kingside castling
                if not white_king_has_moved and not white_kingside_rook_has_moved:
                    if board[7, 5] == 0 and board[7, 6] == 0 and board[7, 7] == 5:
                        if not is_square_attacked_by_black(board, 7, 4) and not is_square_attacked_by_black(board, 7, 5) and not is_square_attacked_by_black(board, 7, 6):
                            move[i, j] = -500
                            move[7, 6] = 500
                            move[7, 7] = -5
                            move[7, 5] = 5
                            moves.append(move)
                            move = np.zeros((8, 8))
                # queenside castling
                if not white_king_has_moved and not white_queenside_rook_has_moved:
                    if board[7, 1] == 0 and board[7, 2] == 0 and board[7, 3] == 0 and board[7, 0] == 5:
                        if not is_square_attacked_by_black(board, 7, 4) and not is_square_attacked_by_black(board, 7, 3) and not is_square_attacked_by_black(board, 7, 2):
                            move[i, j] = -500
                            move[7, 2] = 500
                            move[7, 0] = -5
                            move[7, 3] = 5
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
            if board[i,j] == 7:
                for x,y in [[-1,-1],[-1,1],[1,-1],[1,1]]:
                    for k in range(1,8):
                        if i+k*x >= 0 and i+k*x < 8 and j+k*y >= 0 and j+k*y < 8:
                            if board[i+k*x,j+k*y] == 0:
                                move[i,j] = -7
                                move[i+k*x,j+k*y] = 7
                                moves.append(move)
                                move = np.zeros((8, 8))
                            elif check_piece_owner(board[i+k*x,j+k*y]):
                                move[i,j] = -7
                                move[i+k*x,j+k*y] = 7 - board[i+k*x,j+k*y]
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
            # castling moves
            if board[i, j] == 1000:
                # kingside castling
                if not black_king_has_moved and not black_kingside_rook_has_moved and board[0, 7] == 10:
                    if board[0, 5] == 0 and board[0, 6] == 0:
                        if not is_square_attacked_by_white(board, 0, 4) and not is_square_attacked_by_white(board, 0, 5) and not is_square_attacked_by_white(board, 0, 6):
                            move[i, j] = -1000
                            move[0, 6] = 1000
                            move[0, 7] = -10
                            move[0, 5] = 10
                            moves.append(move)
                            move = np.zeros((8, 8))
                # queenside castling
                if not black_king_has_moved and not black_queenside_rook_has_moved and board[0, 0] == 10:
                    if board[0, 1] == 0 and board[0, 2] == 0 and board[0, 3] == 0:
                        if not is_square_attacked_by_white(board, 0, 4) and not is_square_attacked_by_white(board, 0, 3) and not is_square_attacked_by_white(board, 0, 2):
                            move[i, j] = -1000
                            move[0, 2] = 1000
                            move[0, 0] = -10
                            move[0, 3] = 10
                            moves.append(move)
                            move = np.zeros((8, 8))
    return moves

# note to self: will have to trigger boleans for castling rights when king or rook moves. also will have to reset them when undoing moves

# minimax algorithm : takes in a board state and returns the best move for the player to move.
def minimax(board, depth, white_to_move = True, best_move = np.zeros((8, 8))):
    # base case: if depth is 0 or game is over, return evaluation of board
    if depth == 0 or evaluate_board(board) > 460 or evaluate_board(board) < -460:
        return evaluate_board(board), best_move
    if white_to_move:
        # next player is black, so set white_to_move to False for next recursion
        white_to_move = False
        max_eval = float('-inf')
        for move in generate_white_moves(board):
            new_board = board + move
            eval, _ = minimax(new_board, depth - 1, white_to_move, best_move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        # next player is white, so set white_to_move to True for next recursion
        white_to_move = True
        min_eval = float('inf')
        for move in generate_black_moves(board):
            new_board = board + move
            eval, _ = minimax(new_board, depth - 1, white_to_move, best_move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move
    
def minimax_alpha_beta(board, depth, alpha, beta, white_to_move = True, best_move = np.zeros((8, 8))):
    # base case: if depth is 0 or game is over, return evaluation of board
    if depth == 0 or evaluate_board(board) > 460 or evaluate_board(board) < -460:
        return evaluate_board(board), best_move
    if white_to_move:
        # next player is black, so set white_to_move to False for next recursion
        white_to_move = False
        max_eval = float('-inf')
        for move in generate_white_moves(board):
            new_board = board + move
            eval, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, white_to_move, best_move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # beta cut-off
        return max_eval, best_move
    else:
        # next player is white, so set white_to_move to True for next recursion
        white_to_move = True
        min_eval = float('inf')
        for move in generate_black_moves(board):
            new_board = board + move
            eval, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, white_to_move, best_move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break # alpha cut-off
        return min_eval, best_move

# mate in 2 test case (white to move):
test_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 500, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 5, 0, 0, 0, 0, 0, 0],
                       [5, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 1000, 0]])

print(minimax_alpha_beta(test_board, 3, float('-inf'), float('inf'), True))