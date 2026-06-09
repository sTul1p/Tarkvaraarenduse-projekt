import pygame
import random
import sys

pygame.init()

TILE = 30
ROWS = 15
COLS = 15

WIDTH = COLS * TILE
HEIGHT = ROWS * TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

maze = [
    [1 if r == 0 or c == 0 or r == ROWS-1 or c == COLS-1 else 0
     for c in range(COLS)]
    for r in range(ROWS)
]

pac_r, pac_c = 1, 1
ghost_r, ghost_c = 10, 10

while True:
    clock.tick(8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            nr, nc = pac_r, pac_c

            if event.key == pygame.K_UP:
                nr -= 1
            elif event.key == pygame.K_DOWN:
                nr += 1
            elif event.key == pygame.K_LEFT:
                nc -= 1
            elif event.key == pygame.K_RIGHT:
                nc += 1

            if maze[nr][nc] == 0:
                pac_r, pac_c = nr, nc

    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    random.shuffle(moves)

    for dr, dc in moves:
        nr = ghost_r + dr
        nc = ghost_c + dc

        if maze[nr][nc] == 0:
            ghost_r, ghost_c = nr, nc
            break

    if pac_r == ghost_r and pac_c == ghost_c:
        print("Mäng läbi!")
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (c*TILE, r*TILE, TILE, TILE)
                )

    pygame.draw.circle(
        screen,
        YELLOW,
        (pac_c*TILE + TILE//2,
         pac_r*TILE + TILE//2),
        TILE//2 - 2
    )

    pygame.draw.circle(
        screen,
        RED,
        (ghost_c*TILE + TILE//2,
         ghost_r*TILE + TILE//2),
        TILE//2 - 2
    )

    pygame.display.flip()

    #https://github.com/hbokmann/Pacman