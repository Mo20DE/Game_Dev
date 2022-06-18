import pygame as pg
from player import *
from entities import *
from settings import *

from utils_v2 import HUD_Button, Image, Sound, Text, SoundBar, ModeBar, Sound, TickBox, TickBox_Container, Vec, draw_alpha
import sys

pg.init()

# game class
class Game:

    def __init__(self):

        # create window
        self.screen = pg.display.set_mode((Width, Height))

        pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.running = True

        # sound
        self.music = Sound('music\_arcade_music.wav', 0.3)
        self.music.play(None, None, -1)
        self.sound = SoundBar((20, 20), (250, 5), (360, 160), False, None, (0, 97, 255), None, BORDER_CLR, True, GREY)
        self.modeBar = ModeBar((360, 330), 3, (250, 5), (20, 20), None, (0, 97, 255), BORDER_CLR)

        # title image
        self.titlescreen = Image(300, 90)._render_image('images\_title.png', False, True)

        # menu
        self.buttons = {
            'play_0': HUD_Button(Image(135, 45)._render_image('images\_buttons\play_0.png', False, True), ((Width/2)-75, 220)),
            'play_1': HUD_Button(Image(135, 45)._render_image('images\_buttons\play_1.png', False, True), ((Width/2)-75, 220)),
            'option_0': HUD_Button(Image(135, 45)._render_image('images\_buttons\options_0.png', False, True), ((Width/2)-75, 295)),
            'option_1': HUD_Button(Image(135, 45)._render_image('images\_buttons\options_1.png', False, True), ((Width/2)-75, 295)),
            'exit_0': HUD_Button(Image(135, 45)._render_image('images\_buttons\exit_0.png', False, True), ((Width/2)-75, 370)),
            'exit_1': HUD_Button(Image(135, 45)._render_image('images\_buttons\exit_1.png', False, True), ((Width/2)-75, 370)),
            'back_0': HUD_Button(Image(135, 45)._render_image('images\_buttons\_back_0.png', False, True), (70, 450)),
            'back_1': HUD_Button(Image(135, 45)._render_image('images\_buttons\_back_1.png', False, True), (70, 450))
        }
        self.pic = ['play_0', 'option_0', 'exit_0', 'back_0']

        # text
        self.mode_text = {
            'version': Text(Width - 88, Height - 30, "Build v1.1", 'Verdana', 15, GREY),
            'volume' : Text(350, 80, 'Volume', 'Verdana', 36, (255, 255, 255)),
            'zero': Text(352, 190, '0', 'Calibri', 20, WHITE),
            'max': Text(596, 190, 'MAX', 'Calibri', 20, WHITE),
            'difficulty': Text(350, 250, 'Difficulty', 'Verdana', 36, (255, 255, 255)),
            'easy': Text(338, 360, 'Easy', 'Arial', 20, GREEN),
            'normal': Text(455, 360, 'Normal', 'Verdana', 17, YELLOW),
            'hard': Text(595, 360, 'Hard', 'Verdana', 17, RED),
            'mode': Text(730, 180, 'Game Mode', 'Verdana', 36, WHITE),
            'bot_play': Text(760, 320, 'Bot', 'Verdana', 18, WHITE),
            'player_play': Text(865, 320, '2 Player', 'Verdana', 18, WHITE)
        }
        
        # states
        self.pressed = False
        self.not_button = False
        self.game_ended = False

        self.states = {
            'play': False, 
            'option': False, 
            'exit': False, 
            'back': False, 
            'restart': False
        }
        self.gameStates = States(self.states)

        # game end window
        self.win_suf_coords = Vec(185, -500)
        self.win_surf = pg.Surface((700, 420))
        self.win_buffer = None

        # coordinates of ball
        self.current_pos, self.prev_pos = [0, 0], [0, 0]
        # default game mode
        self.game_mode = 'bot'

        # score
        self.player_text = {
            'you': Text(280, 110, 'You', 'Verdana', 70, WHITE),
            'bot': Text(530, 110, 'Gabo-Bot', 'Verdana', 60, WHITE),
            'player2': Text(565, 110, 'Player 2', 'Verdana', 60, WHITE),
            'you_won': Text(270, 375, 'You Won. Nice!', 'Verdana', 70, GREEN),
            'you_lose': Text(270, 375, 'You Lose. Bad!', 'Verdana', 70, RED)
        }

        # tickbox
        self.tickBox_container = TickBox_Container(
            True,
            TickBox((755, 260), [40, 40], GREY), # play against bot
            TickBox((880, 260), [40, 40], GREY), # play against player
        )

    def check_states(self, img1, img2, state, index,  ms_pos):
        
        if not self.pressed and self.buttons[img1].checkClicked(ms_pos):
            self.pressed = True
   
        if self.buttons[img1].checkCollision(ms_pos):
            self.pic[index] = img2
            if self.pressed and self.buttons[img1].checkCollision(ms_pos):
                if pg.mouse.get_pressed()[0] == 0:
                    self.states[state] = True
                    self.pressed = False
            else: self.pressed = False
        else: 
            self.pic[index] = img1
        
    def compute_current_prev_loc(self):
        self.current_pos[0] = self.ball.rect.x
        self.current_pos[1] = self.ball.rect.y
        self.prev_pos[0] = self.current_pos[0] + self.ball.vx
        self.prev_pos[1] = self.current_pos[1] + self.ball.vy
    
    def options(self):

        # draw text
        self.mode_text['volume'].draw_text(self.screen)
        self.mode_text['difficulty'].draw_text(self.screen)  

        # draw bars
        self.sound.draw_soundbar(self.screen)
        self.modeBar.draw_modebar(self.screen)
        # draw back button
        self.buttons[self.pic[3]].blit_button(self.screen)

        # draw mixer volume
        self.mode_text['zero'].draw_text(self.screen)
        self.mode_text['max'].draw_text(self.screen)

        # draw modes
        self.mode_text['easy'].draw_text(self.screen)
        self.mode_text['normal'].draw_text(self.screen)
        self.mode_text['hard'].draw_text(self.screen)

        # tickbox
        self.mode_text['mode'].draw_text(self.screen)
        self.tickBox_container.draw_container_objects(self.screen)
        self.mode_text['bot_play'].draw_text(self.screen)
        self.mode_text['player_play'].draw_text(self.screen)
    
    def set_difficulty(self):

        if self.modeBar.difficulty == 0:
            self.player_ai.speed = 8.5 # easy
        elif self.modeBar.difficulty == 1:
            self.player_ai.speed = 14 # normal
        else: self.player_ai.speed = 25 # hard
    
    def check_game_mode(self):
        if self.tickBox_container.tickBoxes[0].isActive:
            self.game_mode = 'bot'
            self.player.both_keys = True
        else: 
            self.game_mode = 'player'
            self.player.both_keys = False

    def new(self):

        # Start a new game, when game over
        self.all_sprites = pg.sprite.Group()
        self.game_shapes = pg.sprite.Group()

        # initialize players
        self.player = Player((player_x, player_y) ,['w', 's'], True)
        self.player_2 = Player((player_x_2, player_y_2), ['up', 'down'])

        self.utility = Utility()
        # Line
        self.line = Line()
        # Ball
        self.ball = Ball()
        # bot
        self.player_ai = Bot_Movement()

        # Add objects to game_shapes group
        self.game_shapes.add(self.line)

        # Add players to all_sprites group
        self.all_sprites.add(self.player)

        self.all_sprites.add(self.ball)

        self.ball_effect = BallEffect(self.ball, 20)

        self.set_difficulty()

    def update(self):

        ms_pos = pg.mouse.get_pos()

        if self.ball.pl_1_score == 5 or self.ball.pl_2_score == 5:
            self.game_ended = True

        if self.states['play']:

            # update states when in-game
            self.gameStates.update_states(ms_pos, self.ball, self.player, self.player_2)

            if not self.game_ended:
                
                # reset player position
                if self.ball.goal:
                    self.player.resetPos()
                    if self.game_mode == 'player':
                        self.player_2.resetPos()

                self.compute_current_prev_loc()
                # refer to utility class and call collision method - check collision
                self.utility.check_collision(self.ball, self.player)
                self.utility.check_collision(self.ball, self.player_2)

                # Game Lopp - Update #
                self.all_sprites.update()

                # update effect balls
                self.ball_effect.update_balls(self.prev_pos, self.current_pos)

                # initialize bot (movement)
                if self.game_mode == 'bot':
                    # bot moves
                    self.player_ai.compute_movement(self.ball, self.player_2)
                else:
                    # second player moves
                    self.player_2.update()
            
            # restart game
            elif self.states['restart']:

                self.game_ended = False
                self.states['restart'] = False
                self.win_suf_coords.reset_vector()

            # go back home
            elif not self.states['play']: 
                
                self.pic[0] = 'play_0'
                self.game_ended = False
                self.win_suf_coords.reset_vector()
        else:
            
            # main menu #
            self.check_states('option_0', 'option_1', 'option', 1, ms_pos)

            if not self.states['option']:
                self.check_states('play_0', 'play_1', 'play', 0, ms_pos)
                self.check_states('exit_0', 'exit_1', 'exit', 2, ms_pos)

                if self.states['exit'] and not self.states['option']:
                    self.playing = False
                    self.running = False
                    sys.exit()

            else:

                # option menu #
                if self.pressed and self.buttons['option_0'].checkCollision(ms_pos) and not self.states['play']:
                    self.pressed = False
               
                self.check_states('back_0', 'back_1', 'back', 3, ms_pos)
                # go back to menu
                if self.states['back']:
                    self.states['option'] = False
                    self.states['back'] = False

                # update bars
                self.sound.update_soundbar(ms_pos)
                # play music
                self.sound.get_audio_input(self.music)
                self.modeBar.update_modebar(ms_pos)

                # update tickbox
                self.tickBox_container.update_container_objects(ms_pos)
                self.check_game_mode()
              
                # set bot difficulty according to modebar
                self.set_difficulty()
        
        # after updating everithing, update the display
        pg.display.update()

    def draw(self):

        # background
        self.screen.fill(BG_COLOR)
        # version
        self.mode_text['version'].draw_text(self.screen)

        if self.states['play']:

            self.gameStates.draw_states(self.screen)
            if not self.game_ended:
                
                self.line.middle_line(self.screen, LIGHT_GREY, (Width/2, plat_height), (Width/2, Height))
                Text((Width/2) - 25, (Height / 2) - 10, f"{self.ball.pl_1_score}", 'Calibri', 24, BLACK).draw_text(self.screen)
                Text((Width/2) + 12, (Height / 2) - 10, f"{self.ball.pl_2_score}", 'Calibri', 24, BLACK).draw_text(self.screen)
                self.ball_effect.draw_balls(self.screen)
                
                self.all_sprites.draw(self.screen)
                self.player_2.draw_player(self.screen)

            else:
                self.game_end_screen()

        elif self.states['option']:
            self.options()

        else:
            self.screen.blit(self.titlescreen, (380, 70))
            self.buttons[self.pic[0]].blit_button(self.screen)
            self.buttons[self.pic[1]].blit_button(self.screen)
            self.buttons[self.pic[2]].blit_button(self.screen)
        
    def events(self):

        # Game Loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    # Quit the game(loop)
                    self.playing = False
                # Quit the program(loop)
                self.running = False
    
    def run(self):

        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def game_end_screen(self):

        draw_alpha(self.screen, self.win_surf, (self.win_suf_coords.x, self.win_suf_coords.y), 222, self.win_buffer)
        if self.win_suf_coords.y <= 75:
            self.win_suf_coords.y += 10

        else:
            
            self.player_text['you'].draw_text(self.screen)
            if self.game_mode == 'bot':
                self.player_text['bot'].draw_text(self.screen)
            else:
                self.player_text['player2'].draw_text(self.screen)

            # draw score
            Text(320, 230, f'{self.ball.pl_1_score}', 'Calibri', 100, WHITE).draw_text(self.screen)
            Text(660, 230, f'{self.ball.pl_2_score}', 'Calibri', 100, WHITE).draw_text(self.screen)

            # who won
            if self.ball.pl_1_score == 5:
                self.player_text['you_won'].draw_text(self.screen)

            elif self.ball.pl_2_score == 5:
                self.player_text['you_lose'].draw_text(self.screen)

# main game loop
def main():

    game = Game()
    while game.running:
        game.new()
        game.run()
    pg.quit()

# call main - function
if __name__ == '__main__':
    main()

        