import pygame
import sys
import random

pygame.init()

# Ekraani seaded
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Hiir")
clock = pygame.time.Clock()

# Värvid
TAUST      = (173, 216, 230)   # Hele sinine taust
RING_VÄRV  = (0, 0, 139)       # Tumesinine ring (ääris)
BOONUS     = (220, 20, 60)     # Punane boonusring

MUST = (0, 0, 0)         # Teksti värv

#Mängu konstandid
ALGRAADIUS   = 10    # Iga uue ringi algne raadius pikslites
KASV         = 5     # Mitu pikslit kasvab iga olemasolev ring kliki järel
MAX_RINGID   = 10    # Maksimaalselt nii palju ringi korraga ekraanil

# Boonuse tõenäosus iga kliki puhul (0.0–1.0)
BOONUS_TÕENÄOSUS = 0.2

font = pygame.font.SysFont("Arial", 18)

# Ringide nimekiri
# Iga ring on sõnastik: {x, y, raadius, on_boonus}
ringid = []

#Põhitsükkel
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1) Kasvatame kõiki olemasolevaid ringe
            for r in ringid:
                r["raadius"] += KASV

            # 2) Otsustame, kas uus ring on boonus
            on_boonus = random.random() < BOONUS_TÕENÄOSUS

            # 3) Lisame uue ringi klikitud koordinaatidele
            mx, my = event.pos
            ringid.append({
                "x":        mx,
                "y":        my,
                "raadius":  ALGRAADIUS,
                "on_boonus": on_boonus,
            })

            # 4) Kui ringe on üle maksimumi, kustutame vanemaid eest
            while len(ringid) > MAX_RINGID:
                ringid.pop(0)

    # Joonistamine
    screen.fill(TAUST)

    for r in ringid:
        värv = BOONUS if r["on_boonus"] else RING_VÄRV
        pygame.draw.circle(screen, värv, (r["x"], r["y"]), r["raadius"], 2)

    juhis = font.render("Kliki ekraanile, et ringid tekiksid", True, MUST)
    screen.blit(juhis, (8, 8))

    loendur = font.render(f"Renge ekraanil: {len(ringid)} / {MAX_RINGID}", True, MUST)
    screen.blit(loendur, (W - loendur.get_width() - 8, 8))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()