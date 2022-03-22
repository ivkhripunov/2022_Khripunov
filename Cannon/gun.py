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
    def __init__(self, screen: pygame.Surface, x=40, y=450, gravity=4):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(1, 5)]
        self.live = 30
        self.gravity = gravity
        self.reduction = 0.7
        self.generator_key = randint(1, 1)

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
        if self.generator_key == 1:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.radius
            )

class Target(Ball):
    def __init__(self):
        super().__init__(screen, randint(100, 700), randint(100, 500), gravity=0)
        """
        Инициализация класса
        """
        self.color = RED
        self.vx = randint(5, 10)
        self.vy = randint(5, 10)
        self.radius = randint(10, 30)
        self.reduction = 1
        #self.generator_key == 1


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global ball_array, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.radius += 5
        self.angle = math.atan((event.pos[1] - new_ball.y) / (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        ball_array.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.pos[1] - 450) / (event.pos[0] - 40))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(
            self.screen,
            self.color,
            [[20, 450], [20 - 5 * math.sin(self.angle), 450 + 5 * math.cos(self.angle)],
             [20 - 5 * math.sin(self.angle) + self.f2_power * math.cos(self.angle),
              450 + 5 * math.cos(self.angle) + self.f2_power * math.sin(self.angle)],
             [20 + self.f2_power * math.cos(self.angle), 450 + self.f2_power * math.sin(self.angle)]]
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


def create_target_array(number_of_targets):
    targets_array = []
    for i in range(number_of_targets):
        targets_array.append(Target())

    return targets_array


def draw_game_objects(guns, targets, balls):
    screen.fill(WHITE)
    guns.draw()
    for target in targets:
        target.draw()

    for ball in balls:
        ball.draw()

    pygame.display.update()


def move_game_objects(targets, balls):
    for target in targets:
        target.move()

    for ball in balls:
        ball.move()


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
target_array = create_target_array(3)

clock = pygame.time.Clock()
gun = Gun(screen)
finished = False

while not finished:
    draw_game_objects(gun, target_array, ball_array)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            bullet += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    if bullet:
        target_array, score = process_event(ball_array[-1], target_array, score)

    move_game_objects(target_array, ball_array)
    gun.power_up()

pygame.quit()
