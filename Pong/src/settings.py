import pygame as pg

# Screen
Width, Height = 1050, 550
Title = "Pong"
FPS = 60

# colors
BG_COLOR = pg.Color('grey12')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
PINK =  (255,20,147)
GREEN = (50, 255, 50)
YELLOW = (249, 215, 28)
RED = (255, 50, 50)
GREY = (160, 160, 160)
LIGHT_GREY = (200, 200, 200)
BORDER_CLR = '#555555'

# Player variables
# Player 1
pl_width = 7
pl_height = 80
player_x = 15
player_y = (Height / 2) - (pl_height / 2)

# Player 2
pl_width_2 = 7
pl_height_2 = 80
player_x_2 = Width -  pl_width_2 - 15
player_y_2 = (Height / 2) - (pl_height_2 / 2)

# Ball variables
ball_dia = 20
ball_x = Width / 2
ball_y = Height / 2
invert_vel = -1 

pl_1_score = 0
pl_2_score = 0
b_vel = [-7.05, 7.05]
score_time = None


# Platform
plat_width = 975
plat_height = 0
plat_x = 0
plat_y = 0

# Middle line
l_width = 3
l_height = 700
l_x = 1200 / 2
l_y = 0

