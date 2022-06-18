import pygame as pg
from entities.gamedata import GameData
from framework.static import *

class AlgoMenu:

    def __init__(self, game_ent: GameData):

        # buffer which includes every important data
        self.game_ent = game_ent

        #self.menu_surf = algo_menu
        #self.menu_btns = algo_menu_buttons
        self.menu_status = "unfolded" # unfolded/collapsed

        self.states = {
            "unfolded_clicked": False,
            "collapsed_clicked": False
        }

    def draw_menu(self, screen):

        self.menu_surf[self.menu_status].blit_button(screen)

        if self.menu_status == "collapsed":
            # blit menu caption
            screen.blit(algo_menu["caption"], caption_pos)
            # blit menu buttons
            for btn in self.menu_btns.values():
                btn.blit_button(screen)
    
    def handleMenuClicked(self, mPos):

        # check click for collapsed and unfolded menu
        if (self.menu_surf["unfolded"].checkPreciseClick(mPos, (150, 302), (718, 750)) and not self.gm.states["restart"]):

            self.states["collapsed_clicked"] = True
        
        '''if self.states["collapsed_clicked"] and not self.menu_surf["unfolded"].checkPreciseClick(mPos, (150, 302), (718, 750)):
            self.states["collapsed_clicked"] = False'''
        
        if self.states["collapsed_clicked"] and self.menu_surf["unfolded"].checkPreciseReleaseClick(mPos, (150, 302), (718, 750)):
            self.menu_status = "collapsed"
            self.states["collapsed_clicked"] = False
        

        if self.menu_surf["collapsed"].checkPreciseClick(mPos, (150, 302), (350, 384)): #and not self.gm.states["restart"]

            self.states["unfolded_clicked"] = True
        
        '''if self.states["collapsed_clicked"] and not self.menu_surf["unfolded"].checkPreciseClick(mPos, (150, 302), (718, 750)):
            self.states["collapsed_clicked"] = False'''
        
        if self.states["unfolded_clicked"] and self.menu_surf["collapsed"].checkPreciseReleaseClick(mPos, (150, 302), (350, 384)):
            self.menu_status = "unfolded"
            self.states["unfolded_clicked"] = False
        
        '''if self.menu_surf["collapsed"].checkPreciseClick(mPos, (150, 302), (350, 384)):
            self.menu_status = "unfolded"'''
        
    def on_nn_btn_click(self):
        pass

    def on_exp_btn_click(self):
        pass

    def on_greedy_btn_click(self):
        pass

    def on_random_btn_click(self):
        pass

    def update_menu(self):

        mPos = pg.mouse.get_pos()
        # update game menu attribute
        self.gm.setAlgoMenuStatus(self.menu_status)

        # check click for collapsed and unfolded menu
        self.handleMenuClicked(mPos)
        
        # actions
        if self.menu_status == "collapsed":
            for btn in self.menu_btns.values():
                btn.checkClicked(mPos)