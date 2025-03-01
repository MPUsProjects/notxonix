import pygame as pg
import math
import random

if __name__ == '__main__':
    pg.init()

    width = random.randint(250, 400)
    height = random.randint(250, 400)
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Кликер")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    radius = 10
    speed = 200
    balls = []
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                y = pos[1]
                x = pos[0]
                balls.append([x, y, speed / math.sqrt(2), -speed / math.sqrt(2)])
            if event.type == pg.QUIT:
                running = False

        screen.fill(BLACK)
        t = clock.tick() / 1000
        for ball in balls:
            pg.draw.circle(screen, WHITE, [int(ball[0]), int(ball[1])], radius)
            ball[0] -= ball[2] * t
            ball[1] += ball[3] * t
            if ball[0] < radius:
                ball[0] = radius
                ball[2] = -ball[2]
            if ball[0] > width - radius:
                ball[0] = width - radius
                ball[2] = -ball[2]
            if ball[1] < radius:
                ball[1] = radius
                ball[3] = -ball[3]
            if ball[1] > height - radius:
                ball[1] = height - radius
                ball[3] = -ball[3]
        pg.display.flip()
