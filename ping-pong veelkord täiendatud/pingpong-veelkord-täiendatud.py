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
TAEVAS     = (135, 206, 235)
PRUUN      = (139, 69, 19)
HELEPRUUN  = (160, 82, 45)
ORANŽ      = (255, 140, 0)
TUMEORANŽ  = (204, 85, 0)
MUST       = (0, 0, 0)
PUNANE     = (200, 0, 0)
VALGE      = (255, 255, 255)

font     = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
clock    = pygame.time.Clock()


#Helilaadur
def laadi_heli(failinimi):
    """Otsib helifaili skripti kaustast ja töökataloogist.
    Tagastab pygame.Sound objekti või None, kui faili ei leita."""
    if not mixer_ok:
        return None
    script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    cwd        = os.path.abspath(os.getcwd())
    for kaust in (script_dir, cwd):
        tee = os.path.join(kaust, failinimi)
        if os.path.exists(tee):
            try:
                return pygame.mixer.Sound(tee)
            except pygame.error:
                pass
    return None

# Helid – kui faili ei leita, on väärtus None (mäng töötab heli puudumiseta)
heli_paddle   = laadi_heli("paddle_hit.mp3")   # Lühike "plink" padi põrkel
heli_gameover = laadi_heli("gameover.mp3")     # Laskuv "thud" mängu lõppedes


# Taustamuusika

def laadi_muusika():
    """Otsib background.mp3 ja käivitab selle lõpmatult.
    Tagastab True edu korral."""
    if not mixer_ok:
        return False
    script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    cwd        = os.path.abspath(os.getcwd())
    for kaust in (script_dir, cwd):
        tee = os.path.join(kaust, "background.mp3")
        if os.path.exists(tee):
            try:
                pygame.mixer.music.load(tee)
                pygame.mixer.music.play(-1)   # -1 = korda lõputult
                return True
            except pygame.error:
                continue
    return False

muusika_ok = laadi_muusika()


#Mängu muutujad

ball              = pygame.Rect(W - 30, 30, 20, 20)
ball_dx, ball_dy  = 4 * random.choice([-1, 1]), 4

pad       = pygame.Rect(260, 420, 120, 20)
PAD_SPEED = 6

score     = 0
game_over = False


#Joonistusfunktsioonid

def draw():
    screen.fill(TAEVAS)

    # Skoor vasakus ülanurgas
    screen.blit(font.render(f"Skoor: {score}", True, MUST), (10, 10))

    # Juhend paremas ülanurgas
    juhend = font.render("<- -> nooled: liiguta alust", True, MUST)
    screen.blit(juhend, (W - juhend.get_width() - 10, 10))

    # Alus (pruun + heledam triip)
    pygame.draw.rect(screen, PRUUN, pad)
    pygame.draw.rect(screen, HELEPRUUN,
                     (pad.x + 5, pad.y + 4, pad.width - 10, 6))

    # Pall (oranž ring, tume ääris)
    pygame.draw.circle(screen, ORANŽ,      ball.center, 10)
    pygame.draw.circle(screen, TUMEORANŽ,  ball.center, 10, 2)

    pygame.display.flip()


def draw_game_over():
    screen.fill(TAEVAS)

    # "Mäng läbi" pealkiri
    yl = big_font.render("MÄNG LÄBI!", True, PUNANE)
    screen.blit(yl, (W // 2 - yl.get_width() // 2, H // 2 - 80))

    # Lõplik skoor
    sk = font.render(f"Lõplik skoor: {score}", True, MUST)
    screen.blit(sk, (W // 2 - sk.get_width() // 2, H // 2))

    # Valikud
    uuesti = font.render("Vajuta R – mängi uuesti   |   ESC – välju", True, MUST)
    screen.blit(uuesti, (W // 2 - uuesti.get_width() // 2, H // 2 + 60))

    pygame.display.flip()


#Mängu lähtestamine

def reset_game():
    """Lähtestab kõik mängumuutujad algsesse seisu ja taaskäivitab muusika."""
    global ball, ball_dx, ball_dy, score, game_over
    ball     = pygame.Rect(W - 30, 30, 20, 20)
    ball_dx  = 4 * random.choice([-1, 1])
    ball_dy  = 4
    pad.x    = 260
    score    = 0
    game_over = False
    if mixer_ok:
        laadi_muusika()


#Peamängusündmuste tsükkel

running = True
while running:
    clock.tick(60)

    # Sündmuste töötlemine
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

    # Aluse juhtimine nooleklahvidega
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pad.x -= PAD_SPEED
    if keys[pygame.K_RIGHT]:
        pad.x += PAD_SPEED

    # Alus ei lähe ekraanist välja
    pad.left  = max(pad.left, 0)
    pad.right = min(pad.right, W)

    # Palli liigutamine
    ball.x += ball_dx
    ball.y += ball_dy

    # Põrkumine vasakult/paremalt seinalt
    if ball.left <= 0 or ball.right >= W:
        ball_dx *= -1

    # Põrkumine ülemisest seinast
    if ball.top <= 0:
        ball_dy *= -1

    # Kokkupõrge padiga – ainult alla liikuval pallil
    if ball_dy > 0 and ball.colliderect(pad):
        ball_dy *= -1
        score   += 1
        # Padi põrke heli
        if heli_paddle:
            heli_paddle.play()

    # Pall kukkus alla: mäng lõpeb
    if ball.top > H:
        game_over = True
        if mixer_ok:
            pygame.mixer.music.stop()
        # Mängu lõpu heli
        if heli_gameover:
            heli_gameover.play()

    draw()

pygame.quit()
sys.exit()
