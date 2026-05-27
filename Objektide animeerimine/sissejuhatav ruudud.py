import pygame, sys, random
pygame.init()

#värvid
red = [255, 34, 34]
lBlue = [158, 207, 238]

#ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Animeerimine")
screen.fill(lBlue)
clock = pygame.time.Clock()

#koordinaatide ja kiiruste loomine
coords = []
for i in range(10):
    posX = random.randint(0, screenX)
    posY = random.randint(0, screenY)
    speed = random.randint(1, 5)
    coords.append([posX, posY, speed])

gameover = False
while not gameover:
    clock.tick(60)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    for i in range(len(coords)):
        pygame.draw.rect(screen, red, [coords[i][0], coords[i][1], 20, 20])
        coords[i][1] += coords[i][2]

        #kui jõuab alla, alustab uuesti ülevalt
        if coords[i][1] > screenY:
            coords[i][1] = random.randint(-40, -10)
            coords[i][0] = random.randint(0, screenX)

    pygame.display.flip()
    screen.fill(lBlue)

pygame.quit()