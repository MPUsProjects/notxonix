import pygame as pg

import assets.gamelib.const
from sqlite3 import connect as sqlconnect
from assets.gamelib.const import *
from requests import get as reqget, post as reqpost, RequestException


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


# класс доски (технические классы)
def standart_death_func():
    global STATUS
    STATUS = 0


class Board:
    def __init__(self, origin: tuple[int, int], size: tuple[int, int], cellsize: int, field_texture: pg.Surface,
                 trail_texture: pg.Surface, void_texture: pg.Surface, player_texture: pg.Surface,
                 ballspritegroup: pg.sprite.Group, horwallspritegroup: pg.sprite.Group,
                 vertwallspritegroup: pg.sprite.Group):
        self.field_texture = field_texture
        self.trail_texture = trail_texture
        self.void_texture = void_texture
        self.cellsize = cellsize
        self.bsize = size
        self.board = list(map(lambda x: list(map(lambda y: Cell(self, (x, y)), range(size[1]))), range(size[0])))
        self.origin = origin

        self.playertexture = pg.Surface((40, 40))
        self.playertexture.fill((0, 255, 0))
        self.playertexture = player_texture
        self.deathfunc = standart_death_func
        self.playerpos = (0, 0)
        self.ballgroup = ballspritegroup
        self.horwallgroup = horwallspritegroup
        self.vertwallgroup = vertwallspritegroup

    def spawn_player(self):
        self.playerpos = (0, 0)

    def __create_cell(self, coords: tuple[int, int], cellcode: str = CELLVOID):
        if cellcode == CELLVOID:
            return Cell(self, coords, CELLVOID)
        if cellcode == CELLFIELD:
            return Cell(self, coords, CELLFIELD)

    def set_standart_board(self):
        self.board = list(map(lambda y: list(map(lambda x: self.__create_cell((y, x)), range(14))), range(7)))
        for i in range(14):
            self.board[0][i].set_cell_state(CELLFIELD)
            self.board[-1][i].set_cell_state(CELLFIELD)
        for j in range(1, 7):
            self.board[j][0].set_cell_state(CELLFIELD)
            self.board[j][-1].set_cell_state(CELLFIELD)
        self.board[0][0].set_player_state(True)
        self.new_walls()

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
                if self.board[j][i].is_player():
                    scr.blit(self.playertexture, (self.origin[0] + self.cellsize * i,
                                                  self.origin[1] + self.cellsize * j))

    def on_board_coords(self, coords: tuple[int, int]):
        '''Возвращает координаты точки относительно клеток поля Board в виде (№строки, №столбца)'''
        if (self.origin[0] <= coords[0] < self.origin[0] + self.cellsize * self.bsize[1] and
                self.origin[0] <= coords[1] < self.origin[1] + self.cellsize * self.bsize[0]):
            return (coords[1] - self.origin[1]) // self.cellsize, (coords[0] - self.origin[0]) // self.cellsize
        return None

    def on_screen_coords(self, bcoords: tuple[int, int]):
        '''bcoords: tuple[row, col]'''
        x = bcoords[1] * self.cellsize + self.origin[0]
        y = bcoords[0] * self.cellsize + self.origin[1]
        return (x, y)

    def set_player_pos(self, newpos: tuple[int, int]):
        '''newpos: tuple(row, col)'''
        if 0 <= newpos[0] < len(self.board) and 0 <= newpos[1] < len(self.board[0]):
            if self.board[newpos[0]][newpos[1]].get_cell_state() == CELLVOID:
                self.board[newpos[0]][newpos[1]].set_cell_state(CELLTRAIL)
            elif self.board[newpos[0]][newpos[1]].get_cell_state() == CELLTRAIL:
                self.deathfunc()
            elif (self.board[newpos[0]][newpos[1]].get_cell_state() == CELLFIELD and
                  self.board[self.playerpos[0]][self.playerpos[1]].get_cell_state() == CELLTRAIL):
                self.fill_new_territory()
                for row in self.board:
                    for cell in row:
                        if cell.get_cell_state() == CELLTRAIL:
                            cell.set_cell_state(CELLFIELD)
                self.new_walls()

            self.board[self.playerpos[0]][self.playerpos[1]].set_player_state(False)
            self.board[newpos[0]][newpos[1]].set_player_state(True)
            self.playerpos = newpos

    def move_player(self, row: int, col: int):
        '''-1 <= int(row) <= 1
        -1 <= int(col) <= 1'''
        self.set_player_pos((self.playerpos[0] + row, self.playerpos[1] + col))

    def new_walls(self):
        self.horwallgroup.empty()
        self.vertwallgroup.empty()
        for j in range(len(self.board)):
            for i in range(len(self.board[0])):
                if self.board[j][i].get_cell_state() != CELLFIELD:
                    continue

                if j >= 1 and self.board[j - 1][i].get_cell_state() == CELLVOID:
                    pos = self.on_screen_coords((j, i))
                    Wall(WALLHOR, pos, self.horwallgroup)
                if j < len(self.board) - 1 and self.board[j + 1][i].get_cell_state() == CELLVOID:
                    pos = self.on_screen_coords((j, i))
                    Wall(WALLHOR, (pos[0], pos[1] + self.cellsize - 1), self.horwallgroup)
                if i >= 1 and self.board[j][i - 1].get_cell_state() == CELLVOID:
                    pos = self.on_screen_coords((j, i))
                    Wall(WALLVERT, pos, self.vertwallgroup)
                if i < len(self.board[0]) - 1 and self.board[j][i + 1].get_cell_state() == CELLVOID:
                    pos = self.on_screen_coords((j, i))
                    Wall(WALLVERT, (pos[0] + self.cellsize - 1, pos[1]), self.vertwallgroup)

    def fill_new_territory(self):
        pass


# класс стены


WALLVERT = 1
WALLHOR = 2


class Wall(pg.sprite.Sprite):
    def __init__(self, orientation, position: tuple[int, int], wallgroup: pg.sprite.Group):
        super().__init__(wallgroup)
        self.orientation = orientation
        self.image = pg.Surface((40, 1) if orientation == WALLHOR else (1, 40))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def get_orientation(self):
        return self.orientation


class Ball(pg.sprite.Sprite):
    def __init__(self, balltexture: pg.Surface, pos: tuple[int, int], ballspritegroup: pg.sprite.Group,
                 horwallspritegroup: pg.sprite.Group, vertwallspritegroup: pg.sprite.Group, board):
        super().__init__(ballspritegroup)
        self.image = balltexture
        self.horwallgroup = horwallspritegroup
        self.vertwallgroup = vertwallspritegroup
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.board = board

        self.vx = 1
        self.vy = 1
        self.movetimer = 0

    def update(self):
        if pg.sprite.spritecollideany(self, self.horwallgroup):
            self.vy *= -1
        if pg.sprite.spritecollideany(self, self.vertwallgroup):
            self.vx *= -1

        self.movetimer += 1
        if self.movetimer >= 3:
            self.movetimer = 0
            self.rect.x += self.vx
            self.rect.y += self.vy

        bcoords = self.board.on_board_coords((self.rect.x + 20, self.rect.y + 20))
        '''if self.board.board[bcoords[0]][bcoords[1]].is_player():
            standart_death_func()'''


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
    def __init__(self, api_address: str, api_key: str, localdb: LocalDB = None):
        self.api_address = api_address
        self.api_key = api_key
        self.ldb = ldb

    def get(self):
        if reqget(self.api_address).ok:
            cdb_username = 'USERNAME'  # ВСТАВИТЬ СЮДА ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗ LDB
            json_request = {'api_key': self.api_key,
                            'game_id': CDB_GAME_ID,
                            'username': cdb_username}
            try:
                res = reqget(self.api_address, json=json_request).json()
                return res
            except RequestException:
                return None
        else:
            return None

    def save(self, data):
        if reqget(self.api_address).ok:
            cdb_username = 'USERNAME'  # ВСТАВИТЬ СЮДА ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗ LDB
            json_request = {'api_key': self.api_key,
                            'game_id': CDB_GAME_ID,
                            'username': cdb_username,
                            'data': data}
            reqpost(self.api_address, json=json_request)
            return True
        else:
            print('something went wrong')
            return False

    def get_to_ldb(self):
        if self.ldb is not None:
            pass

    def save_from_ldb(self):
        if self.ldb is not None:
            pass


"""
ценный сердцу код через firebase

import firebase_admin as fba
from firebase_admin import db
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
"""


def skin_check(num):
    if gamedb['Skin'] == gamedb['Loki']:
        return 'loki'
    elif gamedb['Skin'] == gamedb['Warrior']:
        return 'warrior'
    elif gamedb['Skin'] == gamedb['Main']:
        return 'main_hero'
    elif gamedb['Skin'] == gamedb['Mexicanes']:
        return 'mexicanes'
    elif gamedb['Skin'] == gamedb['Shrek']:
        return 'shrek'


ldb = LocalDB(LDBFILE)
gamedb = ldb.get_all()