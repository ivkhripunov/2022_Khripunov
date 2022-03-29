import math
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
        self.radius = randint(10, 30)
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

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global ball_array, bullet
        bullet += 1
        new_ball = Ball(self.x)
        new_ball.radius += 5
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        ball_array.append(new_ball)
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

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Opponent(Gun):
    def __init__(self):
        super().__init__(WIDTH - 100)


def create_target_array(number_of_targets):
    targets_array = []
    for i in range(number_of_targets):
        targets_array.append(Target())

    return targets_array


def draw_game_objects(guns, targets, balls):
    screen.fill(WHITE)
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


def process_event(ball, targets, rating):
    for i in range(len(targets)):
        quaddistance = (targets[i].x - ball.x) ** 2 + (targets[i].y - ball.y) ** 2

        if quaddistance <= (targets[i].radius + ball.radius) ** 2:
            rating += 1
            targets[i] = Target()

    return targets, rating


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
score = 0
ball_array = []
target_array = create_target_array(4)

clock = pygame.time.Clock()
finished = False
gun = Gun()
opponent = Opponent()
while not finished:
    draw_game_objects(gun, target_array, ball_array)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end()
            bullet += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting()

    if bullet:
        target_array, score = process_event(ball_array[-1], target_array, score)

    move_game_objects(target_array, ball_array)
    gun.power_up()

pygame.quit()
