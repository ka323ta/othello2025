# Generation ID: Hutch_1765850282371_es3mgscuk (前半)

# from sakura import othello
from copy import deepcopy
# import sys

class StrongAI:
    def __init__(self):
        self.max_depth = 6
        self.corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        self.x_squares = [(1, 1), (1, 6), (6, 1), (6, 6)]
        self.edges = [(0, i) for i in range(8)] + [(7, i) for i in range(8)] + \
                     [(i, 0) for i in range(8)] + [(i, 7) for i in range(8)]

    def next_move(self, board, player):
        legal_moves = self.get_legal_moves(board, player)
        if not legal_moves:
            return None

        best_move = None
        best_value = float('-inf')

        for move in legal_moves:
            new_board = self.make_move(board, move, player)
            value = self.minimax(new_board, self.max_depth - 1, float('-inf'), float('inf'),
                               3 - player, player)
            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    def minimax(self, board, depth, alpha, beta, player, maximizing_player):
        legal_moves = self.get_legal_moves(board, player)

        if depth == 0 or not legal_moves:
            opponent = 3 - player
            opponent_moves = self.get_legal_moves(board, opponent)
            if not opponent_moves:
                return self.evaluate_final(board, maximizing_player)
            if player == maximizing_player:
                return self.evaluate_board(board, player, maximizing_player, len(legal_moves))
            else:
                return self.evaluate_board(board, player, maximizing_player, len(legal_moves))

        if player == maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = self.make_move(board, move, player)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, 3 - player, maximizing_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = self.make_move(board, move, player)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, 3 - player, maximizing_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board, player, maximizing_player, legal_moves_count):
        score = 0

        for i in range(8):
            for j in range(8):
                if board[i][j] == maximizing_player:
                    score += self.evaluate_position(i, j, board, maximizing_player)
                elif board[i][j] == (3 - maximizing_player):
                    score -= self.evaluate_position(i, j, board, 3 - maximizing_player)

        opponent = 3 - player
        opponent_moves = len(self.get_legal_moves(board, opponent))
        mobility_score = (legal_moves_count - opponent_moves) * 20
        score += mobility_score if player == maximizing_player else -mobility_score

        return score

    def evaluate_position(self, i, j, board, player):
        if (i, j) in self.corners:
            return 1000
        if (i, j) in self.x_squares:
            return -300
        if (i, j) in self.edges:
            if self.is_stable_stone(board, i, j, player):
                return 30
            return 5
        return 1

    def is_stable_stone(self, board, i, j, player):
        if board[i][j] != player:
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < 8 and 0 <= nj < 8:
                if board[ni][nj] != player and board[ni][nj] != 0:
                    return False
        return True

    def evaluate_final(self, board, player):
        player_count = sum(row.count(player) for row in board)
        opponent_count = sum(row.count(3 - player) for row in board)
        return (player_count - opponent_count) * 100

    def get_legal_moves(self, board, player):
        legal_moves = []
        N = len(board)
        for i in range(1, N - 1):
            for j in range(1, N - 1):
                if self.is_legal_move(board, i, j, player):
                    legal_moves.append((i, j))
        return legal_moves

    def is_legal_move(self, board, row, col, player):
        if board[row][col] != 0:
            return False

        opponent = 3 - player
        N = len(board)

        for di, dj in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            ni, nj = row + di, col + dj
            found_opponent = False

        while 0 <= ni < N and 0 <= nj < N:
            if board[ni][nj] == opponent:
                found_opponent = True
            elif board[ni][nj] == player:
                if found_opponent:
                    return True
                break
            else:
                break
            ni += di
            nj += dj

        return False


    def make_move(self, board, move, player):
        new_board = deepcopy(board)
        row, col = move
        new_board[row][col] = player
        opponent = 3 - player
        N = len(board)

        for di, dj in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            ni, nj = row + di, col + dj
            flipped = []

            while 0 <= ni < N and 0 <= nj < N:
                if new_board[ni][nj] == opponent:
                    flipped.append((ni, nj))
                elif new_board[ni][nj] == player:
                    for fi, fj in flipped:
                        new_board[fi][fj] = player
                    break
                else:
                    break
                ni += di
                nj += dj

        return new_board


_ai = StrongAI()

def myai(board, player):
    return _ai.next_move(board, player)

# Generation ID: Hutch_1765850282371_es3mgscuk (後半)

# othello.play(ai=StrongAI())
