from math import sqrt, pi, cos, sin

import pygame
import pygame.draw as dr

pygame.init()

white = (250, 250, 250)
grey = (214, 214, 214)
white_grey = (100, 100, 100)
areal = (170, 170, 160)
black = (0, 0, 0)
almost_black = (240, 240, 240)
brown = (168, 138, 98)
fish = (50, 168, 121)
blue = (27, 44, 150)
red = (196, 43, 87)
light_brown = (222, 207, 184)
dark_brown = (89, 69, 37)

FPS = 30
screen = pygame.display.set_mode((794, 1123))

# лед
dr.rect(screen, white, (0, 450, 794, 1123 / 2))
# небо
dr.rect(screen, grey, (0, 0, 794, 450))


def draw_chum(x, y, R, width):
    dr.circle(screen, grey, (x, y), R)

    dr.line(screen, black, (x - R, y), (x + R, y), width + 4)  # base
    dr.line(screen, black, (x - sqrt(15) / 4 * R, y - R / 4), (x + sqrt(15) / 4 * R, y - R / 4),
            width)  # 1 level
    dr.line(screen, black, (x - sqrt(3) / 2 * R, y - R / 2), (x + sqrt(3) / 2 * R, y - R / 2), width)  # 2 level
    dr.line(screen, black, (x - sqrt(7) / 4 * R, y - 3 * R / 4), (x + sqrt(7) / 4 * R, y - 3 * R / 4), width)  # 3 level
    dr.circle(screen, black, (x, y), R, width)  # arc

    dr.line(screen, black, (x - 5 * R / 6, y), (x - 5 * R / 6, y - R / 4), width)  # 1 level vertical elements
    dr.line(screen, black, (x + 5 * R / 6, y), (x + 5 * R / 6, y - R / 4), width)
    dr.line(screen, black, (x - 5 * R / 12, y), (x - 5 * R / 12, y - R / 4), width)
    dr.line(screen, black, (x + 5 * R / 12, y), (x + 5 * R / 12, y - R / 4), width)
    dr.line(screen, black, (x, y), (x, y - R / 4), width)  # middle

    dr.line(screen, black, (x - 5 * R / 24, y - R / 4), (x - 5 * R / 24, y - R / 2), width)  # 2 level vertical elements
    dr.line(screen, black, (x + 5 * R / 24, y - R / 4), (x + 5 * R / 24, y - R / 2), width)
    dr.line(screen, black, (x - 15 * R / 24, y - R / 4), (x - 15 * R / 24, y - R / 2), width)
    dr.line(screen, black, (x + 15 * R / 24, y - R / 4), (x + 15 * R / 24, y - R / 2), width)

    dr.line(screen, black, (x, y - R / 2), (x, y - 3 * R / 4), width)  # 3 level vertical elements
    dr.line(screen, black, (x - 10 / 24 * R, y - R / 2), (x - 10 / 24 * R, y - 3 * R / 4), width)
    dr.line(screen, black, (x + 10 / 24 * R, y - R / 2), (x + 10 / 24 * R, y - 3 * R / 4), width)

    dr.line(screen, black, (x, y - 3 * R / 4), (x, y - R), width)  # 4 level vertical element

    dr.rect(screen, almost_black, (x - 5 * R / 3, y, 10 * R / 3, 4 * R / 3))  # hide


def draw_rect_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


def draw_ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    dr.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


def draw_fish(x, y, k):
    dr.polygon(screen, red, ((x + 25 * k, y + 10 * k), (x + 20 * k, y + 26 * k), (x + 35 * k, y + 40 * k)))  # fin 1
    dr.polygon(screen, black, ((x + 25 * k, y + 10 * k), (x + 20 * k, y + 26 * k), (x + 35 * k, y + 40 * k)), width=3)

    dr.polygon(screen, red, ((x + 25 * k, y - 15 * k), (x + 45 * k, y - 15 * k), (x + 35 * k, y + 10 * k)))  # fin 2
    dr.polygon(screen, black, ((x + 25 * k, y - 15 * k), (x + 45 * k, y - 15 * k), (x + 35 * k, y + 10 * k)), width=3)

    draw_ellipse_angle(screen, fish, (x, y, 70 * k, 25 * k), -30)  # body
    draw_ellipse_angle(screen, black, (x, y, 70 * k, 25 * k), -30, width=3)

    dr.polygon(screen, fish, (  # tail
        (x + 70 * k / 2 + 70 * k / 2 * cos(pi / 6), y + 35 * k - sin(pi / 6) * 25 * k / 2),
        (x + 30 * k / 2 + 70 * k * cos(pi / 6), y + 80 * k / 2 + sin(pi / 6) * 25 * k),
        (x + 60 * k / 2 + 70 * k * cos(pi / 6), y + 30 * k / 2 + sin(pi / 6) * 25 * k)))

    dr.polygon(screen, black, (
        (x + 70 * k / 2 + 70 * k / 2 * cos(pi / 6), y + 35 * k - sin(pi / 6) * 25 * k / 2),
        (x + 30 * k / 2 + 70 * k * cos(pi / 6), y + 80 * k / 2 + sin(pi / 6) * 25 * k),
        (x + 60 * k / 2 + 70 * k * cos(pi / 6), y + 30 * k / 2 + sin(pi / 6) * 25 * k)), width=3)

    dr.circle(screen, blue, (x + 20 * k, y + 3 * k), 6 * k)  # eye
    dr.circle(screen, black, (x + 20 * k, y + 3 * k), 2 * k)  # eye ball
    dr.circle(screen, white, (x + 22 * k, y + 5 * k), 1 * k)


def draw_cat(x, y, k):
    dr.ellipse(screen, grey, (x, y, 200 * k, 50 * k))  # body

    draw_ellipse_angle(screen, grey, (x - 250 * k / 4, y + 20 * k, 100 * k, 20 * k), 12)  # paws
    draw_ellipse_angle(screen, grey, (x - 210 * k / 4, y + 43 * k, 100 * k, 20 * k), 20)
    draw_ellipse_angle(screen, grey, (x + 450 * k / 4, y + 43 * k, 100 * k, 20 * k), -40)
    draw_ellipse_angle(screen, grey, (x + 670 * k / 4, y + 35 * k, 100 * k, 20 * k), -25)

    draw_fish(x - 45 * k, y - 10 * k, 1)  # fish

    draw_ellipse_angle(screen, grey, (x + 660 * k / 4, y - 32 * k, 130 * k, 30 * k), 30)  # tail

    dr.polygon(screen, grey,  # ear 1
               ((x + 110 * k / 4, y - 30 * k), (x + 200 * k / 4, y - 50 * k), (x + 220 * k / 4, y - 20 * k)))

    dr.polygon(screen, grey,  # ear 2
               ((x + 20 * k / 4, y - 30 * k), (x + 10 * k / 4, y - 50 * k), (x + 130 * k / 4, y - 20 * k)))

    dr.polygon(screen, white,  # tusk 1
               ((x + 50 * k / 4, y - 5 * k), (x + 75 * k / 4, y + 17 * k), (x + 90 * k / 4, y - 5 * k)))

    dr.polygon(screen, white,  # tusk 2
               ((x - 10 * k / 4, y - 10 * k), (x + 15 * k / 4, y + 12 * k), (x + 30 * k / 4, y - 10 * k)))

    dr.ellipse(screen, grey, (x - 38 * k / 4, y - 40 * k, 70 * k, 50 * k))  # head

    dr.ellipse(screen, white, (x - 10 * k / 4, y - 30 * k, 21 * k, 14 * k))  # eye 1
    dr.circle(screen, black, (x + 53 * k / 4, y - 23 * k), k * 5)

    dr.ellipse(screen, white, (x + 100 * k / 4, y - 25 * k, 21 * k, 14 * k))  # eye 2
    dr.circle(screen, black, (x + 165 * k / 4, y - 18 * k), k * 5)

    dr.circle(screen, black, (x + 40 * k / 4, y - 6 * k), 3)  # nose


def draw_chuckcha(x, y, k, bgcolor, lefthanded):
    dr.ellipse(screen, areal, (x - 10 * k, y - 90 * k, 220 * k, 150 * k))  # areal 1
    dr.ellipse(screen, (138, 124, 101), (x + 10 * k, y - 70 * k, 180 * k, 120 * k))  # areal 2
    dr.ellipse(screen, brown, (x, y, 200 * k, 350 * k))  # body
    dr.rect(screen, bgcolor, (x, y + 175 * k, 200 * k, 200 * k))  # hide

    dr.ellipse(screen, brown, (x, y + 230 * k, 80 * k, 40 * k))  # leg 1
    dr.ellipse(screen, brown, (x + 20 * k, y + 150 * k, 60 * k, 100 * k))

    dr.ellipse(screen, brown, (x + 120 * k, y + 230 * k, 80 * k, 40 * k))  # leg 2
    dr.ellipse(screen, brown, (x + 120 * k, y + 150 * k, 60 * k, 100 * k))
    if not lefthanded:
        dr.ellipse(screen, brown, (x - 60 * k, y + 60 * k, 150 * k, 45 * k))  # hand 1
        draw_ellipse_angle(screen, brown, (x + 130 * k, y + 75 * k, 150 * k, 45 * k), -30)  # hand 2
        dr.line(screen, black, (x - 55 * k, y + 230 * k), (x - 55 * k, y - 60 * k), width=2)  # stick
    else:
        dr.ellipse(screen, brown, (x + 110 * k, y + 60 * k, 150 * k, 45 * k))  # hand 1
        draw_ellipse_angle(screen, brown, (x - 80 * k, y + 75 * k, 150 * k, 45 * k), 210)  # hand 2
        dr.line(screen, black, (x + 230 * k, y + 230 * k), (x + 230 * k, y - 60 * k), width=2)  # stick

    dr.rect(screen, dark_brown, (x + 70 * k, y + 20 * k, 55 * k, 152 * k))  # clothes vertical
    dr.rect(screen, dark_brown, (x, y + 175 * k, 200 * k, 30 * k))  # clothes horizontal

    dr.ellipse(screen, light_brown, (x + 25 * k, y - 55 * k, 150 * k, 90 * k))  # head
    dr.arc(screen, black, (x + 23 * k, y + 1 * k, 150 * k, 90 * k), 3 * pi / 10, 7 * pi / 10, width=2)  # mouth

    dr.line(screen, black, (x + 50 * k, y - 30 * k), (x + 80 * k, y - 20 * k), width=2)  # eye 1
    dr.line(screen, black, (x + 150 * k, y - 30 * k), (x + 120 * k, y - 20 * k), width=2)  # eye 2



draw_chum(75, 505, 70, 3)
draw_chum(470, 525, 70, 3)
draw_chum(250, 550, 200, 3)
draw_chum(150, 605, 100, 3)
draw_chum(300, 655, 100, 3)

draw_chuckcha(640, 460, 0.2, white, False)
draw_chuckcha(720, 480, 0.2, white, False)
draw_chuckcha(658, 510, 0.2, white, False)
draw_chuckcha(710, 550, 0.2, white, False)
draw_chuckcha(630, 550, 0.2, white, True)
draw_chuckcha(530, 545, 0.2, almost_black, True)
draw_chuckcha(500, 630, 0.2, almost_black, True)
draw_chuckcha(600, 670, 0.7, white, False)

draw_cat(200, 750, 0.6)
draw_cat(-100, 790, 0.6)
draw_cat(120, 900, 0.6)
draw_cat(700, 900, 0.6)
draw_cat(500, 970, 0.6)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
