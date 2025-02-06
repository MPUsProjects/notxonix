import pygame as pg
from assets.gamelib.const import *
from assets.gamelib.scripts import *
from assets.gamelib.objects import *


FIELDTEXTURES = {}
WALLTEXTURES = {}
BALLTEXTURES = {}
PLAYERTEXTURES = {}
BGTEXTURES = {}
DECOTEXTURES = {}


def loading_screen():
    """Возможно, обтянутый кожей живой человек и не машина никогда его не увидит - слишком мало время загрузки"""

    # Загружаем спрайты, звуки и прочее, чтобы во время игры был минимум файловой работы
    global scr, FIELDTEXTURES, WALLTEXTURES, BALLTEXTURES, PLAYERTEXTURES, BGTEXTURES, DECOTEXTURES

    # Сделаем пользователю картинку загрузки, чтобы не беспокоился
    scr.blit(pg.image.load('assets/textures/background/loading_screen1.png'), (0, 0))
    pg.display.update()

    # Загрузка текстур разных видов
    FIELDTEXTURES = load_field_textures()
    WALLTEXTURES = load_wall_textures()
    BALLTEXTURES = load_wall_textures()
    PLAYERTEXTURES = load_player_textures()
    BGTEXTURES = load_bg_textures()
    DECOTEXTURES = load_deco_textures()

    # Загрузка звуков разных видов (пока их нет :/ )


def main_screen():
    global clock, scr, running, scrnow

    # прочая настройка для экрана
    bg_coord = 0
    # bg = pg.image.load('assets/textures/background/background_menu_movable.jpg')
    bg = pg.image.load('assets/textures/background/menunegotovo.png')
    # bg = pg.image.load('assets/textures/background/loading_screen1.png')

    while running and scrnow == MAINSCR:
        scr.fill('black')
        time = clock.tick()

        # апдейты
        scr.blit(bg, (bg_coord, 0))
        scr.blit(bg, (bg_coord + 503, 0))
        scr.blit(bg, (bg_coord + 1006, 0))
        bg_coord -= time * 0.02
        if bg_coord <= -503:
            bg_coord = 0

        # технический блок
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
                break


def game_screen():
    pass


def shop_screen():
    pass


# инициализация
pg.init()
scr = pg.display.set_mode((640, 360))
pg.display.set_caption(f'{APPNAME} {APPVER}')
pg.display.set_icon(pg.image.load('pepse loga.png'))
running = True
scrnow = MAINSCR
ball1 = pg.image.load('assets/textures/player/ball1.png')

# настройка
clock = pg.time.Clock()

# игровой цикл
loading_screen()  # загрузим ресурсы игры
# сам цикл
while running:
    if scrnow == MAINSCR:
        main_screen()
    elif scrnow == GAMESCR:
        game_screen()
    elif scrnow == SHOPSCR:
        shop_screen()