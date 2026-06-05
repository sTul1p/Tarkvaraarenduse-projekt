import pygame
import sys
import random
import os

pygame.init()
try:
    pygame.mixer.init()
    mixer_ok = True
except pygame.error:
    mixer_ok = False

# Ekraani seaded
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("PingPong")

# Värvid
TAEVAS = (135, 206, 235)
PRUUN = (139, 69, 19)
HELEPRUUN = (160, 82, 45)
ORANŽ = (255, 140, 0)
TUMEORANŽ = (204, 85, 0)
MUST = (0, 0, 0)
PUNANE = (200, 0, 0)
VALGE = (255, 255, 255)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
clock = pygame.time.Clock()

# Taustamuusika laadimine
if mixer_ok:
    try:
        music_file = os.path.join(os.path.dirname(__file__), "background.wav")
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 = korda lõputult
    except pygame.error:
        mixer_ok = False

# Mängu muutujad
ball = pygame.Rect(W - 30, 30, 20, 20)
ball_dx, ball_dy = 4 * random.choice([-1, 1]), 4

pad = pygame.Rect(260, 420, 120, 20)
PAD_SPEED = 6

score = 0
game_over = False

def draw():
    screen.fill(TAEVAS)

    # Skoor ülemises nurgas
    tekst = font.render(f"Skoor: {score}", True, MUST)
    screen.blit(tekst, (10, 10))

    # Juhend
    juhend = font.render("<- -> nooled: liiguta alust", True, MUST)
    screen.blit(juhend, (W - juhend.get_width() - 10, 10))

    # Alus
    pygame.draw.rect(screen, PRUUN, pad)
    pygame.draw.rect(screen, HELEPRUUN, (pad.x + 5, pad.y + 4, pad.width - 10, 6))

    # Pall
    pygame.draw.circle(screen, ORANŽ, ball.center, 10)
    pygame.draw.circle(screen, TUMEORANŽ, ball.center, 10, 2)

    pygame.display.flip()

def draw_game_over():
    screen.fill(TAEVAS)

    # "Mäng läbi" tekst
    yl_tekst = big_font.render("MÄNG LÄBI!", True, PUNANE)
    screen.blit(yl_tekst, (W // 2 - yl_tekst.get_width() // 2, H // 2 - 80))

    # Lõplik skoor
    skoor_tekst = font.render(f"Lõplik skoor: {score}", True, MUST)
    screen.blit(skoor_tekst, (W // 2 - skoor_tekst.get_width() // 2, H // 2))

    # Uuesti mängimise juhend
    uuesti = font.render("Vajuta R – mängi uuesti   |   ESC – välju", True, MUST)
    screen.blit(uuesti, (W // 2 - uuesti.get_width() // 2, H // 2 + 60))

    pygame.display.flip()

def reset_game():
    global ball, ball_dx, ball_dy, score, game_over
    ball = pygame.Rect(W - 30, 30, 20, 20)
    ball_dx = 4 * random.choice([-1, 1])
    ball_dy = 4
    pad.x = 260
    score = 0
    game_over = False
    if mixer_ok:
        pygame.mixer.music.play(-1)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if game_over:
        draw_game_over()
        continue

    # Klaviatuuri sisend – aluse juhtimine x-suunal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pad.x -= PAD_SPEED
    if keys[pygame.K_RIGHT]:
        pad.x += PAD_SPEED

    # Alus ei lähe mängu piiridest välja
    if pad.left < 0:
        pad.left = 0
    if pad.right > W:
        pad.right = W

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
        score += 1

    # Pall kukkus alla – mäng lõpetatakse
    if ball.top > H:
        game_over = True
        if mixer_ok:
            pygame.mixer.music.stop()

    draw()

pygame.quit()
sys.exit()