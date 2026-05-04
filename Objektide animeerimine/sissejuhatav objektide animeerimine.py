import pygame, sys
pygame.init()

# Värvid
lBlue = [153, 204, 255]

# Ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Animeerimine")
screen.fill(lBlue)
clock = pygame.time.Clock()

# Graafika laadimine
ball = pygame.image.load("Soccer_ball.png")

# Kiirus ja asukoht
posX, posY = 0, 0
speedX, speedY = 3, 4

gameover = False
while not gameover:
    clock.tick(60)

    # Mängu sulgemine ristist
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    # Pildi lisamine ekraanile
    screen.blit(ball, (posX, posY))

    posX += speedX
    posY += speedY

    # Kui puudub ääri, siis muudab suunda
    if posX > screenX - ball.get_rect().width or posX < 0:
        speedX = -speedX

    if posY > screenY - ball.get_rect().height or posY < 0:
        speedY = -speedY

    pygame.display.flip()
    screen.fill(lBlue)

pygame.quit()