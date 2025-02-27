import pygame as pg
from assets.gamelib.scripts import *


pg.init()
scr = pg.display.set_mode((640, 360))
walls = load_wall_textures()
field = load_field_textures()
x = 0
y = 0
# стены
for i in range(15):
    scr.blit(walls['wall1'], (x, 0))
    scr.blit(walls['wall1'], (x, 320))
    scr.blit(walls['wall1'], (600, y))
    scr.blit(walls['wall1'], (0, y))
    x += 40
    y += 40
x = 40
y = 40
# зона игрока
for i in range(14):
    scr.blit(field['captured'], (x, 40))
    scr.blit(field['captured'], (x, 280))
    x += 40
for i in range(6):
    scr.blit(field['captured'], (560, y))
    scr.blit(field['captured'], (40, y))
    y += 40
# зона шарика
x = 80
y = 80
for i in range(5):
    for z in range(12):
        scr.blit(field['ballfield'], (x, y))
        x += 40
    x = 80
    y += 40
running = True
# сам цикл
while running:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
            break