import pygame as pg
import sys

# setup
pg.init()
scr = pg.display.set_mode((640, 360))
clock = pg.time.Clock()
running = True
menu = True

scale_factor = 2

# Список скинов
skinns = ['ball1.png', 'ball2.png', 'ballpepsi.png']
print(skinns)
skins = [pg.transform.scale(pg.image.load(skin_file), (int(100 * scale_factor), int(100 * scale_factor)))
         for skin_file in skinns]
current_skin_index = 0

# Главный игровой цикл
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    # Изменение скина с помощью стрелок
    if keys[pg.K_RIGHT]:
        current_skin_index = (current_skin_index + 1) % len(skins)  # Переключение на следующий скин
    elif keys[pg.K_LEFT]:
        current_skin_index = (current_skin_index - 1 + len(skins)) % len(skins)  # Переключение на предыдущий скин

    # Отображение фона
    scr.fill((255, 255, 255))  # Белый фон
    bg = pg.image.load('background_menu_movable.jpg')

    # Отображение текущего скина
    current_skin = skins[current_skin_index]
    scr.blit(bg, (0, 0))
    scr.blit(current_skin, (640 // 2 - current_skin.get_width() // 2, 360 // 2 - current_skin.get_height() // 2))

    # Обновление дисплея
    pg.display.flip()

    # Ограничение FPS
    pg.time.Clock().tick(30)