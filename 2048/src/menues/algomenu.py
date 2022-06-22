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
    
    def get_free_fields(self, bd):

        # get all empty fields on board
        empty_fields = []
        for i in range(len(bd)):
            for j in range(len(bd)):
                if bd[i, j] == 0:
                    empty_fields.append([i, j])

        return empty_fields
    
    def shift_matrix(self, matrix, move_dir):

        bd = matrix.copy()
        reward = 0

        # transform matrix for processing
        if move_dir == "right":
            bd = bd[::, ::-1]

        elif move_dir == "up":
            bd = bd.T

        elif move_dir == "down":
            bd = bd.T[::, ::-1]
        
        # go through every entry of the board
        for i, row in enumerate(bd):
            
            for j, elem in enumerate(row):

                if j == 0: continue

                idx_off = 1
                for _ in range(j):

                    # non-zero element
                    if elem == 0: break

                    # zero and non-zero element
                    offset = j - idx_off
                    if bd[i, offset] == 0:
                        bd[i, offset] = elem
                        bd[i, offset+1] = 0
                        idx_off += 1
                        
                    # two non-zero elements
                    elif elem == bd[i, offset]:
                        bd[i, offset] = 2*elem
                        reward += 2*elem
                        bd[i, offset+1] = 0
                        idx_off += 1
        
        # retransform matrix
        if move_dir == "right":
            bd = bd[::, ::-1]

        elif move_dir == "up":
            bd = bd.T

        elif move_dir == "down":
            bd = bd.T[::, ::-1]
        
        emp_fields = self.get_free_fields(bd)
        # choose an empty field for a tile
        new_tile_pos = random.choice(emp_fields)
        np.random.shuffle(urn)
        if emp_fields:
            bd[new_tile_pos[0], new_tile_pos[1]] = random.choice(urn)

        # return move-reward
        return bd, reward
    
    def on_nn_btn_click(self):
        pass

    def on_exp_btn_click(self):
        pass

    def on_greedy_btn_click(self, samples):

        board = self.gameM.game_ent.boards[self.gameM.game_ent.mode].board
        rewards = []
        for i in range(4):
            move_dir = self.moves[i] # e.g.: up
            bd = board.copy()
            old_bd = board.copy()
            rewards.append(self.shift_matrix(bd, move_dir)[1])
            for _ in range(samples-1):

                up = self.shift_matrix(bd, "up")
                down = self.shift_matrix(bd, "down")
                left = self.shift_matrix(bd, "left")
                right = self.shift_matrix(bd, "right")
                bds = [up[0], down[0], left[0], right[0]]
                sample = [up[1], down[1], left[1], right[1]]

                if np.allclose(bd, old_bd):
                    bd = bds[(np.argmax(sample)+1)%4].copy()
                else:
                    bd = bds[np.argmax(sample)].copy()
                rewards[i] += np.max(sample)
                old_bd = bd.copy()
        
        #print(rewards)
        return self.moves[np.argmax(rewards)]

        '''for i in range(4):
            move = self.moves[i]
            bd = board.copy()
            rewards.append(self.shift_matrix(bd, move)[1])
            for _ in range(samples):
                bd, reward = self.shift_matrix(bd, self.on_random_btn_click())
                rewards[i] += reward

        print(f"Rewards: {rewards}")
        # get best move
        return self.moves[np.argmax(rewards)]'''

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

            self.gameM.game_ent.boards[self.gameM.game_ent.mode].anim_move = False
            self.stop_time = pg.time.get_ticks()
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
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click(10)
                self.step_run = False

            # random algorithm
            elif self.toggle_btn_row.getActiveButton() == 3:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_random_btn_click()
                self.step_run = False
        
        # run auto until stop
        elif self.auto_run and self.current_time - self.auto_run_time > 20:

            # neural network algorithm
            if self.toggle_btn_row.getActiveButton() == 0:
                pass

            # expectimax algorithm
            elif self.toggle_btn_row.getActiveButton() == 1:
                pass

            # greedy algorithm
            elif self.toggle_btn_row.getActiveButton() == 2:
                self.auto_run_time = pg.time.get_ticks()
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click(10)

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
        
