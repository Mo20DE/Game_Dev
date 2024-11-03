from framework.static import *
from entities.entities import Algorithms
from framework.utils import Keys, ButtonsRow, SpeedBar
# from framework.helper import CodeEditor
from entities.custom_algo import custom_algo


class AlgoMenu:

    def __init__(self, gameM):

        # game menu instance
        self.gameM = gameM
        self.menu_status = "unfolded" # unfolded/collapsed
        self.step_run = False
        self.auto_run = False

        self.tile_speed = 0
        self.step_time = 0
        self.stop_time = 0
        self.auto_run_time = 0

        # class that handles key input
        self.keys = Keys(esc_key=False)
        # class that includes algorithms for solving the puzzle
        self.algos = Algorithms()
        # class that represents a code editor
        # self.code_editor = CodeEditor()
    
    def load_menu_variables(self, theme, load_vars=True):

        self.menu_surf = game_assets[theme]["algo_menu"]["surfaces"]["menu_bg"]
        self.buttons = {
            "ai_menu_btn": game_assets[theme]["algo_menu"]["buttons"]["ai_menu_btn"],
            "auto_run_btn": game_assets[theme]["algo_menu"]["buttons"]["auto_run_btn"],
            "stop_btn": game_assets[theme]["algo_menu"]["buttons"]["stop_btn"],
            "step_btn": game_assets[theme]["algo_menu"]["buttons"]["step_btn"],
            "add_algo_btn": game_assets[theme]["algo_menu"]["buttons"]["add_algo_btn"]
        }
        self.load_ai_menu_btn_pos()

        # speed bar
        if load_vars:
            # toggle button row to choose ai strategy
            self.toggle_btn_row = ButtonsRow(
                toggle_btn_row_pos, 17, 4, 
                toggle_algo_menu_btns_path[0],
                toggle_algo_menu_btns_path[1],
                active_btn=2, axis=1, btn_gap=10
            )
            # speedbar for tile movement speed
            self.speedBar = SpeedBar(
                speed_bar_pos,
                game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][0],
                game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][0],
                game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][1],
                game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][1],
                def_btn_pos="middle"
            )
            self.speedBar.defineMixerInterval(15, [1000, 30])
        else:
            self.speedBar.setPropertyImg(game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][0], prop="bar")
            self.speedBar.setPropertyImg(game_assets[theme]["algo_menu"]["surfaces"]["speed_bar"][1], prop="bar_scroll")
            self.speedBar.setPropertyImg(game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][0]),
            self.speedBar.setPropertyImg(game_assets[theme]["algo_menu"]["buttons"]["speed_bar_btn"][1], prop="btn_oh")
    
    def reset_menu(self):

        if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_2")
        self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
            can_do_move=True, anim_spawn=True, anim_move=True)
        self.menu_status = "unfolded"
        self.auto_run = False
        
    def load_ai_menu_btn_pos(self):

        if self.gameM.game_ent.sett_vars["how_to"]:
            self.buttons["ai_menu_btn"].resetButtonPos()
        else: self.buttons["ai_menu_btn"].setButtonPos((165, 660))

    def setBoardAttributes(self):

        mxr_idx = self.speedBar.getCurrentMixerPoint(only_idx=True)
        self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
            anim_spawn=True if mxr_idx <= 10 else False)
        self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
            anim_move=True if mxr_idx <= 11 else False)
    
    def handleMenuButtonsActions(self, mPos):

        # get local scope time
        current_time = pg.time.get_ticks()

        # handle button actions
        if self.gameM.game_ent.boards[self.gameM.game_ent.mode].game_state != "lost":
            if not self.auto_run :

                if self.buttons["add_algo_btn"].isBtnClicked(mPos):
                    # self.code_editor.run_code_editor()
                    pass

                elif self.buttons["step_btn"].isBtnClicked(mPos):

                    if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                    self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
                        ai_used=True, can_do_move=False)
                    self.step_time = pg.time.get_ticks()
                    self.step_run = True

                elif self.buttons["auto_run_btn"].isBtnClicked(mPos):

                    self.setBoardAttributes()
                    if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                    self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
                        ai_used=True, can_do_move=False)
                    self.stop_time = pg.time.get_ticks()
                    self.auto_run = True
          
            elif (self.buttons["stop_btn"].isBtnClicked(mPos) and current_time - self.stop_time > 400):

                if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
                    can_do_move=True, anim_spawn=True, anim_move=True)
                self.auto_run = False
        
        elif self.auto_run:
            self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
                can_do_move=True, anim_spawn=True, anim_move=True)
            self.auto_run = False
        
        ### run algorithms ###

        board = self.gameM.game_ent.boards[self.gameM.game_ent.mode].board
        # run one step
        if self.step_run or (self.auto_run and current_time - 
            self.auto_run_time > self.speedBar.getCurrentMixerPoint()):

            # custom algorithm:
            if self.toggle_btn_row.active_btn == 0:
                
                # self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = exec(self.code_editor.code)
                pass
            
            # expectimax algorithm
            elif self.toggle_btn_row.active_btn == 1:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.algos.smartStrategy(board, 3)

            # greedy algorithm
            elif self.toggle_btn_row.active_btn == 2:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.algos.greedyStrategy(board, 3)

            # random algorithm
            else:
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].curr_move = self.algos.randomStrategy()

            # reset flag    
            if self.step_run: self.step_run = False
            else: self.auto_run_time = pg.time.get_ticks()
        
    def draw(self, screen):

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
            game_state = self.gameM.game_ent.boards[self.gameM.game_ent.mode].game_state
            if not self.auto_run and game_state != "lost": 
                self.buttons["step_btn"].blitButton(screen)
                self.buttons["auto_run_btn"].blitButton(screen)
                if self.toggle_btn_row.active_btn == 0:
                    self.buttons["add_algo_btn"].blitButton(screen)

            else: 
                self.gameM.draw_deact_game_menu_btn_images(screen, only_step_auto_run=True 
                    if game_state == "lost" else False)
                if game_state != "lost": self.buttons["stop_btn"].blitButton(screen)

            # draw speed bar

            self.speedBar.draw(screen)

    def update(self, mPos):

        if self.menu_status == "unfolded":
            if self.buttons["ai_menu_btn"].isBtnClicked(mPos):
                if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                # ai menu button pressed
                self.menu_status = "collapsed"
        else:

            # quit button pressed
            if (quit_btn.isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key")):
                self.reset_menu()
            # update toggle button row
            elif self.toggle_btn_row.updateButtonRow(mPos):
                if self.gameM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.gameM.game_ent.boards[self.gameM.game_ent.mode].set_board_flags(
                    can_do_move=True, anim_spawn=True, anim_move=True)
                self.auto_run = False
            else:
                # handle menu auto-run, step, stop button actions
                self.handleMenuButtonsActions(mPos)
                if self.speedBar.update(mPos, btn_react_on_bar=True):
                    self.setBoardAttributes()
            
