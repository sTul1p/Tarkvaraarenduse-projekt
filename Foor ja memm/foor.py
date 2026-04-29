import pygame

pygame.init()

screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption("Foor - Sander Tulp")

must = (0, 0, 0)
hall = (50, 50, 50)
punane = (255, 0, 0)
kollane = (255, 220, 0)
roheline = (0, 200, 0)
valge = (255, 255, 255)

screen.fill(must)

pygame.draw.rect(screen, hall, [100, 10, 100, 280])
pygame.draw.rect(screen, valge, [100, 10, 100, 280], 2)

pygame.draw.circle(screen, punane, [150, 55], 35)
pygame.draw.circle(screen, kollane, [150, 150], 35)
pygame.draw.circle(screen, roheline, [150, 245], 35)

pygame.display.flip()

jookseb = True
while jookseb:
    for sonnum in pygame.event.get():
        if sonnum.type == pygame.QUIT:
            jookseb = False

pygame.quit()