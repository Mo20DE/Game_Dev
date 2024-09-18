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
        self.ai_used = False

        if self.dim < 3 or self.dim > 5:
            raise ValueError("Invalid Board Dimension.")

        # matrix representation of board
        # initialize empty board
        self.board = np.zeros([self.dim]*2)
        self.board_dim = self.board.shape

        # every used tile on the board
        self.board_tiles = {}
        # meta information
        self.tile_positions = {}

        self.game_state = "playing"
        self.curr_move = None
        self.prevMove = Move()
        self.reset_o_undo = False

        self.can_do_move = True
        self.tiles_moving = False
        self.board_changed = False
        self.anim_move = True
        self.anim_spawn = True
        self.anim_spawn_buff = False
        self.tiles_merged = 0
        self.move_time = 0
        
        self.old_score = 0
        self.score_buff = [0, None]
        # load necessary board variables
        self.load_board_variables()
        # setup board
        self.init_board(gen_tiles)
    
    def load_board_variables(self, theme=None):

        # update game theme
        if theme is not None: self.theme = theme

        # choose board image and nitialize all tiles with the proper size
        self.board_img = game_assets[self.theme]["in_game"]["boards"][tile_info[self.dim][1]]
        self.board_rect = self.board_img.get_rect(topleft=board_pos)
        self.all_available_tiles = game_assets[self.theme]["in_game"]["tiles"][tile_info[self.dim][2]]

        if theme is not None:
            for tile in self.board_tiles.values():
                tile.tile_img = self.all_available_tiles[str(tile.num)]

    def init_board(self, gen_tiles):

        # set board tiles moving speed
        self.move_speed = tile_info[self.dim][0]

        # save every position of a tile (x, y)
        for i in range(self.dim):
            for j in range(self.dim):
                x_coord = board_pos[0]+((j+1)*gap_off[self.dim])+(j*tile_dim[self.dim]) - align_off[self.dim][j]
                y_coord = board_pos[1]+((i+1)*gap_off[self.dim])+(i*tile_dim[self.dim]) - align_off[self.dim][i]
                self.tile_positions[str(i)+str(j)] = [x_coord, y_coord]

        # create 2 random tiles
        if gen_tiles:
            self.generate_tile()
            self.generate_tile()
    
    def set_board_flags(self, ai_used=None, can_do_move=None, anim_spawn=None, anim_move=None):
        
        if ai_used is not None: self.ai_used = ai_used
        if can_do_move is not None: self.can_do_move = can_do_move
        if anim_spawn is not None: self.anim_spawn = anim_spawn
        if anim_move is not None: self.anim_move = anim_move

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
            spwn_eff=self.anim_spawn
        )
    
    def transform_matrix(self, move_dir, mat):

        if move_dir == "right": return mat[::, ::-1]
        elif move_dir == "up": return mat.T
        elif move_dir == "down": return mat.T[::, ::-1]
        else: return mat
    
    # algorithm to shift the board
    # matrix according to input
    def shift_matrix(self, mat, move_dir):

        merge_buffer = np.zeros(mat.shape)
        self.moveBuffer = []
        self.doneTiles = []
        self.tiles_merged = 0
        # flag to save tile positions
        tile_flag = True
        if self.score_buff[0] > 0: self.resetScoreBuffer()

        # transform matrix for processing
        mat = self.transform_matrix(move_dir, mat)
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
                        self.score_buff[0] += int(2*elem)
                        # save tiles to move
                        self.find_start_end_pos(move_dir, i, j, idx_offset, tile_flag)
                        if tile_flag: tile_flag = False

                # reset flag
                tile_flag = True
        # retransform matrix
        mat = self.transform_matrix(move_dir, mat)
        
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
            make_click_sound("swipe")
        elif self.tiles_merged == 1:
            make_click_sound("merge_1")
        elif self.tiles_merged == 2:
            make_click_sound("merge_2")
        else:
            make_click_sound("merge_3")
    
    def get_free_fields(self):

        # get all empty fields on board
        return [[i, j] for i in range(self.dim) for j in range(self.dim) if self.board[i, j] == 0]
    
    def isMoveDone(self):
        return True if len(self.moveBuffer) == 0 else False
    
    def canMove(self, prevBoard):
        return False if np.allclose(prevBoard, self.board) else True

    # check if the game is over
    def isLost(self):

        if len(self.get_free_fields()) > 0: return False

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
    
    def resetScoreBuffer(self):
        self.score_buff = [0, None]

    def get_events(self):

        curr_time = pg.time.get_ticks()
        if self.can_do_move and curr_time - self.move_time > 250:

            if not self.anim_spawn and not self.anim_move:
                self.set_board_flags(anim_spawn=True, anim_move=True)

            keys = pg.key.get_pressed()
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.curr_move = "up"

            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.curr_move = "down"

            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                self.curr_move = "left"

            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.curr_move = "right"
            
        if self.curr_move is not None: 
            self.move_time = pg.time.get_ticks()
            self.tiles_moving = True
    
    def copyBoardTiles(self):

        board_tiles = {}
        for idx, tile in zip(self.board_tiles.keys(), self.board_tiles.values()):
            board_tiles[idx] = BoardTile(tile.size, tile.pos, 
                tile.num, tile.dim, tile.tile_img)
        return board_tiles

    def restart(self):

        # reset score
        self.old_score = self.score
        self.score = 0
        self.moves_done = 0
        # clear board
        self.board = np.zeros(self.board_dim)
        self.board_tiles = {}

        self.game_state = "playing"
        self.can_do_move = True
        self.tiles_moving = False
        self.curr_move = None
        self.board_changed = True
        self.reset_o_undo = True
        self.prevMove.init_move()

        # buffer for every move
        self.moveBuffer = []
        self.doneTiles = []

        # get two random tiles
        self.generate_tile()
        self.generate_tile()
    
    def undoMove(self):

        if self.prevMove.board is not None:
            self.board = self.prevMove.board
            self.board_tiles = self.prevMove.board_tiles
            self.score = self.prevMove.score
            self.prevMove.init_move()
            self.moves_done -= 1

            self.moveBuffer = []
            self.doneTiles = []

            self.game_state = "playing"
            self.can_do_move = True
            self.tiles_moving = False
            self.curr_move = None
            self.board_changed = True
            self.reset_o_undo = True

    def draw(self, screen):
        
        # draw board
        screen.blit(self.board_img, self.board_rect)
        # draw every board tile
        for tile in self.board_tiles.values():
            tile.draw_tile(screen)

    def update(self):

        # check if game is over
        if self.isLost():
            self.game_state = "lost"
            self.old_score = self.score
        
        if not self.tiles_moving:
            # get every event
            self.get_events()
            # is there a move to make
            if self.curr_move != None:
                prevBoard = self.board.copy()
                # shift board matrix
                self.shift_matrix(self.board, self.curr_move)
                # check whether the move changed the board
                if not self.canMove(prevBoard):
                    # reset tile movement
                    self.can_do_move = True
                    self.curr_move = None
                    self.tiles_moving = False
                else:
                    self.score_buff[1] = Text(220, 66, "+"+str(self.score_buff[0]), 
                        "Arial", 28, moves_done_color[self.theme], bold=True, alpha_val=255)
                    # save previous move
                    self.prevMove.board = prevBoard
                    self.prevMove.board_tiles = self.copyBoardTiles()
                    self.prevMove.score = self.score
        else:
            # do move operation
            self.animate_move(self.curr_move)
            # check whether move is done
            if self.isMoveDone():
                #generate a new tile
                self.generate_tile()
                self.moves_done += 1

                self.tiles_moving = False
                self.curr_move = None
                self.board_changed = True

