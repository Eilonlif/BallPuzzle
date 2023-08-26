from directions import Directions
from pieces import Pieces


class Board:
    N = 4

    def __init__(self, board, strongs, start_dir, end_dir):
        self.board = board
        self.strongs = strongs
        self.pieces = Pieces()
        self.start_dir = start_dir
        self.end_dir = end_dir

        self.board, self.start, self.end = self.replace_board()

    def __str__(self):
        s = ""
        for row in self.board:
            for ele in row:
                s += self.pieces[ele["id"]]["shape"]
            s += '\n'
        return s

    def __getitem__(self, item):
        return self.board[item]

    def replace_board(self):
        new_board = []
        start, end = None, None
        for i, row in enumerate(self.board):
            tmp_board = []
            for j, ele in enumerate(row):
                if ele == 7:
                    self.pieces[ele]["walk"] = {self.start_dir: self.start_dir}
                    start = i, j
                elif ele == 8:
                    self.pieces[ele]["walk"] = {self.end_dir: self.end_dir}
                    end = i, j
                tmp_board.append(self.pieces[ele])
            new_board.append(tmp_board.copy())
        if start is None or end is None:
            raise ValueError()
        return new_board, start, end

    @staticmethod
    def check_inside_borders(i, j):
        return 0 <= i < Board.N and 0 <= j < Board.N


