import pygame
import sys

pygame.init()

TILE = 30
ROWS, COLS = 15, 15
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

maze = [
    [1 if r == 0 or c == 0 or r == ROWS-1 or c == COLS-1 else 0
     for c in range(COLS)]
    for r in range(ROWS)
]

pellets = {(r, c) for r in range(1, ROWS-1)
                  for c in range(1, COLS-1)}

pac_r, pac_c = 1, 1
score = 0

while True:
    clock.tick(10)

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

    if (pac_r, pac_c) in pellets:
        pellets.remove((pac_r, pac_c))
        score += 10

    screen.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):
            x = c * TILE
            y = r * TILE

            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, TILE, TILE))

    for r, c in pellets:
        pygame.draw.circle(
            screen,
            WHITE,
            (c*TILE + TILE//2, r*TILE + TILE//2),
            3
        )

    pygame.draw.circle(
        screen,
        YELLOW,
        (pac_c*TILE + TILE//2, pac_r*TILE + TILE//2),
        TILE//2 - 2
    )

    pygame.display.set_caption(f"Skoor: {score}")
    pygame.display.flip()

    #https://www.pygame.org/docs/