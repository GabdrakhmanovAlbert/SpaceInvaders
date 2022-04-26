import pygame
from pygame.sprite import Sprite
from bullet import Bullet
import time


class Gun():
    '''Пушка - игрок'''

    def __init__(self, screen):
        '''инициализация пушки'''
        self.screen = screen
        self.img = pygame.image.load('img/skins_gun/пушка_1.png')
        self.rect = self.img.get_rect()
        self.center = float(self.rect.centerx)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx  # * размещает  по центру экрана
        self.rect.bottom = self.screen_rect.bottom  # * размещает внизу экрана

        self.speed = 1.1  # скорость движения
        self.mright = False  # отвечают за движение игрока
        self.mleft = False
        self.power_bullet = 1  # ! не забудь про прокачку урона
        self.block_controls = False  # * блокировка обработки событий игрока

    def output(self):
        '''Рисование пушки'''
        self.screen.blit(self.img, self.rect)

    def update_gun(self):
        """Обновление позиции пушки"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += self.speed
        elif self.mleft and self.rect.left > self.screen_rect.left:
            self.center -= self.speed

        self.rect.centerx = self.center

    def revive_gun(self):
        '''Размещает пушку по центру внизу экрана, ослабляет скорость и силу пуль'''
        self.center = self.screen_rect.centerx
        self.speed = 1.1
        self.power_bullet = 1


class Live(Sprite):
    '''Жизни пушки'''
    '''Те объекты, что размещены в верхнем левом углу экрана'''

    def __init__(self, screen):
        super(Live, self).__init__()
        self.screen = screen
        self.image = pygame.transform.scale(
            pygame.image.load('img/bonus/heart.png'), (25, 20))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
