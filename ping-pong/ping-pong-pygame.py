import pygame
import sys
import random

pygame.init()

# Ekraani seaded
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("PingPong")

# Värvid
TAEVAS = (135, 206, 235)
PRUUN = (139, 69, 19)
HELEPRUUN = (160, 82, 45)
ORANЗ = (255, 140, 0)
TUMEORANЗ = (204, 85, 0)
MUST = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Mängu muutujad
ball = pygame.Rect(310, 230, 20, 20)
ball_dx, ball_dy = 4 * random.choice([-1, 1]), 4

pad = pygame.Rect(260, 320, 120, 20)
pad_dx = 3

score = 0

def draw():
    screen.fill(TAEVAS)

    # Skoor ülemises nurgas
    tekst = font.render(f"Skoor: {score}", True, MUST)
    screen.blit(tekst, (10, 10))

    # Alus
    pygame.draw.rect(screen, PRUUN, pad)
    pygame.draw.rect(screen, HELEPRUUN, (pad.x + 5, pad.y + 4, pad.width - 10, 6))

    # Pall
    pygame.draw.circle(screen, ORANЗ, ball.center, 10)
    pygame.draw.circle(screen, TUMEORANЗ, ball.center, 10, 2)

    pygame.display.flip()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pall liigub
    ball.x += ball_dx
    ball.y += ball_dy

    # Põrkub vasakult/paremalt seinalt
    if ball.left <= 0 or ball.right >= W:
        ball_dx *= -1

    # Põrkub ülemisest seinast
    if ball.top <= 0:
        ball_dy *= -1

    # Kokkupõrge alusega (ainult kui pall langeb alla)
    if ball_dy > 0 and ball.colliderect(pad):
        ball_dy *= -1
        score += 1  # positiivne punkt

    # Pall kukkus alla
    if ball.top > H:
        score -= 1  # negatiivne punkt
        ball.center = (W // 2, 100)
        ball_dx = 4 * random.choice([-1, 1])
        ball_dy = 4

    # Alus liigub edasi-tagasi
    pad.x += pad_dx
    if pad.left <= 0 or pad.right >= W:
        pad_dx *= -1

    draw()

pygame.quit()
sys.exit()