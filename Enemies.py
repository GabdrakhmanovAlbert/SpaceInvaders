import random
import pygame
import sys


class Enemy(pygame.sprite.Sprite):
    '''Пришелец - какашка'''
    '''Обычный враг'''
    speed = 0.1
    MAX_SPEED = 2

    def __init__(self, screen, picture, extra_speed=0):
        '''инициализация говна и задаём начальную позицию'''
        super(Enemy, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        if self.speed < self.MAX_SPEED:
            self.speed += extra_speed

    def draw(self):
        '''Вывод пришельца на экран'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''Перемещает пришельцев'''
        self.y += self.speed
        self.rect.y = self.y


class Car(Enemy):
    '''Прищелец - машина'''
    '''Имеет более быструю скорость, чем обычный враг'''
    speed = 0.5
    MAX_SPEED = 3

    def __init__(self, screen, picture, extra_speed=0):
        '''инициализация и задаём начальную позицию'''
        super().__init__(screen, picture, extra_speed)


class Ghost(Enemy):
    '''Пришелец - призрак'''
    '''Умеет становится невидимым и неуязвимым на короткое время'''

    def __init__(self, screen, picture, picture_invisible, extra_speed=0):
        '''Инициализация призрака'''
        super().__init__(screen, picture, extra_speed)
        # параметры невидимой картинки призрака
        self.invis_image = pygame.image.load(picture_invisible)
        ''' #? нужно ли это
        self.invis_rect = self.rect
        self.invis_rect.x = self.rect.x
        self.invis_rect.y = self.rect.y
        self.invis_x = self.x
        self.invis_y = self.y
        '''
        self.frames_invisibility = 0
        # содержит инфу видимый или нет
        self.is_invisible = False

    def draw(self):
        '''Отрисовывает видимого призрака'''
        self.screen.blit(self.image, self.rect)

    def draw_invisible(self):
        '''Отрисовывает невидимого призрака'''
        self.screen.blit(self.invis_image, self.rect)
    
    def ability(self):
        '''Распределяет, когда призрак становится видимым, а когда невидимым'''
        if self.frames_invisibility == 0:
            self.frames_invisibility = random.randint(100, 1000)
            self.is_invisible = not self.is_invisible
        else:
            self.frames_invisibility -= 1
        
        if self.is_invisible:
            self.draw_invisible()
        else:
            self.draw()


class Armored_Enemy(Enemy):
    '''Пришелец - солдат со щитом'''
    '''Имеет щит случайной прочности (1-4 ед), при получении урона меняется картинка на более светлый щит, если щит белый был - враг умирает'''
    speed = 0.05

    def __init__(self, screen, picture, extra_speed=0):
        super().__init__(screen, picture, extra_speed)
        # в относительном пути к файлу картинки по 20 индексу находится количество жизней
        # например: img/protected_enemy/2armored_enemy.png
        self.counter_lives = int(picture[20])

    def change_shield(self):
        '''Меняет картинку, если враг в него попал'''
        self.counter_lives -= 1
        if self.counter_lives <= 0:
            return
        self.image = pygame.image.load(
            f'img/protected_enemy/{self.counter_lives}armored_enemy.png')
    
    def ability(self, enemies):
        '''Ортрисовка врага с щитом'''
        if self.counter_lives == 0:
            enemies.remove(self)
        else:
            self.draw()








# TODO скорее всего создать Бонус.py
class Bonus(Enemy):
    '''Бонусы для игрока'''
    '''Спаунятся за экраном, двигаются со скоростю обычного игрока, исчезают при коллизии с игроком'''
    # TODO функцию добавления этих объектов в Group() of enemies очень редко
    type_bonuses = ['img/bonus/heart.png', 'img/bonus/shield.png']

    def __init__(self, screen, extra_speed=0):
        super().__init__(screen, random.choice(self.type_bonuses), extra_speed)
    # TODO функции для проверки на столкновение с игроком(исчезает бонус), столкновение с пулей(исчезает бонус, активируется способность),
    # TODO столкновение c краем экрана (исчезает бонус)


# * массив специальных врагов: машина, призрак, солдат с щитом
enemies_pictures = ['img/enemy_car.png', 'img/ghost/', 'img/protected_enemy/']
ghost_pictures = [['enemy_ghost0.png', 'enemy_ghost0_invisible1.png']]
protected_enemy_pictures = [
    '1armored_enemy.png', '2armored_enemy.png',
    '3armored_enemy.png', '4armored_enemy.png',
    '5armored_enemy.png', '6armored_enemy.png',
    '7armored_enemy.png']


def create_enemy(screen, extra_speed, stats):
    '''Создание случайного врага'''
    global enemies_pictures, ghost_pictures, protected_enemy_pictures

    stats.counter_warriors += 1

    if stats.counter_warriors in stats.indexes_special_enemies:
        type_enemy = random.choice(enemies_pictures)
        stats.indexes_special_enemies.discard(stats.counter_warriors)
    else:
        type_enemy = 'img/enemy_kaka.png'

    enemy = return_enemy(screen, type_enemy, extra_speed)
    return enemy

def return_enemy(screen, type_enemy, extra_speed):
    '''Возвращает врага по type_enemy'''
    if type_enemy.endswith('/'):
        if type_enemy == 'img/ghost/':
            files = random.choice(ghost_pictures)
            return Ghost(screen, type_enemy + files[0], type_enemy + files[1], extra_speed)
        elif type_enemy == 'img/protected_enemy/':
            file = random.choice(protected_enemy_pictures)
            return Armored_Enemy(screen, type_enemy + file, extra_speed)
    else:
        if type_enemy == 'img/enemy_car.png':
            return Car(screen, type_enemy, extra_speed)
        else:
            return Enemy(screen, 'img/enemy_kaka.png', extra_speed)
