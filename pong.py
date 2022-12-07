import sys
import random
import pygame as pg

pg.init()
clock: pg.time = pg.time.Clock()

screen_width: int = 1280
screen_height: int = 960
screen: pg.display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('The Pong Game')

# Game Rectangles
ball: pg.Rect = pg.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # center ball at middle of screen
player: pg.Rect = pg.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent_length: int = 120
opponent: pg.Rect = pg.Rect(10, screen_height / 2 - 70, 10, opponent_length)

# game variables
ball_speed_x: int = 7 * random.choice((1, -1))
ball_speed_y: int = 7 * random.choice((1, -1))
player_speed: int = 0
opponent_speed: int = 19
init_score_time: bool or int = True
difficulty: int = 1

# score variables
player_score: int = 0
opponent_score: int = 0
game_font: pg.font = pg.font.Font("freesansbold.ttf", 32)

# color variables
bg_color: pg.Color = pg.Color('grey12')
red: pg.Color = pg.Color('red')
light_grey: tuple = (200, 200, 200)


def collision_vertical(entity: pg.Rect):
    if entity.top <= 0:
        entity.top = 0
    elif entity.bottom >= screen_height:
        entity.bottom = screen_height


def ball_animation():
    global ball_speed_x, ball_speed_y, init_score_time, difficulty, opponent_speed

    # ball movement
    ball.x += ball_speed_x * difficulty
    ball.y += ball_speed_y * difficulty

    # collision ball - screen
    if ball.top <= 0 or ball.bottom >= screen_height:  # vertical (y) axis
        ball_speed_y *= -1

    elif ball.left <= 0:  # horizontal (x) axis
        init_score_time = pg.time.get_ticks()  # calculate time since pygame.init() was executed | executed only once
        set_score('left')

    elif ball.right >= screen_width:  # horizontal (x) axis
        init_score_time = pg.time.get_ticks()
        set_score('right')

    # collision ball - players + difficulty change in ball movement & opponent speed
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        ball_speed_increase()
        opponent_ai_difficulty_increase()


def ball_speed_increase():
    global difficulty

    if difficulty <= 1.5:
        difficulty += 0.1

    elif difficulty <= 1.8:
        difficulty += 0.075

    else:
        difficulty += 0.05


def ball_restart():
    global ball_speed_y, ball_speed_x, player_score, opponent_score, init_score_time, difficulty, opponent_speed, \
            opponent_length

    current_time = pg.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - init_score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
        if current_time - init_score_time < 700:
            screen.blit((game_font.render("3", False, red)), (screen_width/2 - 10, screen_height/2 + 60))
        elif 700 < current_time - init_score_time < 1400:
            screen.blit((game_font.render("2", False, red)), (screen_width / 2 - 10, screen_height / 2 + 60))
        else:
            screen.blit((game_font.render("1", False, red)), (screen_width / 2 - 10, screen_height / 2 + 60))

    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        init_score_time = False
        difficulty = 1
        opponent_speed = 23
        opponent_length = 120


def set_score(score_side: str):
    global player_score, opponent_score

    if score_side == 'left':
        player_score += 1
    else:
        opponent_score += 1


def opponent_ai():
    global opponent_speed

    if opponent.top < ball.y:
        opponent.top += opponent_speed

    elif opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed


def opponent_ai_difficulty_increase():
    global opponent_speed, opponent_length
    # increasing length doesn't work for now

    if opponent_speed < 40:
        opponent_speed *= 1.1
        opponent_length *= 1.2

    elif opponent_speed < 48:
        opponent_speed *= 1.06
        opponent_length *= 1.08

    else:
        opponent_speed = 48
        opponent_length *= 1.04


while True:
    # input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                player_speed += 10
            if event.key == pg.K_UP:
                player_speed -= 10
        # release button, reverse operation
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                player_speed -= 10
            if event.key == pg.K_UP:
                player_speed += 10

    # visuals
    screen.fill(bg_color)  # drawn first
    pg.draw.ellipse(screen, light_grey, ball)
    pg.draw.rect(screen, light_grey, player)
    pg.draw.rect(screen, light_grey, opponent)

    pg.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))  # drawn last

    # scoring
    player_text = game_font.render(f"{player_score}", False, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(player_text, (660, 470))
    screen.blit(opponent_text, (600, 470))

    # logic
    ball_animation()
    if init_score_time:
        ball_restart()
    opponent_ai()
    collision_vertical(player)
    collision_vertical(opponent)
    player.y += player_speed

    # updating window
    pg.display.flip()  # draws a picture from the lopp
    clock.tick(60)  # limits how fast the computer runs the loop (e.g. 60 times per second)
