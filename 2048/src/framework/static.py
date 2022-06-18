import pygame as pg
from framework.utils import Image, HUDButton, ToggleButton, Colors


width, height, caption, fps = 450, 750, "2048", 60

# start tiles
urn = [2, 2, 2, 2, 2, 2, 2, 2, 4, 4]

### main menu temp_theme ###

# all modes and default mode
mode = [["3x3", "4x4", "5x5"], 1]

preview_pos = (50, 40)
preview_size = (350, 350)

l_r_slide_btn_pos = ([50, 450], [350, 450])
l_r_slide_btn_size = (50, 52)

mode_font_pos = (195, 460)
mode_font_size = (66, 40)

start_button_pos = (135, 570)
start_button_size = [190, 90]

settings_button_pos = (135, 670)
exit_button_pos = (235, 670)
sett_exit_button_size = (90, 46)





### in-game temp_theme ###
game_icon_pos = (40, 40)
game_icon_size = (100, 100)

score_img_pos = (162, 40)
best_score_img_pos = (295, 40)
s_b_img_size = (110, 65)



score_x_pos = {1: 210, 2: 202, 3: 195, 4: 190, 5: 182, 6: 176}
best_score_x_pos = {1: 343, 2: 335, 3: 328, 4: 323, 5: 315, 6: 309}


# in-game buttons
home_btn_pos = (162, 122)
home_btn_size = (42, 42)

new_game_btn_pos = (225, 122)
undo_btn_pos = (325, 122)

n_u_btn_size = (82, 42)



# restart menu temp_theme
restart_window_pos = (85, 250)
restart_window_size = (280, 200)

yes_btn_pos = (130, 360)
no_btn_pos = (240, 360)
btn_size = (85, 50)


# image of every board size
board_pos = (40, 220) # originally (40, 200)
board_size = (370, 370)

# dimension of every tile
tile_dim = {3: 104, 4: 78, 5: 62}
# gap offset of every board
gap_off = {3: 20, 4: 16, 5: 13}

align_off = {
    3: {
        "x": [3.4, 9.4, 14.5],
        "y": [3.4, 8.5, 14.5]
    },
    4: {
        "x": [4, 7.2, 13, 16.2],
        "y": [5, 7.6, 13.2, 17.6]
    },
    5: {
        "x": [3, 5.2, 8.8, 10.2, 13.2],
        "y": [3, 5, 9, 9.2, 13.2]
    }
}


### in-game contants ###
tile_info = {
    3: [28, "3x3_board", "3x3_board_tiles"], 
    4: [32, "4x4_board", "4x4_board_tiles"], 
    5: [40, "5x5_board", "5x5_board_tiles"]}

moves_done_color = {"light_theme": Colors.DARKGREY, "dark_theme": Colors.WHITE}


alpha_surf = pg.Surface((width, height))
alpha_surf.fill(Colors.BLACK)
alpha_buffer = None


## settings menu ##

back_btn_pos = [160, 645]
back_btn_size = (140, 64)

reset_board_btn_pos = [[90, 380], [160, 380], [230, 380], [300, 380]]

reset_btn_size = (62, 40)

on_off_btn_pos = [30, 30]
on_off_btn_size = (60, 40)

reset_menu_pos = [restart_window_pos[0], restart_window_pos[1]-10]
reset_menu_size = (restart_window_size[0]+40, restart_window_size[1]+40)

reset_button_yes_no_size = btn_size
reset_btn_yes_pos = [120, 394]
reset_btn_no_pos = [250, 394]
ok_btn_pos = [185, 394]


## setings menu ##



restart_window_pos = (65, 180)
restart_window_size = (320, 230)

made_by = (100, 15)

boards_delete_btn_pos = (180, 185)
boards_delete_btn_size = (110, 50)

reset_b_score_btn_pos = (310, 185)
reset_b_score_btn_size = (110, 50)


reset_btns_pos1 = (130, 270)
reset_btns_pos2 = (240, 270)
reset_btns_pos3 = (130, 335)
reset_btns_pos4 = (240, 335)

reset_btns_size = (80, 46)

quit_btn_pos = (72, 188)
quit_btn_size = (16, 16)

toggle_sound_btn_pos = (340, 270)

toggle_undo_btn_pos = (340, 340)
toggle_ai_menu_btn_pos = (340, 410)

toggle_how_to_btn_pos = (340, 480)

toggle_game_theme_btn_pos = (340, 550)

toggle_btn_size = (60, 30)

yes_btn_pos = [130, 335]
no_btn_pos = [240, 335]
ok_btn_pos = [185, 335]

app_icon_size = (300, 300)

long_restart_btn_pos = (230, 122)
long_restart_btn_size = (115, 42)

tiles_path = {

    "2": "/in_game/tiles/2_tile.png",
    "4": "/in_game/tiles/4_tile.png", 
    "8": "/in_game/tiles/8_tile.png",
    "16": "/in_game/tiles/16_tile.png",
    "32": "/in_game/tiles/32_tile.png",
    "64": "/in_game/tiles/64_tile.png",
    "128": "/in_game/tiles/128_tile.png",
    "256": "/in_game/tiles/256_tile.png",
    "512": "/in_game/tiles/512_tile.png",
    "1024": "/in_game/tiles/1024_tile.png",
    "2048": "/in_game/tiles/2048_tile.png",
    "4096": "/in_game/tiles/4096_tile.png",
    "8192": "/in_game/tiles/8192_tile.png",
    "16384": "/in_game/tiles/16384_tile.png",
    "32768": "/in_game/tiles/32768_tile.png",
    "65536": "/in_game/tiles/65536_tile.png",
    "131072": "/in_game/tiles/131072_tile.png",
    "262144": "/in_game/tiles/262144_tile.png"
}

def load_tiles(dim, theme):

    all_available_tiles = {} # all 14 available tiles
    for key, value in zip(tiles_path.keys(), tiles_path.values()):
        first_path = "img/"+theme
        tile_img = Image(tile_dim[dim], tile_dim[dim])._render_image(first_path+value, False, True)
        all_available_tiles[key] = tile_img

    return all_available_tiles


############ every game surface/image/button ############


game_assets = {

    # light game theme properties
    "light_theme": {

        "in_game": {

            "boards": {

                "3x3_board": Image(board_size[0], board_size[1])._render_image("img/light_theme/in_game/boards/3x3_board.png", False, True),
                "4x4_board": Image(board_size[0], board_size[1])._render_image("img/light_theme/in_game/boards/4x4_board.png", False, True),
                "5x5_board": Image(board_size[0], board_size[1])._render_image("img/light_theme/in_game/boards/5x5_board.png", False, True)
            },

            "tiles": {

                "3x3_board_tiles": load_tiles(3, "light_theme"),
                "4x4_board_tiles": load_tiles(4, "light_theme"),
                "5x5_board_tiles": load_tiles(5, "light_theme")
            }
        },

        "main_menu": {

            "surfaces": {

                "theme": Image(width, height)._render_image("img/light_theme/main_menu/surfaces/light_theme_bg.png", False, True),

                "board_previews": {

                    "3x3": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/3x3_preview.png", False, True),
                    "4x4": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/4x4_preview.png", False, True),
                    "5x5": Image(preview_size[0], preview_size[1])._render_image("img/light_theme/main_menu/surfaces/5x5_preview.png", False, True)
                },

                "board_font": {

                    "3x3": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/3x3_font.png", False, True),
                    "4x4": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/4x4_font.png", False, True),
                    "5x5": Image(mode_font_size[0], mode_font_size[1])._render_image("img/light_theme/main_menu/surfaces/5x5_font.png", False, True)
                }
            },

            "buttons": {
                
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
            }
        },

        "game_menu": {

            "surfaces": {

                "icon": Image(game_icon_size[0], game_icon_size[1])._render_image("img/light_theme/game_menu/surfaces/icon.png", False, True),
                "score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/light_theme/game_menu/surfaces/score.png", False, True),
                "best_score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/light_theme/game_menu/surfaces/best_score.png", False, True),
                "restart_msg_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/game_menu/surfaces/restart_msg_bg.png", False, True),
                "game_over_screen": Image(360, 130)._render_image("img/light_theme/game_menu/surfaces/game_over.png", False, True)
            },

            "buttons": {

                "home_btn": HUDButton(
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button.png", False, True),
                    home_btn_pos,
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/light_theme/game_menu/buttons/home_button_onHover.png", False, True)
                ),

                "new_game_long_btn": HUDButton(
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button.png", False, True),
                    long_restart_btn_pos,
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/light_theme/game_menu/buttons/new_game_button_onHover.png", False, True)
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
            }
        },

        "settings": {

            "surfaces": {

                "delete_board_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/delete_b_data_bg.png", False, True),

                # backgrounds (board question and notification)
                "3x3_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/3x3_b_msg_bg.png", False, True),
                "4x4_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/4x4_b_msg_bg.png", False, True),
                "5x5_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/5x5_b_msg_bg.png", False, True),
                "all_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/every_b_msg_bg.png", False, True),

                "3x3_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/3x3_not_msg_bg.png", False, True),
                "4x4_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/4x4_not_msg_bg.png", False, True),
                "5x5_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/5x5_not_msg_bg.png", False, True),
                "all_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/board_messages/every_not_msg_bg.png", False, True),


                "reset_b_sc_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/reset_b_sc_bg.png", False, True),

                # backgrounds (best score question and notification)
                "3x3_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/3x3_b_sc_msg_bg.png", False, True),
                "4x4_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/4x4_b_sc_msg_bg.png", False, True),
                "5x5_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/5x5_b_sc_msg_bg.png", False, True),
                "all_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/every_b_sc_msg_bg.png", False, True),

                "3x3_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/3x3_not_msg_bg.png", False, True),
                "4x4_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/4x4_not_msg_bg.png", False, True),
                "5x5_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/5x5_not_msg_bg.png", False, True),
                "all_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/light_theme/settings/surfaces/best_score_messages/every_not_msg_bg.png", False, True),

                "sett_bg": Image(width, height)._render_image("img/light_theme/settings/surfaces/sett_menu_bg.png", False, True),
                "made_by": Image(made_by[0], made_by[1])._render_image("img/light_theme/settings/surfaces/made_by.png", False, True)
            },

            "buttons": {

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
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/yes_button.png", False, True),
                    yes_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/yes_button_onHover.png", False, True)
                ),

                "no_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/no_button.png", False, True),
                    no_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/no_button_onHover.png", False, True)
                ),

                "ok_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/ok_button.png", False, True),
                    ok_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/ok_button_onHover.png", False, True)
                ),

                "back_home_btn": HUDButton(
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/back_button.png", False, True),
                    back_btn_pos,
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/back_button_onHover.png", False, True)
                ),

                "quit_btn": HUDButton(
                    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/quit_btn.png", False, True),
                    quit_btn_pos,
                    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/quit_btn_onHover.png", False, True)
                ),

                "toggle_sound_btn": ToggleButton(
                    toggle_sound_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_undo_btn": ToggleButton(
                    toggle_undo_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_ai_menu_btn": ToggleButton(
                    toggle_ai_menu_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_how_to_btn": ToggleButton(
                    toggle_how_to_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_game_theme_btn": ToggleButton(
                    toggle_game_theme_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_light_theme_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_dark_theme_button.png", False, True)
                )
            }
        }

    },


    # dark game theme properties
    "dark_theme": {

        "in_game": {

            "boards": {

                "3x3_board": Image(board_size[0], board_size[1])._render_image("img/dark_theme/in_game/boards/3x3_board.png", False, True),
                "4x4_board": Image(board_size[0], board_size[1])._render_image("img/dark_theme/in_game/boards/4x4_board.png", False, True),
                "5x5_board": Image(board_size[0], board_size[1])._render_image("img/dark_theme/in_game/boards/5x5_board.png", False, True)
            },

            "tiles": {

                "3x3_board_tiles": load_tiles(3, "dark_theme"),
                "4x4_board_tiles": load_tiles(4, "dark_theme"),
                "5x5_board_tiles": load_tiles(5, "dark_theme")
            }
        },

        "main_menu": {

            "surfaces": {

                "theme": Image(width, height)._render_image("img/dark_theme/main_menu/surfaces/dark_theme_bg.png", False, True),

                "board_previews": {

                    "3x3": Image(preview_size[0], preview_size[1])._render_image("img/dark_theme/main_menu/surfaces/3x3_preview.png", False, True),
                    "4x4": Image(preview_size[0], preview_size[1])._render_image("img/dark_theme/main_menu/surfaces/4x4_preview.png", False, True),
                    "5x5": Image(preview_size[0], preview_size[1])._render_image("img/dark_theme/main_menu/surfaces/5x5_preview.png", False, True)
                },

                "board_font": {

                    "3x3": Image(mode_font_size[0], mode_font_size[1])._render_image("img/dark_theme/main_menu/surfaces/3x3_font.png", False, True),
                    "4x4": Image(mode_font_size[0], mode_font_size[1])._render_image("img/dark_theme/main_menu/surfaces/4x4_font.png", False, True),
                    "5x5": Image(mode_font_size[0], mode_font_size[1])._render_image("img/dark_theme/main_menu/surfaces/5x5_font.png", False, True)
                }
            },

            "buttons": {
                
                "start_btn": HUDButton(
                    Image(start_button_size[0], start_button_size[1])._render_image("img/dark_theme/main_menu/buttons/start_button.png", False, True),
                    start_button_pos,
                    Image(start_button_size[0], start_button_size[1])._render_image("img/dark_theme/main_menu/buttons/start_button_onHover.png", False, True)
                ),
                
                "sett_btn": HUDButton(
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/dark_theme/main_menu/buttons/settings_button.png", False, True),
                    settings_button_pos,
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/dark_theme/main_menu/buttons/settings_button_onHover.png", False, True)
                ),

                "exit_btn": HUDButton(
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/dark_theme/main_menu/buttons/exit_button.png", False, True),
                    exit_button_pos,
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/dark_theme/main_menu/buttons/exit_button_onHover.png", False, True)
                ),

                "left_slide_btn": HUDButton(
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/dark_theme/main_menu/buttons/left_slide_button.png", False, True),
                    l_r_slide_btn_pos[0],
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/dark_theme/main_menu/buttons/left_slide_button_onHover.png", False, True)
                ),
                
                "right_slide_btn": HUDButton(
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/dark_theme/main_menu/buttons/right_slide_button.png", False, True),
                    l_r_slide_btn_pos[1],
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/dark_theme/main_menu/buttons/right_slide_button_onHover.png", False, True)
                )
            }
        },

        "game_menu": {

            "surfaces": {

                "icon": Image(game_icon_size[0], game_icon_size[1])._render_image("img/dark_theme/game_menu/surfaces/icon.png", False, True),
                "score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/dark_theme/game_menu/surfaces/score.png", False, True),
                "best_score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/dark_theme/game_menu/surfaces/best_score.png", False, True),
                "restart_msg_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/game_menu/surfaces/restart_msg_bg.png", False, True),
                "game_over_screen": Image(360, 130)._render_image("img/light_theme/game_menu/surfaces/game_over.png", False, True)
            },

            "buttons": {

                "home_btn": HUDButton(
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/home_button.png", False, True),
                    home_btn_pos,
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/home_button_onHover.png", False, True)
                ),

                "new_game_long_btn": HUDButton(
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/new_game_button.png", False, True),
                    long_restart_btn_pos,
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/new_game_button_onHover.png", False, True)
                ),

                "new_game_short_btn": HUDButton(
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/new_gm_button.png", False, True),
                    new_game_btn_pos,
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/new_gm_button_onHover.png", False, True)
                ),

                "undo_btn": HUDButton(
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/undo_button.png", False, True),
                    undo_btn_pos,
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/dark_theme/game_menu/buttons/undo_button_onHover.png", False, True)
                )
            }
        },

        "settings": {

            "surfaces": {

                "delete_board_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/delete_b_data_bg.png", False, True),
                # backgrounds (board question and notification)
                "3x3_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/3x3_b_msg_bg.png", False, True),
                "4x4_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/4x4_b_msg_bg.png", False, True),
                "5x5_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/5x5_b_msg_bg.png", False, True),
                "all_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/every_b_msg_bg.png", False, True),

                "3x3_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/3x3_not_msg_bg.png", False, True),
                "4x4_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/4x4_not_msg_bg.png", False, True),
                "5x5_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/5x5_not_msg_bg.png", False, True),
                "all_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/board_messages/every_not_msg_bg.png", False, True),


                "reset_b_sc_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/reset_b_sc_bg.png", False, True),
                # backgrounds (best score question and notification)
                "3x3_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/3x3_b_sc_msg_bg.png", False, True),
                "4x4_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/4x4_b_sc_msg_bg.png", False, True),
                "5x5_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/5x5_b_sc_msg_bg.png", False, True),
                "all_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/every_b_sc_msg_bg.png", False, True),

                "3x3_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/3x3_not_msg_bg.png", False, True),
                "4x4_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/4x4_not_msg_bg.png", False, True),
                "5x5_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/5x5_not_msg_bg.png", False, True),
                "all_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/dark_theme/settings/surfaces/best_score_messages/every_not_msg_bg.png", False, True),

                "sett_bg": Image(width, height)._render_image("img/dark_theme/settings/surfaces/sett_menu_bg.png", False, True),
                "made_by": Image(made_by[0], made_by[1])._render_image("img/dark_theme/settings/surfaces/made_by.png", False, True)
            },

            "buttons": {

                "boards_delete_btn": HUDButton(
                    Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/reset_boards_button.png", False, True),
                    boards_delete_btn_pos,
                    Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/reset_boards_button_onHover.png", False, True)
                ),

                "best_score_reset_btn": HUDButton(
                    Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/reset_b_sc_button.png", False, True),
                    reset_b_score_btn_pos,
                    Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/reset_b_sc_button_onHover.png", False, True)
                ),

                "3x3_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/3x3_reset_button.png", False, True),
                    reset_btns_pos1,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/3x3_reset_button_onHover.png", False, True)
                ),

                "4x4_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/4x4_reset_button.png", False, True),
                    reset_btns_pos2,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/4x4_reset_button_onHover.png", False, True)
                ),

                "5x5_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/5x5_reset_button.png", False, True),
                    reset_btns_pos3,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/5x5_reset_button_onHover.png", False, True)
                ),

                "all_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/all_reset_button.png", False, True),
                    reset_btns_pos4,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/all_reset_button_onHover.png", False, True)
                ),

                "yes_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/yes_button.png", False, True),
                    yes_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/yes_button_onHover.png", False, True)
                ),

                "no_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/no_button.png", False, True),
                    no_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/no_button_onHover.png", False, True)
                ),

                "ok_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/ok_button.png", False, True),
                    ok_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/ok_button_onHover.png", False, True)
                ),

                "back_home_btn": HUDButton(
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/back_button.png", False, True),
                    back_btn_pos,
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/dark_theme/settings/buttons/menu_buttons/back_button_onHover.png", False, True)
                ),

                "quit_btn": HUDButton(
                    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/quit_btn.png", False, True),
                    quit_btn_pos,
                    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/light_theme/settings/buttons/menu_buttons/quit_btn_onHover.png", False, True)
                ),

                "toggle_sound_btn": ToggleButton(
                    toggle_sound_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_undo_btn": ToggleButton(
                    toggle_undo_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_ai_menu_btn": ToggleButton(
                    toggle_ai_menu_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_how_to_btn": ToggleButton(
                    toggle_how_to_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_on_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_off_button.png", False, True)
                ),

                "toggle_game_theme_btn": ToggleButton(
                    toggle_game_theme_btn_pos,
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_light_theme_button.png", False, True),
                    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/light_theme/settings/buttons/toggle_buttons/toggle_dark_theme_button.png", False, True)
                )
            }
        }

    },
}





'''# menu for algorithms
algo_menu_size = (450, 400)
algo_menu_pos = [[0, height-32], [0, height-algo_menu_size[1]]]

caption_size = (290, 70)
caption_pos = [80, 385]

algo_menu = {
    "unfolded": HUDButton(Image(algo_menu_size[0], algo_menu_size[1])._render_image("img/temp_theme/in_game/algo_menu/algo_menu_surf_1.png", False, True), algo_menu_pos[0]),
    "collapsed": HUDButton(Image(algo_menu_size[0], algo_menu_size[1])._render_image("img/temp_theme/in_game/algo_menu/algo_menu_surf_2.png", False, True), algo_menu_pos[1]),
    "caption": Image(caption_size[0], caption_size[1])._render_image("img/temp_theme/in_game/algo_menu/algo_menu_caption.png", False, True)
}

algo_menu_btn_size = (220, 65)

nn_btn_pos = [115, 470]
exp_btn_pos = [115, 535]
greedy_btn_pos = [115, 600]
random_btn_pos = [115, 665]

algo_btn_images = [
    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/neural_network_btn.png", False, True),
    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/neural_network_btn_onHover.png", False, True),

    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/expectimax_btn.png", False, True),
    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/expectimax_btn_onHover.png", False, True),

    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/greedy_btn.png", False, True),
    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/greedy_btn_onHover.png", False, True),

    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/random_btn.png", False, True),
    Image(algo_menu_btn_size[0], algo_menu_btn_size[1])._render_image("img/temp_theme/in_game/algo_menu/buttons/random_btn_onHover.png", False, True),
]

algo_menu_buttons = {
    "nn_btn": HUDButton(algo_btn_images[0], nn_btn_pos, algo_btn_images[1]),
    "exp_btn": HUDButton(algo_btn_images[2], exp_btn_pos, algo_btn_images[3]),
    "greedy_btn": HUDButton(algo_btn_images[4], greedy_btn_pos, algo_btn_images[5]),
    "random_btn": HUDButton(algo_btn_images[6], random_btn_pos, algo_btn_images[7]),
}'''
