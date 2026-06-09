import pygame  # Mängumootor graafika ja sündmuste jaoks
import sys  # Süsteemifunktsioonid (väljumine)
import random  # Juhuslikkus boonuste jaoks

pygame.init()  # Käivitame pygame'i moodulid

# Ekraani seaded
W, H = 640, 480  # Akna laius ja kõrgus pikslites
screen = pygame.display.set_mode((W, H))  # Loome akna antud mõõtmetega
pygame.display.set_caption("Hiir")  # Määrame akna pealkirja
clock = pygame.time.Clock()  # Kellaobj kaadrisageduse piiramiseks

# Värvid RGB formaadis
TAUST      = (173, 216, 230)  # Hele sinine taust
RING_VÄRV  = (0, 0, 139)      # Tumesinine tavaline ring (ääris)
BOONUS     = (220, 20, 60)    # Punane boonusring

MUST = (0, 0, 0)  # Musta värv teksti jaoks

# Mängu konstandid
ALGRAADIUS        = 10   # Iga uue ringi algne raadius pikslites
KASV              = 5    # Mitu pikslit kasvab iga ring kliki järel
MAX_RINGID        = 10   # Maksimaalselt nii palju ringi korraga ekraanil
BOONUS_TÕENÄOSUS  = 0.2  # Tõenäosus, et uus ring on boonusring (0.0–1.0)

font = pygame.font.SysFont("Arial", 18)  # Laeme fondi ekraanitekstide jaoks

# Ringide nimekiri – iga ring on sõnastik väljadega: x, y, raadius, on_boonus
ringid = []

# Põhitsükkel – töötab kuni mäng suletakse
running = True
while running:

    # Sündmuste töötlemine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Kasutaja sulges akna
            running = False  # Lõpetame põhitsükli

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Vasak hiireklõps
            # 1) Arvutame uue ringi raadiuse – iga järgmine ring on KASV võrra suurem
            uus_raadius = ALGRAADIUS + len(ringid) * KASV  # Mida rohkem ringe, seda suurem uus

            # 2) Lisame uue ringi klikitud asukohale
            on_boonus = random.random() < BOONUS_TÕENÄOSUS  # Otsustame juhusliku boonuse
            mx, my = event.pos  # Loeme hiire koordinaadid kliki hetkel
            ringid.append({        # Lisame uue ringi nimekirja
                "x":         mx,          # Ringi keskpunkti x-koordinaat
                "y":         my,          # Ringi keskpunkti y-koordinaat
                "raadius":   uus_raadius, # Uus ring on alati suurem kui eelmine
                "on_boonus": on_boonus,   # Kas tegemist on boonusringiga
            })

            # 3) Kui ringe on üle maksimumi, eemaldame kõige vanema
            while len(ringid) > MAX_RINGID:
                ringid.pop(0)  # Esimene element on vanim ring

    # Joonistamine
    screen.fill(TAUST)  # Täidame tausta värviga (kustutame eelmise kaadri)

    for r in ringid:  # Joonistame kõik ringid
        värv = BOONUS if r["on_boonus"] else RING_VÄRV  # Boonusring punane, tavaline sinine
        pygame.draw.circle(screen, värv, (r["x"], r["y"]), r["raadius"], 2)  # Joonistame ringi äärisena (paksus 2)

    # Juhistekst ekraani vasakus ülanurgas
    juhis = font.render("Kliki ekraanile, et ringid tekiksid", True, MUST)
    screen.blit(juhis, (8, 8))  # Kuvame teksti koordinaatidel (8, 8)

    # Ringide loendur ekraani paremas ülanurgas
    loendur = font.render(f"Renge ekraanil: {len(ringid)} / {MAX_RINGID}", True, MUST)
    screen.blit(loendur, (W - loendur.get_width() - 8, 8))  # Joondame paremale

    pygame.display.flip()  # Uuendame ekraani (kuvame uue kaadri)
    clock.tick(60)  # Piirame kaadrisageduse 60 kaadri sekundiga

pygame.quit()  # Sulgeme pygame'i moodulid korrektselt
sys.exit()  # Lõpetame programmi