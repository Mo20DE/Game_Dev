import pygame as pg
from framework.static import *
from entities.gamedata import GameData

from menues.mainmenu import MainMenu
from menues.settingsmenu import SettingsMenu
from menues.gamemenu import GameMenu
from menues.algomenu import AlgoMenu


class MenuesManager:

    def __init__(self):

        # important entities
        self.game_ent = GameData()
        
        self.mainM = MainMenu(self.game_ent)
        self.gameM = GameMenu(self.game_ent)
        self.algoM = AlgoMenu(self.game_ent)
        self.settM = SettingsMenu(self.mainM, self.gameM, self.algoM)
    
    def draw_menues(self, screen):
        
        # draw settings #
        if self.game_ent.game_states["settings"]:

            self.settM.draw(screen)
        
        # draw game menu
        elif self.game_ent.game_states["playing"]:

            self.gameM.draw(screen)

        # draw main menu
        else: self.mainM.draw(screen)

    def update_menues(self):

        mPos = pg.mouse.get_pos()

        # update settings #
        if self.game_ent.game_states["settings"]:

            self.settM.update(mPos)
        
        # update game menu
        elif self.game_ent.game_states["playing"]:
            
            self.gameM.update(mPos)
        
        # update main menu
        else: self.mainM.update(mPos)

    