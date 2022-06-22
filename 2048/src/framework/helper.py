from framework.utils import *
from entities.entities import BoardTile
from entities.board import Board
import json

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
                        new_board.game_state = board["game_state"]
                        new_board.board = np.array(board["np_board"], dtype=int)
                        # add board tiles
                        new_board.board_tiles = {
                            tile_idx: BoardTile(
                                b_data["size"],
                                b_data["pos"],
                                b_data["num"],
                                b_data["dim"],
                                new_board.all_available_tiles[b_data["tile_idx"]],
                            )
                            for tile_idx, b_data in zip(board["board_tiles"].keys(), board["board_tiles"].values())
                        }

                        # save previous board and tiles
                        #new_board.prev_board = new_board.board
                        #new_board.prev_board_tiles = new_board.board_tiles
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
                    board_ = board.prev_board.tolist()
                    board_tiles_ = board.prev_board_tiles
                    print(board_)
                    print(board_tiles_)
                    print("tiles moving")
                    for tile in board_tiles_.keys():
                        print(tile)
                
                else:
                    board_ = board.board.tolist()
                    board_tiles_ = board.board_tiles

                board_info = {
                    "mode": key,
                    "dim": board.dim,
                    "score": board.score,
                    "moves_done": board.moves_done,
                    "game_state": board.game_state,
                    "np_board": board_,
                    "board_tiles": {
                        tile_idx: {
                            "size": tile.size, 
                            "pos": tile.pos, 
                            "num": tile.num, 
                            "dim": tile.dim, 
                            "tile_idx": str(tile.num)
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

def load_b_sc_and_settings(path_name):

    # default best score
    best_scores = {
        "3x3": 0, 
        "4x4": 0, 
        "5x5": 0
    }
    # default settings
    sett_vars = {
        "sound": True,
        "show_undo": True,
        "show_ai_menu": False,
        "how_to": True,
        "theme": "light_theme"
    }

    if fileExists(path_name):
        try:
            # open file
            with open(path_name, "r") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                if isinstance(data[0], dict) and isinstance(data[1], dict):
                    best_scores = data[0]
                    sett_vars = data[1]
            # close file
            f.close()
        
        except Exception as excp:
            print("JSON-rror occured: loading bestscores and settings!")
            raise excp
    
    return best_scores, sett_vars

def save_b_sc_and_settings(path_name, best_scores, settings):

    try:
        save_data = []
        # open file
        file = open(path_name, "w")
        save_data.append(best_scores)
        save_data.append(settings)
        json.dump(save_data, file, indent=2)
        # close file
        file.close()
    
    except Exception as excp:
        print("JSON-error occured: saving bestscores and settings!")
        raise excp

