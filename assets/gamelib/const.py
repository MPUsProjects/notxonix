import pygame as pg
# базовые
APPNAME = 'Notxonix'
APPVER = 'indev-20250128'

# технические
MAINSCR = 1
GAMESCR = 2
SHOPSCR = 3

# скины
skinns = ['loki.png', 'main_hero.png', 'warrior.png']
skins = [pg.transform.scale(pg.image.load(skin_file), (int(100 * 3), int(100 * 3)))
         for skin_file in skinns]
current_skin_index = 0

# cellcodes
__CELLPLAYER = '@'
__CELLVOID = '.'
__CELLFIELD = '#'