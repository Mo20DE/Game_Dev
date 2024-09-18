from framework.utils import *
from framework.static import *
from entities.gamedata import GameData
from menues.algomenu import AlgoMenu


# game menu (in-game)
class GameMenu:

    def __init__(self, game_ent: GameData):

        # buffer which includes every important data
        self.game_ent = game_ent
        self.algoM = AlgoMenu(self)

        self.restart_menu = False
        self.board_changed = False
        self.timer = 0

        self.keys = Keys(ret_key=False, esc_key=False)
        self.load_menu_variables(load_algoM=True)

    def load_menu_variables(self, reload_boards=False, load_algoM=False):

        # get current game theme
        theme = self.game_ent.sett_vars["theme"]
        self.algoM.load_menu_variables(theme, load_vars=(True if load_algoM else False))
        self.load_next_goal = True

        # menu background
        self.menu_bg = game_assets[theme]["main_menu"]["surfaces"]["theme"]
        self.alpha_surf = alpha_surfs[theme]

        # surfaces
        self.menu_surfaces = {

            "icon": game_assets[theme]["game_menu"]["surfaces"]["icon"],
            "score_surf": game_assets[theme]["game_menu"]["surfaces"]["score_frame"],
            "best_score_surf": game_assets[theme]["game_menu"]["surfaces"]["best_score_frame"],
            "restart_game_bg": game_assets[theme]["game_menu"]["surfaces"]["restart_msg_bg"],
            "how_to_play_surf": game_assets[theme]["game_menu"]["surfaces"]["how_to_play"],
        }

        # GUI elements
        self.buttons = {

            "home_btn": game_assets[theme]["game_menu"]["buttons"]["home_btn"],
            "restart_btn": game_assets[theme]["game_menu"]["buttons"]["new_game_short_btn"],
            "long_restart_btn": game_assets[theme]["game_menu"]["buttons"]["new_game_long_btn"],
            "undo_btn": game_assets[theme]["game_menu"]["buttons"]["undo_btn"],
            "try_again_btn": game_assets[theme]["game_menu"]["buttons"]["try_again_btn"],

            "yes_btn": game_assets[theme]["settings"]["buttons"]["yes_btn"],
            "no_btn": game_assets[theme]["settings"]["buttons"]["no_btn"],
            "made_by_btn": game_assets[theme]["main_menu"]["buttons"]["made_by_btn"]
        }

        if self.load_next_goal: self.load_next_goal_tile()

        self.game_over_surf = Text(
            game_over_surf_pos[0], game_over_surf_pos[1], "Game Over!", 
            "Arial", 56, moves_done_color[theme], bold=True
        )
        size = 15
        self.how_to_play_text = [
            Text(how_to_pos[0], how_to_pos[1]+5, "How To Play:                 arrow keys", "Arial", size, moves_done_color[theme], bold=True),
            Text(how_to_pos[0]+97, how_to_pos[1]+5, "Use your                     to move the tiles. When", "Arial", size, moves_done_color[theme]),
            Text(how_to_pos[0], how_to_pos[1]+25, "two tiles with the same number touch, they", "Arial", size, moves_done_color[theme]),
            Text(how_to_pos[0]+282, how_to_pos[1]+25, "merge into one!", "Arial", size, moves_done_color[theme], bold=True)
        ]
        # load every board
        if reload_boards:
            for board in self.game_ent.boards.values():
                board.load_board_variables(theme=theme)
    
    def draw_current_score(self, screen, score):

        x_pos = score_x_pos[len(str(score))]
        Text(x_pos, 72, score, "Calibri", 25, Colors.WHITE, bold=True).draw_text(screen)

        score_buff = self.game_ent.boards[self.game_ent.mode].score_buff
        if score_buff[0] > 0:
            score_buff[1].draw_text(screen)
            score_buff[1].set_alpha(-10, shift=True)
            if score_buff[1].y > 5: 
                score_buff[1].y -= 3
                self.game_ent.boards[self.game_ent.mode].score_buff = score_buff
            else: 
                self.game_ent.boards[self.game_ent.mode].resetScoreBuffer()
        
    def draw_best_score(self, screen, score):

        # update best score
        if score > self.game_ent.bestscores[self.game_ent.mode]:
            self.game_ent.bestscores[self.game_ent.mode] = score
        
        # draw best score
        x_pos = best_score_x_pos[len(str(self.game_ent.bestscores[self.game_ent.mode]))]
        Text(x_pos, 72, self.game_ent.bestscores[self.game_ent.mode], "Calibri", 25, Colors.WHITE, bold=True).draw_text(screen)

    def draw_moves_counter(self, screen):

        moves_counter = str(self.game_ent.boards[self.game_ent.mode].moves_done)
        Text(45, 600, moves_counter + " Moves", "Calibri", 18, moves_done_color[self.game_ent.sett_vars["theme"]]).draw_text(screen)
    
    def draw_deact_game_menu_btn_images(self, screen, only_step_auto_run=True):

        if not only_step_auto_run:
            is_undo_on = self.game_ent.sett_vars["show_undo"]
            screen.blit(deact_btn_imgs["home"], home_btn_pos)
            screen.blit(deact_btn_imgs["new"] if is_undo_on else deact_btn_imgs["new_long"], 
                new_game_btn_pos if is_undo_on else long_restart_btn_pos)
            if is_undo_on: screen.blit(deact_btn_imgs["undo"], undo_btn_pos)
        else: screen.blit(deact_btn_imgs["auto_run"], auto_run_btn_pos)
        screen.blit(deact_btn_imgs["step"], step_btn_pos)
    
    def draw_game_timer(self, screen):

        curr_timer = self.game_ent.board_timers[self.game_ent.mode]
        parsed_time = curr_timer.split(":")
        str_len = sum([len(_str) for _str in parsed_time])

        if (self.game_ent.boards[self.game_ent.mode].game_state != "lost" and not 
            self.restart_menu and curr_timer != "99:59:59"):

            curr_time = pg.time.get_ticks()
            if curr_time - self.timer >= 1000: # triggers if one second is over

                self.timer = pg.time.get_ticks()
                num = int(parsed_time[-1])+1
                if num < 10: 
                    parsed_time[-1] = ':0'+str(num) # seconds
                elif num < 60:
                    parsed_time[-1] = ':'+str(num) # seconds
                else:
                    parsed_time[-1] = ':00' # seconds
                    num2 = int(parsed_time[-2]) # minutes
                    if num2 == 59:
                        parsed_time[-2] = ':00' # minutes
                        if len(parsed_time) == 2:
                            parsed_time = ['1', ':00', ':00'] # hours
                        else:
                            parsed_time[0] = str(int(parsed_time[0])+1) # hours
                    else:
                        if len(parsed_time) == 2:
                            parsed_time[-2] = str(num2+1) # minutes
                        else:
                            if num2+1 < 10:
                                parsed_time[-2] = ':0'+str(num2+1) # minutes
                            else:
                                parsed_time[-2] = ':'+str(num2+1) # minutes
            
                curr_timer = ""
                for i, _str in enumerate(parsed_time):
                    if i > 0 and _str[0] != ':': 
                        curr_timer += ':'+_str
                    else: curr_timer += _str

                # update timer
                self.game_ent.board_timers[self.game_ent.mode] = curr_timer
        # draw timer
        Text(timer_y_pos[str_len], 600, curr_timer, "Calibri", 18, 
            moves_done_color[self.game_ent.sett_vars["theme"]]).draw_text(screen)
    
    def load_next_goal_tile(self):

        self.next_goal_tile = Text(
            goal_sent_pos[0], goal_sent_pos[1], 
            next_goal_sent[self.game_ent.next_goal_tiles[self.game_ent.mode]],
            "Arial", 18, moves_done_color[self.game_ent.sett_vars["theme"]]
        )

    def check_next_goal_tile(self):

        mode = self.game_ent.mode
        max_tile = max([tile.num for tile in self.game_ent.boards[mode].board_tiles.values()])
        if max_tile == int(self.game_ent.next_goal_tiles[mode]) and max_tile != 2097152:
            max_tile = str(max_tile*2)
            self.game_ent.next_goal_tiles[mode] = max_tile
            self.next_goal_tile.text = next_goal_sent[max_tile]
    
    def draw_how_to_play(self, screen):

        for text in self.how_to_play_text:
            text.draw_text(screen)
    
    def draw(self, screen):

        # draw menu background
        screen.blit(self.menu_bg, bg_pos)
        
        # draw images
        screen.blit(self.menu_surfaces["icon"], game_icon_pos)
        screen.blit(self.menu_surfaces["score_surf"], score_img_pos)
        screen.blit(self.menu_surfaces["best_score_surf"], best_score_img_pos)
        self.buttons["made_by_btn"].blitButton(screen)
        if self.load_next_goal: self.load_next_goal_tile()
        self.next_goal_tile.draw_text(screen)

        # draw buttons
        if not self.algoM.auto_run:
            self.buttons["home_btn"].blitButton(screen)
            if self.game_ent.sett_vars["show_undo"]:
                self.buttons["restart_btn"].blitButton(screen)
                self.buttons["undo_btn"].blitButton(screen)
            else: self.buttons["long_restart_btn"].blitButton(screen)

        # draw score of the current board
        # and best score and moves counter
        # and goal sentence
        score = self.game_ent.boards[self.game_ent.mode].score
        self.draw_current_score(screen, score)
        self.draw_best_score(screen, score)
        self.draw_moves_counter(screen)
        self.draw_game_timer(screen)

        ### draw current board ###
        self.game_ent.boards[self.game_ent.mode].draw(screen)

        # draw game over screen if player lost
        if self.game_ent.boards[self.game_ent.mode].game_state == "lost":
            draw_alpha(screen, self.alpha_surf, alpha_pos2, alpha_val2)
            self.game_over_surf.draw_text(screen)
            self.buttons["try_again_btn"].blitButton(screen)

        # draw 'how to play' surface
        if self.game_ent.sett_vars["how_to"]: self.draw_how_to_play(screen)
        # draw algoMenu
        if self.game_ent.sett_vars["show_ai_menu"]: self.algoM.draw(screen)
        
        # draw restart menu
        if self.restart_menu:

            draw_alpha(screen, alpha_surf, bg_pos, alpha_val)
            screen.blit(self.menu_surfaces["restart_game_bg"], restart_window_pos)
            self.buttons["yes_btn"].blitButton(screen)
            self.buttons["no_btn"].blitButton(screen)

    def update(self, mPos):

        if self.restart_menu:

            if self.buttons["yes_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_RETURN, "ret_key"):
                
                if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                #if self.game_ent.boards[self.game_ent.mode].game_state != "lost":
                    #check_new_stats([self.game_ent.boards[self.game_ent.mode], True])
                
                self.game_ent.boards[self.game_ent.mode].restart()
                self.game_ent.board_timers[self.game_ent.mode] = "0:00"
                self.keys.reset_bools("esc_key")
                self.timer = pg.time.get_ticks()
                self.restart_menu = False

            elif self.buttons["no_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.keys.reset_bools("ret_key")
                self.timer = pg.time.get_ticks()
                self.restart_menu = False
        else:
            curr_time = pg.time.get_ticks()
            # update game menu buttons
            if not self.algoM.auto_run and not self.game_ent.boards[self.game_ent.mode].tiles_moving:
                # check to go back to home screen
                if self.buttons["home_btn"].isBtnClicked(mPos) or (self.keys.keyPressed(pg.K_ESCAPE, "esc_key") 
                    and self.algoM.menu_status == "unfolded"):

                    if self.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                    self.game_ent.boards[self.game_ent.mode].resetScoreBuffer()
                    # reset previous move if back to home screens
                    self.game_ent.boards[self.game_ent.mode].prevMove.init_move()
                    # reset algo menu
                    self.algoM.reset_menu()
                    self.keys.reset_bools("esc_key")
                    # go back to home screen
                    self.game_ent.resetState("playing")
                    self.buttons["home_btn"].btn_clicked = False
                    self.load_next_goal = True
                
                elif self.game_ent.sett_vars["show_undo"]:
                    # check restart button
                    if self.buttons["restart_btn"].isBtnClicked(mPos):
                        if self.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                        self.restart_menu = True
                    
                    # check undo game
                    elif self.buttons["undo_btn"].isBtnClicked(mPos):
                        if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                        self.game_ent.boards[self.game_ent.mode].undoMove()

                elif self.buttons["long_restart_btn"].isBtnClicked(mPos):
                    # check restart button
                    if self.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                    self.restart_menu = True
                
                if self.restart_menu: 
                    self.game_ent.boards[self.game_ent.mode].set_board_flags(anim_spawn=True, anim_move=True)
            
            # update board
            if self.game_ent.boards[self.game_ent.mode].game_state != "lost":
                ### update current board ###
                self.game_ent.boards[self.game_ent.mode].update()
                if curr_time - self.algoM.step_time > 600 and not self.algoM.auto_run:
                    self.game_ent.boards[self.game_ent.mode].can_do_move = True
                # check next goal tile
                self.check_next_goal_tile()
                # if board changed, save board
                board = self.game_ent.boards[self.game_ent.mode]
                self.board_changed = board.board_changed
                if self.board_changed:
                    #check_new_stats([self.game_ent.boards[self.game_ent.mode], False, self.game_ent.boards[self.game_ent.mode].score])
                    if self.game_ent.sett_vars["sound"] and not board.reset_o_undo:
                        self.game_ent.boards[self.game_ent.mode].make_tile_sound()
                    if board.reset_o_undo: self.game_ent.boards[self.game_ent.mode].reset_o_undo = False
                
            elif self.buttons["try_again_btn"].isBtnClicked(mPos):
                if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.game_ent.boards[self.game_ent.mode].restart()
                self.game_ent.board_timers[self.game_ent.mode] = "0:00"
                self.timer = pg.time.get_ticks()
            
            # update algoMenu
            if self.game_ent.sett_vars["show_ai_menu"]: 
                self.algoM.update(mPos)
                if not self.game_ent.game_states["playing"]: 
                    self.algoM.reset_menu()
            if self.algoM.menu_status == "unfolded":
                self.buttons["made_by_btn"].isBtnClickedOpenLink(mPos)
        
