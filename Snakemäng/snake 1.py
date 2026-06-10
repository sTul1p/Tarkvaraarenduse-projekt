import pygame
import time
import random

# pygame initsialiseerimine
pygame.init()

# mänguakna suurus
LAIUS = 720
KÕRGUS = 480

# mänguakna loomine
aken = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussimäng v1")

# fps kontroller (edureka lähenemine: pygame.time.Clock)
fps = pygame.time.Clock()
KIIRUS = 12  # madu liikumise kiirus

# värvid RGB formaadis (geeksforgeeks lähenemine)
MUST  = pygame.Color(0, 0, 0)
VALGE = pygame.Color(255, 255, 255)
PUNANE  = pygame.Color(255, 0, 0)
ROHELINE = pygame.Color(0, 200, 0)
TUMEROHELINE = pygame.Color(0, 128, 0)


def kuva_skoor(skoor):
    """Kuvab mängija skoori ekraani vasakus ülanurgas."""
    # loome fondiobjekti (geeksforgeeks meetod)
    font = pygame.font.SysFont("arial", 22)
    # renderdame teksti pinnale
    pind = font.render(f"Skoor: {skoor}", True, VALGE)
    aken.blit(pind, (10, 10))


def mängu_lõpp(skoor):
    """Kuvab mängu lõpu ekraani ja ootab klahvivajutust."""
    aken.fill(MUST)
    font_suur = pygame.font.SysFont("times new roman", 50)
    font_väike = pygame.font.SysFont("arial", 24)

    # mäng läbi tekst
    t1 = font_suur.render("MÄNG LÄBI", True, PUNANE)
    t2 = font_väike.render(f"Skoor: {skoor}   Vajuta R uuesti või Q väljumiseks", True, VALGE)

    aken.blit(t1, (LAIUS // 2 - t1.get_width() // 2, KÕRGUS // 2 - 60))
    aken.blit(t2, (LAIUS // 2 - t2.get_width() // 2, KÕRGUS // 2 + 10))
    pygame.display.flip()

    # oota klahvivajutust (edureka: time.sleep lähenemine asendatud klahviga)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    return True   # uuesti
                if ev.key == pygame.K_q:
                    return False  # välju


def mängi():
    """
    Põhimängu funktsioon.
    Geeksforgeeks lähenemine: madu positsioon + keha nimekiri,
    suund stringina ('UP','DOWN','LEFT','RIGHT').
    """
    # madu algpositsioon (geeksforgeeks meetod – x,y koordinaadid pikslites)
    madu_pos = [200, 200]

    # madu keha – esimesed 3 segmenti (geeksforgeeks: [100,50],[90,50]...)
    madu_keha = [
        [200, 200],
        [180, 200],
        [160, 200],
    ]

    # toidu asukoht (geeksforgeeks: random.randrange * 10)
    toit_pos = [
        random.randrange(1, LAIUS // 20) * 20,
        random.randrange(1, KÕRGUS // 20) * 20,
    ]
    toit_olemas = True

    # suund (geeksforgeeks: string 'RIGHT','LEFT','UP','DOWN')
    suund = "RIGHT"
    uus_suund = suund

    skoor = 0

    while True:
        # sündmuste käsitlemine
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                # geeksforgeeks: suuna muutmine klahvidega, 180° ei lubata
                if ev.key == pygame.K_UP and suund != "DOWN":
                    uus_suund = "UP"
                elif ev.key == pygame.K_DOWN and suund != "UP":
                    uus_suund = "DOWN"
                elif ev.key == pygame.K_LEFT and suund != "RIGHT":
                    uus_suund = "LEFT"
                elif ev.key == pygame.K_RIGHT and suund != "LEFT":
                    uus_suund = "RIGHT"

        suund = uus_suund

        # madu liigutamine (geeksforgeeks: positsioon += samm)
        if suund == "UP":    madu_pos[1] -= 20
        elif suund == "DOWN":  madu_pos[1] += 20
        elif suund == "LEFT":  madu_pos[0] -= 20
        elif suund == "RIGHT": madu_pos[0] += 20

        # lisa uus pea kehasse
        madu_keha.insert(0, list(madu_pos))

        # kas sõime toidu?
        if madu_pos == toit_pos:
            skoor += 10
            toit_olemas = False  # genereeri uus toit
        else:
            madu_keha.pop()  # eemalda saba

        # uue toidu genereerimine
        if not toit_olemas:
            toit_pos = [
                random.randrange(1, LAIUS // 20) * 20,
                random.randrange(1, KÕRGUS // 20) * 20,
            ]
            toit_olemas = True

        # seina kontrollimine (geeksforgeeks: mäng lõpeb seinaga)
        if (madu_pos[0] < 0 or madu_pos[0] >= LAIUS or
                madu_pos[1] < 0 or madu_pos[1] >= KÕRGUS):
            return skoor

        # iseendasse sõitmise kontroll
        if madu_pos in madu_keha[1:]:
            return skoor

        # joonistamine
        aken.fill(MUST)

        # joonista toit – punane ruut (geeksforgeeks lähenemine)
        pygame.draw.rect(aken, PUNANE, pygame.Rect(toit_pos[0], toit_pos[1], 18, 18))

        # joonista madu – roheline keha, tumeroheline pea
        for i, segment in enumerate(madu_keha):
            värv = TUMEROHELINE if i == 0 else ROHELINE
            pygame.draw.rect(aken, värv, pygame.Rect(segment[0], segment[1], 18, 18))

        # kuva skoor
        kuva_skoor(skoor)

        pygame.display.flip()
        fps.tick(KIIRUS)


# peaprogramm
if __name__ == "__main__":
    while True:
        skoor = mängi()
        if not mängu_lõpp(skoor):
            break
    pygame.quit()

# Allikas: https://www.edureka.co/blog/snake-game-with-pygame/
# Allikas: https://www.geeksforgeeks.org/python/snake-game-in-python-using-pygame-module/
