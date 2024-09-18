from framework.helper import load_board_data, load_game_data, load_stats


class GameData:

    def __init__(self):

        # every game state
        self.game_states = {
            "playing": False,
            "settings": False,
            "exit": False
        }

        # load best score, board timers and settings variables
        self.bestscores, self.board_timers, self.next_goal_tiles, self.sett_vars = load_game_data('data/game_data.json')
        # load every board
        self.boards = load_board_data('data/board_data.json', self.sett_vars["theme"])
        # load game statistics
        self.stats = load_stats('data/statistics.json')

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
            if del_board: 
                del self.boards[mode]
                self.board_timers[mode] = "0:00"
                self.next_goal_tiles[mode] = "2048"
            self.bestscores[mode] = 0
        else:
            if del_board: 
                self.boards.clear()
                self.board_timers = {"3x3": "0:00", "4x4": "0:00", "5x5": "0:00"}
                self.next_goal_tiles = {"3x3": "2048", "4x4": "2048", "5x5": "2048"}
            self.bestscores = {"3x3": 0, "4x4": 0, "5x5": 0}
    
    def resetState(self, state, _bool=False):
        # reset specfic state
        self.game_states[state] = _bool
    
