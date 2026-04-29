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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()