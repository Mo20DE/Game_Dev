from framework.utils import *
from framework.static import *
from entities.statistics import Statistics

from menues.mainmenu import MainMenu
from menues.gamemenu import GameMenu

        

class SettingsMenu:

    def __init__(self, mainM: MainMenu, gameM: GameMenu):

        self.mainM = mainM
        self.gameM = gameM

        # attribute to control reset actions
        self.del_res_menu_stage = 1
        self.del_res_buff = None
        self.keys = Keys(ret_key=False, esc_key=False)
        self.stats = Statistics(self)

        self.menu_surf_states = {

            "show_stats": False,

            "show_no_b_data_surf": False, # show "no board data availible to delete" surface
            "show_del_b_data_surf": False, # show "delete board data" surface

            "show_no_mode_b_data_surf": False, # show "no 'mode' board data available" surface
            "show_yes_no_b_data_surf": False, # show "sure to delete board data" surface

            "show_no_b_sc_surf": False, # show "no best score availible to delete" surface
            "show_b_sc_surf": False, # show "reset best score" surface

            "show_no_mode_b_sc_surf": False, # show "no 'mode' best score data available" surface
            "show_yes_no_b_sc_surf": False # show "sure to delete best score" surface
        }

        # load every needed variable
        self.load_menu_variables()
        # load and set toggle buttons
        self.setToggleButtons()

    def load_menu_variables(self):
        
        # get current game theme
        theme = self.mainM.game_ent.sett_vars["theme"]

        # set app icon
        pg.display.set_icon(game_assets[theme]["game_menu"]["surfaces"]["icon"])

        # surfaces
        self.menu_surf = {

            "menu_bg": game_assets[theme]["settings"]["surfaces"]["sett_bg"],
            "board_msg": {

                "delete_board_bg": game_assets[theme]["settings"]["surfaces"]["delete_board_bg"],

                "3x3_del_board": game_assets[theme]["settings"]["surfaces"]["3x3_board_msg"],
                "4x4_del_board": game_assets[theme]["settings"]["surfaces"]["4x4_board_msg"],
                "5x5_del_board": game_assets[theme]["settings"]["surfaces"]["5x5_board_msg"],
                "all_del_board": game_assets[theme]["settings"]["surfaces"]["all_board_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_not_msg"]
            },

            "b_score_msg": {

                "reset_b_sc_bg": game_assets[theme]["settings"]["surfaces"]["reset_b_sc_bg"],

                "3x3_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_msg"],
                "4x4_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_msg"],
                "5x5_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_msg"],
                "all_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["all_b_sc_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_b_sc_not_msg"]
            }
        }

        # temporary surface
        self.com_soon_surf = Surface(restart_window_pos, restart_window_size, com_soon_surf_clr[theme], roundness=12)
        self.com_soon_text = Text(100, 230, "Coming Soon", "Arial", 38, moves_done_color[theme], bold=True)

        # GUI elements
        self.menu_btns = {

            "stats_btn": game_assets[theme]["settings"]["buttons"]["stats_btn"],
            "del_board_btn": game_assets[theme]["settings"]["buttons"]["boards_delete_btn"],
            "reset_b_sc_btn": game_assets[theme]["settings"]["buttons"]["best_score_reset_btn"],
            "back_btn": game_assets[theme]["settings"]["buttons"]["back_home_btn"],

            "yes_btn": game_assets[theme]["settings"]["buttons"]["yes_btn"],
            "no_btn": game_assets[theme]["settings"]["buttons"]["no_btn"],
            "ok_btn": game_assets[theme]["settings"]["buttons"]["ok_btn"],

            "3x3_reset_btn": game_assets[theme]["settings"]["buttons"]["3x3_reset_btn"],
            "4x4_reset_btn": game_assets[theme]["settings"]["buttons"]["4x4_reset_btn"],
            "5x5_reset_btn": game_assets[theme]["settings"]["buttons"]["5x5_reset_btn"],
            "all_reset_btn": game_assets[theme]["settings"]["buttons"]["all_reset_btn"]
        }

    def setToggleButtons(self):

        self.toggle_btns = {

            "toggle_sound_btn": toggle_btns["toggle_sound_btn"],
            "toggle_undo_btn": toggle_btns["toggle_undo_btn"],
            "toggle_ai_menu_btn": toggle_btns["toggle_ai_menu_btn"],
            "toggle_how_to_btn": toggle_btns["toggle_how_to_btn"],
            "toggle_game_theme_btn": toggle_btns["toggle_game_theme_btn"]
        }

        sett_vars = self.mainM.game_ent
        # set status of toggle buttons
        self.toggle_btns["toggle_sound_btn"].set_button_status(sett_vars.getButtonStatus("sound"))
        self.toggle_btns["toggle_undo_btn"].set_button_status(sett_vars.getButtonStatus("show_undo"))
        self.toggle_btns["toggle_ai_menu_btn"].set_button_status(sett_vars.getButtonStatus("show_ai_menu"))
        self.toggle_btns["toggle_how_to_btn"].set_button_status(sett_vars.getButtonStatus("how_to"))
        self.toggle_btns["toggle_game_theme_btn"].set_button_status(sett_vars.getButtonStatus("theme"))
    
    def reset_menu_variables(self, *args, drm_stage=1, reset_all=False, settings=False):
        
        # reset main flag
        self.del_res_menu_stage = drm_stage

        if not reset_all:
            # reset specific menu surface state variables
            for arg in args: self.menu_surf_states[arg] = False
        
        else:
            self.mainM.game_ent.resetState("settings", settings)
            # reset every menu surface state variable
            self.menu_surf_states = {

                "show_stats": False,

                "show_no_b_data_surf": False, # show "no board data availible to delete" surface
                "show_del_b_data_surf": False, # show "delete board data" surface

                "show_no_mode_b_data_surf": False, # show "no 'mode' board data available" surface
                "show_yes_no_b_data_surf": False, # show "sure to delete board data" surface

                "show_no_b_sc_surf": False, # show "no best score availible to delete" surface
                "show_b_sc_surf": False, # show "reset best score" surface

                "show_no_mode_b_sc_surf": False, # show "no 'mode' best score data available" surface
                "show_yes_no_b_sc_surf": False # show "sure to delete best score" surface
            }
    
    def deleteData(self, state):

        # get correct game mode
        mode = self.del_res_buff
        # reset board data
        if state == "show_yes_no_b_data_surf":
            self.mainM.game_ent.resetData(mode, True)
        # reset best score
        else: self.mainM.game_ent.resetData(mode, False)
    
    def changeGameTheme(self):
        
        # releoad object properties
        self.load_menu_variables()
        self.mainM.load_menu_variables()
        self.gameM.load_menu_variables(reload_boards=True)
        self.stats.load_variables(changePageTheme=True)
    
    def drawOne(self, screen, state, key, surf):

        if self.menu_surf_states[state]:

            # draw notifications message
            screen.blit(self.menu_surf[key][surf], restart_window_pos)
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
    
    def drawTwo(self, screen, state, key, surf):

        if self.menu_surf_states[state]:

            # draw notifications message
            screen.blit(self.menu_surf[key][surf], restart_window_pos)
            # draw quit btn
            quit_btn.blitButton(screen)

            # draw buttons for delete options
            self.menu_btns["3x3_reset_btn"].blitButton(screen)
            self.menu_btns["4x4_reset_btn"].blitButton(screen)
            self.menu_btns["5x5_reset_btn"].blitButton(screen)
            self.menu_btns["all_reset_btn"].blitButton(screen)

    def drawThree(self, screen, state, key):

        if self.menu_surf_states[state]:
            
            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf[key]["3x3_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf[key]["4x4_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf[key]["5x5_notf_msg"], restart_window_pos)
            
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
    
    def drawFour(self, screen, state, key, surf1, surf2, surf3, surf4):

        if self.menu_surf_states[state]:

            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf[key][surf1], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf[key][surf2], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf[key][surf3], restart_window_pos)
            
            elif self.del_res_buff == "all":
                screen.blit(self.menu_surf[key][surf4], restart_window_pos)
            
            # draw yes button
            self.menu_btns["yes_btn"].blitButton(screen)
            # draw no button
            self.menu_btns["no_btn"].blitButton(screen)

    def handleMenuCase(self, case, mode=None):

        # lock other buttons
        boards = self.mainM.game_ent.boards
        best_scores = self.mainM.game_ent.bestscores

        if case == "1.1":

            # go to next stage
            self.del_res_menu_stage = 2
            # no board data availible to delete<
            if len(boards) == 0:
                self.menu_surf_states["show_no_b_data_surf"] = True
            # board data available to delete
            else:
                self.menu_surf_states["show_del_b_data_surf"] = True
        
        elif case == "1.2":

            # go to next stage
            self.del_res_menu_stage = 3
            # save picked mode
            self.del_res_buff = mode

            if mode != "all" and mode not in boards:
                self.menu_surf_states["show_no_mode_b_data_surf"] = True
            else:
                self.menu_surf_states["show_yes_no_b_data_surf"] = True
            
        elif case == "2.1":

            # go to next stage
            self.del_res_menu_stage = 2
            # no best score available to delete
            if sum([b_sc for b_sc in best_scores.values()]) == 0:
                self.menu_surf_states["show_no_b_sc_surf"] = True
            # best score available to delete
            else:
                self.menu_surf_states["show_b_sc_surf"] = True
        
        elif case == "2.2":

            # go to next stage
            self.del_res_menu_stage = 3
            # save picked mode
            self.del_res_buff = mode

            if mode != "all":
                if best_scores[mode] == 0:
                    self.menu_surf_states["show_no_mode_b_sc_surf"] = True
                else:
                    self.menu_surf_states["show_yes_no_b_sc_surf"] = True
            else:
                self.menu_surf_states["show_yes_no_b_sc_surf"] = True
    
    def handleStageOne(self, mPos):

        # case 1: statistics button clicked
        if self.menu_btns["stats_btn"].isBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.menu_surf_states["show_stats"] = True

        # case 2: delete board button clicked
        elif self.menu_btns["del_board_btn"].isBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            # handle case 1
            self.handleMenuCase(case="1.1")

        # case 3: reset best score button clicked
        elif self.menu_btns["reset_b_sc_btn"].isBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            # handle case 2
            self.handleMenuCase(case="2.1")
        
        # case 4: sound toggle button clicked
        elif self.toggle_btns["toggle_sound_btn"].isToggleBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.mainM.game_ent.changeValue("sound")

        # case 5: undo toggle button clicked
        elif self.toggle_btns["toggle_undo_btn"].isToggleBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.mainM.game_ent.changeValue("show_undo")
        
        # case 6: ai menu toggle button clicked
        elif self.toggle_btns["toggle_ai_menu_btn"].isToggleBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.mainM.game_ent.changeValue("show_ai_menu")
        
        # case 7: how-to toggle button clicked
        elif self.toggle_btns["toggle_how_to_btn"].isToggleBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.mainM.game_ent.changeValue("how_to")
            self.gameM.algoM.load_ai_menu_btn_pos()

        # case 8: game theme toggle button clicked
        elif self.toggle_btns["toggle_game_theme_btn"].isToggleBtnClicked(mPos):
            if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.mainM.game_ent.changeValue("theme")
            self.changeGameTheme()
        
        self.mainM.menu_btns["made_by_btn"].isBtnClickedOpenLink(mPos)
        
    def handleStageTwo(self, mPos, state1, state2, case):

        ### board data ###
        # nothing to delete (board data/best score)
        if self.menu_surf_states[state1]:

            # ok button clicked
            if self.menu_btns["ok_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.reset_menu_variables(state1)
        
        # there are board data/best scores to delete
        elif self.menu_surf_states[state2]:
            
            # quit button clicked
            if quit_btn.isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                self.reset_menu_variables(state2)

            # 3x3 button clicked
            elif self.menu_btns["3x3_reset_btn"].isBtnClicked(mPos):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.handleMenuCase(case=case ,mode="3x3")

            # 4x4 button clicked
            elif self.menu_btns["4x4_reset_btn"].isBtnClicked(mPos):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.handleMenuCase(case=case, mode="4x4")

            # 4x4 button clicked
            elif self.menu_btns["5x5_reset_btn"].isBtnClicked(mPos):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.handleMenuCase(case=case, mode="5x5")

            # all button clicked
            elif self.menu_btns["all_reset_btn"].isBtnClicked(mPos):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.handleMenuCase(case=case, mode="all")
    
    def handleStageThree(self, mPos, state1, state2):

            
        # can't delete specfic mode board data/best score
        if self.menu_surf_states[state1]:

            # ok button clicked
            if self.menu_btns["ok_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.reset_menu_variables(state1, drm_stage=2)
        
        elif self.menu_surf_states[state2]:

            # yes button clicked
            if self.menu_btns["yes_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_RETURN, "ret_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                
                # delete data
                self.deleteData(state2)
                self.reset_menu_variables(reset_all=True, settings=True)

            # no button clicked
            elif self.menu_btns["no_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.reset_menu_variables(state2, drm_stage=2)
    
    def draw(self, screen):

        if not self.menu_surf_states["show_stats"]:

            # draw menu background
            screen.blit(self.menu_surf["menu_bg"], bg_pos)
            self.mainM.menu_btns["made_by_btn"].blitButton(screen)

            # draw statistics button
            self.menu_btns["stats_btn"].blitButton(screen)
            # draw delete board data button
            self.menu_btns["del_board_btn"].blitButton(screen)
            # draw reset best score button
            self.menu_btns["reset_b_sc_btn"].blitButton(screen)

            # draw "sound" toggle button
            self.toggle_btns["toggle_sound_btn"].blitButton(screen)
            # draw "show undo" toggle button
            self.toggle_btns["toggle_undo_btn"].blitButton(screen)
            #draw "show ai menu" toggle button
            self.toggle_btns["toggle_ai_menu_btn"].blitButton(screen)
            # draw "how-to" toggle button
            self.toggle_btns["toggle_how_to_btn"].blitButton(screen)
            # draw "game theme" toggle button
            self.toggle_btns["toggle_game_theme_btn"].blitButton(screen)
            
            # draw back button
            self.menu_btns["back_btn"].blitButton(screen)

            # draw menu surfaces
            if any(self.menu_surf_states.values()):
                draw_alpha(screen, alpha_surf, bg_pos, alpha_val)

            ### board data ###
            self.drawOne(screen, "show_no_b_data_surf", "board_msg", "all_notf_msg")
            self.drawTwo(screen, "show_del_b_data_surf", "board_msg", "delete_board_bg")
            self.drawThree(screen, "show_no_mode_b_data_surf", "board_msg")
            self.drawFour(screen, "show_yes_no_b_data_surf", "board_msg", "3x3_del_board", 
            "4x4_del_board", "5x5_del_board", "all_del_board")

            ### best score ###
            self.drawOne(screen, "show_no_b_sc_surf", "b_score_msg", "all_notf_msg")
            self.drawTwo(screen, "show_b_sc_surf", "b_score_msg", "reset_b_sc_bg")
            self.drawThree(screen, "show_no_mode_b_sc_surf", "b_score_msg")
            self.drawFour(screen, "show_yes_no_b_sc_surf", "b_score_msg", "3x3_reset_b_sc", 
            "4x4_reset_b_sc", "5x5_reset_b_sc", "all_reset_b_sc")

            if self.menu_surf_states["show_stats"]:
                self.com_soon_surf.draw_surface(screen)
                self.com_soon_text.draw_text(screen)
                self.menu_btns["ok_btn"].blitButton(screen)

        else:
            # draw statistics page
            self.stats.draw_stats(screen)

    def update(self, mPos):

        # statistics button clicked
        if self.menu_surf_states["show_stats"]:

            # update statistics page
            self.stats.update_stats(mPos)

        # "delete board" and "reset best score" buttons can be clicked
        elif self.del_res_menu_stage == 1:

            # handle menu
            self.handleStageOne(mPos)
            # back button clicked (reset settings menu)
            if self.menu_btns["back_btn"].isBtnClicked(mPos) or self.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                self.keys.reset_bools("esc_key")
                self.reset_menu_variables(reset_all=True)

        elif self.del_res_menu_stage == 2:

            ### board data ###
            self.handleStageTwo(mPos, "show_no_b_data_surf", "show_del_b_data_surf", "1.2")
            ### best score ###
            self.handleStageTwo(mPos, "show_no_b_sc_surf", "show_b_sc_surf", "2.2")
                
        # menu stage 3 (last stage)
        else:
            ### board data ###
            self.handleStageThree(mPos, "show_no_mode_b_data_surf", "show_yes_no_b_data_surf")
            ### best score ###
            self.handleStageThree(mPos, "show_no_mode_b_sc_surf", "show_yes_no_b_sc_surf")
        
