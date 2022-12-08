import sys
import random
import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    pass


class Ball(Block):
    pass


class Opponent(Block):
    pass


class GameManager:
    pass


# general setup
pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
clock = pg.time.Clock()

# main window
screen_width: int = 1280
screen_height: int = 960
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('The Pong Tournament')

# global variables
bg_color = pg.Color('2F373F')
accent_font: tuple = (27, 35, 43)
basic_font = pg.font.Font('freesansbold.ttf', 32)
plob_sound = pg.mixer.Sound('pong.wav')
score_sound = pg.mixer.Sound('score.wav')
middle_strip = pg.Rect(screen_width/2 - 2, 0, 4, screen_height)

# game objects
player = Player('Paddle.png', screen_width-20, screen_height/2, 5)
opponent = Opponent('Paddle.png', 20, screen_width/2, 5)
paddle_group = pg.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pg.sprite.GroupSingle()

game_manager = GameManager(ball_sprite, paddle_group)


while True:
    # input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                player.movement += player.speed
            if event.key == pg.K_UP:
                player.movement += player.speed
        # release button, reverse operation
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                player.movement += player.speed
            if event.key == pg.K_UP:
                player.movement += player.speed

    # background
    screen.fill(bg_color)
    pg.draw.rect(screen, accent_color, middle_strip)

    # run the game
    game_manager.run_game()

    # rendering
    pg.display.flip()
    clock.tick(120)

