import pygame


class Bullet(pygame.sprite.Sprite):
    speed = 3.5

    def __init__(self, screen, gun, extra_speed=0):
        """Создаём пулю в позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (255, 255, 0)
        self.speed += extra_speed
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """Перемещение пули вверх"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовать пулю"""
        pygame.draw.rect(self.screen, self.color, self.rect)
