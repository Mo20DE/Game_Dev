import pygame as pg
from pygame import mixer, RESIZABLE

from abc import ABC, abstractmethod
import webbrowser

import math, os
import numpy as np

pg.display.init()
pg.mixer.init()
pg.font.init()


'''
This script provides several classes
and methods to create python games much
easier. The base module used for this 
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
    
    # method with colorkey option  
    def _render_image(self, path, convert=False, transform=True, colorkey=False, mode=0) -> pg.Surface:
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
    
    # method with colorkey option
    def _render_images(self, amount, src, convert=False, transform=True, colorkey=False, mode=0):
        # go through every imae transform and append it
        temp = []
        for i in range(amount):
            # call build function to render single image
            self.image = self._render_image(src[i], convert, transform, colorkey, mode)
            temp.append(self.image)
        # append all proccessed images to main list
        self.images.append(temp)
        return temp
    
    # blit image
    def blitImage(self, screen, pos):
        screen.blit(self.image, pos)


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


# Text object
class Text:

    def __init__(self, x, y, text, font, t_size, t_color, bold=False, italic=False, alpha_val=None):

        self.x, self.y = x, y
        self.pos_cpy = (self.x, self.y)
        self.text = str(text)
        self.font = font
        self.t_size = t_size
        self.t_color = t_color
        self.alpha_val = alpha_val
        self._font = pg.font.SysFont(self.font, self.t_size, bold=bold, italic=italic)
        self.rendered_text = self._font.render(self.text, True, self.t_color)
        if self.alpha_val: self.rendered_text.set_alpha(self.alpha_val)
        self.text_size = self.get_size()
    
    def get_rendered_text(self):
        return self._font.render(self.text, True, self.t_color)
    
    def render_text_on_surface(self, surf):
        surf.blit(self.get_rendered_text(), (self.x, self.y))
    
    def get_image(self):
        return self._font.render(self.text, True, self.t_color)
    
    def get_width(self):
        return self.rendered_text.get_width()
    
    def get_height(self):
        return self.rendered_text.get_height()
    
    def get_size(self):
        return self.rendered_text.get_size()
    
    def get_size_of_str(self, str):
        return self._font.render(str, True, self.t_color).get_size()
    
    def set_pos(self, pos):
        self.x, self.y = pos
    
    def get_pos(self):
        return self.x, self.y
    
    def reset_pos(self):
        self.x, self.y = self.pos_cpy
    
    def set_alpha(self, alpha_val, shift=False):
        if shift and self.alpha_val: 
            self.alpha_val += alpha_val
        else: self.alpha_val = alpha_val
        self.rendered_text.set_alpha(self.alpha_val)
    
    def draw_text(self, canvas):

        # try to render text
        try: 
            canvas.blit(self.rendered_text, (self.x, self.y))
        # catch exception
        except Exception as excp:
            print("Text error occurred!")
            raise excp
            

# sound wrapper
class Sound:

    def __init__(self, sound_path):

        self.sound = sound_path
        self.sound_obj = mixer.Sound(self.sound)
        self.sound_length = int(self.sound_obj.get_length())
    
    def play(self, loops=0, start=0.0, fade_ms=0):

        mixer.music.load(self.sound)
        mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
    
    def stop(self):
        mixer.music.stop()
    
    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def fadeout(self, time):
        mixer.music.fadeout(time)
    
    def get_length(self):
        return self.sound_length
    
    def get_pos(self):
        return int(mixer.music.get_pos()/1000)
    
    def set_pos(self, pos):
        mixer.music.set_pos(pos)

    def set_volume(self, volume):
        mixer.music.set_volume(volume)
    
    def get_volume(self):
        return mixer.music.get_volume()
    
    def get_busy(self):
        return mixer.music.get_busy()


class HUDButton:

    def __init__(self, image, pos, img_onHover=None, web_link=None, prec_click_cd=None):

        # class attributes
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
        
        self.pos_cpy = self.pos
        # attributes for button movement
        self.btn_moving = False
        self.is_btn_on_dest = False
        self.moveDir = None
        self.moveSpeed = 0
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
    
    def setButtonPos(self, pos, centered=False):

        self.pos = pos
        if centered: 
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]
        else: self.rect.topleft = pos
    
    def getButtonPos(self):
        return self.pos
    
    def resetButtonPos(self):

        self.rect.x = self.pos_cpy[0]
        self.rect.y = self.pos_cpy[1]
    
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
    
    def set_button_pos(self, pos):

        self.pos = pos
        self.btn1.setButtonPos(pos)
        if self.mode != "single":
            self.btn2.setButtonPos(pos)
        
    def get_button_pos(self):
        return self.btn1.getButtonPos()
    
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
        self.bg_button = HUDButton(self.back_img, self.pos, self.bg_clr)

        # visual tick button
        self.tick_size = (self.size[0]-10, self.size[1]-10)
        self.tick_pos = (self.bg_button.rect.x+5, self.bg_button.rect.y+5)
        self.tick_img = pg.Surface(self.tick_size)
        self.tick_img.fill(self.default_values["tick_color"])
        self.tick_rect = HUDButton(self.tick_img, self.tick_pos, self.tick_clr)

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

    def __init__(self, **kwargs):
        self.keys_pressed = kwargs
    
    def reset_bools(self, dict_key):
        self.keys_pressed[dict_key] = False
    
    def keyPressed(self, key, dict_key=None):

        # get pressed keys
        keys = pg.key.get_pressed()
        if dict_key is None: return keys[key]

        if not self.keys_pressed[dict_key] and keys[key]:
            self.keys_pressed[dict_key] = True
        
        if self.keys_pressed[dict_key] and not keys[key]:
            self.reset_bools(dict_key)
            return True

        return False

# base class
class BaseClass:

    def __init__(self, pos, size, color=None):

        self.pos = pos
        self.size = size
        self.color = color
    
    def setPos(self, pos): self.pos = pos
    def setSize(self, size): self.size = size
    def setColor(self, color): self.color = color
    def getPos(self): return self.pos
    def getSize(self): return self.size
    def getColor(self): return self.color


# surface class
class Surface(BaseClass):
    
    def __init__(self, pos, size, clr_or_path_or_surf=None, roundness=None):

        # call base class constructor
        super().__init__(pos, size, clr_or_path_or_surf if isinstance(clr_or_path_or_surf, tuple) else None)

        self.surf = pg.Surface(self.size)
        # 1. create a new surface
        if self.color: self.surf.fill(self.color)
        # 2. make surface from path
        elif isinstance(clr_or_path_or_surf, str):
            self.surf = Image(self.size[0], self.size[1])._render_image(clr_or_path_or_surf)
        # 3. transform given surface
        elif isinstance(clr_or_path_or_surf, pg.Surface): 
            self.surf = pg.transform.scale(clr_or_path_or_surf, self.size)
        
        self.roundness = roundness
        self.rect = self.surf.get_rect(topleft=self.pos)
        self.draw_round_corner = False

        if roundness is not None: 
            self.img_cpy = self.surf
            self.set_rounded(roundness)
            self.draw_round_corner = True
        
    def set_rounded(self, roundness):

        size = self.surf.get_size()
        self.rect_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(self.rect_image, (255, 255, 255), (0, 0, *size), border_radius=roundness)

        self.image = self.surf.copy().convert_alpha()
        self.image.blit(self.rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

    def set_pos(self, pos):

        self.setPos(pos)
        self.rect.topleft = pos

    def set_size(self, size):

        self.setSize(size)
        self.surf = pg.transform.scale(self.surf, self.size)
        self.rect.size = self.size

    def set_color(self, color):

        self.setColor(color)
        self.surf.fill(self.color)
        if self.draw_round_corner:
            self.set_rounded(self.roundness)
    
    def rect_collidepoint(self, mPos):
        return self.rect.collidepoint(mPos)
    
    def get_surface(self): 
        return self.image if self.draw_round_corner else self.surf
    
    def draw_surface(self, surface, alpha=None):

        if alpha is not None: 
            self.image.set_alpha(alpha if self.draw_round_corner else self.surf)
        surface.blit(self.image if self.draw_round_corner else self.surf, self.rect)


class Rectangle(BaseClass):

    def __init__(self, pos, size, color, border_rad=0):

        super().__init__(pos, size, color)
        self.border_rad = border_rad
        self.rect = pg.Rect(
            self.pos[0], self.pos[1], 
            self.size[0], self.size[1]
        )
    
    def set_pos(self, pos):
        self.setPos(pos)
        self.rect.topleft = pos
    
    def resize_rect(self, size):
        self.setSize(size)
        self.rect.size = size
    
    def rect_collidepoint(self, mPos):
        return self.rect.collidepoint(mPos)
    
    def draw_rect(self, surface):
        pg.draw.rect(
            surface, self.color, self.rect, 
            border_radius=self.border_rad
        )


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

    SCRLR_CLR1 = (67, 67, 67)
    SCRLR_CLR2 = (89, 89, 89)
    SCRLR_CLR3 = (144, 144, 144)
    SCRLR_CLR4 = (183, 183, 183)



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

            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.non_click_img)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_images(2, self.on_click_img)
        else:
            self.non_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.non_click_img)
            self.on_click_img = Image(self.btn_rad, self.btn_rad)._render_image(self.on_click_img)

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

    def __init__(self, pos, bar_img, btn_img, bar_img_scroll=None, 
            btn_img_onHover=None, def_btn_pos="start"):
        
        self.pos = pos
        self.bar_img = bar_img
        self.btn_img = btn_img
        self.bar_img_scroll = bar_img_scroll
        self.btn_img_onHover = btn_img_onHover

        self.bar_size = self.bar_img.get_size()
        self.btn_size = bar_img.get_size()

        self.bar_rect = self.bar_img.get_rect(topleft=self.pos)
        self.btn = HUDButton(self.btn_img, (0, 0), self.btn_img_onHover)

        if def_btn_pos == "middle":
            self.btn.setButtonPos(self.bar_rect.center, centered=True)
            self.btn_x_off = math.dist((self.bar_rect.left,0), (self.bar_rect.centerx,0))
        elif def_btn_pos == "start": 
            self.btn.setButtonPos((self.bar_rect.left, self.bar_rect.centery), centered=True)
            self.btn_x_off = 0
        else: raise Exception("Invalid default button position!")

        # default tile movement speed
        self.btn_pressed = False
        self.transformScrollBar()
    
    def reset_btn_to_start(self):
        self.btn.rect.centerx = self.pos[0]
        self.transformScrollBar()
    
    def transformScrollBar(self):

        length = math.dist((self.bar_rect.x,0), (self.btn.rect.centerx,0))
        self.bar_img_scroll_cpy = pg.transform.scale(self.bar_img_scroll, (length, self.bar_size[1]))
    
    def isCursorOnBtnAreaOrInRange(self, mPos):

        if ((mPos[0] >= self.btn.rect.left and mPos[0] <= self.btn.rect.right
            and mPos[1] >= self.btn.rect.top and mPos[1] <= self.btn.rect.bottom)
            or mPos[0] >= self.btn.rect.left and mPos[0] <= self.btn.rect.right):
            return True
        return False
    
    def defineMixerInterval(self, steps, mxr_range):
        
        self.mxr_ival = np.linspace(self.bar_rect.left, self.bar_rect.right, steps)
        self.mxr_range = np.linspace(mxr_range[0], mxr_range[1], steps)
    
    def getCurrentMixerPoint(self, only_idx=False):

        mxr_idx = 0
        for i in range(len(self.mxr_ival)-1):
            if self.mxr_ival[i] <= self.btn.rect.centerx < self.mxr_ival[i+1]:
                break
            mxr_idx += 1
            
        return self.mxr_range[mxr_idx] if not only_idx else mxr_idx
    
    def setCurrentMixerPoint(self, point):
        
        self.btn.rect.centerx = self.mxr_ival[point]
        self.transformScrollBar()
    
    def setPropertyImg(self, img, prop="btn"):
        
        if prop == "btn":
            self.btn_img = img
            self.btn.img = img
        elif prop == "btn_oh":
            self.btn_img_onHover = img
            self.btn.img_oh = img
        elif prop == "bar":
            self.bar_img = img
        elif prop == "bar_scroll":
            self.bar_img_scroll = img
            self.transformScrollBar()
        else: raise Exception("Incorrect property type.")
    
    def setBarPos(self, pos):

        self.pos = pos
        self.bar_rect.topleft = self.pos
        self.btn.setButtonPos(
            (self.bar_rect.x+self.btn_x_off,
            self.bar_rect.centery), centered=True)
    
    def getBarPos(self): return self.pos

    def drawBarImg(self, screen):
        screen.blit(self.bar_img, self.bar_rect)
    
    def isBarClicked(self, mPos):
        return True if self.bar_rect.collidepoint(mPos) and pg.mouse.get_pressed()[0] else False

    def draw(self, screen):

        # draw bar and button
        screen.blit(self.bar_img, self.bar_rect)
        if self.bar_img_scroll != None:
            # transfom scroll bar if variable set
            if self.btn_pressed: self.transformScrollBar()
            screen.blit(self.bar_img_scroll_cpy, self.bar_rect)

        self.btn.blitButton(screen)
    
    def update(self, mPos, btn_react_on_bar=False):

        if self.btn_pressed and not self.btn.checkKeyPressed(): 
            self.btn_pressed = False
        # update bar and button
        if self.btn.isBtnClicked(mPos, only_click=True):
            self.btn_pressed = True
        
        if self.btn_pressed or (btn_react_on_bar and self.isBarClicked(mPos)):

            self.btn_x_off = math.dist((self.bar_rect.x,0), (mPos[0],0))
            self.btn.rect.centerx = mPos[0]
            self.btn.rect.centery = self.bar_rect.centery

        # adjust mixer button x axis coordinate
        if self.btn.rect.centerx < self.bar_rect.left:
            self.btn.rect.centerx = self.bar_rect.left
        
        elif self.btn.rect.centerx > self.bar_rect.right:
            self.btn.rect.centerx = self.bar_rect.right
        
        return self.btn_pressed
            

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
        self.can_show_scroller = True
        self.scroll_status = None # flag which indicates scroll direction
        self.scroll_timer = 0

        self.canvas_size = None
        self.page_btm_end_pos = None
        self.click_buff = None

        self.scrlr_themes = {
            "light_theme": (Colors.SCRLR_CLR1, Colors.SCRLR_CLR2),
            "dark_theme": (Colors.SCRLR_CLR3, Colors.SCRLR_CLR4)
        }

    def reset_page(self, reset_opt="position"):

        # case 1: reset position of page and scroller
        # case 2: reset content 
        # case 3: reset everything -> content, size, position of page and scroller
    
        if reset_opt == "position" and self.can_set_scroller:
            self.page_rect.topleft = self.page_pos
            self.scroller_btn.rect.top = self.scroller_btn.pos[1]
        
        elif reset_opt == "content":
            self.page_surf = self.page_cpy
            self.page_surf = pg.transform.scale(self.page_surf, self.page_size)
            self.page_rect = self.page_surf.get_rect(topleft=self.page_pos)
        
        elif reset_opt == "all":
            self.page_surf = self.page_cpy
            self.page_rect = self.page_surf.get_rect(topleft=self.page_pos)
            self.page_size = list(self.page_surf.get_size())
            if self.can_set_scroller:
                self.scroller_btn.rect.top = self.scroller_btn.pos[1]
            self.text_buffer.clear()
            self.set_scroller()
    
    def add_text(self, *args):

        # save text in buffer
        for text in args: self.text_buffer.append(text)
        self.reloadPage()
    
    def reloadPage(self):

        self.reset_page(reset_opt="content")
        self.render_text()

    def render_text(self):
        for text in self.text_buffer:
            text.render_text_on_surface(self.page_surf)
    
    def extendPage(self, pixel):

        self.page_size[1] += pixel
        # re-render text
        self.reloadPage()
        self.page_btm_end_pos = None
    
    def changeTextColor(self, color, reload_page=False):

        for elem in self.text_buffer:
            elem.t_color = color
        if reload_page: self.reloadPage()
    
    def changePageColor(self, color):

        self.page_clr = color
        self.page_surf.fill(self.page_clr)
        self.page_cpy = self.page_surf.copy()
        self.render_text()
    
    def changeScrollerTheme(self, screen_size):

        self.scroller_theme = "dark_theme" if self.scroller_theme == "light_theme" else "light_theme"
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
            Surface(scroller_pos, (scroller_width, scroller_height), 
            clr_or_path_or_surf=self.scrlr_themes[self.scroller_theme][0], roundness=15).get_surface(),
            scroller_pos,
            Surface(scroller_pos, (scroller_width, scroller_height), 
            clr_or_path_or_surf=self.scrlr_themes[self.scroller_theme][1], roundness=15).get_surface()
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
        if self.can_set_scroller and self.can_show_scroller:
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
    
    def __init__(self, width, height, caption, fps, bg_color=None, app_icon=None, win_resizeable=False):

        self.width = width
        self.height = height
        self.fps = fps

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
    def runMain(self):
        
        # this code was old 'main_loop()'
        while self.run:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        pg.quit()


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

def convertSecToTimeFormat(seconds):

    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    time = ""
    if hour > 0: 
        time += str(hour)+":"
        if min > 9: time += str(min)+":"
        else: time += "0"+str(min)+":"
        if sec > 9: time += str(sec)
        else: time += "0"+str(sec)
    elif min > 0:
        time += str(min)+":"
        if sec > 9: time += str(sec)
        else: time += "0"+str(sec)
    else:
        if sec > 9: time += "0:"+str(sec)
        else: time += "0:0"+str(sec)

    return time

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

def load_dir(directory):
    return load_images(directory)

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

# function to clean a list
def cleanList(list, *args):
    formats = args
    for name in list:
        if all(fmt not in name for fmt in formats):
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
    str_list = cleanList(str_list, 'png', 'jpg', 'bmp')
    temp_list = []
    # order list by keywords
    for key in order_keywords:
        for path in str_list:
            if key in path:
                temp_list.append(path)

    images = Image(width, height)._render_images(len(temp_list), temp_list, convert, transform, colorkey, mode)
    return images

