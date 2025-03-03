import pygame as pg
from assets.gamelib.const import *
from assets.gamelib.scripts import *
from assets.gamelib.objects import *
import sys
from random import randint


FIELDTEXTURES = {}
WALLTEXTURES = {}
BALLTEXTURES = {}
PLAYERTEXTURES = {}
BGTEXTURES = {}
DECOTEXTURES = {}

skins_ingame = ['main_hero.png', 'loki.png', 'warrior.png', 'mexicanes.png', 'shrek.png']
# скины которые впринципе есть в игре

skins_onacc = ['main_hero.png']


def shutdown():
    global running, ldb, gamedb
    running = False
    pg.quit()
    ldb.save(gamedb)
    ldb.close()


def death_func():
    global ballamount, scrnow, STATUS
    scrnow = GAMEOVERSCR
    STATUS = 0


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
    BALLTEXTURES = load_ball_textures()
    PLAYERTEXTURES = load_player_textures()
    BGTEXTURES = load_bg_textures()
    DECOTEXTURES = load_deco_textures()

    # Загрузка звуков разных видов (пока их нет :/ )

    # Отрисовка фона экрана игры
    gamebg = pg.Surface(scr.get_size())
    xsize, ysize = scr.get_size()
    for i in range(0, xsize, 40):
        for j in range(0, ysize, 40):
            gamebg.blit(WALLTEXTURES['wall1'], (i, j))
    BGTEXTURES['gamebg'] = gamebg


def main_screen():
    global clock, scr, running, scrnow

    # прочая настройка для экрана
    bg_coord = 0
    # bg = pg.image.load('assets/textures/background/background_menu_movable.jpg')
    bg = BGTEXTURES['menunegotovo']
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
        scr.blit(BTN, (200, 0))
        scr.blit(BTN, (200, 60))
        scr.blit(BTN, (200, 120))
        scr.blit(GAME, (280, 110))
        scr.blit(MT1, (265, 170))
        scr.blit(LEAVE, (280, 230))
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
            if event.type == pg.MOUSEBUTTONUP:
                x = event.pos[0]
                y = event.pos[1]
                if 255 < x < 390 and 90 < y < 150:
                    scrnow = GAMESCR
                    break
                elif 255 < x < 390 and 160 < y < 210:
                    scrnow = SKINSCR
                elif 255 < x < 390 and 220 < y < 270:
                    shutdown()
                    running = False
                    break


def game_screen():
    global scr, scrnow, clock, running, gameboard, horwalls, vertwalls, ballgroup, STATUS
    board = gameboard
    board.set_standart_board()
    bboard = board.board
    ballamount = randint(1, 4)
    for _ in range(ballamount):
        a = Ball(BALLTEXTURES['ball2'], (randint(81, 500), randint(81, 240)), ballgroup, horwalls,
                 vertwalls, board)
        a.deathfunc = death_func

    while running and scrnow == GAMESCR:
        # тех часть
        scr.blit(BGTEXTURES['gamebg'], (0, 0))

        # апдейты
        board.draw(scr)
        ballgroup.draw(scr)
        ballgroup.update()

        # основная часть
        fieldamount = sum(map(lambda y: sum(map(lambda x: 1 if bboard[y][x].get_cell_state() == CELLFIELD else 0,
                                                range(len(bboard[0])))), range(len(bboard))))
        if fieldamount >= len(bboard) * len(bboard[0]) * 0.75:
            gamedb['Money'] = str(int(gamedb['Money']) + ballamount)
            scrnow = GAMEOVERSCR
            board.spawn_player()
            STATUS = 1

        # тех часть
        pg.display.update()
        for event in pg.event.get():
            # проверка на закрытие
            if event.type == pg.QUIT:
                shutdown()
                break
            # управление кнопками
            elif event.type == pg.KEYDOWN:
                if event.key == KUP:
                    board.move_player(-1, 0)
                elif event.key == KDOWN:
                    board.move_player(1, 0)
                elif event.key == KLEFT:
                    board.move_player(0, -1)
                elif event.key == KRIGHT:
                    board.move_player(0, 1)
    horwalls.empty()
    vertwalls.empty()
    ballgroup.empty()


def game_over_screen():
    global clock, scr, running, scrnow, STATUS
    pg.display.update()
    while running and scrnow == GAMEOVERSCR:
        scr.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                shutdown()
                break
            if event.type == pg.MOUSEBUTTONUP:
                x = event.pos[0]
                y = event.pos[1]
                if 260 <= x <= 420 and 165 <= y <= 210:
                    scrnow = MAINSCR
        # фон
        bg = BGTEXTURES['back']
        bg = pg.transform.rotozoom(bg, 0, 1.4)
        scr.blit(bg, (0, 0))
        scr.blit(OVER, (150, 50))
        if STATUS == 0:
            scr.blit(LOSTEX, (250, 100))
        elif STATUS == 1:
            scr.blit(WINTEX, (250, 100))
        scr.blit(BTN, (215, 70))
        scr.blit(LEAVE, (294, 180))
        pg.display.flip()

        # Ограничение FPS
        pg.time.Clock().tick(30)


def skin_changer():
    global clock, scr, running, scrnow, skins_onacc
    current_skin_index = int(gamedb['Skin'])
    print(current_skin_index)
    # Главный игровой цикл
    while running and scrnow == SKINSCR:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                shutdown()
                break
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    current_skin_index = (current_skin_index + 1) % len(skins_pic)  # Переключение на следующий скин
                    gamedb['Skin'] = str(current_skin_index)
                elif event.key == pg.K_LEFT:
                    current_skin_index = (current_skin_index - 1) % len(skins_pic)  # Переключение на предыдущий скин
                    gamedb['Skin'] = str(current_skin_index)
                elif event.key == pg.K_ESCAPE:
                    scrnow = MAINSCR
            if event.type == pg.MOUSEBUTTONUP:
                cor = event.pos
                if cor[0] <= 60 and 20 <= cor[1] <= 40:
                    scrnow = MAINSCR
                if cor[0] >= 570 and 20 <= cor[1] <= 40:
                    scrnow = SHOPSCR
                if 260 <= cor[0] <= 320 and 300 <= cor[1] <= 360:
                    current_skin_index = (current_skin_index - 1) % len(skins_pic)
                    gamedb['Skin'] = str(current_skin_index)  # Переключение на предыдущий скин
                if 390 <= cor[0] <= 550 and 300 <= cor[1] <= 360:
                    current_skin_index = (current_skin_index + 1) % len(skins_pic)  # Переключение на следующий скин
                    gamedb['Skin'] = str(current_skin_index)
        # Отображение фона
        scr.fill((255, 255, 255))  # Белый фон
        bg = BGTEXTURES['back']
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
                            gamedb['Money'] = str(money)
                            skins_pic.append(pg.transform.scale(pg.image.load(f'assets/textures/player/loki.png'),
                                                                (int(100 * 3), int(100 * 3))))
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")
                    elif gamedb['LB'] == '1' and gamedb["MexB"] == '0':
                        if money >= MEXICANES:
                            gamedb["MexB"] = '1'
                            money -= MEXICANES
                            gamedb['Money'] = str(money)
                            skins_pic.append(pg.transform.scale(pg.image.load(f'assets/textures/player/mexicanes.png'),
                                                                (int(100 * 3), int(100 * 3))))
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")
                if 300 <= cor[0] <= 490 and 70 <= cor[1] <= 360:
                    if gamedb['WB'] == '0':
                        if money >= WARRIOR:
                            gamedb["WB"] = '1'
                            money -= WARRIOR
                            gamedb['Money'] = str(money)
                            skins_pic.append(pg.transform.scale(pg.image.load(f'assets/textures/player/warrior.png'),
                                                                (int(100 * 3), int(100 * 3))))
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")
                    elif gamedb['WB'] == '1' and gamedb["ShrekB"] == '0':
                        if money >= SHREK:
                            gamedb["ShrekB"] = '1'
                            money -= SHREK
                            gamedb['Money'] = str(money)
                            skins_pic.append(pg.transform.scale(pg.image.load(f'assets/textures/player/shrek.png'),
                                                                (int(100 * 3), int(100 * 3))))
                        else:
                            print("НЕДОСТАТОЧНО ДЕНЕГ")

        # Отображение фона
        scr.fill((255, 255, 255))  # Белый фон
        bg = BGTEXTURES['back']
        bg = pg.transform.rotozoom(bg, 0, 1.4)

        # Отображение текущего скина
        scr.blit(bg, (0, 0))
        if gamedb['LB'] == '0':
            scr.blit(skins_pic1[1], (20, 50))
        if gamedb['WB'] == '0':
            scr.blit(skins_pic1[2], (300, 50))
        if gamedb['LB'] == '1' and gamedb['MexB'] == '0':
            scr.blit(skins_pic1[3], (20, 50))
        if gamedb['WB'] == '1' and gamedb['ShrekB'] == '0':
            scr.blit(skins_pic1[4], (300, 50))
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
running = True
scrnow = MAINSCR

# настройка
clock = pg.time.Clock()
ldb = LocalDB(LDBFILE)
gamedb = ldb.get_all()

ballamount = 0

'''gamedb['WB'] = '0'
gamedb['LB'] = '0'
gamedb["MexB"] = '0'
gamedb["ShrekB"] = '0'
gamedb['Money'] = '0'
gamedb['Skin'] = '0'
gamedb['Money'] = '100'''
money = int(gamedb['Money'])
if gamedb['LB'] == '1':
    skins_onacc.append(LOKI_SKIN)
if gamedb['WB'] == '1':
    skins_onacc.append(WARRIOR_SKIN)
if gamedb['MexB'] == '1':
    skins_onacc.append(MEXICAN_SKIN)
if gamedb['ShrekB'] == '1':
    skins_onacc.append(SHREK_SKIN)

# игровой цикл
loading_screen()  # загрузим ресурсы игры

horwalls = pg.sprite.Group()
vertwalls = pg.sprite.Group()
ballgroup = pg.sprite.Group()
gameboard = Board((41, 41), (7, 14), 40, FIELDTEXTURES['captured'], FIELDTEXTURES['capture'],
                  FIELDTEXTURES['ballfield'], PLAYERTEXTURES[skin_check(gamedb['Skin'])],
                  ballgroup, horwalls, vertwalls)
gameboard.deathfunc = death_func

skins_pic = [pg.transform.scale(pg.image.load(f'assets/textures/player/{skin_file}'),
                                    (int(100 * 3), int(100 * 3))) for skin_file in skins_onacc]
skins_pic1 = [pg.transform.scale(pg.image.load(f'assets/textures/player/{skin_file}'),
                                   (int(100 * 3), int(100 * 3))) for skin_file in skins_ingame]

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
    elif scrnow == GAMEOVERSCR:
        game_over_screen()