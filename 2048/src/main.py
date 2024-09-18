import pygame as pg
from framework.utils import Main
from framework.static import width, height, caption, fps
from framework.helper import save_board_data, save_game_data, save_stats

from entities.gamedata import GameData
from menues.mainmenu import MainMenu
from menues.settingsmenu import SettingsMenu
from menues.gamemenu import GameMenu


class Game(Main):

    def __init__(self):

        # call parent constructor
        super().__init__(width, height, caption, fps)
    
    def saveGameData(self):

        # save every board
        save_board_data(
            self.game_ent.boards, 
            'data/board_data.json'
        )

        # save best scores and settings
        save_game_data(
            'data/game_data.json',
             self.game_ent.bestscores,
             self.game_ent.board_timers,
             self.game_ent.next_goal_tiles,
             self.game_ent.sett_vars
        )

        # save statistics
        save_stats('data/statistics.json', self.game_ent.stats)

        # reset board flag
        self.game_ent.boards[self.game_ent.mode].board_changed = False

    def new(self):

        # main entities
        self.game_ent = GameData()
        self.mainM = MainMenu(self.game_ent)
        self.gameM = GameMenu(self.game_ent)
        self.settM = SettingsMenu(self.mainM, self.gameM)
        
    def events(self):

        # save board if board state changed
        if self.gameM.board_changed:
            self.saveGameData()

        # exit game (quit)
        self.handle_quit(
            # save game data
            self.saveGameData,
            # page scrolling in settings
            self.settM.stats.handlePageScrolling
        )
        
        # exit game (exit)
        if self.game_ent.game_states["exit"]:
            self.saveGameData()
            self.run = False
    
    def update(self):
        
        # refresh display
        self.dp_update()
        # update the menues
        mPos = pg.mouse.get_pos()

        # update settings #
        if self.game_ent.game_states["settings"]:
            self.settM.update(mPos)
        
        # update game menu
        elif self.game_ent.game_states["playing"]:
            self.gameM.update(mPos)
            self.settM.stats.checkAndUpdateStats()

        # update main menu
        else: self.mainM.update(mPos)

    def draw(self):

        # draw menues onto screen
        if self.game_ent.game_states["settings"]:
            self.settM.draw(self.screen)
        
        # draw game menu
        elif self.game_ent.game_states["playing"]:
            self.gameM.draw(self.screen)

        # draw main menu
        else: self.mainM.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.runMain()

