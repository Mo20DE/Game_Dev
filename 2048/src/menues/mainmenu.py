from framework.static import *
from framework.utils import *
from entities.gamedata import GameData

from entities.board import Board
from datetime import datetime


# Start Screen (Main Menu)
class MainMenu:

    def __init__(self, game_ent: GameData):

        # buffer which includes every important data
        self.game_ent = game_ent
        # load every needed variable
        self.load_menu_variables()
        
    def load_menu_variables(self):

        # get current game theme
        theme = self.game_ent.sett_vars["theme"]
        # surfaces
        self.menu_bg = game_assets[theme]["main_menu"]["surfaces"]["theme"]
        self.init_or_update_preview(theme)
        self.build_version = Text(8, made_by_pos[1], "Build v1.0", "Arial", 15, 
            moves_done_color[self.game_ent.sett_vars["theme"]], bold=True)

        # GUI elements
        self.menu_btns = {
            
            "start_btn": game_assets[theme]["main_menu"]["buttons"]["start_btn"],
            "sett_btn": game_assets[theme]["main_menu"]["buttons"]["sett_btn"],
            "exit_btn": game_assets[theme]["main_menu"]["buttons"]["exit_btn"],
            "left_btn": game_assets[theme]["main_menu"]["buttons"]["left_slide_btn"],
            "right_btn": game_assets[theme]["main_menu"]["buttons"]["right_slide_btn"],
            "made_by_btn": game_assets[theme]["main_menu"]["buttons"]["made_by_btn"]
        }
    
    def init_or_update_preview(self, theme):

        self.currentBoardPreview = game_assets[theme]["main_menu"]["surfaces"]["board_previews"][self.game_ent.mode]
        self.currentModeFont = game_assets[theme]["main_menu"]["surfaces"]["board_font"][self.game_ent.mode]
    
    def draw_current_datetime(self, screen):

        theme = self.game_ent.sett_vars["theme"]
        Text(date_time_pos[0], date_time_pos[1], datetime.now().strftime("%d.%m.%Y - %H:%M"), 
        "Arial", 22, moves_done_color[theme]).draw_text(screen)

    def onStartButtonClick(self, mPos):
        
        self.menu_btns["made_by_btn"].isBtnClickedOpenLink(mPos)
        if self.menu_btns["start_btn"].isBtnClicked(mPos):
            if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            # change game state
            self.game_ent.resetState("playing", True)
            quit_btn.setButtonPos(algo_quit_btn_pos)
            # make a fresh board
            if self.game_ent.mode not in self.game_ent.boards:
                self.game_ent.boards[self.game_ent.mode] = Board(3 + self.game_ent.modes[-1], self.game_ent.sett_vars["theme"])

    def onSlideButtonClick(self, mPos):

        # right slide button clicked
        if self.menu_btns["right_btn"].isBtnClicked(mPos):
            
            if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")

            self.game_ent.modes[-1] = (self.game_ent.modes[-1]+1)%3
            self.game_ent.mode = self.game_ent.modes[self.game_ent.modes[-1]]

            # change the board preview and text
            self.init_or_update_preview(self.game_ent.sett_vars["theme"])
        
        # left slide button clicked
        elif self.menu_btns["left_btn"].isBtnClicked(mPos):

            if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            
            if self.game_ent.modes[-1] == 0: self.game_ent.modes[-1] = 2
            else: self.game_ent.modes[-1] = self.game_ent.modes[-1]-1
            self.game_ent.mode = self.game_ent.modes[self.game_ent.modes[-1]]

            # change the board preview and text
            self.init_or_update_preview(self.game_ent.sett_vars["theme"])
    
    def onSettingsButtonClick(self, mPos):
        
        if self.menu_btns["sett_btn"].isBtnClicked(mPos):
            if self.game_ent.sett_vars["sound"]: make_click_sound("click_1")
            self.game_ent.resetState("settings", True)
            quit_btn.setButtonPos(quit_btn_pos)
    
    def onExitButtonClick(self, mPos):

        if self.menu_btns["exit_btn"].isBtnClicked(mPos):
            self.game_ent.resetState("exit", True)
        
    def draw(self, screen):

        # draw menu background
        screen.blit(self.menu_bg, bg_pos)
        # draw datetime
        self.draw_current_datetime(screen)
        # draw start screen
        screen.blit(self.currentBoardPreview, preview_pos) # board preview
        screen.blit(self.currentModeFont, mode_font_pos) # mode font
        self.build_version.draw_text(screen)

        self.menu_btns["start_btn"].blitButton(screen)
        self.menu_btns["left_btn"].blitButton(screen)
        self.menu_btns["right_btn"].blitButton(screen)
        self.menu_btns["sett_btn"].blitButton(screen)
        self.menu_btns["exit_btn"].blitButton(screen)
        self.menu_btns["made_by_btn"].blitButton(screen)
        
    def update(self, mPos):

        # update start screen
        self.onStartButtonClick(mPos)
        self.onSlideButtonClick(mPos)
        self.onSettingsButtonClick(mPos)
        self.onExitButtonClick(mPos)

