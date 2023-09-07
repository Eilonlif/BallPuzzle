from board import Board
from directions import Directions
from solver import Solver

if __name__ == "__main__":
    board = [[1, 6, 7, 9],
             [8, 1, 5, 1],
             [9, 3, 1, 5],
             [0, 0, 0, 6]]

    strong = [[0, 0, 1, 0],
              [1, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

    start_dir, end_dir = Directions.down, Directions.right

    b = Board(board, strong, start_dir, end_dir)
    s = Solver(b, goal=5)

    s.solve()
