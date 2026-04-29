import pygame
import sys

#Initsialiseerimine
pygame.init()

#Akna seaded
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ülesanne 2")

#Värvid
WHITE = (255, 255, 255)

#Laen pildid
#Pildid peavad olema samas kaustas skriptiga
try:
    background = pygame.image.load("bgshop.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except FileNotFoundError:
    background = None
    print("bgshop.jpg ei leitud! / bgshop.jpg not found!")

try:
    seller = pygame.image.load("seller.png")
    #Müüja suurus
    seller_height = 380
    seller_width = int(seller.get_width() * (seller_height / seller.get_height()))
    seller = pygame.transform.scale(seller, (seller_width, seller_height))
except FileNotFoundError:
    seller = None
    print("seller.png ei leitud! / seller.png not found!")

try:
    chat = pygame.image.load("chat.png")
    #Jutumull suurus
    chat_width = 320
    chat_height = int(chat.get_height() * (chat_width / chat.get_width()))
    chat = pygame.transform.scale(chat, (chat_width, chat_height))
except FileNotFoundError:
    chat = None
    print("chat.png ei leitud! / chat.png not found!")

#Font
try:
    font = pygame.font.SysFont("Arial", 28, bold=True)
except:
    font = pygame.font.Font(None, 32)

#Positsioonid
seller_x = 20
seller_y = HEIGHT - (seller.get_height() if seller else 380) - 10

chat_x = 230
chat_y = 60

#Mängusilmus
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Joonista taust
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((80, 60, 40))

    # Joonista müüja
    if seller:
        screen.blit(seller, (seller_x, seller_y))

    #Jutumull
    if chat:
        screen.blit(chat, (chat_x, chat_y))

        #Jutumulli tekst
        name_text = "Tere, olen Sander"
        text_surface = font.render(name_text, True, WHITE)

        # Teksti keskel jutumullis
        text_x = chat_x + (chat.get_width() - text_surface.get_width()) // 2
        text_y = chat_y + (chat.get_height() - text_surface.get_height()) // 2 - 10
        screen.blit(text_surface, (text_x, text_y))

    pygame.display.flip()
    clock.tick(60)