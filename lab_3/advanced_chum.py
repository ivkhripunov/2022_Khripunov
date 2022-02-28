from math import sqrt, pi, cos, sin

import pygame
import pygame.draw as dr

pygame.init()

WHITE = (250, 250, 250)
GREY = (214, 214, 214)
WHITE_GREY = (100, 100, 100)
AREAL = (170, 170, 160)
BLACK = (0, 0, 0)
ALMOST_BLACK = (240, 240, 240)
BROWN = (168, 138, 98)
FISH = (50, 168, 121)
BLUE = (27, 44, 150)
RED = (196, 43, 87)
LIGHT_BROWN = (222, 207, 184)
DARK_BROWN = (89, 69, 37)

WIDTH = 794
HEIGHT = 1123
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Ice
dr.rect(screen, WHITE, (0, 450, WIDTH, HEIGHT / 2))
# Sky
dr.rect(screen, GREY, (0, 0, WIDTH, 450))


def draw_1_level_chum(x, y, radius, width):
    """
    The function, which is used to draw the 1st level of chum
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.line(screen, BLACK, (x - 5 * radius / 6, y), (x - 5 * radius / 6, y - radius / 4), width)
    dr.line(screen, BLACK, (x + 5 * radius / 6, y), (x + 5 * radius / 6, y - radius / 4), width)
    dr.line(screen, BLACK, (x - 5 * radius / 12, y), (x - 5 * radius / 12, y - radius / 4), width)
    dr.line(screen, BLACK, (x + 5 * radius / 12, y), (x + 5 * radius / 12, y - radius / 4), width)
    dr.line(screen, BLACK, (x, y), (x, y - radius / 4), width)  # middle


def draw_2_level_chum(x, y, radius, width):
    """
    The function, which is used to draw the 2nd level of chum
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.line(screen, BLACK, (x - 5 * radius / 24, y - radius / 4), (x - 5 * radius / 24, y - radius / 2), width)
    dr.line(screen, BLACK, (x + 5 * radius / 24, y - radius / 4), (x + 5 * radius / 24, y - radius / 2), width)
    dr.line(screen, BLACK, (x - 15 * radius / 24, y - radius / 4), (x - 15 * radius / 24, y - radius / 2), width)
    dr.line(screen, BLACK, (x + 15 * radius / 24, y - radius / 4), (x + 15 * radius / 24, y - radius / 2), width)


def draw_3_level_chum(x, y, radius, width):
    """
    The function, which is used to draw the 3rd level of chum
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.line(screen, BLACK, (x, y - radius / 2), (x, y - 3 * radius / 4), width)
    dr.line(screen, BLACK, (x - 10 / 24 * radius, y - radius / 2), (x - 10 / 24 * radius, y - 3 * radius / 4), width)
    dr.line(screen, BLACK, (x + 10 / 24 * radius, y - radius / 2), (x + 10 / 24 * radius, y - 3 * radius / 4), width)


def draw_4_level_chum(x, y, radius, width):
    """
    The function, which is used to draw the 4th level of chum
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.line(screen, BLACK, (x, y - 3 * radius / 4), (x, y - radius), width)


def draw_basic_contour(x, y, radius, width):
    """
    The function, which is used to draw the chum base
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.line(screen, BLACK, (x - radius, y), (x + radius, y), width + 4)  # base
    dr.line(screen, BLACK, (x - sqrt(15) / 4 * radius, y - radius / 4), (x + sqrt(15) / 4 * radius, y - radius / 4),
            width)  # 1 level
    dr.line(screen, BLACK, (x - sqrt(3) / 2 * radius, y - radius / 2), (x + sqrt(3) / 2 * radius, y - radius / 2),
            width)  # 2 level
    dr.line(screen, BLACK, (x - sqrt(7) / 4 * radius, y - 3 * radius / 4),
            (x + sqrt(7) / 4 * radius, y - 3 * radius / 4), width)  # 3 level
    dr.circle(screen, BLACK, (x, y), radius, width)  # arc


def draw_chum(x, y, radius, width):
    """
    The function, which is used to draw the whole chum
    :param x: x coordinates of the center of the chum base
    :param y: y coordinates of the center of the chum base
    :param radius: Radius of chum
    :param width: The width of contour
    :return: nothing
    """
    dr.circle(screen, GREY, (x, y), radius)
    draw_basic_contour(x, y, radius, width)
    draw_1_level_chum(x, y, radius, width)
    draw_2_level_chum(x, y, radius, width)
    draw_3_level_chum(x, y, radius, width)
    draw_4_level_chum(x, y, radius, width)
    # Drawing the path
    dr.rect(screen, ALMOST_BLACK, (x - 5 * radius / 3, y, 10 * radius / 3, 4 * radius / 3))


def draw_rect_angle(surface, color, rect, angle, width=0):
    """
    The function, which is used to rotate a rectangle.
    :param surface: screen
    :param color: color
    :param rect: the parameters of rectangle itself
    :param angle: the angle of rotation counter-clockwise
    :param width: the width of the contour
    :return: nothing
    """
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


def draw_ellipse_angle(surface, color, rect, angle, width=0):
    """
    The function, which is used to rotate a rectangle.
    :param surface: screen
    :param color: color
    :param rect: the parameters of rectangle, in which the ellipse is located
    :param angle: the angle of rotation counter-clockwise
    :param width: the width of the contour
    :return: nothing
    """
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    dr.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


def fin1(x, y, k):
    """
    The function, which is used to draw the 1 fin
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    dr.polygon(screen, RED, ((x + 25 * k, y + 10 * k), (x + 20 * k, y + 26 * k), (x + 35 * k, y + 40 * k)))
    dr.polygon(screen, BLACK, ((x + 25 * k, y + 10 * k), (x + 20 * k, y + 26 * k), (x + 35 * k, y + 40 * k)), width=3)


def fin2(x, y, k):
    """
    The function, which is used to draw the 2 fin
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    dr.polygon(screen, RED, ((x + 25 * k, y - 15 * k), (x + 45 * k, y - 15 * k), (x + 35 * k, y + 10 * k)))
    dr.polygon(screen, BLACK, ((x + 25 * k, y - 15 * k), (x + 45 * k, y - 15 * k), (x + 35 * k, y + 10 * k)), width=3)


def fish_body(x, y, k):
    """
    The function, which is used to draw the body of a fish
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    draw_ellipse_angle(screen, FISH, (x, y, 70 * k, 25 * k), -30)  # body
    draw_ellipse_angle(screen, BLACK, (x, y, 70 * k, 25 * k), -30, width=3)


def fish_tail(x, y, k):
    """
    The function, which is used to draw the tail of a fish
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    dr.polygon(screen, FISH, (
        (x + 70 * k / 2 + 70 * k / 2 * cos(pi / 6), y + 35 * k - sin(pi / 6) * 25 * k / 2),
        (x + 30 * k / 2 + 70 * k * cos(pi / 6), y + 80 * k / 2 + sin(pi / 6) * 25 * k),
        (x + 60 * k / 2 + 70 * k * cos(pi / 6), y + 30 * k / 2 + sin(pi / 6) * 25 * k)))

    dr.polygon(screen, BLACK, (
        (x + 70 * k / 2 + 70 * k / 2 * cos(pi / 6), y + 35 * k - sin(pi / 6) * 25 * k / 2),
        (x + 30 * k / 2 + 70 * k * cos(pi / 6), y + 80 * k / 2 + sin(pi / 6) * 25 * k),
        (x + 60 * k / 2 + 70 * k * cos(pi / 6), y + 30 * k / 2 + sin(pi / 6) * 25 * k)), width=3)


def fish_eye(x, y, k):
    """
    The function, which is used to draw the eye of a fish
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    dr.circle(screen, BLUE, (x + 20 * k, y + 3 * k), 6 * k)  # eye
    dr.circle(screen, BLACK, (x + 20 * k, y + 3 * k), 2 * k)  # eye ball
    dr.circle(screen, WHITE, (x + 22 * k, y + 5 * k), 1 * k)  # blink


def draw_fish(x, y, k):
    """
    The function, which is used to draw the whole fish
    :param x: x coordinates of the fish
    :param y: y coordinates of the fish
    :param k: compression ratio
    :return:
    """
    fin1(x, y, k)
    fin2(x, y, k)
    fish_body(x, y, k)
    fish_tail(x, y, k)
    fish_eye(x, y, k)


def cat_paws(x, y, k):
    """
    The function, which is used to draw cat paws
    :param x: x coordinates of the cat
    :param y: y coordinates of the cat
    :param k: compression ratio
    :return: nothing
    """
    draw_ellipse_angle(screen, GREY, (x - 250 * k / 4, y + 20 * k, 100 * k, 20 * k), 12)
    draw_ellipse_angle(screen, GREY, (x - 210 * k / 4, y + 43 * k, 100 * k, 20 * k), 20)
    draw_ellipse_angle(screen, GREY, (x + 450 * k / 4, y + 43 * k, 100 * k, 20 * k), -40)
    draw_ellipse_angle(screen, GREY, (x + 670 * k / 4, y + 35 * k, 100 * k, 20 * k), -25)


def cat_ears(x, y, k):
    """
    The function, which is used to draw cat ears
    :param x: x coordinates of the cat
    :param y: y coordinates of the cat
    :param k: compression ratio
    :return: nothing
    """
    dr.polygon(screen, GREY,
               ((x + 110 * k / 4, y - 30 * k), (x + 200 * k / 4, y - 50 * k), (x + 220 * k / 4, y - 20 * k)))
    dr.polygon(screen, GREY,
               ((x + 20 * k / 4, y - 30 * k), (x + 10 * k / 4, y - 50 * k), (x + 130 * k / 4, y - 20 * k)))


def cat_tusk(x, y, k):
    """
    The function, which is used to draw cat tusks
    :param x: x coordinates of the cat
    :param y: y coordinates of the cat
    :param k: compression ratio
    :return: nothing
    """
    dr.polygon(screen, WHITE,
               ((x + 50 * k / 4, y - 5 * k), (x + 75 * k / 4, y + 17 * k), (x + 90 * k / 4, y - 5 * k)))
    dr.polygon(screen, WHITE,
               ((x - 10 * k / 4, y - 10 * k), (x + 15 * k / 4, y + 12 * k), (x + 30 * k / 4, y - 10 * k)))


def cat_eyes(x, y, k):
    """
    The function, which is used to draw cat eyes
    :param x: x coordinates of the cat
    :param y: y coordinates of the cat
    :param k: compression ratio
    :return: nothing
    """
    dr.ellipse(screen, WHITE, (x - 10 * k / 4, y - 30 * k, 21 * k, 14 * k))  # eye 1
    dr.circle(screen, BLACK, (x + 53 * k / 4, y - 23 * k), k * 5)

    dr.ellipse(screen, WHITE, (x + 100 * k / 4, y - 25 * k, 21 * k, 14 * k))  # eye 2
    dr.circle(screen, BLACK, (x + 165 * k / 4, y - 18 * k), k * 5)


def cat_head(x, y, k):
    """
    The function, which is used to draw cat head
    :param x: x coordinates of the cat
    :param y: y coordinates of the cat
    :param k: compression ratio
    :return: nothing
    """
    dr.ellipse(screen, GREY, (x - 38 * k / 4, y - 40 * k, 70 * k, 50 * k))  # head itself
    cat_ears(x, y, k)
    cat_tusk(x, y, k)
    cat_eyes(x, y, k)
    dr.circle(screen, BLACK, (x + 40 * k / 4, y - 6 * k), 3)  # cat's nose


def draw_cat(x, y, k):
    dr.ellipse(screen, GREY, (x, y, 200 * k, 50 * k))  # cat's body
    cat_paws(x, y, k)
    draw_fish(x - 45 * k, y - 10 * k, 1)  # fish
    draw_ellipse_angle(screen, GREY, (x + 660 * k / 4, y - 32 * k, 130 * k, 30 * k), 30)  # cat's tail
    cat_head(x, y, k)


def chuckcha_base(x, y, k, bgcolor):
    """
    The function, which is used to draw the base of chuckcha
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :param bgcolor: background color
    :return: nothing
    """
    dr.ellipse(screen, AREAL, (x - 10 * k, y - 90 * k, 220 * k, 150 * k))  # areal 1
    dr.ellipse(screen, (138, 124, 101), (x + 10 * k, y - 70 * k, 180 * k, 120 * k))  # areal 2
    dr.ellipse(screen, BROWN, (x, y, 200 * k, 350 * k))  # body
    dr.rect(screen, bgcolor, (x, y + 175 * k, 200 * k, 200 * k))  # hide


def chuckcha_legs(x, y, k):
    """
    The function, which is used to draw chuckcha legs
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :return: nothing
    """
    dr.ellipse(screen, BROWN, (x, y + 230 * k, 80 * k, 40 * k))  # leg 1
    dr.ellipse(screen, BROWN, (x + 20 * k, y + 150 * k, 60 * k, 100 * k))

    dr.ellipse(screen, BROWN, (x + 120 * k, y + 230 * k, 80 * k, 40 * k))  # leg 2
    dr.ellipse(screen, BROWN, (x + 120 * k, y + 150 * k, 60 * k, 100 * k))


def chuckcha_arms(x, y, k, lefthanded):
    """
    The function, which is used to draw chuckcha arms
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :param lefthanded: used to define whether chuckcha is lefthanded or righthanded
    :return: nothing
    """
    if not lefthanded:
        dr.ellipse(screen, BROWN, (x - 60 * k, y + 60 * k, 150 * k, 45 * k))  # hand 1
        draw_ellipse_angle(screen, BROWN, (x + 130 * k, y + 75 * k, 150 * k, 45 * k), -30)  # hand 2
        dr.line(screen, BLACK, (x - 55 * k, y + 230 * k), (x - 55 * k, y - 60 * k), width=2)  # stick
    else:
        dr.ellipse(screen, BROWN, (x + 110 * k, y + 60 * k, 150 * k, 45 * k))  # hand 1
        draw_ellipse_angle(screen, BROWN, (x - 80 * k, y + 75 * k, 150 * k, 45 * k), 210)  # hand 2
        dr.line(screen, BLACK, (x + 230 * k, y + 230 * k), (x + 230 * k, y - 60 * k), width=2)  # stick


def chuckcha_clothes(x, y, k):
    """
    The function, which is used to draw chuckcha clothes
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :return: nothing
    """
    dr.rect(screen, DARK_BROWN, (x + 70 * k, y + 20 * k, 55 * k, 152 * k))  # clothes vertical
    dr.rect(screen, DARK_BROWN, (x, y + 175 * k, 200 * k, 30 * k))  # clothes horizontal


def chuckcha_head(x, y, k):
    """
    The function, which is used to draw the chuckcha head
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :return: nothing
    """
    dr.ellipse(screen, LIGHT_BROWN, (x + 25 * k, y - 55 * k, 150 * k, 90 * k))  # head
    dr.arc(screen, BLACK, (x + 23 * k, y + 1 * k, 150 * k, 90 * k), 3 * pi / 10, 7 * pi / 10, width=2)  # mouth
    dr.line(screen, BLACK, (x + 50 * k, y - 30 * k), (x + 80 * k, y - 20 * k), width=2)  # eye 1
    dr.line(screen, BLACK, (x + 150 * k, y - 30 * k), (x + 120 * k, y - 20 * k), width=2)  # eye 2


def draw_chuckcha(x, y, k, bgcolor, lefthanded):
    """
    The function, which is used to draw the chuckcha
    :param x: x coordinates of chukcha
    :param y: y ccordinates of chukcha
    :param k: compression ratio
    :param bgcolor: background color
    :param lefthanded: used to define whether chuckcha is lefthanded or righthanded
    :return: nothing
    """
    chuckcha_base(x, y, k, bgcolor)
    chuckcha_legs(x, y, k)
    chuckcha_arms(x, y, k, lefthanded)
    chuckcha_clothes(x, y, k)
    chuckcha_head(x, y, k)


chum_par = [[75, 505, 70, 3], [470, 525, 70, 3], [250, 550, 200, 3], [150, 605, 100, 3], [300, 655, 100, 3]]
for element in chum_par:
    draw_chum(element[0], element[1], element[2], element[3])

chuckcha_par = [[640, 460, 0.2, WHITE, False], [720, 480, 0.2, WHITE, False], [658, 510, 0.2, WHITE, False],
                [710, 550, 0.2, WHITE, False], [630, 550, 0.2, WHITE, True], [530, 545, 0.2, ALMOST_BLACK, True],
                [500, 630, 0.2, ALMOST_BLACK, True], [600, 670, 0.7, WHITE, False]]

for element in chuckcha_par:
    draw_chuckcha(element[0], element[1], element[2], element[3], element[4])

cat_par = [[200, 750, 0.6], [-100, 790, 0.6], [120, 900, 0.6], [700, 900, 0.6], [500, 970, 0.6]]

for element in cat_par:
    draw_cat(element[0], element[1], element[2])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()