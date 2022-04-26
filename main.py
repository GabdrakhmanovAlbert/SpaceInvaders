import pygame
import controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
import time


def run():
    pygame.init()  # иницилизация всех модулей и подмодулей
    screen = pygame.display.set_mode((700, 800))  # * создание окна с размерами
    pygame.display.set_caption(
        "Space Invaders [Updated] ^__^")  # заголовок к окну
    bg_color = (0, 0, 50)  # задаём цвет в RGB
    gun = Gun(screen)  # * создание игрока пушки
    bullets = Group()  # * создание групп пуль и врагов
    enemies = Group()
    stats = Stats()  # * статистика игрока
    # * создаём армию, но не отрисовываем (заполняем enemies)
    controls.create_army(screen, enemies, stats)
    score = Scores(screen, stats)

    while True:
        # * this_round_begin и this_round_end нужны для равномерного перемещения пришельцев
        this_round_begin = int(round(time.time() * 1000))
        controls.events(screen, gun, bullets)
        if stats.play:
            gun.update_gun()
            controls.update_bullets(
                screen, stats, score, enemies, bullets, gun)
            controls.update_enemies(
                gun, enemies, score, stats, screen, bullets)
            controls.update_screen(
                screen, gun, bg_color, enemies, bullets, stats, score
            )
        this_round_end = int(round(time.time() * 1000))
        if this_round_end - this_round_begin <= 10:
            time.sleep(0.001 * (10 - (this_round_end - this_round_begin)))


if __name__ == "__main__":
    run()
