import pygame, sys, random
pygame.init()

#Ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Auto mäng")
clock = pygame.time.Clock()

#Pildid
bg = pygame.image.load("bg_rally.jpg")
bg = pygame.transform.scale(bg, [screenX, screenY])

red_car = pygame.image.load("f1_red.png")
red_car = pygame.transform.scale(red_car, [60, 100])

blue_car = pygame.image.load("f1_blue.png")
blue_car = pygame.transform.scale(blue_car, [60, 100])

#Piirid
ROAD_LEFT = 140
ROAD_RIGHT = 410

#Punane auto
redX = screenX // 2 - 30
redY = screenY - 120

#Sinised autod
NUM_BLUE = 3
blue_cars = []
for i in range(NUM_BLUE):
    bx = random.randint(ROAD_LEFT, ROAD_RIGHT - 60)
    by = random.randint(-400, -100)
    speed = random.randint(3, 6)
    blue_cars.append([bx, by, speed])

#Skoor
score = 0
font = pygame.font.SysFont("Arial", 30)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #Taust
    screen.blit(bg, (0, 0))

    #Skoor ekraanil
    score_text = font.render("Skoor: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    #Punane auto
    screen.blit(red_car, (redX, redY))

    #Sinised autod
    for car in blue_cars:
        car[1] += car[2]

        if car[1] > screenY:
            car[0] = random.randint(ROAD_LEFT, ROAD_RIGHT - 60)
            car[1] = random.randint(-300, -60)
            car[2] = random.randint(3, 6)
            score += 1

        screen.blit(blue_car, (car[0], car[1]))

    pygame.display.flip()

pygame.quit()