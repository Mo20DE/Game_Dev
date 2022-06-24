from framework.utils import *
from framework.static import *
from entities.entities import BoardTile, Move

import numpy as np
import random


# class that represents an nxn board
class Board:

    def __init__(self, dim, theme, gen_tiles=True):

        self.dim = dim
        self.theme = theme
        self.score = 0
        self.moves_done = 0

        if self.dim < 3 or self.dim > 5:
            raise ValueError("Invalid Board Dimension")

        # matrix representation of board
        # initialize empty board
        self.board = np.zeros((self.dim, self.dim))
        self.prev_board = None
        self.board_dim = self.board.shape

        self.board_tiles = {} # every used tile on the board
        self.prev_board_tiles = {}
        # meta information
        self.tile_positions = {}

        # buffer for every move
        self.moveBuffer = []
        self.doneTiles = []

        self.game_state = "playing"
        self.curr_move = None
        self.prevMove = []

        self.keyPressed = False
        self.tiles_moving = False

        self.board_changed = False
        self.key_lock = False
        self.anim_move = True

        # load necessary board variables
        self.load_board_variables()
        # setup board
        self.init_board(gen_tiles)
    
    def load_board_variables(self, theme=None):

        # update game theme
        if theme is not None: self.theme = theme

        # choose board image and nitialize all tiles with the proper size
        self.board_img = game_assets[self.theme]["in_game"]["boards"][tile_info[self.dim][1]]
        self.all_available_tiles = game_assets[self.theme]["in_game"]["tiles"][tile_info[self.dim][2]]
        # make an rect of the board image
        self.board_rect = self.board_img.get_rect(topleft=board_pos)

        if theme is not None:
            for tile in self.board_tiles.values():
                tile.tile_img = self.all_available_tiles[str(tile.num)]

    def init_board(self, gen_tiles):

        # set board tiles moving speed
        self.move_speed = tile_info[self.dim][0]

        # save every positions of a field (every x,y cordinate)
        # exp.: index = [2, 1] self.tile_positions["tile_positions"][str(index[0]+str(index[1]))]
        for i in range(self.dim):
            for j in range(self.dim):
                x_coord = board_pos[0]+((j+1)*gap_off[self.dim])+(j*tile_dim[self.dim]) - align_off[self.dim]["x"][j]
                y_coord = board_pos[1]+((i+1)*gap_off[self.dim])+(i*tile_dim[self.dim]) - align_off[self.dim]["y"][i]
                self.tile_positions[str(i)+str(j)] = [x_coord, y_coord]
        
        # save border of the board
        #self.tile_positions["border"]["left"] = self.tile_positions["tile_positions"]["00"][0]
        #self.tile_positions["border"]["right"] = self.tile_positions["tile_positions"]["0"+str(self.dim-1)][0]+tile_dim[self.dim] #self.board_rect.right - gap_off[self.dim]
        #self.tile_positions["border"]["top"] = self.tile_positions["tile_positions"]["00"][1] #self.board_rect.top + gap_off[self.dim]
        #self.tile_positions["border"]["bottom"] = self.tile_positions["tile_positions"]["0"+str(self.dim-1)][1] #self.board_rect.bottom - gap_off[self.dim]

        # create 2 random tiles
        if gen_tiles:
            self.generate_tile()
            self.generate_tile()

    def generate_tile(self):
        
        emp_fields = self.get_free_fields()
        # choose an empty field for a tile
        new_tile_pos = random.choice(emp_fields)
        # get a random tile
        np.random.shuffle(urn)
        # get a random tile
        tile_num = random.choice(urn)
        # add new tile position to the matrix
        self.board[new_tile_pos[0], new_tile_pos[1]] = tile_num
        # create a new board tile
        tile_idx = str(new_tile_pos[0])+str(new_tile_pos[1])
        # add new board tile
        self.add_board_tile(tile_idx, tile_num)
        
        print(self.board)
    
    def add_board_tile(self, idx, tile_num):

        self.board_tiles[idx] = BoardTile(
                (tile_dim[self.dim], 
                tile_dim[self.dim]), 
                self.tile_positions[idx], 
                tile_num, self.dim,
                self.all_available_tiles[str(tile_num)],
                spwn_eff=self.anim_move
        )
    
    # algorithm to shift the board
    # matrix according to input
    def shift_matrix(self, mat, move_dir):

        # merge buffer
        merge_buffer = np.zeros(mat.shape)
        # move buffer information
        self.moveBuffer = []
        # flag to save tile positions
        tile_flag = True

        self.tiles_merged = 0
        # save prevous board
        self.prev_board = self.board.copy()
        self.prev_board_tiles = self.board_tiles.copy()

        # transform matrix for processing
        if move_dir == "right":
            mat = mat[::, ::-1]

        elif move_dir == "up":
            mat = mat.T

        elif move_dir == "down":
            mat = mat.T[::, ::-1]
        
        # go through every entry of the board
        for i, row in enumerate(mat):
            for j, elem in enumerate(row):

                if j == 0: continue
                idx_offset = 1
                for _ in range(j):

                    # non-zero element
                    if elem == 0: break
                    # zero and non-zero element
                    offset = j - idx_offset
                    if (mat[i, offset] == 0 and 
                        merge_buffer[i, offset] != 1):

                        mat[i, offset] = elem
                        mat[i, offset+1] = 0
                        idx_offset += 1
                        # save tiles to move
                        self.find_start_end_pos(move_dir, i, j, idx_offset, tile_flag)
                        if tile_flag: tile_flag = False

                    # two non-zero elements
                    elif (elem == mat[i, offset] and 
                        merge_buffer[i, offset] != 1):

                        merge_buffer[i, offset] = 1
                        mat[i, offset] = 2*elem
                        mat[i, offset+1] = 0
                        idx_offset += 1
                        self.tiles_merged += 1
                        # save tiles to move
                        self.find_start_end_pos(move_dir, i, j, idx_offset, tile_flag)
                        if tile_flag: tile_flag = False

                # reset flag
                tile_flag = True

        # retransform matrix
        if move_dir == "right":
            mat = mat[::, ::-1]

        elif move_dir == "up":
            mat = mat.T

        elif move_dir == "down":
            mat = mat.T[::, ::-1]
        
    def find_start_end_pos(self, move_dir, i, j, idx_off, flag):

        if move_dir == "left":

            # left move - all dimensons same
            if flag: self.moveBuffer.append([(i, j), 0]) # start
            self.moveBuffer[-1][1] = (i, j-idx_off+1) # end

        elif move_dir == "right":

            if self.dim == 3:
                if flag: self.moveBuffer.append([(i, idx_off-j), 0]) # start
                self.moveBuffer[-1][1] = (i, idx_off-j+1) # end

            elif self.dim == 4:
                if flag: self.moveBuffer.append([(i, idx_off-j+1), 0]) # start
                self.moveBuffer[-1][1] = (i, idx_off-j+2) # end

            elif self.dim == 5:
                if flag: self.moveBuffer.append([(i, idx_off-j+2), 0]) # start
                self.moveBuffer[-1][1] = (i, idx_off-j+3) # end

        elif move_dir == "up":

            # up move - all dimensons same
            if flag: self.moveBuffer.append([(j, i), 0]) # start
            self.moveBuffer[-1][1] = (j-idx_off+1, i) # end

        elif move_dir == "down":

            if self.dim == 3:
                if flag: self.moveBuffer.append([(idx_off-j, i), 0]) # start
                self.moveBuffer[-1][1] = (idx_off-j+1, i) # end

            elif self.dim == 4:
                if flag: self.moveBuffer.append([(idx_off-j+1, i), 0]) # start
                self.moveBuffer[-1][1] = (idx_off-j+2, i) # end

            elif self.dim == 5:
                if flag: self.moveBuffer.append([(idx_off-j+2, i), 0]) # start
                self.moveBuffer[-1][1] = (idx_off-j+3, i) # end

    def animate_move(self, move_dir):

        for i, pos in enumerate(self.moveBuffer):

            tile_idx = str(pos[0][0])+str(pos[0][1])
            dest_pos = str(pos[1][0])+str(pos[1][1])

            
            if move_dir == "up" and tile_idx in self.board_tiles:

                if not self.anim_move or not self.board_tiles[tile_idx].tile_rect.y - self.move_speed > self.tile_positions[dest_pos][1]:
                    self.board_tiles[tile_idx].tile_rect.y = self.tile_positions[dest_pos][1]
                    self.doneTiles.append((i, tile_idx, dest_pos))
                else:
                    self.board_tiles[tile_idx].tile_rect.y -= self.move_speed
                
            elif move_dir == "down" and tile_idx in self.board_tiles:

                if not self.anim_move or not self.board_tiles[tile_idx].tile_rect.y + self.move_speed < self.tile_positions[dest_pos][1]:
                    self.board_tiles[tile_idx].tile_rect.y = self.tile_positions[dest_pos][1]
                    self.doneTiles.append((i, tile_idx, dest_pos))
                else:
                    self.board_tiles[tile_idx].tile_rect.y += self.move_speed
            
            elif move_dir == "left" and tile_idx in self.board_tiles:

                if not self.anim_move or not self.board_tiles[tile_idx].tile_rect.x > self.tile_positions[dest_pos][0] + self.move_speed:
                    self.board_tiles[tile_idx].tile_rect.x = self.tile_positions[dest_pos][0]
                    self.doneTiles.append((i, tile_idx, dest_pos))
                else:
                    self.board_tiles[tile_idx].tile_rect.x -= self.move_speed
            
            elif move_dir == "right" and tile_idx in self.board_tiles:

                if not self.anim_move or not self.board_tiles[tile_idx].tile_rect.x < self.tile_positions[dest_pos][0] - self.move_speed:
                    self.board_tiles[tile_idx].tile_rect.x = self.tile_positions[dest_pos][0]
                    self.doneTiles.append((i, tile_idx, dest_pos))
                else:
                    self.board_tiles[tile_idx].tile_rect.x += self.move_speed
                
        # update board information        
        self.update_tiles()
    
    def update_tiles(self):
        
        idx_off = 0
        for elem in self.doneTiles:

            i, tile_idx, dest_pos = elem[0], elem[1], elem[2]
            # case 1 - destination of tile is empty
            if dest_pos not in self.board_tiles:

                self.board_tiles[dest_pos] = self.board_tiles[tile_idx]
                del self.board_tiles[tile_idx]
                self.board_tiles[dest_pos].pos = self.tile_positions[dest_pos]
                self.moveBuffer.pop(i-idx_off); idx_off += 1

            # case 2 - destination of tile is not empty
            else:
                # case 2.1 - destination tile doesn't move (merge)
                self.board_tiles[tile_idx].pos = self.tile_positions[dest_pos]
                self.board_tiles[tile_idx].num *= 2
                self.board_tiles[tile_idx].tile_img = self.all_available_tiles[str(self.board_tiles[tile_idx].num)]
                self.board_tiles[dest_pos] = self.board_tiles[tile_idx]
                del self.board_tiles[tile_idx]
                self.moveBuffer.pop(i-idx_off); idx_off += 1
                self.score += self.board_tiles[dest_pos].num
        
        self.doneTiles = []
    
    def make_tile_sound(self):
        
        if self.tiles_merged == 0:
            sound_effects["swipe"].play()
        elif self.tiles_merged == 1:
            sound_effects["merge_1"].play()
        elif self.tiles_merged == 2:
            sound_effects["merge_2"].play()
        else:
            sound_effects["merge_3"].play()

    def key_pressed(self, keys):

        for key in keys:
            if key: return True
        return False
    
    def get_free_fields(self):
        # get all empty fields on board
        return [[i, j] for i in range(self.dim) for j in range(self.dim) if self.board[i, j] == 0]
    
    def isMoveDone(self):
        return True if len(self.moveBuffer) == 0 else False
    
    def canMove(self):
        return False if np.allclose(self.prev_board, self.board) else True

    # check if the game is over
    def isLost(self, free_fields):

        if len(free_fields) > 0: return False

        mat_T = self.board.T
        range_x = self.board_dim[0]-1

        # check horizontally and vertically
        for i in range(range_x+1):
            for j in range(range_x):
                if self.board[i, j] != 0 or mat_T[i, j] != 0:
                    if (self.board[i, j] == self.board[i, j+1] 
                        or mat_T[i, j] == mat_T[i, j+1]):
                        return False
        return True
    
    def get_events(self):

        if not self.key_lock:

            keys = pg.key.get_pressed()
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.curr_move = "up"

            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.curr_move = "down"

            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                self.curr_move = "left"

            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.curr_move = "right"
            
        if self.curr_move != None:
            self.keyPressed = True
            self.tiles_moving = True
    
    def doMove(self):
        # move up or down or left or right
        self.animate_move(self.curr_move)

    def undoMove(self):

        if self.prevMove is not None:

            self.board = self.prevMove.board
            self.board_tiles = self.prevMove.board_tiles
            self.score = self.prevMove.score
            self.moves_done = self.prevMove.moves_done

            self.prev_board_tiles = {}
            self.moveBuffer = []
            self.doneTiles = []

            self.game_state = "playing"
            self.keyPressed = False
            self.tiles_moving = False
            self.prev_board = None
            self.curr_move = None
            self.prevMove = None

            self.board_changed = True
    
    def restart(self):

        # reset score
        self.score = 0
        self.moves_done = 0

        # clear board
        self.board = np.zeros(self.board_dim)
        self.prev_board = None
        self.board_tiles = {}
        self.prev_board_tiles = {}

        self.game_state = "playing"
        self.keyPressed = False
        self.tiles_moving = False
        self.curr_move = None
        self.prevMove = None

        # buffer for every move
        self.moveBuffer = []
        self.doneTiles = []

        # get two random tiles
        self.generate_tile()
        self.generate_tile()

    def draw(self, screen):
        
        # draw board
        screen.blit(self.board_img, self.board_rect)

        # draw every board tile
        for tile in self.board_tiles.values():
            tile.draw_tile(screen)

    def update(self):
        
        # reset flag
        if self.board_changed: self.board_changed = False

        # check if game is over
        if self.isLost(self.get_free_fields()):
            self.game_state = "lost"

        if self.keyPressed:
            keys = pg.key.get_pressed()
            if self.key_pressed(keys):
                self.keyPressed = True
            else: self.keyPressed = False

        if not self.keyPressed and not self.tiles_moving:

            self.get_events() # get every event
            # is there a move to make
            if self.curr_move != None:
                # shift board matrix
                self.shift_matrix(self.board, self.curr_move)
                # check whether the move changed the board
                if not self.canMove():
                    # reset tile movement
                    self.tiles_moving = False
                    self.curr_move = None
                else:
                    # save previous move
                    self.prevMove = Move(
                        self.prev_board, self.prev_board_tiles, 
                        self.score, self.moves_done
                    )
                # reset key pressed
                self.keyPressed = False

        elif not self.keyPressed and self.tiles_moving:

            # shift tiles on screen
            self.doMove()
            # check whether move is done
            if self.isMoveDone():

                #generate a new tile
                self.generate_tile()
                self.moves_done += 1

                keys = pg.key.get_pressed()
                if self.key_pressed(keys):
                    self.keyPressed = True
                else: self.keyPressed = False

                self.tiles_moving = False
                self.curr_move = None
                self.board_changed = True
        
