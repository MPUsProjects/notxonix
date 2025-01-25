import pygame as pg
import os


PATH = 'assets/textures/'


def load_textures(type: str):
    textures = {}
    path = PATH + f'{type}/'
    for file in os.listdir(path):
        if os.path.isfile(path + file) and file.endswith('.png'):
            textures[f'{file[:-4]}'] = pg.image.load(path + file)
    return textures


def load_field_textures():
    return load_textures('field')


def load_wall_textures():
    return load_textures('wall')


def load_ball_textures():
    return load_textures('ball')


def load_player_textures():
    return load_textures('player')


def load_bg_textures():
    return load_textures('background')


def load_deco_textures():
    return load_textures('deco')