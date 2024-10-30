from utils import Main, Image
from static import *
from entities import Ball


class PinShot(Main):

    def __init__(self):

        super().__init__(width, height, caption, fps)
    
    def new(self):

        self.bg = Image(width, height)._render_image(bg)
        self.ball = Ball()

    def events(self):

        self.handle_quit()

    def update(self):

        self.ball.update()
        self.dp_update()
    
    def draw(self):

        self.screen.blit(self.bg, (0, 0))
        self.ball.draw(self.screen)


if __name__ == '__main__':

    game = PinShot()
    game.runMain()
