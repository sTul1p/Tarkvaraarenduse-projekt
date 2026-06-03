import pygame
import sys
import random

pygame.init()

# Ekraan
screenX = 640
screenY = 480
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Auto mäng")
clock = pygame.time.Clock()

# Pildid
bg = pygame.image.load("bg_rally.jpg")
bg = pygame.transform.scale(bg, (screenX, screenY))

red_car = pygame.image.load("f1_red.png")
red_car = pygame.transform.scale(red_car, (60, 100))

blue_car = pygame.image.load("f1_blue.png")
blue_car = pygame.transform.scale(blue_car, (60, 100))
blue_car = pygame.transform.rotate(blue_car, 180)

CAR_W = 60
CAR_H = 100

# Raja keskel olevad x-koordinaadid (auto joonistatakse keskpunktist)
# Tee on ligikaudu x=140 kuni x=500, kolm rada:
LANE_CENTERS = [195, 310, 425]  # iga raja keskpunkt

def draw_car(surface, image, center_x, y):
    """Joonista auto nii, et auto horisontaalne keskpunkt = center_x"""
    surface.blit(image, (center_x - CAR_W // 2, y))

# Punane auto: keskmises rajas
redX = LANE_CENTERS[1]   # 310 = täpselt keskel
redY = screenY - 120

# Sinised autod
NUM_BLUE = 3
SPEED = 5

blue_cars = []
for i in range(NUM_BLUE):
    lane = random.choice(LANE_CENTERS)
    y = -200 - i * 180
    blue_cars.append([lane, y])

# Skoor
score = 0
font = pygame.font.SysFont("Arial", 30)

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Taust
    screen.blit(bg, (0, 0))

    # Punane auto (keskel)
    draw_car(screen, red_car, redX, redY)

    # Sinised autod
    for car in blue_cars:
        car[1] += SPEED

        if car[1] > screenY:
            while True:
                new_lane = random.choice(LANE_CENTERS)
                free = True
                for other in blue_cars:
                    if other != car and other[0] == new_lane:
                        if other[1] < 150:
                            free = False
                            break
                if free:
                    break

            car[0] = new_lane
            car[1] = -200
            score += 1

        draw_car(screen, blue_car, car[0], car[1])

    # Skoor
    score_text = font.render("Skoor: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()