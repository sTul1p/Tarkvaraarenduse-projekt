import pygame
import random

# --- pygame initsialiseerimine ---
pygame.init()

# --- ekraani seaded ---
LAIUS  = 640
KÕRGUS = 480
RUUT   = 20
VEERUD = LAIUS  // RUUT
RIDAD  = KÕRGUS // RUUT

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussimäng v3 – takistused ja boonus")
kell = pygame.time.Clock()
KIIRUS = 10

# --- värvid ---
MUST         = (0, 0, 0)
VALGE        = (255, 255, 255)
ROHELINE     = (50, 205, 50)
PUNANE       = (220, 20, 60)
KULDNE       = (255, 215, 0)
ORANŽ        = (255, 140, 0)
TAUSTAVÄRV   = (15, 15, 35)
RUUDUSTIK    = (25, 25, 50)
HALL         = (100, 100, 100)
HELESININE   = (100, 149, 237)
TUMEHALL     = (60, 60, 60)

# --- fondid ---
font_suur  = pygame.font.SysFont("Arial", 42, bold=True)
font_kesk  = pygame.font.SysFont("Arial", 26, bold=True)
font_väike = pygame.font.SysFont("Arial", 18)


def joonista_taust():
    """Joonistab ruudustiku tausta (v2-st võetud)."""
    ekraan.fill(TAUSTAVÄRV)
    for x in range(0, LAIUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (x, 0), (x, KÕRGUS), 1)
    for y in range(0, KÕRGUS, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (0, y), (LAIUS, y), 1)


def joonista_madu(madu):
    """Joonistab madu ümardatud ruutudena (v2-st võetud)."""
    for i, (x, y) in enumerate(madu):
        if i == 0:
            pygame.draw.rect(ekraan, VALGE,
                             (x*RUUT+1, y*RUUT+1, RUUT-2, RUUT-2), border_radius=5)
            pygame.draw.rect(ekraan, ROHELINE,
                             (x*RUUT+2, y*RUUT+2, RUUT-4, RUUT-4), border_radius=4)
        else:
            heledus = max(60, 180 - i * 5)
            pygame.draw.rect(ekraan, (0, heledus, 0),
                             (x*RUUT+1, y*RUUT+1, RUUT-2, RUUT-2), border_radius=3)


def joonista_toit(pos):
    """Joonistab tavalise toidu punase ringina."""
    cx = pos[0] * RUUT + RUUT // 2
    cy = pos[1] * RUUT + RUUT // 2
    pygame.draw.circle(ekraan, PUNANE, (cx, cy), RUUT // 2 - 1)
    pygame.draw.circle(ekraan, (255, 120, 120), (cx, cy), RUUT // 2 - 4)


def joonista_boonus(pos, timer):
    """
    Joonistab boonustoidu – vilkuv kuldne ring.
    UUS v3-s: visuaalne eristus tavalisest toidust.
    """
    if (timer // 10) % 2 == 0:   # vilgub iga 10 kaadri järel
        cx = pos[0] * RUUT + RUUT // 2
        cy = pos[1] * RUUT + RUUT // 2
        pygame.draw.circle(ekraan, KULDNE, (cx, cy), RUUT // 2 - 1)
        pygame.draw.circle(ekraan, ORANŽ,  (cx, cy), RUUT // 2 - 3)


def joonista_takistused(takistused):
    """
    Joonistab halliga takistusruudud.
    UUS v3-s: takistused on staatilised müürid mänguväljal.
    """
    for tx, ty in takistused:
        pygame.draw.rect(ekraan, TUMEHALL,
                         (tx*RUUT, ty*RUUT, RUUT, RUUT))
        pygame.draw.rect(ekraan, HALL,
                         (tx*RUUT+1, ty*RUUT+1, RUUT-2, RUUT-2), border_radius=2)


def joonista_hud(skoor, rekord):
    """Kuvab skoori ja rekordi HUD-ribal (v2-st võetud)."""
    pygame.draw.rect(ekraan, (10, 10, 25), (0, 0, LAIUS, 22))
    s = font_väike.render(f"Skoor: {skoor}", True, VALGE)
    r = font_väike.render(f"Rekord: {rekord}", True, KULDNE)
    ekraan.blit(s, (6, 3))
    ekraan.blit(r, (LAIUS - r.get_width() - 6, 3))


def uus_toit_pos(madu, takistused, välistatud=None):
    """Genereerib toidu asukohta mis ei kattu maduga ega takistustega."""
    keelatud = set(map(tuple, madu)) | set(takistused)
    if välistatud:
        keelatud.add(tuple(välistatud))
    vabad = [(x, y) for x in range(VEERUD)
             for y in range(1, RIDAD) if (x, y) not in keelatud]
    return random.choice(vabad) if vabad else (VEERUD // 2, RIDAD // 2)


def genereeri_takistused(arv, madu, toit):
    """
    Genereerib juhuslikud takistused mänguväljale.
    UUS v3-s: takistused ei kattu madu ega toiduga.
    """
    keelatud = set(map(tuple, madu)) | {tuple(toit)}
    takistused = []
    katsed = 0
    while len(takistused) < arv and katsed < 1000:
        katsed += 1
        x = random.randint(0, VEERUD - 1)
        y = random.randint(1, RIDAD - 1)
        if (x, y) not in keelatud and (x, y) not in takistused:
            takistused.append((x, y))
    return takistused


def lõpp_ekraan(skoor, rekord):
    """Kuvab mängu lõpu ekraani."""
    while True:
        joonista_taust()
        t1 = font_suur.render("MÄNG LÄBI", True, PUNANE)
        t2 = font_kesk.render(f"Skoor: {skoor}", True, VALGE)
        t3 = font_kesk.render(f"Rekord: {rekord}", True, KULDNE)
        t4 = font_väike.render("R – uuesti   |   Q – välju", True, HALL)
        ekraan.blit(t1, (LAIUS//2 - t1.get_width()//2, 140))
        ekraan.blit(t2, (LAIUS//2 - t2.get_width()//2, 210))
        ekraan.blit(t3, (LAIUS//2 - t3.get_width()//2, 255))
        ekraan.blit(t4, (LAIUS//2 - t4.get_width()//2, 320))
        pygame.display.flip()
        kell.tick(30)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r: return True
                if ev.key == pygame.K_q: return False


def mängi():
    """
    Põhimängu tsükkel.
    v3 UUED ASJAD võrreldes v2-ga:
      - 5 takistust mänguväljal (tapavad madu)
      - boonustoit ilmub perioodiliselt, annab +3 punkti
      - wrap-around seinad (v2-st) jäävad alles
    """
    # madu algseisund (v2-st)
    madu      = [(VEERUD // 2, RIDAD // 2)]
    suund     = (1, 0)
    jrg_suund = suund
    rekord    = 0

    # toit (v2-st)
    toit = uus_toit_pos(madu, [])

    # UUS: 5 takistust alguses
    takistused = genereeri_takistused(5, madu, toit)

    # UUS: boonustoidu muutujad
    on_boonus    = False
    boonus_pos   = None
    boonus_timer = 0
    BOONUS_KESTUS = 120           # kaadrid kuni boonus kaob
    jrg_boonus   = random.randint(25, 60)  # millal järgmine boonus ilmub

    skoor = 0

    while True:
        kell.tick(KIIRUS)

        # sündmused
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP    and suund != (0, 1):  jrg_suund = (0, -1)
                elif ev.key == pygame.K_DOWN  and suund != (0,-1): jrg_suund = (0, 1)
                elif ev.key == pygame.K_LEFT  and suund != (1, 0): jrg_suund = (-1, 0)
                elif ev.key == pygame.K_RIGHT and suund != (-1,0): jrg_suund = (1, 0)

        suund = jrg_suund

        # uue pea arvutamine – wrap-around (v2-st)
        px, py  = madu[0]
        uus_pea = (
            (px + suund[0]) % VEERUD,
            (py - 1 + suund[1]) % (RIDAD - 1) + 1,
        )

        # kokkupõrke kontroll
        if uus_pea in madu:
            if lõpp_ekraan(skoor, rekord): return mängi()
            return
        # UUS: takistusesse sõitmine tapab
        if uus_pea in takistused:
            if lõpp_ekraan(skoor, rekord): return mängi()
            return

        madu.insert(0, uus_pea)

        # toidu söömine
        sõin = False
        if uus_pea == toit:
            skoor += 1
            sõin   = True
            toit   = uus_toit_pos(madu, takistused, boonus_pos)
        # UUS: boonustoidu söömine
        elif on_boonus and uus_pea == boonus_pos:
            skoor += 3            # +3 korraga
            sõin      = True
            on_boonus = False
            boonus_pos = None
            madu.append(madu[-1]) # madu kasvab 2 lisasegmenti võrra
            madu.append(madu[-1])

        if not sõin:
            madu.pop()
            # UUS: boonuse ilmumise loendur
            jrg_boonus -= 1
            if jrg_boonus <= 0 and not on_boonus:
                boonus_pos   = uus_toit_pos(madu, takistused, toit)
                on_boonus    = True
                boonus_timer = BOONUS_KESTUS
                jrg_boonus   = random.randint(40, 100)
        else:
            # UUS: boonuse taimer – kaob kui aeg otsa
            if on_boonus:
                boonus_timer -= 1
                if boonus_timer <= 0:
                    on_boonus  = False
                    boonus_pos = None

        rekord = max(rekord, skoor)

        # joonistamine
        joonista_taust()
        joonista_takistused(takistused)   # UUS
        joonista_toit(toit)
        if on_boonus and boonus_pos:
            joonista_boonus(boonus_pos, boonus_timer)  # UUS
        joonista_madu(madu)
        joonista_hud(skoor, rekord)
        pygame.display.flip()


# --- peaprogramm ---
if __name__ == "__main__":
    mängi()
    pygame.quit()

 # Allikas: https://www.geeksforgeeks.org/python/snake-game-in-python-using-pygame-module/
# Allikas: https://realpython.com/pygame-a-primer/