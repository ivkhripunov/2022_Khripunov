import time
from random import randint, uniform

import pygame
from numpy import cos, sin, pi
from pygame import draw as dr

pygame.init()

FPS = 30
WIDTH = 1200
HEIGHT = 900
timer = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Player(object):
    def __init__(self, player_name):
        """
        Инициализация класса
        :param player_name: имя игрока
        """
        self.name = player_name
        self.score = 0
        self.rating = 0

    def set_points(self, score, rating):
        """
        Обновление рейтинговых значений
        :param score: обновсленный счет
        :param rating: обновленынй рейтинг
        :return: none
        """
        self.score = score
        self.rating = rating


# заполнение списка игроков
print("Number of players:")
number_of_players = int(input())
players = []
for i in range(number_of_players):
    print("Player's name:")
    player_name = input()
    players.append(Player(player_name))


def score_table(players):
    """
    Заполнение таблицы с рейтингом
    :param players: массив игроков
    :return:
    """
    players.sort(key=lambda player: player.rating, reverse=True)
    score_file = open('score.txt', 'w')
    score_file.write("Best players:\n")

    for i in range(len(players)):
        score_file.write(str(i + 1) + ")" + " " + players[i].name + " " + str(players[i].rating) + "\n")

    score_file.close()


class Target(object):
    def __init__(self, color):
        """
        Инициализация класса
        :param color: цвет цели
        """
        self.color = color
        self.coord = [randint(100, 1100), randint(100, 900)]
        self.radius = randint(10, 30)
        self.direction = uniform(0, 2 * pi)
        self.speed = randint(5, 10)
        self.generator_key = randint(-1, 1)

    def draw(self):
        """
        Отрисовка цели
        """
        if self.generator_key == 0:
            dr.circle(screen, self.color, self.coord, self.radius)
        elif self.generator_key == 1:
            dr.rect(screen, self.color, (self.coord[0], self.coord[1], self.radius, self.radius))
        elif self.generator_key == -1:
            dr.circle(screen, self.color, self.coord, self.radius)
            dr.circle(screen, (255, 0, 0), self.coord, self.radius * 3 / 4)

    def move(self):
        """
        Изменение координат цели, контроль столкновений со стенками
        """
        if self.generator_key == -1:
            self.direction = uniform(self.direction - pi / 6, self.direction + pi / 6)
            self.speed = randint(self.speed - 1, self.speed + 1)

        x, y = self.coord
        x += self.speed * cos(self.direction)
        y += self.speed * sin(self.direction)

        if x < 0 + self.radius:
            self.direction = pi - self.direction + uniform(-pi / 6, pi / 6)
            x = self.radius

        elif y < 0 + self.radius:
            self.direction = - self.direction + uniform(-pi / 6, pi / 6)
            y = self.radius

        elif x > WIDTH - self.radius:
            self.direction = pi - self.direction + uniform(-pi / 6, pi / 6)
            x = WIDTH - self.radius

        elif y > HEIGHT - self.radius:
            self.direction = - self.direction + uniform(-pi / 6, pi / 6)
            y = HEIGHT - self.radius

        self.coord = x, y


def process_event(ball_array, counter, rating):
    """
    Обработка события
    :param ball_array: массив целей
    :param counter: количество сбитых игроком целей
    :param rating: рейтинг игрока
    :return: измененное количество сбитых целей, измененный рейтинг, измененное количество промахов
    """
    for i in range(len(ball_array)):
        x, y = pygame.mouse.get_pos()
        quad_distance = (x - ball_array[i].coord[0]) ** 2 + (
                y - ball_array[i].coord[1]) ** 2

        if quad_distance <= ball_array[i].radius ** 2:
            print("Gotcha!")
            counter += 1
            rating += ball_array[i].radius * ball_array[i].speed + ball_array[i].generator_key * ball_array[i].radius
            if ball_array[i].generator_key == -1:
                print("You hit the bomb!")
                ball_array[i] = Target(COLORS[randint(0, 5)])
                return True, counter, rating

            ball_array[i] = Target(COLORS[randint(0, 5)])
            continue

    if rating < 0:
        rating = 0
    return False, counter, rating


def game_over_screen(player):
    """
    Экран смерти
    :param player: игрок
    """
    print("Game over")
    print("Here are you stats, ", player.name, ":")
    print("Score: ", player.score)
    print("Rating: ", player.rating)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()

# игроки поочереди играют
for player in players:

    # заполнение массива целей
    ball_array = []

    for i in range(10):
        ball_array.append(Target(COLORS[randint(0, 5)]))

    print(player.name, "'s ", "turn")
    print("Start in 5 sec")
    print("You will have {} seconds".format(timer))
    time.sleep(5)

    finished = False
    start_time = time.time()

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                finished, score, rating = process_event(ball_array, player.score,
                                                        player.rating)
                player.set_points(score, rating)

        if finished:
            game_over_screen(player)
            continue

        for target in ball_array:
            target.draw()
            target.move()

        if time.time() - start_time >= timer:
            finished = True
            game_over_screen(player)
            continue

        pygame.display.update()
        screen.fill(BLACK)

pygame.quit()

score_table(players)
