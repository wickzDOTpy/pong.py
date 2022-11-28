import sys, random
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
opponent: pg.Rect = pg.Rect(10, screen_height / 2 - 70, 10, 140)

# Colors
bg_color: pg.Color = pg.Color('grey12')
light_grey: tuple = (200, 200, 200)

# game variables
ball_speed_x: int = 7 * random.choice((1, -1))
ball_speed_y: int = 7 * random.choice((1, -1))
player_speed: int = 0
opponent_speed: int = 23  # opponent difficulty

# score variables
player_score: int = 0
opponent_score: int = 0
game_font: pg.font = pg.font.Font("freesansbold.ttf", 32)


def collision_vertical(entity):
    if entity.top <= 0:
        entity.top = 0
    elif entity.bottom >= screen_height:
        entity.bottom = screen_height


def ball_animation():
    global ball_speed_x, ball_speed_y

    # ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # collision ball - screen
    if ball.top <= 0 or ball.bottom >= screen_height:  # vertical (y) axis
        ball_speed_y *= -1
    elif ball.left <= 0:  # horizontal (x) axis
        ball_restart('left')
    elif ball.right >= screen_width:  # horizontal (x) axis
        ball_restart('right')

    # collision ball - players
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart(side):
    global ball_speed_y, ball_speed_x
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

    update_score(side)


def update_score(side):
    global player_score, opponent_score

    if side == 'left':
        player_score += 1
    else:
        opponent_score += 1


def opponent_ai():
    global opponent_speed

    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed


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
    opponent_ai()
    collision_vertical(player)
    collision_vertical(opponent)
    player.y += player_speed

    # updating window
    pg.display.flip()  # draws a picture from the lopp
    clock.tick(60)  # limits how fast the computer runs the loop (e.g. 60 times per second)
    print(player_score, opponent_score)
