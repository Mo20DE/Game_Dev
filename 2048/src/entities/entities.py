from framework.utils import *
from framework.static import *

import random


# class to represent a board tile
class BoardTile:

    def __init__(self, size, pos, num, dim, image, spwn_eff=True):
        
        self.size = size
        self.num = num
        self.pos = pos
        self.dim = dim

        self.tile_img = image
        self.tile_rect = self.tile_img.get_rect(topleft=self.pos)

        self.spawn_effect = spwn_eff
        self.merge_effect = [False, False]
        self.size_cpy = [self.size[0]-30]*2
        self.spawn_off = 3
        self.tile_center = ((self.pos[0]+(tile_dim[self.dim]/2)), (self.pos[1]+(tile_dim[self.dim]/2)))
    
    def do_spawn_effect(self, screen):

        self.img_cpy = pg.transform.scale(self.tile_img, self.size_cpy)
        self.img_cpy_rect = self.img_cpy.get_rect()
        self.img_cpy_rect.center = self.tile_center

        screen.blit(self.img_cpy, self.img_cpy_rect)
        self.size_cpy[0] += self.spawn_off
        self.size_cpy[1] += self.spawn_off

        if (self.size[0]+5, self.size[1]+5) <= tuple(self.size_cpy):
            self.spawn_effect = False
    
    def do_merge_effect(self, screen):

        self.img_cpy = pg.transform.scale(self.tile_img, self.size_cpy)
        self.img_cpy_rect = self.img_cpy.get_rect()
        self.img_cpy_rect.center = self.tile_center

        screen.blit(self.img_cpy, self.img_cpy_rect)

        if tuple(self.size_cpy) >= (self.size[0]+15, self.size[1]+15):
            self.merge_effect[1] = True

        elif not self.merge_effect[1]:
            self.size_cpy[0] += self.spawn_off
            self.size_cpy[1] += self.spawn_off
        
        elif self.merge_effect[1]:
            self.size_cpy[0] -= self.spawn_off-1
            self.size_cpy[1] -= self.spawn_off-1
        
        elif self.size_cpy <= tuple(self.size):
            self.merge_effect[0] = False
        
        '''
        self.img_cpy = pg.transform.scale(self.tile_img, self.size_cpy)
        self.img_cpy_rect = self.img_cpy.get_rect()
        self.img_cpy_rect.center = self.tile_center

        screen.blit(self.img_cpy, self.img_cpy_rect)

        if tuple(self.size_cpy) >= (self.size[0]+15, self.size[1]+15):
            self.merge_effect[1] = True

        elif not self.merge_effect[1]:
            self.size_cpy[0] += self.spawn_off
            self.size_cpy[1] += self.spawn_off
        
        elif self.merge_effect[1]:
            self.size_cpy[0] -= self.spawn_off-1
            self.size_cpy[1] -= self.spawn_off-1
        
        elif self.size_cpy <= tuple(self.size):
            self.merge_effect[0] = False'''
    
    def set_pos(self, axis, pos):

        self.pos[0 if axis == "x" else 1] = pos
        if axis == "x": self.tile_rect.x = pos
        else: self.tile_rect.y = pos
    
    def shift_pos(self, axis, off):

        self.pos[0 if axis == "x" else 1] += off
        if axis == "x": self.tile_rect.x += off
        else: self.tile_rect.y += off

    def reset_spawn_effect(self):
        self.spawn_effect = True
    
    def reset_merge_effect(self):
        self.merge_effect[0] = True
    
    def draw_tile(self, screen):

        if self.spawn_effect: self.do_spawn_effect(screen)
        elif self.merge_effect[0]: self.do_merge_effect(screen)
        else: screen.blit(self.tile_img, self.tile_rect)


# class which represents a move
class Move:

    def __init__(self): self.init_move()
    
    def init_move(self):

        self.board = None
        self.board_tiles = None
        self.score = 0
        self.moves_done = 0
    

class Algorithms:

    def __init__(self) -> None:

        # every possible move
        self.moves = ["left", "right", "down", "up"]
        self.weight_mat = {
            3: self.construct_weight_matrix(3),
            4: self.construct_weight_matrix(4),
            5: self.construct_weight_matrix(5)
        }
    
    def construct_weight_matrix(self, dim):

        f = lambda i, row: row[::-1] if i%2==1 else row
        return np.array(
            [f(j, [2**((i+1)+(dim*j)) for i in range(dim)])
            for j in range(dim)])
    
    def shift_matrix(self, mat_, move_dir) -> tuple:
    
        reward, merges = 0, 0
        # move buffer information
        b_len = len(mat_)
        if b_len > 5:
            if b_len == 9: dim = 3
            elif b_len == 16: dim = 4
            else: dim = 5
            mat = mat_.reshape((dim, dim))
        else: mat = mat_.copy()

        # merge buffer
        merge_buffer = np.zeros(mat.shape)

        # transform matrix for processing
        if move_dir == "right":
            mat = mat[::, ::-1]
        elif move_dir == "up":
            mat = mat.T
        elif move_dir == "down":
            mat = mat.T[::, ::-1]
        
        # go through every entry of the board
        for i, row in enumerate(mat):
            for j, elem in enumerate(row):

                if j == 0: continue
                idx_off = 1
                for _ in range(j):

                    # non-zero element
                    if elem == 0: break
                    # zero and non-zero element
                    offset = j - idx_off
                    if (mat[i, offset] == 0 and 
                        merge_buffer[i, offset] != 1):
                        mat[i, offset] = elem
                        mat[i, offset+1] = 0
                        idx_off += 1

                    # two non-zero elements
                    elif (elem == mat[i, offset] and 
                        merge_buffer[i, offset] != 1):
                        merge_buffer[i, offset] = 1
                        mat[i, offset] = 2*elem
                        reward += 2*elem
                        merges += 1
                        mat[i, offset+1] = 0
                        idx_off += 1

        # retransform matrix
        if move_dir == "right":
            mat = mat[::, ::-1]
        elif move_dir == "up":
            mat = mat.T
        elif move_dir == "down":
            mat = mat.T[::-1, ::]
        
        return mat, reward, merges
    
    def isArrayZero(self, array) -> bool:
        # compare two arrays
        return np.allclose(array, np.zeros(array.shape))
    
    def cantMove(self, board) -> bool:

        equal_cnt = 0
        for  move in self.moves:
            if np.allclose(board, self.shift_matrix(board, move)[0]):
                equal_cnt += 1
        return True if equal_cnt > 2 else False
    
    #def canShiftDir(self, board, dir):
    #    return True if not np.allclose(board, self.shift_matrix(board, dir)[0]) else False
    def canShiftDir(self, board, mod_board) -> bool:
        return True if not np.allclose(board, mod_board) else False
    
    def get_free_fields(self, board) -> list:
        # get all empty fields on board
        dim = len(board)
        return [[i, j] for i in range(dim) for j in range(dim) if board[i, j] == 0]
    
    # check if the game is over
    def isLost(self, bd) -> bool:

        if len(self.get_free_fields(bd)) > 0: return False

        mat_T = bd.T
        range_x =  mat_T.shape[0]-1

        # check horizontally and vertically
        for i in range(range_x+1):
            for j in range(range_x):
                if bd[i, j] != 0 or mat_T[i, j] != 0:
                    if (bd[i, j] == bd[i, j+1] 
                        or mat_T[i, j] == mat_T[i, j+1]):
                        return False
        return True

    def tryInsertTile(self, board) -> bool:

        free_pos = self.get_free_fields(board)
        # check if there is a free position on the board
        if len(free_pos) > 0:
            new_pos = random.choice(free_pos)
            np.random.shuffle(urn)
            rand_tile = random.choice(urn)
            #print(f"Inserted tile: {rand_tile} at position: {new_pos}")
            board[new_pos[0], new_pos[1]] = rand_tile
            return True

        return False
    
    # def eval_board(self, board, n_empty): 

    #     grid = board
    #     utility = 0
    #     smoothness = 0

    #     big_t = np.sum(np.power(grid, 2))
    #     s_grid = np.sqrt(grid)
    #     smoothness -= np.sum(np.abs(s_grid[::,0] - s_grid[::,1]))
    #     smoothness -= np.sum(np.abs(s_grid[::,1] - s_grid[::,2]))
    #     smoothness -= np.sum(np.abs(s_grid[::,2] - s_grid[::,3]))
    #     smoothness -= np.sum(np.abs(s_grid[0,::] - s_grid[1,::]))
    #     smoothness -= np.sum(np.abs(s_grid[1,::] - s_grid[2,::]))
    #     smoothness -= np.sum(np.abs(s_grid[2,::] - s_grid[3,::]))
        
    #     empty_w = 100000
    #     smoothness_w = 3

    #     empty_u = n_empty * empty_w
    #     smooth_u = smoothness ** smoothness_w
    #     big_t_u = big_t

    #     utility += (big_t + empty_u + smooth_u)

    #     return (utility, empty_u, smooth_u, big_t_u)

    # def chance(self, board, depth = 0):

    #     empty_cells = self.get_free_fields(board)
    #     n_empty = len(empty_cells)

    #     #if n_empty >= 7 and depth >= 5:
    #     #    return self.eval_board(board, n_empty)

    #     if n_empty >= 6 and depth >= 2:
    #         return self.eval_board(board, n_empty)

    #     elif n_empty >= 0 and depth >= 4:
    #         return self.eval_board(board, n_empty)

    #     if n_empty == 0:
    #         _, utility = self.maximize(board, depth + 1)
    #         return utility

    #     possible_tiles = []

    #     chance_2 = (.9 * (1 / n_empty))
    #     chance_4 = (.1 * (1 / n_empty))
        
    #     for empty_cell in empty_cells:
    #         possible_tiles.append((empty_cell, 2, chance_2))
    #         possible_tiles.append((empty_cell, 4, chance_4))

    #     utility_sum = [0, 0, 0, 0]

    #     for t in possible_tiles:
    #         t_board = board.copy()
    #         t_board[t[0][0]][t[0][1]] = t[1]
    #         _, utility = self.maximize(t_board, depth + 1)

    #         for i in range(4):
    #             utility_sum[i] += utility[i] * t[2]
        
    #     return tuple(utility_sum)
    
    # def maximize(self, board, depth = 0):

    #     shifted_matrices = [self.shift_matrix(board, move)[0] for move in self.moves]
    #     max_utility = (float('-inf'), 0, 0, 0)
    #     best_direction = None

    #     for i, new_board in enumerate(shifted_matrices):

    #         if self.canShiftDir(board, new_board):
    #             utility = self.chance(new_board, depth + 1)

    #             if utility[0] >= max_utility[0]:
    #                 max_utility = utility
    #                 best_direction = self.moves[i]
        
    #     return best_direction, max_utility
    #     #return self.maximize(board)[0]
    
    def smartStrategy(self, board, depth) -> str:

        # look for the highest reward, highest merges, and highest number of free fields
        #boards_in_all_dir = [self.shift_matrix(board, move) for move in self.moves]

        return self.expectimax(board, depth)
    
    def expectimax(self, board, depth):

        best_move = None
        best_utility = float('-inf')
        for move in self.moves:
            new_board = self.shift_matrix(board, move)[0]
            if not self.canShiftDir(board, new_board):
                continue

            utility = self.chance_node(new_board, depth)
            if utility > best_utility:
                best_utility = utility
                best_move = move
        
        return best_move
    
    def chance_node(self, board, depth):

        if depth == 0:
            # evaluate leafs of game-tree
            return self.evaluate_state(board)

        total_score = 0
        free_tiles = self.get_free_fields(board)
        for free_tile in free_tiles:

            board[free_tile[0], free_tile[1]] = 2
            total_score += 0.1 * self.compute_move_score(board, depth-1)
            board[free_tile[0], free_tile[1]] = 0
            board[free_tile[0], free_tile[1]] = 4
            total_score += 0.9 * self.compute_move_score(board, depth-1)
            board[free_tile[0], free_tile[1]] = 0

        return total_score/len(free_tiles)    
    
    def compute_move_score(self, board, depth):

        best_score = -1
        for move in self.moves:
            b_copy = board.copy()
            new_board = self.shift_matrix(b_copy, move)[0]
            if self.canShiftDir(board, new_board):
                score = self.chance_node(new_board, depth-1)
                best_score = max(score, best_score)
        
        return best_score

    def eval_board(self, board):

        dim = len(board)
        result = 0
        for i in range(dim):
            for j in range(dim):
                result += board[i][j] * self.weight_mat[dim][i][j]

        return result
    
    def evaluate_state(self, state):
        """
        This function evaluates a board state based on several metrics:
        1. The max-tile should be in a corner.
        2. Tiles should be arranged in a monotonous manner.
        3. Many empty cells are preferred -> low risk of getting stuck.
        Optional:
        4. Prefer smooth boards -> tile with similar values arranged adjacently.
        """

        MONOTONICITY_WEIGHT = 0.5
        EMPTY_CELLS_WEIGHT = 10.0

        n = state.shape[0]
        empty_cells = 0
        monotonicity = 0.0
        smoothness = 0.0

        left_to_right = 0
        right_to_left = 0
        top_to_bottom = 0
        bottom_to_top = 0

        for i in range(n):
            for j in range(n):
                if state[i, j] == 0:
                    empty_cells += 1

                if j < n - 1:
                    smoothness -= abs(state[i, j] - state[i, j+1])
                    if state[i, j] > state[i, j+1]:
                        left_to_right += 1
                    elif state[i, j] < state[i, j+1]:
                        right_to_left += 1
                    else:
                        left_to_right += 1
                        right_to_left += 1

                if i < n - 1:
                    smoothness -= abs(state[i, j] - state[i+1, j])
                    if state[i, j] > state[i+1, j]:
                        top_to_bottom += 1
                    elif state[i, j] < state[i+1, j]:
                        bottom_to_top += 1
                    else:
                        top_to_bottom += 1
                        bottom_to_top += 1

        max_log_tile = np.log2(state.max())
        monotonicity = max(left_to_right + bottom_to_top, right_to_left + bottom_to_top, 
                        right_to_left + top_to_bottom, left_to_right + top_to_bottom)

        is_corner = state[0, 0] == state.max() or state[3, 0] == state.max() or \
                    state[0, 3] == state.max() or state[3, 3] == state.max()

        utility = (monotonicity * MONOTONICITY_WEIGHT +
                smoothness / max_log_tile +
                empty_cells * EMPTY_CELLS_WEIGHT)

        return utility
    
    def greedyStrategy(self, board, depth):

        first_boards = []
        rew_samples = []

        for move in self.moves:
            move_data = self.shift_matrix(board, move)
            # do first known move
            brd, reward = move_data[0], move_data[1]
            # save data
            first_boards.append(brd)
            rew_samples.append(reward)

        # build sum of samples
        for i in range(4):
            rew_samples[i] += self.getBestGreedyMove(
                first_boards[i], rew_samples[i], depth)
        
        final_move = self.moves[np.argmax(rew_samples)]
        if not self.canShiftDir(board, self.shift_matrix(board, final_move)[0]):
            return self.randomStrategy()

        return final_move

    def getBestGreedyMove(self, board, reward, depth):

        # recursion anchor
        if depth < 1 or not self.tryInsertTile(board): 
            return reward

         # expand tree
        sample_data = [
            self.shift_matrix(board, "left"),
            self.shift_matrix(board, "right"),
            self.shift_matrix(board, "down"),
            self.shift_matrix(board, "up")
        ]
        # get newly computed boards
        boards = [bds[0] for bds in sample_data]
        # get newly computed rewards
        rewards = [rwds[1] for rwds in sample_data]

        # take best board and reward
        board = boards[np.argmax(rewards)]
        reward += np.max(rewards)

        # make recursive call (continue to earch tree)
        return self.getBestGreedyMove(board, reward, depth-1)
        
    def randomStrategy(self):

        # generate a random move
        return np.random.choice(self.moves)


'''# make move in all directions according to depth
        shifted_matrices, can_shift_dir = [], []
        for move in self.moves:
            shifted_matrices.append(self.shift_matrix(board, move))
            can_shift_dir.append(self.canShiftDir(board, shifted_matrices[-1][0]))
        
        # no desired move possible
        if not any(can_shift_dir[0:3]): 

            return "up"
        rewards, merges, free_fields = [], [], []
        for i in range(3):
            rewards.append(shifted_matrices[i][1])
            merges.append(shifted_matrices[i][2])
            free_fields.append(len(self.get_free_fields(shifted_matrices[i][0])))
        
        print(rewards, merges, free_fields)
        left = (rewards[0]*merges[0])/free_fields[0]
        right = (rewards[1]*merges[1])/free_fields[1]
        down = (rewards[2]*merges[2])/free_fields[2]

        return self.moves[np.argmax([left, right, down])]


        for _ in range(depth-1):
            idx = 0
            for new_mat, can_shift_mat in zip(shifted_matrices, can_shift_mat):
                if can_shift_mat:
                    free_fields = self.get_free_fields(new_mat[0])
                    # save previous data
                    rewards[idx] += new_mat[idx][1]
                    merges[idx] += new_mat[idx][2]
                    free_fields[idx] += len(free_fields)
                    # check if there is a free position on the board
                    if len(free_pos) > 0:
                        new_pos = random.choice(free_pos)
                        np.random.shuffle(urn)
                        rand_tile = random.choice(urn)
                        #print(f"Inserted tile: {rand_tile} at position: {new_pos}")
                        board[new_pos[0], new_pos[1]] = rand_tile 


     monotonic_reward = [0, 0, 0]
        smoothness = [0, 0, 0]
        data_of_every_dir = data_of_every_dir[0:3]
        for k, b_data in enumerate(data_of_every_dir):
            # evaluate monotnic order of board
            b_len = len(board)
            for i, row in enumerate(b_data[0]):
                if (i+1) % 2 == 0: row = row[::-1]
                for j in range(b_len-1):
                    if np.sum(row) > 0:
                        if row[j] > 0 and row[j] > row[j+1]:
                            monotonic_reward[k] += 0.5
                        elif row[j] > 0 and row[j] < row[j+1]:
                            monotonic_reward[k] -= 1
                        if row[j] > 0 and row[j+1] > 0:
                            if row[j]-row[j+1] == 0:
                                smoothness[k] += log2(row[j])
        
        end_results = []
        for i, data in enumerate(data_of_every_dir):
            end_results.append(
                (len(self.get_free_fields(data[0]))+(0.9*2)+(0.1*4)) + 
                data[1] + data[2] + monotonic_reward[i] +
                smoothness[i]
            )
        
        if int(end_results[0]) == int(end_results[1]) == int(end_results[2]):
            if can_move_three_dir[1] or can_move_three_dir[2]:
                return np.random.choice(["down", "right"])
            else: return "left"
        
        print(end_results)
        return self.moves[np.argmax(end_results)]'''

'''
def cornerStrategy(self, board: np.ndarray) -> str:


        ### heuristics ###
        # free fields on the board
        # smoothness (measures the value difference of adjacent tiles - trying to minimize this count)
        # weight matrix

        # do move in all 4 directions
        data_of_every_dir = [self.simOneStep(board, move) for move in self.moves]
        can_move_dir = [self.canShiftDir(board, b_data[0]) for b_data in data_of_every_dir]

        # can only move upwards
        if not any(can_move_dir[0:3]): return "up"

        # delete board data of a direction we can't move
        cleaned_data_of_every_dir = {}
        for i, data in enumerate(data_of_every_dir):
            if can_move_dir[i]: 
                cleaned_data_of_every_dir[self.moves[i]] = data
        
        # if there is only one direction to move -> execute move
        if len(cleaned_data_of_every_dir) == 1: 
            return list(cleaned_data_of_every_dir.keys())[0]
        
        # get the free fields of every board
        free_fields = [len(self.get_free_fields(data[0])) 
            for data in cleaned_data_of_every_dir.values()]

        # make symmetric weight matrix
        if self.sym_mat is None:
            self.sym_mat = self.constructSymMatrix(board.shape)
        elif self.sym_mat.shape != board.shape:
            self.sym_mat = self.constructSymMatrix(board.shape)

        ## evaluate every board ## - choose the best (most promising) move (at least 2 moves)
        data_len = len(cleaned_data_of_every_dir)
        weights, smoothness_scores = [], np.zeros(data_len)

        for s, data in enumerate(cleaned_data_of_every_dir.values()):

            # evaluate weights of each move
            weight_sum = 0
            _board = data[0]
            b_len = len(board)
            for i in range(b_len):
                for j in range(b_len):

                    # compute weights (monotonicity)
                    weight_sum += _board[i, j] * self.sym_mat[i, j]

                    # compute smoothness
                    if _board[i, j] == 0: continue
                    temp_score = 0
                    for k in range(-1, 2):
                        p = i + k
                        if p < 0 or p >= b_len: continue
                        for l in range(-1, 2):
                            q = j + l
                            if q < 0 or q >= b_len: continue
                            if _board[p, q] > 0:
                                temp_score -= abs(_board[i, j] - _board[p, q])

                    smoothness_scores[s] -= temp_score
            weights.append(weight_sum)

        final_score = [[], []] 
        smoothWeight = 0.1
        mono2Weight  = 1.0
        emptyWeight  = 2.7
        maxWeight    = 1.0

        # compute final score
        data = list(cleaned_data_of_every_dir.values())
        for i, move in enumerate(cleaned_data_of_every_dir.keys()):
            #heur_score = weights[i] - smoothness_scores[i]
            #act_score = min(weights[i], 1)
            #act_score = max(act_score, heur_score)

            final_score[0].append(move)
            final_score[1].append(
                smoothness_scores[i] * smoothWeight +
                weights[i] * mono2Weight +
                math.log(free_fields[i]) * emptyWeight + 
                np.max(data[i][0]) * maxWeight
            )
        
        print(final_score)
        print(final_score[0][np.argmax(final_score[1])])
        return final_score[0][np.argmax(final_score[1])]
        '''