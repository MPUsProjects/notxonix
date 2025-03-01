import pygame as pg
from assets.gamelib.scripts import *
from assets.gamelib.const import *


WALLS = load_wall_textures()
FIELD = load_field_textures()
pg.init()
WALLS = load_wall_textures()
FIELD = load_field_textures()
scr = pg.display.set_mode((640, 360))
x = 0
y = 0
# стены
for i in range(15):
    scr.blit(WALLS['wall1'], (x, 0))
    scr.blit(WALLS['wall1'], (x, 320))
    scr.blit(WALLS['wall1'], (600, y))
    scr.blit(WALLS['wall1'], (0, y))
    x += 40
    y += 40
x = 40
y = 40
# зона игрока
for i in range(14):
    scr.blit(FIELD['captured'], (x, 40))
    scr.blit(FIELD['captured'], (x, 280))
    x += 40
for i in range(6):
    scr.blit(FIELD['captured'], (560, y))
    scr.blit(FIELD['captured'], (40, y))
    y += 40
# зона шарика
x = 80
y = 80
for i in range(5):
    for z in range(12):
        scr.blit(FIELD['ballfield'], (x, y))
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
