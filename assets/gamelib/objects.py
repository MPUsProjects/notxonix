import pygame as pg
import firebase_admin as fba
from firebase_admin import db
import assets.gamelib.const
from sqlite3 import connect as sqlconnect
from assets.gamelib.const import *
import random

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


"self.image = skin_check(gamedb['Skin'])"  # для отображения картинки скина


# "Визуальные" классы
class Button(pg.sprite.Sprite):
    def __init__(self, text: str, center: tuple[int, int], size: tuple[int, int], *group):
        super().__init__(*group)
        self.text = text
        self.center = center
        self.size = size
        self.surface = pg.Surface(size)
        self.rect = pg.Rect((0, 0), (0, 0))
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


# Исполнительные классы
class LocalDB:
    def __init__(self, dbfile):
        self.connectobj = sqlconnect(dbfile)
        self.db = self.connectobj.cursor()

    def get(self, key):
        # Результат лишь один, т.к. ключ уникален по условию, прописанному в бд
        return self.db.execute(f"""SELECT value FROM datatable WHERE key = '{key}'""").fetchall()[0][0]

    def get_all(self):
        '''Возвращает словарь key: value, соответствующий базе данных'''
        return dict(self.db.execute("""SELECT key, value FROM datatable""").fetchall())

    def save(self, keyvaluedict: dict):
        for key in keyvaluedict.keys():
            value = keyvaluedict[key]
            # Проверка на существование - если есть такая ячейка, пишем в неё, иначе делаем новую
            if len(self.db.execute(f"""SELECT key FROM datatable WHERE key = '{key}'""").fetchall()) > 0:
                self.db.execute(f"""UPDATE datatable SET value = '{value}' WHERE key = '{key}'""")
            else:
                self.db.execute(f"""INSERT INTO datatable(key, value) VALUES('{key}', '{value}')""")
        self.connectobj.commit()  # коммитим изменения в бд, чтобы они вступили в силу

    def close(self):
        self.connectobj.close()


class CloudDB:
    def __init__(self):
        cred = fba.credentials.Certificate(assets.gamelib.const.DBCERT)
        self.default_app = fba.initialize_app(cred, {
            "databaseURL": assets.gamelib.const.DBURL
        })

    def get_rtdb(self, key):
        return db.reference(f'/{key}/').get()

    def write_rtdb(self, key, value):
        db.reference(f'/{key}/').set(value)

    def get_storage(self, name):
        pass

    def write_storage(self, name):
        pass


def skin_check(num):
    if num == '1':
        return assets.gamelib.const.LOKI_SKIN
    elif num == '2':
        return assets.gamelib.const.WARRIOR_SKIN
    elif num == '0':
        return assets.gamelib.const.MINER_SKIN
    elif num == '3':
        return assets.gamelib.const.MEXICAN_SKIN


ldb = LocalDB(LDBFILE)
gamedb = ldb.get_all()