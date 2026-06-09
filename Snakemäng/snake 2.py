import pygame
import sys
import random

# --- Pygame initsialiseerimine ---
pygame.init()

# --- Ekraani ja mänguvälja seaded ---
LAIUS = 640
KÕRGUS = 480
RUUT = 20        # ühe lahtri suurus pikslites
VEERUD = LAIUS // RUUT   # 32 veergu
RIDAD = KÕRGUS // RUUT   # 24 rida

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussimäng v2 - Skoor ja wrap-around")
kell = pygame.time.Clock()

# --- Värvid ---
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
TUMEROHELINE = (0, 128, 0)
ROHELINE = (50, 205, 50)
PUNANE = (220, 20, 60)
KULDNE = (255, 215, 0)
TAUSTAVÄRV = (20, 20, 40)
RUUDUSTIK_VÄRV = (30, 30, 55)

# --- Fondid ---
font_suur = pygame.font.SysFont("Arial", 40, bold=True)
font_kesk = pygame.font.SysFont("Arial", 26, bold=True)
font_väike = pygame.font.SysFont("Arial", 18)


def joonista_taust():
    """Joonistab ruudustiku tausta."""
    ekraan.fill(TAUSTAVÄRV)
    for x in range(0, LAIUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK_VÄRV, (x, 0), (x, KÕRGUS), 1)
    for y in range(0, KÕRGUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK_VÄRV, (0, y), (LAIUS, y), 1)


def joonista_madu(madu):
    """Joonistab madu – pea ja keha erinevate värvidega."""
    for i, (x, y) in enumerate(madu):
        if i == 0:
            # Pea – heledam
            pygame.draw.rect(
                ekraan, ROHELINE,
                (x * RUUT + 1, y * RUUT + 1, RUUT - 2, RUUT - 2),
                border_radius=4,
            )
        else:
            # Keha – tumedam
            pygame.draw.rect(
                ekraan, TUMEROHELINE,
                (x * RUUT + 2, y * RUUT + 2, RUUT - 4, RUUT - 4),
                border_radius=3,
            )


def joonista_toit(pos):
    """Joonistab toidu punase ringina."""
    cx = pos[0] * RUUT + RUUT // 2
    cy = pos[1] * RUUT + RUUT // 2
    pygame.draw.circle(ekraan, PUNANE, (cx, cy), RUUT // 2 - 1)
    # Väike valge highlight
    pygame.draw.circle(ekraan, (255, 120, 120), (cx, cy), RUUT // 2 - 4)


def joonista_hud(skoor, rekord):
    """Kuvab skoori ja rekordi ekraani ülaosas."""
    pygame.draw.rect(ekraan, (10, 10, 25), (0, 0, LAIUS, 22))
    s = font_väike.render(f"Skoor: {skoor}", True, VALGE)
    r = font_väike.render(f"Rekord: {rekord}", True, KULDNE)
    ekraan.blit(s, (6, 3))
    ekraan.blit(r, (LAIUS - r.get_width() - 6, 3))


def uus_toit_pos(madu):
    """Genereerib uue toidu asukoha, mis ei kattu maduga."""
    madu_hulk = set(map(tuple, madu))
    # Toit ei teki HUD-ribale (rida 0 on reserveeritud skoorile)
    vabad = [
        (x, y)
        for x in range(VEERUD)
        for y in range(1, RIDAD)
        if (x, y) not in madu_hulk
    ]
    return random.choice(vabad) if vabad else (VEERUD // 2, RIDAD // 2)


def mängi(rekord):
    """Põhimängu tsükkel. Tagastab saavutatud skoori."""
    # Algseisund
    madu = [(VEERUD // 2, RIDAD // 2)]
    suund = (1, 0)          # alguses paremale
    järgmine_suund = suund
    toit = uus_toit_pos(madu)
    skoor = 0
    kiirus = 8  # alg-fps

    while True:
        kell.tick(kiirus)

        # --- Sündmused ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and suund != (0, 1):
                    järgmine_suund = (0, -1)
                elif event.key == pygame.K_DOWN and suund != (0, -1):
                    järgmine_suund = (0, 1)
                elif event.key == pygame.K_LEFT and suund != (1, 0):
                    järgmine_suund = (-1, 0)
                elif event.key == pygame.K_RIGHT and suund != (-1, 0):
                    järgmine_suund = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    return skoor

        suund = järgmine_suund

        # --- Liigutamine wrap-aroundiga (seinad ei tapa) ---
        pea_x, pea_y = madu[0]
        uus_x = (pea_x + suund[0]) % VEERUD
        # Y-telg: jätab HUD-riba (rida 0) vahele
        uus_y = (pea_y - 1 + suund[1]) % (RIDAD - 1) + 1
        uus_pea = (uus_x, uus_y)

        # --- Iseendasse sõitmine – mäng lõpeb ---
        if uus_pea in madu:
            return skoor

        # --- Madu liigutamine ---
        madu.insert(0, uus_pea)

        # --- Toidu söömine ---
        if uus_pea == toit:
            skoor += 1
            toit = uus_toit_pos(madu)
            # Kiireneme iga 5 punkti järel (max 18 fps)
            kiirus = min(8 + skoor // 5 * 2, 18)
        else:
            madu.pop()  # saba eemaldamine, kui toitu ei söödud

        # --- Joonistamine ---
        joonista_taust()
        joonista_toit(toit)
        joonista_madu(madu)
        joonista_hud(skoor, rekord)
        pygame.display.flip()


def alg_ekraan():
    """Kuvab lihtsa alg-/lõpuekraani."""
    ekraan.fill(MUST)
    joonista_taust()
    pealkiri = font_suur.render("Ussimäng v2", True, ROHELINE)
    alusta = font_kesk.render("Vajuta ENTER mängimiseks", True, VALGE)
    välju = font_väike.render("ESC – välju", True, (150, 150, 150))
    ekraan.blit(pealkiri, (LAIUS // 2 - pealkiri.get_width() // 2, 160))
    ekraan.blit(alusta, (LAIUS // 2 - alusta.get_width() // 2, 240))
    ekraan.blit(välju, (LAIUS // 2 - välju.get_width() // 2, 290))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False


def lõpp_ekraan(skoor, rekord):
    """Kuvab mängu lõpu ekraani."""
    ekraan.fill(MUST)
    joonista_taust()
    läbi = font_suur.render("MÄNG LÄBI", True, PUNANE)
    sk = font_kesk.render(f"Skoor: {skoor}", True, VALGE)
    rek = font_kesk.render(f"Rekord: {rekord}", True, KULDNE)
    uuesti = font_väike.render("R – uuesti  |  ESC – välju", True, (150, 150, 150))
    ekraan.blit(läbi, (LAIUS // 2 - läbi.get_width() // 2, 150))
    ekraan.blit(sk, (LAIUS // 2 - sk.get_width() // 2, 220))
    ekraan.blit(rek, (LAIUS // 2 - rek.get_width() // 2, 260))
    ekraan.blit(uuesti, (LAIUS // 2 - uuesti.get_width() // 2, 320))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # mängi uuesti
                elif event.key == pygame.K_ESCAPE:
                    return False  # välju


# --- Peaprogramm ---
if __name__ == "__main__":
    rekord = 0  # rekord salvestatakse mälusiseselt

    if not alg_ekraan():
        pygame.quit()
        sys.exit()

    while True:
        skoor = mängi(rekord)
        rekord = max(rekord, skoor)  # uuendame rekordit
        if not lõpp_ekraan(skoor, rekord):
            break

    pygame.quit()
    sys.exit()

    #https://realpython.com/pygame-a-primer/