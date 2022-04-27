import pygame
import sys
from bullet import Bullet
import Enemies
import time
import armies
import random


def events(screen, gun, bullets):
    """Обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # даёт закрывать окно при помощи крестика
            sys.exit()
        if (not gun.block_controls):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    gun.mright = True
                elif event.key == pygame.K_LEFT:
                    gun.mleft = True
                elif event.key == pygame.K_SPACE:
                    for _ in range(gun.power_bullet):
                        new_bullet = Bullet(screen, gun)
                        bullets.add(new_bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    gun.mright = False
                elif event.key == pygame.K_LEFT:
                    gun.mleft = False
                elif event.key == pygame.K_SPACE:
                    gun.rapid_fire = False


def update_screen(screen, gun, bg_color, enemies, bullets, stats, score):
    '''Обновление экрана после каждого события, отрисовка игровых объектов и надписей'''
    screen.fill(bg_color)  # залить каким-то цветом в RGB
    score.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    for enemy in enemies.sprites():
        if isinstance(enemy, Enemies.Ghost):
            enemy.ability()
        elif isinstance(enemy, Enemies.Armored_Enemy):
            enemy.ability(enemies)
        else:
            enemy.draw()
    # появление надписи о следующем раунде
    if score.is_next_round:
        score.is_next_round = False
        score.next_round(stats)
        pygame.display.flip()
        pygame.time.delay(2000)
        gun.block_controls = False
    pygame.display.flip()  # обновляет часть экрана(без арг - весь экран), чтобы цвет менять


def update_bullets(screen, stats, score, enemies, bullets, gun):
    '''Обновлять позиции пуль и ставит новую усиленную армию, при отсутствии врагов'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, enemies, False, False)
    if collisions:
        for bullet, enemies_list in collisions.items():
            for enemy in enemies_list:
                if isinstance(enemy, Enemies.Ghost):
                    if (not enemy.is_invisible):
                        points_for_enemy(bullets, enemies,
                                         enemy, bullet, stats, score)
                elif isinstance(enemy, Enemies.Armored_Enemy):
                    bullets.remove(bullet)
                    enemy.change_shield()
                else:
                    points_for_enemy(bullets, enemies, enemy,
                                     bullet, stats, score)

    if len(enemies) == 0:
        gun.block_controls = True
        make_harder(screen, bullets, enemies, gun, stats)
        score.is_next_round = True
        stats.counter_rounds += 1


def points_for_enemy(bullets, enemies, enemy, bullet, stats, score):
    '''Выдаёт поинты за врага, удаляет пулю и врага'''
    stats.score += 10
    bullets.remove(bullet)
    enemies.remove(enemy)
    score.image_score()
    check_high_score(stats, score)
    score.image_lives()


def make_harder(screen, bullets, enemies, gun, stats):
    '''Создаёт более быструю армию пришельцев, ускоряет пули и игрока'''
    bullets.empty()

    extra_speed_monsters = random.randint(5, 15) / 100
    create_army(screen, enemies, stats, extra_speed=extra_speed_monsters)

    extra_speed_gun = random.randint(0, 7) / 100
    if gun.speed < 3.5:
        gun.speed += extra_speed_gun
    if gun.speed > 3.5:
        gun.speed = 3.5

    extra_speed_bullet = random.randint(0, 20)
    if stats.bullet_speed < 15:
        stats.bullet_speed += extra_speed_bullet
    elif stats.bullet_speed > 15:
        stats.bullet_speed = 15


def gun_kill(stats, screen, score, gun, enemies, bullets):
    '''Столкновение пушки и армии'''
    if stats.guns_left > 0:
        stats.guns_left -= 1
        score.is_next_round = True
        stats.bullet_speed = 0
        score.image_lives()
        enemies.empty()
        bullets.empty()
        create_army(screen, enemies, stats)
        gun.revive_gun()
        time.sleep(2)
    else:
        stats.play = False
        pygame.time.delay(500)
        score.show_game_over()
        pygame.time.delay(2000)
        sys.exit()


def create_army(screen, enemies, stats, extra_speed=0):
    '''Создание армии пришельцев (вернее её случайный выбор)'''
    select_army = random.randint(4, 4)  # !!!
    if select_army == 1:
        armies.rectangle(screen, enemies, extra_speed, stats)
    elif select_army == 2:
        armies.wedge(screen, enemies, extra_speed)
    elif select_army == 3:
        armies.chess(screen, enemies, extra_speed)
    elif select_army == 4:
        armies.heart(screen, enemies, extra_speed)
    elif select_army == 5:
        armies.skelet(screen, enemies, extra_speed)
    elif select_army == 6:
        armies.smiley_face(screen, enemies, extra_speed)
    elif select_army == 7:
        armies.semicircle(screen, enemies, extra_speed)  # !!!


def update_enemies(gun, enemies, score, stats, screen, bullets):
    '''Обновляет позицию какашек'''
    enemies.update()
    if pygame.sprite.spritecollideany(gun, enemies):
        gun_kill(stats, screen, score, gun, enemies, bullets)
    check_army(stats, screen, score, gun, enemies, bullets)


def check_army(stats, screen, score, gun, enemies, bullets):
    '''Проверка, добрались ли пришельцы до края экрана'''
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, score, gun, enemies, bullets)
            break


def check_high_score(stats, score):
    '''Проверка новых рекордов'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.image_high_score()
        with open('scores.txt', 'w') as f:
            f.write(str(stats.high_score))
