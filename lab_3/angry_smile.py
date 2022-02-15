import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))
screen.fill((162, 184, 147))
dr.circle(screen, 0xFFFF00, (400, 400), 400)
dr.rect(screen, 0x000000, (150, 500, 500, 100))
dr.circle(screen, 0xFF0000, (230, 250), 80)
dr.circle(screen, 0x000000, (230, 250), 30)

dr.circle(screen, 0xFF0000, (570, 250), 60)
dr.circle(screen, 0x000000, (570, 250), 30)

dr.polygon(screen, 0x000000, ((230, 170), (50, 50), (70, 30), (260, 120)))
dr.polygon(screen, 0x000000, ((570, 190), (730, 50), (710, 30), (550, 120)))
#pygame.transform.rotate(screen, )
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()