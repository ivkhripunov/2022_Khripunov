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

clock = pygame.time.Clock()


class Player(object):
    def __init__(self, player_name, rating=0):
        """
        Инициализация класса
        :param player_name: имя игрока
        :param rating: рейтинг(счет)
        """
        self.name = player_name
        self.score = 0
        self.rating = rating

    def set_points(self, score, rating):
        """
        Обновление рейтинговых значений
        :param score: обновсленный счет (количество сбитых целей)
        :param rating: обновленынй рейтинг
        :return: none
        """
        self.score = score
        self.rating = rating


def players_list():
    """
    Заполнение массива игроков: каждый вводит свое имя.
    :return: массив игроков
    """
    print("Number of players:")
    number_of_players = int(input())
    players = []
    for i in range(number_of_players):
        print("Player's name:")
        player_name = input()
        players.append(Player(player_name))

    return players


def analyse_rating_table(players):
    """
    Анализ таблицы с результатами (если полученные в игре результаты меньше результатов из таблицы,
    то табличные данные не будут изменены; если появился новый игрок, то его результаты будут занесены в таблицу.
    :param players: массив игроков
    :return: измененный массив игроков
    """
    rating_file = open('score.txt', 'r')

    table = rating_file.readlines()

    for line in table:
        if line != "Leaderboard:\n":
            name = line.split()[0]
            rating = int(line.split()[1])

            player_found = False
            for player in players:
                if player.name == name:
                    if player.rating < rating:
                        player.rating = rating

                    player_found = True

            if not player_found:
                players.append(Player(name, rating))

    rating_file.close()

    return players


def write_rating_table(players):
    """
    Заполнение таблицы с рейтингом
    :param players: массив игроков
    """

    players = analyse_rating_table(players)

    rating_file = open('score.txt', 'w')
    rating_file.write("Leaderboard:\n")
    players.sort(key=lambda player: player.rating, reverse=True)
    for i in range(len(players)):
        rating_file.write(players[i].name + " " + str(players[i].rating) + "\n")

    rating_file.close()


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


def start_screen(player, timer):
    """
    Стартовый экран
    :param player: игрок
    :param timer: таймер игры
    :return: флаг окончания игры, время начала игры
    """
    print(player.name, "'s ", "turn")
    print("Start in 5 sec")
    print("You will have {} seconds".format(timer))
    print("Do not hit bombs!")
    print("Press button on the keyboard to hit the target")
    time.sleep(5)

    return False, time.time()


def create_ball_array(COLORS):
    """
    Создаем массив целей
    :param COLORS: массив цветов
    :return: массив целей
    """
    ball_array = []

    for i in range(10):
        ball_array.append(Target(COLORS[randint(1, 5)]))

    return ball_array


def process_step(finished, ball_array):
    """
    Обработка игрового шага
    :param finished: флаг окончания игры
    :param ball_array: массив целей
    :return: флаг, массив целей (после изменения координат)
    """
    if finished:
        game_over_screen(player)

    if time.time() - start_time >= timer:
        finished = True
        game_over_screen(player)

    for target in ball_array:
        target.draw()
        target.move()

    pygame.display.update()
    screen.fill(BLACK)

    return finished, ball_array

players = players_list()

# игроки поочереди играют
for player in players:

    ball_array = create_ball_array(COLORS)
    finished, start_time = start_screen(player, timer)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                finished, score, rating = process_event(ball_array, player.score,
                                                        player.rating)
                player.set_points(score, rating)

#переопределение массива целей - необходимая мера
        finished, ball_array = process_step(finished, ball_array)

        if finished:
            continue

pygame.quit()

write_rating_table(players)
