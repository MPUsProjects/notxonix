import pygame as pg
from assets.gamelib.scripts import *


pg.init()
scr = pg.display.set_mode((640, 360))
walls = load_wall_textures()
scr.blit(walls['wall1'], (0, 0))
scr.blit(pg.image.load('assets/textures/wall/wall1.png'), (walls['wall1'].get_size()[0], 0))
running = True
# сам цикл
while running:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
            break