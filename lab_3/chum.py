import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((700, 1000))
# лед
dr.rect(screen, 0xFFFFFF, (0, 450, 700, 550))
# небо
dr.rect(screen, (214, 214, 214), (0, 0, 700, 450))
# чум
dr.circle(screen, (214, 214, 214), (200, 550), 160)
dr.circle(screen, (0, 0, 0), (200, 550), 160, 3)
dr.line(screen, (0, 0, 0), (200, 550), (520, 550), 3)
# тропинка
dr.rect(screen, (250, 250, 250), (0, 550, 500, 200))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
