import pygame as pg
import sys
from assets.gamelib.const import *

# setup
pg.init()
scr = pg.display.set_mode((640, 360))
clock = pg.time.Clock()
running = True
menu = True

pg.display.set_caption(f'{APPNAME} {APPVER}')

skinns = ['main_hero.png', 'loki.png', 'warrior.png']
skins = [pg.transform.scale(pg.image.load(skin_file), (int(100 * 3), int(100 * 3)))
         for skin_file in skinns]
current_skin_index = 0

# Главный игровой цикл
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                current_skin_index = (current_skin_index + 1) % len(skins)  # Переключение на следующий скин
            elif event.key == pg.K_LEFT:
                current_skin_index = (current_skin_index - 1) % len(skins)  # Переключение на следующий скин
            elif event.key == pg.K_ESCAPE:
                print("закрытие экрана")

    # Отображение фона
    scr.fill((255, 255, 255))  # Белый фон
    bg = pg.image.load('back.png')
    bg = pg.transform.rotozoom(bg, 0, 1.4)

    # Отображение текущего скина
    current_skin = skins[current_skin_index]
    scr.blit(bg, (0, 0))
    scr.blit(current_skin, (190, 50))

    # Обновление дисплея
    pg.display.flip()

    # Ограничение FPS
    pg.time.Clock().tick(30)