from menues.gamemenu import GameMenu
from framework.utils import Keys, ModeBar, SoundBar
from entities.entities import Algorithms, ButtonsRow, SpeedBar
from framework.static import *


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

        # object to handle key input
        self.keys = Keys()
        # class that includes algorithms for solving the puzzle
        self.algos = Algorithms()
        # load every needed variable
        self.load_menu_variables(load_vars=True)
    
    def load_menu_variables(self, load_vars=False):

        # get current game theme
        theme = self.gameM.game_ent.sett_vars["theme"]

        self.menu_surf = game_assets[theme]["algo_menu"]["surfaces"]["menu_bg"]
        self.buttons = {
            "ai_menu_btn": game_assets[theme]["algo_menu"]["buttons"]["ai_menu_btn"],
            "auto_run_btn": game_assets[theme]["algo_menu"]["buttons"]["auto_run_btn"],
            "stop_btn": game_assets[theme]["algo_menu"]["buttons"]["stop_btn"],
            "step_btn": game_assets[theme]["algo_menu"]["buttons"]["step_btn"]
        }

        # speed bar
        if load_vars:
            # toggle button row to choose ai strategy
            self.toggle_btn_row = ButtonsRow(
                toggle_btn_row_pos, 17, 4, 
                toggle_algo_menu_btns_path[0],
                toggle_algo_menu_btns_path[1],
                active_btn=3, axis=1, btn_gap=8
            )
            # speedbar for tile movement speed
            self.speedBar = SpeedBar(
                speed_bar_pos,
                game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][0],
                game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][0],
                game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][1],
                game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][1]
            )
        else:
            self.speedBar.bar_img = game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][0],
            self.speedBar.btn_img = game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][0],
            self.speedBar.bar_img_scroll = game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][1],
            self.speedBar.btn_img_onHover = game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][1]
    
    def on_nn_btn_click(self):
        pass

    def on_exp_btn_click(self):
        pass

    def on_greedy_btn_click(self):
        # get the best greedy move
        board = self.gameM.game_ent.boards[self.gameM.game_ent.mode].board
        return self.algos.greedyStrategy(board=board, samples=2, depth=5)

    def on_random_btn_click(self):
        # generate a random move
        return self.algos.randomStrategy()
    
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
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click()
                self.step_run = False

            # random algorithm
            elif self.toggle_btn_row.getActiveButton() == 3:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_random_btn_click()
                self.step_run = False
        
        # run auto until stop
        elif self.auto_run and self.current_time - self.auto_run_time > self.algos.speed:

            # neural network algorithm
            if self.toggle_btn_row.getActiveButton() == 0:
                pass

            # expectimax algorithm
            elif self.toggle_btn_row.getActiveButton() == 1:
                pass

            # greedy algorithm
            elif self.toggle_btn_row.getActiveButton() == 2:
                self.auto_run_time = pg.time.get_ticks()
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.on_greedy_btn_click()

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

                self.speedBar.draw(screen)

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
                    self.speedBar.update(mPos)

