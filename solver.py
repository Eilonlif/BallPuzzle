from copy import deepcopy

from tqdm import tqdm

from board import Board
from directions import Directions


class Solver:
    def __init__(self, board, goal):
        self.board = board
        self.pieces = board.pieces
        self.goal = goal

    @staticmethod
    def auto_play(board):
        walk_dir = board[board.start]["walk"][board.start_dir]
        new_cord = Directions.add_direction_to_coordinate(board.start, walk_dir)
        while new_cord != board.end:
            if not Board.check_inside_borders(*new_cord):
                return False
            if walk_dir not in board[new_cord]["walk"]:
                return False
            walk_dir = board[new_cord]["walk"][walk_dir]
            new_cord = Directions.add_direction_to_coordinate(new_cord, walk_dir)
        return walk_dir == Directions.invert(board.end_dir)

    @staticmethod
    def calc_empties(board):
        empties = set()
        for i, row in enumerate(board.board):
            for j, ele in enumerate(row):
                if ele["id"] == 0:
                    empties.add((i, j))
        return empties

    @staticmethod
    def move_restrictions(board, strong, i, j):
        if not Board.check_inside_borders(i, j):
            return False
        return board[i][j]["id"] > 0 and not strong[i][j]

    @staticmethod
    def calc_move(board):
        empties = Solver.calc_empties(board)
        moves = []
        for place in empties:
            check = {(t, Directions.invert(d)) for d in
                     Directions.all_directions if
                     Solver.move_restrictions(board, board.strong,
                                              *(t := Directions.add_direction_to_coordinate(place, d)))}
            if check:
                for c in check:
                    moves.append(c)
        return moves

    @staticmethod
    def do_move(board, pieces, moves):
        boards = []
        for m in moves:
            deep_copied_board = deepcopy(board)
            place, d = m
            i, j = place
            new_i, new_j = Directions.add_direction_to_coordinate(place, d)

            deep_copied_board[new_i][new_j] = deep_copied_board[i][j].copy()
            deep_copied_board[i][j] = pieces[0].copy()
            boards.append((deep_copied_board, (i, j, d)))
        return boards

    @staticmethod
    def calc_n_moves(board, n, pieces):
        boards = [(board, [])]
        for _ in tqdm(range(n)):
            next_move_boards = []
            while boards:
                b, moves = boards.pop(0)
                for new_b, d in Solver.do_move(b, pieces, Solver.calc_move(b)):
                    next_move_boards.append((deepcopy(new_b), moves + [d]))

            for board, moves in next_move_boards:
                if board not in map(lambda x: x[0], boards):
                    boards.append((deepcopy(board), moves.copy()))

        return boards

    def solve(self):
        for board, moves in self.calc_n_moves(self.board, self.goal, self.pieces):
            if Solver.auto_play(board):
                print(board)
                print(moves)
