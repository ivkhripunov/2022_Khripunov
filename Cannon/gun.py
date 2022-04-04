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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Ball:
    def __init__(self, x=40, y=450, gravity=4, reduction=0.1, target=False):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
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
        self.type = 1

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

    def draw(self):
        if self.type == 1:
            pygame.draw.circle(
                screen,
                self.color,
                (self.x, self.y),
                self.radius
            )

        if self.type == 2 and not self.target:
            pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius)


class Target(Ball):
    def __init__(self):
        super().__init__(randint(100, 700), randint(100, 500), gravity=0, reduction=0, target=True)
        """
        Инициализация класса
        """
        self.color = RED
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.radius = randint(10, 15)
        self.reduction = 1
        self.generator_key = randint(1, 2)

    def draw(self):
        if self.generator_key == 1:
            super().draw()
        elif self.generator_key == 2:
            pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.radius))
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), int(self.radius * 3 / 4))

    def move(self):
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
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY
        self.x = x
        self.rocket = Rocket()
        self.released = False

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, balls_array):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(self.x)
        new_ball.radius += 5
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def move(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x -= 5
            elif event.key == pygame.K_RIGHT:
                self.x += 5

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

        if self.released:
            self.rocket.move()

    def targetting(self):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] - self.x != 0 and event.pos[0] > self.x and event.pos[1] < 450:
            self.angle = math.atan((event.pos[1] - 450) / (event.pos[0] - self.x))
        elif event.pos[0] - self.x != 0 and event.pos[0] < self.x and event.pos[1] < 450:
            self.angle = math.atan((event.pos[1] - 450) / (event.pos[0] - self.x)) + math.pi
        else:
            self.angle = - math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(
            screen,
            self.color,
            [[self.x, 450], [self.x - 5 * math.sin(self.angle), 450 + 5 * math.cos(self.angle)],
             [self.x - 5 * math.sin(self.angle) + self.f2_power * math.cos(self.angle),
              450 + 5 * math.cos(self.angle) + self.f2_power * math.sin(self.angle)],
             [self.x + self.f2_power * math.cos(self.angle), 450 + self.f2_power * math.sin(self.angle)]]
        )
        pygame.draw.rect(screen, GREEN, (self.x - 15, 450, 30, 15))
        pygame.draw.circle(screen, GREY, (self.x - 8, 466), 5)
        pygame.draw.circle(screen, GREY, (self.x + 8, 466), 5)

        self.rocket.draw()

    def release(self):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.released = True
            self.rocket.v = 10

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Rocket:
    def __init__(self):
        self.x = 100
        self.y = 460
        self.v = 0
        self.direction = math.pi / 2
        self.key = 1

    def draw(self):
        if self.key:
            pygame.draw.polygon(
                screen,
                BLACK,
                [[self.x, self.y], [self.x - 5 * math.sin(-self.direction), self.y + 5 * math.cos(-self.direction)],
                 [self.x - 5 * math.sin(-self.direction) + 30 * math.cos(-self.direction),
                  self.y + 5 * math.cos(-self.direction) + 30 * math.sin(-self.direction)],
                 [self.x + 30 * math.cos(-self.direction), self.y + 30 * math.sin(-self.direction)]]
            )

    def move(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction += 0.05
            if event.key == pygame.K_DOWN:
                self.direction -= 0.05

            if self.direction < -math.pi / 2:
                self.direction = - math.pi / 2
            elif self.direction > math.pi / 2:
                self.direction = math.pi / 2

        self.x += self.v * math.cos(self.direction)
        self.y += - self.v * math.sin(self.direction)


class Bomber:
    def __init__(self):
        self.color = MAGENTA
        self.x = -2000
        self.y = 100

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 100, 20))
        pygame.draw.rect(screen, self.color, (self.x + 50, self.y - 30, 20, 80))

    def move(self):
        self.x += 7
        if self.x > WIDTH + 10:
            self.x = randint(-5000, - 1000)
            self.y = randint(50, 150)

    def bomb(self):
        if randint(50, 200) < self.x < randint(600, 750) and len(target_array) < 50:
            new_ball = Target()
            new_ball.radius = randint(3, 7)
            new_ball.vx = randint(-5, 5)
            new_ball.vy = randint(-3, 3)
            new_ball.x = int(self.x) + 20
            new_ball.y = self.y + 20
            target_array.append(new_ball)


class Opponent(Gun):
    def __init__(self):
        super().__init__()
        self.x = WIDTH / 2 + 50
        self.direction = True
        self.angle = - 3 * math.pi / 5
        self.f2_power = 30
        self.rocket.key = 0

    def fire(self, balls_array):
        self.f2_power = randint(40, 60)
        new_ball = Ball(int(self.x))
        new_ball.radius += 5
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls_array.append(new_ball)

    def move(self):
        if self.x > WIDTH - 25 or self.x < WIDTH / 2 + 50:
            self.direction = not self.direction

        if self.direction:
            self.x += 3
            self.angle -= math.pi / 1000

        else:
            self.x -= 3
            self.angle += math.pi / 1000


def create_target_array(number_of_targets):
    targets_array = []
    for i in range(number_of_targets):
        targets_array.append(Target())

    return targets_array


def draw_game_objects(guns, targets, balls):
    screen.fill(WHITE)

    bomber.draw()

    guns.draw()
    opponent.draw()
    for target in targets:
        target.draw()

    for ball in balls:
        ball.draw()

    pygame.draw.rect(screen, GREEN, (0, 471, WIDTH, 130))
    pygame.draw.rect(screen, GREEN, (WIDTH / 2 - 25, 400, 50, 100))

    pygame.display.update()


def move_game_objects(targets, balls):
    for target in targets:
        target.move()

    for ball in balls:
        ball.move()

    gun.move()
    bomber.move()

    if (time.time() - start_time) % 3 < 0.05:
        opponent.fire(ball_array)

    bomber.bomb()

    opponent.move()
    gun.power_up()


def process_hit(ball, targets, rating):
    targets_to_delete = []
    for i in range(len(targets)):
        quaddistance = (targets[i].x - ball.x) ** 2 + (targets[i].y - ball.y) ** 2
        quad_distance_rocket = (targets[i].x - gun.rocket.x) ** 2 + (targets[i].y - gun.rocket.y) ** 2

        if quaddistance <= (targets[i].radius + ball.radius) ** 2 or quad_distance_rocket <= 1000:
            rating += 1
            targets_to_delete.append(targets[i])

    for element in targets_to_delete:
        targets.remove(element)
    return targets, rating


def start_game():
    new_gun = Gun()
    new_opponent = Opponent()
    begin_time = time.time()
    new_bomber = Bomber()
    return begin_time, [], create_target_array(4), 0, 0, False, new_gun, new_opponent, new_bomber


def process_event(flag, bullets):
    if event.type == pygame.QUIT:
        flag = True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        gun.fire2_start()
    elif event.type == pygame.MOUSEBUTTONUP:
        gun.fire2_end(ball_array)
        bullets += 1
    elif event.type == pygame.MOUSEMOTION:
        gun.targetting()

    gun.release()

    return flag, bullets


start_time, ball_array, target_array, bullet, score, finished, gun, opponent, bomber = start_game()
while not finished:
    draw_game_objects(gun, target_array, ball_array)
    clock.tick(FPS)
    for event in pygame.event.get():
        finished, bullet = process_event(finished, bullet)

    if bullet or gun.released:
        target_array, score = process_hit(ball_array[-1], target_array, score)

    move_game_objects(target_array, ball_array)

pygame.quit()
