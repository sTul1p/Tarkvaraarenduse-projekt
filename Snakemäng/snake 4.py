import pygame
import sys

pygame.init()

# Ekraan
LAIUS = 640
KÕRGUS = 480
ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussi Mäng")

# Värvid
MUST = (0, 0, 0)
ROHELINE = (50, 205, 50)
ORANZ = (255, 140, 0)
PUNANE = (220, 20, 60)
HALL = (100, 100, 100)
TUMEHALL = (60, 60, 60)
KULDNE = (255, 215, 0)
HELESININE = (100, 149, 237)
TAEVAS = (15, 15, 35)

# Fondid
font_suur = pygame.font.SysFont("Arial", 48, bold=True)
font_kesk = pygame.font.SysFont("Arial", 28, bold=True)
font_vaike = pygame.font.SysFont("Arial", 18)

kell = pygame.time.Clock()


def tekst_keskel(tekst, font, varv, y):
    pind = font.render(tekst, True, varv)
    x = (LAIUS - pind.get_width()) // 2
    ekraan.blit(pind, (x, y))


def menuu():
    valikud = [
        ("LIHTNE", ROHELINE),
        ("KESKMINE", ORANZ),
        ("RASKE", PUNANE)
    ]

    valitud = 0

    while True:
        ekraan.fill(TAEVAS)

        # Pealkiri
        tekst_keskel("Ussi Mäng", font_suur, ROHELINE, 50)
        tekst_keskel("Kõrgeim skoor: 43", font_vaike, KULDNE, 120)

        # Nupud
        for i, (nimi, varv) in enumerate(valikud):
            y = 180 + i * 70

            if i == valitud:
                pygame.draw.rect(
                    ekraan,
                    varv,
                    (190, y, 260, 50),
                    border_radius=8
                )
                tekst = font_kesk.render(nimi, True, MUST)
            else:
                pygame.draw.rect(
                    ekraan,
                    TUMEHALL,
                    (190, y, 260, 50),
                    border_radius=8
                )
                tekst = font_kesk.render(nimi, True, HALL)

            ekraan.blit(
                tekst,
                (LAIUS // 2 - tekst.get_width() // 2, y + 8)
            )

        # Selgitus
        kirjeldused = [
            "LIHTNE: madu läbib seinad",
            "KESKMINE: seinad tapavad",
            "RASKE: rohkem takistusi ja kiirem"
        ]

        tekst_keskel(kirjeldused[valitud],
                     font_vaike,
                     HELESININE,
                     390)

        tekst_keskel(
            "↑ ↓ vali | ENTER alusta | ESC valju",
            font_vaike,
            HALL,
            430
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    valitud = (valitud - 1) % len(valikud)

                elif event.key == pygame.K_DOWN:
                    valitud = (valitud + 1) % len(valikud)

                elif event.key == pygame.K_RETURN:
                    print("Valitud:", valikud[valitud][0])

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        kell.tick(30)


menuu()