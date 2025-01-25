import pygame as pg
from assets.gamelib.const import *
from assets.gamelib.scripts import *
from assets.gamelib.objects import *


def main_screen():
    global clock, scr, running, scrnow

    # прочая настройка для экрана
    bg_coord = 0
    # bg = pg.image.load('assets/textures/background_menu_movable.jpg')
    bg = pg.image.load('assets/textures/background/loading_screen1.png')

    while running and scrnow == MAINSCR:
        scr.fill('black')
        time = clock.tick()

        # апдейты
        scr.blit(bg, (bg_coord, 0))
        """
        scr.blit(bg, (bg_coord + 503, 0))
        scr.blit(bg, (bg_coord + 1006, 0))
        """

        # рабочий блок
        """
        bg_coord -= time * 0.0125
        if bg_coord <= -503:
            bg_coord = 0
        """

        # технический блок
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
                break


def game_screen():
    pass


# инициализация
pg.init()
scr = pg.display.set_mode((640, 360))
pg.display.set_caption(f'{APPNAME} {APPVER}')
# pg.display.set_icon('')
running = True
scrnow = MAINSCR
ball1 = pg.image.load('assets/textures/ball1.png')

# настройка
clock = pg.time.Clock()

# игровой цикл
while running:
    if scrnow == MAINSCR:
        main_screen()
    elif scrnow == GAMESCR:
        game_screen()