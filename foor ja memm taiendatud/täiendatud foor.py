import pygame

pygame.init()

screen = pygame.display.set_mode([300, 400])
pygame.display.set_caption("Foor-Sander Tulp")

#Värvid
must = (0, 0, 0)
hall = (50, 50, 50)
punane = (255, 0, 0)
kollane = (255, 220, 0)
roheline = (0, 200, 0)
valge = (255, 255, 255)
sinine = (0, 80, 255)

screen.fill(must)

#Foori kast
pygame.draw.rect(screen, hall, [100, 10, 100, 280])
pygame.draw.rect(screen, valge, [100, 10, 100, 280], 2)

#Foori tuled
pygame.draw.circle(screen, punane,  [150, 55], 35)
pygame.draw.circle(screen, kollane, [150, 150], 35)
pygame.draw.circle(screen, roheline,[150, 245], 35)

#Post
pygame.draw.rect(screen, hall, [142, 290, 16, 60])  # 16px lai post, 60px kõrge
pygame.draw.rect(screen, valge, [142, 290, 16, 60], 1)

#Postialus
alus_punktid = [
    (150, 360),   #ülemine tipp (posti all)
    (110, 395),   #vasak alumine
    (190, 395)    #parem alumine
]

#Kolmeks jagatud kõrgus
alus_korgus = 395 - 360
riba = alus_korgus // 3

#Sinine riba
pygame.draw.polygon(screen, sinine, [
    (150, 360),
    (110, 360 + riba),
    (190, 360 + riba)
])

#Must riba
pygame.draw.polygon(screen, must, [
    (150, 360 + riba),
    (110, 360 + 2*riba),
    (190, 360 + 2*riba)
])

#Valge riba
pygame.draw.polygon(screen, valge, [
    (150, 360 + 2*riba),
    (110, 395),
    (190, 395)
])

#Kontuur
pygame.draw.polygon(screen, valge, alus_punktid, 2)

pygame.display.flip()

#Aken
jookseb = True
while jookseb:
    for sonnum in pygame.event.get():
        if sonnum.type == pygame.QUIT:
            jookseb = False

pygame.quit()