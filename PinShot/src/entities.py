from utils import Image
from static import *

import pygame as pg
import math

class Ball:

    def __init__(self):
        
        self.pos = [200, 200]
        self.ball = Image(35, 35)._render_image(ball)
        self.rect = self.ball.get_rect()
        self.rect.topleft = self.pos

        self.arrow = Image(28, 120)._render_image(arrow)
        self.arr_rect = self.arrow.get_rect(center=self.rect.center)

        self.arrow_cpy = self.arrow.copy()

        self.vel = [0,0]

    def draw(self, surface):

        if pg.mouse.get_pressed()[0]:
            surface.blit(self.arrow_cpy, self.arr_rect)

        surface.blit(self.ball, self.rect)
    
    def update(self):

        if pg.mouse.get_pressed()[0]:

            b_x, b_y = self.rect.center
            m_x, m_y = pg.mouse.get_pos()

            #skalar = (b_x*m_x)+(b_y*m_y)
            
            #len_b = math.sqrt(b_x**2 + b_y**2)
            #len_m = math.sqrt(m_x**2 + m_y**2)

            #rad_angle = math.acos(skalar/(len_b*len_m))
            #angle = math.degrees(rad_angle)

            d_x, d_y = abs(b_x-m_x), abs(b_y-m_y)
            angle = math.atan2(d_y, d_x) * (180/math.pi) + 90
            self.arrow_cpy = pg.transform.rotate(self.arrow, angle)
            self.arr_rect = self.arrow_cpy.get_rect(center=self.rect.center)

            print(angle)

