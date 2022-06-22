from framework.utils import Main
from framework.static import width, height, caption, fps
from framework.helper import save_board_data, save_b_sc_and_settings

from menues.menuesmanager import MenuesManager

class Game(Main):

    def __init__(self):

        # call parent constructor
        super().__init__(width, height, caption, fps)
    
    def saveGameData(self):

        # save every board
        save_board_data(
            self.mm.game_ent.boards, 
            'data/board_data.json'
        )

        # save best scores and settings
        save_b_sc_and_settings(
            'data/score_and_settings_data.json',
             self.mm.game_ent.bestscores,
             self.mm.game_ent.sett_vars
        )

    def new(self):

        # create controller object
        self.mm = MenuesManager()
        
    def events(self):

        # save board if board state changed
        if self.mm.gameM.board_changed:
            self.saveGameData()

        # exit game (quit)
        self.handle_quit(self.saveGameData)
        
        # exit game (exit)
        if self.mm.game_ent.game_states["exit"]:
            self.saveGameData()
            self.run = False
    
    def update(self):
        
        # refresh display
        self.dp_update()
        # update the menues
        self.mm.update_menues()

    def draw(self):

        # draw menues onto screen
        self.mm.draw_menues(self.screen)


def main():
    app = Game()
    app.runGame()

if __name__ == "__main__":
    main()