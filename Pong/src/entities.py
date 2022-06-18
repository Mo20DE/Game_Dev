import pygame as pg
import math
import random
from settings import *

from utils_v2 import HUD_Button, Vec, load_render_images_by_order


# Ball class
class Ball(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.screen = pg.display.set_mode((Width, Height))

        # Draw Ball
        #self.ball = pg.image.load("D:/game_project/images/puck.png")
        self.image = pg.Surface((ball_dia, ball_dia), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, WHITE,(ball_dia/2, ball_dia/2), ball_dia/2)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = Width/2, Height/2

        # Ball velocity
        self.vx = random.choice(b_vel)
        self.vy = random.choice(b_vel)

        self.pl_1_score = 0
        self.pl_2_score = 0

        self.ball_moving = False
        self.goal = True
        self.restart = False
        self.goal_mem = Vec(0, 0)
        self.cooldown = 0
        self.pos = (Width/2, Height/2)
    
    def update(self):
        
        if self.goal or self.restart:
            if self.cooldown >= 50:
                self.cooldown = 0
                self.goal = False
                self.restart = False
                self.ball_moving = True
            else: 
                self.cooldown += 1
                self.ball_moving = False

        if not self.goal and not self.restart:
            # move ball
            self.rect.x -= self.vx
            self.rect.y -= self.vy
            # call collision method
            self.collision() 
            # call handling method
            self.handle_ball_goal_coll()

    def collision(self):

        # frame collision
        if self.rect.top < 0 or self.rect.bottom > Height:
            self.vy *= invert_vel

    def handle_ball_goal_coll(self):

        # check left and right collision
        global b_vel
        if self.rect.right < 0 or self.rect.left > Width:

            if self.rect.right < 0:
                self.goal_mem.y = 1
            else:
                self.goal_mem.x = 1

            self.rect.center = (Width/2, Height/2)
            # change ball direction
            self.set_vel()
            self.goal = True
        
        # increase score
        if self.goal_mem.x == 1 or self.goal_mem.y == 1:

            if self.goal_mem.x == 1:
                self.pl_1_score += 1
            else:
                self.pl_2_score += 1

            self.goal_mem.x = 0
            self.goal_mem.y = 0
    
    def set_vel(self):

        self.vx = random.choice(b_vel)
        self.vy = random.choice(b_vel)
    
    def resetPos(self):

        self.restart = True
        self.cooldown = 0
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

# Middle - Line class
class Line(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l_width, l_height))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = l_x
    
    def middle_line(self, _surface, _color, _x_pos, _y_pos):

        pg.draw.aaline(_surface, _color, _x_pos, _y_pos)

# Text object
class Text:

    def __init__(self, surface, _font, size, text, color, x_pos, y_pos):

        # call parent class sprite constructer
        self.font = pg.font.SysFont(_font, size)
        self.textsurf = self.font.render(text, 1, color)
        surface.blit(self.textsurf, [x_pos, y_pos])

    def get_width(self):

        return self.textsurf.get_width()

    def get_height(self):

        return self.textsurf.get_height()

# game states
class States:

    def __init__(self, gamestates):

        self.gamestates = gamestates
        self.images = load_render_images_by_order(['home', 'restart'], 'images\states', False, True, 50, 50, None, 1)

        self.states_buttons = {
            'home': HUD_Button(self.images[0], (465, 10)),
            'home_2': HUD_Button(self.images[1], (465, 10)),
            'restart': HUD_Button(self.images[2], (535, 10)),
            'restart_2': HUD_Button(self.images[3], (535, 10))
        }

        self.clicked = [False, False]
        self.current_img = ['home', 'restart']
    
    def reset_stats(self, ball, pl_1, pl_2):

        ball.pl_1_score = 0
        ball.pl_2_score = 0
        ball.set_vel()
        ball.resetPos()
        pl_1.resetPos()
        pl_2.resetPos()
    
    def update_button(self, key, key2, img_key, flag, idx, mousePos, ball, pl_1, pl_2):

        if self.states_buttons[key].checkCollision(mousePos):
            self.current_img[idx] = img_key
        else: self.current_img[idx] = key

        if self.states_buttons[key].checkClicked(mousePos) and not self.clicked[idx]:
            self.clicked[idx] = True
        
        if not self.states_buttons[key].checkKeyPressed() and self.clicked[idx]:
            if self.states_buttons[key].checkCollision(mousePos):
                self.gamestates[key2] = flag
                self.reset_stats(ball, pl_1, pl_2)
                self.clicked[idx]  = False
            else: self.clicked[idx]  = False
    
    def return_home(self, mousePos, ball, pl_1, pl_2):

        self.update_button('home', 'play', 'home_2', False, 0, mousePos, ball, pl_1, pl_2)

    def restart_game(self, mousePos, ball, pl_1, pl_2):

        self.update_button('restart', 'restart', 'restart_2', True, 1, mousePos, ball, pl_1, pl_2)

    def update_states(self, mousePos, ball, pl_1, pl_2):

        self.return_home(mousePos, ball, pl_1, pl_2)
        self.restart_game(mousePos, ball, pl_1, pl_2)

    def draw_states(self, screen):

        self.states_buttons[self.current_img[0]].blit_button(screen)
        self.states_buttons[self.current_img[1]].blit_button(screen)

# Utility class
class Utility:

    def __init__(self):

        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.col = False
        self.sound_ball = pg.mixer.Sound("music/ball_sound.wav")

    # collision
    def check_collision(self, sprite1, sprite2):
    
        self.col = pg.sprite.collide_rect(sprite1, sprite2)
        if self.col:
            # if collision play sound effect
            self.sound_ball.play()
            sprite1.vx *= invert_vel - random.uniform(math.sin(0.09), math.sin(0.12))
    
    def check_coll(self, rect1, rect2):
        return rect1.colliderect(rect2)

# class for ball movement effect
# implemented as linked list
class Ball_Shadow:

    def __init__(self, image, alpha, pos):

        self.image = image
        self.alpha = alpha
        self.pos = pos # initial position
        self.image.set_alpha(self.alpha)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

        self.prev_pos = [0, 0]
        self.current_pos = [0, 0]
        self.next_pos = [0, 0]
    
    def set_new_pos(self, curr_pos, next_pos):
        self.current_pos = curr_pos
        self.next_pos = next_pos

# class that produces ball effect
class BallEffect:

    def __init__(self, ball: Ball, amount):

        self.ball = ball
        self.amount = amount
        self.img = self.ball.image
        self.alpha = 120
        self.ball_pos = (self.ball.rect.centerx, self.ball.rect.centery)

        self.ball_shadows = []
        # compute effect balls
        for _ in range(self.amount):

            self.ball_shadow = Ball_Shadow(self.img.copy(), self.alpha, self.ball_pos)
            self.ball_shadows.append(self.ball_shadow)
            if self.alpha >= 0: self.alpha -= 10

    def update_balls(self, prev_pos, current_pos):
        
        if self.ball.ball_moving:

            for i, ball in enumerate(self.ball_shadows):
                if i == 0:
                    ball.current_pos[0] = current_pos[0]
                    ball.current_pos[1] = current_pos[1]
                    ball.prev_pos[0] = prev_pos[0]
                    ball.prev_pos[1] = prev_pos[1]
                else:
                    ball.next_pos[0] = self.ball_shadows[i-1].current_pos[0]
                    ball.next_pos[1] = self.ball_shadows[i-1].current_pos[1]
                    ball.current_pos[0] = self.ball_shadows[i-1].prev_pos[0]
                    ball.current_pos[1] = self.ball_shadows[i-1].prev_pos[1]
           
    def draw_balls(self, screen):

        if self.ball.ball_moving:
            
            for ball in self.ball_shadows[::-1]:
                if ball.current_pos != [0,0]:
                    screen.blit(ball.image, ball.current_pos)

# Score platform
class Platform(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.screen = pg.display.set_mode((Width, Height))
        self.image = pg.Surface([plat_width, plat_height])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = plat_x, plat_y

