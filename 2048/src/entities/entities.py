from framework.utils import *
from framework.static import *


# class to represent a board tile
class BoardTile:

    def __init__(self, size, pos, num, dim, image, spwn_eff=True):
        
        self.size = size
        self.num = num
        self.pos = pos
        self.dim = dim

        self.tile_img = image
        self.tile_rect = self.tile_img.get_rect(topleft=self.pos)

        self.spawn_effect = spwn_eff
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

