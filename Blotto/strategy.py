import random as rand
from math import floor
from collections import deque

# class BaseSoldier():
#     def __init__(self):
#         self.count = 0
#         self.mode = rand.choice([-1, 1])
#         self.feinted = False
#         self.feinting = False
#         self.last_obs_window = None
#         self.cons_no_movement = 0
#         self.last_move = 0
#         self.counter_offset = False

# soldier = BaseSoldier()

count = 0
mode = rand.choice([-1, 1])
feinted = False
feinting = False
last_obs_window = None
cons_no_movement = 0
last_move = 0
counter_offset = False

def strategy(ally: list, enemy: list, offset: int) -> int:
    global count, mode, feinted, feinting, last_obs_window, cons_no_movement, last_move, counter_offset
    if counter_offset:
        if offset == 0:
            if enemy[3] >= 9:
                return 1
            if ally[3] > enemy[3] + 1:
                move_score = rand.randint(0, ally[3] + 3)
                if move_score == 0:
                    return 1
                else:
                    return 0
            if enemy[3] > ally[3] + 3:
                return 1
            return 0
        return 1

    if count == 0:  # First turn, move towards nearest castle
        count += 1
        mode = None
        last_move = offset
        return offset

    count += 1

    if last_obs_window == None:
        last_obs_window = deque(enemy)
    else:
        for i in range(1, 5):
            if (last_obs_window[i - last_move] == enemy[i]):
                cons_no_movement += 1
                if cons_no_movement >= 6:
                    counter_offset = True
            else:
                cons_no_movement = -5

    if count >= 97:
        last_move = offset
        return offset
    if feinting:
        feinting = False
        feinted = True
        mode = None
        last_move = offset
        return offset

    # Check if agent is at a castle
    if offset == 0:
        if mode != None:
            feinted = False
        ally_count = ally[3]  # Number of ally soldiers at castle
        enemy_count = enemy[3]  # Number of enemy soldiers at castle
        mode = None  # Set mode to None when at castle
        # Check if agents are being outnumbered
        if ally_count > enemy_count + enemy[2] + enemy[4] + 1:
            move_score = rand.randint(0, ally[3] + 1)
            if move_score == 0:
                mode = rand.choice([-1, 1])  # Assign random mode to disperse
                last_move = mode
                return mode
        if enemy_count - ally_count >= 2 and not feinted:
            feinting = True
            mode = rand.choice([-1, 1])  # Assign random mode to disperse
            last_move = mode
            return mode
        if enemy_count + floor((enemy[2] + enemy[4]) * 0.9) - ally_count - floor((ally[2] + ally[4]) * 0.5) > 2:
            mode = rand.choice([-1, 1])  # Assign random mode to disperse
            last_move = mode
            return mode
        if enemy_count - ally_count >= 2 or enemy_count - ally_count > 0 and enemy_count >= 10:
            mode = rand.choice([-1, 1])
            last_move = mode
            return mode
        else:
            last_move = 0
            return 0
    else:
        castle_1_index = 3 + (offset) % 3
        castle_2_index = 3 - (-offset) % 3
        if ally[3] + ally[castle_1_index] > enemy[castle_1_index] and ally[castle_1_index] <= enemy[castle_1_index]:
            last_move = 1
            return 1
        if ally[3] + ally[castle_2_index] > enemy[castle_2_index] and ally[castle_2_index] <= enemy[castle_2_index]:
            last_move = -1
            return -1
        else:
            if mode is not None:  # If not at castle, move according to mode
                last_move = mode
                return mode
            else:
                mode = rand.choice([-1, 1])  # Assign random mode to disperse
                last_move = mode
                return mode
    
    return 1



# def strategyLocal(ally: list, enemy: list, offset: int, soldier) -> int:
#     if soldier.counter_offset:
#         if offset == 0:
#             if enemy[3] >= 9:
#                 return 1
#             if ally[3] > enemy[3] + 1:
#                 move_score = rand.randint(0, ally[3] + 3)
#                 if move_score == 0:
#                     return 1
#                 else:
#                     return 0
#             if enemy[3] > ally[3] + 3:
#                 return 1
#             return 0
#         return 1

#     if soldier.count == 0:  # First turn, move towards nearest castle
#         soldier.count += 1
#         soldier.mode = None
#         soldier.last_move = offset
#         return offset

#     soldier.count += 1

#     if soldier.last_obs_window == None:
#         soldier.last_obs_window = deque(enemy)
#     else:
#         for i in range(1, 5):
#             if (soldier.last_obs_window[i - soldier.last_move] == enemy[i]):
#                 soldier.cons_no_movement += 1
#                 if soldier.cons_no_movement >= 6:
#                     soldier.counter_offset = True
#             else:
#                 soldier.cons_no_movement = -5

#     if soldier.count >= 97:
#         soldier.last_move = offset
#         return offset
#     if soldier.feinting:
#         soldier.feinting = False
#         soldier.feinted = True
#         soldier.mode = None
#         soldier.last_move = offset
#         return offset

#     # Check if agent is at a castle
#     if offset == 0:
#         if soldier.mode != None:
#             soldier.feinted = False
#         ally_count = ally[3]  # Number of ally soldiers at castle
#         enemy_count = enemy[3]  # Number of enemy soldiers at castle
#         soldier.mode = None  # Set soldier.mode to None when at castle
#         # Check if agents are being outnumbered
#         if ally_count > enemy_count + enemy[2] + enemy[4] + 1:
#             move_score = rand.randint(0, ally_count + 1)
#             if move_score == 0:
#                 soldier.mode = rand.choice([-1, 1])  # Assign random soldier.mode to disperse
#                 soldier.last_move = soldier.mode
#                 return soldier.mode
#         if enemy_count - ally_count > 0 and not soldier.feinted:
#             soldier.feinting = True
#             soldier.mode = rand.choice([-1, 1])  # Assign random soldier.mode to disperse
#             soldier.last_move = soldier.mode
#             return soldier.mode
#         if enemy_count + floor((enemy[2] + enemy[4]) * 0.9) - ally_count - floor((ally[2] + ally[4]) * 0.5) > 2:
#             soldier.mode = rand.choice([-1, 1])  # Assign random soldier.mode to disperse
#             soldier.last_move = soldier.mode
#             return soldier.mode
#         if soldier.feinted and enemy_count - ally_count > 0:
#             soldier.mode = rand.choice([-1, 1])
#             soldier.last_move = soldier.mode
#             return soldier.mode
#         else:
#             soldier.last_move = 0
#             return 0
#     else:
#         castle_1_index = 3 + (offset) % 3
#         castle_2_index = 3 - (-offset) % 3
#         if ally[3] + ally[castle_1_index] > enemy[castle_1_index] and ally[castle_1_index] <= enemy[castle_1_index]:
#             soldier.last_move = 1
#             return 1
#         if ally[3] + ally[castle_2_index] > enemy[castle_2_index] and ally[castle_2_index] <= enemy[castle_2_index]:
#             soldier.last_move = -1
#             return -1
#         else:
#             if soldier.mode is not None:  # If not at castle, move according to soldier.mode
#                 soldier.last_move = soldier.mode
#                 return soldier.mode
#             else:
#                 soldier.mode = rand.choice([-1, 1])  # Assign random soldier.mode to disperse
#                 soldier.last_move = soldier.mode
#                 return soldier.mode
    
#     return 1


def offset(ally: list, enemy: list, offset: int):
    return offset

def neg1(ally: list, enemy: list, offset: int):
    return -1
    

def get_strategies():

    # soldier = BaseSoldier()
    """
    Returns a list of strategies to play against each other.

    In the local tester, all of the strategies will be used as separate players, and the 
    pairwise winrate will be calculated for each strategy.

    In the official grader, only the first element of the list will be used as your strategy.
    """
    strategies = [strategy, strategy]

    return strategies
