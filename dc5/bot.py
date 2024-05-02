import random
import math

N = 96

COORDS = [(-3, 0, 4), (-3, 1, 3), (-3, 1, 4), (-3, 2, 2), (-3, 2, 3), (-3, 3, 1), (-3, 3, 2), (-3, 4, 0), (-3, 4, 1), (-2, -1, 4), (-2, 0, 3), (-2, 0, 4), (-2, 1, 2), (-2, 1, 3), (-2, 2, 1), (-2, 2, 2), (-2, 3, 0), (-2, 3, 1), (-2, 4, -1), (-2, 4, 0), (-1, -2, 4), (-1, -1, 3), (-1, -1, 4), (-1, 0, 2), (-1, 0, 3), (-1, 1, 1), (-1, 1, 2), (-1, 2, 0), (-1, 2, 1), (-1, 3, -1), (-1, 3, 0), (-1, 4, -2), (-1, 4, -1), (0, -3, 4), (0, -2, 3), (0, -2, 4), (0, -1, 2), (0, -1, 3), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 2, -1), (0, 2, 0), (0, 3, -2), (0, 3, -1), (0, 4, -3), (0, 4, -2), (1, -3, 3), (1, -3, 4), (1, -2, 2), (1, -2, 3), (1, -1, 1), (1, -1, 2), (1, 0, 0), (1, 0, 1), (1, 1, -1), (1, 1, 0), (1, 2, -2), (1, 2, -1), (1, 3, -3), (1, 3, -2), (1, 4, -3), (2, -3, 2), (2, -3, 3), (2, -2, 1), (2, -2, 2), (2, -1, 0), (2, -1, 1), (2, 0, -1), (2, 0, 0), (2, 1, -2), (2, 1, -1), (2, 2, -3), (2, 2, -2), (2, 3, -3), (3, -3, 1), (3, -3, 2), (3, -2, 0), (3, -2, 1), (3, -1, -1), (3, -1, 0), (3, 0, -2), (3, 0, -1), (3, 1, -3), (3, 1, -2), (3, 2, -3), (4, -3, 0), (4, -3, 1), (4, -2, -1), (4, -2, 0), (4, -1, -2), (4, -1, -1), (4, 0, -3), (4, 0, -2), (4, 1, -3)]
INDICES = {(-3, 0, 4): 0, (-3, 1, 3): 1, (-3, 1, 4): 2, (-3, 2, 2): 3, (-3, 2, 3): 4, (-3, 3, 1): 5, (-3, 3, 2): 6, (-3, 4, 0): 7, (-3, 4, 1): 8, (-2, -1, 4): 9, (-2, 0, 3): 10, (-2, 0, 4): 11, (-2, 1, 2): 12, (-2, 1, 3): 13, (-2, 2, 1): 14, (-2, 2, 2): 15, (-2, 3, 0): 16, (-2, 3, 1): 17, (-2, 4, -1): 18, (-2, 4, 0): 19, (-1, -2, 4): 20, (-1, -1, 3): 21, (-1, -1, 4): 22, (-1, 0, 2): 23, (-1, 0, 3): 24, (-1, 1, 1): 25, (-1, 1, 2): 26, (-1, 2, 0): 27, (-1, 2, 1): 28, (-1, 3, -1): 29, (-1, 3, 0): 30, (-1, 4, -2): 31, (-1, 4, -1): 32, (0, -3, 4): 33, (0, -2, 3): 34, (0, -2, 4): 35, (0, -1, 2): 36, (0, -1, 3): 37, (0, 0, 1): 38, (0, 0, 2): 39, (0, 1, 0): 40, (0, 1, 1): 41, (0, 2, -1): 42, (0, 2, 0): 43, (0, 3, -2): 44, (0, 3, -1): 45, (0, 4, -3): 46, (0, 4, -2): 47, (1, -3, 3): 48, (1, -3, 4): 49, (1, -2, 2): 50, (1, -2, 3): 51, (1, -1, 1): 52, (1, -1, 2): 53, (1, 0, 0): 54, (1, 0, 1): 55, (1, 1, -1): 56, (1, 1, 0): 57, (1, 2, -2): 58, (1, 2, -1): 59, (1, 3, -3): 60, (1, 3, -2): 61, (1, 4, -3): 62, (2, -3, 2): 63, (2, -3, 3): 64, (2, -2, 1): 65, (2, -2, 2): 66, (2, -1, 0): 67, (2, -1, 1): 68, (2, 0, -1): 69, (2, 0, 0): 70, (2, 1, -2): 71, (2, 1, -1): 72, (2, 2, -3): 73, (2, 2, -2): 74, (2, 3, -3): 75, (3, -3, 1): 76, (3, -3, 2): 77, (3, -2, 0): 78, (3, -2, 1): 79, (3, -1, -1): 80, (3, -1, 0): 81, (3, 0, -2): 82, (3, 0, -1): 83, (3, 1, -3): 84, (3, 1, -2): 85, (3, 2, -3): 86, (4, -3, 0): 87, (4, -3, 1): 88, (4, -2, -1): 89, (4, -2, 0): 90, (4, -1, -2): 91, (4, -1, -1): 92, (4, 0, -3): 93, (4, 0, -2): 94, (4, 1, -3): 95}
GRAPH = [[11, 2], [13, 4, 2], [0, 1], [15, 6, 4], [1, 3], [17, 8, 6], [3, 5], [19, 8], [5, 7], [22, 11], [24, 13, 11], [0, 9, 10], [26, 15, 13], [1, 10, 12], [28, 17, 15], [3, 12, 14], [30, 19, 17], [5, 14, 16], [32, 19], [7, 16, 18], [35, 22], [37, 24, 22], [9, 20, 21], [39, 26, 24], [10, 21, 23], [41, 28, 26], [12, 23, 25], [43, 30, 28], [14, 25, 27], [45, 32, 30], [16, 27, 29], [47, 32], [18, 29, 31], [49, 35], [51, 37, 35], [20, 33, 34], [53, 39, 37], [21, 34, 36], [55, 41, 39], [23, 36, 38], [57, 43, 41], [25, 38, 40], [59, 45, 43], [27, 40, 42], [61, 47, 45], [29, 42, 44], [62, 47], [31, 44, 46], [64, 51, 49], [33, 48], [66, 53, 51], [34, 48, 50], [68, 55, 53], [36, 50, 52], [70, 57, 55], [38, 52, 54], [72, 59, 57], [40, 54, 56], [74, 61, 59], [42, 56, 58], [75, 62, 61], [44, 58, 60], [46, 60], [77, 66, 64], [48, 63], [79, 68, 66], [50, 63, 65], [81, 70, 68], [52, 65, 67], [83, 72, 70], [54, 67, 69], [85, 74, 72], [56, 69, 71], [86, 75, 74], [58, 71, 73], [60, 73], [88, 79, 77], [63, 76], [90, 81, 79], [65, 76, 78], [92, 83, 81], [67, 78, 80], [94, 85, 83], [69, 80, 82], [95, 86, 85], [71, 82, 84], [73, 84], [90, 88], [76, 87], [92, 90], [78, 87, 89], [94, 92], [80, 89, 91], [95, 94], [82, 91, 93], [84, 93]]
MAGNITUDES = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 4, 2, 3, 2, 2, 2, 2, 3, 3, 4, 4, 4, 3, 4, 2, 3, 1, 2, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 3, 3, 2, 2, 1, 1, 2, 1, 3, 2, 4, 3, 4, 4, 4, 3, 3, 2, 2, 2, 2, 3, 2, 4, 3, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

CRADLES = [[1, 2, 0, 11], [5, 8, 7, 19], [47, 46, 62, 60], [84, 95, 93, 94], [76, 88, 87, 90], [35, 33, 49, 48]]
CRADLE_BRANCHES = [[10, 13], [17, 16], [44, 61], [85, 82], [79, 78], [34, 51]]

# -1 is free, -2 is self-locked, 0-2 are occupied by players
turn = 0
board = [-1] * N
scores = [0, 0, 0]

cur_cradle = -1
cradle_empty = []

comp = []
aggro = 1


# For local testing arena
def reset():
    global turn, board, scores, cur_cradle, cradle_empty, comp, aggro
    turn = 0
    board = [-1] * N
    scores = [0, 0, 0]

    cur_cradle = -1
    cradle_empty = []

    comp.clear()
    aggro = 1


# Data on the component of some vertex
def get_component(start, vertices=False, potential=False):
    degree = {start: 0}

    def dfs(u):
        for v in GRAPH[u]:
            if (board[v] == board[u] or (potential and board[v] == -1)) and v not in degree:
                degree[u] += 1
                degree[v] = 1
                dfs(v)
    dfs(start)

    diameter = len(degree) - list(degree.values()).count(3)
    return (list(degree.keys()), diameter) if vertices else diameter


# If we placed this chip, what would the diameter of its component be?
def test_diameter(vertex, player):
    assert board[vertex] == -1
    board[vertex] = player
    res = get_component(vertex)
    board[vertex] = -1
    return res


# Would placing this chip increase the diameter of some component?
def test_increase(vertex, player):
    assert board[vertex] == -1
    max_neighbor = -1
    for v in GRAPH[vertex]:
        if board[v] == player:
            max_neighbor = max(max_neighbor, get_component(v))
    return test_diameter(vertex, player) > max_neighbor


# Update states as described above
def update_board(board_copy, player):
    global turn, board
    turn = len(board_copy)
    for coord, val in board_copy.items():
        board[INDICES[coord]] = val
    for i in range(N):
        if board[i] == -1 and test_diameter(i, player) >= 5:
            board[i] = -2


# Find the scores of each player
def update_scores():
    global scores
    scores = [0, 0, 0]
    dist = [-1] * N
    for i in range(N):
        if dist[i] == -1 and board[i] >= 0:
            dist[i] = 0
            queue = [i]
            while len(queue) > 0:
                u = queue.pop(0)
                for v in GRAPH[u]:
                    if dist[v] == -1 and board[v] == board[u]:
                        dist[v] = dist[u] + 1
                        queue.append(v)
            length = get_component(i)
            if length == 4:
                scores[board[i]] += 3
            elif length == 3:
                scores[board[i]] += 1


# How many neighbors can we place chips in?
def free_degree(vertex):
    res = 0
    for v in GRAPH[vertex]:
        if board[v] == -1:
            res += 1
    return res


# Biased (strategic!) random pick from a pool of moves
def pick_move(pool, player):
    weights = []
    for u in pool:
        weight = 0

        # Spots further from the center cause less self-locking
        weight += math.exp(MAGNITUDES[u])

        # Inconvenience your opponent, especially if you're low on options or your opponent is strong
        colors = set()
        for v in GRAPH[u]:
            if board[v] >= 0 and board[v] != player:
                colors.add(board[v])
        for color in colors:
            if test_increase(u, color):
                length = test_diameter(u, color)
                if length == 4:
                    weight += aggro * scores[color] * 5
                elif length == 3:
                    weight += aggro * scores[color] * 1.5
        weights.append(weight)

    move = random.choices(pool, weights)[0]
    comp.append(move)
    return COORDS[move]


def strategy(board_copy, player):
    # Set everything up, keep the board up to date
    global comp, aggro
    update_board(board_copy, player)
    update_scores()

    # Cradle opener stuff
    global turn, cur_cradle, cradle_empty
    if cur_cradle != -1:
        if board[CRADLES[cur_cradle][3]] != -1:
            comp.append(CRADLES[cur_cradle][0])
        else:
            cradle_empty.append(CRADLES[cur_cradle][1])
            cradle_empty.append(CRADLES[cur_cradle][2])
            move = COORDS[CRADLES[cur_cradle][3]]
            cur_cradle = -1
            return move
    
    if turn < 35:
        free_cradles = [[], [], []]
        for i, cradle in enumerate(CRADLES):
            free = True
            for u in cradle:
                if board[u] != -1:
                    free = False
                    break
            if free:
                branches = 0
                for u in CRADLE_BRANCHES[i]:
                    if board[u] == -1:
                        branches += 1
                free_cradles[branches].append(i)
        for i in reversed(range(3)):
            if free_cradles[i]:
                cur_cradle = random.choice(free_cradles[i])
                return COORDS[CRADLES[cur_cradle][0]]

    comp = [x for x in comp if (get_component(x) < 4 and get_component(x, potential=True) >= 3)]

    while cradle_empty and board[cradle_empty[-1]] != -1:
        cradle_empty.pop()
        if len(cradle_empty) % 2:
            cradle_empty.pop()
    if cradle_empty:
        return COORDS[cradle_empty.pop()]

    # If we're working on a component, try to build on it
    build = [[], [], []]
    for u in comp:
        for v in GRAPH[u]:
            if board[v] == -1 and test_increase(v, player):
                if test_diameter(v, player) == 4:
                    build[0].append(v)
                elif get_component(v, potential=True) >= 4:
                    build[1].append(v)
                else:
                    build[2].append(v)

    for i in range(3):
        if build[i]:
            return pick_move(build[i], player)

    # 5 grades of starting locations
    # As good starting locations start running out, become more aggressive
    candidates = [[], [], [], [], []]

    for i in range(N):
        if board[i] != -1:
            continue
        length = test_diameter(i, -1)
        degree = free_degree(i)

        if length >= 4 and degree >= 2:
            candidates[0].append(i)
        elif length >= 4:
            candidates[1].append(i)
        elif length >= 3 and degree >= 2:
            candidates[2].append(i)
            aggro = max(aggro, 3)
        elif length >= 3:
            candidates[3].append(i)
            aggro = max(aggro, 3)
        else:
            candidates[4].append(i)
            aggro = max(aggro, 100)

    # Have some randomness, but higher grades always better
    for i in range(5):
        if len(candidates[i]) > 0:
            return pick_move(candidates[i], player)

    return None
