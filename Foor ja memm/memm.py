import pygame

pygame.init()

screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption("Lumemees - Sander Tulp")

# Värvid
must = (0, 0, 0)
valge = (255, 255, 255)
punane = (255, 0, 0)
oranz = (255, 140, 0)

screen.fill(must)

# Keha (alumine ring) - suur
pygame.draw.circle(screen, valge, [150, 220], 60)

# Keha (keskmine ring)
pygame.draw.circle(screen, valge, [150, 135], 40)

# Pea (ülemine ring) - väike
pygame.draw.circle(screen, valge, [150, 65], 28)

# Silmad
pygame.draw.circle(screen, must, [141, 58], 4)
pygame.draw.circle(screen, must, [159, 58], 4)

# Nina (kolmnurk - oranž)
pygame.draw.polygon(screen, oranz, [[150, 65], [165, 70], [150, 75]])

# Suu (punktid)
pygame.draw.circle(screen, must, [140, 78], 3)
pygame.draw.circle(screen, must, [150, 82], 3)
pygame.draw.circle(screen, must, [160, 78], 3)

# Nupud kehal
pygame.draw.circle(screen, must, [150, 120], 4)
pygame.draw.circle(screen, must, [150, 135], 4)
pygame.draw.circle(screen, must, [150, 150], 4)

pygame.display.flip()

# Akna avatud hoidmine
jookseb = True
while jookseb:
    for sonnum in pygame.event.get():
        if sonnum.type == pygame.QUIT:
            jookseb = False

pygame.quit()