import pygame as pg

# setup
pg.init()
scr = pg.display.set_mode((640, 360))
clock = pg.time.Clock()
running = True
menu = True

# load font
font = pg.font.SysFont('Arial', 32)

# load text
close = font.render("exit", 0, (255, 255, 255))

# game code
while running:
    bg = pg.image.load('background_menu_movable.jpg')

    pg.display.update()
    clock.tick(60)
pg.quit()