import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruudustiku seadistamine")

font = pygame.font.SysFont(None, 32)


#NUPU KLASS
class Nupp:
    def __init__(self, text, x, y, w, h, väärtus):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.väärtus = väärtus
        self.valitud = False

    def joonista(self, ekraan):
        värv = (200, 200, 200)
        if self.valitud:
            värv = (100, 200, 100)

        pygame.draw.rect(ekraan, värv, self.rect)
        pygame.draw.rect(ekraan, (0, 0, 0), self.rect, 2)

        tekst = font.render(self.text, True, (0, 0, 0))
        ekraan.blit(tekst, (self.rect.x + 10, self.rect.y + 10))

    def kas_klikiti(self, pos):
        return self.rect.collidepoint(pos)


#RUUDUSTIK
def joonista_ruudustik(ekraan, ruudu_suurus, joone_värv):
    laius, kõrgus = ekraan.get_size()
    ekraan.fill((144, 238, 144))

    for x in range(0, laius + 1, ruudu_suurus):
        pygame.draw.line(ekraan, joone_värv, (x, 0), (x, kõrgus))

    for y in range(0, kõrgus + 1, ruudu_suurus):
        pygame.draw.line(ekraan, joone_värv, (0, y), (laius, y))


#MENÜÜ
def menuu():
    clock = pygame.time.Clock()

    # Ruudu suuruse nupud
    suuruse_nupud = [
        Nupp("10", 50, 100, 80, 40, 10),
        Nupp("20", 150, 100, 80, 40, 20),
        Nupp("40", 250, 100, 80, 40, 40),
    ]

    # Värvi nupud
    värvi_nupud = [
        Nupp("Punane", 50, 200, 120, 40, (255, 0, 0)),
        Nupp("Sinine", 200, 200, 120, 40, (0, 0, 255)),
        Nupp("Must", 350, 200, 120, 40, (0, 0, 0)),
    ]

    start_nupp = Nupp("ALUSTA", 250, 350, 140, 50, None)

    valitud_suurus = None
    valitud_värv = None

    while True:
        screen.fill((220, 220, 220))

        # Tekstid
        screen.blit(font.render("Vali ruudu suurus:", True, (0, 0, 0)), (50, 60))
        screen.blit(font.render("Vali joone värv:", True, (0, 0, 0)), (50, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Suurus
                for nupp in suuruse_nupud:
                    if nupp.kas_klikiti(pos):
                        valitud_suurus = nupp.väärtus
                        for n in suuruse_nupud:
                            n.valitud = False
                        nupp.valitud = True

                # Värv
                for nupp in värvi_nupud:
                    if nupp.kas_klikiti(pos):
                        valitud_värv = nupp.väärtus
                        for n in värvi_nupud:
                            n.valitud = False
                        nupp.valitud = True

                # Start
                if start_nupp.kas_klikiti(pos):
                    if valitud_suurus and valitud_värv:
                        return valitud_suurus, valitud_värv

        # Joonista nupud
        for nupp in suuruse_nupud:
            nupp.joonista(screen)

        for nupp in värvi_nupud:
            nupp.joonista(screen)

        start_nupp.joonista(screen)

        pygame.display.flip()
        clock.tick(60)


#MAIN
def main():
    ruudu_suurus, joone_värv = menuu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        joonista_ruudustik(screen, ruudu_suurus, joone_värv)
        pygame.display.flip()


if __name__ == "__main__":
    main()