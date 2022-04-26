import pygame.font
from gun import Live
from pygame.sprite import Group


class Scores():
    '''Вывод игровой информации'''

    def __init__(self, screen, stats):
        '''Инициализируем подсчёт очков'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (116, 255, 3)
        self.text_color_lose = (235, 14, 14)
        self.back_color = (0, 0, 50)
        # pg.font.SysFont(вид шрифта, размер, полужирный:bool, курсив:bool)
        self.font = pygame.font.SysFont('algerian', 28, True)
        self.font_heading = pygame.font.SysFont(
            'algerian', 60, False, False)  # ? bahnschrift тоже смотрится норм
        self.image_score()
        self.image_high_score()
        self.image_lives()
        self.image_game_over()
        self.is_next_round = True

    def transform_score(self, score):
        '''Добавляет к игровому счёту доп. нули слева, для формата "000001"'''
        to_print_score = str(score)
        if len(to_print_score) >= 6:
            return str(score)
        extra_zeros = 6 - len(to_print_score)
        zeros = []
        for _ in range(extra_zeros):
            zeros.append('0')
        to_print_score = to_print_score.split()
        to_print_score.insert(0, ''.join(zeros))
        return ''.join(to_print_score)

    def image_score(self):
        '''Преобразовывает текст счёта в графическое изображение'''
        to_print_score = self.transform_score(self.stats.score)
        self.message_score = self.font.render(
            '<SCORE> ' + to_print_score, True, self.text_color, self.back_color)
        self.score_rect = self.message_score.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20

    def image_high_score(self):
        '''Преобразует рекорд в графическое изображение'''
        to_print_high_score = self.transform_score(self.stats.high_score)
        self.message_high_score = self.font.render(
            '<HI-SCORE> ' + to_print_high_score, False, self.text_color, self.back_color)
        self.high_score_rect = self.message_high_score.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx - 150
        self.high_score_rect.top = 20

    def image_game_over(self):
        '''Сообщение о поражении в графическое изображение'''
        self.message_game_over = self.font_heading.render(
            'GAME OVER', True, self.text_color_lose)
        self.game_over_rect = self.message_game_over.get_rect()
        self.game_over_rect.centerx = self.screen_rect.centerx
        self.game_over_rect.top = 300

    def image_lives(self):
        '''Преобразует количество жизней в графическое изображение'''
        self.lives = Group()
        for live_number in range(self.stats.guns_left):
            live = Live(self.screen)
            live.rect.x = 10
            live.rect.y = 15 + live_number * live.rect.width
            self.lives.add(live)

    def show_score(self):
        '''Вывод счёта на экран'''
        self.screen.blit(self.message_score, self.score_rect)
        self.screen.blit(self.message_high_score, self.high_score_rect)
        self.lives.draw(self.screen)

    def show_game_over(self):
        '''Вывод сообщения о поражении на экран'''
        self.screen.blit(self.message_game_over, self.game_over_rect)
        pygame.display.flip()

    def next_round(self, stats):
        '''Создание и отрисовка счётчика раундов'''
        self.message_next_round = self.font_heading.render(
            f'ROUND {stats.counter_rounds}', True, self.text_color)
        self.next_round_rect = self.message_next_round.get_rect()
        self.next_round_rect.centerx = self.screen_rect.centerx
        self.next_round_rect.top = 300

        self.screen.blit(self.message_next_round, self.next_round_rect)
