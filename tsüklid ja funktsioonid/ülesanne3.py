import pygame
import sys

def joonista_ruudustik(ekraan, ruudu_suurus=20, joone_värv=(255, 0, 0)):
    laius, kõrgus = ekraan.get_size()

    # Täidab tausta rohelisega
    ekraan.fill((144, 238, 144))

    # Joonistab vertikaalsed jooned
    x = 0
    while x <= laius:
        pygame.draw.line(ekraan, joone_värv, (x, 0), (x, kõrgus))
        x += ruudu_suurus

    # Joonistab horisontaalsed jooned
    y = 0
    while y <= kõrgus:
        pygame.draw.line(ekraan, joone_värv, (0, y), (laius, y))
        y += ruudu_suurus

def main():
    pygame.init()
    ekraan = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Harjutamine")

    # Muuda neid väärtusi ruudustiku muutmiseks:
    ruudu_suurus = 20          # ruudu suurus pikslites
    joone_värv = (255, 0, 0)

    while True:
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        joonista_ruudustik(ekraan, ruudu_suurus, joone_värv)
        pygame.display.flip()

if __name__ == "__main__":
    main()