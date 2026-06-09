import pygame
import sys
import random

# --- Pygame initsialiseerimine ---
pygame.init()

# --- Ekraani seaded ---
LAIUS = 600
KÕRGUS = 400
RUUT = 20  # ühe lahtri suurus pikslites

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussimäng v1 - Lihtne")
kell = pygame.time.Clock()

# --- Värvid ---
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
ROHELINE = (0, 200, 0)
PUNANE = (200, 0, 0)

# --- Font ---
font = pygame.font.SysFont("Arial", 24)


def joonista_skoor(skoor):
    """Kuvab skoori ekraani vasakus ülanurgas."""
    tekst = font.render(f"Skoor: {skoor}", True, VALGE)
    ekraan.blit(tekst, (5, 5))


def mängi():
    """Põhimängu funktsioon."""
    # Madu algne positsioon ja keha (nimekiri koordinaatidest)
    madu = [(LAIUS // 2, KÕRGUS // 2)]
    suund = (RUUT, 0)  # alguses liigub paremale

    # Genereerime esimese toidu asukoha
    toit = (
        random.randrange(0, LAIUS // RUUT) * RUUT,
        random.randrange(0, KÕRGUS // RUUT) * RUUT,
    )

    skoor = 0

    while True:
        # --- Sündmuste töötlemine ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Muudame suunda, kuid ei luba 180-kraadist pööret
                if event.key == pygame.K_UP and suund != (0, RUUT):
                    suund = (0, -RUUT)
                elif event.key == pygame.K_DOWN and suund != (0, -RUUT):
                    suund = (0, RUUT)
                elif event.key == pygame.K_LEFT and suund != (RUUT, 0):
                    suund = (-RUUT, 0)
                elif event.key == pygame.K_RIGHT and suund != (-RUUT, 0):
                    suund = (RUUT, 0)

        # --- Uue pea arvutamine ---
        uus_pea = (madu[0][0] + suund[0], madu[0][1] + suund[1])

        # --- Seina kontrollimine – mäng lõpeb ---
        if (
            uus_pea[0] < 0 or uus_pea[0] >= LAIUS
            or uus_pea[1] < 0 or uus_pea[1] >= KÕRGUS
        ):
            return skoor

        # --- Iseendasse sõitmise kontroll ---
        if uus_pea in madu:
            return skoor

        # --- Madu liigutamine ---
        madu.insert(0, uus_pea)

        # --- Toidu söömine ---
        if uus_pea == toit:
            skoor += 1
            # Genereerime uue toidu
            toit = (
                random.randrange(0, LAIUS // RUUT) * RUUT,
                random.randrange(0, KÕRGUS // RUUT) * RUUT,
            )
        else:
            # Eemaldame saba, et madu ei kasvaks
            madu.pop()

        # --- Joonistamine ---
        ekraan.fill(MUST)

        # Joonistame madu
        for segment in madu:
            pygame.draw.rect(ekraan, ROHELINE, (*segment, RUUT - 2, RUUT - 2))

        # Joonistame toidu
        pygame.draw.rect(ekraan, PUNANE, (*toit, RUUT - 2, RUUT - 2))

        # Kuvame skoori
        joonista_skoor(skoor)

        pygame.display.flip()
        kell.tick(8)  # mängu kiirus (kaadrit sekundis)


def mängu_lõpp(skoor):
    """Kuvab mängu lõpu ekraani."""
    ekraan.fill(MUST)
    lõpp_tekst = font.render(f"Mäng läbi! Skoor: {skoor}", True, VALGE)
    restart_tekst = font.render("Vajuta R uuesti mängimiseks või Q väljumiseks", True, VALGE)
    ekraan.blit(lõpp_tekst, (LAIUS // 2 - lõpp_tekst.get_width() // 2, KÕRGUS // 2 - 30))
    ekraan.blit(restart_tekst, (LAIUS // 2 - restart_tekst.get_width() // 2, KÕRGUS // 2 + 10))
    pygame.display.flip()

    # Ootame klahvivajutust
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # mängi uuesti
                elif event.key == pygame.K_q:
                    return False  # välju


# --- Peaprogramm ---
if __name__ == "__main__":
    while True:
        skoor = mängi()
        if not mängu_lõpp(skoor):
            break
    pygame.quit()
    sys.exit()

    #https://www.edureka.co/blog/snake-game-with-pygame/
    #https://www.geeksforgeeks.org/python/snake-game-in-python-using-pygame-module/