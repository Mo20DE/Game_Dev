from matplotlib.pyplot import draw
from framework.utils import *
from framework.static import *
from entities.gamedata import GameData


# game menu (in-game)
class GameMenu:

    def __init__(self, game_ent: GameData):

        # buffer which includes every important data
        self.game_ent = game_ent

        # game states
        self.states = {
            "restart_menu": False,
            "yes": False,
            "no": False
        }

        self.current_time = 0
        self.board_changed_time = 0
        self.board_changed = False
        self.canMenuBtnsClick = True

        self.keys = Keys()
        self.load_menu_variables()
    
    def load_menu_variables(self, reload_boards=False):

        # get current game theme
        theme = self.game_ent.sett_vars["theme"]
        # menu background
        self.menu_bg = game_assets[theme]["main_menu"]["surfaces"]["theme"]
        self.alpha_surf = alpha_surfs[theme]

        # surfaces
        self.menu_surfaces = {

            "icon": game_assets[theme]["game_menu"]["surfaces"]["icon"],
            "score_surf": game_assets[theme]["game_menu"]["surfaces"]["score_frame"],
            "best_score_surf": game_assets[theme]["game_menu"]["surfaces"]["best_score_frame"],
            "restart_game_bg": game_assets[theme]["game_menu"]["surfaces"]["restart_msg_bg"],
            "goal_sent_surf": game_assets[theme]["game_menu"]["surfaces"][self.get_goal_sentece()],
            "how_to_play_surf": game_assets[theme]["game_menu"]["surfaces"]["how_to_play"],
            "game_over_surf": game_assets[theme]["game_menu"]["surfaces"]["game_over_surf"]
        }

        # GUI elements
        self.buttons = {

            "home_btn": game_assets[theme]["game_menu"]["buttons"]["home_btn"],
            "restart_btn": game_assets[theme]["game_menu"]["buttons"]["new_game_short_btn"],
            "long_restart_btn": game_assets[theme]["game_menu"]["buttons"]["new_game_long_btn"],
            "undo_btn": game_assets[theme]["game_menu"]["buttons"]["undo_btn"],
            "try_again_btn": game_assets[theme]["game_menu"]["buttons"]["try_again_btn"],

            "yes_btn": game_assets[theme]["settings"]["buttons"]["yes_btn"],
            "no_btn": game_assets[theme]["settings"]["buttons"]["no_btn"]
        }

        # load every board
        if reload_boards:
            for board in self.game_ent.boards.values():
                board.load_board_variables(theme=theme)
    
    def get_goal_sentece(self):

        b_sc = self.game_ent.bestscores[self.game_ent.mode]
        if b_sc < 2048: return "goal_sent_2048"
        elif b_sc < 4096: return "goal_sent_4096"
        elif b_sc < 8192: return "goal_sent_8192"
        return "goal_sent_16384"
    
    def draw_current_score(self, screen, score):

        x_pos = score_x_pos[len(str(score))]
        Text(x_pos, 72, score, "Calibri", 25, Colors.WHITE).draw_text(screen)
    
    def draw_best_score(self, screen, score):

        if len(self.game_ent.bestscores) < len(self.game_ent.boards):
            boards = self.game_ent.boards
            for mode, board in zip(boards.keys(), boards.values()):
                if mode not in self.game_ent.bestscores:
                    self.game_ent.bestscores[mode] = board.score
        
        # update best score
        if score > self.game_ent.bestscores[self.game_ent.mode]:
            self.game_ent.bestscores[self.game_ent.mode] = score
        
        # draw best score
        x_pos = best_score_x_pos[len(str(self.game_ent.bestscores[self.game_ent.mode]))]
        Text(x_pos, 72, self.game_ent.bestscores[self.game_ent.mode], "Calibri", 25, Colors.WHITE).draw_text(screen)

    def draw_moves_counter(self, screen):

        moves_counter = str(self.game_ent.boards[self.game_ent.mode].moves_done)
        Text(45, 600, moves_counter + " Moves", "Arial", 18, moves_done_color[self.game_ent.sett_vars["theme"]]).draw_text(screen)
    
    def draw(self, screen):

        # draw menu background
        screen.blit(self.menu_bg, bg_pos)
        
        # draw images
        screen.blit(self.menu_surfaces["icon"], game_icon_pos)
        screen.blit(self.menu_surfaces["score_surf"], score_img_pos)
        screen.blit(self.menu_surfaces["best_score_surf"], best_score_img_pos)
        screen.blit(self.menu_surfaces["goal_sent_surf"], goal_sent_pos)

        # draw buttons
        self.buttons["home_btn"].blitButton(screen)
        if self.game_ent.sett_vars["show_undo"]:
            self.buttons["restart_btn"].blitButton(screen)
            self.buttons["undo_btn"].blitButton(screen)
        else:
            self.buttons["long_restart_btn"].blitButton(screen)

        # draw score of the current board
        # and best score and moves counter
        # and goal sentence
        score = self.game_ent.boards[self.game_ent.mode].score
        self.draw_current_score(screen, score)
        self.draw_best_score(screen, score)
        self.draw_moves_counter(screen)

        ### draw current board ###
        self.game_ent.boards[self.game_ent.mode].draw(screen)

        # draw game over screen if player lost
        if self.game_ent.boards[self.game_ent.mode].game_state == "lost":
            draw_alpha(screen, self.alpha_surf, alpha_pos2, alpha_val2, alpha_buffer2)
            screen.blit(self.menu_surfaces["game_over_surf"], game_over_surf_pos)
            self.buttons["try_again_btn"].blitButton(screen)

        # draw 'how to play' surface
        if self.game_ent.sett_vars["how_to"]:
            screen.blit(self.menu_surfaces["how_to_play_surf"], how_to_pos)

        # draw restart menu
        if self.states["restart_menu"]:

            draw_alpha(screen, alpha_surf, bg_pos, alpha_val, alpha_buffer)
            screen.blit(self.menu_surfaces["restart_game_bg"], restart_window_pos)
            self.buttons["yes_btn"].blitButton(screen)
            self.buttons["no_btn"].blitButton(screen)

    def update(self, mPos):

        if self.states["restart_menu"]:

            if self.buttons["yes_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_RETURN):
                self.game_ent.boards[self.game_ent.mode].restart()
                self.states["restart_menu"] = False

            elif self.buttons["no_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE):
                self.states["restart_menu"] = False
                
        else:

            self.current_time = pg.time.get_ticks()
            if self.game_ent.boards[self.game_ent.mode].tiles_moving:
                self.board_changed_time = pg.time.get_ticks()
            
            if self.current_time - self.board_changed_time > 500 and self.canMenuBtnsClick:

                # check to go back to home screen
                if self.buttons["home_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE):
                    # go back to home screen
                    self.game_ent.resetState("playing")
                    # reset previous move if back to home screens
                    self.game_ent.boards[self.game_ent.mode].prevMove = None
                
                if self.game_ent.sett_vars["show_undo"]:
                    # check restart button
                    if self.buttons["restart_btn"].isBtnClicked(mPos):
                        self.states["restart_menu"] = True
                    
                    # check undo game
                    if self.buttons["undo_btn"].isBtnClicked(mPos):
                        self.game_ent.boards[self.game_ent.mode].undoMove()
                else:
                    # check restart button
                    if self.buttons["long_restart_btn"].isBtnClicked(mPos):
                        self.states["restart_menu"] = True
            
            # update board
            if self.game_ent.boards[self.game_ent.mode].game_state != "lost":
                ### update current board ###
                self.game_ent.boards[self.game_ent.mode].update()
                # if board changed, save board
                self.board_changed = self.game_ent.boards[self.game_ent.mode].board_changed
                if self.board_changed and self.game_ent.sett_vars["sound"]:
                    self.game_ent.boards[self.game_ent.mode].make_tile_sound()
            
            else:
                if self.buttons["try_again_btn"].isBtnClicked(mPos):
                    self.game_ent.boards[self.game_ent.mode].restart()

