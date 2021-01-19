import pygame as pg
import os


def music_play(self, name):
    fullname = os.path.join('data/textures/tanks_lvls', f'{name}.wav')
    sound = pg.mixer.Sound(fullname)
    sound.play()




# строки эти в инит поставь
fullname = os.path.join('data/music', 'M_M_T.wav')
pg.mixer.music.load(fullname)
pg.mixer.music.play(-1)


# а вот эту в начало самой игры
pg.mixer.music.stop()
