from scipy.fftpack import shift
from menues.gamemenu import GameMenu
from framework.utils import Keys
from entities.entities import ButtonsRow
from framework.static import *
import numpy as np
import random


class AlgoMenu:

    def __init__(self, gameM: GameMenu):

        # game menu instance
        self.gameM = gameM
        self.menu_status = "unfolded" # unfolded/collapsed
        self.auto_run = False
        self.step_run = False

        self.current_time = 0
        self.stop_time = 0
        self.auto_run_time = 0
        self.moves = [
            "up", "down", 
            "left", "right"
        ]

        # object to handle key input
        self.keys = Keys()
        # toggle button row to choose ai strategy
        self.toggle_btn_row = ButtonsRow(
            (37, 680), 15, 4, 
            toggle_algo_menu_btns_path[0],
            toggle_algo_menu_btns_path[1],
            active_btn=3, axis=1
        )

        self.samples=2
        self.depth=5
        self.speed=100
        
        # load every needed variable
        self.load_menu_variables()
    
    def load_menu_variables(self):

        # get current game theme
        theme = self.gameM.game_ent.sett_vars["theme"]

        self.menu_surf = game_assets[theme]["algo_menu"]["surfaces"]["menu_bg"]
        self.buttons = {
            "ai_menu_btn": game_assets[theme]["algo_menu"]["buttons"]["ai_menu_btn"],
            "auto_run_btn": game_assets[theme]["algo_menu"]["buttons"]["auto_run_btn"],
            "stop_btn": game_assets[theme]["algo_menu"]["buttons"]["stop_btn"],
            "step_btn": game_assets[theme]["algo_menu"]["buttons"]["step_btn"]
        }
    
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
        
        # expand tree
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
    
    def on_nn_btn_click(self):
        pass

    def on_exp_btn_click(self):
        pass

    def on_greedy_btn_click(self, board, samples, depth):

        '''return self.moves[
            np.argmax([
                self.getBestGreedyMove(board, "up", depth),
                self.getBestGreedyMove(board, "down", depth),
                self.getBestGreedyMove(board, "left", depth),
                self.getBestGreedyMove(board, "right", depth)
            ])
        ]'''

        first_boards = []
        rew_samples = np.zeros(4)

        for i, move in enumerate(self.moves):
            # do first known move
            brd, reward = self.shift_matrix(board, move)
            # save data
            first_boards.append(brd)
            rew_samples[i] = reward

        for _ in range(samples):
            rew_samples[0] += self.getBestGreedyMove(first_boards[0], rew_samples[0], depth)
            rew_samples[1] += self.getBestGreedyMove(first_boards[1], rew_samples[1], depth)
            rew_samples[2] += self.getBestGreedyMove(first_boards[2], rew_samples[2], depth)
            rew_samples[3] += self.getBestGreedyMove(first_boards[3], rew_samples[3], depth)
        
        return self.moves[np.argmax(rew_samples)]

    def on_random_btn_click(self):
        # generate a random move
        return np.random.choice(self.moves)
    
    def handleMenuButtonsActions(self, mPos):

        # get local scope time
        self.current_time = pg.time.get_ticks()

        # handle button actions
        if self.buttons["step_btn"].isBtnClicked(mPos) and not self.auto_run:
            self.step_run = True

        elif (self.buttons["auto_run_btn"].isBtnClicked(mPos) and not self.auto_run and
            self.gameM.game_ent.boards[self.gameM.game_ent.mode].game_state != "lost"):

            self.stop_time = pg.time.get_ticks()
            self.gameM.game_ent.boards[self.gameM.game_ent.mode].anim_move = False
            self.gameM.canMenuBtnsClick = False
            self.auto_run = True
        
        elif ((self.buttons["stop_btn"].isBtnClicked(mPos) and self.current_time - self.stop_time > 400) or
            (self.gameM.game_ent.boards[self.gameM.game_ent.mode].game_state == "lost" and self.auto_run)):

            self.gameM.game_ent.boards[self.gameM.game_ent.mode].anim_move = True
            self.gameM.canMenuBtnsClick = True
            self.auto_run = False
        
        ## run algorithms ##

        # run one step
        if self.step_run:

            # neural network algorithm
            if self.toggle_btn_row.getActiveButton() == 0:
                self.step_run = False
                pass

            # expectimax algorithm
            elif self.toggle_btn_row.getActiveButton() == 1:
                self.step_run = False
                pass

            # greedy algorithm
            elif self.toggle_btn_row.getActiveButton() == 2:
                board = self.gameM.game_ent.boards[self.gameM.game_ent.mode].board
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click(board, samples=self.samples, depth=self.depth)
                self.step_run = False

            # random algorithm
            elif self.toggle_btn_row.getActiveButton() == 3:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_random_btn_click()
                self.step_run = False
        
        # run auto until stop
        elif self.auto_run and self.current_time - self.auto_run_time > self.speed:

            # neural network algorithm
            if self.toggle_btn_row.getActiveButton() == 0:
                pass

            # expectimax algorithm
            elif self.toggle_btn_row.getActiveButton() == 1:
                pass

            # greedy algorithm
            elif self.toggle_btn_row.getActiveButton() == 2:
                self.auto_run_time = pg.time.get_ticks()
                board = self.gameM.game_ent.boards[self.gameM.game_ent.mode].board
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click(board, samples=self.samples, depth=self.depth)

            # random algorithm
            elif self.toggle_btn_row.getActiveButton() == 3:
                self.auto_run_time = pg.time.get_ticks()
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_random_btn_click()
        
    def draw(self, screen):

        if not self.gameM.states["restart_menu"]:

            if self.menu_status == "unfolded":
                # draw ai menu button
                self.buttons["ai_menu_btn"].blitButton(screen)

            elif self.menu_status == "collapsed":
                # draw menu
                screen.blit(self.menu_surf, algo_menu_bg_pos)
                # draw quit button
                quit_btn.blitButton(screen)
                # draw toggle button row
                self.toggle_btn_row.blitButtonRow(screen)

                # draw buttons
                self.buttons["step_btn"].blitButton(screen)
                if not self.auto_run: self.buttons["auto_run_btn"].blitButton(screen)
                else: self.buttons["stop_btn"].blitButton(screen)

    def update(self, mPos):

        if not self.gameM.states["restart_menu"]:
            
            if self.menu_status == "unfolded":
                if self.buttons["ai_menu_btn"].isBtnClicked(mPos):

                    self.gameM.game_ent.boards[self.gameM.game_ent.mode].key_lock = True
                    # ai menu button pressed
                    self.menu_status = "collapsed"
                    #self.gameM.canMenuBtnsClick = False

            else:
                # quit button pressed
                if (quit_btn.isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE) 
                    or not self.gameM.game_ent.game_states["playing"]):

                    self.gameM.game_ent.boards[self.gameM.game_ent.mode].key_lock = False
                    self.gameM.canMenuBtnsClick = True
                    self.auto_run = False
                    self.menu_status = "unfolded"

                elif self.toggle_btn_row.updateButtonRow(mPos):
                    # update toggle button row
                    self.auto_run = False
                else:
                    # handle menu auto-run, step, stop button actions
                    self.handleMenuButtonsActions(mPos)
        
