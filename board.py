from pieces import Pieces


class Board:
    N = 4

    def __init__(self, board, strong, start_dir, end_dir):
        self.board = board
        self.strong = strong
        self.start_dir = start_dir
        self.end_dir = end_dir

        self.pieces = Pieces()
        self.pieces[7]["walk"] = {self.start_dir: self.start_dir}
        self.pieces[8]["walk"] = {self.end_dir: self.end_dir}

        self.start, self.end = self.find_start_end()
        self.board = self.replace_board()

    def __str__(self):
        s = ""
        for row in self.board:
            for ele in row:
                s += self.pieces[ele["id"]]["shape"]
            s += '\n'
        return s

    def __getitem__(self, item):
        match item:
            case (_, _):
                return self.board[item[0]][item[1]]
            case _:
                return self.board[item]

    def find_start_end(self):
        start, end = None, None
        for i, row in enumerate(self.board):
            for j, ele in enumerate(row):
                if ele == 7:
                    start = i, j
                elif ele == 8:
                    end = i, j

        start_end = [start, end]
        if start is None or end is None:
            raise ValueError("Start or end tile are missing!")
        return start_end

    def replace_board(self):
        new_board = []
        for i, row in enumerate(self.board):
            tmp_board = []
            for j, ele in enumerate(row):
                tmp_board.append(self.pieces[ele])
            new_board.append(tmp_board.copy())
        return new_board

    @staticmethod
    def check_inside_borders(i, j):
        return 0 <= i < Board.N and 0 <= j < Board.N
