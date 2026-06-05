import pygame
import sys
import random

pygame.init()

W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("PingPong")

TAEVAS = (135, 206, 235)
PRUUN = (139, 69, 19)
HELEPRUUN = (160, 82, 45)
ORANŽ = (255, 140, 0)
TUMEORANŽ = (204, 85, 0)
MUST = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

ball = pygame.Rect(W - 30, 30, 20, 20)
ball_dx, ball_dy = 4 * random.choice([-1, 1]), 4

pad = pygame.Rect(260, 320, 120, 20)
pad_dx = 3

score = 0

def draw():
    screen.fill(TAEVAS)
    tekst = font.render(f"Skoor: {score}", True, MUST)
    screen.blit(tekst, (10, 10))
    pygame.draw.rect(screen, PRUUN, pad)
    pygame.draw.rect(screen, HELEPRUUN, (pad.x + 5, pad.y + 4, pad.width - 10, 6))
    pygame.draw.circle(screen, ORANŽ, ball.center, 10)
    pygame.draw.circle(screen, TUMEORANŽ, ball.center, 10, 2)
    pygame.display.flip()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0:
        ball.left = 0
        ball_dx = abs(ball_dx)

    if ball.right >= W:
        ball.right = W
        ball_dx = -abs(ball_dx)

    if ball.top <= 0:
        ball.top = 0
        ball_dy = abs(ball_dy)

    # Alumine sein: -1 punkt ja põrkab tagasi
    if ball.bottom >= H:
        ball.bottom = H
        ball_dy = -abs(ball_dy)
        score -= 1

    # Kokkupõrge alusega: +1 punkt
    if ball.colliderect(pad):
        if ball_dy > 0:
            ball.bottom = pad.top
            ball_dy = -abs(ball_dy)
        elif ball_dy < 0:
            ball.top = pad.bottom
            ball_dy = abs(ball_dy)
        score += 1

    pad.x += pad_dx
    if pad.left < 0:
        pad.left = 0
        pad_dx = abs(pad_dx)
    elif pad.right > W:
        pad.right = W
        pad_dx = -abs(pad_dx)

    draw()

pygame.quit()
sys.exit()