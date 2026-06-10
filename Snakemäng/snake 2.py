import pygame
import random

# pygame initsialiseerimine
pygame.init()

# ekraani ja mänguvälja seaded (realpython lähenemine: konstantidena)
LAIUS  = 640
KÕRGUS = 480
RUUT   = 20          # ühe lahtri suurus pikslites
VEERUD = LAIUS  // RUUT   # 32 veergu
RIDAD  = KÕRGUS // RUUT   # 24 rida

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussimäng v2")
kell = pygame.time.Clock()
KIIRUS = 10  # alg-fps

# värvid
MUST        = (0, 0, 0)
VALGE       = (255, 255, 255)
ROHELINE    = (50, 205, 50)
TUMEROHELINE = (0, 128, 0)
PUNANE      = (220, 20, 60)
KULDNE      = (255, 215, 0)
TAUSTAVÄRV  = (15, 15, 35)    # tume taust
RUUDUSTIK   = (25, 25, 50)    # ruudustiku värv
HALL        = (120, 120, 120)

# fondid (realpython: SysFont lähenemine)
font_suur  = pygame.font.SysFont("Arial", 42, bold=True)
font_kesk  = pygame.font.SysFont("Arial", 26, bold=True)
font_väike = pygame.font.SysFont("Arial", 18)


def joonista_taust():
    """
    Joonistab ruudustiku taustaefekti.
    Realpython: eraldi abifunktsioon joonistamiseks.
    """
    ekraan.fill(TAUSTAVÄRV)
    for x in range(0, LAIUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (x, 0), (x, KÕRGUS), 1)
    for y in range(0, KÕRGUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (0, y), (LAIUS, y), 1)


def joonista_madu(madu):
    """
    Joonistab madu – pea eraldi värviga, keha heledus
    väheneb saba poole (realpython: visuaalne täiustus).
    """
    for i, (x, y) in enumerate(madu):
        if i == 0:
            # pea – valge ääristus + roheline sisu
            pygame.draw.rect(ekraan, VALGE,
                             (x * RUUT + 1, y * RUUT + 1, RUUT - 2, RUUT - 2),
                             border_radius=5)
            pygame.draw.rect(ekraan, ROHELINE,
                             (x * RUUT + 2, y * RUUT + 2, RUUT - 4, RUUT - 4),
                             border_radius=4)
        else:
            # keha – heledus kahaneb saba poole
            heledus = max(60, 180 - i * 5)
            pygame.draw.rect(ekraan, (0, heledus, 0),
                             (x * RUUT + 1, y * RUUT + 1, RUUT - 2, RUUT - 2),
                             border_radius=3)


def joonista_toit(pos):
    """Joonistab toidu punase ringina."""
    cx = pos[0] * RUUT + RUUT // 2
    cy = pos[1] * RUUT + RUUT // 2
    pygame.draw.circle(ekraan, PUNANE, (cx, cy), RUUT // 2 - 1)
    pygame.draw.circle(ekraan, (255, 120, 120), (cx, cy), RUUT // 2 - 4)


def joonista_hud(skoor, rekord):
    """
    Kuvab skoori ja rekordi ekraani ülaosas
    (geeksforgeeks: show_score funktsioon laiendatult).
    """
    pygame.draw.rect(ekraan, (10, 10, 25), (0, 0, LAIUS, 22))
    s = font_väike.render(f"Skoor: {skoor}", True, VALGE)
    r = font_väike.render(f"Rekord: {rekord}", True, KULDNE)
    ekraan.blit(s, (6, 3))
    ekraan.blit(r, (LAIUS - r.get_width() - 6, 3))


def uus_toit(madu):
    """Genereerib uue toidu asukoha, mis ei kattu maduga."""
    madu_hulk = set(map(tuple, madu))
    # HUD-riba (rida 0) on reserveeritud
    vabad = [(x, y) for x in range(VEERUD)
             for y in range(1, RIDAD)
             if (x, y) not in madu_hulk]
    return random.choice(vabad) if vabad else (VEERUD // 2, RIDAD // 2)


def alg_ekraan():
    """Kuvab alustamise ekraani (realpython: eraldi olekuhaldus)."""
    while True:
        joonista_taust()
        t1 = font_suur.render("Ussimäng v2", True, ROHELINE)
        t2 = font_kesk.render("Vajuta ENTER alustamiseks", True, VALGE)
        t3 = font_väike.render("Nooleklahvid – liigu   |   ESC – välju", True, HALL)
        ekraan.blit(t1, (LAIUS // 2 - t1.get_width() // 2, 160))
        ekraan.blit(t2, (LAIUS // 2 - t2.get_width() // 2, 240))
        ekraan.blit(t3, (LAIUS // 2 - t3.get_width() // 2, 290))
        pygame.display.flip()
        kell.tick(30)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return True
                if ev.key == pygame.K_ESCAPE:
                    return False


def lõpp_ekraan(skoor, rekord):
    """Kuvab mängu lõpu ekraani."""
    while True:
        joonista_taust()
        t1 = font_suur.render("MÄNG LÄBI", True, PUNANE)
        t2 = font_kesk.render(f"Skoor: {skoor}", True, VALGE)
        t3 = font_kesk.render(f"Rekord: {rekord}", True, KULDNE)
        t4 = font_väike.render("R – uuesti   |   ESC – välju", True, HALL)
        ekraan.blit(t1, (LAIUS // 2 - t1.get_width() // 2, 140))
        ekraan.blit(t2, (LAIUS // 2 - t2.get_width() // 2, 210))
        ekraan.blit(t3, (LAIUS // 2 - t3.get_width() // 2, 255))
        ekraan.blit(t4, (LAIUS // 2 - t4.get_width() // 2, 320))
        pygame.display.flip()
        kell.tick(30)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    return True
                if ev.key == pygame.K_ESCAPE:
                    return False


def mängi(rekord):
    """
    Põhimängu tsükkel.
    Realpython lähenemine: tuple-põhised koordinaadid (veerg, rida),
    wrap-around seintest läbiminek.
    """
    # madu algseisund – koordinaadid ruutudes (realpython: tuple lähenemine)
    madu = [(VEERUD // 2, RIDAD // 2)]
    suund      = (1, 0)   # algsuund: parem
    jrg_suund  = suund
    toit = uus_toit(madu)
    skoor = 0
    kiirus = KIIRUS

    while True:
        kell.tick(kiirus)

        # sündmuste käsitlemine
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                # geeksforgeeks: 180° pööret ei lubata
                if ev.key == pygame.K_UP    and suund != (0, 1):
                    jrg_suund = (0, -1)
                elif ev.key == pygame.K_DOWN  and suund != (0, -1):
                    jrg_suund = (0, 1)
                elif ev.key == pygame.K_LEFT  and suund != (1, 0):
                    jrg_suund = (-1, 0)
                elif ev.key == pygame.K_RIGHT and suund != (-1, 0):
                    jrg_suund = (1, 0)
                elif ev.key == pygame.K_ESCAPE:
                    return skoor

        suund = jrg_suund

        # uue pea arvutamine wrap-aroundiga
        # (realpython: % operaator piiride sees hoidmiseks)
        px, py = madu[0]
        uus_pea = (
            (px + suund[0]) % VEERUD,
            (py - 1 + suund[1]) % (RIDAD - 1) + 1,  # jätab HUD-riba vahele
        )

        # iseendasse sõitmine – mäng lõpeb
        if uus_pea in madu:
            return skoor

        madu.insert(0, uus_pea)

        # toidu söömine
        if uus_pea == toit:
            skoor += 1
            toit = uus_toit(madu)
            # kiireneme iga 5 punkti järel (max 20 fps)
            kiirus = min(KIIRUS + skoor // 5 * 2, 20)
        else:
            madu.pop()   # saba eemaldamine

        rekord = max(rekord, skoor)

        # joonistamine
        joonista_taust()
        joonista_toit(toit)
        joonista_madu(madu)
        joonista_hud(skoor, rekord)
        pygame.display.flip()


# peaprogramm
if __name__ == "__main__":
    rekord = 0
    if alg_ekraan():
        while True:
            skoor = mängi(rekord)
            rekord = max(rekord, skoor)
            if not lõpp_ekraan(skoor, rekord):
                break
    pygame.quit()

# Allikas: https://realpython.com/pygame-a-primer/
# Allikas: https://www.geeksforgeeks.org/python/snake-game-in-python-using-pygame-module/
