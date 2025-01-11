import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, text: str, center: tuple[int, int], size: tuple[int, int], *group):
        super().__init__(*group)
        self.text = text
        self.center = center
        self.size = size
        self.surface = pg.Surface(size)
        self.rect.x = int(center[0] - size[0] / 2)
        self.rect.y = int(center[1] - size[1] / 2)


    def render(self):
        pass

    def update(self):
        pass

    def check_click(self, coords: tuple[int, int]):
        w, h = self.size
        x, y = self.center
        x1, y1 = coords
        return True if x - w / 2 <= x1 <= x + w / 2 and y - h / 2 <= y1 <= y + h / 2 else False