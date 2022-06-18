import pygame as pg
from entities import *
from settings import *


# player class
class Player(pg.sprite.Sprite):

    # sprite for the player
    def __init__(self, pos, keys, keys2=False):

        pg.sprite.Sprite.__init__(self)
        self.init_pos = pos
        self.keys = keys
        self.sec_keys = keys2

        if self.keys == ['w', 's'] or self.keys == ['W', 'S']:
            self.keys[0] = pg.K_w 
            self.keys[1] = pg.K_s

            if self.sec_keys:
                self.keys2 = [None, None]
                self.keys2[0] = pg.K_UP
                self.keys2[1] = pg.K_DOWN

        elif self.keys == ['up', 'down'] or self.keys == ['UP', 'DOWN']:
            self.keys[0] = pg.K_UP 
            self.keys[1] = pg.K_DOWN
        
        else: raise ValueError('Invalid keys provided!')

        self.screen = pg.display.set_mode((Width, Height))
        self.image = pg.Surface((pl_width, pl_height))
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect()
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]
        # velocity Player 1
        self.vx = 0
        self.vy = 0
        
        if keys2: self.both_keys = True
        else: self.both_keys = False
    
    def update(self):

        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        if keys[self.keys[0]]:
            self.vy -= 8.25
        elif self.sec_keys and self.both_keys:
            if keys[self.keys2[0]]:
                self.vy -= 8.25

        if keys[self.keys[1]]:
            self.vy += 8.25
        elif self.sec_keys and self.both_keys:
            if keys[self.keys2[1]]:
                self.vy += 8.25

        # if key pressed move rectangle
        self.rect.y += self.vy
        # call collision method
        self.collision()
    
    def collision(self):

        # border collision
        if self.rect.top < 0:
            self.rect.y = 0
        if self.rect.bottom > Height:
            self.rect.y = Height-pl_height
    
    def draw_player(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def resetPos(self):

        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]

# class for bot movement
class Bot_Movement:

    def __init__(self):

        self.speed = 12
    
    def compute_movement(self, _ball, _player):

        if _ball.rect.right > Width/2:
            
            _player.vy = self.speed
            if _player.rect.y > _ball.rect.y and abs(_player.rect.y - _ball.rect.y) > 10:
                _player.rect.y -= _player.vy

            elif _player.rect.y < _ball.rect.y and abs(_player.rect.y - _ball.rect.y) > 10 and _player.rect.bottom < Height:
                _player.rect.y += _player.vy
    
    def reset_speed(self):
        self.speed = 12
        
