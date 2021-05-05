import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w//self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    # to this dictionary we'll add keys which is the current position of the head of our snake, and then is going to be set equal to which direction is going to turn

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0  # this keeps track of the direction we're moving towards

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # dictionary that holds all the key values

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    # we need to actually remember where we actually turn, so the tail can turn at that point

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Loop through list of positions of the body, ie cubes
        for i, c in enumerate(self.body):
            p = c.pos[:]  # This stores the cubes position on the grid

            if p in self.turns:  # If the cubes current position is one where we turned

                # get the direction value, see in which direction we are gonna move
                turn = self.turns[p]
                c.move(turn[0], turn[1])  # Move our cube in that direction
                # If this is the last cube in our body remove the turn from the dict. if we didnt do that, every time we hit that position on the screen our snake would change directions in that point
                if i == len(self.body)-1:
                    self.turns.pop(p)

            else:  # If we are not turning the cube, because the snake is always moving, we need to check if we are hitting the edge of the screen
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    # If we haven't reached the edge just move in our current direction
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        pass

    def addCube(self):
        # find out where the tail is, and then add another cube there

        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

                if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # draw eyes if it's the head
            else:
                c.draw(surface,)


def drawGrid(w, rows, surface):
    # how big each square in the grid is going to be, we need to check the space between each
    sizeBtwn = w // rows
    x = 0
    y = 0

    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack

    surface.fill((0, 0, 0))
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.set_caption("Judith's Snake Game")
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # make sure we don't place a snack on top of the snake
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

# def message_box(subject, content):
#     pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    game_running = True
    CLOCK = pygame.time.Clock()
    while game_running:

        pygame.time.delay(50)
        # clock object that allows us to say how many times the while loop will run per second
        CLOCK.tick(10)

        s.move()

        # check if we hit the cube
        if s.body[0].pos==snack.pos:
            s.addCube()
            snack=cube(randomSnack(rows, s),color=(0,255,0))
            

        redrawWindow(win)

    pass


main()
