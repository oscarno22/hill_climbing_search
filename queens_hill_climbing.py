"""
Oscar Nolen
ITCS 6150 Project 2

This project implements hill-climbing search for the N-queens problem
"""

import copy
import random


def objective(grid):
    heuristic = 0
    n = len(grid)

    for row in grid:
        if len(row) > 1:
            heuristic += len(row) * (len(row) - 1) // 2  # check pairwise row conflicts

    for i in range(n):
        for j in range(i + 1, n):
            for col_i in grid[i]:
                for col_j in grid[j]:
                    if col_i == col_j:  # check row conflicts
                        heuristic += 1
                    if abs(col_i - col_j) == abs(i - j):  # check diagonal conflicts
                        heuristic += 1

    return heuristic


def get_moves(grid):
    n = len(grid)
    possible_moves = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # up-left, up-right, down-left, down-right

    for from_row in range(n):
        for from_col in grid[from_row]:
            for dr, dc in directions:  # for each queen, check each move direction
                steps = 1  # allows multiple moves in a single direction
                while True:
                    to_row = from_row + dr * steps
                    to_col = from_col + dc * steps

                    if 0 <= to_row < n and 0 <= to_col < n:  # respect bounds of board
                        if to_col not in grid[to_row]:  # respect other queens
                            possible_moves.append((from_row, from_col, to_row, to_col))
                        else:
                            break  # ran into a queen, so stop checking moves in given direction
                    else:
                        break  # ran out of bounds, so stop checking moves in given direction

                    steps += 1  # continue moving in given direction

    return possible_moves


def get_move_states(grid, moves):
    resultant_states = []

    for move in moves:
        from_row, from_col, to_row, to_col = move
        new_grid = copy.deepcopy(grid)

        new_grid[from_row].remove(from_col)  # move queen from original position
        new_grid[to_row].append(to_col)  # move queen to new position
        new_grid[to_row].sort()

        resultant_states.append(new_grid)

    return resultant_states


def get_min_neighbor(moves):
    min_indices = []

    objective_vals = [objective(move) for move in moves]
    min_val = min(objective_vals)

    for idx in range(len(objective_vals)):  # append indices of states with best heuristic
        if objective_vals[idx] == min_val:
            min_indices.append(idx)
    random_idx = random.choice(min_indices)  # randomly choose one of the best states

    return moves[random_idx]


def to_array(grid):
    n = len(grid)
    array_state = []

    for _ in range(n):  # initialize empty NxN array
        row = [0 for _ in range(n)]
        array_state.append(row)
    for i in range(n):  # add queens to their positions
        for j in grid[i]:
            array_state[i][j] = 1

    return array_state


def generate_start_state(n):
    grid = [[] for _ in range(n)]
    all_positions = [(row, col) for row in range(n) for col in range(n)]
    chosen_positions = random.sample(all_positions, n)  # randomly choose i, j indices without replacement

    for row, col in chosen_positions:
        grid[row].append(col)

    return grid


def hill_climbing(grid):
    current = grid
    step_count = 0
    path = []  # track search path

    while True:
        path.append(current)
        move_states = get_move_states(current, get_moves(current))
        min_neighbor = get_min_neighbor(move_states)
        if objective(current) <= objective(min_neighbor):  # if updating doesn't improve heuristic
            return current, step_count, path

        current = min_neighbor  # if updating improves heuristic
        step_count += 1


def hill_climbing_with_sideways(grid):
    current = grid
    step_count = 0
    max_sideways_moves = 50  # limit number of consecutive sideways moves
    sideways_moves = 0
    path = []  # track search path

    while True:
        path.append(current)
        move_states = get_move_states(current, get_moves(current))
        min_neighbor = get_min_neighbor(move_states)

        current_objective = objective(current)
        min_neighbor_objective = objective(min_neighbor)

        if current_objective < min_neighbor_objective:  # if updating worsens heuristic
            return current, step_count, path
        elif current_objective == min_neighbor_objective:  # if updating equals current heuristic
            if sideways_moves < max_sideways_moves:  # if we can still make sideways moves
                current = min_neighbor
                sideways_moves += 1
            else:  # if we've exhausted sideways moves
                return current, step_count, path
        else:  # if updating improves heuristic
            current = min_neighbor
            sideways_moves = 0

        step_count += 1


def random_restart_hill_climbing(n, search):
    total_steps = 0  # track steps over all iterations
    restarts = 0  # track number of restarts

    while True:
        current = generate_start_state(n)
        final_state, steps, path = search(current)
        total_steps += steps

        if objective(final_state) == 0:  # found goal state
            return final_state, total_steps, restarts

        restarts += 1  # if found non-goal state, restart


def main():
    n = input("Enter integer > 0: ")
    print("\n")

    for i in range(4):
        print("HILL CLIMBING SEARCH " + str(i))
        grid = generate_start_state(int(n))
        final, steps, path = hill_climbing(grid)
        for state in path:
            for row in to_array(state):
                print(row)
            print("\n")

    """
    for i in range(4):
        print("HILL CLIMBING WITH  SIDEWAYS MOVE SEARCH " + str(i))
        grid = generate_start_state(int(n))
        final, steps, path = hill_climbing_with_sideways(grid)
        for state in path:
            for row in to_array(state):
                print(row)
            print("\n")
    """

    """
    successes = 0
    success_steps = []
    failures = 0
    failure_steps = []

    print("RUNNING STANDARD HILL CLIMBING WITH N=" + n + ", 100 TIMES")
    for _ in range(100):
        grid = generate_start_state(int(n))
        final_state, step_count, path = hill_climbing(grid)

        if objective(final_state) == 0:
            successes += 1
            success_steps.append(step_count)
        else:
            failures += 1
            failure_steps.append(step_count)

    print("SUCCESS RATE: " + str(successes / 100))
    print("FAILURE RATE: " + str(failures / 100))
    if successes > 0:
        print("AVG SUCCESS STEPS: " + str(sum(success_steps) / len(success_steps)))
    else:
        print("AVG SUCCESS STEPS NOT CALCULABLE, SINCE NO SUCCESSES")
    if failures > 0:
        print("AVG FAILURE STEPS: " + str(sum(failure_steps) / len(failure_steps)))
    else:
        print("AVG FAILURE STEPS NOT CALCULABLE, SINCE NO FAILURES")
    print("\n")

    side_successes = 0
    side_success_steps = []
    side_failures = 0
    side_failure_steps = []

    print("RUNNING HILL CLIMBING WITH SIDEWAYS MOVE WITH N=" + n + ", 100 TIMES")
    for _ in range(100):
        grid = generate_start_state(int(n))
        final_state, step_count, path = hill_climbing_with_sideways(grid)

        if objective(final_state) == 0:
            side_successes += 1
            side_success_steps.append(step_count)
        else:
            side_failures += 1
            side_failure_steps.append(step_count)

    print("SUCCESS RATE: " + str(side_successes / 100))
    print("FAILURE RATE: " + str(side_failures / 100))
    if side_successes > 0:
        print("AVG SUCCESS STEPS: " + str(sum(side_success_steps) / len(side_success_steps)))
    else:
        print("AVG SUCCESS STEPS NOT CALCULABLE, SINCE NO SUCCESSES")
    if side_failures > 0:
        print("AVG FAILURE STEPS: " + str(sum(side_failure_steps) / len(side_failure_steps)))
    else:
        print("AVG FAILURE STEPS NOT CALCULABLE, SINCE NO FAILURES")
    print("\n")

    steps = []
    num_restarts = []
    print("RUNNING RANDOM RESTART HILL CLIMBING WITH N=" + n + ", 100 TIMES")
    for _ in range(100):
        best_state, total_steps, restarts = random_restart_hill_climbing(int(n), hill_climbing)
        steps.append(total_steps)
        num_restarts.append(restarts)

    avg_steps = sum(steps) / len(steps)
    avg_restarts = sum(num_restarts) / len(num_restarts)

    print("AVG STEPS: " + str(avg_steps))
    print("AVG RESTARTS: " + str(avg_restarts))

    side_steps = []
    side_num_restarts = []
    print("RUNNING RANDOM RESTART HILL CLIMBING W/ SIDEWAYS MOVE WITH N=" + n + ", 100 TIMES")
    for _ in range(100):
        best_state, total_steps, restarts = random_restart_hill_climbing(int(n), hill_climbing_with_sideways)
        side_steps.append(total_steps)
        side_num_restarts.append(restarts)

    avg_side_steps = sum(side_steps) / len(side_steps)
    avg_side_restarts = sum(side_num_restarts) / len(side_num_restarts)

    print("AVG STEPS: " + str(avg_side_steps))
    print("AVG RESTARTS: " + str(avg_side_restarts))
    """


if __name__ == '__main__':
    main()
