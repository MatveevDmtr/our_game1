import pygame
from PIL import Image
SCREEN_SIZE = 1250, 700
clock = pygame.time.Clock()
velocity = 1000
fps = 60
num_cells_in_line = 20
size_of_cell = (SCREEN_SIZE[1] - 70) // num_cells_in_line
immediate_quit = False
MONEY_P_1 = 100000
MONEY_P_2 = 100000



sprite_group_weapons = pygame.sprite.Group()


base = pygame.sprite.Sprite(sprite_group_weapons)
base.cost = 2000
base.type_of_weapon = 'База'
base.full_hp = 100
base.hp = base.full_hp
base.attack_radius = 20
base.harm_koef = 1
base.speed = 0
base.level = 1
base.image = 'player2_base.png'


# Инициализация параметров танка
tank = pygame.sprite.Sprite(sprite_group_weapons)
tank.cost = 2000
tank.type_of_weapon = 'Танк'
tank.full_hp = 100
tank.hp = tank.full_hp
tank.attack_radius = 10
tank.harm_koef = 1
tank.speed = 5
tank.level = 1
tank.image = 'tank.png'

artillery = pygame.sprite.Sprite(sprite_group_weapons)
artillery.cost = 1000
artillery.type_of_weapon = 'Артиллерия'
artillery.full_hp = 100
artillery.hp = artillery.full_hp
artillery.attack_radius = 20
artillery.harm_koef = 1
artillery.speed = 1
artillery.level = 1
artillery.image = 'artillery.png'

men = pygame.sprite.Sprite(sprite_group_weapons)
men.cost = 100
men.type_of_weapon = 'Пехота'
men.full_hp = 100
men.hp = men.full_hp
men.attack_radius = 20
men.harm_koef = 1
men.speed = 1
men.level = 1
men.image = 'men.png'

rocket = pygame.sprite.Sprite(sprite_group_weapons)
rocket.cost = 100
rocket.type_of_weapon = 'Ракетница'
rocket.full_hp = 100
rocket.hp = rocket.full_hp
rocket.attack_radius = 20
rocket.harm_koef = 1
rocket.speed = 1
rocket.level = 1
rocket.image = 'rocket.png'

alpha = pygame.sprite.Sprite(sprite_group_weapons)
alpha.cost = 100
alpha.type_of_weapon = 'Спецназ'
alpha.full_hp = 100
alpha.hp = alpha.full_hp
alpha.attack_radius = 20
alpha.harm_koef = 1
alpha.speed = 1
alpha.level = 1
alpha.image = 'men.png'
# Инициализация параметров ПВО


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.top = to_center_text_in_horizontal(SCREEN_SIZE[1] - 70, 0, SCREEN_SIZE[1])
        self.cell_size = size_of_cell
        self.left = to_center_text_in_horizontal(SCREEN_SIZE[1] - 70, 0, SCREEN_SIZE[0])

    def redraw_board(self):
        board.render(screen)

    def add_elem(self, sprite, cell, player):
        self.board[cell[1]][cell[0]] = Weapon(sprite, screen,
                                              (self.left + cell[0] * self.cell_size, self.top + cell[1] * self.cell_size), player, sprite_group_weapons)

    def remove_elem(self, cell):
        removing_elem = self.board[cell[1]][cell[0]]
        self.board[cell[1]][cell[0]] = 0
        return removing_elem

    def insert_elem(self, elem, cell):
        self.board[cell[1]][cell[0]] = elem

    def reverse_board(self):
        list_x = []
        for i in range(self.height - 1, -1, -1):
            list_x.append(self.board[i])
        self.board = list_x
        for line in self.board:
            for elem in line:
                if elem != 0:
                    elem.location = (elem.location[0], 2 * self.top + (self.height - 1) * self.cell_size - elem.location[1])
                    elem.side = (elem.side + 2) % 4
                    elem.default_side = (elem.default_side + 2) % 4
                    elem.image = elem.rotate_center(elem.image, elem.location, 180)[0]

    def find_way(self, cell_1, cell_2):
        def is_digit(elem):
            if elem in range(-1, 100):
                return True
            return False
        print('before', self.board)
        board_of_searching = []
        for i in range(len(self.board)):
            list_x = []
            for j in range(len(self.board[i])):
                list_x.append(self.board[i][j])
            board_of_searching.append(list_x)
        for i in range(self.height):
            for j in range(self.width):
                if board_of_searching[i][j] == 0:
                    board_of_searching[i][j] = -1
                if (i, j) == cell_1:
                    board_of_searching[i][j] = 0
        last_numbered = [cell_1]
        not_found = True
        inserting_number = 1
        while not_found:
            list_x = []
            if last_numbered:
                for elem in last_numbered:
                    if elem[1] > 0 and board_of_searching[elem[0]][elem[1] - 1] == -1:
                        board_of_searching[elem[0]][elem[1] - 1] = inserting_number
                        list_x.append((elem[0], elem[1] - 1))
                    if elem[1] < self.height - 1 and board_of_searching[elem[0]][elem[1] + 1] == -1:
                        board_of_searching[elem[0]][elem[1] + 1] = inserting_number
                        list_x.append((elem[0], elem[1] + 1))
                    if elem[0] > 0 and board_of_searching[elem[0] - 1][elem[1]] == -1:
                        board_of_searching[elem[0] - 1][elem[1]] = inserting_number
                        list_x.append((elem[0] - 1, elem[1]))
                    if elem[0] < self.width - 1 and board_of_searching[elem[0] + 1][elem[1]] == -1:
                        board_of_searching[elem[0] + 1][elem[1]] = inserting_number
                        list_x.append((elem[0] + 1, elem[1]))
                    last_numbered = list_x
                    if (elem[0], elem[1] - 1) == cell_2 or \
                            (elem[0], elem[1] + 1) == cell_2 or \
                            (elem[0] - 1, elem[1]) == cell_2 or \
                            (elem[0] + 1, elem[1]) == cell_2:
                        not_found = False
                        break
            else:
                return False
            inserting_number += 1
        for line in board_of_searching:
            for elem in line:
                if str(elem)[-1].isdigit():
                    print(elem, end=' ')
                else:
                    print('p', end=' ')
            print()
        not_found = True
        cell_now = cell_2
        list_way = [cell_2]
        while not_found:
            if cell_now == cell_1:
                break
            cell_now_contents = board_of_searching[cell_now[0]][cell_now[1]]
            print(cell_now_contents)
            print(is_digit(cell_now_contents))
            if is_digit(board_of_searching[cell_now[0] - 1][cell_now[1]]) and board_of_searching[cell_now[0] - 1][cell_now[1]] == cell_now_contents - 1:
                list_way.append((cell_now[0] - 1, cell_now[1]))
                cell_now = (cell_now[0] - 1, cell_now[1])
            elif is_digit(board_of_searching[cell_now[0] + 1][cell_now[1]]) and board_of_searching[cell_now[0] + 1][cell_now[1]] == cell_now_contents - 1:
                list_way.append((cell_now[0] + 1, cell_now[1]))
                cell_now = (cell_now[0] + 1, cell_now[1])
            elif is_digit(board_of_searching[cell_now[0]][cell_now[1] - 1]) and board_of_searching[cell_now[0]][cell_now[1] - 1] == cell_now_contents - 1:
                list_way.append((cell_now[0], cell_now[1] - 1))
                cell_now = (cell_now[0], cell_now[1] - 1)
            elif is_digit(board_of_searching[cell_now[0]][cell_now[1]] + 1) and board_of_searching[cell_now[0]][cell_now[1] + 1] == cell_now_contents - 1:
                list_way.append((cell_now[0], cell_now[1] + 1))
                cell_now = (cell_now[0], cell_now[1] + 1)
        print(list_way)
        list_way.reverse()
        print('after way', self.board)
        return list_way

    def cross_cell_border(self, weapon, cell_1, cell_2):
        delta = 3
        start_location = weapon.location
        if cell_1[0] - cell_2[0] == 1:
            side_to_turn = 4
            delta1, delta2 = (-1) * delta, 0
        elif cell_2[0] - cell_1[0] == 1:
            side_to_turn = 2
            delta1, delta2 = delta, 0
        elif cell_1[1] - cell_2[1] == 1:
            side_to_turn = 1
            delta1, delta2 = 0, (-1) * delta
        elif cell_2[1] - cell_1[1] == 1:
            side_to_turn = 3
            delta1, delta2 = 0, delta
        weapon.turning_weapon(side_to_turn)
        while abs(weapon.location[0] - start_location[0]) < board.cell_size - 3 and abs(weapon.location[1] - start_location[1]) < board.cell_size - 3:
            weapon.location = (weapon.location[0] + delta1, weapon.location[1] + delta2)
            self.redraw_board()
            clock.tick(velocity / fps)
        weapon.location = (start_location[0] + (delta1 // 3) * self.cell_size, start_location[1] + (delta2 // 3) * self.cell_size)

    def move_weapon(self, cell_1, cell_2):
        weapon = self.board[cell_1[1]][cell_1[0]]
        print(weapon.speed)
        if abs(cell_2[0] - cell_1[0]) <= weapon.speed and abs(cell_2[1] - cell_1[1]) <= weapon.speed:
            way = self.find_way(cell_1, cell_2)
            if way:
                for i in range(len(way) - 1):
                    self.cross_cell_border(weapon, way[i], way[i + 1])
                weapon.turning_weapon(weapon.default_side)
                board.remove_elem(cell_1)
                board.insert_elem(weapon, cell_2)
            else:
                write_to_console('Невозможно найти путь в указанную клетку')
        else:
            write_to_console('Вашим войскам не хватает скорости, чтобы преодолеть это расстояние!')

    def attack(self, cell_1, cell_2):
        attacking_weapon = self.board[cell_1[1]][cell_1[0]]
        attacked_weapon = self.board[cell_2[1]][cell_2[0]]
        if cell_1 != cell_2 and attacking_weapon.attack_radius > abs(cell_2[0] - cell_1[0]) and attacking_weapon.attack_radius > abs(cell_2[1] - cell_1[1]):
            vertical = False
            side_to_turn = 1
            if (cell_1[0] - cell_2[0]) == 0:
                vertical = True
                if cell_2[1] - cell_1[1] > 0:
                    side_to_turn = 3
                else:
                    side_to_turn = 1
            elif cell_2[1] - cell_1[1] == 0:
                if cell_2[0] - cell_1[0] > 0:
                    side_to_turn = 2
                else:
                    side_to_turn = 4
                tan_alpha = (cell_1[1] - cell_2[1]) / (cell_1[0] - cell_2[0])
            else:
                tan_alpha = (cell_1[1] - cell_2[1]) / (cell_1[0] - cell_2[0])
            if cell_2[0] - cell_1[0] > 0 and cell_2[1] - cell_1[1] > 0:
                if tan_alpha >= 1:
                    side_to_turn = 2
                else:
                    side_to_turn = 3
            elif cell_2[0] - cell_1[0] > 0 and cell_2[1] - cell_1[1] < 0:
                if tan_alpha >= -1:
                    side_to_turn = 2
                else:
                    side_to_turn = 1
            elif cell_2[0] - cell_1[0] < 0 and cell_2[1] - cell_1[1] > 0:
                if tan_alpha >= -1:
                    side_to_turn = 4
                else:
                    side_to_turn = 3
            elif cell_2[0] - cell_1[0] < 0 and cell_2[1] - cell_1[1] < 0:
                if tan_alpha >= 1:
                    side_to_turn = 1
                else:
                    side_to_turn = 4
            print('side to turn', side_to_turn)
            attacking_weapon.turning_weapon(side_to_turn)
            delta = self.cell_size // 2
            if side_to_turn == 1:
                delta1, delta2 = delta, 0
            elif side_to_turn == 2:
                delta1, delta2 = 2 * delta, delta
            elif side_to_turn == 3:
                delta1, delta2 = delta, 2 * delta
            elif side_to_turn == 4:
                delta1, delta2 = 0, delta
            start_point_x = self.left + cell_1[0] * self.cell_size + delta1
            start_point_y = self.top + cell_1[1] * self.cell_size + delta2
            end_point_x = self.left + cell_2[0] * self.cell_size + delta
            end_point_y = self.top + cell_2[1] * self.cell_size + delta
            if cell_2[0] - cell_1[0] > 0:
                right_side = 1
            else:
                right_side = -1
            i = 0
            x = start_point_x
            y = start_point_y
            print(start_point_x, start_point_y, end_point_x, end_point_y)
            if vertical:
                if cell_2[1] - cell_1[1] > 0:
                    right_side = 1
                else:
                    right_side = -1
                while i < abs(start_point_x - end_point_x):
                    y += right_side * (delta // 2)
                    self.draw_bullet((x, y))
                    i += delta // 2
                    clock.tick(velocity / fps)
            else:
                while i < abs(start_point_x - end_point_x):
                    x += right_side * (delta // 2)
                    y += right_side * (delta // 2) * tan_alpha
                    if y in range(board.top, board.top + board.height * board.cell_size):
                        self.draw_bullet((x, y))
                    i += delta // 2
                    clock.tick(velocity / fps)
            attacked_weapon.damage(attacking_weapon.harm_koef * (attacking_weapon.attack_radius - ((abs(cell_2[0] - cell_1[0]) + abs(cell_2[1] - cell_1[1])) // 2)), cell_2)
            attacking_weapon.turning_weapon(attacking_weapon.default_side)
            board.redraw_board()
        else:
            write_to_console('Расстояние превышает радиус атаки или вы пытаетесь выстрелить по своим')

    def draw_bullet(self, location):
        self.redraw_board()
        pygame.draw.circle(screen, pygame.Color('red'), location, self.cell_size // 8)
        pygame.display.flip()

    def render(self, screen):
        print('render')
        background = Image.open('sand_board_1.jpg')
        background = background.resize((self.width * self.cell_size, self.height * self.cell_size), Image.ANTIALIAS)
        blit_pil_image(screen, background, (self.left, self.top))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', pygame.Rect(self.left + j * self.cell_size,
                                                              self.top + i * self.cell_size,
                                                              self.cell_size, self.cell_size), width=3)
        pygame.display.flip()
        for line in self.board:
            for element in line:
                if element != 0:
                    element.show_image()
        pygame.display.flip()

    def get_cell(self, pos):
        if pos[1] > self.top + self.height * self.cell_size or pos[1] < self.top or \
                pos[0] > self.left + self.width * self.cell_size or pos[0] < self.left:
            x, y = -1, -1
        else:
            y = (pos[1] - self.top) / self.cell_size
            if y % 1 == 0:
                y = y // 1 - 1
            else:
                y //= 1
            x = (pos[0] - self.left) / self.cell_size
            if x % 1 == 0:
                x = x // 1 - 1
            else:
                x //= 1
        return int(x), int(y)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell == (-1, -1):
            print('None')
        else:
            print(cell)
        self.answer_click(cell)

    def answer_click(self, cell):
        pygame.draw.rect(screen, 'green', pygame.Rect(self.left + cell[0] * self.cell_size,
                                                      self.top + cell[1] * self.cell_size,
                                                      self.cell_size, self.cell_size), width=3)
        pygame.display.flip()


class Buttons_in_game_process():
    def __init__(self):
        self.font_size = 28

    def draw_next_step_button(self):
        font_color = pygame.Color('yellow')
        font = pygame.font.Font(None, self.font_size)
        text = font.render('Следующий ход', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        self.button_next_step_left = to_center_text_in_horizontal(text_w, board.left + num_cells_in_line * size_of_cell, SCREEN_SIZE[0])
        self.button_next_step_top = board.top + board.height * board.cell_size - text_h - 7
        screen.fill(pygame.Color('blue'),
                    pygame.Rect(self.button_next_step_left - 10, self.button_next_step_top - 5, text_w + 20,
                                text_h + 10))
        screen.blit(text, (self.button_next_step_left, self.button_next_step_top))
        self.button_next_step_location = (self.button_next_step_left - 10, self.button_next_step_top - 5, self.button_next_step_left + text_w + 10,
                                self.button_next_step_top + text_h + 5)
        pygame.display.flip()

    def draw_add_buttons(self):
        size_of_font_add_buttons = 20
        font_color = pygame.Color('yellow')
        font = pygame.font.Font(None, size_of_font_add_buttons)
        texts = [f'Добавить танк ({tank.cost})$', f'Добавить артиллерийское орудие ({artillery.cost}$)', f'Добавить отряд пехотинцев ({men.cost}$)', f'Добавить ракету ({rocket.cost}$)', f'Добавить отряд спецназа ({alpha.cost}$)']
        self.buttons_location = []
        for i in range(5):
            text = font.render(texts[i], True, font_color)
            text_w, text_h = text.get_rect()[2:]
            button_left = to_center_text_in_horizontal(text_w, board.left + num_cells_in_line * size_of_cell, SCREEN_SIZE[0])
            button_top = board.top + board.height * board.cell_size - text_h - 12 - (i + 1) * 40
            screen.fill(pygame.Color('blue'),
                        pygame.Rect(button_left - 10, button_top - 5, text_w + 20,
                                    text_h + 10))
            screen.blit(text, (button_left, button_top))
            self.buttons_location.append((button_left - 10, button_top - 5, button_left + text_w + 10,
                                    button_top + text_h + 5))
            pygame.display.flip()

class Weapon(pygame.sprite.Sprite):
    quit = False
    if_to_redraw_everything = False
    default_location = (100, 100)

    def __init__(self, sprite, screen, location, player, *group):
        super().__init__(*group)
        self.player = player
        self.default_side = 1
        self.image = Image.open(sprite.image)
        self.image = self.image.resize((size_of_cell, size_of_cell), Image.ANTIALIAS)
        self.image.save(sprite.image)
        self.image = pygame.image.load(sprite.image)
        self.full_hp = sprite.full_hp
        self.hp = sprite.hp
        self.attack_radius = sprite.attack_radius
        self.harm_koef = sprite.harm_koef
        self.speed = sprite.speed
        self.level = 1
        self.side = 1
        self.type_of_weapon = sprite.type_of_weapon
        self.screen = screen
        self.location = location
        self.deleted = False
        # Имена и значения характеристик оружия
        self.stats_names = ['Уровень', 'Здоровье', 'Максимальный урон', 'Радиус атаки', 'Скорость']
        self.stats_points = [str(self.level), str(self.hp) + '/' + str(self.full_hp), str(self.attack_radius * self.harm_koef),
                             str(self.attack_radius), str(self.speed)]

    def show_image(self):
        screen.blit(self.image, self.location)

    # Функция показа изображений по координатам

    def rotate_center(self, image, location, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=location).center)
        return rotated_image, new_rect

    def turning_weapon(self, side_to_turn):
        print('self side', self.side)
        turning_right = 1
        if side_to_turn - self.side < 2:
            turning_right = -1
        angle = 0
        natural_image = self.image
        size_before = (board.cell_size, board.cell_size)
        while (angle + 720) % 360 != (((self.side - side_to_turn) * 90) + 720) % 360:
            angle += turning_right * 5
            self.image, coords_to_blit_image = self.rotate_center(natural_image, self.location, angle)
            self.location = (coords_to_blit_image[0] + size_before[0] // 2, coords_to_blit_image[1] + size_before[1] // 2)
            size_before = tuple(coords_to_blit_image[2:])
            board.redraw_board()
            clock.tick(velocity / fps)
        self.side = side_to_turn

    # Функция центровки текста в указанных пределах

    def damage(self, points, cell):
        self.hp -= points
        self.stats_points = [str(self.level), str(self.hp) + '/' + str(self.full_hp),
                             str(self.attack_radius * self.harm_koef),
                             str(self.attack_radius), str(self.speed)]
        if self.hp <= 0:
            write_to_console('Вражейское орудие уничтожено!')
            board.remove_elem(cell)
            if self.type_of_weapon == 'База':
                write_to_console(f'Игрок {hod} победил!')
                clock.tick(10)
                global winner
                winner = hod
                end_of_game = True

    def cure(self, points):
        self.hp += points

    def upgrade(self):
        # Улучшение
        # Все значения умножаются на коэффиценты, а в список записываются округленные значения
        self.level += 1
        self.hp = round(int((self.hp / self.full_hp) * 1.5), 2)
        self.harm_koef = round(self.harm_koef * 1.5, 2)
        self.attack_radius = round(self.attack_radius * 1.5, 2)
        self.speed = round(self.speed * 1.5, 2)
        self.stats_points = [str(self.level), str(self.hp) + '/' + str(self.full_hp),
                             str(round(self.attack_radius * self.harm_koef, 2)),
                             str(self.attack_radius), str(self.speed)]

    def show_stats(self, running):
        # Размеры таблицы статистики
        size_of_table_x = 230
        size_of_table_y = 380
        location_to_save = self.location
        if self.location[0] + size_of_table_x > SCREEN_SIZE[0] or self.location[1] + size_of_table_y > SCREEN_SIZE[1]:
            self.location = (self.location[0] - size_of_table_x + board.cell_size // 2, self.location[1] - size_of_table_y + board.cell_size // 2)
        else:
            self.location = (self.location[0] + board.cell_size // 2, self.location[1] + board.cell_size // 2)
        # Фоновая картинка
        background = Image.open('tank_bg.jpg')
        background = background.resize((size_of_table_x, size_of_table_y), Image.ANTIALIAS)
        blit_pil_image(self.screen, background, self.location)
        # Параметра текста
        font_size = 24
        font_color = pygame.Color('yellow')
        font = pygame.font.Font(None, font_size)
        text = font.render('Статистика', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        num_lines = 5
        # Заголовок
        screen.blit(text, (
        to_center_text_in_horizontal(text_w, self.location[0], self.location[0] + size_of_table_x), self.location[1] + 30 + int((1/3) * size_of_table_y)))
        line_now = 0
        # Запись построчно сначала имени характеристики, а потом ее значения
        for i in range(self.location[1] + 60 + int((1/3) * size_of_table_y), self.location[1] + int((1/3) * size_of_table_y) + (num_lines + 2) * 30, 30):
            screen.blit(font.render(self.stats_names[line_now], True, font_color), (self.location[0] + 5, i))
            points_to_show = font.render(self.stats_points[line_now], True, font_color)
            points_width, points_height = points_to_show.get_rect()[2:]
            screen.blit(points_to_show, (self.location[0] + size_of_table_x - 5 - points_width, i))
            line_now += 1
            # Кнопка улучшить, ее центровка и рисование
        text = font.render('Улучшить', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        coords_left_top_button_upgrade = (to_center_text_in_horizontal(text_w + 20, self.location[0], self.location[0] + size_of_table_x // 2), self.location[1] + (line_now + 2) * 25 + 30 + int((1 / 3) * size_of_table_y), text_w + 20, text_h + 10)
        screen.fill(pygame.Color('blue'), pygame.Rect(coords_left_top_button_upgrade[0], coords_left_top_button_upgrade[1], text_w + 20, text_h + 10))
        screen.blit(text, (
            to_center_text_in_horizontal(text_w, self.location[0], self.location[0] + size_of_table_x // 2),
            self.location[1] + (line_now + 2) * 30 + int((1 / 3) * size_of_table_y)))
        # Кнопка удалить
        text = font.render('Удалить', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        coords_left_top_button_delete = (to_center_text_in_horizontal(text_w + 20, self.location[0] + size_of_table_x // 2, self.location[0] + size_of_table_x),
            self.location[1] + (line_now + 2) * 25 + 30 + int((1 / 3) * size_of_table_y), text_w + 20, text_h + 10)
        screen.fill(pygame.Color('blue'), pygame.Rect(
            coords_left_top_button_delete[0],
            coords_left_top_button_delete[1], text_w + 20, text_h + 10))
        screen.blit(text, (
            to_center_text_in_horizontal(text_w, self.location[0] + size_of_table_x // 2, self.location[0] + size_of_table_x),
            self.location[1] + (line_now + 2) * 30 + int((1 / 3) * size_of_table_y)))
        # Флип экрана для рисования
        pygame.display.flip()
        # Обработка событий кнопок
        immediate_quit = False
        while not(immediate_quit) and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    immediate_quit = True
                    Weapon.quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Левый щелчок мыши
                    coords = list(event.pos)
                    if coords[0] in range(coords_left_top_button_upgrade[0], coords_left_top_button_upgrade[0] + coords_left_top_button_upgrade[2] + 1) and coords[1] in range(coords_left_top_button_upgrade[1], coords_left_top_button_upgrade[1] + coords_left_top_button_upgrade[3] + 1):
                        # Улучшение
                        print('upgrade')
                        self.upgrade()
                        self.show_stats(False)
                        pygame.display.flip()
                    elif coords[0] in range(coords_left_top_button_delete[0], coords_left_top_button_delete[0] + text_w + 20) and coords[1] in range(coords_left_top_button_delete[1], coords_left_top_button_delete[1] + text_h + 10):
                        #
                        self.deleted = True
                        running = False
                        removed_elem = board.remove_elem((board.get_cell(self.location)[0] + 1, board.get_cell(self.location)[1] + 1))
                        redraw_everything()
                        print(board.board)
                    else:
                        running = False
        self.location = location_to_save
        board.redraw_board()


def to_center_text_in_horizontal(text_w, x1, x2):
    return x1 + (x2 - x1 - text_w) // 2


board = Board(num_cells_in_line, num_cells_in_line)
button_punnel_main_during_game = Buttons_in_game_process()


def blit_pil_image(screen, image, location):
    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
    screen.blit(pygame_image, location)

background_of_game = Image.open('fon_during_game.jpg')
def redraw_everything():
    screen.fill('black')
    background = background_of_game.resize(SCREEN_SIZE, Image.ANTIALIAS)
    blit_pil_image(screen, background, (0, 0))
    board.render(screen)
    button_punnel_main_during_game.draw_next_step_button()
    show_money(hod)
    button_punnel_main_during_game.draw_add_buttons()
    write_to_console('')


def write_to_console(text_to_write):
    if text_to_write == '':
        console_left = board.left
        console_top = board.top + board.height * board.cell_size + 10
        screen.fill(pygame.Color('blue'),
                    pygame.Rect(console_left, console_top, board.width * board.cell_size,
                                40))
        pygame.display.flip()
    else:
        console_font_size = 24
        console_font_color = pygame.Color('yellow')
        console_font = pygame.font.Font(None, console_font_size)
        text = console_font.render(text_to_write, True, console_font_color)
        console_text_w, console_text_h = text.get_rect()[2:]
        console_left = board.left
        console_top = board.top + board.height * board.cell_size + 10
        screen.fill(pygame.Color('blue'),
                    pygame.Rect(console_left, console_top, board.width * board.cell_size,
                                40))
        screen.blit(text, (to_center_text_in_horizontal(console_text_w, console_left, console_left + board.width * board.cell_size), console_top + 5))
        pygame.display.flip()


def if_coords_on_board(mouse_pos):
    if mouse_pos[0] > board.left and mouse_pos[0] < board.left + board.width * size_of_cell \
            and mouse_pos[1] > board.top and mouse_pos[1] < board.top + board.height * size_of_cell:
        return True
    return False


def show_money(player):
    money_font_size = 24
    money_font_color = pygame.Color('yellow')
    money_font = pygame.font.Font(None, money_font_size)
    if player == 0:
        text = money_font.render(str(MONEY_P_1) + '$', True, money_font_color)
    else:
        text = money_font.render(str(MONEY_P_2) + '$', True, money_font_color)
    text_player = money_font.render('Игрок ' + str(player), True, money_font_color)
    money_text_w, money_text_h = text.get_rect()[2:]
    text_player_w, text_player_h = text_player.get_rect()[2:]
    money_left = to_center_text_in_horizontal(70, 0, board.left)
    money_top = board.top + board.height * board.cell_size - 40
    screen.fill(pygame.Color('blue'),
                pygame.Rect(money_left, money_top, 70,
                            50))
    screen.blit(text, (
    to_center_text_in_horizontal(money_text_w, money_left, money_left + 70),
    money_top + 45 - money_text_h))
    screen.blit(text_player, (
        to_center_text_in_horizontal(text_player_w, money_left, money_left + 70),
        money_top + 5))
    pygame.display.flip()

def start_game():
    pass

def end_game():
    background = Image.open('tank_background2.jpg')
    background = background.resize(SCREEN_SIZE, Image.ANTIALIAS)
    blit_pil_image(screen, background, (0, 0))
    winner_font_size = 48
    money_font_color = pygame.Color('yellow')
    money_font = pygame.font.Font(None, winner_font_size)
    text = money_font.render(f'Игрок {winner} победил! Ура!', True, money_font_color)
    winner_text_w, winner_text_h = text.get_rect()[2:]
    winner_left = to_center_text_in_horizontal(winner_text_w, 0, SCREEN_SIZE[0])
    winner_top = to_center_text_in_horizontal(winner_text_h, 0, SCREEN_SIZE[1])
    screen.fill(pygame.Color('blue'),
                pygame.Rect(winner_left, winner_top, 70,
                            50))
    screen.blit(text, (winner_left, winner_top))
    pygame.display.flip()



pygame.init()
size = 700, 700
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Игра')
screen.fill('black')
weapons_list = [tank, artillery, men, rocket, alpha]
#tank1 = Weapon(tank, screen, (100, 100), 1, sprite_group_weapons)
print(board.board)
end_of_game = False
hod = 2
board.add_elem(base, (0, num_cells_in_line - 1), 1)
board.add_elem(base, (num_cells_in_line - 1, 0), 2)
while not(immediate_quit) and not(end_of_game):
    running = True
    if hod == 1:
        hod = 2
    else:
        hod = 1
    redraw_everything()
    while not(immediate_quit) and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                immediate_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                #board.move_weapon((1, 2), (0, 0))
                #board.attack((0, 0), (10, 15))
                if if_coords_on_board(mouse_pos):
                    if event.button == 1:
                        cell_pressed_1 = board.get_cell(mouse_pos)
                        object_chosen = board.board[cell_pressed_1[1]][cell_pressed_1[0]]
                        print('object_chosen', object_chosen)
                        board.redraw_board()
                        board.answer_click(cell_pressed_1)
                        if object_chosen != 0:
                            object_is_chosen = True
                            print('choosing')
                            while not(immediate_quit) and not(end_of_game) and object_is_chosen:
                                for event_while_chosen in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        object_is_chosen = False
                                        running = False
                                        immediate_quit = True
                                    elif event_while_chosen.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_pos_2 = event_while_chosen.pos
                                        if if_coords_on_board(mouse_pos_2):
                                            cell_pressed_2 = board.get_cell(mouse_pos_2)
                                            object_chosen_2 = board.board[cell_pressed_2[1]][cell_pressed_2[0]]
                                            print(object_chosen_2, 'object 2')
                                            board.redraw_board()
                                            board.answer_click(cell_pressed_2)
                                            if object_chosen_2 != 0:
                                                print(object_chosen.player, object_chosen_2.player)
                                                if object_chosen.player == hod and object_chosen.player == object_chosen_2.player:
                                                    if event_while_chosen.button == 1:
                                                        print('changing')
                                                        object_chosen = object_chosen_2
                                                        cell_pressed_1 = cell_pressed_2
                                                        board.answer_click(cell_pressed_1)
                                                    elif event_while_chosen.button == 3:
                                                        object_chosen_2.show_stats(True)
                                                        redraw_everything()
                                                        object_is_chosen = False
                                                else:
                                                    if object_chosen.player == hod and event_while_chosen.button == 1:
                                                        board.attack(cell_pressed_1, cell_pressed_2)
                                                        object_is_chosen = False
                                                    elif object_chosen.player != hod and event_while_chosen.button == 1:
                                                        object_chosen = object_chosen_2
                                                        cell_pressed_1 = cell_pressed_2
                                                        board.answer_click(cell_pressed_1)
                                                    elif event_while_chosen.button == 3:
                                                        object_chosen_2.show_stats(True)
                                                        redraw_everything()
                                                        object_is_chosen = False
                                            else:
                                                print('mb moving')
                                                if object_chosen.player == hod:
                                                    board.move_weapon(cell_pressed_1, cell_pressed_2)
                                                board.redraw_board()
                                                object_is_chosen = False
                        else:
                            board.redraw_board()
                            board.answer_click(cell_pressed_1)
                    elif event.button == 3:
                        cell_pressed_1 = board.get_cell(mouse_pos)
                        object_chosen = board.board[cell_pressed_1[1]][cell_pressed_1[0]]
                        if object_chosen != 0:
                            object_chosen.show_stats(True)
                            redraw_everything()
                        else:
                            board.redraw_board()
                            board.get_click(mouse_pos)
                elif mouse_pos[0] in range(button_punnel_main_during_game.button_next_step_location[0],
                                           button_punnel_main_during_game.button_next_step_location[2]) \
                        and mouse_pos[1] in range(button_punnel_main_during_game.button_next_step_location[1],
                                                  button_punnel_main_during_game.button_next_step_location[3]):
                    running = False
                    mouse_pos = (-1, -1)
                else:
                    add_but_loc = button_punnel_main_during_game.buttons_location
                    for i in range(len(add_but_loc)):
                        if mouse_pos[0] in range(add_but_loc[i][0], add_but_loc[i][0] + add_but_loc[i][2]) and mouse_pos[1] in range(add_but_loc[i][1], add_but_loc[i][1] + add_but_loc[i][3]):
                            if (MONEY_P_1, MONEY_P_2)[hod - 1] >= weapons_list[i].cost:
                                j = 0
                                place_found = False
                                list_inserting_cells = [(0, num_cells_in_line - 2), (1, num_cells_in_line - 2), (1, num_cells_in_line - 1)]
                                while j < 3:
                                    if board.board[list_inserting_cells[j][1]][list_inserting_cells[j][0]] == 0:
                                        board.add_elem(weapons_list[i], list_inserting_cells[j], hod)
                                        board.redraw_board()
                                        if hod == 1:
                                            print('aaaaaa', weapons_list[i].cost)
                                            MONEY_P_1 -= weapons_list[i].cost
                                            print(MONEY_P_1)
                                        else:
                                            MONEY_P_2 -= weapons_list[i].cost
                                        show_money(hod)
                                        redraw_everything()
                                        place_found = True
                                        break
                                    j += 1
                                if not(place_found):
                                    write_to_console('Освободите место в зоне снаряжения войск')
                                else:
                                    mouse_pos = (-1, -1)
                            else:
                                write_to_console('У вас недостаточно денег для этой покупки')
        if Weapon.quit:
            running = False
            immediate_quit = True
    board.reverse_board()
if end_of_game:
    end_game()
pygame.quit()
