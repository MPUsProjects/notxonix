import pygame as pg
from random import randint, randrange


class Ball(pg.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color("red"), (radius, radius), radius)
        self.rect = pg.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


# инициализация
pg.init()
scr = pg.display.set_mode((640, 360))
pg.display.set_caption('𝕭𝖆𝖑𝖑𝖘')
radius = 50
image = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA, 32)
pg.draw.circle(image, pg.Color("red"), (radius, radius), radius)
pg.display.set_icon(image)

# настройка
width, height = scr.get_size()
clock = pg.time.Clock()
horizontal_borders = pg.sprite.Group()
vertical_borders = pg.sprite.Group()
Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
balls = pg.sprite.Group()
for i in range(20):
    balls.add(Ball(20, 100, 100))


# рабочий цикл
running = True
while running:
    # технический блок
    scr.fill('white')
    time = clock.tick(100)

    # updates
    horizontal_borders.draw(scr)
    vertical_borders.draw(scr)
    balls.draw(scr)
    balls.update()

    # Real code
    pass

    # технический блок
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
            break
        elif event.type == pg.MOUSEBUTTONDOWN:
            balls.add(Ball(20, event.pos[0], event.pos[1]))