import math
import time
from random import randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, x=40, y=450, gravity=4, reduction=0.1, target=False):
        """
        Инициализация класса Ball
        :param x: координата
        :param y: координата
        :param gravity: значение гравитации для шара
        :param reduction: коэффициент угасания
        :param target: цель/не цель
        """

        self.x = x
        self.y = y
        self.radius = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(1, 5)]
        self.live = 30
        self.gravity = gravity
        self.reduction = reduction
        self.target = target

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 + self.radius:
            self.vx = - self.reduction * self.vx
            self.vy = self.reduction * self.vy
            self.x = self.radius

        elif self.y < 0 + self.radius:
            self.vy = - self.reduction * self.vy
            self.vx = self.reduction * self.vx
            self.y = self.radius

        elif self.x > WIDTH - self.radius:
            self.vx = - self.reduction * self.vx
            self.vy = self.reduction * self.vy
            self.x = WIDTH - self.radius

        elif self.y > HEIGHT - self.radius:
            self.vy = - self.reduction * self.vy
            self.vx = self.reduction * self.vx
            self.y = HEIGHT - self.radius

    def draw(self, surface):
        """
        Отрисовка шарика
        :param surface: поверхность для отрисовки
        """
        pygame.draw.circle(
            surface,
            self.color,
            (self.x, self.y),
            self.radius
        )


class Target(Ball):
    def __init__(self):
        """
        Инициализация класса цели
        """
        super().__init__(randint(100, 700), randint(100, 500), gravity=0, reduction=0, target=True)
        self.color = RED
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.radius = randint(10, 15)
        self.reduction = 1
        self.generator_key = randint(1, 2)

    def draw(self, surface):
        """
        Отрисовка цели
        :param surface: поверхность для отрисовки
        """
        if self.generator_key == 1:
            super().draw(surface)
        elif self.generator_key == 2:
            pygame.draw.circle(surface, self.color, (self.x, self.y), int(self.radius))
            pygame.draw.circle(surface, (0, 255, 0), (self.x, self.y), int(self.radius * 3 / 4))

    def move(self):
        """
        Обработка передвижения цели
        """
        if self.generator_key == 1:
            super().move()
        elif self.generator_key == 2:
            self.vx += randint(-3, 3)
            if self.vx > 10:
                self.vx = 10
            if self.vx < -10:
                self.vx = -10
            self.vy += randint(-3, 3)
            if self.vy > 10:
                self.vy = 10
            if self.vy < -10:
                self.vy = -10
            super().move()


class Gun:
    def __init__(self, x=100):
        """
        Инициализация класса пушки
        :param x: положение пушки по горизонтали
        """
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY
        self.x = x
        self.v = 0
        self.rocket = Rocket()
        self.released = False

    def fire2_start(self):
        """
        Функция начала прицеливания
        """
        self.f2_on = 1

    def fire2_end(self, balls_array):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        :param balls_array: массив шаровых снарядов
        """
        new_ball = Ball(self.x)
        new_ball.radius += 5
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

        return balls_array

    def move(self):
        """
        Движение танка
        """
        self.x += self.v

        if self.x < 25:
            self.x = 25
        if self.x > WIDTH - 25:
            self.x = WIDTH - 25
        if WIDTH / 2 - 50 < self.x < WIDTH / 2:
            self.x = WIDTH / 2 - 50
        if WIDTH / 2 < self.x < WIDTH / 2 + 50:
            self.x = WIDTH / 2 + 50
        if not self.released:
            self.rocket.x = self.x - 10

    def move_key(self, events):
        """
        Обработка движения пушки по нажатию
        :param events: игровое событие
        """

        if events.key == pygame.K_LEFT:
            self.v = -5
        elif events.key == pygame.K_RIGHT:
            self.v = 5

    def stop_key(self, events):
        """
        Остановка движения по нажатию
        :param events: игровое событие
        """
        if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
            self.v = 0

    def targeting(self, events):
        """Прицеливание. Зависит от положения мыши.
        :param events: игровое событие
        """
        if events.pos[0] - self.x != 0 and events.pos[0] > self.x and events.pos[1] < 450:
            self.angle = math.atan((events.pos[1] - 450) / (events.pos[0] - self.x))
        elif events.pos[0] - self.x != 0 and events.pos[0] < self.x and events.pos[1] < 450:
            self.angle = math.atan((events.pos[1] - 450) / (events.pos[0] - self.x)) + math.pi
        else:
            self.angle = - math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self, surface):
        """
        Отрисовка пушки и ракеты
        :param surface: поверхность для отрисовки
        """
        pygame.draw.polygon(
            surface,
            self.color,
            [[self.x, 450], [self.x - 5 * math.sin(self.angle), 450 + 5 * math.cos(self.angle)],
             [self.x - 5 * math.sin(self.angle) + self.f2_power * math.cos(self.angle),
              450 + 5 * math.cos(self.angle) + self.f2_power * math.sin(self.angle)],
             [self.x + self.f2_power * math.cos(self.angle), 450 + self.f2_power * math.sin(self.angle)]]
        )
        pygame.draw.rect(surface, GREEN, (self.x - 15, 450, 30, 15))
        pygame.draw.circle(surface, GREY, (self.x - 8, 466), 5)
        pygame.draw.circle(surface, GREY, (self.x + 8, 466), 5)

        self.rocket.draw(surface)

    def release(self, events):
        """
        Функция запуска ракеты по нажатию на стрелку вверх
        :param events: игровое событие
        """
        if events.type == pygame.KEYDOWN and events.key == pygame.K_UP:
            self.released = True
            self.rocket.v = 10

    def power_up(self):
        """
        Зарядка ракеты
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Rocket:
    def __init__(self):
        """
        Инициализация класса ракета
        """
        self.x = 100
        self.y = 460
        self.v = 0
        self.angle_change = 0
        self.direction = math.pi / 2
        self.key = 1

    def draw(self, surface):
        """
        Отрисовка ракеты
        :param surface: поверхность для отрисовки
        """
        if self.key:
            pygame.draw.polygon(
                surface,
                BLACK,
                [[self.x, self.y], [self.x - 5 * math.sin(-self.direction), self.y + 5 * math.cos(-self.direction)],
                 [self.x - 5 * math.sin(-self.direction) + 30 * math.cos(-self.direction),
                  self.y + 5 * math.cos(-self.direction) + 30 * math.sin(-self.direction)],
                 [self.x + 30 * math.cos(-self.direction), self.y + 30 * math.sin(-self.direction)]]
            )

    def change_direction_key(self, events):
        """
        Начало поворота по нажатию клавиши
        :param events: игровое событие
        """
        if events.key == pygame.K_UP:
            self.angle_change = 0.05
        elif events.key == pygame.K_DOWN:
            self.angle_change = -0.05

    def stop_change_direction_key(self, events):
        """
        Остановка поворота по отпусканию клавиши
        :param events:
        """
        if events.key == pygame.K_UP or events.key == pygame.K_DOWN:
            self.angle_change = 0

    def move(self):
        """
        Обработка движения ракеты с учетом возможности изменения направления ее движения нажатием на стрелки
        """
        self.direction += self.angle_change
        if self.direction < -math.pi / 2:
            self.direction = - math.pi / 2
        elif self.direction > math.pi / 2:
            self.direction = math.pi / 2

        self.x += self.v * math.cos(self.direction)
        self.y += - self.v * math.sin(self.direction)


class Bomber:
    def __init__(self):
        """
        Инициализация класса бомбардировщика
        """
        self.color = MAGENTA
        self.x = -2000
        self.y = 100

    def draw(self, surface):
        """
        Отрисовка бомбардировщика
        :param surface: поверхность для отрисовки
        """
        pygame.draw.rect(surface, self.color, (self.x, self.y, 100, 20))
        pygame.draw.rect(surface, self.color, (self.x + 50, self.y - 30, 20, 80))

    def move(self):
        """
        Обработка движения бомбардировщика
        """
        self.x += 7
        if self.x > WIDTH + 10:
            self.x = randint(-5000, - 1000)
            self.y = randint(50, 150)

    def bomb(self, target_pool):
        """
        Функция бомбометания
        @:param target_pool массив целей
        :return обновленный массив целей
        """
        if randint(50, 200) < self.x < randint(600, 750) and len(target_pool) < 50:
            new_ball = Target()
            new_ball.radius = randint(3, 7)
            new_ball.vx = randint(-5, 5)
            new_ball.vy = randint(-3, 3)
            new_ball.x = int(self.x) + 20
            new_ball.y = self.y + 20
            target_pool.append(new_ball)

        return target_pool


class Opponent(Gun):
    def __init__(self):
        """
        Инициализация класса бота
        """
        super().__init__()
        self.x = WIDTH / 2 + 50
        self.direction = True
        self.angle = - 3 * math.pi / 5
        self.f2_power = 30
        self.rocket.key = 0

    def fire(self, balls_array):
        """
        Реализация стрельбы ботом
        :param balls_array: массив шаровых снарядов
        :return: обновленный массив шаровых снарядов
        """
        self.f2_power = randint(40, 60)
        new_ball = Ball(int(self.x))
        new_ball.radius += 5
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls_array.append(new_ball)

        return balls_array

    def move(self, events=0):
        """
        Обработка движения танка-бота
        """
        if self.x > WIDTH - 25 or self.x < WIDTH / 2 + 50:
            self.direction = not self.direction

        if self.direction:
            self.x += 3
            self.angle -= math.pi / 1000

        else:
            self.x -= 3
            self.angle += math.pi / 1000


def create_target_array(number_of_targets):
    """
    Создание начального массива целей нужного размера
    :param number_of_targets: необходимое количество целей
    """
    targets_array = []
    for i in range(number_of_targets):
        targets_array.append(Target())

    return targets_array


def draw_game_objects(game_clock, surface, gun_player, targets, balls, opponent_player, bombardier):
    """
    Отрисовка игры
    :param game_clock: игровые часы
    :param surface: поверхность для отрисовки
    :param gun_player: пушка-игрок
    :param targets: массив целей
    :param balls: массив шаровых снарядов
    :param opponent_player: пушка-бот
    :param bombardier: бомбардировщик
    """
    surface.fill(WHITE)

    bombardier.draw(surface)
    gun_player.draw(surface)
    opponent_player.draw(surface)
    for target in targets:
        target.draw(surface)

    for ball in balls:
        ball.draw(surface)

    pygame.draw.rect(surface, GREEN, (0, 471, WIDTH, 130))
    pygame.draw.rect(surface, GREEN, (WIDTH / 2 - 25, 400, 50, 100))
    game_clock.tick(FPS)
    pygame.display.update()


def move_game_objects(begin_time, gun_player, targets, balls, opponent_player, bombardier):
    """
    Обработка движения игровых оъектов
    :param begin_time: время начала игры
    :param gun_player: пушка-игрок
    :param targets: массив целей
    :param balls: массив шаровых снарядов
    :param opponent_player: пушка-бот
    :param bombardier: бомбардировщик
    """
    for target in targets:
        target.move()

    for ball in balls:
        ball.move()

    bombardier.move()
    gun_player.move()
    gun_player.rocket.move()

    if (time.time() - begin_time) % 3 < 0.05:
        balls = opponent_player.fire(balls)

    targets = bombardier.bomb(targets)

    gun_player.rocket.move()
    opponent_player.move()
    gun_player.power_up()

    return gun_player, targets, balls, opponent_player, bombardier


def process_hit(game_gun, ball, targets, rating):
    """
    Обработка события попадание
    :param game_gun: основная пушка
    :param ball: шаровой снаряд
    :param targets: массив целей
    :param rating: сбитые цели
    :return: массив целей, обновленный с учетом уничтоженных объектов
    """
    targets_to_delete = []
    for i in range(len(targets)):
        quad_distance = (targets[i].x - ball.x) ** 2 + (targets[i].y - ball.y) ** 2
        quad_distance_rocket = (targets[i].x - game_gun.rocket.x) ** 2 + (targets[i].y - game_gun.rocket.y) ** 2

        if quad_distance <= (targets[i].radius + ball.radius) ** 2 or quad_distance_rocket <= 2000:
            rating += 1
            targets_to_delete.append(targets[i])

    for element in targets_to_delete:
        targets.remove(element)
    return targets, rating


def start_game():
    """
    Функция начала игры. Инициализирует основные игровые объекты
    :return время начало игры, массив шаровых снарядов, массив целей,
    количество снарядов, счет, флаг конца игры, пушка-игрок, пушка-бот, бомбардировщик
    """
    new_gun = Gun()
    new_opponent = Opponent()
    begin_time = time.time()
    new_bomber = Bomber()
    flag = False
    bullets = 0
    rating = 0
    balls_array = []

    print("Welcome to canon game!")
    print("Use left and arrow keys to move your tank.")
    print("Press up arrow key to release the rocket.")
    print("Use up and down arrow keys to control the rocket.")
    print("The game will start in 5 seconds.")
    print("Good luck!")
    time.sleep(0)

    return begin_time, balls_array, create_target_array(4), bullets, rating, flag, new_gun, new_opponent, new_bomber


def process_event(events, flag, bullets, array_of_balls, game_gun):
    """
    Обработка игрового события
    :param events: игровое событие
    :param flag: флаг конца игры
    :param bullets: количество снарядов
    :param array_of_balls: массив шаровых снарядов
    :param game_gun: основная пушка
    :return: флаг конца игры, количество снарядов, массив шаровых снарядов, пушка
    """
    if events.type == pygame.QUIT:
        flag = True
    elif events.type == pygame.MOUSEBUTTONDOWN:
        game_gun.fire2_start()
    elif events.type == pygame.MOUSEBUTTONUP:
        array_of_balls = game_gun.fire2_end(array_of_balls)
        bullets += 1

    elif events.type == pygame.MOUSEMOTION:
        game_gun.targeting(events)

    if events.type == pygame.KEYDOWN:
        game_gun.move_key(events)
        if game_gun.released:
            game_gun.rocket.change_direction_key(events)

    elif events.type == pygame.KEYUP:
        game_gun.stop_key(events)
        if game_gun.released:
            game_gun.rocket.stop_change_direction_key(events)

    game_gun.release(events)

    return flag, bullets, array_of_balls, game_gun


def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    start_time, ball_array, target_array, bullet, score, finished, gun, opponent, bomber = start_game()

    while not finished:
        draw_game_objects(clock, screen, gun, target_array, ball_array, opponent, bomber)

        for event in pygame.event.get():
            finished, bullet, ball_array, gun = process_event(event, finished, bullet, ball_array, gun)

        if len(ball_array) or gun.released:
            target_array, score = process_hit(gun, ball_array[-1], target_array, score)

        gun, target_array, ball_array, opponent, bomber = move_game_objects(start_time, gun,
                                                                            target_array,
                                                                            ball_array,
                                                                            opponent,
                                                                            bomber)
    pygame.quit()


game()
