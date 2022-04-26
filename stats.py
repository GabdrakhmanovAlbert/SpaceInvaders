class Stats():
    '''Создание статистики текущей игры'''

    def __init__(self):
        '''Инициализация статистики'''
        self.reset_stats()
        self.play = True
        with open('scores.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        '''статистика, изменяющаяся во время игры'''
        self.guns_left = 2  # количество жизней пушки
        self.bullet_speed = 0  #? скорость пуль

        self.score = 0  # счёт текущей игры

        self.counter_rounds = 1

        # * Особый враг - не Абстрактная какашка
        #! Первая задаёт лимит случайной генерации особых врагов на раунд
        #! Вторая количество особых врагов на раунд
        #! Третья индексы размещения особых врагов на игровом поле
        self.special_enemy_limiter = 0
        self.special_enemies = 0
        self.indexes_special_enemies = set()
