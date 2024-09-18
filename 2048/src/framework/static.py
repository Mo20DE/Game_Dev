import pygame as pg
from framework.utils import Image, HUDButton, ToggleButton, Colors, Sound


################ Main Program Begin ################

width, height, caption, fps = 450, 780, "2048 by MZM", 60

################ Main Program End ################



################ Main Menu Begin ################

# all modes and default mode
#mode = [["3x3", "4x4", "5x5"], 1]

date_time_pos = [140, 34]

preview_pos = [50, 85]
preview_size = [350, 350]

l_r_slide_btn_pos = ([50, 485], [350, 485])
l_r_slide_btn_size = (50, 52)

mode_font_pos = (195, 495)
mode_font_size = (66, 40)

start_button_pos = (135, 590)
start_button_size = [190, 90]

settings_button_pos = (135, 690)
exit_button_pos = (235, 690)
sett_exit_button_size = (90, 46)

################ Main Menu End ################



################ Game Menu Begin ################

# audio
sound_effects = {
    "swipe": Sound("audio/swipe.wav"),
    "merge_1": Sound("audio/merge_1.wav"),
    "merge_2": Sound("audio/merge_2.wav"),
    "merge_3": Sound("audio/merge_3.wav"),

    "click_1": Sound("audio/click_1.wav"),
    "click_2": Sound("audio/click_2.wav")
}

def make_click_sound(click_kind):
    # play a click sound
    sound_effects[click_kind].play()

next_goal_sent = {
    "2048": "Join the numbers and get to the 2048 tile!",
    "4096": "Your next goal is to get to the 4096 tile!",
    "8192": "Your next goal is to reach the 8192 tile!",
    "16384": "Join the numbers to reach the 16384 tile!",
    "32768 ": "Can you get to the 32768 tile? Try it out!",
    "65536": "Not bad! Try to reach the 65536 tile!",
    "131072": "Great job! Try to get to the 131072 tile!",
    "262144": "Fantastic! Now try to get to the 262144 tile!",
    "524288": "You are insane! Can you get any further?",
    "1048576": "What a crazy player you are!" 
}

## GameMenu ##
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

long_restart_btn_pos = (230, 122)
long_restart_btn_size = (105, 42)

# restart menu temp_theme
restart_window_pos = (85, 250)
restart_window_size = (280, 200)

yes_btn_pos = (130, 360)
no_btn_pos = (240, 360)
btn_size = (85, 50)


try_again_btn_pos = (170, 480)
try_again_btn_size = (110, 40)

game_over_surf_pos = (68, 360)
game_over_surf_size = (320, 66)

moves_done_color = {
    "light_theme": Colors.DARKGREY, 
    "dark_theme": Colors.WHITE
}

goal_sent_pos = (40, 185)
goal_sent_sizes = (
    (330, 24),
    (330, 24),
    (330, 24),
    (330, 24)
)

how_to_pos = (25, 630)
how_to_size = (405, 45)

timer_y_pos = {
    3: 370,
    4: 360,
    5: 346,
    6: 336
}

## board ##

# urn for tile genration
urn = [2, 2, 2, 2, 4, 2, 2, 2, 2, 2]

board_pos = (40, 220) # originally (40, 200)
board_size = (370, 370)

# dimension of every tile
tile_dim = {3: 107, 4: 78, 5: 62}
# gap offset of every board
gap_off = {3: 19, 4: 16.1, 5: 13}

align_off = {
    3: [5.2, 13, 19],
    4: [4.5, 7.6, 12.4, 16.49],
    5: [3, 5.2, 8.8, 10.2, 13.2]
}

### in-game constants ###
tile_info = {
    3: [40, "3x3_board", "3x3_board_tiles"], 
    4: [43, "4x4_board", "4x4_board_tiles"], 
    5: [46, "5x5_board", "5x5_board_tiles"]
}

################ Game Menu End ################


################ Algo Menu Begin ################

ai_menu_btn_pos = (165, 690)
ai_menu_btn_size = (120, 55)

step_btn_pos = (205, 660)
step_btn_size = (85, 40)

auto_run_btn_pos = (300, 660)
auto_run_btn_size = (105, 40)

stop_btn_pos = (300, 660)
stop_btn_size = (85, 40)

add_algo_btn_pos = (125, 660)
add_algo_btn_size = (70, 40)

algo_menu_bg_pos = (10, 630)
algo_menu_bg_size = (430, 150)

algo_quit_btn_pos = (14, 635)

toggle_btn_row_pos = (32, 671)

speed_bar_pos = (240, 750)
speed_bar_size = (145, 7)

speed_bar_btn_size = (20, 20)

################ Algo Menu End ################


################ Settings Begin ################

bg_pos = (0, 0)

made_by_pos = (350, 755)
made_by_size = (90, 18)

back_btn_pos = [160, 676]
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

restart_window_pos = (65, 180)
restart_window_size = (320, 230)

statistics_btn_pos = (305, 190)
statistics_btn_size = (110, 45)

reset_stats_btn_pos = (175, 600)
reset_stats_btn_size = (110, 50)

boards_delete_btn_pos = (185, 255)
boards_delete_btn_size = (105, 45)

reset_b_score_btn_pos = (310, 255)
reset_b_score_btn_size = (105, 45)


reset_btns_pos1 = (130, 270)
reset_btns_pos2 = (240, 270)
reset_btns_pos3 = (130, 335)
reset_btns_pos4 = (240, 335)

reset_btns_size = (80, 46)

quit_btn_pos = (70, 186)
quit_btn_size = (18, 18)

toggle_sound_btn_pos = (355, 325)

toggle_undo_btn_pos = (355, 395)

toggle_ai_menu_btn_pos = (355, 465)

toggle_how_to_btn_pos = (355, 535)

toggle_game_theme_btn_pos = (355, 605)

toggle_btn_size = (60, 30)

yes_btn_pos = [130, 335]
no_btn_pos = [240, 335]
ok_btn_pos = [185, 335]

# stats #
stats_bg_clr = {
    "light_theme": (234, 216, 196),
    "dark_theme": (97, 99, 125)
}
com_soon_surf_clr = {
    "light_theme": (210, 165, 83),
    "dark_theme": (48, 83, 139)
}

info_surf_bg_clr = {
    "light_theme": (218, 195, 172),
    "dark_theme": (108, 110, 135)
}

stats_score_x = [390, 378, 368, 356, 344, 332, 320] # digit length: 1-7

info_btn_size = (20, 20)
info_btn_pos = (385, 122)

################ Settings End ################


################ General Constants Begin ################

app_icon_size = (300, 300)

# alpha vars for new game (button)
alpha_surf = pg.Surface((width, height))
alpha_surf.fill(Colors.BLACK)
alpha_val = 180

# alpha vars for try again (button)
alpha_s1 = pg.Surface(board_size)
alpha_s2 = pg.Surface(board_size)
alpha_s1.fill(Colors.LIGHTCREAMYELLOW)
alpha_s2.fill(Colors.LIGHTCREAMBLUE)
alpha_pos2 = board_pos
alpha_val2 = 130

alpha_surfs = {
    "light_theme": alpha_s1,
    "dark_theme": alpha_s2
}


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
    "262144": "/in_game/tiles/262144_tile.png",
    "524288": "/in_game/tiles/524288_tile.png",
    "1048576": "/in_game/tiles/1048576_tile.png"
}

toggle_algo_menu_btns_path = [
    ["img/light_theme/algo_menu/buttons/toggle_btn_off.png",
    "img/light_theme/algo_menu/buttons/toggle_btn_off_onHover.png"],
    ["img/light_theme/algo_menu/buttons/toggle_btn_on.png",
    "img/light_theme/algo_menu/buttons/toggle_btn_on_onHover.png"]
]

toggle_images = [

    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/general/on_toggle_button.png"),
    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/general/off_toggle_button.png"),

    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/general/toggle_light_theme_button.png"),
    Image(toggle_btn_size[0], toggle_btn_size[1])._render_image("img/general/toggle_dark_theme_button.png")
]

toggle_btns = {

    "toggle_sound_btn": ToggleButton(
        toggle_sound_btn_pos,
        toggle_images[0], toggle_images[1]
    ),

    "toggle_undo_btn": ToggleButton(
        toggle_undo_btn_pos,
        toggle_images[0], toggle_images[1]
    ),

    "toggle_ai_menu_btn": ToggleButton(
        toggle_ai_menu_btn_pos,
        toggle_images[0], toggle_images[1]
    ),

    "toggle_how_to_btn": ToggleButton(
        toggle_how_to_btn_pos,
        toggle_images[0], toggle_images[1]
    ),

    "toggle_game_theme_btn": ToggleButton(
        toggle_game_theme_btn_pos,
        toggle_images[2], toggle_images[3]
    )
}

quit_btn = HUDButton(
    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/general/quit_btn.png"),
    algo_quit_btn_pos,
    Image(quit_btn_size[0], quit_btn_size[1])._render_image("img/general/quit_btn_onHover.png")
)

deact_btn_imgs = {
    "home": Image(home_btn_size[0], home_btn_size[1])._render_image("img/general/home_button_deact.png"),
    "new": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/general/new_gm_button_deact.png"),
    "new_long": Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/general/new_game_button_deact.png"),
    "undo": Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/general/undo_button_deact.png"),
    "auto_run": Image(auto_run_btn_size[0], auto_run_btn_size[1])._render_image("img/general/auto_run_btn_deact.png"),
    "step": Image(step_btn_size[0], step_btn_size[1])._render_image("img/general/step_btn_deact.png")
}


################ General Constants End ################


def load_tiles(dim, theme):

    all_available_tiles = {} # all 14 available tiles
    for key, value in zip(tiles_path.keys(), tiles_path.values()):
        first_path = "img/"+theme
        tile_img = Image(tile_dim[dim], tile_dim[dim])._render_image(first_path+value)
        all_available_tiles[key] = tile_img

    return all_available_tiles

def generate_theme_assets(theme):

    theme_assets = {

        "in_game": {

            "boards": {

                "3x3_board": Image(board_size[0], board_size[1])._render_image("img/"+theme+"/in_game/boards/3x3_board.png"),
                "4x4_board": Image(board_size[0], board_size[1])._render_image("img/"+theme+"/in_game/boards/4x4_board.png"),
                "5x5_board": Image(board_size[0], board_size[1])._render_image("img/"+theme+"/in_game/boards/5x5_board.png")
            },

            "tiles": {

                "3x3_board_tiles": load_tiles(3, theme),
                "4x4_board_tiles": load_tiles(4, theme),
                "5x5_board_tiles": load_tiles(5, theme)
            }
        },

        "main_menu": {

            "surfaces": {

                "theme": Image(width, height)._render_image("img/"+theme+"/main_menu/surfaces/"+theme+"_bg.png"),

                "board_previews": {

                    "3x3": Image(preview_size[0], preview_size[1])._render_image("img/"+theme+"/main_menu/surfaces/3x3_preview.png"),
                    "4x4": Image(preview_size[0], preview_size[1])._render_image("img/"+theme+"/main_menu/surfaces/4x4_preview.png"),
                    "5x5": Image(preview_size[0], preview_size[1])._render_image("img/"+theme+"/main_menu/surfaces/5x5_preview.png")
                },

                "board_font": {

                    "3x3": Image(mode_font_size[0], mode_font_size[1])._render_image("img/"+theme+"/main_menu/surfaces/3x3_font.png"),
                    "4x4": Image(mode_font_size[0], mode_font_size[1])._render_image("img/"+theme+"/main_menu/surfaces/4x4_font.png"),
                    "5x5": Image(mode_font_size[0], mode_font_size[1])._render_image("img/"+theme+"/main_menu/surfaces/5x5_font.png")
                }
            },

            "buttons": {
                
                "start_btn": HUDButton(
                    Image(start_button_size[0], start_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/start_button.png"),
                    start_button_pos,
                    Image(start_button_size[0], start_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/start_button_onHover.png")
                ),
                
                "sett_btn": HUDButton(
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/settings_button.png"),
                    settings_button_pos,
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/settings_button_onHover.png")
                ),

                "exit_btn": HUDButton(
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/exit_button.png"),
                    exit_button_pos,
                    Image(sett_exit_button_size[0], sett_exit_button_size[1])._render_image("img/"+theme+"/main_menu/buttons/exit_button_onHover.png")
                ),

                "left_slide_btn": HUDButton(
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/"+theme+"/main_menu/buttons/left_slide_button.png"),
                    l_r_slide_btn_pos[0],
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/"+theme+"/main_menu/buttons/left_slide_button_onHover.png")
                ),
                
                "right_slide_btn": HUDButton(
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/"+theme+"/main_menu/buttons/right_slide_button.png"),
                    l_r_slide_btn_pos[1],
                    Image(l_r_slide_btn_size[0], l_r_slide_btn_size[1])._render_image("img/"+theme+"/main_menu/buttons/right_slide_button_onHover.png")
                ),

                "made_by_btn": HUDButton(
                    Image(made_by_size[0], made_by_size[1])._render_image("img/"+theme+"/main_menu/buttons/made_by.png"),
                    made_by_pos,
                    Image(made_by_size[0], made_by_size[1])._render_image("img/"+theme+"/main_menu/buttons/made_by_onHover.png"),
                    web_link="https://mzm20.itch.io"
                )
            }
        },

        "game_menu": {

            "surfaces": {

                "icon": Image(game_icon_size[0], game_icon_size[1])._render_image("img/"+theme+"/game_menu/surfaces/icon.png"),
                "score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/"+theme+"/game_menu/surfaces/score.png"),
                "best_score_frame": Image(s_b_img_size[0], s_b_img_size[1])._render_image("img/"+theme+"/game_menu/surfaces/best_score.png"),
                "restart_msg_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/game_menu/surfaces/restart_msg_bg.png"),
                "how_to_play": Image(how_to_size[0], how_to_size[1])._render_image("img/"+theme+"/game_menu/surfaces/how_to_play.png"),
            },

            "buttons": {

                "home_btn": HUDButton(
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/home_button.png"),
                    home_btn_pos,
                    Image(home_btn_size[0], home_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/home_button_onHover.png")
                ),

                "new_game_long_btn": HUDButton(
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/new_game_button.png"),
                    long_restart_btn_pos,
                    Image(long_restart_btn_size[0], long_restart_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/new_game_button_onHover.png")
                ),

                "new_game_short_btn": HUDButton(
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/new_gm_button.png"),
                    new_game_btn_pos,
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/new_gm_button_onHover.png")
                ),

                "undo_btn": HUDButton(
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/undo_button.png"),
                    undo_btn_pos,
                    Image(n_u_btn_size[0], n_u_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/undo_button_onHover.png")
                ),

                "try_again_btn": HUDButton(
                    Image(try_again_btn_size[0], try_again_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/try_again_btn.png"),
                    try_again_btn_pos,
                    Image(try_again_btn_size[0], try_again_btn_size[1])._render_image("img/"+theme+"/game_menu/buttons/try_again_btn_onHover.png")
                )
            }
        },

        "algo_menu": {

            "surfaces": {

                "menu_bg": Image(algo_menu_bg_size[0], algo_menu_bg_size[1])._render_image("img/"+theme+"/algo_menu/surfaces/menu_surf.png"),
                "speed_bar": [
                    Image(speed_bar_size[0], speed_bar_size[1])._render_image("img/"+theme+"/algo_menu/surfaces/speed_bar.png"),
                    Image(speed_bar_size[0], speed_bar_size[1])._render_image("img/"+theme+"/algo_menu/surfaces/speed_bar_scroll.png")
                ]
            },

            "buttons": {

                "ai_menu_btn": HUDButton(
                    Image(ai_menu_btn_size[0], ai_menu_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/ai_menu_button.png"),
                    ai_menu_btn_pos,
                    Image(ai_menu_btn_size[0], ai_menu_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/ai_menu_button_onHover.png")
                ),

                "auto_run_btn": HUDButton(
                    Image(auto_run_btn_size[0], auto_run_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/auto_run_btn.png"),
                    auto_run_btn_pos,
                    Image(auto_run_btn_size[0], auto_run_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/auto_run_btn_onHover.png")
                ),

                "stop_btn": HUDButton(
                    Image(stop_btn_size[0], stop_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/stop_btn.png"),
                    stop_btn_pos,
                    Image(stop_btn_size[0], stop_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/stop_btn_onHover.png")
                ), 

                "add_algo_btn": HUDButton(
                    Image(add_algo_btn_size[0], add_algo_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/add_algo_btn.png"),
                    add_algo_btn_pos,
                    Image(add_algo_btn_size[0], add_algo_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/add_algo_btn_onHover.png")
                ), 

                "step_btn": HUDButton(
                    Image(step_btn_size[0], step_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/step_btn.png"),
                    step_btn_pos,
                    Image(step_btn_size[0], step_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/step_btn_onHover.png")
                ),

                "speed_bar_btn": [
                    Image(speed_bar_btn_size[0], speed_bar_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/speed_bar_btn.png"),
                    Image(speed_bar_btn_size[0], speed_bar_btn_size[1])._render_image("img/"+theme+"/algo_menu/buttons/speed_bar_btn_onHover.png")
                ],
            }
        },

        "settings": {

            "surfaces": {

                "delete_board_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/delete_b_data_bg.png"),

                # backgrounds (board question and notification)
                "3x3_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/3x3_b_msg_bg.png"),
                "4x4_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/4x4_b_msg_bg.png"),
                "5x5_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/5x5_b_msg_bg.png"),
                "all_board_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/every_b_msg_bg.png"),

                "3x3_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/3x3_not_msg_bg.png"),
                "4x4_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/4x4_not_msg_bg.png"),
                "5x5_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/5x5_not_msg_bg.png"),
                "all_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/board_messages/every_not_msg_bg.png"),


                "reset_b_sc_bg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/reset_b_sc_bg.png"),

                # backgrounds (best score question and notification)
                "3x3_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/3x3_b_sc_msg_bg.png"),
                "4x4_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/4x4_b_sc_msg_bg.png"),
                "5x5_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/5x5_b_sc_msg_bg.png"),
                "all_b_sc_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/every_b_sc_msg_bg.png"),

                "3x3_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/3x3_not_msg_bg.png"),
                "4x4_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/4x4_not_msg_bg.png"),
                "5x5_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/5x5_not_msg_bg.png"),
                "all_b_sc_not_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/best_score_messages/every_not_msg_bg.png"),

                "sett_bg": Image(width, height)._render_image("img/"+theme+"/settings/surfaces/sett_menu_bg.png"),

                "stats_bg": Image(width, height)._render_image("img/"+theme+"/settings/surfaces/stats_bg.png"),
                "reset_stats_msg": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/reset_stats_msg_bg.png"),
                "reset_not_possible": Image(restart_window_size[0], restart_window_size[1])._render_image("img/"+theme+"/settings/surfaces/reset_not_possible.png"),
            },

            "buttons": {

                "stats_btn": HUDButton(
                    Image(statistics_btn_size[0], statistics_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/stats_button.png"),
                    statistics_btn_pos,
                    Image(statistics_btn_size[0], statistics_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/stats_button_onHover.png")
                ),

                "boards_delete_btn": HUDButton(
                    Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_boards_button.png"),
                    boards_delete_btn_pos,
                    Image(boards_delete_btn_size[0], boards_delete_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_boards_button_onHover.png")
                ),

                "best_score_reset_btn": HUDButton(
                    Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_b_sc_button.png"),
                    reset_b_score_btn_pos,
                    Image(reset_b_score_btn_size[0], reset_b_score_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_b_sc_button_onHover.png")
                ),

                "3x3_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/3x3_reset_button.png"),
                    reset_btns_pos1,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/3x3_reset_button_onHover.png")
                ),

                "4x4_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/4x4_reset_button.png"),
                    reset_btns_pos2,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/4x4_reset_button_onHover.png")
                ),

                "5x5_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/5x5_reset_button.png"),
                    reset_btns_pos3,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/5x5_reset_button_onHover.png")
                ),

                "all_reset_btn": HUDButton(
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/all_reset_button.png"),
                    reset_btns_pos4,
                    Image(reset_btns_size[0], reset_btns_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/all_reset_button_onHover.png")
                ),

                "yes_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/yes_button.png"),
                    yes_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/yes_button_onHover.png")
                ),

                "no_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/no_button.png"),
                    no_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/no_button_onHover.png")
                ),

                "ok_btn": HUDButton(
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/ok_button.png"),
                    ok_btn_pos,
                    Image(btn_size[0], btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/ok_button_onHover.png")
                ),

                "back_home_btn": HUDButton(
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/back_button.png"),
                    back_btn_pos,
                    Image(back_btn_size[0], back_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/back_button_onHover.png")
                ),

                "reset_stats_btn": HUDButton(
                    Image(reset_stats_btn_size[0], reset_stats_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_stats_button.png"),
                    reset_stats_btn_pos,
                    Image(reset_stats_btn_size[0], reset_stats_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/reset_stats_button_onHover.png")
                ),

                "info_stats_btn": HUDButton(
                    Image(info_btn_size[0], info_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/info_btn.png"),
                    info_btn_size,
                    Image(info_btn_size[0], info_btn_size[1])._render_image("img/"+theme+"/settings/buttons/menu_buttons/info_btn_onHover.png")
                )
            }
        }
    }

    return theme_assets


############ all surfaces ############

game_assets = {

    # light game theme properties
    "light_theme": generate_theme_assets("light_theme"),
    "dark_theme": generate_theme_assets("dark_theme")
}

