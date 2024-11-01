from framework.utils import *
from entities.entities import BoardTile
from entities.board import Board
from framework.static import width
import json, sys

# helper functions for loading 
# and storing game data

def load_board_data(path_name, theme):

    all_boards = {}
    # if file already exists
    if fileExists(path_name):
        try:
            # open file
            with open(path_name, 'r') as inp:
                file_content = json.load(inp)
                if isinstance(file_content, list) and file_content:
                    for board in file_content:
                        # make new board
                        new_board = Board(board["dim"], theme, gen_tiles=False)
                        # modify board
                        new_board.score = board["score"]
                        new_board.moves_done = board["moves_done"]
                        new_board.ai_used = board["ai_used"]
                        new_board.game_state = board["game_state"]
                        new_board.board = np.array(board["np_board"], dtype=int)
                        # new_board.board = np.array([
                        #     [16, 128, 256, 512],
                        #     [8, 64, 128, 256],
                        #     [4, 16, 32, 128],
                        #     [0, 2, 4, 8]
                        # ])
                        print("TEST")
                        # add board tiles
                        new_board.board_tiles = {
                            tile_idx: BoardTile(
                                b_data["size"],
                                b_data["pos"],
                                b_data["num"],
                                b_data["dim"],
                                new_board.all_available_tiles[str(b_data["num"])],
                            )
                            for tile_idx, b_data in zip(board["board_tiles"].keys(), board["board_tiles"].values())
                        }
                        # save board in list
                        all_boards[board["mode"]] = new_board
                # close file
                inp.close()

        except Exception as excp:
            print("JSON-error occured: loading board-data!")
            raise excp

    return all_boards

def save_board_data(object, path_name):
    
    game_data = []
    try:
        with open(path_name, 'w') as outp:
            for key, board in zip(object.keys(), object.values()):

                if board.tiles_moving:
                    board_ = board.prevMove.board.tolist()
                    board_tiles_ = board.prevMove.board_tiles
                else:
                    board_ = board.board.tolist()
                    board_tiles_ = board.board_tiles

                board_info = {
                    "mode": key,
                    "dim": board.dim,
                    "score": board.score,
                    "moves_done": board.moves_done,
                    "ai_used": board.ai_used,
                    "game_state": board.game_state,
                    "np_board": board_,
                    "board_tiles": {
                        tile_idx: {
                            "num": tile.num, 
                            "dim": tile.dim,
                            "size": tile.size, 
                            "pos": tile.pos,  
                        } 
                        for tile_idx, tile in zip(board_tiles_.keys(), board_tiles_.values())
                    }
                }
                game_data.append(board_info)

            json.dump(game_data, outp, indent=2)
        # close file
        outp.close()

    except Exception as excp:
        print("JSON-error occured: saving board-data!")
        raise excp

def load_game_data(path_name):

    # default best score
    best_scores = {
        "3x3": 0, 
        "4x4": 0, 
        "5x5": 0
    }
    # default board timers
    board_timers = {
        "3x3": "0:00", 
        "4x4": "0:00", 
        "5x5": "0:00"
    }
    # default next goal tiles
    next_goal_tiles = {
        "3x3": "2048",
        "4x4": "2048",
        "5x5": "2048"
    }
    # default settings
    sett_vars = {
        "sound": True,
        "show_undo": True,
        "show_ai_menu": True,
        "how_to": True,
        "theme": "dark_theme"
    }

    if fileExists(path_name):
        try:
            # open file
            with open(path_name, "r") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    if (isinstance(data[0], dict) and isinstance(data[1], dict) and 
                        isinstance(data[2], dict) and isinstance(data[3], dict)):
                        best_scores = data[0]
                        board_timers = data[1]
                        next_goal_tiles = data[2]
                        sett_vars = data[3]
            # close file
            f.close()
        
        except Exception as excp:
            print("JSON-error occured: loading bestscores and settings!")
            raise excp
    
    return best_scores, board_timers, next_goal_tiles, sett_vars

def save_game_data(path_name, best_scores, board_timers, next_goal_tiles, settings):

    try:
        save_data = []
        # open file
        file = open(path_name, "w")
        save_data.append(best_scores)
        save_data.append(board_timers)
        save_data.append(next_goal_tiles)
        save_data.append(settings)
        json.dump(save_data, file, indent=2)
        # close file
        file.close()
    
    except Exception as excp:
        print("JSON-error occured: saving bestscores and settings!")
        raise excp


def load_stats(path_name=None):

    # default stats
    stats = [[width, 550], {}]
    for i in range(3):
        y_off, mode = i*180, f"{3+i}x{3+i}"
        stats[1][mode] = {
            f"All Play - {mode}": {"x": 40, "y": 20+y_off, "font": "Arial", "f_size": 22, "bold": True}, # x, y, font, font size, bold
            "Best Score": {"score": 0, "x": 40, "y": 60+y_off, "font": "Arial", "f_size": 22, "bold": False}, # x, y, font, font size, bold
            "Total Score": {"score": 0, "x": 40, "y": 100+y_off, "font": "Arial", "f_size": 22, "bold": False}, # x, y, font, font size, bold
            "Top Tile": {"score": 0, "x": 40, "y": 140+y_off, "font": "Arial", "f_size": 22, "bold": False}, # x, y, font, font size, bold
        }
        
    if path_name is not None:
        if fileExists(path_name):
            try:
                # open file
                with open(path_name, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        stats = data
            except Exception as excp:
                print("JSON-error occured: loading game statistics!")
                raise excp

    return stats

def save_stats(path_name, stats):
    
    try:
        # open file
        file = open(path_name, "w")
        json.dump(stats, file, indent=2)
        # close file
        file.close()
    
    except Exception as excp:
        print("JSON-error occured: saving game statistics!")
        raise excp




## helper functions for custom algorithm integration ##

import logging
logging.basicConfig()
# optionally, set the qt api to use (in ['pyqt4', 'pyqt5', 'pyside'])
# import os; os.environ['QT_API'] = 'pyside'
import sys
from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class CodeEditor:

    def __init__(self):

        self.app = QtWidgets.QApplication(sys.argv)

        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Python Code Editor")
        self.window.setFixedWidth(800)
        self.window.setFixedHeight(600)

        self.editor = PyCodeEdit(server_script=server.__file__, color_scheme='darcula')
        self.editor.zoom_in(4)
        self.editor.file.open('/Users/mzm/Desktop/github/Game_Dev/2048/src/entities/custom_algo.py')

        self.window.setCentralWidget(self.editor)

        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self.editor)
        self.shortcut.activated.connect(self.save_code)

        self.code = self.editor.toPlainText()
        print(self.code)
    
    def save_code(self):

        self.code = self.editor.toPlainText()
        print(self.code)

        f = open("src/entities/custom_algo.py", "a")
        f.truncate(0)
        
        f.write(self.code)
        f.close()
    
    def run_code_editor(self):

        self.window.show()
        self.app.exec_()
        
