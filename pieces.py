from directions import Directions


class Pieces:
    def __init__(self):
        self.pieces = [
            {"id": 0, "shape": ' ', "walk": {}},
            {"id": 1, "shape": '║', "walk": {Directions.down: Directions.down, Directions.up: Directions.up}},
            {"id": 2, "shape": '═', "walk": {Directions.left: Directions.left, Directions.right: Directions.right}},
            {"id": 3, "shape": '╚', "walk": {Directions.down: Directions.right, Directions.left: Directions.up}},
            {"id": 4, "shape": '╔', "walk": {Directions.left: Directions.down, Directions.up: Directions.right}},
            {"id": 5, "shape": '╗', "walk": {Directions.up: Directions.left, Directions.right: Directions.down}},
            {"id": 6, "shape": '╝', "walk": {Directions.right: Directions.up, Directions.down: Directions.left}},
            {"id": 7, "shape": '*', "walk": None},
            {"id": 8, "shape": '#', "walk": None},
            {"id": 9, "shape": '.', "walk": {}}
        ]

    def __getitem__(self, item):
        return self.pieces[item]
