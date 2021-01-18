import sys

import pygame as pg
import os

COLOR1 = (252, 221, 118)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.attack = 0
        self.building = 0
        self.attack_tank = []

        # создадим группу, содержащую все спрайты
        self.all_sprites = pg.sprite.Group()

    def render(self, sc):
        self.sc = sc
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pg.draw.rect(self.sc, COLOR1, (j * self.cell_size + self.left,
                                                   i * self.cell_size + self.left,
                                                   self.cell_size, self.cell_size))
                    pg.draw.rect(self.sc, (255, 255, 255), (j * self.cell_size + self.left,
                                                            i * self.cell_size + self.left,
                                                            self.cell_size, self.cell_size), 1)
                elif self.board[i][j] == 1:
                    pg.draw.rect(self.sc, (0, 0, 0), (j * self.cell_size + self.left,
                                                   i * self.cell_size + self.left,
                                                   self.cell_size, self.cell_size))
                    pg.draw.rect(self.sc, (255, 255, 255), (j * self.cell_size + self.left,
                                                            i * self.cell_size + self.left,
                                                            self.cell_size, self.cell_size), 1)
                elif self.board[i][j] == 2:
                    pg.draw.rect(self.sc, (255, 0, 0), (j * self.cell_size + self.left,
                                                   i * self.cell_size + self.left,
                                                   self.cell_size, self.cell_size))
                    pg.draw.rect(self.sc, (255, 255, 255), (j * self.cell_size + self.left,
                                                            i * self.cell_size + self.left,
                                                            self.cell_size, self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.width = 600 // self.cell_size
        self.height = 600 // self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        else:
            print('None')

    def get_cell(self, pos):
        pos_x, pos_y = pos
        if pos_x >= self.left and pos_y >= self.top:
            if pos_x <= (self.left + (self.cell_size * self.width)) and \
                    pos_y <= (self.top + (self.cell_size * self.height)):
                x_coord = pos_x - self.left
                y_coord = pos_y - self.top
                table_x = x_coord // self.cell_size
                table_y = y_coord // self.cell_size
                return tuple([table_x, table_y])
            return None
        return None

    def on_click(self, cell):
        if self.board[cell[1]][cell[0]] == 0 and self.building == 1:
            self.board[cell[1]][cell[0]] = 1
            self.attack = 0
        elif self.board[cell[1]][cell[0]] == 1 and self.attack == 1:
            self.board[cell[1]][cell[0]] = 0
            self.attack = 0
            self.board[self.attack_tank[1]][self.attack_tank[0]] = 1
        elif self.board[cell[1]][cell[0]] == 1 and self.attack == 0:
            self.board[cell[1]][cell[0]] = 2
            self.attack_tank = [cell[0], cell[1]]
            self.attack = 1
        elif self.board[cell[1]][cell[0]] == 1 and self.building == 1:
            self.board[cell[1]][cell[0]] = 0
            self.attack = 0

    def build(self):
        if self.building == 1:
            self.building = 0
        else:
            self.building = 1


def load_image_tanks(name, colorkey=None):
    fullname = os.path.join('data/textures/tanks_lvls', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('РЕВЕРСИ')
    size = width, height = 600, 600
    screen = pg.display.set_mode(size)

    fps = 30
    clock = pg.time.Clock()
    itera = 0

    board = Board(width // 30, height // 30)
    running = True
    while running:  # главный игровой цикл
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    board.get_click(event.pos)
                elif event.button == 3:
                    board.build()

        # формирование кадра
        screen.fill((0, 0, 0))
        board.render(screen)
        pg.display.flip()  # смена кадра

        # изменение игрового мира
        clock.tick(fps)
