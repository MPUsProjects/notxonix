import pygame as pg

import assets.gamelib.const
from sqlite3 import connect as sqlconnect
from assets.gamelib.const import *
from requests import get as reqget, post as reqpost
from requests.exceptions import InvalidSchema, RequestException
from werkzeug.security import generate_password_hash
from json import dumps as to_json


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

        bcoords = self.board.on_board_coords((self.rect.x, self.rect.y))
        '''if self.board.board[bcoords[0]][bcoords[1]].is_player():
            standart_death_func()'''


"self.image = skin_check(gamedb['Skin'])"  # для отображения картинки скина


# "Визуальные" классы
# НАЧАЛО НОВОГО КОДА
class Button:
    def __init__(self, screen: pg.Surface, text: pg.Surface, surface: pg.Surface, center: tuple[int, int]):
        self.center = center
        self.surface = surface
        self.scr = screen
        self.size = self.surface.get_size()
        self.text = text

    def update(self):
        self.scr.blit(self.surface, self.surface.get_rect(center=self.center))
        self.scr.blit(self.text, self.text.get_rect(center=self.center))

    def check_click(self, coords: tuple[int, int]):
        w, h = self.size
        x, y = self.center
        x1, y1 = coords
        return x - (w // 2) + 1 <= x1 <= x + (w // 2) and y - (h // 2) + 1 <= y1 <= y + (h // 2)


class TextInput:
    def __init__(self, screen: pg.Surface, coords: tuple[int, int], size: tuple[int, int], font: pg.font.Font,
                 inactive_color: pg.Color, active_color: pg.Color,  inactive_text: str, inactive_text_color: pg.Color,
                 text_color: pg.Color, allowed_symbols: str = None, max_symbols: int = -1, hidden: bool = False):
        self.scr = screen
        self.coords = coords
        self.size = size
        self.font = font
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.inactive_text = inactive_text
        self.text = ''
        self.inactive_text_color = inactive_text_color
        self.text_color = text_color
        self.allowed_symb = allowed_symbols
        self.maxlen = max_symbols
        self.hidden = hidden

        self.active = False

    def update(self):
        surf = pg.Surface(self.size)
        surf.fill((0, 0, 0))
        inpsurf = pg.Surface((self.size[0] - 2, self.size[1] - 2))
        if self.active:
            inpsurf.fill(self.active_color)
        else:
            inpsurf.fill(self.inactive_color)
        surf.blit(inpsurf, (1, 1))
        if self.text:
            if self.hidden:
                text = self.font.render('*' * len(self.text), False, self.text_color)
            else:
                text = self.font.render(self.text, False, self.text_color)
        else:
            text = self.font.render(self.inactive_text, False, self.inactive_text_color)
        surf.blit(text, (2, 2))
        self.scr.blit(surf, surf.get_rect(center=self.coords))

    def check_click(self, mousecoords):
        mx, my = mousecoords
        sx, sy = self.size
        x, y = self.coords
        if x - (sx // 2) + 1 <= mx <= x + (sx // 2) and y - (sy // 2) + 1 <= my <= y + (sy // 2):
            self.active = True
            return True
        else:
            self.active = False
            return False

    def backspace(self):
        if self.active and self.text:
            self.text = self.text[:-1]

    def add_symbol(self, symbol: str):
        if self.active:
            checker = True
            if self.allowed_symb is not None:
                checker = checker and symbol.lower() in self.allowed_symb
            if self.maxlen >= 0:
                checker = checker and len(self.text) <= self.maxlen - 1

            if checker:
                self.text += symbol

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear(self):
        self.text = ''

    def copy(self):
        return TextInput(self.scr, self.coords, self.size, self.font, self.inactive_color, self.active_color,
                         self.inactive_text, self.inactive_text_color, self.text_color, self.allowed_symb, self.maxlen)
# КОНЕЦ НОВОГО КОДА


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

    # НАЧАЛО НОВОГО КОДА
    def saveone(self, key: str, value: str):
        if len(self.db.execute(f"""SELECT key FROM datatable WHERE key = '{key}'""").fetchall()) > 0:
            self.db.execute(f"""UPDATE datatable SET value = '{value}' WHERE key = '{key}'""")
        else:
            self.db.execute(f"""INSERT INTO datatable(key, value) VALUES('{key}', '{value}')""")
        self.connectobj.commit()
    # КОНЕЦ НОВОГО КОДА

    def close(self):
        self.connectobj.close()


# НАЧАЛО НОВОГО КОДА
# Объект связки облачной базы данных с локальной, а также
# позволяющий войти в аккаунт
class CloudDB:
    def __init__(self, api_address: str, loginapi_address: str, check_address: str, localdb: LocalDB, gamedb: dict):
        self.api_address = api_address
        self.api_login_address = loginapi_address
        self.check_address = check_address
        self.ldb = localdb
        self.gamedb = gamedb

    def check_connection(self):
        """try:
            reqget(self.check_address).ok
            return True
        except InvalidSchema:
            return False
        except RequestException:
            return False"""
        reqget(self.check_address)
        return True

    def get(self):
        if self.check_connection():
            json_request = {'username': self.gamedb['username'],
                            'pwdhash': self.gamedb['pwdhash']}
            try:
                res = reqget(self.api_address, json=json_request)
                if res.status_code == 403:
                    return None
                else:
                    return res.json()
            except RequestException:
                return None
        else:
            return None

    def save(self, data: dict):
        if self.check_connection():
            dat = data.copy()
            del dat['username']
            del dat['pwdhash']
            del dat['logged_in']
            json_request = {'username': self.gamedb['username'],
                            'pwdhash': self.gamedb['pwdhash'],
                            'data': dat}
            res = reqpost(self.api_address, json=json_request)
            if res.status_code == 403:
                return False
            return True
        else:
            print('something went wrong')
            return False

    def get_to_ldb(self):
        res = self.get()
        if res is not None:
            self.ldb.save(res)
            self.gamedb = self.ldb.get_all()
            return True
        else:
            return False

    def save_from_ldb(self):
        return self.save(self.gamedb)

    def login(self, username, password):
        if self.check_connection():
            pwdhash = password
            reqres = reqget(self.api_login_address, json={
                'username': username,
                'pwdhash': pwdhash
            }).json()
            if reqres == '1':
                self.gamedb['username'] = username
                self.gamedb['pwdhash'] = pwdhash
                self.gamedb['logged_in'] = '1'
                self.ldb.save(self.gamedb)
                return True
            else:
                return False
        else:
            print('something went wrong')
            return False

    # Единственная функция CloudDB без веб-запросов - выход из аккаунта
    # (локальная база данных "забывает" об аккаунте)
    def unlogin(self):
        self.gamedb['username'] = ''
        self.gamedb['pwdhash'] = ''
        self.gamedb['logged_in'] = '0'
        self.ldb.save(self.gamedb)
# КОНЕЦ НОВОГО КОДА


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
    num = str(num)
    if num == gamedb['Main']:
        return 'main_hero'
    elif num == gamedb['Warrior']:
        return 'warrior'
    elif num == gamedb['Loki']:
        return 'loki'
    elif num == gamedb['Mexicanes']:
        return 'mexicanes'
    elif num == gamedb['Shrek']:
        return 'shrek'


ldb = LocalDB(LDBFILE)
gamedb = ldb.get_all()