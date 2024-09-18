from framework.utils import *
from framework.static import *

from framework.helper import load_stats
from pygame import MOUSEWHEEL

'''if self.rerender_stats_page: 
    render_stats_page()
    self.rerender_stats_page = False'''

class Statistics:

    def __init__(self, settM):
        
        self.settM = settM
        self.init_properties()
        self.load_variables()
    
    def init_properties(self):

        self.opt_type = None
        self.stats_changed = False
        theme = self.settM.mainM.game_ent.sett_vars["theme"]

        # scroll page with stats
        self.scrollPage = ScrollPage(
            [0, 140], # position
            self.settM.mainM.game_ent.stats[0], # size
            page_clr=stats_bg_clr[theme], scroller_theme=theme # color, theme
        )
        # stats description
        self.info_surf = Surface((55, 130), (340, 520), 
            clr_or_path_or_surf=info_surf_bg_clr[theme], roundness=15)
        
        # render stats onto page
        self.render_stats_page()
        
    def load_variables(self, changePageTheme=False):

        theme = self.settM.mainM.game_ent.sett_vars["theme"]

        self.bg = game_assets[theme]["settings"]["surfaces"]["stats_bg"]
        self.reset_msg =  game_assets[theme]["settings"]["surfaces"]["reset_stats_msg"]
        self.reset_not_poss = game_assets[theme]["settings"]["surfaces"]["reset_not_possible"]

        self.info_stats_btn = game_assets[theme]["settings"]["buttons"]["info_stats_btn"]
        self.reset_stats_btn = game_assets[theme]["settings"]["buttons"]["reset_stats_btn"]

        # scroll page with stats
        if changePageTheme:
            self.scrollPage.changeTextColor(moves_done_color[theme])
            self.scrollPage.changePageColor(stats_bg_clr[theme])
            self.scrollPage.changeScrollerTheme((width, height))
            self.info_surf.set_color(info_surf_bg_clr[theme])

    def render_stats_page(self):

        theme = self.settM.mainM.game_ent.sett_vars["theme"]
        self.scrollPage.reset_page("content")
        self.scrollPage.text_buffer.clear()

        # add stats to page
        for dic in self.settM.mainM.game_ent.stats[1].values(): # 3x3, 4x4, 5x5
            for text, data in zip(dic.keys(), dic.values()):
                # render title: All Play - 3x3, Best Score, 128
                self.scrollPage.add_text(
                    Text(data["x"], data["y"], text,
                    data["font"], data["f_size"], 
                    moves_done_color[theme], bold=data["bold"])
                )
                # render non-tile stats
                if len(data) == 6:
                    self.scrollPage.add_text(
                        Text(stats_score_x[len(str(data["score"]))-1], data["y"], data["score"],
                        data["font"], data["f_size"], 
                        moves_done_color[theme])
                    )
                elif len(data) > 6:
                    for key in ["Games Reached", "Shortest Time", "Fewest Moves"]:
                        self.scrollPage.add_text(
                            Text(data[key]["x"], data[key]["y"], key,
                            data[key]["font"], data[key]["f_size"],
                            moves_done_color[theme])
                        )
                        self.scrollPage.add_text(
                            Text(stats_score_x[len(str(data[key]["score"]))-1], data[key]["y"], data[key]["score"],
                            data[key]["font"], data[key]["f_size"], 
                            moves_done_color[theme])
                        )
    
    def checkAndUpdateStats(self):

        temp = self.settM.gameM
        mode = temp.game_ent.mode
        bd = temp.game_ent.boards[mode]

        # if temp.board_changed and not bd.ai_used:
        if temp.board_changed: 

            best_score = temp.game_ent.bestscores[mode]
            stats = temp.game_ent.stats[1]
            # GENERAL STATS

            # best score
            if best_score > stats[mode]["Best Score"]["score"]:
                self.settM.gameM.game_ent.stats[1][mode]["Best Score"]["score"] = best_score
            # total score
            if bd.old_score > 0:
                self.settM.gameM.game_ent.stats[1][mode]["Total Score"]["score"] += bd.old_score
                self.settM.gameM.game_ent.boards[mode].old_score = 0
                self.stats_changed = True
            # top tile
            max_tile = int(bd.board.flatten().max())
            if max_tile >= 8 and max_tile > stats[mode]["Top Tile"]["score"]:
                self.settM.gameM.game_ent.stats[1][mode]["Top Tile"]["score"] = max_tile
                self.stats_changed = True
            
            # REACHED TILES
            if max_tile >= 128:
                time = temp.game_ent.board_timers[mode]
                moves = bd.moves_done
                tile = str(max_tile)

                if tile not in stats[mode].keys():
                    # insert new stats for max tile
                    last_elem = list(stats[mode].values())[-1]
                    last_y_pos = (last_elem["y"] if len(last_elem) == 6 
                        else last_elem["Fewest Moves"]["y"])
                    #last_y_pos = list(stats[mode].values())[-1]["y"]
                    self.settM.gameM.game_ent.stats[1][mode][tile] = {
                        "x": 40, "y": last_y_pos+60, 
                        "font": "Arial", "f_size": 22, "bold": True,
                        "Games Reached": {
                            "score": 1, "x":40, "y":last_y_pos+100, 
                            "font":"Arial", "f_size":22, "bold":False
                        },
                        "Shortest Time": {
                            "score": time, "x": 40, "y": last_y_pos+140, 
                            "font": "Arial", "f_size": 22, "bold": False
                        },
                        "Fewest Moves": {
                            "score": moves, "x": 40, "y": last_y_pos+180, 
                            "font": "Arial", "f_size": 22, "bold": False
                        }
                    }

                    # update all y positions of stats below
                    last_y_pos += 180
                    if mode != "5x5":
                        next_modes = (["4x4", "5x5"] if mode == "3x3" else ["5x5"])
                        for next_mode in next_modes:
                            last_y_pos += 60
                            for key in stats[next_mode].keys():
                                self.settM.gameM.game_ent.stats[1][next_mode][key]["y"] = last_y_pos
                                if key.isdigit():
                                    self.settM.gameM.game_ent.stats[1][next_mode][key]["Games Reached"]["y"] += 40
                                    self.settM.gameM.game_ent.stats[1][next_mode][key]["Shortest Time"]["y"] += 40
                                    self.settM.gameM.game_ent.stats[1][next_mode][key]["Fewest Moves"]["y"] += 40
                                    last_y_pos += 80
                                last_y_pos += 40
                    self.scrollPage.extendPage(180)
                else:
                    self.settM.gameM.game_ent.stats[1][mode][tile]["Games Reached"]["score"] += 1
                    if time < stats[mode][tile]["Shortest Time"]["score"]:
                        self.settM.gameM.game_ent.stats[1][mode][tile]["Shortest Time"]["score"] = time
                    if moves < stats[mode][tile]["Fewest Moves"]["score"]:
                        self.settM.gameM.game_ent.stats[1][mode][tile]["Fewest Moves"]["score"] = moves

    def handlePageScrolling(self, event):
        
        if self.settM.menu_surf_states["show_stats"] and self.opt_type is None:
            if event.type == MOUSEWHEEL: self.scrollPage.mouseWheelEvent(event, pg_off=6)
    
    def can_reset_stats(self):

        score, counter = 0, 0
        stats = self.settM.mainM.game_ent.stats
        for dic in stats[1].values():
            counter += len(dic.values())
            for i in range(1, 4):
                score += list(dic.values())[i]["score"]

        return score > 0 or counter > 12

    def reset_stats(self):

        self.settM.mainM.game_ent.stats = load_stats()
        self.scrollPage.reset_page(reset_opt="all")
        self.render_stats_page()
        self.opt_type = None

    def checkNewStats(self, data):

        # if not board.ai_used:
        board = data[0]
        mode = self.settM.gameM.game_ent.mode
        stats = self.settM.mainM.game_ent.stats[1][mode]
        if len(stats): last_y_pos = list(stats.values())[-1]["y"]
        else: last_y_pos = list(stats.values())[-1]["Fewest Moves"]["y"]

        # update best score
        b_score = data[2]
        if b_score > stats["Best Score"]["score"]:
            self.settM.mainM.game_ent.stats[1][mode]["Best Score"]["score"] = b_score
        
        # update total score
        if data[1] or board.game_state == "lost":
            self.settM.mainM.game_ent.stats[1][mode]["Total Score"]["score"] += board.score

        # update top tile
        top_tile = int(board.board.max())
        if top_tile > stats["Top Tile"]["score"] and board.moves_done > 0 and top_tile > 4:
            self.settM.mainM.game_ent.stats[1][mode]["Top Tile"]["score"] = top_tile

        for tile in board.board_tiles.values():
            num = str(tile.num)+" - Tile"
            if num not in stats and tile.num >= 16:

                if len(stats) > 4: last_y_pos += 120
                # save text to table
                self.settM.mainM.game_ent.stats[1][mode][num] = {
                    "x":40, "y":last_y_pos+60, "font":"Arial", "f_size":22, "bold":True,
                    
                    "Games Reached":
                        {"score": 1, "x":40, "y":last_y_pos+100, "font":"Arial", "f_size":22, "bold":False},
                    "Shortest Time":
                        {"score": self.settM.gameM.game_ent.board_timers[mode], "x":40, "y":last_y_pos+140, "font":"Arial", "f_size":22, "bold":False},
                    "Fewest Moves":
                        {"score": board.moves_done, "x":40, "y":last_y_pos+180, "font":"Arial", "f_size":22, "bold":False}
                }

                # shift other stats
                if mode != "5x5":
                    next_modes = (["4x4", "5x5"] if mode == "3x3" else ["5x5"])
                    for _mode in next_modes:
                        keys = list(self.settM.mainM.game_ent.stats[1][_mode].keys())
                        for key in keys:
                            self.settM.mainM.game_ent.stats[1][_mode][key]["y"] += 180

                    '''stats = self.settM.mainM.game_ent.stats[1][mode]
                    last_y_pos = list(stats.values())[-1]["y"]
                    for _mode in next_modes:
                        keys = list(self.settM.mainM.game_ent.stats[1][_mode].keys())
                        last_y_pos += 180
                        for key in keys:
                            self.settM.mainM.game_ent.stats[1][_mode][key]["y"] = last_y_pos
                            last_y_pos += 40
                        if len(keys) > 4:
                            for _key in ["Games Reached", "Shortest Time", "Fewest Moves"]:
                                self.settM.mainM.game_ent.stats[1][_mode][key][_key]["y"] = last_y_pos
                                last_y_pos += 40'''

                    # extend the page
                    self.scrollPage.extendPage(180)
            
            elif num in stats:
                pass
    
    def draw_stats_info(self, screen):

        draw_alpha(screen, alpha_surf, bg_pos, alpha_val)
        self.info_surf.draw_surface(screen)
        quit_btn.blitButton(screen)

    def draw_stats(self, screen):

        if self.stats_changed:
            # update page content
            self.render_stats_page()
            self.stats_changed = False

        # draw page
        self.scrollPage.draw_page(screen, page_bottom_end_pos=596, draw_img=self.bg)
        #self.info_stats_btn.blitButton(screen)
        self.reset_stats_btn.blitButton(screen)
        self.settM.menu_btns["back_btn"].blitButton(screen)
        self.settM.mainM.menu_btns["made_by_btn"].blitButton(screen)

        if self.opt_type == "info":
            self.draw_stats_info(screen)

        elif self.opt_type == "reset":
            draw_alpha(screen, alpha_surf, bg_pos, alpha_val)
            if self.can_reset:
                screen.blit(self.reset_msg, restart_window_pos)
                self.settM.menu_btns["yes_btn"].blitButton(screen)
                self.settM.menu_btns["no_btn"].blitButton(screen)
            else:
                screen.blit(self.reset_not_poss, restart_window_pos)
                self.settM.menu_btns["ok_btn"].blitButton(screen)
    
    def update_stats(self, mPos):

        if self.opt_type is None:

            # update page

            # info description
            self.scrollPage.update_page(mPos)
            if self.info_stats_btn.isBtnClicked(mPos):
                self.scrollPage.can_show_scroller = False
                quit_btn.setButtonPos((60, 136))
                self.opt_type = "info"
            
            # reset scores
            elif self.reset_stats_btn.isBtnClicked(mPos):

                if self.settM.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.can_reset = self.can_reset_stats()
                self.opt_type = "reset"
            
            # back button
            elif self.settM.menu_btns["back_btn"].isBtnClicked(mPos) or self.settM.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.settM.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_2")
                self.settM.reset_menu_variables("show_stats")
                quit_btn.setButtonPos(quit_btn_pos)
                self.scrollPage.reset_page()
            
            self.settM.mainM.menu_btns["made_by_btn"].isBtnClickedOpenLink(mPos)
        
        elif self.opt_type == "info":
            
            if quit_btn.isBtnClicked(mPos) or self.settM.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                self.scrollPage.can_show_scroller = True
                self.opt_type = None

        else:

            if self.settM.menu_btns["yes_btn"].isBtnClicked(mPos) or self.settM.keys.keyPressed(pg.K_RETURN, "ret_key"):
                if self.settM.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.reset_stats()

            elif self.settM.menu_btns["no_btn"].isBtnClicked(mPos) or self.settM.menu_btns["ok_btn"].isBtnClicked(mPos) or self.settM.keys.keyPressed(pg.K_ESCAPE, "esc_key"):
                if self.settM.mainM.game_ent.sett_vars["sound"]: make_click_sound("click_1")
                self.opt_type = None

