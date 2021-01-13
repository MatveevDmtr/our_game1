import pygame
from PIL import Image
clock = pygame.time.Clock()
velocity = 240
fps = 60
size_of_cell = 50



sprite_group_weapons = pygame.sprite.Group()

# Инициализация параметров танка
tank = pygame.sprite.Sprite(sprite_group_weapons)
tank.type_of_weapon = 'tank'
tank.full_hp = 100
tank.hp = 90
tank.attack_radius = 1
tank.harm_koef = 1
tank.speed = 1
tank.level = 1
tank.image = 'tank_1.jpg'

# Инициализация параметров ПВО
pvo = pygame.sprite.Sprite(sprite_group_weapons)
pvo.type_of_weapon = 'pvo'
pvo.full_hp = 100
pvo.hp = 90
pvo.attack_radius = 1
pvo.harm_koef = 1
pvo.speed = 1
pvo.level = 1
pvo.image = 'tank_1.jpg'


class Weapon(pygame.sprite.Sprite):
    quit = False
    if_to_redraw_everything = False
    default_location = (100, 100)

    def __init__(self, sprite, screen, location, side, *group):
        super().__init__(*group)
        self.image = Image.open(sprite.image)
        self.image = self.image.resize((size_of_cell, size_of_cell), Image.ANTIALIAS)
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, "RGB")
        self.full_hp = sprite.full_hp
        self.hp = sprite.hp
        self.attack_radius = sprite.attack_radius
        self.harm_koef = sprite.harm_koef
        self.speed = sprite.speed = 1
        self.level = 1
        self.side = 1
        self.type_of_weapon = sprite.type_of_weapon
        self.screen = screen
        self.location = Weapon.default_location
        self.deleted = False
        # Имена и значения характеристик оружия
        self.stats_names = ['Уровень', 'Здоровье', 'Максимальный урон', 'Радиус атаки', 'Скорость']
        self.stats_points = [str(self.level), str(self.hp) + '/' + str(self.full_hp), str(self.attack_radius * self.harm_koef),
                             str(self.attack_radius), str(self.speed)]

    # Функция показа изображений по координатам
    def blit_pil_image(self, screen, image, location):
        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
        screen.blit(pygame_image, location)

    def rotate_center(self, image, location, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center=location).center)
        return rotated_image, new_rect

    def turning_weapon(self, side_to_turn):
        turning_right = 1
        if self.side - side_to_turn > 2 or 0 > self.side - side_to_turn >= -2:
            turning_right = -1
        angle = 0
        while abs(angle) < abs(self.side - side_to_turn) * 90:
            angle += turning_right * 5
            image_to_show, coords_to_blit_image = self.rotate_center(self.image, self.location, angle)
            screen.blit(image_to_show, coords_to_blit_image[0:2])
            pygame.display.flip()
            clock.tick(velocity // fps)
        self.side = side_to_turn


    # Функция центровки текста в указанных пределах
    def to_center_text_in_horizontal(self, text_w, x1, x2):
        return x1 + (x2 - x1 - text_w) // 2

    def damage(self, points):
        self.hp -= points

    def cure(self, points):
        self.hp += points

    def upgrade(self):
        # Улучшение
        # Все значения умножаются на коэффиценты, а в список записываются округленные значения
        self.level += 1
        self.hp = round(int((self.hp / self.full_hp) * 1.1), 2)
        self.harm_koef = round(self.harm_koef * 1.1, 2)
        self.attack_radius = round(self.attack_radius * 1.1, 2)
        self.speed = round(self.speed * 1.1, 2)
        self.stats_points = [str(self.level), str(self.hp) + '/' + str(self.full_hp),
                             str(round(self.attack_radius * self.harm_koef, 2)),
                             str(self.attack_radius), str(self.speed)]

    def show_stats(self, running):
        # Размеры таблицы статистики
        size_of_table_x = 230
        size_of_table_y = 380
        # Фоновая картинка
        background = Image.open('tank_background2.jpg')
        background = background.resize((size_of_table_x, size_of_table_y), Image.ANTIALIAS)
        self.blit_pil_image(self.screen, background, self.location)
        # Параметра текста
        font_size = 24
        font_color = pygame.Color('yellow')
        font = pygame.font.Font(None, font_size)
        text = font.render('Статистика', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        num_lines = 5
        # Заголовок
        screen.blit(text, (
        self.to_center_text_in_horizontal(text_w, self.location[0], self.location[0] + size_of_table_x), self.location[1] + 30 + int((1/3) * size_of_table_y)))
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
        coords_left_top_button_upgrade = (self.to_center_text_in_horizontal(text_w + 20, self.location[0], self.location[0] + size_of_table_x // 2), self.location[1] + (line_now + 2) * 25 + 30 + int((1 / 3) * size_of_table_y), text_w + 20, text_h + 10)
        screen.fill(pygame.Color('blue'), pygame.Rect(coords_left_top_button_upgrade[0], coords_left_top_button_upgrade[1], text_w + 20, text_h + 10))
        screen.blit(text, (
            self.to_center_text_in_horizontal(text_w, self.location[0], self.location[0] + size_of_table_x // 2),
            self.location[1] + (line_now + 2) * 30 + int((1 / 3) * size_of_table_y)))
        # Кнопка удалить
        text = font.render('Удалить', True, font_color)
        text_w, text_h = text.get_rect()[2:]
        coords_left_top_button_delete = (self.to_center_text_in_horizontal(text_w + 20, self.location[0] + size_of_table_x // 2, self.location[0] + size_of_table_x),
            self.location[1] + (line_now + 2) * 25 + 30 + int((1 / 3) * size_of_table_y), text_w + 20, text_h + 10)
        screen.fill(pygame.Color('blue'), pygame.Rect(
            coords_left_top_button_delete[0],
            coords_left_top_button_delete[1], text_w + 20, text_h + 10))
        screen.blit(text, (
            self.to_center_text_in_horizontal(text_w, self.location[0] + size_of_table_x // 2, self.location[0] + size_of_table_x),
            self.location[1] + (line_now + 2) * 30 + int((1 / 3) * size_of_table_y)))
        # Флип экрана для рисования
        pygame.display.flip()
        self.turning_weapon(3)
        # Обработка событий кнопок
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                        Weapon.if_to_redraw_everything = True
                    else:
                        running = False
                        Weapon.if_to_redraw_everything = True

pygame.init()
size = 700, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра')
screen.fill('black')
tank1 = Weapon(tank, screen, (100, 100), 1, sprite_group_weapons)
running = True
while running:
    tank1.show_stats(True)
    if tank1.deleted:
        print('deleted')
    if Weapon.quit:
        running = False
    elif Weapon.if_to_redraw_everything:
        screen.fill('black')
        pygame.display.flip()
        print('redrawed')
        running = False
pygame.quit()