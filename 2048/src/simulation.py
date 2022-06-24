from tkinter.tix import MAX
from entities.entities import Algorithms
from framework.static import *


algos = Algorithms()

sim_outcome = {
    "best-sample-depth-combination: ": None,
}

import numpy as np
import random

def generate_random_board(dim):

    # shuffle urn
    np.random.shuffle(urn)
    # choose 2 random elements
    tile_1 = np.random.choice(urn)
    tile_2 = np.random.choice(urn)
    # make board
    board = np.zeros((dim, dim), dtype=int)
    # insert tiles
    free_fields = algos.get_free_fields(board)
    pos1 = random.choice(free_fields)
    board[pos1[0], pos1[1]] = tile_1

    free_fields = algos.get_free_fields(board)
    pos2 = random.choice(free_fields)
    board[pos2[0], pos2[1]] = tile_2

    return board

def get_highest_tile(board):
    return np.max(board.flatten())


board = np.array([[2, 3, 2], [4, 2, 1], [2, 3, 2]]) #generate_random_board(4)

'''print(f"Random Board: \n {board}")
print(get_highest_tile(board))
print(algos.isLost(board))'''


# 1. init empty board
# 2. play until lost, with specific sample number and tree depth

# test case for greedy approach
def test_greedy(brd_range, max_range) -> list:

    # final data
    final_data = []

    for i in range(brd_range):

        # initialize a new board with two tiles
        board = generate_random_board(4)
        temp = {"Start-Board": board}
        final_data.append(temp)

        # for every board try different values
        for samples in range(1, max_range-1):
            for depth in range(1, max_range-1):

                final_data[i][f"Sample-Number{samples}{depth}"] = samples
                final_data[i][f"Depth-Number{samples}{depth}"] = depth
                total_reward = 0; moves = 0
                # make a random start
                #board, total_reward = algos.shift_matrix(board, algos.randomStrategy())
                # play game until end
                while not algos.isLost(board) or not algos.tryInsertTile(board):

                    #print(f"Samples: {samples}, Depth: {depth} \n")
                    #print(board)
                    move = algos.greedyStrategy(board=board, samples=samples, depth=depth)
                    print(f"Move: {move}")
                    board, rw = algos.shift_matrix(board, move)
                    total_reward += rw; moves += 1

                # save data
                else:
                    # save end-board, total-reward(score), moves, best-tile
                    final_data[i][f"End-Board{samples}{depth}"] = board
                    final_data[i][f"End-Score{samples}{depth}"] = total_reward
                    final_data[i][f"Total-Moves{samples}{depth}"] = moves
                    final_data[i][f"Best-Tile{samples}{depth}"] = get_highest_tile(board)
    
    return final_data
        

simulated_data = test_greedy(1, 4)
print(simulated_data)

