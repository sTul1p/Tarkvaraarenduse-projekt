import pygame
import sys
import os

#Initsialiseeri pygame
pygame.init()

#Ekraani mõõtmed
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harjutamine")

#Laadi pildid
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bg = pygame.image.load(os.path.join(BASE_DIR, "bg_shop.jpg")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

seller_raw = pygame.image.load(os.path.join(BASE_DIR, "seller.png")).convert_alpha()
seller_h = int(HEIGHT * 0.64)
seller_w = int(seller_raw.get_width() * (seller_h / seller_raw.get_height()))
seller = pygame.transform.scale(seller_raw, (seller_w, seller_h))

chat_raw = pygame.image.load(os.path.join(BASE_DIR, "chat.png")).convert_alpha()
chat_w = 270
chat_h = int(chat_raw.get_height() * (chat_w / chat_raw.get_width()))
chat = pygame.transform.scale(chat_raw, (chat_w, chat_h))

#LISATUD: VIKK logo
vikk_raw = pygame.image.load(os.path.join(BASE_DIR, "VIKK_LOGO.webp")).convert_alpha()
vikk_w = 600
vikk_h = int(vikk_raw.get_height() * (vikk_w / vikk_raw.get_width()))
vikk_logo = pygame.transform.scale(vikk_raw, (vikk_w, vikk_h))

#LISATUD: Tort
tort_raw = pygame.image.load(os.path.join(BASE_DIR, "Tort.png")).convert_alpha()
tort_h = int(HEIGHT * 0.30)
tort_w = int(tort_raw.get_width() * (tort_h / tort_raw.get_height()))
tort = pygame.transform.scale(tort_raw, (tort_w, tort_h))

#LISATUD: Mõõk
moook_raw = pygame.image.load(os.path.join(BASE_DIR, "Mõõk.png")).convert_alpha()
moook_h = int(HEIGHT * 0.30)
moook_w = int(moook_raw.get_width() * (moook_h / moook_raw.get_height()))
moook = pygame.transform.scale(moook_raw, (moook_w, moook_h))
moook = pygame.transform.rotate(moook, -50)

#Font
font = pygame.font.SysFont("Georgia", 20, bold=True)

#Tekst
text = "Tere, olen Sander"
text_surf = font.render(text, True, (255, 255, 255))

#Positsioonid
seller_x = 105
seller_y = HEIGHT - seller_h - 16

chat_x = seller_x + seller_w - 118
chat_y = 64

#Teksti positsioon jutumulli sees
text_x = chat_x + (chat_w - text_surf.get_width()) // 2
text_y = chat_y + int(chat_h * 0.35)

#LISATUD: Positsioonid
vikk_x = 8
vikk_y = 8
tulevik_x = vikk_x + vikk_w + 6

tort_x = WIDTH // 2 - tort_w // 10
tort_y = HEIGHT - tort_h - 180

moook_x = WIDTH - moook_w + 20
moook_y = 30

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(bg, (0, 0))
    screen.blit(seller, (seller_x, seller_y))
    screen.blit(chat, (chat_x, chat_y))
    screen.blit(text_surf, (text_x, text_y))

    #LISATUD: logo, tort ja mõõk joonistamine
    screen.blit(vikk_logo, (vikk_x, vikk_y))
    screen.blit(tort, (tort_x, tort_y))
    screen.blit(moook, (moook_x, moook_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()