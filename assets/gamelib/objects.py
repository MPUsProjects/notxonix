import pygame as pg
import assets.gamelib.const


CELLVOID = 1  # поле шарика
CELLFIELD = 2  # поле игрока
CELLTRAIL = 3  # след игрока


# технические классы
class Cell:
    def __init__(self, board, bcoords: tuple[int, int], cellstate=CELLVOID, playerhere=False):
        self.board = board
        self.row = bcoords[0]
        self.col = bcoords[1]
        self.cell = cellstate
        self.playerhere = playerhere

    def get_cell_state(self):
        return self.cell

    def set_cell_state(self, newstate):
        self.cell = newstate

    def is_player(self):
        return self.playerhere

    def set_player_state(self, newstate: bool):
        self.playerhere = newstate


class Board:
    def __init__(self, origin: tuple[int, int], size: tuple[int, int], cellsize: int, field_texture: pg.Surface,
                 trail_texture: pg.Surface, void_texture: pg.Surface):
        self.field_texture = field_texture
        self.trail_texture = trail_texture
        self.void_texture = void_texture
        self.cellsize = cellsize
        self.bsize = size
        self.board = list(map(lambda x: list(map(lambda y: Cell(self, (x, y)), range(size[1]))), range(size[0])))
        self.origin = origin

    def read_file(self, file):
        with open(file) as f:
            self.board = list(map(lambda x: list(map(lambda y: None, x)), f.readlines()))

    def __create_cell(self, coords: tuple[int, int], cellcode: str):
        if cellcode == assets.gamelib.const.__CELLPLAYER:
            return Cell(self, coords, CELLFIELD, True)
        if cellcode == assets.gamelib.const.__CELLVOID:
            return Cell(self, coords, CELLVOID)
        if cellcode == assets.gamelib.const.__CELLFIELD:
            return Cell(self, coords, CELLFIELD)

    def __set_standart_board(self):
        pass

    def draw(self, scr: pg.Surface):
        for i in range(self.bsize[1]):
            for j in range(self.bsize[0]):
                if self.board[j][i].get_cell_state() == CELLFIELD:
                    scr.blit(self.field_texture, (self.origin[0] + self.cellsize * i,
                                                  self.origin[1] + self.cellsize * j))
                elif self.board[j][i].get_cell_state() == CELLTRAIL:
                    scr.blit(self.trail_texture, (self.origin[0] + self.cellsize * i,
                                                  self.origin[1] + self.cellsize * j))
                elif self.board[j][i].get_cell_state() == CELLVOID:
                    scr.blit(self.void_texture, (self.origin[0] + self.cellsize * i,
                                                 self.origin[1] + self.cellsize * j))

    def on_board_coords(self, coords: tuple[int, int]):
        '''Возвращает координаты точки относительно клеток поля Board в виде (№строки, №столбца)'''
        if (self.origin[0] <= coords[0] < self.origin[0] + self.cellsize * self.bsize[1] and
                self.origin[0] <= coords[1] < self.origin[1] + self.cellsize * self.bsize[0]):
            return ((coords[1] - self.origin[1]) // self.cellsize, (coords[0] - self.origin[0]) // self.cellsize)
        return None


class Player:
    def __init__(self, board):
        self.board = board

    def move(self, key_pressed):
        pass


# "Визуальные" классы
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