'''
class HUDButton:

    def __init__(self, image, pos, img_onHover=None):

        self.img = image
        self.pos = pos

        if img_onHover != None:
            self.img_oh = img_onHover
            self.hovering = False
        
        # flag to controll clicking on button
        self.canBtnClick = True

        # rectangle for collision detection
        self.rect = self.img.get_rect(topleft=self.pos)
        # list for collision detection
        self.click_buff = {"not_btn_click": False, "btn_click": False}
        self.btn_clicked = False

        # attributes for button movement
        self.poscpy = self.pos
        self.moveVec = Vec(0, 0)
        self.btn_moving = False

    def checkCollision(self, mPos):

        if self.rect.collidepoint(mPos):
            self.hovering = True
            return True

        if self.hovering: self.hovering = False
        return False
    
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
    
    def setCanBtnClicked(self, bool):
        self.canBtnClick = bool
    
    def resetClickBuff(self):

        self.click_buff["not_btn_click"] = False
        self.click_buff["btn_click"] = False
    
    def setButtonPos(self, pos):

        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def resetButtonPos(self):

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def resetCollVec(self):
        self.col_vec = [False, False]
    
    def resetBtnClicked(self):
        self.btn_clicked = False
    
    def resetMoveVec(self):
        self.moveVec.reset_vector()
    
    def reserBtnMoving(self):
        self.btn_moving = False
    
    def moveButton(self, destPos, speed, dir):

        if dir == "left":
            if self.rect.x > destPos[0] + speed:
                self.rect.x -= speed
                self.canBtnClick = False
            else: 
                self.rect.x = destPos[0]
                self.canBtnClick = True
        
        elif dir == "right":
            if self.rect.x < destPos[0] - speed:
                self.rect.x += speed
                self.canBtnClick = False
            else: 
                self.rect.x = destPos[0]
                self.canBtnClick = True
        
        elif dir == "up":
            if self.rect.y > destPos[1] + speed:
                self.rect.y -= speed
                self.canBtnClick = False
            else: 
                self.rect.y = destPos[1]
                self.canBtnClick = True
        
        elif dir == "down":
            if self.rect.y < destPos[1] - speed:
                self.rect.y += speed
                self.canBtnClick = False
            else: 
                self.rect.y = destPos[1]
                self.canBtnClick = True
    
    def isBtnClicked(self):

        mPos = pg.mouse.get_pos()
        # reset button click flag once
        if self.btn_clicked: self.btn_clicked = False

        if self.canBtnClick:
            # mouse clicked, but not on button
            if self.checkPressedAndNotColl(mPos):
                self.click_buff["not_btn_click"] = True

            # check button clicked
            if self.checkPressedAndColl(mPos) and not self.click_buff["not_btn_click"]:
                self.click_buff["btn_click"] = True

            # button clicked but released on non button area
            if ((self.click_buff["not_btn_click"] and self.isBtnReleasedOnNonBtnArea(mPos))
                or (self.click_buff["not_btn_click"] and self.isBtnReleasedOnBtnArea)):
                self.click_buff["not_btn_click"] = False

            # if button clicked and after released
            if self.click_buff["btn_click"] and self.isBtnReleasedOnBtnArea():
                self.click_buff["btn_click"] = False
                self.btn_clicked = True

        return self.btn_clicked
    
    def checkPreciseBtnClick(self, xPos, yPos):
        return self.isBtnClicked() and checkPreciseMouseClick(xPos, yPos)
    
    def blitButton(self, screen):

        if not self.hovering:
            screen.blit(self.img, self.rect)
        else: screen.blit(self.img_oh, self.rect)
        
'''

'''
############ every game image ############
game_surfaces = {

    "light_theme": { # light game theme properties

        "in_game": {

            "boards": {

            },

            "tiles": {

            }
        },

        "main_menu": {

            "surfaces": {

                "board_previews": {

                    "3x3_preview": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/3x3_preview.png", False, True),
                    "4x4_preview": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/4x4_preview.png", False, True),
                    "5x5_preview": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/5x5_preview.png", False, True)
                },

                "board_font": {
                    "3x3_font": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/3x3_font.png", False, True),
                    "4x4_font": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/4x4_font.png", False, True),
                    "5x5_font": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/5x5_font.png", False, True)
                }
            },

            "buttons": {
                
            
                "start_btn": Image(start_button_size[0], start_button_size[1])._render_image("img/light_theme/main_menu/buttons/start_button.png", False, True),
                "start_btn_oh": Image(start_button_size[0], start_button_size[1])._render_image("img/light_theme/main_menu/buttons/start_button_onHover.png", False, True),

                "sett_btn": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/settings_button.png", False, True),
                "sett_btn_oh": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/settings_button_onHover.png", False, True),
                
                "exit_btn": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/exit_button.png", False, True),
                "exit_btn_oh": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/exit_button_onHover.png", False, True),

                "left_slide_btn": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/left_slide_button.png", False, True),
                "left_slid_btn_oh": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/left_slide_button_onHover.png", False, True),

                "right_slide_btn": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/right_slide_button.png", False, True),
                "right_slide_btn_oh": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/right_slide_button_onHover.png", False, True)
            }
        },

        "game_menu": {

            "surfaces": {

                "icon": Image(game_icon_size[0], game_icon_size[1])._render_image("img/light_theme/game_menu/surfaces/icon.png", False, True),
                "score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/light_theme/game_menu/surfaces/score.png", False, True),
                "best_score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/light_theme/game_menu/surfaces/score.png", False, True),
                "restart_msg_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/game_menu/surfaces/restart_msg_bg.png", False, True)
            },

            "buttons": {

                "home_btn": Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button.png", False, True),
                "home_btn_oh": Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button_onHover.png", False, True),

                "new_game_btn_long": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button.png", False, True),
                "new_game_btn_oh_long": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button_onHover.png", False, True),

                "new_game_btn": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_gm_button.png", False, True),
                "new_game_btn_oh": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_gm_button_onHover.png", False, True),

                "undo_btn": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/undo_button.png", False, True),
                "undo_btn_oh": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/undo_button_onHover.png", False, True)
            }
        },

        "settings": {

            "surfaces": {

                # backgrounds (board question and notification)
                "3x3_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/3x3_b_msg_bg.png", False, True),
                "4x4_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/4x4_b_msg_bg.png", False, True),
                "5x5_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/5x5_b_msg_bg.png", False, True),
                "every_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/every_b_msg_bg.png", False, True),

                "3x3_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/3x3_not_msg_bg.png", False, True),
                "4x4_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/4x4_not_msg_bg.png", False, True),
                "5x5_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/5x5_not_msg_bg.png", False, True),
                "every_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/every_not_msg_bg.png", False, True),

                "delete_board_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/delete_b_data_bg.png", False, True),

                # backgrounds (best score question and notification)
                "3x3_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/3x3_b_sc_msg_bg.png", False, True),
                "4x4_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/4x4_b_sc_msg_bg.png", False, True),
                "5x5_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/5x5_b_sc_msg_bg.png", False, True),
                "every_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/every_b_sc_msg_bg.png", False, True),

                "3x3_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/3x3_not_msg_bg.png", False, True),
                "4x4_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/4x4_not_msg_bg.png", False, True),
                "5x5_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/5x5_not_msg_bg.png", False, True),
                "every_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/every_not_msg_bg.png", False, True),

                "reset_b_sc_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/reset_b_sc_bg.png", False, True),

                "sett_bg": Image(width, height)._render_image("img/light_theme/settings/surfaces/sett_menu_bg.png", False, True),
                "made_by": Image(made_by[0], made_by[1])._render_image("img/light_theme/settings/surfaces/made_by.png", False, True)
            },

            "buttons": {

                

                "back_btn": Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/back_button.png", False, True),
                "back_btn_oh": Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/back_button_onHover.png", False, True),

                "yes_btn": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/yes_button.png", False, True),
                "yes_btn_oh": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/yes_button_onHover.png", False, True),
                "no_btn": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/no_button.png", False, True),
                "no_btn_oh": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/no_button_onhover.png", False, True),
                "ok_btn": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/ok_button.png", False, True),
                "ok_btn_oh": Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/ok_button_onHover.png", False, True)
            }
        }

    },

    "dark_theme": {}
}'''



'''
# all preloaded game images
all_images_light = {


}

# all preloaded game buttons
all_buttons_light = {

    "main_menu": {

        "start_btn": HUDButton(
            Image(start_button_size[0], start_button_size[1])._render_image("img/light_theme/main_menu/buttons/start_button.png", False, True),
            start_button_pos,
            Image(start_button_size[0], start_button_size[1])._render_image("img/light_theme/main_menu/buttons/start_button_onHover.png", False, True)
        ),
                
        "sett_btn": HUDButton(
            Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/settings_button.png", False, True),
            settings_button_pos,
            Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/settings_button_onHover.png", False, True)
        ),

        "exit_btn": HUDButton(
            Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/exit_button.png", False, True),
            exit_button_pos,
            Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/light_theme/main_menu/buttons/exit_button_onHover.png", False, True)
        ),

        "left_slide_btn": HUDButton(
            Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/left_slide_button.png", False, True),
            l_r_slide_btn_pos[0],
            Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/left_slide_button_onHover.png", False, True)
        ),
        
        "right_slide_btn": HUDButton(
            Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/right_slide_button.png", False, True),
            l_r_slide_btn_pos[1],
            Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/light_theme/main_menu/buttons/right_slide_button_onHover.png", False, True)
        )
    },

    "game_menu": {

        "home_btn": HUDButton(
            Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button.png", False, True),
            home_btn_pos,
            Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button_onHover.png", False, True)
        ),

        "new_game_long_btn": HUDButton(
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button.png", False, True),
            new_game_btn_pos,
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button_onHover.png", False, True)
        ),

        "new_game_short_btn": HUDButton(
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_gm_button.png", False, True),
            new_game_btn_pos,
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_gm_button_onHover.png", False, True)
        ),

        "undo_btn": HUDButton(
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/undo_button.png", False, True),
            undo_btn_pos,
            Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/light_theme/game_menu/buttons/undo_button_onHover.png", False, True)
        )
    },

    "settings": {

        "boards_delete_btn": HUDButton(
            Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/reset_boards_button.png", False, True),
            boards_delete_btn_pos,
            Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/reset_boards_button_onHover.png", False, True)
        ),

        "best_score_reset_btn": HUDButton(
            Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/reset_b_sc_button.png", False, True),
            reset_b_score_btn_pos,
            Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/reset_b_sc_button_onHover.png", False, True)
        ),

        "3x3_reset_btn": HUDButton(
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/3x3_reset_button.png", False, True),
            reset_btns_pos1,
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/3x3_reset_button_onHover.png", False, True)
        ),

        "4x4_reset_btn": HUDButton(
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/4x4_reset_button.png", False, True),
            reset_btns_pos2,
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/4x4_reset_button_onHover.png", False, True)
        ),

        "5x5_reset_btn": HUDButton(
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/5x5_reset_button.png", False, True),
            reset_btns_pos3,
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/5x5_reset_button_onHover.png", False, True)
        ),

        "all_reset_btn": HUDButton(
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/all_reset_button.png", False, True),
            reset_btns_pos4,
            Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/all_reset_button_onHover.png", False, True)
        ),

        "yes_btn": HUDButton(
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/yes_button.png", False, True),
            yes_btn_pos,
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/yes_button_onHover.png", False, True)
        ),

        "no_btn": HUDButton(
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/no_button.png", False, True),
            no_btn_pos,
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/no_button_onhover.png", False, True)
        ),

        "ok_btn": HUDButton(
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/ok_button.png", False, True),
            ok_btn_pos,
            Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/ok_button_onHover.png", False, True)
        ),

        "toggle_undo_btn": ToggleButton(
            toggle_undo_btn_pos,
            Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True),
            Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True)
        ),

        "toggle_ai_menu_btn": ToggleButton(

        ),

        "toggle_game_theme_btn": ToggleButton(
            toggle_game_theme_btn_pos,
            Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True),
            Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True)
        ),

        "back_home_btn": HUDButton(
            Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/back_button.png", False, True),
            back_btn_pos,
            Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/back_button_onHover.png", False, True)
        )
    }
}


all_images_dark = {


}

all_buttons_dark = {

    
}'''




'''
def update_mode(self, dir):

        if dir == "right":
            if self.game_ent.mode == "3x3": self.game_ent.mode = "4x4"
            elif self.game_ent.mode == "4x4": self.game_ent.mode = "5x5"
            else: self.game_ent.mode = "3x3"
        else:
            if self.game_ent.mode == "3x3": self.game_ent.mode = "5x5"
            elif self.game_ent.mode == "4x4": self.game_ent.mode = "3x3"
            else: self.game_ent.mode = "4x4"'''



import pygame as pg
from framework.utils import *
from framework.static import *
from entities.entities import ResetButtons, ToggleButton

from menues.mainmenu import MainMenu
from menues.gamemenu import GameMenu
from menues.algomenu import AlgoMenu


class SettingsMenu:

    def __init__(self, mainM: MainMenu, gameM: GameMenu, algoM: AlgoMenu):

        self.mainM = mainM
        self.gameM = gameM # game menu instance (includes boards and bestscores)
        self.algoM = algoM

        # attribute to control reset actions
        self.can_reset = False
        self.can_btns_clicked = True

        self.menu_surf_states = {

            "show_no_b_data_surf": False, # show "no board data availible to delete" surface
            "show_del_b_data_surf": False, # show "delete board data" surface
            "show_yes_no_b_data_surf": False, # show "sure to delete board data" surface

            "show_no_b_sc_surf": False, # show "no best score availible to delete" surface
            "show_b_sc_surf": False, # show "reset best score" surface
            "show_yes_no_b_sc_surf": False # show "sure to delete best score" surface
        }

        # flags to controll, whether some button 
        # or surfaces(menues) should be shown or not
        self.show_flags = {
            "show_undo_btn": True,
            "show_ai_menu": True
        }

        # load every needed variable
        self.load_menu_variables()
    
    def load_menu_variables(self):
        
        # get current game theme
        theme = self.mainM.game_ent.theme

        # surfaces
        self.menu_bg = game_assets[theme]["settings"]["surfaces"]["sett_bg"]
        self.made_by = game_assets[theme]["settings"]["surfaces"]["made_by"]

        self.menu_surf = {

            "board_msg": {

                "delete_board_bg": game_assets[theme]["settings"]["surfaces"]["delete_board_bg"],

                "3x3_del_board": game_assets[theme]["settings"]["surfaces"]["3x3_board_msg"],
                "4x4_del_board": game_assets[theme]["settings"]["surfaces"]["4x4_board_msg"],
                "5x5_del_board": game_assets[theme]["settings"]["surfaces"]["5x5_board_msg"],
                "all_del_board": game_assets[theme]["settings"]["surfaces"]["all_board_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_not_msg"]
            },

            "b_score_msg": {

                "reset_b_sc_bg": game_assets[theme]["settings"]["surfaces"]["reset_b_sc_bg"],

                "3x3_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_msg"],
                "4x4_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_msg"],
                "5x5_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_msg"],
                "all_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["all_b_sc_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_b_sc_not_msg"]
            }
        }

        # GUI elements
        self.menu_btns = {

            "del_board_btn": game_assets[theme]["settings"]["buttons"]["boards_delete_btn"],
            "reset_b_sc_btn": game_assets[theme]["settings"]["buttons"]["best_score_reset_btn"],
            "back_btn": game_assets[theme]["settings"]["buttons"]["back_home_btn"],

            "toggle_undo_btn": game_assets[theme]["settings"]["buttons"]["toggle_undo_btn"],
            "toggle_ai_menu_btn": game_assets[theme]["settings"]["buttons"]["toggle_ai_menu_btn"],
            "toggle_game_theme_btn": game_assets[theme]["settings"]["buttons"]["toggle_game_theme_btn"],

            "yes_btn": game_assets[theme]["settings"]["buttons"]["yes_btn"],
            "no_btn": game_assets[theme]["settings"]["buttons"]["no_btn"],
            "ok_btn": game_assets[theme]["settings"]["buttons"]["ok_btn"],

            "3x3_reset_btn": game_assets[theme]["settings"]["buttons"]["3x3_reset_btn"],
            "4x4_reset_btn": game_assets[theme]["settings"]["buttons"]["4x4_reset_btn"],
            "5x5_reset_btn": game_assets[theme]["settings"]["buttons"]["5x5_reset_btn"],
            "all_reset_btn": game_assets[theme]["settings"]["buttons"]["all_reset_btn"]
        }

    def handle_button_actions(self, mPos):
        
        # back button clicked
        if self.menu_btns["back_btn"].isBtnClicked(mPos):
            self.reset_menu_variables()

        # "delete board" and "reset best score" buttons can be clicked
        if self.can_btns_clicked:

            # case 1: delete board button clicked
            if self.menu_btns["del_board_button"].isBtnClicked(mPos):
                # handle case 1
                self.handleCase(1)

            # case 2: reset best score button clicked
            elif self.menu_btns["reset_b_sc_btn"].isBtnClicked(mPos):
                # handle case 2
                self.handleCase(2)
            
            # case 3: undo toggle button clicked
            elif self.menu_btns["toggle_undo_btn"].isToggleBtnClicked(mPos):
                self.show_flags["show_undo_btn"] = False
            
            # case 4: ai menu toggle button clicked
            elif self.menu_btns["toggle_ai_menu_btn"].isToggleBtnClicked(mPos):
                self.show_flags["show_ai_menu"] = False

            # case 5: game theme toggle button clicked
            elif self.menu_btns["toggle_game_theme_btn"].isToggleBtnClicked(mPos):
                self.changeGameTheme()

        else:

            pass

    def handleCase(self, case):

        if case == 1:
            # lock other buttons
            self.can_btns_clicked = False
            boards_len = len(self.mainM.game_ent.boards)
            sum_score = sum([score for score in self.mainM.game_ent.bestscores.values()])
            # case 1.1: no board data availible to delete<
            if boards_len == 0 and sum_score == 0:
                self.menu_surf_states["show_no_b_sc_surf"] = True
            # case 1.2: board data available to delete
            else:
                self.menu_surf_states["show_del_b_data_surf"] = True
        
        if case == 2:
            # lock other buttons
            self.can_btns_clicked = False
            sum_score = sum([score for score in self.mainM.game_ent.bestscores.values()])
            # case 2.1: no best score available to delete
            if sum_score == 0:
                self.menu_surf_states["show_no_b_sc_surf"] = True
            # case 2.2: best score available to delete
            else:
                self.menu_surf_states["show_b_sc_surf"] = True
    
    def reset_menu_variables(self, reset_all=True, *args):
        
        if reset_all:

            self.mainM.game_ent.game_states["settings"] = False
            self.can_btns_clicked = True
            self.menu_surf_states = {

                "show_no_b_data_surf": False, # show "no board data availible to delete" surface
                "show_del_b_data_surf": False, # show "delete board data" surface
                "show_yes_no_b_data_surf": False, # show "sure to delete board data" surface

                "show_no_b_sc_surf": False, # show "no best score availible to delete" surface
                "show_b_sc_surf": False, # show "reset best score" surface
                "show_yes_no_b_sc_surf": False # show "sure to delete best score" surface
            }
        
        else:

            if "reset_btn_clicked" in args:
                self.can_btns_clicked = True

            for arg in args:
                self.menu_surf_states[arg] = False

    def draw_menues_and_buttons(self, screen):

        # draw back button
        self.menu_btns["back_btn"].blitButton(screen)

        # draw delete board data button
        self.menu_btns["del_board_button"].blitButton(screen)
        # draw reset best score button
        self.menu_btns["reset_b_sc_btn"].blitButton(screen)

        # draw "show undo" toggle button
        self.menu_btns["toggle_undo_btn"].blitButton(screen)
        #draw "show ai menu" toggle button
        self.menu_btns["toggle_ai_menu_btn"].blitButton(screen)
        # draw "game theme" toggle button
        self.menu_btns["toggle_game_theme_btn"].blitButton(screen)
        

    def changeGameTheme(self):
        pass
    
    def draw_reset_menu(self, screen):

        screen.blit(self.sett_reset_sur, reset_menu_pos)
        # text for reset menu
        Text(90, 272, "Are you sure to reset " , "Arial", 30, Colors.BLACK).draw_text(screen)
        Text(90, 312, self.reset_board_btns.btn_mode + self.choose_text[self.active_tickbox] + " ?", "Arial", 30, Colors.BLACK).draw_text(screen)
        self.menu_btns["yes"].blitButton(screen)
        self.menu_btns["no"].blitButton(screen)

    def draw_nothing_to_reset_menu(self, screen):

        screen.blit(self.sett_reset_sur, reset_menu_pos)
        # text info
        Text(120, 272, "  There is no " + self.reset_board_btns.btn_mode , "Arial", 30, Colors.BLACK).draw_text(screen)
        Text(120, 312, " " + self.choose_text[self.active_tickbox] + " to reset!", "Arial", 30, Colors.BLACK).draw_text(screen)
        self.menu_btns["ok"].blitButton(screen)

    def handle_reset_menu_actions(self, mPos):

        keys = pg.key.get_pressed()

        # yes button pressed
        if self.menu_btns["yes"].isBtnClicked(mPos) or keys[pg.K_RETURN]:

            # delete board data
            if self.active_tickbox == 1:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.boards.clear()
                    #self.gameM.bestscores.clear()

                else: del self.gameM.game_ent.boards[self.reset_board_btns.btn_mode]
                    #del self.gameM.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)

            # delete best score
            else:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.bestscores.clear()

                else: del self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)
            
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
        # no button pressed        
        elif self.menu_btns["no"].isBtnClicked(mPos) or keys[pg.K_ESCAPE]:
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
    
    def handle_nothing_to_reset_menu_actions(self, mPos):
        
        keys = pg.key.get_pressed()

        if self.menu_btns["ok"].isBtnClicked(mPos) or keys[pg.K_ESCAPE]:
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
    def canReset(self):

        if self.reset_board_btns.btn_mode != "every":

            if self.active_tickbox == 1:
                return True if self.reset_board_btns.btn_mode in self.gameM.game_ent.boards else False

            if self.reset_board_btns.btn_mode in self.gameM.game_ent.bestscores:
                if self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode] > 0:
                    return True

            return False

        else:

            if self.active_tickbox == 1:
                return True if len(self.gameM.game_ent.boards) > 0 else False

            cnt = sum([i for i in self.gameM.game_ent.bestscores.values()])
            return True if len(self.gameM.game_ent.bestscores) > 0 and cnt > 0 else False
    
    def draw(self, screen):

        # draw menu background
        screen.blit(self.menu_bg, (0, 0))

        # draw menues and buttons
        self.draw_menues_and_buttons(screen)


        ## temp ##

    def update(self, mPos):

        self.handle_button_actions(mPos)

        '''if self.reset_board_btns.btn_clicked:
            if self.can_reset:
                self.handle_reset_menu_actions(mPos)
            else:
                self.handle_nothing_to_reset_menu_actions(mPos)
        else: 
            self.tickboxes.update_container_objects(mPos)
            self.reset_board_btns.update_buttons(mPos)
        
        # handle toggle button actions
        self.theme_toggle_btn.handle_button_action(mPos)'''

        # TODO change color theme, set/unset undo button, show/dont show ai menu


        #print(self.states)
        #print(self.reset_board_btns.states)
        #print(self.tickboxes.getActiveButton())
        #print(self.reset_board_btns.btn_clicked, self.reset_board_btns.btn_idx)
        #print(self.reset_board_btns.btn_mode)
        #print(self.states)


'''class SettingsMenu:

    def __init__(self, mainM: MainMenu, gameM: GameMenu, algoM: AlgoMenu):

        self.mainM = mainM
        self.gameM = gameM # game menu instance (includes boards and bestscores)
        self.algoM = algoM

        # attribute to control reset actions
        self.can_reset = False

        self.menu_states = {

            "show_menu_surf": False
        }

        # flags to controll, whether some button 
        # or surfaces(menues) should be shown or not
        self.show_flags = {
            "undo_btn": True,
            "ai_menu": True
        }

        # load every needed variable
        self.load_menu_variables()
        self.sett_reset_sur = sett_images["settings_reset_surf"]

        # tickboxes to choose to resetboard or best score
        self.tickboxes = TickBox_Container(
            True,
            TickBox((120, 290), (60, 60)),
            TickBox((266, 290), (60, 60))
        )

        # here GUI elements
        self.menu_btns = {
            "yes": sett_hud_btns_2["yes_btn"], # yes button
            "no": sett_hud_btns_2["no_btn"], # no button
            "ok": sett_hud_btns_2["ok_btn"], # ok button
            "back": sett_hud_btns_2["back_btn"] # back button
        }

        # reset buttons for board and best score
        self.reset_board_btns = ResetButtons()
        self.choose_text = {1: " board", 2: " best score"}
        self.active_tickbox = 0

        ####### temp #######
        self.theme_toggle_btn = ToggleButton((300, 450), [toggle_buttons["toggle_off"], toggle_buttons["toggle_off_oh"]], [toggle_buttons["toggle_on"], toggle_buttons["toggle_on_oh"]])
    
    def load_menu_variables(self):
        
        # get current game theme
        theme = self.mainM.game_ent.theme

        # surfaces
        self.menu_bg = game_assets[theme]["settings"]["surfaces"]["sett_bg"]
        self.made_by = game_assets[theme]["settings"]["surfaces"]["made_by"]

        self.menu_surf = {

            "board_msg": {

                "delete_board_bg": game_assets[theme]["settings"]["surfaces"]["delete_board_bg"],

                "3x3_del_board": game_assets[theme]["settings"]["surfaces"]["3x3_board_msg"],
                "4x4_del_board": game_assets[theme]["settings"]["surfaces"]["4x4_board_msg"],
                "5x5_del_board": game_assets[theme]["settings"]["surfaces"]["5x5_board_msg"],
                "all_del_board": game_assets[theme]["settings"]["surfaces"]["all_board_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_not_msg"]
            },

            "b_score_msg": {

                "reset_b_sc_bg": game_assets[theme]["settings"]["surfaces"]["reset_b_sc_bg"],

                "3x3_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_msg"],
                "4x4_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_msg"],
                "5x5_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_msg"],
                "all_reset_b_sc": game_assets[theme]["settings"]["surfaces"]["all_b_sc_msg"],

                "3x3_notf_msg": game_assets[theme]["settings"]["surfaces"]["3x3_b_sc_not_msg"],
                "4x4_notf_msg": game_assets[theme]["settings"]["surfaces"]["4x4_b_sc_not_msg"],
                "5x5_notf_msg": game_assets[theme]["settings"]["surfaces"]["5x5_b_sc_not_msg"],
                "all_notf_msg": game_assets[theme]["settings"]["surfaces"]["all_b_sc_not_msg"]
            }
        }

        # GUI elements
        self.menu_btns = {

            "del_board_btn": game_assets[theme]["settings"]["buttons"]["boards_delete_btn"],
            "reset_b_sc_btn": game_assets[theme]["settings"]["buttons"]["best_score_reset_btn"],
            "back_btn": game_assets[theme]["settings"]["buttons"]["back_home_btn"],

            "toggle_undo_btn": game_assets[theme]["settings"]["buttons"]["toggle_undo_btn"],
            "toggle_ai_menu_btn": game_assets[theme]["settings"]["buttons"]["toggle_ai_menu_btn"],
            "toggle_game_theme_btn": game_assets[theme]["settings"]["buttons"]["toggle_game_theme_btn"],

            "yes_btn": game_assets[theme]["settings"]["buttons"]["yes_btn"],
            "no_btn": game_assets[theme]["settings"]["buttons"]["no_btn"],
            "ok_btn": game_assets[theme]["settings"]["buttons"]["ok_btn"],

            "3x3_reset_btn": game_assets[theme]["settings"]["buttons"]["3x3_reset_btn"],
            "4x4_reset_btn": game_assets[theme]["settings"]["buttons"]["4x4_reset_btn"],
            "5x5_reset_btn": game_assets[theme]["settings"]["buttons"]["5x5_reset_btn"],
            "all_reset_btn": game_assets[theme]["settings"]["buttons"]["all_reset_btn"]
        }

    def changeGameTheme(self):
        pass
    
    def checkBackButton(self, mPos):

        if self.menu_btns["back"].isBtnClicked(mPos):

            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
            self.gameM.game_ent.resetStateAndWasClicked("settings")
    
    def draw_reset_menu(self, screen):

        screen.blit(self.sett_reset_sur, reset_menu_pos)
        # text for reset menu
        Text(90, 272, "Are you sure to reset " , "Arial", 30, Colors.BLACK).draw_text(screen)
        Text(90, 312, self.reset_board_btns.btn_mode + self.choose_text[self.active_tickbox] + " ?", "Arial", 30, Colors.BLACK).draw_text(screen)
        self.menu_btns["yes"].blitButton(screen)
        self.menu_btns["no"].blitButton(screen)

    def draw_nothing_to_reset_menu(self, screen):

        screen.blit(self.sett_reset_sur, reset_menu_pos)
        # text info
        Text(120, 272, "  There is no " + self.reset_board_btns.btn_mode , "Arial", 30, Colors.BLACK).draw_text(screen)
        Text(120, 312, " " + self.choose_text[self.active_tickbox] + " to reset!", "Arial", 30, Colors.BLACK).draw_text(screen)
        self.menu_btns["ok"].blitButton(screen)

    def handle_reset_menu_actions(self, mPos):

        keys = pg.key.get_pressed()

        # yes button pressed
        if self.menu_btns["yes"].isBtnClicked(mPos) or keys[pg.K_RETURN]:

            # delete board data
            if self.active_tickbox == 1:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.boards.clear()
                    #self.gameM.bestscores.clear()

                else: del self.gameM.game_ent.boards[self.reset_board_btns.btn_mode]
                    #del self.gameM.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)

            # delete best score
            else:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.bestscores.clear()

                else: del self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)
            
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
        # no button pressed        
        elif self.menu_btns["no"].isBtnClicked(mPos) or keys[pg.K_ESCAPE]:
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
    
    def handle_nothing_to_reset_menu_actions(self, mPos):
        
        keys = pg.key.get_pressed()

        if self.menu_btns["ok"].isBtnClicked(mPos) or keys[pg.K_ESCAPE]:
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
    def canReset(self):

        if self.reset_board_btns.btn_mode != "every":

            if self.active_tickbox == 1:
                return True if self.reset_board_btns.btn_mode in self.gameM.game_ent.boards else False

            if self.reset_board_btns.btn_mode in self.gameM.game_ent.bestscores:
                if self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode] > 0:
                    return True

            return False

        else:

            if self.active_tickbox == 1:
                return True if len(self.gameM.game_ent.boards) > 0 else False

            cnt = sum([i for i in self.gameM.game_ent.bestscores.values()])
            return True if len(self.gameM.game_ent.bestscores) > 0 and cnt > 0 else False
    
    def draw(self, screen):

        # draw menu background
        screen.blit(self.menu_bg, (0, 0))

        self.tickboxes.draw_container_objects(screen)
        self.reset_board_btns.draw_buttons(screen)
        # draw back button
        self.menu_btns["back"].blitButton(screen)

        if self.reset_board_btns.btn_clicked:
            # get active tickbox button
            self.active_tickbox = self.tickboxes.getActiveButton()
            # get state of reset
            self.can_reset = self.canReset()
            # draw reset window
            if self.can_reset: self.draw_reset_menu(screen)
            else: self.draw_nothing_to_reset_menu(screen)
        

        ## temp ##
        self.theme_toggle_btn.draw_button(screen)

    def update(self, mPos):

        # if back button clicked
        self.checkBackButton(mPos)

        if self.reset_board_btns.btn_clicked:
            if self.can_reset:
                self.handle_reset_menu_actions(mPos)
            else:
                self.handle_nothing_to_reset_menu_actions(mPos)
        else: 
            self.tickboxes.update_container_objects(mPos)
            self.reset_board_btns.update_buttons(mPos)
        
        # handle toggle button actions
        self.theme_toggle_btn.handle_button_action(mPos)

        # TODO change color theme, set/unset undo button, show/dont show ai menu


        #print(self.states)
        #print(self.reset_board_btns.states)
        #print(self.tickboxes.getActiveButton())
        #print(self.reset_board_btns.btn_clicked, self.reset_board_btns.btn_idx)
        #print(self.reset_board_btns.btn_mode)
        #print(self.states)'''

# toggle button class
class _ToggleButton:

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
            if callable(load_btn_status):
                res = load_btn_status()
                if isinstance(res, str) and (res == "on" or res == "off"):
                    self.status = load_btn_status()
                else: raise ValueError("Function output is either no string or has incorrect status type!")
            else: raise ValueError("Argmument must be a function!")
        else: self.status = "off" # default button status
    
    def get_button_status(self):
        return self.status
    
    def isButtonActive(self):
        return True if self.status == "on" else False
    
    def resetButtonClickd(self):
        self.btn_clicked = False
    
    def draw_button(self, screen):

        if self.mode == "single":
            self.btn1.blitButton(screen)
        else:
            if self.status == "off": self.btn1.blitButton(screen)
            else: self.btn2.blitButton(screen)

    def handle_button_action(self, mPos):

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

        #print(self.status)


'''
def handle_button_actions(self, mPos):
        
        # back button clicked (reset settings menu)
        if self.menu_btns["back_btn"].isBtnClicked(mPos):
            self.reset_menu_variables(reset_all=True)

        # "delete board" and "reset best score" buttons can be clicked
        if self.del_res_menu_stage == 1:

            self.handleStageOne(mPos)

        elif self.del_res_menu_stage == 2:

            ### board data ###
            self.handleStageTwo(mPos, "show_no_b_data_surf", "show_del_b_data_surf", "1.2")
            ### best score ###
            self.handleStageTwo(mPos, "show_no_b_sc_surf", "show_b_sc_surf", "2.2")
                
        # menu stage 3 (last stage)
        else:
            
            ### board data ###
            self.handleStageThree(self, "show_no_mode_b_data_surf", "show_yes_no_b_data_surf")
            ### best score ###
            self.handleStageThree(mPos, "show_no_mode_b_sc_surf", "show_yes_no_b_sc_surf")
            '''


'''
def draw_menues_and_buttons(self, screen):

        # draw back button
        self.menu_btns["back_btn"].blitButton(screen)

        # draw delete board data button
        self.menu_btns["del_board_btn"].blitButton(screen)
        # draw reset best score button
        self.menu_btns["reset_b_sc_btn"].blitButton(screen)

        # draw "show undo" toggle button
        self.menu_btns["toggle_undo_btn"].blitButton(screen)
        #draw "show ai menu" toggle button
        self.menu_btns["toggle_ai_menu_btn"].blitButton(screen)
        # draw "game theme" toggle button
        self.menu_btns["toggle_game_theme_btn"].blitButton(screen)

        # draw menues

        ### board data ###
        if self.menu_surf_states["show_no_b_data_surf"]:

            # draw notifications message
            screen.blit(self.menu_surf["board_msg"]["all_notf_msg"], restart_window_pos)
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_del_b_data_surf"]:

            # draw notifications message
            screen.blit(self.menu_surf["board_msg"]["delete_board_bg"], restart_window_pos)
            # draw quit btn
            self.menu_btns["quit_btn"].blitButton(screen)

            # draw buttons for delete options
            self.menu_btns["3x3_reset_btn"].blitButton(screen)
            self.menu_btns["4x4_reset_btn"].blitButton(screen)
            self.menu_btns["5x5_reset_btn"].blitButton(screen)
            self.menu_btns["all_reset_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_no_mode_b_data_surf"]:
            
            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["board_msg"]["3x3_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["board_msg"]["4x4_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["board_msg"]["5x5_notf_msg"], restart_window_pos)
            
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_yes_no_b_data_surf"]:

            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["board_msg"]["3x3_del_board"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["board_msg"]["4x4_del_board"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["board_msg"]["5x5_del_board"], restart_window_pos)
            
            # draw yes button
            self.menu_btns["yes_btn"].blitButton(screen)
            # draw no button
            self.menu_btns["no_btn"].blitButton(screen)


        ### best score ###
        if self.menu_surf_states["show_no_b_sc_surf"]:
            
            screen.blit(self.menu_surf["b_score_msg"]["all_notf_msg"], restart_window_pos)
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_b_sc_surf"]:

            # draw notifications message
            screen.blit(self.menu_surf["b_score_msg"]["reset_b_sc_bg"], restart_window_pos)
            # draw quit btn
            self.menu_btns["quit_btn"].blitButton(screen)

            # draw buttons for delete options
            self.menu_btns["3x3_reset_btn"].blitButton(screen)
            self.menu_btns["4x4_reset_btn"].blitButton(screen)
            self.menu_btns["5x5_reset_btn"].blitButton(screen)
            self.menu_btns["all_reset_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_no_mode_b_sc_surf"]:
            
            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["b_score_msg"]["3x3_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["b_score_msg"]["4x4_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["b_score_msg"]["5x5_notf_msg"], restart_window_pos)
            
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_yes_no_b_sc_surf"]:

            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["b_score_msg"]["3x3_reset_b_sc"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["b_score_msg"]["3x3_reset_b_sc"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["b_score_msg"]["3x3_reset_b_sc"], restart_window_pos)
            
            # draw yes button
            self.menu_btns["yes_btn"].blitButton(screen)
            # draw no button
            self.menu_btns["no_btn"].blitButton(screen)
        
        print(self.menu_surf_states, "\n")'''



'''
def handle_reset_menu_actions(self, mPos):

        keys = pg.key.get_pressed()

        # yes button pressed
        if self.menu_btns["yes"].isBtnClicked(mPos) or keys[pg.K_RETURN]:

            # delete board data
            if self.active_tickbox == 1:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.boards.clear()
                    #self.gameM.bestscores.clear()

                else: del self.gameM.game_ent.boards[self.reset_board_btns.btn_mode]
                    #del self.gameM.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)

            # delete best score
            else:

                if self.reset_board_btns.btn_mode == "every":
                    self.gameM.game_ent.bestscores.clear()

                else: del self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode]

                print("deleted: ", self.reset_board_btns.btn_mode)
            
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
        # no button pressed        
        elif self.menu_btns["no"].isBtnClicked(mPos) or keys[pg.K_ESCAPE]:
            # reset menu variables
            self.reset_board_btns.resetMenuVariables()
            self.can_reset = False
        
    def canReset(self):

        if self.reset_board_btns.btn_mode != "every":

            if self.active_tickbox == 1:
                return True if self.reset_board_btns.btn_mode in self.gameM.game_ent.boards else False

            if self.reset_board_btns.btn_mode in self.gameM.game_ent.bestscores:
                if self.gameM.game_ent.bestscores[self.reset_board_btns.btn_mode] > 0:
                    return True

            return False

        else:

            if self.active_tickbox == 1:
                return True if len(self.gameM.game_ent.boards) > 0 else False

            cnt = sum([i for i in self.gameM.game_ent.bestscores.values()])
            return True if len(self.gameM.game_ent.bestscores) > 0 and cnt > 0 else False'''


'''
### board data ###
        if self.menu_surf_states["show_no_b_data_surf"]:

            # draw notifications message
            screen.blit(self.menu_surf["board_msg"]["all_notf_msg"], restart_window_pos)
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_del_b_data_surf"]:

            # draw notifications message
            screen.blit(self.menu_surf["board_msg"]["delete_board_bg"], restart_window_pos)
            # draw quit btn
            self.menu_btns["quit_btn"].blitButton(screen)

            # draw buttons for delete options
            self.menu_btns["3x3_reset_btn"].blitButton(screen)
            self.menu_btns["4x4_reset_btn"].blitButton(screen)
            self.menu_btns["5x5_reset_btn"].blitButton(screen)
            self.menu_btns["all_reset_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_no_mode_b_data_surf"]:
            
            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["board_msg"]["3x3_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["board_msg"]["4x4_notf_msg"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["board_msg"]["5x5_notf_msg"], restart_window_pos)
            
            # draw ok button
            self.menu_btns["ok_btn"].blitButton(screen)
        
        if self.menu_surf_states["show_yes_no_b_data_surf"]:

            # draw notifications message
            if self.del_res_buff == "3x3":
                screen.blit(self.menu_surf["board_msg"]["3x3_del_board"], restart_window_pos)
            
            elif self.del_res_buff == "4x4":
                screen.blit(self.menu_surf["board_msg"]["4x4_del_board"], restart_window_pos)
            
            elif self.del_res_buff == "5x5":
                screen.blit(self.menu_surf["board_msg"]["5x5_del_board"], restart_window_pos)
            
            # draw yes button
            self.menu_btns["yes_btn"].blitButton(screen)
            # draw no button
            self.menu_btns["no_btn"].blitButton(screen)'''



'''
 # images
        self.game_accs = {
            "game_icon_surf": menu_images["game_icon"],
            "score_surf": menu_images["score_img"],
            "best_score_surf": menu_images["best_score_img"],
        }

        # GUI elements
        self.buttons = {
            "home": hud_game_menu_buttons["home_btn"], # home button
            "restart": hud_game_menu_buttons["new_game_btn"], # restart/new game button
            "undo": hud_game_menu_buttons["undo_btn"], # undo button

            "yes": hud_restart_menu_buttons["yes_btn"], # yes button
            "no": hud_restart_menu_buttons["no_btn"] # no button
        }
'''


### static bin ###

'''
# main menu board previews and mode fonts
board_preview = {
    "3x3": [Image(preview_size[0], preview_size[1])._render_image("img/temp_theme/mainmenu/game_previews/2048_bg_3x3_preview.png", False, True),
            Image(mode_font_size[0], mode_font_size[1])._render_image("img/temp_theme/mainmenu/font/3x3_font.png", False, True)],

    "4x4": [Image(preview_size[0], preview_size[1])._render_image("img/temp_theme/mainmenu/game_previews/2048_bg_4x4_preview.png", False, True),
            Image(mode_font_size[0], mode_font_size[1])._render_image("img/temp_theme/mainmenu/font/4x4_font.png", False, True)],

    "5x5": [Image(preview_size[0], preview_size[1])._render_image("img/temp_theme/mainmenu/game_previews/2048_bg_5x5_preview.png", False, True),
            Image(mode_font_size[0], mode_font_size[1])._render_image("img/temp_theme/mainmenu/font/5x5_font.png", False, True)]
}



# main menu button temp_theme
mm_buttons = {
    "left_slide_btn": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/temp_theme/mainmenu/buttons/left_arrow_button.png", False, True),
    "right_slide_btn": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/temp_theme/mainmenu/buttons/right_arrow_button.png", False, True),
    "start_btn": Image(start_button_size[0], start_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/start_game_button.png", False, True),
    "sett_btn": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/settings_button.png", False, True),
    "exit_btn": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/exit_game_button.png", False, True),

    "left_slide_btn_onHover": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/temp_theme/mainmenu/buttons/left_arrow_button_onHover.png", False, True),
    "right_slide_btn_onHover": Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/temp_theme/mainmenu/buttons/right_arrow_button_onHover.png", False, True),
    "start_btn_onHover": Image(start_button_size[0], start_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/start_game_button_onHover.png", False, True),
    "sett_btn_onHover": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/settings_button_onHover.png", False, True),
    "exit_btn_onHover": Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/temp_theme/mainmenu/buttons/exit_game_button_onHover.png", False, True),
}

# actual hud buttons
hud_buttons = {
    "hud_left_slide_btn": HUDButton(mm_buttons["left_slide_btn"], l_r_slide_btn_pos[0], mm_buttons["left_slide_btn_onHover"]),
    "hud_right_slide_btn": HUDButton(mm_buttons["right_slide_btn"], l_r_slide_btn_pos[1], mm_buttons["right_slide_btn_onHover"]),
    "hud_start_btn": HUDButton(mm_buttons["start_btn"], start_button_pos, mm_buttons["start_btn_onHover"]),
    "hud_sett_btn": HUDButton(mm_buttons["sett_btn"], settings_button_pos, mm_buttons["sett_btn_onHover"]),
    "hud_exit_btn": HUDButton(mm_buttons["exit_btn"], exit_button_pos, mm_buttons["exit_btn_onHover"])
}



menu_images = {
    "game_icon": Image(game_icon_size[0], game_icon_size[1])._render_image("img/temp_theme/in_game/rest/2048_icon.png", False, True),
    "score_img": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/temp_theme/in_game/rest/score.png", False, True),
    "best_score_img": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/temp_theme/in_game/rest/best.png", False, True),
    "game_over_screen": Image(360, 130)._render_image("img/temp_theme/in_game/rest/game_over.png", False, True)
}




# game menu button temp_theme
game_menu_buttons = {
    "home_btn": [Image(home_btn_size[0], home_btn_size[1])._render_image("img/temp_theme/in_game/buttons/home.png", False, True),
                Image(home_btn_size[0], home_btn_size[1])._render_image("img/temp_theme/in_game/buttons/home_onHover.png", False, True)],
    "new_game_btn": [Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/temp_theme/in_game/buttons/new_game.png", False, True),
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/temp_theme/in_game/buttons/new_game_onHover.png", False, True)],
    "undo_btn": [Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/temp_theme/in_game/buttons/undo.png", False, True),
                Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/temp_theme/in_game/buttons/undo_onHover.png", False, True)]
}

hud_game_menu_buttons = {
    "home_btn": HUDButton(game_menu_buttons["home_btn"][0], home_btn_pos, game_menu_buttons["home_btn"][1]),
    "new_game_btn": HUDButton(game_menu_buttons["new_game_btn"][0], new_game_btn_pos, game_menu_buttons["new_game_btn"][1]),
    "undo_btn": HUDButton(game_menu_buttons["undo_btn"][0], undo_btn_pos, game_menu_buttons["undo_btn"][1]),
}



restart_menu_images = {
    "restart_window": Image(restart_window_size[0], restart_window_size[1])._render_image("img/temp_theme/in_game/buttons/restart/restart_window.png", False, True),
    "yes_button": [Image(btn_size[0], btn_size[1])._render_image("img/temp_theme/in_game/buttons/restart/yes_button.png", False, True),
                Image(btn_size[0], btn_size[1])._render_image("img/temp_theme/in_game/buttons/restart/yes_button_onHover.png", False, True)],
    "no_button": [Image(btn_size[0], btn_size[1])._render_image("img/temp_theme/in_game/buttons/restart/no_button.png", False, True),
                Image(btn_size[0], btn_size[1])._render_image("img/temp_theme/in_game/buttons/restart/no_button_onHover.png", False, True)]
}

hud_restart_menu_buttons = {
    "yes_btn": HUDButton(restart_menu_images["yes_button"][0], yes_btn_pos, restart_menu_images["yes_button"][1]),
    "no_btn": HUDButton(restart_menu_images["no_button"][0], no_btn_pos, restart_menu_images["no_button"][1])
}








sett_images = {
    "settings_surf": Image(width, height)._render_image("img/temp_theme/settings_menu/settings_menu_surf.jpg", False, True),
    "settings_reset_surf": Image(reset_menu_size[0], reset_menu_size[1])._render_image("img/temp_theme/settings_menu/sett_reset_menu.png", False, True),
    "back_btn": [Image(back_btn_size[0], back_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/sett_back_button.png", False, True),
                Image(back_btn_size[0], back_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/sett_back_button_onHover.png", False, True)],
    
    "3x3_reset": [Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/3x3_reset_btn.png", False, True),
                Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/3x3_reset_btn_onHover.png", False, True)],
    "4x4_reset": [Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/4x4_reset_btn.png", False, True),
                Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/4x4_reset_btn_onHover.png", False, True)],
    "5x5_reset": [Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/5x5_reset_btn.png", False, True),
                Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/5x5_reset_btn_onHover.png", False, True)],
    "all_reset": [Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/all_reset_btn.png", False, True),
                Image(reset_btn_size[0], reset_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/all_reset_btn_onHover.png", False, True)],
    
    "on_off_btn": [Image(on_off_btn_size[0], on_off_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/on_off_button.png", False, True),
                Image(on_off_btn_size[0], on_off_btn_size[1])._render_image("img/temp_theme/settings_menu/buttons/on_off_button_shifter.png", False, True)],

    "yes_button": [Image(reset_button_yes_no_size[0], reset_button_yes_no_size[1])._render_image("img/temp_theme/settings_menu/buttons/yes_button_reset.png", False, True),
                Image(reset_button_yes_no_size[0], reset_button_yes_no_size[1])._render_image("img/temp_theme/settings_menu/buttons/yes_button_reset_onHover.png", False, True)],
    "no_button": [Image(reset_button_yes_no_size[0], reset_button_yes_no_size[1])._render_image("img/temp_theme/settings_menu/buttons/no_button_reset.png", False, True),
                Image(reset_button_yes_no_size[0], reset_button_yes_no_size[1])._render_image("img/temp_theme/settings_menu/buttons/no_button_reset_onHover.png", False, True)],
    "ok_button": [Image(reset_button_yes_no_size[0]+5, reset_button_yes_no_size[1]+5)._render_image("img/temp_theme/settings_menu/buttons/sett_ok_btn.png", False, True),
                Image(reset_button_yes_no_size[0]+5, reset_button_yes_no_size[1]+5)._render_image("img/temp_theme/settings_menu/buttons/sett_ok_btn_onHover.png", False, True)]
}

sett_hud_buttons = {
        "3x3_reset_btn": HUDButton(sett_images["3x3_reset"][0], reset_board_btn_pos[0], sett_images["3x3_reset"][1]),
        "4x4_reset_btn": HUDButton(sett_images["4x4_reset"][0], reset_board_btn_pos[1], sett_images["4x4_reset"][1]),
        "5x5_reset_btn": HUDButton(sett_images["5x5_reset"][0], reset_board_btn_pos[2], sett_images["5x5_reset"][1]),
        "all_reset_btn": HUDButton(sett_images["all_reset"][0], reset_board_btn_pos[3], sett_images["all_reset"][1]),
}

sett_hud_btns_2 = {
        "yes_btn": HUDButton(sett_images["yes_button"][0], reset_btn_yes_pos, sett_images["yes_button"][1]),
        "no_btn": HUDButton(sett_images["no_button"][0], reset_btn_no_pos, sett_images["no_button"][1]),
        "ok_btn": HUDButton(sett_images["ok_button"][0], ok_btn_pos, sett_images["ok_button"][1]),
        "back_btn": HUDButton(sett_images["back_btn"][0], back_btn_pos, sett_images["back_btn"][1])
}





## temp ##
btn_sz = (60, 30)
toggle_buttons = {
    "toggle_on": Image(btn_sz[0], btn_sz[1]).render_image("img/temp_theme/temp_buttons/on_toggle_button.png", False, True),
    "toggle_on_oh": Image(btn_sz[0], btn_sz[1]).render_image("img/temp_theme/temp_buttons/on_toggle_button_onHover.png", False, True),
    "toggle_off": Image(btn_sz[0], btn_sz[1]).render_image("img/temp_theme/temp_buttons/off_toggle_button.png", False, True),
    "toggle_off_oh": Image(btn_sz[0], btn_sz[1]).render_image("img/temp_theme/temp_buttons/off_toggle_button_onHover.png", False, True)
}



board_kind = {
    "3x3_board": Image(board_size[0], board_size[1])._render_image("img/temp_theme/bg_3x3/2048_bg_3x3.png", False, True),
    "4x4_board": Image(board_size[0], board_size[1])._render_image("img/temp_theme/bg_3x3/2048_bg_4x4.png", False, True),
    "5x5_board": Image(board_size[0], board_size[1])._render_image("img/temp_theme/bg_3x3/2048_bg_5x5.png", False, True)
}



board_tiles = {
    "l_tiles": {
        "2": "img/temp_theme/in_game/tiles_light/2_tile_light.png",
        "4": "img/temp_theme/in_game/tiles_light/4_tile_light.png", 
        "8": "img/temp_theme/in_game/tiles_light/8_tile_light.png",
        "16": "img/temp_theme/in_game/tiles_light/16_tile_light.png",
        "32": "img/temp_theme/in_game/tiles_light/32_tile_light.png",
        "64": "img/temp_theme/in_game/tiles_light/64_tile_light.png",
        "128": "img/temp_theme/in_game/tiles_light/128_tile_light.png",
        "256": "img/temp_theme/in_game/tiles_light/256_tile_light.png",
        "512": "img/temp_theme/in_game/tiles_light/512_tile_light.png",
        "1024": "img/temp_theme/in_game/tiles_light/1024_tile_light.png",
        "2048": "img/temp_theme/in_game/tiles_light/2048_tile_light.png",
        "4096": "img/temp_theme/in_game/tiles_light/4096_tile_light.png",
        "8192": "img/temp_theme/in_game/tiles_light/8192_tile_light.png",
        "16384": "img/temp_theme/in_game/tiles_light/16384_tile_light.png"
    },
    "d_tiles": {

    }
}



def choose_board_img_tiles_and_tile_speed(self):

        # choose board image
        # initialize all tiles with the proper size
        # choose tile movement speed

        if self.dim == 3:
            self.board_img = game_assets[self.theme]["in_game"]["boards"]["3x3_board"]
            self.all_available_tiles = game_assets[self.theme]["in_game"]["tiles"]["3x3_board_tiles"]
            self.move_speed = 34
        elif self.dim == 4:
            self.board_img = game_assets[self.theme]["in_game"]["boards"]["4x4_board"]
            self.all_available_tiles = game_assets[self.theme]["in_game"]["tiles"]["4x4_board_tiles"]
            self.move_speed = 38
        elif self.dim == 5: 
            self.board_img = game_assets[self.theme]["in_game"]["boards"]["5x5_board"]
            self.all_available_tiles = game_assets[self.theme]["in_game"]["tiles"]["5x5_board_tiles"]
            self.move_speed = 45
        else: 
            raise ValueError("Invalid Board Dimension")'''



'''
# reset button class
class ResetButtons:

    def __init__(self):
        
        # GUI elements
        self.buttons = sett_hud_buttons

        self.btn_mode = None
        self.btn_clicked = False
    
    def three_btn_clicked(self):
        return self.states["3x3_clicked"][1]
    
    def four_btn_clicked(self):
        return self.states["4x4_clicked"][1]
    
    def five_btn_clicked(self):
        return self.states["5x5_clicked"][1]

    def all_btn_clicked(self):
        return self.states["all_clicked"][1]  
    
    def draw_buttons(self, screen):
        
        for btn in self.buttons.values():
            btn.blitButton(screen)
    
    def reset_states(self, state=None):

        if state != None:
            if state in self.states:
                for i, key in enumerate(self.states.keys()):
                    if state == key:
                        self.states[state] = [False, False, i]
                        break

            else: raise ValueError("State not known")

        else:
            self.states["3x3_clicked"] = [False, False, 0] 
            self.states["4x4_clicked"] = [False, False, 1]
            self.states["5x5_clicked"] = [False, False, 2]
            self.states["all_clicked"] = [False, False, 3]
    
    def resetMenuVariables(self):

        self.btn_mode = None
        self.btn_clicked = False

    def update_buttons(self, mPos):

        if self.buttons["3x3_reset_btn"].isBtnClicked(mPos):
            self.btn_mode = "3x3"
            self.btn_clicked = True
        
        if self.buttons["4x4_reset_btn"].isBtnClicked(mPos):
            self.btn_mode = "4x4"
            self.btn_clicked = True
        
        if self.buttons["3x3_reset_btn"].isBtnClicked(mPos):
            self.btn_mode = "5x5"
            self.btn_clicked = True
        
        if self.buttons["3x3_reset_btn"].isBtnClicked(mPos):
            self.btn_mode = "every"
            self.btn_clicked = True'''



'''
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
            if callable(load_btn_status):
                res = load_btn_status()
                if isinstance(res, str) and (res == "on" or res == "off"):
                    self.status = load_btn_status()
                else: raise ValueError("Function output is either no string or has incorrect status type!")
            else: raise ValueError("Argmument must be a function!")
        else: self.status = "off" # default button status
    
    def get_button_status(self):
        return self.status
    
    def isButtonActive(self):
        return True if self.status == "on" else False
    
    def resetButtonClickd(self):
        self.btn_clicked = False
    
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

        return self.btn_clicked'''

          
            
def test(ll=None, *args, su=False):

    print(ll)
    print(args)
    print(su)

test(su=True)

a = {"s": 0, "p": 0}
del a["s"]
print(a)