import pygame
import math

pygame.init()

screen = pygame.display.set_mode([680, 500])
pygame.display.set_caption("Lumemees-Sander Tulp")

#Värvid
must = (0, 0, 0)
valge = (255, 255, 255)
punane = (255, 0, 0)
oranz = (255, 140, 0)
helesinine = (135, 206, 235)
kollane = (255, 215, 0)
pruun = (90, 58, 26)
tume_pruun = (139, 105, 20)
tumehall = (34, 34, 34)
lumevalge = (240, 248, 255)

screen.fill(helesinine)

#Päike
px, py = 580, 70
pygame.draw.circle(screen, kollane, [px, py], 38)
for i in range(8):
    nurk = math.radians(i * 45)
    x1 = int(px + 44 * math.cos(nurk))
    y1 = int(py + 44 * math.sin(nurk))
    x2 = int(px + 60 * math.cos(nurk))
    y2 = int(py + 60 * math.sin(nurk))
    pygame.draw.line(screen, kollane, [x1, y1], [x2, y2], 4)

#Pilved
def joonista_pilv(surf, cx, cy, suurus=1.0):
    pygame.draw.circle(surf, valge, [cx, cy], int(28 * suurus))
    pygame.draw.circle(surf, valge, [cx + int(28 * suurus), cy - int(12 * suurus)], int(34 * suurus))
    pygame.draw.circle(surf, valge, [cx + int(60 * suurus), cy - int(4 * suurus)], int(26 * suurus))
    pygame.draw.rect(surf, valge, [cx, cy, int(86 * suurus), int(26 * suurus)])

joonista_pilv(screen, 60, 90, 1.0)
joonista_pilv(screen, 260, 50, 0.85)
joonista_pilv(screen, 450, 140, 0.85)

#Keha
pygame.draw.circle(screen, valge, [340, 390], 60)
pygame.draw.circle(screen, valge, [340, 305], 40)

#pea
pygame.draw.circle(screen, valge, [340, 235], 28)

#Silmad
pygame.draw.circle(screen, must, [331, 228], 4)
pygame.draw.circle(screen, must, [349, 228], 4)

#Nina
pygame.draw.polygon(screen, oranz, [[340, 235], [355, 240], [340, 245]])

#Suu
pygame.draw.circle(screen, must, [330, 248], 3)
pygame.draw.circle(screen, must, [340, 252], 3)
pygame.draw.circle(screen, must, [350, 248], 3)

# Nupud kehal
pygame.draw.circle(screen, must, [340, 290], 4)
pygame.draw.circle(screen, must, [340, 305], 4)
pygame.draw.circle(screen, must, [340, 320], 4)

#Käed
#Vasak käsi
pygame.draw.line(screen, pruun, [300, 300], [220, 270], 6)

#Parem käsi
pygame.draw.line(screen, pruun, [380, 300], [455, 270], 6)

#Hari
pygame.draw.line(screen, (139, 69, 19), [455, 273], [502, 217], 5)
harjas_x, harjas_y = 502, 217
for offset in range(-3, 4):
    pygame.draw.line(screen, tume_pruun,
                     [harjas_x, harjas_y],
                     [harjas_x + offset * 5, harjas_y - 28], 2)
pygame.draw.line(screen, tume_pruun,
                 [harjas_x - 15, harjas_y - 20],
                 [harjas_x + 18, harjas_y - 20], 3)

#Kübar (äär)
pygame.draw.rect(screen, tumehall, [288, 205, 104, 10], border_radius=4)
#Keha
pygame.draw.rect(screen, tumehall, [306, 155, 68, 52], border_radius=3)
#Ülaosa
pygame.draw.rect(screen, tumehall, [306, 153, 68, 6], border_radius=2)

pygame.display.flip()

#Akna avatud hoidmine
jookseb = True
while jookseb:
    for sonnum in pygame.event.get():
        if sonnum.type == pygame.QUIT:
            jookseb = False

pygame.quit()