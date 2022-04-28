import Enemies
import random
from const import *


#! Вариации размещения армий

def rectangle(screen, enemies, extra_speed, stats):
    '''Создание прямоугольной армии на весь экран'''

    number_enemy_x, number_enemy_y, enemy_width, enemy_height = quantify_enemies_x_y(
        screen)

    launch_special_enemies(stats)

    # * Создание врагов их добавление в группу
    stats.counter_warriors = 0  # * счётчик игроков для размещения врагов по индексу
    for row_number in range(number_enemy_y):
        for number_enemy in range(number_enemy_x):
            enemy = Enemies.create_enemy(
                screen, extra_speed, stats)
            place_xy_enemy(enemy, enemy_width, enemy_height,
                           number_enemy, row_number)
            enemies.add(enemy)
    del stats.counter_warriors


def wedge(screen, enemies, extra_speed):
    '''Создание армии построенной клином'''

    army_outline, army_back, army_center, army_front = get_random_types()
    # * army_outline  - по контуру клина тип врагов
    # * army_back тип врагов на последних 2 линиях
    # * army_center тип врагов на средних 3 линиях
    # * army_front тип врагов на передних 3 линиях

    number_enemy_x, number_enemy_y, enemy_width, enemy_height = quantify_enemies_x_y(
        screen)
    increase = 0  # * отвечает за отступы
    counter_rows = 0  # * счётчик рядов по y
    for row_number in range(number_enemy_y):
        for number_enemy in range(number_enemy_x):
            enemy = place_in_rows_wedge(screen, extra_speed, number_enemy_x, number_enemy_y,
                                        number_enemy, row_number, army_outline, army_back, army_center, army_front)
            place_xy_enemy(enemy, enemy_width, enemy_height,
                           number_enemy, row_number, increase, counter_rows)
            enemies.add(enemy)
        increase = enemy_width * 0.5
        number_enemy_x -= 1
        counter_rows += 1


def chess(screen, enemies, extra_speed):
    '''Построение армии - шахматная доска'''

    number_enemy_x, number_enemy_y, enemy_width, enemy_height = quantify_enemies_x_y(
        screen)
    second_type = random.choice(SPECIAL_ENEMIES_PICTURES)
    for row_number in range(number_enemy_y):
        if row_number % 2 == 0:
            is_odd_row = False
        else:
            is_odd_row = True
        for number_enemy in range(number_enemy_x):
            if is_odd_row:
                enemy = Enemies.return_enemy(
                    screen, second_type, extra_speed)
                place_xy_enemy(enemy, enemy_width, enemy_height,
                               number_enemy, row_number)
                if number_enemy % 2 != 0:
                    enemies.add(enemy)
            else:
                enemy = Enemies.return_enemy(
                    screen, 'img/enemy_kaka.png', extra_speed)
                place_xy_enemy(enemy, enemy_width, enemy_height,
                               number_enemy, row_number)
                if number_enemy % 2 == 0:
                    enemies.add(enemy)


def heart(screen, enemies, extra_speed):
    '''Построение армии - сердце'''

    number_enemy_x, number_enemy_y, enemy_width, enemy_height = quantify_enemies_x_y(
        screen)

    number_enemy_x += 2

    for row_number in range(number_enemy_y):
        for enemy_number in range(number_enemy_x):
            if (row_number == 0) or (row_number == 10):
                if enemy_number == 0:
                    continue
                elif enemy_number > 5:
                    continue
            elif (row_number == 1) or (row_number == 9):
                if (enemy_number != 0) and (enemy_number != 6) and (enemy_number != 7) and (enemy_number != 4):
                    continue
            elif (row_number == 2) or (row_number == 8):
                if (enemy_number != 0) and (enemy_number != 7) and (enemy_number != 8) and (enemy_number != 3) and (enemy_number != 5) and (enemy_number != 4):
                    continue
            elif (row_number == 3) or (row_number == 7):
                if (enemy_number != 1) and (enemy_number != 9) and (enemy_number != 4):
                    continue
            elif (row_number == 4) or (row_number == 6):
                if (enemy_number != 2) and (enemy_number != 10) and (enemy_number != 7):
                    continue
            else:
                if (enemy_number != 11) and (enemy_number != 3) and (enemy_number != 8) and (enemy_number != 5):
                    continue
            enemy = Enemies.return_enemy(
                screen, 'img/enemy_kaka.png', extra_speed)
            place_xy_enemy(enemy, enemy_width, enemy_height,
                           row_number, enemy_number)
            enemy.x -= enemy_width // 2
            enemy.rect.x = enemy.x
            enemies.add(enemy)


def semicircle(screen, enemies, extra_speed):
    '''Построение армии - полукруг'''
    pass


def skelet(screen, enemies, extra_speed):
    '''Построение армии - башка скелета'''
    number_enemy_x, number_enemy_y, enemy_width, enemy_height = quantify_enemies_x_y(
        screen)

    for row_number in range(number_enemy_x):
        for enemy_number in range(number_enemy_y):
            if (row_number == 0) or (row_number == 10):
                if enemy_number == 0:
                    continue
                elif enemy_number > 5:
                    continue
            elif (row_number == 1) or (row_number == 9):
                if (enemy_number != 0) and (enemy_number != 6) and (enemy_number != 7):
                    continue
            elif (row_number == 2) or (row_number == 8):
                if (enemy_number != 0) and (enemy_number != 7) and (enemy_number != 8):
                    continue
            else:
                if row_number % 2 != 0:
                    if (enemy_number == 12) or (enemy_number == 11):
                        continue
                else:
                    if (enemy_number == 12) or (enemy_number == 11) or (enemy_number == 10):
                        continue
            enemy = Enemies.return_enemy(
                screen, 'img/enemy_kaka.png', extra_speed)
            place_xy_enemy(enemy, enemy_width, enemy_height,
                           enemy_number, row_number)
            enemies.add(enemy)


def smiley_face(screen, enemies, width_screen, height_screen, extra_speed):
    '''Построение армии в виде смайлика'''
    global enemies_pictures
    enemy = enemies.Enemy(screen, extra_speed)
    enemy_width = enemy.rect.width
    number_enemy_x = int((width_screen - 2 * enemy_width) / enemy_width) - 1
    enemy_height = enemy.rect.height
    number_enemy_y = int(
        (height_screen - 100 - 2 * enemy_height) / enemy_height) - 4

    for row_number in range(number_enemy_x):
        for enemy_number in range(number_enemy_y):
            if (row_number == 0) or (row_number == 10):
                if (enemy_number < 3) or (enemy_number > 6):
                    continue
            elif (row_number == 1) or (row_number == 9):
                if (enemy_number == 0) or (enemy_number > 6):
                    continue
            elif (row_number == 2) or (row_number == 8):
                if (enemy_number == 7) or (enemy_number > 8):
                    continue
            elif (row_number == 3) or (row_number == 7):
                if (enemy_number > 2) and (enemy_number != 9):
                    continue
            elif (row_number == 4) or (row_number == 6):
                if (enemy_number > 1) and (enemy_number != 9) and (enemy_number != 4) and (enemy_number != 5):
                    continue
            else:
                if (enemy_number > 1) and (enemy_number != 9):
                    continue
            enemy = enemies.Enemy(screen, extra_speed)
            enemy.x = enemy_width + 1.1 * enemy_width * row_number
            enemy.y = enemy_height + 1.1 * enemy_height * enemy_number
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemies.add(enemy)


'''
def skelet(screen, enemies, width_screen, height_screen, extra_speed):
    на якорь смахивает
    enemy = Enemy(screen, extra_speed)
    enemy_width = enemy.rect.width
    # число противников по горизонтали
    number_enemy_x = int((width_screen - 2 * enemy_width) / enemy_width) - 1
    enemy_height = enemy.rect.height
    # число противников по вертикали
    number_enemy_y = int(
        (height_screen - 100 - 2 * enemy_height) / enemy_height) - 4

    for row_number in range(number_enemy_x):
        for enemy_number in range(number_enemy_y):
            if (row_number == 0) or (row_number == 10):
                if enemy_number == 0:
                    continue
                elif enemy_number > 5:
                    continue
            elif (row_number == 1) or (row_number == 9):
                if (enemy_number == 0) or (enemy_number == 6) or (enemy_number == 7):
                    continue
            elif (row_number == 2) or (row_number == 8):
                if (enemy_number == 0) or (enemy_number == 7) or (enemy_number == 8):
                    continue
            enemy = Enemy(screen, extra_speed)
            enemy.x = enemy_width + 1.1 * enemy_width * row_number
            enemy.y = enemy_height + 1.1 * enemy_height * enemy_number
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemies.add(enemy)
'''
#! Доп функции для размещения армий


def launch_special_enemies(stats):
    '''Генерирует кол-во игроков в пределах special_enemy_limiter и добавляет в множество их порядковый номер в строю'''
    # * Повышает лимит специальных врагов каждый новый раунд
    if stats.special_enemy_limiter < 50:
        stats.special_enemy_limiter += 5

    stats.special_enemies = random.randint(0, stats.special_enemy_limiter)
    for _ in range(stats.special_enemies):
        index = random.randint(1, 130)
        if index in stats.indexes_special_enemies:
            while index in stats.indexes_special_enemies:
                index = random.randint(1, 130)
            stats.indexes_special_enemies.add(index)
        else:
            stats.indexes_special_enemies.add(index)


def quantify_enemies_x_y(screen):
    '''Возвращает количество противников по горизонтали и вертикали'''
    width_screen, height_screen = screen.get_rect().size
    enemy = Enemies.Enemy(screen, 'img/enemy_kaka.png')
    enemy_width = enemy.rect.width
    # * число противников по горизонтали
    number_enemy_x = int((width_screen - 2 * enemy_width) / enemy_width) - 2
    enemy_height = enemy.rect.height
    # * число противников по вертикали
    number_enemy_y = int(
        (height_screen - 100 - 2 * enemy_height) / enemy_height) - 6

    return (number_enemy_x, number_enemy_y, enemy_width, enemy_height)


def place_xy_enemy(enemy, enemy_width, enemy_height, number_enemy, row_number, increase=0, counter_rows=0):
    '''Размещение врага по x и y'''
    '''increase - отвечает за отступы; counter_rows - счётчик рядов по y ----- ОНИ НЕОБЯЗАТЕЛЬНЫ'''
    enemy.x = enemy_width + 1.2 * enemy_width * \
        number_enemy + increase * counter_rows
    enemy.y = enemy_height + 1.2 * enemy_height * row_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y


def place_in_rows_wedge(screen, extra_speed, number_enemy_x, number_enemy_y, number_enemy, row_number, army_outline, army_back, army_center, army_front):
    '''Размещение врагов по особому порядку: по рядам и оболочке
       В основном для клина, но подойдёт и для других'''
    if (number_enemy == 0) or (number_enemy == number_enemy_x - 1) or (row_number == number_enemy_y - 3):
        return Enemies.return_enemy(screen, army_outline, extra_speed)
    elif row_number <= 1:
        return Enemies.return_enemy(screen, army_back, extra_speed)
    elif row_number <= 4:
        return Enemies.return_enemy(screen, army_center, extra_speed)
    elif row_number <= 7:
        return Enemies.return_enemy(screen, army_front, extra_speed)
    else:
        return Enemies.Enemy(screen, 'img/enemy_kaka.png', extra_speed)


def get_random_types():
    '''Возвращает 4 разных типа врагов случайным образом'''
    types_enemies_copy = ENEMIES_PICTURES.copy()
    type1 = types_enemies_copy.pop(random.randint(
        0, len(types_enemies_copy) - 1))
    type2 = types_enemies_copy.pop(
        random.randint(0, len(types_enemies_copy) - 1))
    type3 = types_enemies_copy.pop(
        random.randint(0, len(types_enemies_copy) - 1))
    type4 = types_enemies_copy.pop(
        random.randint(0, len(types_enemies_copy) - 1))
    return (type1, type2, type3, type4)
