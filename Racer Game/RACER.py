import pygame
import random
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 1000

RED = (255, 0, 0)

BLACK = (0, 0, 0)

RACER_size = 50
RACER_pos = [WIDTH / 2, HEIGHT - 2 * RACER_size]

TRAFFIC_size = 50
TRAFFIC_pos = [random.randint(0, WIDTH - TRAFFIC_size), 0]
TRAFFIC_list = [TRAFFIC_pos]

RACER_image = pygame.image.load('Batmobile.png')

RACER_image_small_convert = pygame.transform.scale(RACER_image, (30,
        70))

TRAFFIC_image = \
    pygame.image.load('imgbin-car-pixel-art-pixel-qEpgawFV8RXsYneV74warizBV.jpg'
                      )

TRAFFIC_image_small_convert = pygame.transform.scale(TRAFFIC_image,
        (30, 70))

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont('monospace', 35)

myFont2 = pygame.font.SysFont('monospace', 25)


def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 10
    elif score < 60:
        SPEED = 15
    elif score < 100:
        SPEED = 20
    elif score < 150:
        SPEED = 25
    elif score < 200:
        SPEED = 30
    elif score < 250:
        SPEED = 35
    else:
        SPEED = 50
    return SPEED


def TRAFFIC(TRAFFIC_list):
    delay = random.random()
    if len(TRAFFIC_list) < 20 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - TRAFFIC_size)
        y_pos = 0
        TRAFFIC_list.append([x_pos, y_pos])


def SPAWN_TRAFFIC(TRAFFIC_list):
    for TRAFFIC_pos in TRAFFIC_list:
        screen.blit(TRAFFIC_image_small_convert, (TRAFFIC_pos[0],
                    TRAFFIC_pos[1], TRAFFIC_size, TRAFFIC_size))


def UPDATE_TRAFFIC_POS(TRAFFIC_list, score):
    for (index, TRAFFIC_pos) in enumerate(TRAFFIC_list):
        if TRAFFIC_pos[1] >= 0 and TRAFFIC_pos[1] < HEIGHT:
            TRAFFIC_pos[1] += SPEED
        else:
            TRAFFIC_list.pop(index)
            score += 1
    return score


def CHECK_COLLISION(TRAFFIC_list, RACER_pos):
    for TRAFFIC_pos in TRAFFIC_list:
        if COLLISION_DETECTION(TRAFFIC_pos, RACER_pos):
            return True
    return False


def COLLISION_DETECTION(RACER_pos, TRAFFIC_pos):
    R_x = RACER_pos[0]
    R_y = RACER_pos[1]

    T_x = TRAFFIC_pos[0]
    T_y = TRAFFIC_pos[1]

    if T_x >= R_x and T_x < R_x + RACER_size or R_x >= T_x and R_x \
        < T_x + TRAFFIC_size:
        if T_y >= R_y and T_y < R_y + RACER_size or R_y >= T_y and R_y \
            < T_y + TRAFFIC_size:
            return True
    return False


def PLAYER_CAR(x, y):
    screen.blit(RACER_image_small_convert, (x, y))


x = WIDTH
y = HEIGHT
x_change = 0
car_speed = 0
key_pressed = False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key_pressed = True
            x = RACER_pos[0]
            y = RACER_pos[1]

            if event.key == pygame.K_LEFT:
                x -= RACER_size
            elif event.key == pygame.K_RIGHT:
                x += RACER_size

            RACER_pos = [x, y]

    screen.fill(BLACK)
    TRAFFIC(TRAFFIC_list)
    score = UPDATE_TRAFFIC_POS(TRAFFIC_list, score)
    SPEED = set_level(score, SPEED)

    text = 'Score:' + str(score)
    label = myFont.render(text, 1, RED)
    screen.blit(label, (WIDTH - 1000, HEIGHT - 1000))

    text2 = 'Press any arrow key to spawn car!'
    if key_pressed:
        text2 = ''
    label = myFont2.render(text2, -1, RED)
    screen.blit(label, (WIDTH - 750, HEIGHT - 1000))

    if CHECK_COLLISION(TRAFFIC_list, RACER_pos):
        game_over = True
        break

    SPAWN_TRAFFIC(TRAFFIC_list)

    PLAYER_CAR(x, y)

    clock.tick(30)

    pygame.display.update()
