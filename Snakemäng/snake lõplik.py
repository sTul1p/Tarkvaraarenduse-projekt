import pygame
import sys
import random
import os
import json

#pygame initsialiseerimine
pygame.init()
try:
    pygame.mixer.init()
    HELI_OK = True
except pygame.error:
    HELI_OK = False

#ekraani mõõdud
LAIUS = 640
KÕRGUS = 480
RUUT = 20  # ühe lahtri suurus pikslites
VEERUD = LAIUS // RUUT  # 32 veergu
RIDAD = KÕRGUS // RUUT  # 24 rida

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Ussi mäng")
kell = pygame.time.Clock()

#värvid
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
TUMEROHELINE = (0, 128, 0)
ROHELINE = (50, 205, 50)
PUNANE = (220, 20, 60)
KULDNE = (255, 215, 0)
ORANŽ = (255, 140, 0)
TAEVAS = (15, 15, 35)  #taust
RUUDUSTIK = (25, 25, 50)  #tausta ruudustik
HALL = (100, 100, 100)
HELESININE = (100, 149, 237)
TUMEHALL = (60, 60, 60)

#fondid
font_suur = pygame.font.SysFont("Arial", 48, bold=True)
font_kesk = pygame.font.SysFont("Arial", 28, bold=True)
font_väike = pygame.font.SysFont("Arial", 18)

#kõrgeim skoor failist
SKOOR_FAIL = os.path.join(os.path.dirname(__file__), "highscore.json")


def laadi_rekord():
    try:
        with open(SKOOR_FAIL, "r") as f:
            return json.load(f).get("rekord", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def salvesta_rekord(skoor):
    rekord = laadi_rekord()
    if skoor > rekord:
        with open(SKOOR_FAIL, "w") as f:
            json.dump({"rekord": skoor}, f)


#tausta ruudustiku joonistamine
def joonista_taust(nihe):
    ekraan.fill(TAEVAS)
    # Liikuv vertikaalsed jooned
    for x in range(-(nihe % RUUT), LAIUS + RUUT, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (x, 0), (x, KÕRGUS), 1)
    # Horisontaalsed jooned
    for y in range(-(nihe % RUUT), KÕRGUS + RUUT, RUUT):
        pygame.draw.line(ekraan, RUUDUSTIK, (0, y), (LAIUS, y), 1)


#teksti joonistamine keskel
def joonista_tekst_kesk(tekst, font, värv, y_pos):
    pind = font.render(tekst, True, värv)
    x = (LAIUS - pind.get_width()) // 2
    ekraan.blit(pind, (x, y_pos))


#madu joonistamine
def joonista_madu(madu_keha):
    for i, (x, y) in enumerate(madu_keha):
        # Pea: erkkollane-roheline, keha: tumedam
        if i == 0:
            värv = ROHELINE
            pygame.draw.rect(ekraan, VALGE,
                             (x * RUUT + 1, y * RUUT + 1, RUUT - 2, RUUT - 2),
                             border_radius=5)
            pygame.draw.rect(ekraan, värv,
                             (x * RUUT + 2, y * RUUT + 2, RUUT - 4, RUUT - 4),
                             border_radius=4)
        else:
            # Keha: heledus väheneb saba poole
            heledus = max(60, 180 - i * 5)
            värv = (0, heledus, 0)
            pygame.draw.rect(ekraan, värv,
                             (x * RUUT + 1, y * RUUT + 1, RUUT - 2, RUUT - 2),
                             border_radius=3)


#toidu joonistamine
def joonista_toit(toit_pos, on_boonus, boonus_timer):
    x, y = toit_pos
    if on_boonus:
        # Boonustoit vilgub: nähtav ainult iga teise kaadritsükli ajal
        if (boonus_timer // 10) % 2 == 0:
            pygame.draw.circle(ekraan, KULDNE,
                               (x * RUUT + RUUT // 2, y * RUUT + RUUT // 2),
                               RUUT // 2 - 1)
            pygame.draw.circle(ekraan, ORANŽ,
                               (x * RUUT + RUUT // 2, y * RUUT + RUUT // 2),
                               RUUT // 2 - 3)
    else:
        pygame.draw.circle(ekraan, PUNANE,
                           (x * RUUT + RUUT // 2, y * RUUT + RUUT // 2),
                           RUUT // 2 - 1)
        pygame.draw.circle(ekraan, (255, 100, 100),
                           (x * RUUT + RUUT // 2, y * RUUT + RUUT // 2),
                           RUUT // 2 - 4)


#takistuste joonistamine
def joonista_takistused(takistused):
    for (tx, ty) in takistused:
        pygame.draw.rect(ekraan, TUMEHALL,
                         (tx * RUUT, ty * RUUT, RUUT, RUUT))
        pygame.draw.rect(ekraan, HALL,
                         (tx * RUUT + 1, ty * RUUT + 1, RUUT - 2, RUUT - 2),
                         border_radius=2)


#HUD (skoor, rekord, tase)
def joonista_hud(skoor, rekord, tase, paus):
    # Taustariba
    pygame.draw.rect(ekraan, (10, 10, 25), (0, 0, LAIUS, 22))

    skoor_t = font_väike.render(f"Skoor: {skoor}", True, VALGE)
    rekord_t = font_väike.render(f"Rekord: {rekord}", True, KULDNE)
    tase_t = font_väike.render(f"Tase: {tase}", True, HELESININE)
    paus_t = font_väike.render("[ PAUS ]", True, ORANŽ)

    ekraan.blit(skoor_t, (6, 3))
    ekraan.blit(tase_t, (LAIUS // 2 - tase_t.get_width() // 2, 3))
    ekraan.blit(rekord_t, (LAIUS - rekord_t.get_width() - 6, 3))
    if paus:
        ekraan.blit(paus_t, (LAIUS // 2 - paus_t.get_width() // 2, KÕRGUS // 2 - 14))


#uue toidu asukoha genereerimine
def uus_toit(madu, takistused, välistatud=None):
    keelatud = set(map(tuple, madu)) | set(takistused)
    if välistatud:
        keelatud.add(tuple(välistatud))
    # Toit ei teki ülemisele HUD-ribale (rida 0)
    vabad = [(x, y) for x in range(VEERUD)
             for y in range(1, RIDAD)
             if (x, y) not in keelatud]
    return random.choice(vabad) if vabad else (VEERUD // 2, RIDAD // 2)


#takistuste genereerimine
def genereeri_takistused(arv, madu, toit1, toit2=None):
    keelatud = set(map(tuple, madu)) | {tuple(toit1)}
    if toit2:
        keelatud.add(tuple(toit2))
    takistused = []
    katsed = 0
    while len(takistused) < arv and katsed < 1000:
        katsed += 1
        x = random.randint(0, VEERUD - 1)
        y = random.randint(1, RIDAD - 1)
        if (x, y) not in keelatud and (x, y) not in takistused:
            takistused.append((x, y))
    return takistused


#  MENÜÜ: raskusastme valimine
def menüü_ekraan():
    valikud = [
        ("LIHTNE", 6, False, ROHELINE),
        ("KESKMINE", 10, True, ORANŽ),
        ("RASKE", 15, True, PUNANE),
    ]
    valitud = 0  # vaikimisi LIHTNE
    rekord = laadi_rekord()
    taust_nihe = 0

    while True:
        taust_nihe = (taust_nihe + 1) % (RUUT * 60)
        joonista_taust(taust_nihe)

        # Pealkiri
        joonista_tekst_kesk("Ussi Mäng", font_suur, ROHELINE, 60)
        rekord_t = font_väike.render(f"Kõrgeim skoor: {rekord}", True, KULDNE)
        ekraan.blit(rekord_t, (LAIUS // 2 - rekord_t.get_width() // 2, 125))

        # Raskusastme nupud
        for i, (nimi, _, _, värv) in enumerate(valikud):
            y = 180 + i * 70
            if i == valitud:
                # Valitud nupp – suurem, heledama taustaga
                pygame.draw.rect(ekraan, värv,
                                 (LAIUS // 2 - 130, y - 5, 260, 50),
                                 border_radius=8)
                t = font_kesk.render(nimi, True, MUST)
            else:
                pygame.draw.rect(ekraan, TUMEHALL,
                                 (LAIUS // 2 - 130, y - 5, 260, 50),
                                 border_radius=8)
                t = font_kesk.render(nimi, True, HALL)
            ekraan.blit(t, (LAIUS // 2 - t.get_width() // 2, y + 6))

        # Juhised
        j1 = font_väike.render("↑/↓ – vali  |  ENTER – alusta  |  ESC – välju (Kevin magab diivanil)", True, HALL)
        ekraan.blit(j1, (LAIUS // 2 - j1.get_width() // 2, 420))

        # LIHTSA taseme selgitus
        selgitus = [
            "LIHTNE: madu läbib seinad (wrap-around), vähem takistusi",
            "KESKMINE: seinad tapavad, rohkem takistusi",
            "RASKE: kõik tapab, maksimum takistusi, kiire madu",
        ]
        s = font_väike.render(selgitus[valitud], True, HELESININE)
        ekraan.blit(s, (LAIUS // 2 - s.get_width() // 2, 390))

        pygame.display.flip()
        kell.tick(30)

        # Sündmused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    valitud = (valitud - 1) % len(valikud)
                elif event.key == pygame.K_DOWN:
                    valitud = (valitud + 1) % len(valikud)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    kiirus, takistuste_arv_alg, sein_tapab, _ = valikud[valitud][1], \
                        [3, 6, 10][valitud], [False, True, True][valitud], \
                        valikud[valitud][3]
                    return kiirus, takistuste_arv_alg, sein_tapab
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit();
                    sys.exit()


#  MÄNGU LÕPU EKRAAN
def mängu_lõpp_ekraan(skoor, rekord, uus_rekord):
    """Kuvab mängu lõpu ekraani skooriga ning R/ESC valikutega."""
    taust_nihe = 0
    while True:
        taust_nihe = (taust_nihe + 1) % (RUUT * 60)
        joonista_taust(taust_nihe)

        joonista_tekst_kesk("MÄNG LÄBI", font_suur, PUNANE, 130)
        joonista_tekst_kesk(f"Sinu skoor: {skoor}", font_kesk, VALGE, 210)

        if uus_rekord:
            joonista_tekst_kesk("🏆 UUS REKORD!", font_kesk, KULDNE, 260)
        else:
            joonista_tekst_kesk(f"Rekord: {rekord}", font_kesk, KULDNE, 260)

        joonista_tekst_kesk("R – mängi uuesti  |  ESC – menüü", font_väike, HALL, 340)
        pygame.display.flip()
        kell.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "uuesti"
                elif event.key == pygame.K_ESCAPE:
                    return "menüü"



#  PÕHIMÄNG
def mängi(kiirus, takistuste_arv_alg, sein_tapab):
    #madu algseisund
    madu = [(VEERUD // 2, RIDAD // 2)]  # algpositsioon
    suund = (1, 0)  # liigub paremale
    järgmine_suund = suund

    #toit
    toit = uus_toit(madu, [])
    on_boonus = False  # kas praegu on boonustoit väljas
    boonus_pos = None  # boonustoidu positsioon
    boonus_timer = 0  # kui kaua boonustoit jääb nähtavaks
    BOONUS_KESTUS = 150  # kaadrid (≈10 sek 15 fps juures)
    järgmine_boonus = random.randint(30, 80)  # millal ilmub boonus

    #takistused
    takistused = genereeri_takistused(takistuste_arv_alg, madu, toit)

    #skoor ja tase
    skoor = 0
    tase = 1
    rekord = laadi_rekord()
    taust_nihe = 0
    paus = False
    kaadrid = 0  # mitu kaadrit on möödas (boonuse ajastus)

    while True:
        kell.tick(kiirus)
        taust_nihe = (taust_nihe + 1) % (RUUT * 60)

        #sündmuste käsitlemine
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Paus
                if event.key == pygame.K_p:
                    paus = not paus
                # Suunaklahvid – ei luba 180° pööret
                elif event.key == pygame.K_UP and suund != (0, 1):
                    järgmine_suund = (0, -1)
                elif event.key == pygame.K_DOWN and suund != (0, -1):
                    järgmine_suund = (0, 1)
                elif event.key == pygame.K_LEFT and suund != (1, 0):
                    järgmine_suund = (-1, 0)
                elif event.key == pygame.K_RIGHT and suund != (-1, 0):
                    järgmine_suund = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    return "menüü"

        if paus:
            # Pausis – joonista ekraan, kuid ära liigu
            joonista_taust(taust_nihe)
            joonista_takistused(takistused)
            joonista_toit(toit, False, 0)
            if on_boonus and boonus_pos:
                joonista_toit(boonus_pos, True, boonus_timer)
            joonista_madu(madu)
            joonista_hud(skoor, rekord, tase, paus=True)
            pygame.display.flip()
            continue

        kaadrid += 1
        suund = järgmine_suund

        #madu liigutamine
        pea_x, pea_y = madu[0]
        uus_x = pea_x + suund[0]
        uus_y = pea_y + suund[1]

        # Seina käsitlemine (wrap-around vs tapmine)
        if sein_tapab:
            # Raskel/Keskmisel: sein tapab
            if uus_x < 0 or uus_x >= VEERUD or uus_y < 1 or uus_y >= RIDAD:
                salvesta_rekord(skoor)
                return mängu_lõpp_ekraan(skoor, max(rekord, skoor), skoor > rekord)
        else:
            # Lihtsal: madu tuleb vastaspoolelt tagasi
            uus_x = uus_x % VEERUD
            uus_y = (uus_y - 1) % (RIDAD - 1) + 1  # jääb HUD-rist allapoole

        uus_pea = (uus_x, uus_y)

        #iseendasse sõitmine
        if uus_pea in madu:
            salvesta_rekord(skoor)
            return mängu_lõpp_ekraan(skoor, max(rekord, skoor), skoor > rekord)

        #takistusesse sõitmine
        if uus_pea in takistused:
            salvesta_rekord(skoor)
            return mängu_lõpp_ekraan(skoor, max(rekord, skoor), skoor > rekord)

        #madu liigutamise loogika
        madu.insert(0, uus_pea)  # lisa uus pea

        # Kas sõitsime toidule?
        sõin = False
        if uus_pea == toit:
            skoor += 1
            sõin = True
            toit = uus_toit(madu, takistused, boonus_pos)
        elif on_boonus and uus_pea == boonus_pos:
            # Boonustoit: +3 punkti, madu kasvab 3 ruutu
            skoor += 3
            sõin = True
            on_boonus = False
            boonus_pos = None
            # Lisa 2 lisasegmenti
            madu.append(madu[-1])
            madu.append(madu[-1])

        if not sõin:
            madu.pop()  #saba eemaldamine

        #boonustoidu ilmumine
            järgmine_boonus -= 1
            if järgmine_boonus <= 0:
                boonus_pos = uus_toit(madu, takistused, toit)
                on_boonus = True
                boonus_timer = BOONUS_KESTUS
                järgmine_boonus = random.randint(50, 120)
        else:
            # Boonuse taimer, kui aegub, kaob
            boonus_timer -= 1
            if boonus_timer <= 0:
                on_boonus = False
                boonus_pos = None

        #taseme tõus iga 5 punkti järel
        uus_tase = skoor // 5 + 1
        if uus_tase > tase:
            tase = uus_tase
            # Uuel tasemel tekib juurde üks takistus
            uued_takistused = genereeri_takistused(
                1, madu, toit, boonus_pos
            )
            takistused.extend(uued_takistused)

        #rekord jooksvalt
        rekord = max(rekord, skoor)

        #joonistamine
        joonista_taust(taust_nihe)
        joonista_takistused(takistused)
        joonista_toit(toit, False, 0)
        if on_boonus and boonus_pos:
            joonista_toit(boonus_pos, True, boonus_timer)
        joonista_madu(madu)
        joonista_hud(skoor, rekord, tase, paus=False)
        pygame.display.flip()



#  PEAPROGRAM
def peamine():
    """Programmi sisenemispunkt – menüü ja mängu tsükkel."""
    while True:
        # 1. Näita menüüd, saa raskusaste
        kiirus, takistuste_arv, sein_tapab = menüü_ekraan()
        # 2. Mängi
        tulemus = mängi(kiirus, takistuste_arv, sein_tapab)
        # Tulemus on kas "menüü" (ESC) või mängu_lõpp_ekraan tagastus
        if tulemus == "menüü":
            continue  # tagasi menüüsse
        elif tulemus == "uuesti":
            # Uuesti sama raskusastmega – tagasi menüüsse valikuks
            continue


if __name__ == "__main__":
    peamine()
    pygame.quit()
    sys.exit()