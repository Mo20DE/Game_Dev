from framework.helper import load_board_data, load_b_sc_and_settings


class GameData:

    def __init__(self):

        # every game state
        self.game_states = {
            "playing": False,
            "settings": False,
            "exit": False
        }

        # load best score and settings variables
        self.bestscores, self.sett_vars = load_b_sc_and_settings('data/score_and_settings_data.json')
        # load every board
        self.boards = load_board_data('data/board_data.json', self.sett_vars["theme"])

        self.mode = "4x4" # default mode
        self.modes = ["3x3", "4x4", "5x5", 1] # every mode and mode index
    
    def changeValue(self, key):

        if key == "theme":

            if self.sett_vars[key] == "light_theme":
                self.sett_vars[key] = "dark_theme"
            else: self.sett_vars[key] = "light_theme"

        else:
            if self.sett_vars[key]: self.sett_vars[key] = False
            else: self.sett_vars[key] = True
    
    def getButtonStatus(self, key):

        if key == "theme":

            if self.sett_vars[key] == "light_theme": status = "on"
            else: status = "off"
            
        else:
            if self.sett_vars[key]: status = "on"
            else: status = "off"
        
        return status

    def resetData(self, mode, del_board):
        
        if mode != "all":
            if del_board: del self.boards[mode]
            self.bestscores[mode] = 0
        else:
            if del_board: self.boards.clear()
            self.bestscores = {"3x3": 0, "4x4": 0, "5x5": 0}
    
    def resetState(self, state, _bool=False):
        # reset specfic state
        self.game_states[state] = _bool
    
