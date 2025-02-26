import pygame as pg
from assets.gamelib.const import *
from assets.gamelib.scripts import *
from assets.gamelib.objects import *
import sys


FIELDTEXTURES = {}
WALLTEXTURES = {}
BALLTEXTURES = {}
PLAYERTEXTURES = {}
BGTEXTURES = {}
DECOTEXTURES = {}

skins_ingame = ['main_hero.png', 'loki.png', 'warrior.png', 'mexicanes.png']  # скины которые впринципе есть в игре
skins_onacc = ['main_hero.png']


def shutdown():
    global running, ldb, gamedb
    running = False
    pg.quit()
    ldb.save(gamedb)
    ldb.close()


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
    bg = load_bg_textures()['menunegotovo']
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
                shutdown()
                break
            if event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    scrnow = SKINSCR
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    running = False
                    break


def game_screen():
    print('I AM SORRY BOY')


def skin_changer():
    global clock, scr, running, scrnow, skins_onacc
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption(f'{APPNAME} {APPVER}')
    current_skin_index = 0

    # Главный игровой цикл
    while running and scrnow == SKINSCR:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                shutdown()
                break
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    current_skin_index = (current_skin_index + 1) % len(skins_pic)  # Переключение на следующий скин
                elif event.key == pg.K_LEFT:
                    current_skin_index = (current_skin_index - 1) % len(skins_pic)  # Переключение на следующий скин
                elif event.key == pg.K_ESCAPE:
                    scrnow = MAINSCR
            if event.type == pg.MOUSEBUTTONUP:
                cor = event.pos
                if cor[0] <= 60 and 20 <= cor[1] <= 40:
                    scrnow = MAINSCR
                if cor[0] >= 570 and 20 <= cor[1] <= 40:
                    scrnow = SHOPSCR
                if 260 <= cor[0] <= 320 and 300 <= cor[1] <= 360:
                    current_skin_index = (current_skin_index - 1) % len(skins_pic)  # Переключение на следующий скин
                if 390 <= cor[0] <= 550 and 300 <= cor[1] <= 360:
                    current_skin_index = (current_skin_index + 1) % len(skins_pic)  # Переключение на следующий скин
        # Отображение фона
        scr.fill((255, 255, 255))  # Белый фон
        bg = pg.image.load('assets/textures/background/back.png')
        bg = pg.transform.rotozoom(bg, 0, 1.4)

        # Отображение текущего скина
        current_skin = skins_pic[current_skin_index]
        scr.blit(bg, (0, 0))
        if current_skin_index == 2:
            scr.blit(current_skin, (170, 50))
        elif current_skin_index == 0:
            scr.blit(current_skin, (180, 50))
        else:
            scr.blit(current_skin, (190, 50))
        scr.blit(ARR, (370, 300))
        scr.blit(ARR2, (240, 300))
        scr.blit(BACK, (0, 0))
        scr.blit(FOR, (565, 0))
        scr.blit(BF, (60, 21))
        scr.blit(MF, (493, 21))
        scr.blit(ST, (133, 20))
        # Обновление дисплея
        pg.display.flip()

        # Ограничение FPS
        pg.time.Clock().tick(30)


def shop_screen():
    global clock, scr, running, scrnow, skins_onacc, money
    pg.init()
    clock = pg.time.Clock()

    pg.display.set_caption(f'{APPNAME} {APPVER}')

    # Главный игровой цикл
    while running and scrnow == SHOPSCR:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                shutdown()
                break
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    scrnow = MAINSCR
            if event.type == pg.MOUSEBUTTONUP:
                cor = event.pos
                if cor[0] <= 60 and 20 <= cor[1] <= 40:
                    scrnow = SKINSCR
                if 50 <= cor[0] <= 240 and 70 <= cor[1] <= 360:
                    if gamedb['LB'] == '0':
                        if money >= LOKI:
                            gamedb["LB"] = '1'
                            money -= LOKI
                            gamedb['Money'] = str(money - LOKI)
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")
                    elif gamedb['LB'] == '1' and gamedb["MexB"] == '0':
                        if money >= MEXICANES:
                            gamedb["MexB"] = '1'
                            money -= MEXICANES
                            gamedb['Money'] = str(money - MEXICANES)
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")
                if 300 <= cor[0] <= 490 and 70 <= cor[1] <= 360:
                    if gamedb['WB'] == '0':
                        if money >= WARRIOR:
                            gamedb["WB"] = '1'
                            money -= WARRIOR
                            gamedb['Money'] = str(money - WARRIOR)
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")

        # Отображение фона
        scr.fill((255, 255, 255))  # Белый фон
        bg = pg.image.load('assets/textures/background/back.png')
        bg = pg.transform.rotozoom(bg, 0, 1.4)

        # Отображение текущего скина
        scr.blit(bg, (0, 0))
        if gamedb['LB'] == '0':
            scr.blit(skins_pic1[1], (20, 50))
        if gamedb['WB'] == '0':
            scr.blit(skins_pic1[2], (300, 50))
        if gamedb['LB'] == '1' and gamedb['MexB'] == '0':
            scr.blit(skins_pic1[3], (20, 50))
        scr.blit(BACK, (0, 0))
        scr.blit(BF, (60, 21))
        scr.blit(MT, (210, 21))
        scr.blit(MON, (570, 0))
        scr.blit(FONT.render(gamedb['Money'], True, (255, 255, 255)), (550, 18))
        # Обновление дисплея
        pg.display.flip()

        # Ограничение FPS
        pg.time.Clock().tick(30)


''' Окно подтверждения покупки, выйдет в 1.1(
def buy_screen():
    global clock, scr
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption(f'{APPNAME} {APPVER}')
    while running and scrnow == SHOPSCR:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                cor = event.pos
                if cor[0] <= 50:
                    return True
                else:
                    return False
        # Отображение фона
        scr1.fill((255, 255, 255))  # Белый фон
        bg = pg.image.load('assets/textures/background/back.png')
        bg = pg.transform.rotozoom(bg, 0, 1.4)
        scr1.blit(bg, (0, 0))
        scr1.blit(YES, (0, 0))
        scr1.blit(NO, (50, 0))
        # Обновление дисплея
        pg.display.flip()
        # Ограничение FPS
        pg.time.Clock().tick(30)
'''

# инициализация
pg.init()
scr = pg.display.set_mode((640, 360))
pg.display.set_caption(f'{APPNAME} {APPVER}')
pg.display.set_icon(pg.image.load('assets/textures/player/ballpepsi.png'))
running = True
scrnow = MAINSCR
ball1 = pg.image.load('assets/textures/player/ball1.png')

# настройка
clock = pg.time.Clock()
ldb = LocalDB(LDBFILE)
gamedb = ldb.get_all()
money = int(gamedb['Money'])
if gamedb['LB'] == '1':
    skins_onacc.append(LOKI_SKIN)
if gamedb['WB'] == '1':
    skins_onacc.append(WARRIOR_SKIN)
if gamedb['MexB'] == '1':
    skins_onacc.append(MEXICAN_SKIN)
skins_pic = [pg.transform.scale(pg.image.load(f'assets/textures/player/{skin_file}'),
                                   (int(100 * 3), int(100 * 3))) for skin_file in skins_onacc]
skins_pic1 = [pg.transform.scale(pg.image.load(f'assets/textures/player/{skin_file}'),
                                   (int(100 * 3), int(100 * 3))) for skin_file in skins_ingame]
# игровой цикл
loading_screen()  # загрузим ресурсы игры
# сам цикл
while running:
    if scrnow == MAINSCR:
        main_screen()
    elif scrnow == GAMESCR:
        game_screen()
    elif scrnow == SKINSCR:
        skin_changer()
    elif scrnow == SHOPSCR:
        shop_screen()
