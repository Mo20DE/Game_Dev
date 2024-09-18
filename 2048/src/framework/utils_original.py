import pygame as pg
from pygame import mixer, RESIZABLE

from abc import ABC, abstractmethod
import webbrowser

import math, os
import numpy as np

pg.display.init()
pg.font.init()


'''
This script provides several classes
and methods to create python games much
easier. The base module using for this 
script is pygame.

@author: Mohammed Zain Maqsood
@date: 01.08.2021
'''


# ------------- utility classes ------------- #

# creates an Image object with some
# useful methods and holds its attributes
class Image:

    # holds attributes of class
    def __init__(self, width=None, height=None):

        # stores all images
        self.image = None
        self.images = []
        self.width = width
        self.height = height

    # load and transform single image
    def render_image(self, path, convert, transform) -> pg.Surface:
        # try to load and transform image
        self.path = path
        try:
            if convert:
                image = pg.image.load(path).convert()
                image.set_colorkey((255,255,255))
            else: 
                image = pg.image.load(path)
            if transform and self.width is not None and self.height is not None:
                transformed = pg.transform.scale(image, (self.width, self.height))
                image = transformed
            self.image = image
            return self.image
        # raise exception if an error appeared
        except FileNotFoundError as fError:
            raise fError
    
    # method with colorkey option  
    def _render_image(self, path, convert, transform, colorkey=None, mode=None) -> pg.Surface:
        # try to load and transform image
        self.path = path
        try:
            if convert:
                image = pg.image.load(path).convert()
                if colorkey:
                    if mode == 0:
                        image.set_colorkey((0,0,0))
                    elif mode == 1:
                        image.set_colorkey((255,255,255))
            else: 
                image = pg.image.load(path)
            if transform and self.width is not None and self.height is not None:
                transformed = pg.transform.scale(image, (self.width, self.height))
                image = transformed
            self.image = image
            return self.image
        # raise exception if an error appeared
        except FileNotFoundError as fError:
            raise fError

    # load and transform a list of images
    def render_images(self, amount, src, convert, transform):
        # go through every imae transform and append it
        temp = []
        for i in range(amount):
            # call build function to render single image
            self.image = self.render_image(src[i], convert, transform)
            temp.append(self.image)
        # append all proccessed images to main list
        self.images.append(temp)
        return temp
    
    # method with colorkey option
    def _render_images(self, amount, src, convert, transform, colorkey=None, mode=None):
        # go through every imae transform and append it
        temp = []
        for i in range(amount):
            # call build function to render single image
            self.image = self._render_image(src[i], convert, transform, colorkey, mode)
            temp.append(self.image)
        # append all proccessed images to main list
        self.images.append(temp)
        return temp

    # method to flip a singl image
    def flip_image(self, image, horizontally, vertically):
        return pg.transform.flip(image, horizontally, vertically)
    
    # method to flip multiple images
    def flip_images(self, horizonally, vertically, index):
        flipped = []
        for image in self.images[index]:
            flip = self.flip_image(image, horizonally, vertically)
            flipped.append(flip)
        return flipped
    
    '''# transforms image to rect
    def _transform_image_to_rect(self, path, convert, transform):
        self.image = self.render_image(path, convert, transform)
        self.rect = self.image.get_rect()
        self.tile_tuple = (self.image, self.rect)
        return self.tile_tuple'''
        
    # transforms image to rect with x and y coordinates
    def transform_image_to_rect(self, path, convert, transform, x=None, y=None):
        self.image = self.render_image(path, convert, transform)
        self.rect = self.image.get_rect()
        if x != None and y != None:
            self.rect.x = x
            self.rect.y = y
        self.tile_tuple = (self.image, self.rect)
        return self.tile_tuple
    
    # transform a list of images to rect
    def transform_images_to_rect(self, amount, src, convert, transform, x=None, y=None):
        temp = []
        for i in range(amount):
            # call build function to render and transform single image
            img = self.transform_image_to_rect(src[i], convert, transform, x, y)
            # save img (tuple) in list
            temp.append(img)
        # return desired list
        return temp
    
     # transform a list of images to rect
    def _transform_images_to_rect(self, amount, src, convert, transform, x, y, offset=False, x_off=None, y_off=None):
        temp = []
        for i in range(amount):
            # call build function to render and transform single image
            img = self.transform_image_to_rect(src[i], convert, transform, x, y)
            # apply offset to x and y dimension
            if offset:
                x += x_off
                y += y_off
            # save img (tuple) in list
            temp.append(img)
        # return desired list
        return temp
    
    # blit image
    def blitImage(self, screen, pos):
        screen.blit(self.image, pos)


# surface class
class Surface:
    
    def __init__(self, size, pos, color):

        self.surf = pg.Surface(size)
        self.surf.fill(color)
        self.pos = pos
        self.rect = self.surf.get_rect(topleft=self.pos)

    def blit(self, screen, surf2=None):

        if isinstance(surf2, pg.Surface):
            self.surf.blit(surf2, self.rect)
        else: screen.blit(self.surf, self.pos)


# class to animate images
class Animation:
    
    # set values
    def __init__(self, states, anim_speed):

        self.states = states
        self.anim_speed = anim_speed
    
    # animates a single list of images
    def _render_animation(self, image, vec):

        self.image = image
        self.vec = vec
        self.vec.x += 1

        if self.vec.x >= self.anim_speed and self.vec.y < len(self.states) - 1:
            self.vec.x = 0
            self.vec.y += 1
            self.image = self.states[self.vec.y]
        
        if self.vec.y >= len(self.states) - 1 and self.vec.x >= self.anim_speed:
            self.vec.y = 0
        
        return self.image

    # animates a multidimensional list of images
    def render_animation(self, image, list_idx, vec):

        self.image = image
        self.vec = vec
        self.vec.x += 1

        if self.vec.x >= self.anim_speed and self.vec.y < len(self.states[list_idx]) - 1:
            self.vec.x = 0
            self.vec.y += 1
            self.image = self.states[list_idx][self.vec.y]

        if self.vec.y >= len(self.states[list_idx]) - 1 and self.vec.x >= self.anim_speed:
            self.vec.y = 0

        return self.image

    def change_anim_speed(self, speed):
        self.old_speed = self.anim_speed
        self.anim_speed = speed
    
    def reset_speed(self):
        self.anim_speed = self.old_speed

# class to simulate physics
class Physics2D:

    def __init__(self, player, vector=None, border=None):

        # player object
        self.player = player
        if not isinstance(self.player, pg.Rect):
            self.player = self.player.rect
        # width / height
        if border is not None:
            self.border = border
        # player velocity
        self.vel = vector
        # class attributes
        self.bools = [
                False, # top
                False, # left
                False, # right
                False # ground
        ]
        # jump property
        self.jump = [
            False, # jump
            -1, # j_buff
            -1, # offset
        ]
        # gravity offset
        self.grav_off = -1
        self.collision = False
        self.space = False

    # method to handle border collision
    def handle_borderCollision(self, left, right, top, down):

        self._bools = [left, right, top, down]
        # handle collision
        if self._bools[0]: # left
            if self.player.left < 0:
                self.player.left = 0

        if self._bools[1]: # right
            if self.player.right > self.border[0]:
                self.player.right = self.border[0]
        
        if self._bools[2]: # top
            if self.player.top < 0:
                self.player.top = 0
        
        if self._bools[3]: # bottom
            if self.player.bottom > self.border[1]:
                self.player.bottom = self.border[1]
    
    # method to handle border collision for other object
    def handle_borderCollisionOther(self, obj, left, right, top, down):
        self.otherObj = obj
        if not isinstance(self.otherObj, pg.Rect):
            self.otherObj = self.otherObj.rect
        self.__bools = [left, right, top, down]
        # handle collision
        if self.__bools[0]: # left
            if self.otherObj.left < 0:
                self.otherObj.left = 0

        if self.__bools[1]: # right
            if self.otherObj.right > self.border[0]:
                self.otherObj.right = self.border[0]
        
        if self.__bools[2]: # top
            if self.otherObj.top < 0:
                self.otherObj.top = 0
        
        if self.__bools[3]: # bottom
            if self.otherObj.bottom > self.border[1]:
                self.otherObj.bottom = self.border[1]
    
    def handle_customCollision(self, left=None, right=None, top=None, down=None):
        # handle collision
        if left != None: # left
            if self.player.left < left:
                self.player.left = left
        
        if right != None: # right
            if self.player.right > right:
                self.player.right = right
        
        if top != None: # top
            if self.player.top < top:
                self.player.top = top
        
        if down != None: # bottom
            if self.player.bottom > down:
                self.player.bottom = down
    
    # method to provide general tile collision
    def handle_tileCollision(self, tiles):

        self.tiles = tiles
        self.isList = False

        # if self.tiles is list of rectangles
        if isinstance(self.tiles, list):
            self.isList = True
        # horizontal collision detection
        for tile in self.tiles:
            if self.isList:
                # if tile is tuple (image, rect)
                if isinstance(tile, tuple):
                    tile = tile[1]
            # if self.tiles is not a list
            elif not self.isList:
                tile = tile.rect
            # check for horizontal collision
            if self.player.colliderect(tile):
                if self.vel.x < 0: # left
                    self.player.left = tile.right  
                    # left collision detected
                    self.bools[1] = True
                elif self.vel.x > 0 : # right
                    self.player.right = tile.left
                    # right collision detected
                    self.bools[2] = True
                else:
                    self.bools[1] = False
                    self.bools[2] = False

        # vertical collision detection
        for tile in self.tiles:
            if self.isList:
                # if tile is tuple (image, rect)
                if isinstance(tile, tuple):
                    tile = tile[1]
            # if self.tiles is not a list
            elif not self.isList:
                tile = tile.rect
            # check for vertical collision
            if self.player.colliderect(tile):
                self.collision = True
                if self.vel.y < 0: # top
                    self.player.top = tile.bottom
                    self.vel.y = 0
                    # top collision detected
                    self.bools[0] = True
                if self.vel.y > 0: # bottom
                    self.player.bottom = tile.top
                    self.vel.y = 0
                    # bottom collision detected
                    self.bools[3] = True
            else:
                self.collision = False
        if not self.collision:
            self.bools[0] = False
            self.bools[3] = False
    
    # method to move an object
    def move(self, x, y, coord):
        keys = pg.key.get_pressed()
        self.vel.x = 0
        self.vel.y = 0
        if keys[pg.K_a]:
            self.vel.x -= x
        if keys[pg.K_d]:
            self.vel.x += x
        if keys[pg.K_w]:
            self.vel.y -= y
        if keys[pg.K_s]:
            self.vel.y += y
        # update coordinates
        coord.x += self.vel.x
        coord.y += self.vel.y
    
    def moveX(self, x, coord):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x -= x
        if keys[pg.K_d]:
            self.vel.x += x
        coord.x += self.vel.x
        coord.y += self.vel.y
        return pg.Rect(coord.x, coord.y, 30, 60)

    # method to apply gravity to an object
    def applyGravity(self, gravity, offset, step, mode):
        if mode == 0:
            if self.grav_off == -1:
                self.grav_off = offset
            # increase y velocity
            elif not self.bools[3]:
                self.vel.y += self.grav_off * gravity
                self.grav_off += step
            # reset gravity offset
            else:
                self.grav_off = -1
        else:
            if not self.jump[0] and self.grav_off == -1:
                self.grav_off = offset
            if not self.jump[0] and self.grav_off != -1:
                self.vel.y += gravity + self.grav_off
                self.grav_off += step
            else:
                self.grav_off = -1
    
    # method to apply contant gravity
    def applyconstantGravity(self, gravity):
        self.vel.y += gravity
    
    # method to check for collision types
    def collisionType(self, other= None):
        if other is not None:
            self.other = other
            if self.other.x < 0 or self.other.right > self.border[0]:
                return 'horizontal'
            if self.other.y < 0 or self.other.bottom > self.border[1]:
                return 'vertical'
        else:
            if self.player.x < 0 or self.player.right > self.border[0]:
                return 'horizontal'
            if self.player.y < 0 or self.player.bottom > self.border[1]:
                return 'vertical'
    
        # method to invert velocity
    def invertVelocity(self, xDim, yDim):
        if xDim: self.vel.x *= -1
        if yDim: self.vel.y *= -1
    
    # method to invert gravity
    def invertGravity(self, offset):
        self.vel.y -= offset
    
    # method to update coordinates
    def updateCoords(self):
        self.player.x += self.vel.x
        self.player.y += self.vel.y
    
    # reset velocity
    def resetVelocity(self):
        self.vel.x = 0
        self.vel.y = 0
    
    # set new coordinates
    def setAxis(self, x, y):
        self.player.x = x
        self.player.y = y
    
    # set jump booleans
    def setJumpBools(self):
        # shift key pressed
        self.jump[0] = True
        # player no longer on ground
        self.bools[3] = False
    
    # method to simulate jump
    def playerJump(self, j_buff, offset):
        # decrease y velocity
        if self.jump[1] == -1 and self.jump[2] == -1:
            self.jump[1] = j_buff
            self.jump[2] = offset

        if self.jump[0]:
            self.vel.y -=  self.jump[1]
            self.jump[1] -=  self.jump[2]

        # reset jump buffer
        if self.jump[1] <= 0:
            self.jump[0] = False
            self.jump[1] = -1
            self.jump[2] = -1
    
    def flyJump(self, height, off):
        self.vel.y -= height * off
    
    def rotate(self, image, angle):
        return pg.transform.rotate(image, angle)
    
    def _isCollision(self, tiles):
        for tile in tiles:
            temp = self.checkObject(tile)
            if self.player.colliderect(temp):
                return True
        return False
    
    def checkObject(self, Object):
        if not isinstance(Object, pg.Rect):
            return Object.rect
        return Object
        
    # utility
    def checkRect(self, object):
        if not isinstance(object, pg.Rect):
            object = object.rect
        
    def applyMotion(self):
        pass
    
    def objectInteractions(self, obj1):
        self.obj1 = obj1
        # set correct object to work with
        if not isinstance(self.obj1, pg.Rect):
            self.obj1 = self.obj1.rect
        # handle border collision
        self.handle_borderCollision(True,True,True,True) # player
        self.handle_borderCollisionOther(self.obj1,True,True,True,True) # other
        # check collision types and invert velocity
        if self.collisionType() == 'horizontal':
            self.invertVelocity(True, True)

    # utility
    def dict_to_key(self, bool):
        if bool in self.bools:
            return self.bools[bool]


# Tile class
class Tile:

    def __init__(self, width, height, path):

        self.path = path
        self.width = width
        self.height = height
    
    def make_tile(self, x, y, convert, transform):
        self.image = Image(
            self.width, self.height).render_image(self.path, convert, transform
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile = (self.image, self.rect)
        return self.tile

# vector class with some
# usefull methods to work
class Vec:

    def __init__(self, x, y, z=None):

        self.initial_pos = (x, y, z)
        self.x = self.initial_pos[0]
        self.y = self.initial_pos[1]
        self.z = self.initial_pos[2]

    def sum(self):
        sum = self.x + self.y 
        if self.z is not None:
            sum += self.z
        return sum

    def add_vec(self, other):
        self.x += other.x
        self.y += other.y
        if self.is_Z(self.z) and self.is_Z(other.z):
            self.z += other.z 
        
    def sub_vec(self, other):
        self.x -= other.x
        self.y -= other.y
        if self.is_Z(self.z) and self.is_Z(other.z):
            self.z -= other.z
    
    def norm(self):
        norm = math.sqrt((self.x**2) + (self.y**2) + (self.z**2))
        return norm

    def add_value(self, other):
        self.x += other
        self.y += other

    def is_Z(self, z):
        return False if z is None else True
    
    def reset_vector(self):
        self.x = self.initial_pos[0]
        self.y = self.initial_pos[1]
        self.z = self.initial_pos[2]

    def toString(self):
        return f"x = {self.x}, y = {self.y}, z = {self.z}"

# makes text
class Text:

    def __init__(self, x, y, text, font, t_size, t_color, bold=False, italic=False):

        self.x = x
        self.y = y
        self.text = str(text)
        self.font = font
        self.t_size = t_size
        self.t_color = t_color
        self._font = pg.font.SysFont(self.font, self.t_size, bold=bold, italic=italic)
    
    def get_rendered_text(self):
        return self._font.render(self.text, True, self.t_color)
    
    def render_text_on_surface(self, surf):
        surf.blit(self.get_rendered_text(), (self.x, self.y))
    
    def get_image(self):
        font = pg.font.SysFont(self.font, self.t_size, bold=self.bold, italic=self.italic)
        return font.render(self.text, True, self.t_color)
    
    def draw_text(self, canvas):

        # try to render text
        try:
            text = self._font.render(self.text, True, self.t_color)
            canvas.blit(text, (self.x, self.y))

        # catch exception
        except Exception as excp:
            print("Text error occured!")
            raise excp
    

# makes a button
class Button:

    def __init__(self, width, height, b_color, text=None, font=None, t_size=None, t_color=None):

        if text is not None and font is not None and t_size is not None and t_color is not None:
            self.text = text
            self.font = font
            self.t_size = t_size
            self.t_color = t_color

        self.width = width
        self.height = height
        self.b_color = b_color
        self.canvas = None
        self.rect = None
    
    def set_button(self, x, y, canvas, draw):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(self.canvas, self.b_color, self.rect)
        if draw: self.draw_text()
    
    def draw_text(self):
        text = Text(
            self.x + (self.width/2)-52, self.y-30 + (self.height/2),
            self.text, self.font, self.t_size, self.t_color
        )
        text.draw_text(self.canvas)


class HUDButton:

    def __init__(self, image, pos, img_onHover=None, web_link=None, prec_click_cd=None):

        self.img = image
        self.pos = pos
        self.size = (self.img.get_width(), self.img.get_height())

        # hover image
        self.img_oh = img_onHover
        # second image
        self.sec_img = None
        # button hovering flag
        self.hovering = False
        
        # flag to controll clicking on button
        self.canBtnClick = True
        self.btn_clicked = False

        # rectangle for collision detection
        self.rect = self.img.get_rect(topleft=self.pos)
        # list for collision detection
        self.click_buff = {"not_btn_click": False, "btn_click": False}

        # open link if link given
        self.web_link = web_link

        # atrribute for precise btn collision
        self.prec_rect = None
        # initialize pecise click varible if needed
        if prec_click_cd != None:
            x1, x2 = prec_click_cd[0][0], prec_click_cd[0][1]
            y1, y2 = prec_click_cd[1][0], prec_click_cd[1][1]
            self.prec_rect = pg.Rect(x1, y1, x2-x1, y2-y1)

        # attributes for button movement
        self.btn_moving = False
        self.moveDir = None
        self.moveSpeed = 0
        self.is_btn_on_dest = False

        # attribute for clicking
        self.click_cnt = 0

    def checkCollision(self, mPos):
        
        # precise click surface was set
        if self.prec_rect != None:
            if self.prec_rect.collidepoint(mPos):
                return True
        
        # reset hovering flag
        if self.hovering: self.hovering = False

        # check collision with button
        if self.rect.collidepoint(mPos):
            self.hovering = True

        return self.hovering
    
    def checkKeyPressed(self):
        return True if pg.mouse.get_pressed()[0] == 1 else False
    
    def checkPressedAndColl(self, mPos):
        return self.checkCollision(mPos) and self.checkKeyPressed()
    
    def checkPressedAndNotColl(self, mPos):
        return not self.checkCollision(mPos) and self.checkKeyPressed()
    
    def isBtnReleasedOnBtnArea(self, mPos):
        return not self.checkKeyPressed() and self.checkCollision(mPos)
    
    def isBtnReleasedOnNonBtnArea(self, mPos):
        return not self.checkKeyPressed() and not self.checkCollision(mPos)
    
    def isBtnOnStartPos(self):
        return True if self.rect.x == self.pos[0] and self.rect.y == self.pos[1] else False
    
    def isBtnOnDestPos(self):
        return self.is_btn_on_dest
    
    def isBtnMoving(self):
        return self.btn_moving
    
    def checkValidInput(self, axis, dest, speed):

        if ((axis != "x" and axis != "y") or speed < 1):
            raise ValueError("Invalid axis type or speed.")

        if ((axis == "x" and dest == self.pos[0]) or
            (axis == "y" and dest == self.pos[1])):
            raise ValueError("Button position is identical to destination position.")
        
    def determineMoveDir(self, axis, dest, speed):

        if self.moveDir is None:
            if axis == "x":
                if self.rect.x < dest: self.moveDir = "right"
                else: self.moveDir = "left"
            else:
                if self.rect.y < dest: self.moveDir = "down"
                else: self.moveDir = "up"
            
            self.moveSpeed = speed

    # can control button click functionality
    def setCanBtnClicked(self, bool):
        self.canBtnClick = bool
    
    def setBoolsBtnMove(self, bool1, bool2, bool3=None):

        self.canBtnClick = bool1
        self.btn_moving = bool2
        if bool3 != None and isinstance(bool3, bool): 
            self.is_btn_on_dest = bool3
    
    def setButtonPos(self, pos):

        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def resetButtonPos(self):

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def resetClickBuff(self):

        self.click_buff["not_btn_click"] = False
        self.click_buff["btn_click"] = False

    def resetCollVec(self):
        self.col_vec = [False, False]
    
    def resetBtnClicked(self):
        self.btn_clicked = False
    
    def resetMoveVec(self):
        self.moveVec.reset_vector()
    
    def resetBtnMoving(self):
        self.btn_moving = False
    
    def moveButton(self, axis, dest, speed):

        self.checkValidInput(axis, dest, speed)
        self.determineMoveDir(axis, dest, speed)

        # move button according to direction and speed
        if self.moveDir == "right":
            if self.rect.x < dest - speed:
                self.rect.x += speed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.x = dest
                self.setBoolsBtnMove(True, False, True)
        
        elif self.moveDir == "left":
            if self.rect.x > dest + speed:
                self.rect.x -= speed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.x = dest
                self.setBoolsBtnMove(True, False, True)

        elif self.moveDir == "down":
            if self.rect.y < dest - speed:
                self.rect.y += speed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.y = dest
                self.setBoolsBtnMove(True, False, True)

        else:
            if self.rect.y > dest + speed:
                self.rect.y -= speed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.y = dest
                self.setBoolsBtnMove(True, False, True)

    def moveButtonBack(self):

        # button was never moved
        if self.moveDir == None:
            raise ValueError("Button was never moved.")

        if not self.is_btn_on_dest and not self.isBtnOnStartPos():
            raise ValueError("Can't move button back, because button is moving.")
        
        # move button according to direction and speed
        if self.moveDir == "right":
            if self.rect.x > self.pos[0] + self.moveSpeed:
                self.rect.x -= self.moveSpeed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.x = self.pos[0]
                self.setBoolsBtnMove(True, False, False)
        
        elif self.moveDir == "left":
            if self.rect.x < self.pos[0] - self.moveSpeed:
                self.rect.x += self.moveSpeed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.x = self.pos[0]
                self.setBoolsBtnMove(True, False, False)

        elif self.moveDir == "down":
            if self.rect.y > self.pos[1] + self.moveSpeed:
                self.rect.y -= self.moveSpeed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.y = self.pos[1]
                self.setBoolsBtnMove(True, False, False)

        else:
            if self.rect.y < self.pos[1] - self.moveSpeed:
                self.rect.y += self.moveSpeed
                self.setBoolsBtnMove(False, True)
            else: 
                self.rect.y = self.pos[1]
                self.setBoolsBtnMove(True, False, False)
    
    def setNewImage(self, img):
        # main button image
        if isinstance(img, pg.Surface):
            self.img = img
        else: raise ValueError("Invalid image argument!")
    
    def setSecondImage(self, img):
        # second button image
        # (for a specific action) 
        if isinstance(img, pg.Surface):
            self.sec_img = img
        else: raise ValueError("Invalid image argument!")
    
    def isClickCntEven(self):
        return self.click_cnt % 2 == 0
    
    def isBtnClickedOpenLink(self, mPos):

        if self.isBtnClicked(mPos):
            webbrowser.open(self.web_link)
        
    def isBtnClicked(self, mPos, only_click=False):

        # reset button click flag once
        if self.btn_clicked: self.resetBtnClicked()

        if self.canBtnClick:
            # mouse clicked, but not on button
            if self.checkPressedAndNotColl(mPos) and not self.click_buff["btn_click"]:
                self.click_buff["not_btn_click"] = True

            # check button clicked
            if self.checkPressedAndColl(mPos) and not self.click_buff["not_btn_click"]:
                self.click_buff["btn_click"] = True
            
            # button clicked but released on non button area
            if ((self.click_buff["not_btn_click"] and self.isBtnReleasedOnBtnArea(mPos))
                or (self.click_buff["not_btn_click"] and self.isBtnReleasedOnNonBtnArea(mPos)) or
                (self.click_buff["btn_click"] and self.isBtnReleasedOnNonBtnArea(mPos))):
                self.resetClickBuff()

            # if button clicked and after released (correctly)
            if self.click_buff["btn_click"] and self.isBtnReleasedOnBtnArea(mPos):
                self.resetClickBuff()
                self.btn_clicked = True
                # increase variable for second image
                if self.sec_img != None: self.click_cnt += 1
            
            if self.checkPressedAndColl(mPos) and only_click:
                self.btn_clicked = True
            
        return self.btn_clicked
    
    def blitButton(self, screen):

        # blit second image if set
        if self.img_oh == None and self.sec_img != None and self.click_cnt % 2 != 0:
            screen.blit(self.sec_img, self.rect)
        # blit main image
        elif not self.hovering or self.img_oh == None: 
            screen.blit(self.img, self.rect)
        else:
            # blit on-hover image 
            screen.blit(self.img_oh, self.rect)


# toggle button class
class ToggleButton:

    def __init__(self, pos, def_img1, img2, load_btn_status=None):
        
        # buttons
        self.btn1 = None
        self.btn2 = None
        # button mode (single, double)
        self.mode = None
        self.btn_clicked = False

        # initialize all necessary attributes
        self.init_button(pos, def_img1, img2, load_btn_status)
    
    def init_button(self, pos, def_img1, img2, load_btn_status):

        # case 1: two images, one for on-button, one for off-button
        # case 2: four images, two for on, two for off (with hover images)

        # handle images
        # img1 is on button, img2 is off button
        if isinstance(def_img1, pg.Surface) and isinstance(img2, pg.Surface):
            self.btn1 = HUDButton(def_img1, pos)
            self.btn1.setSecondImage(img2)
            self.mode = "single"

        # img1 is list of first button, img2 is list of second button
        elif isinstance(def_img1, list) and isinstance(img2, list):
            if len(def_img1) == 2 and len(img2) == 2:
                if (isinstance(def_img1[0], pg.Surface) and isinstance(def_img1[1], pg.Surface) and 
                    isinstance(img2[0], pg.Surface) and isinstance(img2[1], pg.Surface)):
                    self.btn1 = HUDButton(def_img1[0], pos, def_img1[1])
                    self.btn2 = HUDButton(img2[0], pos, img2[1])
                    self.mode = "double"

                else:raise ValueError("At least one list element is no Image!")
            else: raise Exception("Both lists must contain 2 images in each list!")
        # incorrect type detected
        else: raise ValueError("img1 or/and img2 are type of unsupported class!")

        # button status
        if load_btn_status != None:
            self.loadBtnStatus(loadingFunc=load_btn_status)
        else: self.status = "off" # default button status
    
    def loadBtnStatus(self, loadingFunc):

        if callable(loadingFunc):
            res = loadingFunc()
            if isinstance(res, str) and (res == "on" or res == "off"):
                self.status = res
            else: raise ValueError("Function output is either no string or has incorrect status type!")
        else: raise ValueError("Argmument must be a function!")
    
    def get_button_status(self):
        return self.status
    
    def set_button_status(self, status):

        self.status = status
        if ((self.status == "on" and not self.btn1.isClickCntEven()) or 
            self.status == "off" and self.btn1.isClickCntEven()):
            self.btn1.click_cnt += 1
            if self.btn2 != None: self.btn2.click_cnt += 1
    
    def isButtonActive(self):
        return True if self.status == "on" else False
    
    def blitButton(self, screen):

        if self.mode == "single":
            self.btn1.blitButton(screen)
        else:
            if self.status == "off": self.btn1.blitButton(screen)
            else: self.btn2.blitButton(screen)

    def isToggleBtnClicked(self, mPos):

        # reset btn clicked
        if self.btn_clicked: self.btn_clicked = False
        # check current mode
        if self.mode == "single":

            if self.btn1.isBtnClicked(mPos):
                if self.status == "off": self.status = "on"
                else: self.status = "off"
                # button was clicked
                self.btn_clicked = True
        else:

            if self.status == "off":
                if self.btn1.isBtnClicked(mPos): 
                    self.status = "on"
                    # button was clicked        
                    self.btn_clicked = True
            else:
                if self.btn2.isBtnClicked(mPos): 
                    self.status = "off"
                    # button was clicked        
                    self.btn_clicked = True

        return self.btn_clicked


# HUD Button (GUI)
# HUD Button class
class HUD_Button:

    def __init__(self, image, pos, onHover_img=None, color=None):

        self.image = image
        if color is not None:
            self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.onHover_img = onHover_img

        self.clicked = False
        self.hovering = False
    
    def set_button_pos(self, pos):

        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def checkCollision(self, mousePos):
        return True if self.rect.collidepoint(mousePos) else False
    
    def checkKeyPressed(self):
        return True if pg.mouse.get_pressed()[0] == 1 else False
    
    def checkClicked(self, mousePos):
        if self.checkCollision(mousePos):
            if self.onHover_img != None:
                self.hovering = True
            if self.checkKeyPressed():
                self.clicked = True
                return self.clicked
        else: self.hovering = False

        self.clicked = False
        return self.clicked
    
    def checkAdvancedClick(self, mousePos):
        if self.checkCollision(mousePos):
            if self.checkKeyPressed():
                self.clicked = True
            if self.clicked and pg.mouse.get_pressed()[0] == 0:
                return True
        self.clicked = False
        return self.clicked
    
    def checkPreciseClick(self, mPos, x_pos, y_pos):
        return self.checkKeyPressed() and checkPreciseMouseClick(mPos, x_pos, y_pos)
    
    def checkPreciseReleaseClick(self, mPos, x_pos, y_pos):
        return True if not self.checkKeyPressed() and checkPreciseMouseClick(mPos, x_pos, y_pos) else False
    
    def blit_button(self, screen):
        screen.blit(self.image, self.rect)
        if not self.hovering:
            screen.blit(self.image, self.rect)
        else: screen.blit(self.onHover_img, self.rect)
    
    def moveButton(self, speed_vec):
     
        self.rect.x += speed_vec.x
        self.rect.y += speed_vec.y
    
    def moveToSpecificPosition(self, rectSide, x, y):

        pass
    
    def get_x(self):
        return self.rect.x
    
    def get_y(self):
        return self.rect.y
            

class Sound:

    def __init__(self, sound=None, volume=None):

        pg.mixer.init()

        self.sound = None
        if sound is not None:
            self.sound = mixer.Sound(sound)

        self.volume = volume
        self.set_object = False
    
    def set_sound_volume(self, sound, volume=None):

        if sound is None and self.sound is None:
            raise ValueError('Sound is not set!')
        elif sound is not None and self.sound is None: 
            self.sound = mixer.Sound(sound)

        if ((volume is None and self.volume is not None) or
            (volume is not None and self.volume is None) or
            (volume is not None and self.volume is not None)):
            self.sound.set_volume(self.volume)
    
    def change_sound(self, volume):
        self.volume = volume
        self.sound.set_volume(self.volume)
    
    def play(self, sound=None, volume=None,  settings=None):

        # settings is a tuple of two values
        # 1. value is how many times sound 
        # should play
        # 2. value is when the sound shall play

        if not self.set_object:
            self.set_sound_volume(sound, volume)
            self.set_object = True

        if settings == -1:
            self.sound.play(settings)
        else:
            self.sound.play()
    
    def pause(self):
        pass

    def unpause(self):
        pass

    def fadeout(self):
        pass

# class for sound bar
class SoundBar:

    def __init__(self, button_size, bar_size, pos=None, btn_circ=False, btn_diam=None,
        button_color=None, bar_color=None, border_color=None, left_bar=False, left_bar_color=None, button_image=None, bar_image=None):
        # mixer button #
        self.button_size = button_size
        if button_image is None:
            self.mixer_button = pg.Surface(self.button_size)
            if button_color != None:
                self.button_color = button_color
                self.mixer_button.fill(button_color)

        elif btn_circ and btn_diam != None:
            self.button_diam = btn_diam
            self.button_color = button_color
            self.mixer_button = pg.Surface((self.button_diam,
            self.button_diam), pg.SRCALPHA, 32)

        else:
            self.mixer_button = button_image

        self.mixer_button_rect = self.mixer_button.get_rect()
        self.mixer_button_pos = None

        # bar #
        self.bar_size = bar_size
        if bar_image is None:
            self.mixer_bar = pg.Surface(self.bar_size)
            if bar_color != None:
                self.bar_color = bar_color
                self.mixer_bar.fill(bar_color)
        else:
            self.mixer_bar = bar_image
        
        self.mixer_bar_rect = self.mixer_bar.get_rect()
        self.mixer_bar_pos = None

        self.isleftbar = left_bar
        self.left_bar_color = left_bar_color
        self.border_clr = border_color

        # set bar pos if position is not None
        if pos is not None:
            self.set_barPos(pos)

        self.vel = Vec(0, 0)
        self.pressed = False

        self.alphaset = False
    
    def checkCollision(self, mousePos):
        return True if self.mixer_button_rect.collidepoint(mousePos) else False
    
    def checkKeyPressed(self):
        return True if pg.mouse.get_pressed()[0] == 1 else False
    
    def checkClicked(self, mousePos):
        if self.checkCollision(mousePos):
            if self.checkKeyPressed():
                return True
        return False

    def set_barPos(self, pos):

        # set position of bar
        self.mixer_bar_pos = pos
        self.mixer_bar_rect.x = self.mixer_bar_pos[0]
        self.mixer_bar_rect.y = self.mixer_bar_pos[1]

        # left and right border
        self.border = pg.Surface((self.bar_size[1]*1.5, self.button_size[1]+10))
        if self.border_clr != None:
            self.border.fill(self.border_clr)
        self.left_border_rect = self.border.get_rect()
        self.left_border_rect.midright = self.mixer_bar_rect.midleft
        self.right_border_rect = self.border.get_rect()
        self.right_border_rect.midleft =  self.mixer_bar_rect.midright

        # set mixer_button in center of bar
        self.mixer_button_pos = (self.mixer_bar_pos[0] + (self.mixer_bar.get_width()/2) - (self.button_size[0]/2), pos[1])
        self.mixer_button_rect.x = self.mixer_button_pos[0]
        self.mixer_button_rect.y = self.mixer_button_pos[1]
        self.mixer_button_rect.centery = self.mixer_bar_rect.centery

        if self.isleftbar:
            bar_width = (self.mixer_button_pos[0] + self.button_size[0]/2) - self.mixer_bar_pos[0]
            self.left_bar = pg.Surface((bar_width, self.bar_size[1]))

            self.left_bar.fill(self.left_bar_color)
            self.left_bar_rect = self.left_bar.get_rect()
            self.left_bar_rect.x = self.mixer_bar_rect.x
            self.left_bar_rect.y = self.mixer_bar_rect.y
    
    def set_alpha_var(self):
        
        # alpha buffer
        if self.button_color != None and self.alpha and not self.alphaset:
            self.temp_surf = pg.Surface(self.button_size)
            self.temp_surf.fill(self.button_color)
            self.buffer = None
            self.alphaset = True
    
    def draw_soundbar(self, screen, update=False, mousePos=None, change_mxr_color=False, 
        change_color=None, alpha=False, alpha_value=None, draw_border=True):

        self.alpha = alpha

        # draw border
        if draw_border:
            screen.blit(self.border, (self.left_border_rect.x, self.left_border_rect.y))
            screen.blit(self.border, (self.right_border_rect.x, self.right_border_rect.y))

        # draw bar
        screen.blit(self.mixer_bar, (self.mixer_bar_rect.x, self.mixer_bar_rect.y))

        # draw on the left side of the mixer 
        # button another bar for current volume
        if self.isleftbar:
            if self.pressed:
                bar_x_offset = (self.mixer_button_rect.x + (self.mixer_button.get_width()/2)) - self.mixer_bar_rect.x 
                resized_surf = pg.transform.scale(self.left_bar, (round(bar_x_offset), round(self.bar_size[1])))
                self.left_bar = resized_surf
            screen.blit(self.left_bar, self.mixer_bar_pos)

        # draw mixer button
        if self.pressed and change_mxr_color:
            self.mixer_button.fill(change_color)

        if alpha:
            self.set_alpha_var()
            draw_alpha(screen, self.temp_surf, (self.mixer_button_rect.x, self.mixer_button_rect.y), alpha_value, self.buffer)
            
        else:
            screen.blit(self.mixer_button, (self.mixer_button_rect.x, self.mixer_button_rect.y))
        
        if update and mousePos != None:
            self.update_soundbar(mousePos)

    def update_soundbar(self, mousePos):

        self.vel.x = 0

        # check if user wants to change volume
        if self.checkClicked(mousePos):
            self.pressed = True
        
        # mouse cursor moves in button rect
        btn_rect = self.mixer_button_rect
        if (checkPreciseMouseClick(mousePos, (btn_rect.x, btn_rect.x + self.mixer_button.get_width()), 
            (btn_rect.y, btn_rect.y + self.mixer_button.get_height())) and self.pressed):

            return
        
        # adjust mixer button x axis coordinate
        if self.mixer_button_rect.x < self.mixer_bar_pos[0]:
            self.mixer_button_rect.x += 5

        elif self.mixer_button_rect.x + self.button_size[0] > self.mixer_bar_pos[0] + self.bar_size[0]:
            self.mixer_button_rect.x -= 5

        # move mixer button along x axis according to user input
        if (self.pressed and self.mixer_button_rect.x >= self.mixer_bar_pos[0] and 
            self.mixer_button_rect.x <= (self.mixer_bar_pos[0] + self.bar_size[0]) - self.button_size[0]):

            if mousePos[0] < self.mixer_button_rect.x:
                self.vel.x -= 5
                self.mixer_button_rect.x += self.vel.x

            elif mousePos[0] > self.mixer_button_rect.x:
                self.vel.x += 5
                self.mixer_button_rect.x += self.vel.x
        
        # if user is not pressing, reset boolean for pressing button
        if not self.checkClicked(mousePos) and not self.checkKeyPressed():
            self.pressed = False
    
    def get_audio_input(self, sound: Sound):
        
        if self.mixer_button_rect.x >= self.mixer_bar_pos[0] and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 10:
            if sound.volume > 0.0:
                sound.volume -= 0.005
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 10 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 60:
            sound.volume = 0.1
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 60 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 100:
            sound.volume = 0.2
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 100 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 150:
            sound.volume = 0.3
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 150 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 190:
            sound.volume = 0.4
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 190 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 240:
            sound.volume = 0.5
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 240 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 300:
            sound.volume = 0.6
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 300 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 340:
            sound.volume = 0.7
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 320 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 360:
            sound.volume = 0.8
        elif self.mixer_button_rect.x >= self.mixer_bar_pos[0] + 360 and self.mixer_button_rect.x <= self.mixer_bar_pos[0] + 420:
            sound.volume = 0.9
        # update sound volume
        sound.change_sound(sound.volume)


# bar with n modes
class ModeBar:

    def __init__(self,  pos: tuple,  modes: int, bar_size: list=None, button_size: list=None, 
    bar_clr: tuple=None, btn_clr: tuple=None, intervall_clr: tuple=None):
        
        # position of bar
        self.pos = pg.math.Vector2()
        self.pos.xy = pos

        # mode intervall
        if modes < 2:
            raise ValueError('Minimum of 2 difficulty modes are required!')
        elif modes > 10:
            raise ValueError('Maximum of 10 difficulty modes are possible!')
        else: self.modes = modes

        # default bar and button size
        self.default_sizes = {
            'bar_size': [250, 5],
            'button_size': [8, 20]
        }
        # default color
        self.default_clr = {
            'bar_color': (0, 0, 0),
            'button_color': (120, 32, 213),
            'mode_step_color': (2, 32, 123)
        }

        # size of bar and button
        self.bar_size = bar_size
        self.button_size = button_size
        if self.bar_size is None: self.bar_size = self.default_sizes['bar_size']
        if self.button_size is None: self.button_size = self.default_sizes['button_size']

        # color
        if bar_clr != None: self.bar_clr = bar_clr
        else: self.bar_clr = self.default_clr['bar_color']
        if btn_clr != None: self.button_clr = btn_clr
        else: self.button_clr = self.default_clr['button_color']
        self.interv_clr = intervall_clr

        # bar surface and rect
        self.bar = pg.Surface(self.bar_size) # surface
        self.bar.fill(self.bar_clr)
        self.bar_rect = self.bar.get_rect() # rect
        # initial position of bar
        self.bar_rect.x = self.pos.x
        self.bar_rect.y = self.pos.y

        # button surface/rect and position
        self.mixer = HUD_Button(pg.Surface(self.button_size), (self.pos.x, self.pos.y), self.button_clr)
        self.mixer.rect.x += self.bar_size[0]/2
        self.mixer.rect.centery = self.bar_rect.centery
        self.mixer_vel = pg.math.Vector2() # direction
        self.mixer_vel.xy = (0, 0)

        # compute inmode intervall
        self.block_pos = []
        self.compute_intervall_blocks()

        self.mxrPressed = False
        self.button_set = False
        # initialize difficulty
        self.difficulty = 0

        # adjust a random initial position
        # of button and difficulty
        self.adjustButton()
    
    def compute_intervall_blocks(self):

        ## left and right border ##

        # make left and right border rect of mode bar
        border = pg.Surface((self.bar_size[1]*1.5, self.button_size[1]+10))
        # fill border with color
        if self.interv_clr != None:
            border.fill(self.interv_clr)

        left_border_rect = border.get_rect()
        left_border_rect.midright = self.bar_rect.midleft
        right_border_rect = border.get_rect()
        right_border_rect.midleft = self.bar_rect.midright

        ## intervall blocks ##
        self.blocks_intervall = np.linspace(self.pos.x, self.bar_rect.right, self.modes)
        b_width = border.get_width() - 4
        b_height = border.get_height() - 10

        block = pg.Surface((b_width, b_height))
        # fill block with color
        if self.interv_clr != None:
            block.fill(self.interv_clr)
        block_rect = block.get_rect() 

        self.block_pos.append((border, left_border_rect, 0))
        for i in range(1, self.modes - 1):
            block_copy = block_rect.copy()
            block_copy.x = self.blocks_intervall[i]
            block_copy.centery = self.bar_rect.centery
            self.block_pos.append((block, block_copy, i))

        self.block_pos.append((border, right_border_rect, self.modes-1))
    
    def adjustButton(self):
        
        for i in range(0, self.modes - 1):
            
            right = self.block_pos[i][1].right
            left = self.block_pos[i+1][1].left
            mid_offset = (right + left)/2

            cur_buttonPos = self.mixer.rect.centerx
            if right < cur_buttonPos and left > cur_buttonPos:
                # save current difficulty
                if i == 0 and self.mixer.rect.centerx < mid_offset:
                    self.mixer.rect.left = right
                    self.difficulty = 0
                    break

                elif i == self.modes-2 and self.mixer.rect.centerx > mid_offset:
                    self.mixer.rect.right = left
                    self.difficulty = self.modes-1
                    break

                else:
                    if self.mixer.rect.centerx < mid_offset:
                        self.mixer.rect.centerx = right
                        self.difficulty = i
                    else:
                        self.mixer.rect.centerx = left
                        self.difficulty = i+1
                    break
            
            else: continue

        # button was successfully adjusted
        self.button_set = True

    def draw_modebar(self, canvas):
        
        # draw bar
        canvas.blit(self.bar, self.pos.xy)

        # draw mode steps
        for mode in self.block_pos:
            canvas.blit(mode[0], (mode[1].x, mode[1].y))
        
        # draw border
        canvas.blit(self.block_pos[0][0], (self.block_pos[0][1].x, self.block_pos[0][1].y))
        canvas.blit(self.block_pos[-1][0], (self.block_pos[-1][1].x, self.block_pos[-1][1].y))

        # draw mixer button
        canvas.blit(self.mixer.image, (self.mixer.rect.x, self.mixer.rect.y))

    def update_modebar(self, mousePos):
        
        self.mixer_vel.x = 0

        # check if user wants to game mode
        if self.mixer.checkClicked(mousePos):
            self.mxrPressed = True
            self.button_set = False

        # adjust mixer button x axis coordinate
        if self.mixer.rect.x < self.pos.x:
            self.mixer.rect.left = self.bar_rect.left
        elif self.mixer.rect.right > self.bar_rect.right:
            self.mixer.rect.right = self.bar_rect.right

        # move mixer button along x axis according to user input
        if self.mxrPressed:
            if mousePos[0] < self.mixer.rect.x:
                self.mixer_vel.x -= 8
                self.mixer.moveButton(self.mixer_vel)
            elif mousePos[0] > self.mixer.rect.right:
                self.mixer_vel.x += 8
                self.mixer.moveButton(self.mixer_vel)
        
        # if user is not pressing, reset boolean for pressing button
        if not self.mixer.checkKeyPressed():
            self.mxrPressed = False
            if not self.button_set:
                self.adjustButton()
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_initial_difficulty(self, difficulty):

        if difficulty < 0 or difficulty > self.modes - 1:
            raise ValueError('Invalid difficulty value!')

        else:
            self.set_difficulty(difficulty)
            if self.difficulty == 0:
                self.mixer.rect.left = self.block_pos[0][1].right
            elif self.difficulty == self.modes - 1:
                self.mixer.rect.right = self.block_pos[-1][1].left
            else:
                self.mixer.rect.centerx = self.block_pos[self.difficulty][1].centerx

    def resize_bar(self, bar_size):
        self.bar_size = bar_size
        self.bar = pg.transform.scale(self.bar, self.bar_size)
        self.bar_rect = self.bar.get_rect()
        self.bar_rect.x = self.pos.x
        self.bar_rect.y = self.pos.y
        self.block_pos.clear()
        self.compute_intervall_blocks()
        
    def resize_button(self, btn_size):
        self.button_size = btn_size
        self.mixer.image = pg.transform.scale(self.mixer.image, self.button_size)
        x = self.mixer.rect.x
        self.mixer.rect = self.mixer.image.get_rect()
        self.mixer.rect.x = x
        self.mixer.rect.centery = self.bar_rect.centery

    def resize_barButton(self, bar_size, btn_size):
        self.resize_bar(bar_size)
        self.resize_button(btn_size)

    def relocate(self, pos):
        pass

# tickbox class
class TickBox:

    def __init__(self, pos, size=None, bg_color=None, tick_color=None, border=False, border_clr=None):
        
        self.default_values = {
            'size': [35, 35],
            'bg_color': Colors.DIMGREY,
            'tick_color': Colors.YELLOW,
        }

        # class attributes
        self.pos = pos
        self.size = self.set_values(size, 'size')
        self.bg_clr = self.set_values(bg_color, 'bg_color')
        self.tick_clr = self.set_values(tick_color, 'tick_color')
        self.border = border
        self.border_clr = border_clr

        # background of tickbox
        self.back_img = pg.Surface(self.size)
        self.back_img.fill(self.default_values["bg_color"])
        self.bg_button = HUD_Button(self.back_img, self.pos, self.bg_clr)

        # visual tick button
        self.tick_size = (self.size[0]-10, self.size[1]-10)
        self.tick_pos = (self.bg_button.rect.x+5, self.bg_button.rect.y+5)
        self.tick_img = pg.Surface(self.tick_size)
        self.tick_img.fill(self.default_values["tick_color"])
        self.tick_rect = HUD_Button(self.tick_img, self.tick_pos, self.tick_clr)

        # boolean
        self.isActive = True
        self.clicked = False
    
    def set_values(self, value, key):
        if value != None: return value
        else: return self.default_values[key]
    
    def check_clicked(self, ms_pos):
        if self.bg_button.checkClicked(ms_pos) and not self.clicked:
            self.clicked = True
    
    def check_pressed(self):
        if self.clicked and not self.bg_button.checkKeyPressed():
            self.isActive = False
    
    def check_active(self, ms_pos):
        if not self.isActive and self.bg_button.checkClicked(ms_pos):
            self.clicked = False
    
    def not_clicket(self):
        if not self.clicked and not self.bg_button.checkKeyPressed():
            self.isActive = True
    
    def update_tickbox(self, ms_pos):
        
        # button off
        self.check_clicked(ms_pos)
        self.check_pressed()
        
        # button on
        self.check_active(ms_pos)
        self.not_clicket()
        
    def draw_tickbox(self, screen):
        # draw onto screen
        screen.blit(self.bg_button.image, self.bg_button.pos)
        if self.isActive:
            screen.blit(self.tick_rect.image, self.tick_rect.pos)

# container class for tickboxes
class TickBox_Container:

    def __init__(self, OAT=False, *argv):
        
        if not isinstance(argv[0], TickBox):
            raise ValueError('Object is not of type: TickBox!')
            
        self.amount = len(argv)
        if self.amount < 1:
            raise ValueError('At least 1 tickbox is required!')
        elif self.amount > 5:
            raise ValueError('Maximum of 10 tickboxes possible at once!')
        
        # class attributes

        # one button at a time is active
        # all other are inactive
        self.oat = OAT # one at time
        self.tickBoxes = argv # list with tickbox objects

        if self.oat: # set tick of first item
            for i in range(1, self.amount):
                self.tickBoxes[i].isActive = False

        # save current states of tickboxes
        self.all_clicked_isActive = []
        for tb in self.tickBoxes:
            self.all_clicked_isActive.append([tb.isActive, tb.clicked])
    
    def setTickBoxToActive(self, num):
        if num < 1 or num > self.amount:
            raise ValueError("Invalid Tickbox Index!")

        for i in range(self.amount):
            if i+1 == num: 
                self.tickBoxes[i].isActive = True
            else:  self.tickBoxes[i].isActive = False
    
    # method to get the index of the active button
    def getActiveButton(self):
        if self.oat:
            for i in range(self.amount):
                if self.all_clicked_isActive[i][0]:
                    return i+1
        else: raise ValueError("OAT not activated!")

    # method to update every tickbox 
    # by the own object method
    def update_tickboxes(self, ms_pos):
        for tb in self.tickBoxes:
            tb.update_tickbox(ms_pos)
    
    def update_oat_tickboxes(self, ms_pos):

        for i, tb in enumerate(self.tickBoxes):

            tb.check_clicked(ms_pos)
            if tb.clicked and not self.all_clicked_isActive[i][0]:
                tb.isActive = True
                for j in range(self.amount):
                    if j != i:
                        self.tickBoxes[j].isActive = False
                break
            
            else:
                tb.clicked = False 
                continue
    
    # method to check if one tickbox is clicked
    def check_clicked(self, ms_pos):
        for tb in self.tickBoxes:
            tb.check_clicked(ms_pos)
            if tb.clicked:
                return True
        return False
    
    # method to save old states of tickbox
    def save_old_states(self):
        for i, tb in enumerate(self.tickBoxes):
            self.all_clicked_isActive[i][0] = tb.isActive
            self.all_clicked_isActive[i][1] = tb.clicked
    
    # method to update container objects
    def update_container_objects(self, ms_pos):
        
        self.save_old_states()

        if self.oat:
            self.update_oat_tickboxes(ms_pos)
        else:
            self.update_tickboxes(ms_pos)
    
    # method to draw every container object
    def draw_container_objects(self, screen):

        for tickbox in self.tickBoxes:
            tickbox.draw_tickbox(screen)


# keys class
class Keys:

    def __init__(self):

        self.keys_pressed = {
            "esc_key": False,
            "return_key": False
        }
    
    def reset_bools(self):

        self.keys_pressed = {
            "esc_key": False,
            "return_key": False
        }
    
    def keyPressed(self, key):

        # get pressed keys
        keys = pg.key.get_pressed()

        if key == pg.K_ESCAPE: d_key = "esc_key"
        else: d_key = "return_key"

        if not self.keys_pressed[d_key] and keys[key]:
            self.keys_pressed[d_key] = True
        
        if self.keys_pressed[d_key] and not keys[key]:
            self.reset_bools()
            return True

        return False

class Colors:

    BLACK = (0, 0, 0)
    WHITE  = (255, 255, 255)
    ALMOSTWHITE = (249, 249, 249)

    RED = (255, 0, 0)
    DRED = (100, 0, 0)

    GREEN = (0, 255, 0)

    BLUE = (0, 0, 255)
    DBLUE = (0, 0, 100)
    DIMBLUE = (110, 192, 248)

    SKYBLUE = (51, 171, 249)
    MIDNIGHTBLUE = (55, 55, 62)
    LIGHTCREAMBLUE = (95, 99, 124)

    GREY = (128, 128, 128)
    DIMGREY = (105, 105, 105)
    LIGHTDARKGREY = (50, 50, 50)
    DARKGREY = (33, 33, 33)
    DGREY = (75, 75, 75)
    LDGREY = (89, 89, 89)

    YELLOW = (255, 204, 0)
    LIGHTYELLOW = (250, 248, 240)
    LIGHTCREAMYELLOW = (234, 216, 196)

    BEIGEBROWN = (145, 120, 96)
    LIGHTBEIGE = (235, 227, 192)
    DARKBLUEGREY = (147, 148, 151)


class ButtonsRow:

    def __init__(self, pos:tuple, btn_rad:int, amount:int, non_click_img_path, 
                on_click_img_path, active_btn:int=0, btn_gap:int=10, axis:int=0):

        self.pos = pos
        self.btn_rad = btn_rad
        self.amount = amount
        self.non_click_img = non_click_img_path
        self.on_click_img = on_click_img_path

        self.active_btn = active_btn # default active button
        self.btn_gap = btn_gap
        self.axis = axis

        # check whether the parameters
        # are all of correct type
        self.check_parameters()

        # contains every button
        self.buttons = []
        self.init_buttons()
        self.mode_changed = False
    
    def check_parameters(self):

        # button size
        if self.btn_rad < 10 or self.btn_rad > 100:
            raise ValueError("Invalid button-radius. Button-radius has to be between: 10 and 100 pixel.")
        
        # amount
        if self.amount < 1 or self.amount > 10:
            raise ValueError("Invalid button-amount provided. Button-amount should be between 1 and 10.")
        
        # button gap
        if self.btn_gap < 0 or self.btn_gap > 100:
            raise ValueError("Invalid button-gap provided. Button-gap has to be between: 0 and 100.")
        
        # button mode
        if self.active_btn < 0 or self.active_btn > self.amount-1:
            raise ValueError(f"Invalid Button-mode. Button-mode has to be between: 0 and {self.amount-1}.")
        
        # axis
        if self.axis != 0 and self.axis != 1:
            raise Exception("Invalid axis provided. Axis has to be 0 or 1.")
    
    def setActiveButton(self, idx):

        if idx < 0 and idx > self.amount-1:
            raise ValueError("Invalid Button Index provided.")
        
        self.active_btn = idx
    
    def setButtonStatus(self, idx, status):

        if idx < 0 and idx > self.amount-1:
            raise ValueError("Invalid Button Index provided.")

        if status != "on" and status != "off":
            raise ValueError("Invalid status type. provided")
        
        self.buttons[idx].status = status
    
    def isModeChanged(self):
        return True if self.mode_changed else False
    
    def getActiveButton(self):
        return self.active_btn
    
    def init_buttons(self):

        # make button images
        if isinstance(self.non_click_img, list) and isinstance(self.on_click_img, list):

            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.non_click_img, False, True)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.on_click_img, False, True)
        else:
            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.non_click_img, False, True)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.on_click_img, False, True)

        btn_pos = list(self.pos)
        # init buttons
        for _ in range(self.amount):
            self.buttons.append(
                ToggleButton(
                    btn_pos,
                    self.non_click_img,
                    self.on_click_img
                )
            )

            # compute gap-offset
            btn_pos[self.axis] += self.btn_rad+self.btn_gap
        
        # set active button
        self.buttons[self.active_btn].status = "on"
    
    def blitButtonRow(self, screen):

        for btn in self.buttons:
            btn.blitButton(screen)
    
    def updateButtonRow(self, mPos):

        # reset variable
        if self.mode_changed: self.mode_changed = False
        # check buttons
        for i, btn in enumerate(self.buttons):
            # update buttons
            if self.active_btn != i:
                if btn.isToggleBtnClicked(mPos):
                    self.buttons[self.active_btn].status = "off"
                    self.buttons[i].status = "on"
                    self.active_btn = i
                    self.mode_changed = True
        
        return self.mode_changed


class SpeedBar:

    def __init__(self, pos, bar_img, btn_img, bar_img_scroll=None, btn_img_onHover=None):
        
        self.pos = pos
        self.bar_img = bar_img
        self.btn_img = btn_img
        self.bar_img_scroll = bar_img_scroll
        self.btn_img_onHover = btn_img_onHover

        self.bar_size = self.bar_img.get_size()
        self.btn_size = bar_img.get_size()

        self.bar_rect = self.bar_img.get_rect(topleft=self.pos)

        self.btn = HUDButton(self.btn_img, (0, 0), self.btn_img_onHover)
        self.btn.rect.center = self.bar_rect.center

        # default tile movement speed
        self.min_speed = 1000 # min-speed: 1s per move
        self.max_speed = 30 # max-speed: 20ms per move
        self.tile_speed = 500 # default speed

        self.transformScrollBar()
        self.btn_pressed = False
        self.anim_spawn = True
        self.anim_move = True
    
    def isCursorOnBtnAreaOrInRange(self, mPos):

        if ((mPos[0] >= self.btn.rect.left and mPos[0] <= self.btn.rect.right
            and mPos[1] >= self.btn.rect.top and mPos[1] <= self.btn.rect.bottom)
            or mPos[0] >= self.btn.rect.left and mPos[0] <= self.btn.rect.right):
            return True
        return False
    
    def transformScrollBar(self):

        if self.bar_img_scroll != None:
            length = self.bar_size[0]-(self.bar_rect.right-self.btn.rect.centerx)
            if length > 0:
                self.bar_img_scroll = pg.transform.scale(self.bar_img_scroll, (round(length), round(self.bar_size[1])))
    
    def regulateSpeed(self):

        if self.btn.rect.centerx <= 242:
            self.tile_speed = self.min_speed
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 256:
            self.tile_speed = 905
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 270:
            self.tile_speed = 810
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 284:
            self.tile_speed = 715
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 298:
            self.tile_speed = 620
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 312:
            self.tile_speed = 525
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 326:
            self.tile_speed = 430
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 340:
            self.tile_speed = 335
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 254:
            self.tile_speed = 240
            self.anim_spawn = True
            self.anim_move = True
        elif self.btn.rect.centerx <= 368:
            self.tile_speed = 140
            self.anim_spawn = False
            self.anim_move = True
        elif self.btn.rect.centerx <= 376:
            self.tile_speed = 45
            self.anim_spawn = False
            self.anim_move = False
        else: 
            self.tile_speed = self.max_speed
            self.anim_spawn = False
            self.anim_move = False

    def draw(self, screen):

        # draw bar and button
        screen.blit(self.bar_img, self.bar_rect)

        if self.bar_img_scroll != None:
            # transfom scroll bar if variable set
            self.transformScrollBar()
            screen.blit(self.bar_img_scroll, self.bar_rect)

        self.btn.blitButton(screen)
    
    def update(self, mPos, btn_move_speed=7):

        if self.btn_pressed and not self.btn.checkKeyPressed(): 
            self.btn_pressed = False
        # update bar and button
        if self.btn.isBtnClicked(mPos, only_click=True):
            self.btn_pressed = True
        
        if self.isCursorOnBtnAreaOrInRange(mPos) and self.btn_pressed: return

        # adjust mixer button x axis coordinate
        if self.btn.rect.centerx < self.bar_rect.left:
            self.btn.rect.centerx = self.bar_rect.left+2
        
        elif self.btn.rect.centerx > self.bar_rect.right:
            self.btn.rect.centerx = self.bar_rect.right-2

        if (self.btn_pressed and self.btn.rect.centerx > self.bar_rect.left
            and self.btn.rect.centerx < self.bar_rect.right):

            if mPos[0] < self.btn.rect.centerx:
                self.btn.rect.centerx -= btn_move_speed

            elif mPos[0] > self.btn.rect.centerx:
                self.btn.rect.centerx += btn_move_speed
            
            # regualte the tile movement speed
            self.regulateSpeed()


class ScrollPage:

    def __init__(self, page_pos:list, page_size:list, page_clr=Colors.GREY, page_img:pg.Surface=None,
                scroller_theme="light_theme", scroller_right_edge=True):
        
        # class attributes
        self.page_pos = page_pos
        self.page_size = page_size
        self.page_clr = page_clr
        self.page_surf = page_img
        self.scroller_theme = scroller_theme
        self.scroller_right_edge = scroller_right_edge
        
        # make surface
        if self.page_surf == None:
            self.page_surf = pg.Surface(self.page_size)
            self.page_surf.fill(self.page_clr)
            self.page_cpy = self.page_surf.copy()

        # make a rect from the surface
        self.page_rect = self.page_surf.get_rect(topleft=self.page_pos)
        self.text_buffer = [] # contains text objects
        self.can_set_scroller = False
        self.scroll_status = None # flag which indicates scroll direction
        self.scroll_timer = 0

        self.canvas_size = None
        self.page_btm_end_pos = None
        self.click_buff = None
    
    def reset_page(self, reset_opt="position", refill_bg=False):

        # case 1: reset position of page and scroller
        # case 2: reset content 
        # case 3: reset everything -> content, size, position of page and scroller
    
        if reset_opt == "position" and self.can_set_scroller:
            self.page_rect.topleft = self.page_pos
            self.scroller_btn.rect.top = self.scroller_btn.pos[1]
        
        elif reset_opt == "content":
            self.page_surf = self.page_cpy
            self.page_surf = pg.transform.scale(self.page_surf, self.page_size)
            if refill_bg: self.page_surf.fill(self.page_clr)
            self.page_rect = self.page_surf.get_rect(topleft=self.page_pos)
        
        elif reset_opt == "all":
            self.page_surf = self.page_cpy
            self.page_rect = self.page_surf.get_rect(topleft=self.page_pos)
            self.page_size = list(self.page_surf.get_size())
            if self.can_set_scroller:
                self.scroller_btn.rect.top = self.scroller_btn.pos[1]
            #self.text_buffer.clear()
    
    def add_text(self, *args):

        # save text in buffer
        for text in args: 
            self.text_buffer.append(text)
        self.reloadPage()
    
    def reloadPage(self, refill_bg=False):

        self.reset_page(reset_opt="content", refill_bg=refill_bg)
        for text in self.text_buffer:
            text.render_text_on_surface(self.page_surf)
    
    def extendPage(self, pixel):

        self.page_size[1] += pixel
        # re-render text
        self.reloadPage()
        self.page_btm_end_pos = None
    
    def changeTextColor(self, color, reload_page=False):

        for i in range(len(self.text_buffer)):
            self.text_buffer[i].t_color = color
        if reload_page: self.reloadPage()
    
    def changePageColor(self, color, refill_bg=False):

        self.page_clr = color
        self.reloadPage(refill_bg=refill_bg)
    
    def changeScrollerTheme(self, screen_size):

        if self.scroller_theme == "light_theme": 
            self.scroller_theme = "dark_theme"
        else: self.scroller_theme = "light_theme"
        self.canvas_size = screen_size
        self.set_scroller()
    
    def generate_scroller(self):

        scroller_width = 8
        # generate scroller
        scroller_height = (max(self.canvas_size[1]-(self.page_size[1]*0.40), 100)if self.scroller_right_edge
                        else max(self.page_size[1]-(self.page_size[1]*0.30), 50))
        scroller_pos = ((self.canvas_size[0]-scroller_width-3, 5) if self.scroller_right_edge
                        else (self.page_rect.right-scroller_width-3, self.page_rect.top+5))
        # make scroller surfaces
        self.scroller_btn = HUDButton(
            Image(scroller_width, scroller_height)._render_image("img/"+self.scroller_theme+"/settings/buttons/menu_buttons/scroller_button.png", False, True),
            scroller_pos,
            Image(scroller_width, scroller_height)._render_image("img/"+self.scroller_theme+"/settings/buttons/menu_buttons/scroller_button_onHover.png", False, True)
        )
    
    def set_scroller(self):

        self.can_set_scroller = True
        self.src_alpha = pg.Surface((15, self.canvas_size[1]))

        if self.scroller_theme == "light_theme":
            self.src_alpha.fill(Colors.ALMOSTWHITE)
        else: self.src_alpha.fill(Colors.DARKGREY)

        self.scroller_bg_pos = (self.canvas_size[0]-14, 0)
        self.scroller_bg_rect = self.src_alpha.get_rect(topleft=self.scroller_bg_pos)
        self.generate_scroller()

    def mouseWheelEvent(self, event, pg_off=8):

        if self.can_set_scroller:
            self.scroll_status = ("positive" if event.y > 0 else "negative")
            self.scroll_timer = pg.time.get_ticks()

            if (not (self.page_rect.y == self.page_pos[1] and self.scroll_status == "positive")
                and not (self.page_rect.bottom == self.page_btm_end_pos and self.scroll_status == "negative")):
                if self.scroll_status == "negative":
                    self.page_rect.y += event.y*pg_off
                    dist_bottom = math.dist((0, self.page_btm_end_pos), (0, self.page_rect.bottom))
                    move_perc = 100-((dist_bottom/self.page_full_dist)*100)
                else:
                    self.page_rect.y += event.y*pg_off
                    dist_top = math.dist((0, self.page_pos[1]), (0, self.page_rect.top))
                    move_perc = ((dist_top/self.page_full_dist)*100)

                # shift scroller
                self.scroller_btn.rect.y = self.scroller_full_dist*(move_perc/100)
            
    def scrollerActions(self, mPos):
        
        # scroller clicked
        if self.scroller_btn.isBtnClicked(mPos, only_click=True) and self.click_buff is None: 
            self.click_buff = math.dist((0, self.scroller_btn.rect.top), (0, mPos[1]))

        if self.click_buff != None and self.scroller_btn.checkKeyPressed():

            self.scroller_btn.hovering = True
            temp = self.scroller_btn.rect.top
            self.scroller_btn.rect.top = mPos[1]-self.click_buff
            move_perc = max(int((temp/self.scroller_full_dist)*100), 1)
            self.scroll_timer = pg.time.get_ticks()

            # shift page
            if temp > self.scroller_btn.rect.top or temp < self.scroller_btn.rect.top:
                self.page_rect.top = self.lin_y_pos[min(move_perc, 98)]

        else: self.click_buff = None

    def handleNonScrollerClick(self, mPos):

        if self.scroller_bg_rect.collidepoint(mPos) and self.scroller_btn.checkKeyPressed():
            # update scroller
            if mPos[1] < self.scroller_btn.rect.top:
                self.scroller_btn.rect.y -= 8
            elif mPos[1] > self.scroller_btn.rect.bottom:
                self.scroller_btn.rect.y += 8
            # update page
            move_perc = max(int((self.scroller_btn.rect.top/self.scroller_full_dist)*100), 1)
            self.page_rect.top = self.lin_y_pos[min(move_perc, 98)]
    
    def handleCorrectPositionsAndBorders(self):
        
        # handle page border
        if self.scroll_status == "positive" and self.page_rect.top > self.page_pos[1]:
            self.page_rect.top = self.page_pos[1]
        elif self.scroll_status == "negative" and self.page_rect.bottom < self.page_btm_end_pos:
            self.page_rect.bottom = self.page_btm_end_pos

        # handle scroller border
        if self.scroller_btn.rect.y < self.scroller_btn.pos[1]:
            self.scroller_btn.rect.y = self.scroller_btn.pos[1]
        elif self.scroller_btn.rect.bottom > self.canvas_size[1]-5:
            self.scroller_btn.rect.bottom = self.canvas_size[1]-5

        # correct page position
        if self.scroller_btn.rect.top == self.scroller_btn.pos[1] and self.page_rect.top != self.page_pos[1]:
            self.page_rect.top = self.page_pos[1]
        elif self.scroller_btn.rect.bottom == self.canvas_size[1]-5 and self.page_rect.bottom != self.page_btm_end_pos:
            self.page_rect.bottom = self.page_btm_end_pos
        
        # correct scroller position
        if self.page_rect.top == self.page_pos[1] and self.scroller_btn.rect.top != 5: 
            self.scroller_btn.rect.top = self.scroller_btn.pos[1]
        elif self.page_rect.bottom == self.page_btm_end_pos and self.scroller_btn.rect.bottom != self.canvas_size[1]-5:
            self.scroller_btn.rect.bottom = self.canvas_size[1]-5
    
    def draw_alpha(self, screen, source, location, alpha):

        surf_buffer = pg.Surface((source.get_width(), source.get_height())).convert()
        x, y = location[0], location[1]
        surf_buffer.blit(screen, (-x, -y))
        surf_buffer.blit(source, (0, 0))
        surf_buffer.set_alpha(alpha)
        screen.blit(surf_buffer, location)
    
    def draw_page(self, screen, page_bottom_end_pos=100, redraw_bg=False, draw_img:pg.Surface=None):

        # set variables
        if self.canvas_size is None or self.page_btm_end_pos is None:
            self.canvas_size = screen.get_size()
            if (self.page_surf.get_height() > self.canvas_size[1] or self.page_rect.bottom > self.canvas_size[1]
                or self.page_rect.bottom > page_bottom_end_pos):

                self.set_scroller()
                self.page_btm_end_pos = (self.canvas_size[1]-10 if page_bottom_end_pos == 10 else page_bottom_end_pos)
                self.page_full_dist = math.dist((0, self.page_rect.bottom), (0, self.page_btm_end_pos))
                self.scroller_full_dist = math.dist((0, self.canvas_size[1]-5), (0, self.scroller_btn.rect.bottom))
                self.lin_y_pos = np.linspace(self.page_pos[1], self.page_pos[1]-self.page_full_dist, 100)
        
        # reddraw the background
        if redraw_bg: screen.fill(screen.get_at((0,0)))
        # draw the page
        screen.blit(self.page_surf, self.page_rect)
        if draw_img != None: screen.blit(draw_img, (0, 0))

        # draw scroller bar
        if self.can_set_scroller:
            mPos = pg.mouse.get_pos()
            if (mPos[0] > self.scroller_btn.rect.left-2 or self.click_buff != None) and self.scroller_right_edge:
                self.draw_alpha(screen, self.src_alpha, self.scroller_bg_pos, 70)
            if (pg.time.get_ticks() - self.scroll_timer < 1000) or mPos[0] > self.scroller_btn.rect.left - 2:
                self.scroller_btn.blitButton(screen)
    
    def update_page(self, mPos):

        if self.can_set_scroller:

            # handle scroller actions
            self.scrollerActions(mPos)
            # handle scroller background click
            self.handleNonScrollerClick(mPos)
            # handle correct positions and borders
            self.handleCorrectPositionsAndBorders()

# Game - Base Class
class Main(ABC):
    
    def __init__(self, width, height, caption, FPS, bg_color=None, app_icon=None, win_resizeable=False):

        self.width = width
        self.height = height
        self.FPS = FPS

        # set app icon
        if app_icon is not None: pg.display.set_icon(app_icon)
        if win_resizeable: self.screen = pg.display.set_mode((self.width, self.height), RESIZABLE)
        else: self.screen = pg.display.set_mode((self.width, self.height))

        # background color
        if bg_color is not None:
            self.screen.fill(bg_color)
            
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()
        self.run = True

        # create new game objects
        self.new()
    
    def new(self):
        pass

    @abstractmethod
    def events(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def blit(self, object, pos):
        self.screen.blit(object, pos)
    
    def dp_update(self):
        pg.display.update()
    
    def dp_update_flip(self):
        pg.display.flip()
    
    def dp_update_mode(self, mode):
        return pg.display.update() if mode == 1 else pg.display.flip()
    
    def handle_quit(self, save_fun: callable=None, *other_funs):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if save_fun is not None: 
                    save_fun()
                self.run = False
            for fun in other_funs:
                fun(event)
    # game loop
    def runGame(self):
        
        # this code was old 'main_loop()'
        while self.run:
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.draw()
        pg.quit()

        # this code was old 'runMain()'
        '''while not self.ended:
            self.new()
            self.main_loop()
        self.game_quit()'''


# ------------- utility functions ------------- #

def draw_mouse(screen, image, pos):
    screen.blit(image, pos)

def draw_alpha(screen, source, location, alpha):
    '''
    @ parameters
        source: pg.Surface (most cases "screen")
        surf_buffer: None
    '''

    surf_buffer = pg.Surface((source.get_width(), source.get_height())).convert()
    x, y = location[0], location[1]
    surf_buffer.blit(screen, (-x, -y))
    surf_buffer.blit(source, (0, 0))
    surf_buffer.set_alpha(alpha)

    screen.blit(surf_buffer, location)

def checkPreciseMouseClick(mouse_pos, x_pos, y_pos):
    return (True if mouse_pos[0] > x_pos[0] and mouse_pos[0] < x_pos[1]
    and mouse_pos[1] > y_pos[0] and mouse_pos[1] < y_pos[1] else False)

# load files in a list
def load_images(directory):
    loaded_files = []
    for filename in os.listdir(directory):
        rel_path = os.path.join(directory, filename)
        if os.path.isfile(rel_path):
            loaded_files.append(rel_path)
    return loaded_files

# check if a specific file exists
def fileExists(path):
    return os.path.exists(path)

# function to sort pictures
def sortList(list):
    sorted = []
    for _ in range(len(list)): 
        sorted.append(0)
    for elem in list:
        for i in range(len(list)):
            if str(i) in elem:
                sorted[i] = elem
            else: continue
    return sorted

def cleanList(list):
    formats = ['png', 'jpg', 'bmp']
    for name in list:
        if formats[0] not in name and formats[1] not in name and formats[2] not in name:
            list.remove(name)
    return list

# load and render images
def load_and_render_images(directory, convert, transform, width=None, height=None, colorkey=None, mode=None):
    dir = load_images(directory)
    # cleaning list
    cleanedDir = cleanList(dir)
    images = Image(width, height)._render_images(len(dir), cleanedDir, convert, transform, colorkey, mode)
    return images

def load_render_images_by_order(order_keywords: list, directory: str, convert: bool, transform: bool, width=None, height=None, colorkey=None, mode=None):
    str_list = load_images(directory)
    str_list = cleanList(str_list)
    temp_list = []
    # order list by keywords
    for key in order_keywords:
        for path in str_list:
            if key in path:
                temp_list.append(path)

    images = Image(width, height)._render_images(len(temp_list), temp_list, convert, transform, colorkey, mode)
    return images

