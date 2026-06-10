import pygame, sys, math

TILE = 28
FPS  = 8

MAZE_STR = [
    "#####################",
    "#p..#.......#...#..p#",
    "#.#.#.#####.#.#.#.#.#",
    "#.#...........#...#.#",
    "#.#.#...###.#.#.#.#.#",
    "#...#.........#...#.#",
    "###.###.###.###.###.#",
    "#...#.. GGG ..#...#.#",
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
H = ROWS * TILE + 48

BLACK  = (0,0,0)
BLUE   = (0,0,180)
YELLOW = (255,220,0)
WHITE  = (255,255,255)

MOUTH_FRAMES = [5, 15, 25, 35, 25, 15]


def build_maze():
    """Ehita labürint: 1=sein, 0=tühi käik"""
    maze = []
    for row in MAZE_STR:
        line = []
        for ch in row:
            if ch == '#':
                line.append(1)
            else:
                line.append(0)   # kõik muu on tühi (pelletid, G, tühik)
        maze.append(line)
    return maze


def draw_pacman_shape(surf, cx, cy, radius, direction, mouth_deg):
    """
    Joonistab Pac-Mani kiilulaadse kujuga (polygon).
    Allikas: pygame.org/docs/ref/draw.html
    """
    suuna_nurk = {
        (0, 1):  0,
        (0, -1): math.pi,
        (-1, 0): math.pi / 2,
        (1, 0):  math.pi * 3 / 2,
    }
    nurk = suuna_nurk.get(direction, 0)
    suu  = math.radians(mouth_deg)
    arc_algus = nurk + suu
    arc_lopp  = nurk + 2 * math.pi - suu
    punktid = [(cx, cy)]
    sammud = 30
    for i in range(sammud + 1):
        t = arc_algus + (arc_lopp - arc_algus) * i / sammud
        px = cx + radius * math.cos(t)
        py = cy - radius * math.sin(t)
        punktid.append((px, py))
    pygame.draw.polygon(surf, YELLOW, punktid)
    silma_nurk = nurk + math.pi / 3
    silma_r    = radius * 0.35
    sx = int(cx + silma_r * math.cos(silma_nurk))
    sy = int(cy - silma_r * math.sin(silma_nurk))
    pygame.draw.circle(surf, BLACK, (sx, sy), max(2, radius // 7))


class Pacman:
    def __init__(self):
        self.r, self.c = 17, 10
        self.dir  = (0, 1)
        self.want = (0, 1)
        self.anim = 0

    def handle(self, key):
        """Salvestab soovitud liikumissuuna klahvivajutuse põhjal."""
        d = {pygame.K_UP:(-1,0), pygame.K_DOWN:(1,0),
             pygame.K_LEFT:(0,-1), pygame.K_RIGHT:(0,1)}
        if key in d:
            self.want = d[key]

    def move(self, maze):
        """Liigutab Pac-Mani, kontrollib seintega kokkupõrget."""
        for dr, dc in (self.want, self.dir):
            nr, nc = self.r + dr, (self.c + dc) % COLS   # tunnel
            if 0 <= nr < ROWS and maze[nr][nc] != 1:
                self.dir = (dr, dc)
                self.r, self.c = nr, nc
                break
        self.anim = (self.anim + 1) % len(MOUTH_FRAMES)

    def draw(self, surf):
        cx = self.c * TILE + TILE // 2
        cy = self.r * TILE + TILE // 2
        draw_pacman_shape(surf, cx, cy, TILE // 2 - 1, self.dir, MOUTH_FRAMES[self.anim])


def draw_maze(surf, maze):
    """Joonistab labürindi seinad."""
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                x, y = c*TILE, r*TILE
                pygame.draw.rect(surf, BLUE, (x,y,TILE,TILE))
                pygame.draw.rect(surf, (0,0,100), (x+2,y+2,TILE-4,TILE-4))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("PAC-MAN V1 – Liikumine")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("Arial", 20, bold=True)

    maze = build_maze()
    pac  = Pacman()

    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                pac.handle(ev.key)

        pac.move(maze)

        screen.fill(BLACK)
        draw_maze(screen, maze)
        pac.draw(screen)

        pygame.draw.rect(screen, BLACK, (0, ROWS*TILE, W, 48))
        screen.blit(font.render("V1: Labürint + liikumine  |  Nooleklahvid", True, WHITE),
                    (10, ROWS*TILE+12))

        pygame.display.flip()


if __name__ == "__main__":
    main()