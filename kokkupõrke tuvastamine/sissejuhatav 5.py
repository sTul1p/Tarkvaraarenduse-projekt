import pygame
import random

pygame.init()

# Värvid
lBlue = [153, 204, 255]
black = [0, 0, 0]
red = [255, 0, 0]

# Ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Kokkupõrke tuvastamine")

clock = pygame.time.Clock()

# Mängija suurus ja algpositsioon
PLAYER_W, PLAYER_H = 80, 120
posX, posY = 0, 0
speedX, speedY = 3, 4

# Lae pildid ja eemalda must taust
playerImage = pygame.image.load("mängija-ilma-taustata.png").convert()
playerImage.set_colorkey((0, 0, 0))
playerImage = pygame.transform.scale(playerImage, (PLAYER_W, PLAYER_H))

ENEMY_W, ENEMY_H = 70, 100
enemyImage = pygame.image.load("vastane-ilma-taustata.png").convert()
enemyImage.set_colorkey((0, 0, 0))
enemyImageScaled = pygame.transform.scale(enemyImage, (ENEMY_W, ENEMY_H))

# Vaenlased - 5 juhuslikku
enemies = []
for i in range(5):
    x = random.randint(0, screenX - ENEMY_W)
    y = random.randint(0, screenY - ENEMY_H)
    enemies.append(pygame.Rect(x, y, ENEMY_W, ENEMY_H))

# Skoor
score = 0
totalEnemies = 20
enemyCounter = len(enemies)

font = pygame.font.SysFont("Arial", 24)
bigFont = pygame.font.SysFont("Arial", 48)

gameover = False

while not gameover:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

    screen.fill(lBlue)

    # Liikumine
    posX += speedX
    posY += speedY

    if posX > screenX - PLAYER_W or posX < 0:
        speedX = -speedX
    if posY > screenY - PLAYER_H or posY < 0:
        speedY = -speedY

    player = pygame.Rect(posX, posY, PLAYER_W, PLAYER_H)

    # Joonista vaenlased
    for enemy in enemies:
        screen.blit(enemyImageScaled, enemy)

    # Kokkupõrke tuvastamine
    hit_enemies = [e for e in enemies if player.colliderect(e)]
    for enemy in hit_enemies:
        enemies.remove(enemy)
        score += 1
        if enemyCounter < totalEnemies:
            x = random.randint(0, screenX - ENEMY_W)
            y = random.randint(0, screenY - ENEMY_H)
            enemies.append(pygame.Rect(x, y, ENEMY_W, ENEMY_H))
            enemyCounter += 1

    # Joonista mängija
    screen.blit(playerImage, player)

    # Skoor
    screen.blit(font.render(f"Skoor: {score}", True, black), (10, 10))
    screen.blit(font.render(f"Vaenlasi: {len(enemies)}", True, black), (10, 40))

    if score >= totalEnemies:
        gameover = True

    pygame.display.flip()

# Lõppekraan
screen.fill(lBlue)
msg = bigFont.render("Mäng läbi!", True, red)
scoreFinal = font.render(f"Lõppskoor: {score}", True, black)
screen.blit(msg, (screenX // 2 - msg.get_width() // 2, screenY // 2 - 50))
screen.blit(scoreFinal, (screenX // 2 - scoreFinal.get_width() // 2, screenY // 2 + 20))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()