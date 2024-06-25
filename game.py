import sys
import random

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
RED = [255, 0, 0]
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SPEED = 3
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
Background_color = (0, 0, 0)
Enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
score = 0
clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level(score, SPEED):
    # if score < 20:
    #     SPEED = 1
    # elif score < 40:
    #     SPEED = 10
    # else:
    #     SPEED = 25
    # return SPEED
    SPEED = score / 5 + 1


def drop_enemies(Enemy_list):
    delay = random.random()
    if len(Enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        Enemy_list.append([x_pos, y_pos])


def update_enemy_positions(Enemy_list, score):
    for idx, enemy_pos in enumerate(Enemy_list):
        if 0 <= enemy_pos[1] < HEIGHT:
            enemy_pos[1] += 10
        else:
            Enemy_list.pop(idx)
            score += 1
    return score


def collision_check(Enemy_list, player_pos):
    for enemy_pos in Enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def draw_enemies(Enemy_list):
    for enemy_pos in Enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            player_pos = [x, y]
    screen.fill(Background_color)

    # UPDATE POSITION OF ENEMY
    # if 0 <= enemy_pos[1] < HEIGHT:
    #     enemy_pos[1] += 10

    drop_enemies(Enemy_list)
    score = update_enemy_positions(Enemy_list, score)
    set_level(score, SPEED)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))
    if collision_check(Enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(Enemy_list)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    clock.tick(30)

    pygame.display.update()

    # else:
    #     enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
    #     enemy_pos[1] = SPEED