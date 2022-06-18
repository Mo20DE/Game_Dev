from framework.utils import Main
from framework.static import width, height, caption, fps
from framework.helper import save_board_data, save_b_sc_and_settings

from menues.menuesmanager import MenuesManager

import pygame as pg; import sys

class Game(Main):

    def __init__(self):

        # call parent constructor
        super().__init__(width, height, caption, fps)
    
    def saveGameData(self, quit=True):

        '''for board in self.mm.game_ent.boards.values():
            if board.tiles_moving:
                board.board = board.prev_board.copy()
                board.board_tiles = board.prev_board_tiles.copy()
                print(board.board)
                print(board.board_tiles)'''

        # save every board
        save_board_data(self.mm.game_ent.boards, 'data/board_data.json')
        save_b_sc_and_settings(
            'data/score_and_settings_data.json',
             self.mm.game_ent.bestscores,
             self.mm.game_ent.sett_vars
        )
        # quit game correctly
        if quit:
            self.run = False
            self.ended = True
            sys.exit()
    
    def new(self):

        # create controller object
        self.mm = MenuesManager()

    def draw(self):

        # draw menues onto screen
        self.mm.draw_menues(self.screen)

    def update(self):
        
        # refresh display
        self.dp_update()
        # update the menues
        self.mm.update_menues()
        
    def events(self):
        
        # exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.saveGameData()
        
        if self.mm.game_ent.game_states["exit"]:
            self.saveGameData()
        
        if self.mm.gameM.board_changed:
            self.saveGameData(quit=False)


def main():
    app = Game()
    app.runMain()

if __name__ == "__main__":
    main()