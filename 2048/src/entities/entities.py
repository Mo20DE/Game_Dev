from framework.utils import *
from framework.static import *


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
    
    def reset_spawn_effect(self):
        self.spawn_effect = True
    
    def draw_tile(self, screen):

        if self.spawn_effect: self.do_spawn_effect(screen)
        else: screen.blit(self.tile_img, self.tile_rect)


# class which represents a move
class Move:

    def __init__(self, prevBoard, boardTiles, score, movesDone):
        
        self.board = prevBoard
        self.board_tiles = boardTiles
        self.score = score
        self.moves_done = movesDone


# surface class
class Surface:
    
    def __init__(self, size, pos, color):

        self.surf = pg.Surface(size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft=pos)

    def blit(self, screen, surf2=None):

        if isinstance(surf2, pg.Surface):
            self.surf.blit(surf2, self.rect)
        else: screen.blit(self.surf, self.rect)


class ButtonsRow:

    def __init__(self, pos:tuple, btn_rad:int, amount:int, non_click_img_path, 
                on_click_img_path, active_btn:int=0, btn_gap:int=10, axis:int=0):

        self.pos = pos
        self.btn_rad = btn_rad
        self.amount = amount
        self.non_click_img = non_click_img_path
        self.on_click_img = on_click_img_path

        self.active_btn = active_btn # default active button
        self.btn_gap = btn_gap
        self.axis = axis

        # check whether the parameters
        # are all of correct type
        self.check_parameters()

        # contains every button
        self.buttons = []
        self.init_buttons()
        self.mode_changed = False
    
    def check_parameters(self):

        # button size
        if self.btn_rad < 10 or self.btn_rad > 100:
            raise ValueError("Invalid button-radius. Button-radius has to be between: 10 and 100 pixel.")
        
        # amount
        if self.amount < 1 or self.amount > 10:
            raise ValueError("Invalid button-amount provided. Button-amount should be between 1 and 10.")
        
        # button gap
        if self.btn_gap < 0 or self.btn_gap > 100:
            raise ValueError("Invalid button-gap provided. Button-gap has to be between: 0 and 100.")
        
        # button mode
        if self.active_btn < 0 or self.active_btn > self.amount-1:
            raise ValueError(f"Invalid Button-mode. Button-mode has to be between: 0 and {self.amount-1}.")
        
        # axis
        if self.axis != 0 and self.axis != 1:
            raise Exception("Invalid axis provided. Axis has to be 0 or 1.")
    
    def setActiveButton(self, idx):

        if idx < 0 and idx > self.amount-1:
            raise ValueError("Invalid Button Index provided.")
        
        self.active_btn = idx
    
    def setButtonStatus(self, idx, status):

        if idx < 0 and idx > self.amount-1:
            raise ValueError("Invalid Button Index provided.")

        if status != "on" and status != "off":
            raise ValueError("Invalid status type. provided")
        
        self.buttons[idx].status = status
    
    def isModeChanged(self):
        return True if self.mode_changed else False
    
    def getActiveButton(self):
        return self.active_btn
    
    def init_buttons(self):

        # make button images
        if isinstance(self.non_click_img, list) and isinstance(self.on_click_img, list):

            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.non_click_img, False, True)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.on_click_img, False, True)
        else:
            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.non_click_img, False, True)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.on_click_img, False, True)

        btn_pos = list(self.pos)
        # init buttons
        for _ in range(self.amount):
            self.buttons.append(
                ToggleButton(
                    btn_pos,
                    self.non_click_img,
                    self.on_click_img
                )
            )

            # compute gap-offset
            btn_pos[self.axis] += self.btn_rad+self.btn_gap
        
        # set active button
        self.buttons[self.active_btn].status = "on"
    
    def blitButtonRow(self, screen):

        for btn in self.buttons:
            btn.blitButton(screen)
    
    def updateButtonRow(self, mPos):

        # reset variable
        if self.mode_changed: self.mode_changed = False
        # check buttons
        for i, btn in enumerate(self.buttons):
            # update buttons
            if self.active_btn != i:
                if btn.isToggleBtnClicked(mPos):
                    self.buttons[self.active_btn].status = "off"
                    self.buttons[i].status = "on"
                    self.active_btn = i
                    self.mode_changed = True
        
        return self.mode_changed


import random
class Algorithms:

    def __init__(self):

        # every possible move
        self.moves = [
            "up", "down", 
            "left", "right"
        ]

        # greedy algorithm attributes
        self.samples=5
        self.depth=5
        self.speed=60
        self.failures = 0
    
    def randomStrategy(self):
        # generate a random move
        return np.random.choice(self.moves)
    
    def isArrayZero(self, array):
        # compare two arrays
        return np.allclose(array, np.zeros(array.shape))
    
    def cantMove(self, board):

        equal_cnt = 0
        for  move in self.moves:
            if np.allclose(board, self.shift_matrix(board, move)[0]):
                equal_cnt += 1
        return True if equal_cnt > 2 else False
    
    def shift_matrix(self, mat_, move_dir):
    
        reward = 0
        # merge buffer
        merge_buffer = np.zeros(mat_.shape)
        # move buffer information
        mat = mat_.copy()

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
                        mat[i, offset+1] = 0
                        idx_off += 1

        # retransform matrix
        if move_dir == "right":
            mat = mat[::, ::-1]
        elif move_dir == "up":
            mat = mat.T
        elif move_dir == "down":
            mat = mat.T[::-1, ::]
        
        return mat, reward
    
    def get_free_fields(self, bd) -> tuple:
        # get all empty fields on board
        dim = bd.shape[0]
        return [[i, j] for i in range(dim) for j in range(dim) if bd[i, j] == 0]
    
    # check if the game is over
    def isLost(self, bd):

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
        if len(free_pos) != 0:
            new_pos = random.choice(free_pos)
            np.random.shuffle(urn)
            rand_tile = random.choice(urn)
            #print(f"Inserted tile: {rand_tile} at position: {new_pos}")
            board[new_pos[0], new_pos[1]] = rand_tile
            return True

        return False
    
    def getBestGreedyMove(self, board, reward, depth) -> int:

        # recursion anchor
        if depth == 0 or not self.tryInsertTile(board): 
            return reward
        
        # expand tree (make moves)
        sample_data = [
            self.shift_matrix(board, "up"),
            self.shift_matrix(board, "down"),
            self.shift_matrix(board, "left"),
            self.shift_matrix(board, "right"),
        ]

        # get newly computed boards
        boards = [bds[0] for bds in sample_data]
        # get newly computed rewards
        rewards = [rwds[1] for rwds in sample_data]

        # take best board, move and reward
        board = boards[np.argmax(rewards)]
        reward += np.max(rewards)

        # make recursive call (continue to earch tree)
        return self.getBestGreedyMove(board, reward, depth-1)
    
    def greedyStrategy(self, board, samples, depth) -> str:

        first_boards = []
        rew_samples = np.zeros(4)

        for i, move in enumerate(self.moves):
            # do first known move
            brd, reward = self.shift_matrix(board, move)
            # save data
            first_boards.append(brd)
            rew_samples[i] = reward

        for _ in range(samples):
            # build sum of samples
            rew_samples[0] += self.getBestGreedyMove(first_boards[0], rew_samples[0], depth) # up-move
            rew_samples[1] += self.getBestGreedyMove(first_boards[1], rew_samples[1], depth) # down-move
            rew_samples[2] += self.getBestGreedyMove(first_boards[2], rew_samples[2], depth) # left-move
            rew_samples[3] += self.getBestGreedyMove(first_boards[3], rew_samples[3], depth) # right-move
        
        # if all moves are the same or matrix isn't changing - return a random move
        if self.isArrayZero(rew_samples) or self.cantMove(board): 
            return self.randomStrategy()
        print(f"Rewards: {rew_samples}")
        
        return self.moves[np.argmax(rew_samples/samples)]
    
