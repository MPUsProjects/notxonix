import pygame as pg
import os


PATH = 'assets/textures/'


def load_textures(type: str, scale: int = -1):
    textures = {}
    path = PATH + f'{type}/'
    for file in os.listdir(path):
        if os.path.isfile(path + file) and file.endswith('.png'):
            img = pg.image.load(path + file)
            if scale > 0:
                img = pg.transform.scale(img, (scale, scale))
            textures[f'{file[:-4]}'] = img
    return textures


def load_field_textures():
    return load_textures('field', 40)


def load_wall_textures():
    return load_textures('wall', 40)


def load_ball_textures():
    return load_textures('ball', 40)


def load_player_textures():
    return load_textures('player', 40)


def load_bg_textures():
    return load_textures('background')


def load_deco_textures():
    return load_textures('deco')


def load_misc_textures():
    return load_textures('misc')
