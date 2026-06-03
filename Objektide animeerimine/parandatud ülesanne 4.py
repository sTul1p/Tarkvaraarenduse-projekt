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

# Rajad (vajadusel nihuta mõni piksel)
LANES = [160, 245, 330]

# Punane auto
redX = LANES[1]
redY = screenY - 120

# Sinised autod
NUM_BLUE = 3
SPEED = 5

blue_cars = []

for i in range(NUM_BLUE):
    lane = random.choice(LANES)
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

    # Punane auto
    screen.blit(red_car, (redX, redY))

    # Sinised autod
    for car in blue_cars:
        car[1] += SPEED

        # Kui auto jõuab alla
        if car[1] > screenY:

            while True:
                new_lane = random.choice(LANES)

                # kontroll, et samas rajas poleks teist autot liiga lähedal
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

        screen.blit(blue_car, (car[0], car[1]))

    # Skoor
    score_text = font.render("Skoor: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()