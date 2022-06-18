from framework.utils import *
from framework.static import *


# class to represent a board tile
class BoardTile:

    def __init__(self, size, pos, num, dim, image):
        
        self.size = size
        self.num = num
        self.pos = pos
        self.dim = dim

        self.tile_img = image
        self.tile_rect = self.tile_img.get_rect(topleft=self.pos)

        self.spawn_effect = True # flag for spawn effect
        self.size_cpy = [self.size[0]-30]*2
        self.spawn_off = 3
        self.tile_center = ((self.pos[0]+(tile_dim[self.dim]/2)), (self.pos[1]+(tile_dim[self.dim]/2)))
    
    def do_spawn_effect(self, screen):

        self.img_cpy = pg.transform.scale(self.tile_img, self.size_cpy)
        self.img_cpy_rect = self.img_cpy.get_rect()
        self.img_cpy_rect.center = self.tile_center

        screen.blit(self.img_cpy, self.img_cpy_rect)
        self.size_cpy[0] += self.spawn_off
        self.size_cpy[1] += self.spawn_off

        if (self.size[0]+5, self.size[1]+5) <= tuple(self.size_cpy):
            self.spawn_effect = False
    
    def reset_spawn_effect(self):
        self.spawn_effect = True
    
    def draw_tile(self, screen):

        if self.spawn_effect: self.do_spawn_effect(screen)
        else: screen.blit(self.tile_img, self.tile_rect)


# class which represents a move
class Move:

    def __init__(self, prevBoard, boardTiles, score, movesDone):
        
        self.board = prevBoard
        self.board_tiles = boardTiles
        self.score = score
        self.moves_done = movesDone


# surface class
class Surface:
    
    def __init__(self, size, pos, color):

        self.surf = pg.Surface(size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft=pos)

    def blit(self, screen, surf2=None):

        if isinstance(surf2, pg.Surface):
            self.surf.blit(surf2, self.rect)
        else: screen.blit(self.surf, self.rect)

