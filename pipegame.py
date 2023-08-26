from copy import deepcopy


class dirs:
    up, down, left, right = (-1, 0), (1, 0), (0, -1), (0, 1)

    @staticmethod
    def invert(d):
        return -d[0], -d[1]

    @staticmethod
    def calc_move(t1, t2):
        return t1[0] + t2[0], t1[1] + t2[1]


pieces = [
    {"id": 0, "shape": ' ', "name": "empty", "walk": {}},
    {"id": 1, "shape": '║', "name": "vertical", "walk": {dirs.down: dirs.down, dirs.up: dirs.up}},
    {"id": 2, "shape": '═', "name": "horizontal", "walk": {dirs.left: dirs.left, dirs.right: dirs.right}},
    {"id": 3, "shape": '╚', "name": "turn_dirs.up_dirs.right", "walk": {dirs.down: dirs.right, dirs.left: dirs.up}},
    {"id": 4, "shape": '╔', "name": "turn_dirs.right_dirs.down", "walk": {dirs.left: dirs.down, dirs.up: dirs.right}},
    {"id": 5, "shape": '╗', "name": "turn_dirs.down_dirs.left", "walk": {dirs.up: dirs.left, dirs.right: dirs.down}},
    {"id": 6, "shape": '╝', "name": "turn_dirs.left_dirs.up", "walk": {dirs.right: dirs.up, dirs.down: dirs.left}},
    {"id": 7, "shape": '*', "name": "start", "walk": None},
    {"id": 8, "shape": '#', "name": "end", "walk": None},
    {"id": 9, "shape": '.', "name": ".", "walk": {}}
]

l = [[1, 6, 7, 9],
     [8, 1, 5, 1],
     [9, 3, 1, 5],
     [0, 0, 0, 6]]


def pretty_board(l):
    s = ""
    for row in l:
        for ele in row:
            s += pieces[ele["id"]]["shape"]
        s += '\n'
    return s


def replace_board(l, start_dir, end_dir):
    new_l = []
    for i, row in enumerate(l):
        t_l = []
        for j, ele in enumerate(row):
            match ele:
                case 7:
                    pieces[ele]["walk"] = {start_dir: start_dir}
                    start = i, j
                case 8:
                    pieces[ele]["walk"] = {end_dir: end_dir}
                    end = i, j
            t_l.append(pieces[ele])
        new_l.append(t_l.copy())

    return new_l, start, end


N = 4

strongs = [[0, 0, 1, 0],
           [1, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

start_dir, end_dir = dirs.down, dirs.right
l, start, end = replace_board(l, start_dir, end_dir)

# Inserting obvious strong places
strongs[start[0]][start[1]] = 1
strongs[end[0]][end[1]] = 1


def check_inside_borders(i, j):
    return 0 <= i < N and 0 <= j < N


def auto_play(l, start, start_dir, end, end_dir):
    i, j = start

    walk_dir = l[i][j]["walk"][start_dir]
    new_i, new_j = i + walk_dir[0], j + walk_dir[1]
    while (new_i, new_j) != end:
        if not check_inside_borders(new_i, new_j):
            return False
        if walk_dir not in l[new_i][new_j]["walk"]:
            return False
        walk_dir = l[new_i][new_j]["walk"][walk_dir]
        new_i, new_j = new_i + walk_dir[0], new_j + walk_dir[1]
    if walk_dir != (-end_dir[0], -end_dir[1]):
        return False
    return True


# print(auto_play(l, start, start_dir, end, end_dir))
best_sol = 10


def calc_empties(l):
    empties = set()
    for i, row in enumerate(l):
        for j, ele in enumerate(row):
            if ele["id"] == 0:
                empties.add((i, j))
    return empties


def move_restrictions(l, strongs, i, j):
    if not check_inside_borders(i, j):
        return False
    return (not strongs[i][j]) and l[i][j]["id"] > 0


def calc_move(l):
    empties = calc_empties(l)
    moves = []
    for place in empties:
        check = {(t, dirs.invert(d)) for d in [dirs.up, dirs.down, dirs.left, dirs.right] if
                 move_restrictions(l, strongs, *(t := dirs.calc_move(place, d)))}
        if check:
            for c in check:
                moves.append(c)
    return moves


def do_move(l, moves):
    boards = []
    for m in moves:
        dc_l = deepcopy(l)
        place, d = m
        i, j = place
        new_i, new_j = dirs.calc_move(place, d)

        dc_l[new_i][new_j] = dc_l[i][j].copy()
        dc_l[i][j] = pieces[0].copy()
        boards.append((dc_l, (i, j, d)))
    return boards


def calc_n_moves(l, n):
    boards = [(l, [])]
    for _ in range(n):
        print(len(boards))
        next_move_boards = []
        while boards:

            b, mvs = deepcopy(boards.pop())
            for new_b, d in do_move(b, calc_move(b)):
                next_move_boards.append((new_b, mvs.copy() + [d]))

        for b, mvs in next_move_boards:
            if b not in map(lambda x: x[0], boards):
                boards.append((deepcopy(b), mvs.copy()))

    return boards


print(pretty_board(l))
print('-'*80)
b = calc_n_moves(l, 5)
# for b in do_move(l, calc_move(l)):
#     print(pretty_board(b))
for bo, mvs in b:
    # print(pretty_board(bo))
    if auto_play(bo, start, start_dir, end, end_dir):
        print(pretty_board(bo))
        print(mvs)
