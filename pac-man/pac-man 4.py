import pygame
import sys
import random

TILE = 28
FPS = 8

MAZE_STR = [
    "#####################",
    "#p..#.......#...#..p#",
    "#.#.#.#####.#.#.#.#.#",
    "#.#...........#...#.#",
    "#.#.#...###.#.#.#.#.#",
    "#...#.........#...#.#",
    "###.###.###.###.###.#",
    "#...#.. G G ..#...#.#",
    "#.#.#.#######.#.#.#.#",
    "#.#...........#...#.#",
    "#.#.#.#######.#.#.#.#",
    "#...#...........#...#",
    "###.###.###.###.###.#",
    "#...#...............#",
    "#.#.#.#.###.#.#.#.#.#",
    "#p............#...#p#",
    "#.#.#.#####.#.#.#.#.#",
    "#...#.......#...#...#",
    "#.###########.###.#.#",
    "#...................#",
    "#####################",
]

ROWS = len(MAZE_STR)
COLS = len(MAZE_STR[0])

W = COLS * TILE
H = ROWS * TILE

BLACK = (0, 0, 0)
BLUE = (0, 0, 180)
RED = (220, 20, 20)
PINK = (255, 100, 200)
ORANGE = (255, 160, 0)


def build_maze():
    maze = []
    ghosts = []

    for r, row in enumerate(MAZE_STR):
        line = []

        for c, ch in enumerate(row):
            if ch == '#':
                line.append(1)
            else:
                line.append(0)

            if ch == 'G':
                ghosts.append((r, c))

        maze.append(line)

    return maze, ghosts


class Ghost:
    def __init__(self, r, c, color):
        self.r = r
        self.c = c
        self.color = color
        self.timer = 0

    def move(self, maze):
        self.timer += 1

        if self.timer < 2:
            return

        self.timer = 0

        options = []

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr = self.r + dr
            nc = self.c + dc

            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] != 1:
                    options.append((nr, nc))

        if options:
            self.r, self.c = random.choice(options)

    def draw(self, surf):
        x = self.c * TILE + TILE // 2
        y = self.r * TILE + TILE // 2

        pygame.draw.circle(surf, self.color, (x, y - 2), TILE // 2 - 2)
        pygame.draw.rect(
            surf,
            self.color,
            (x - TILE // 2 + 2, y, TILE - 4, TILE // 2 - 2)
        )

        for ex in (-4, 4):
            pygame.draw.circle(surf, (255,255,255), (x+ex, y-4), 3)
            pygame.draw.circle(surf, BLACK, (x+ex, y-4), 2)


def draw_maze(screen, maze):
    for r in range(ROWS):
        for c in range(COLS):

            if maze[r][c] == 1:
                x = c * TILE
                y = r * TILE

                pygame.draw.rect(screen, BLUE, (x, y, TILE, TILE))
                pygame.draw.rect(
                    screen,
                    (0,0,100),
                    (x+2, y+2, TILE-4, TILE-4)
                )


def main():
    pygame.init()

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pac-Man - Osa 1")

    clock = pygame.time.Clock()

    maze, g_pos = build_maze()

    colors = [RED, PINK, ORANGE]

    ghosts = []

    for i, pos in enumerate(g_pos):
        ghosts.append(
            Ghost(pos[0], pos[1], colors[i % len(colors)])
        )

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for ghost in ghosts:
            ghost.move(maze)

        screen.fill(BLACK)

        draw_maze(screen, maze)

        for ghost in ghosts:
            ghost.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()