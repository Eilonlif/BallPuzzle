class Directions:
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    all_directions = [up, down, left, right]

    @staticmethod
    def invert(d):
        return -d[0], -d[1]

    @staticmethod
    def add_direction_to_coordinate(t1, t2):
        return t1[0] + t2[0], t1[1] + t2[1]
