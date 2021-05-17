import pygame
import random
import sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos+576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos-300))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        # This pipe is on the bottom of the screen because the top pipe will never reach this position
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            # flip(surface_to_flip, flip_in_x_direction?, flip_in_y_direction?)
            screen.blit(pygame.transform.flip(pipe_surface, False, True), pipe)


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False
    return True


def rotate_bird(bird):
    # scales and rotates a surface
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*2, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def display_score(game_state):
    global MAIN_GAME, GAME_OVER

    if game_state == MAIN_GAME:
        score_surface = game_font.render(
            f'Score: {str(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == GAME_OVER:
        score_surface = game_font.render(
            f'Score: {str(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score: {str(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()
# width and height of the screen
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04B_19.ttf', 40)

# Game Variables
gravity = .5
bird_movement = 0
pipe_height = [400, 600, 800]
game_active = True
score = 0
MAIN_GAME = 'MAIN_GAME'
GAME_OVER = 'GAME_OVER'
high_score = 0
can_score = True
game_over_surface = pygame.transform.scale2x(
    pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

bg_surface = pygame.transform.scale2x(
    pygame.image.load('assets/background-day.png').convert())

floor_surface = pygame.transform.scale2x(
    pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-midflap.png').convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-downflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 300))

BIRDFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP, 200)


pipe_surface = pygame.transform.scale2x(
    pygame.image.load('assets/pipe-green.png').convert())
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    # pygame looks for any event that is happening such as mouse movement, key presses...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird Movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        display_score(MAIN_GAME)
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        display_score(GAME_OVER)

    # Floor

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(100)
