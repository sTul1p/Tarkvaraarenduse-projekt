import pygame, sys, random, math
from collections import deque

TILE = 28
FPS  = 8

# 1=sein, .=pellet, p=power-up, G=kummituse algus, tühik=tühi käik
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
RED    = (220,20,20)
PINK   = (255,100,200)
SCARED = (30,30,200)
ORANGE = (255,160,0)
DOT_C  = (255,200,120)

# Animatsiooni kaadrid – suu avamisnurk kraadides
MOUTH_FRAMES = [5, 15, 25, 35, 25, 15]


def build_maze():
    """Ehita labirint: 1=sein, 0=tühi, 2=pellet, 3=power-up"""
    maze, ghosts = [], []
    for r, row in enumerate(MAZE_STR):
        line = []
        for c, ch in enumerate(row):
            if ch == '#':   line.append(1)
            elif ch == 'p': line.append(3)
            elif ch == 'G': line.append(0); ghosts.append((r, c))
            elif ch == ' ': line.append(0)   # tühi (kummituste kodu)
            else:           line.append(2)   # pellet
        maze.append(line)
    return maze, ghosts


def bfs_next(maze, start, goal):
    """Tagasta järgmine samm BFS lühimal teel."""
    if start == goal:
        return None
    q = deque([[start]])
    seen = {start}
    while q:
        path = q.popleft()
        r, c = path[-1]
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr, nc = r+dr, c+dc
            if (nr,nc) in seen: continue
            if not (0<=nr<ROWS and 0<=nc<COLS): continue
            if maze[nr][nc] == 1: continue
            seen.add((nr, nc))
            npath = path + [(nr, nc)]
            if (nr, nc) == goal:
                return npath[1]
            q.append(npath)
    return None


def draw_pacman_shape(surf, cx, cy, radius, direction, mouth_deg):
    """
    Joonistab Pac-Mani kiilulaadse kujuga (polygon + arc).
    cx, cy   – keskpunkti koordinaadid
    radius   – raadius pikslites
    direction – (dr, dc) liikumissuund
    mouth_deg – suu avamisnurk kraadides (0–45)

    Allikas: pygame.org/docs/ref/draw.html – polygon ja arc kasutus
    Inspiratsioon: github.com/hbokmann/Pacman – suuna-põhine joonistus
    """

    # Teisenda liikumissuund nurgaks radiaanides
    # pygame arc: 0° = parem, kasvab vastupäeva
    suuna_nurk = {
        (0, 1):  0,           # parem
        (0, -1): math.pi,     # vasak
        (-1, 0): math.pi / 2, # üles
        (1, 0):  math.pi * 3 / 2,  # alla
    }
    # Kui mäng alles algab (suund 0,0), näita paremale
    nurk = suuna_nurk.get(direction, 0)

    # Suu avamisnurk radiaanides
    suu = math.radians(mouth_deg)

    # Kaare algus- ja lõppnurk (suu vahel jäetud tühik)
    arc_algus = nurk + suu
    arc_lopp  = nurk + 2 * math.pi - suu

    # Loome polügooni: keskpunkt + kaare punktid
    punktid = [(cx, cy)]
    sammud = 30  # mitu punkti kaarel (sujuvus)
    for i in range(sammud + 1):
        t = arc_algus + (arc_lopp - arc_algus) * i / sammud
        px = cx + radius * math.cos(t)
        py = cy - radius * math.sin(t)  # y on ekraanil pööratud
        punktid.append((px, py))

    pygame.draw.polygon(surf, YELLOW, punktid)

    # Silm – väike must punkt
    silma_nurk = nurk + math.pi / 3   # 60° ülespoole suunast
    silma_r    = radius * 0.35
    sx = int(cx + silma_r * math.cos(silma_nurk))
    sy = int(cy - silma_r * math.sin(silma_nurk))
    pygame.draw.circle(surf, BLACK, (sx, sy), max(2, radius // 7))


class Pacman:
    def __init__(self):
        self.r, self.c = 17, 10
        self.dir  = (0, 1)   # algsuund: parem
        self.want = (0, 1)
        self.lives = 3
        self.score = 0
        self.power = 0       # power-up kaadrid järel
        self.anim  = 0       # animatsioonikaader (0–5)

    def handle(self, key):
        """Salvestab soovitud liikumissuuna klahvivajutuse põhjal."""
        d = {pygame.K_UP:(-1,0), pygame.K_DOWN:(1,0),
             pygame.K_LEFT:(0,-1), pygame.K_RIGHT:(0,1)}
        if key in d:
            self.want = d[key]

    def move(self, maze):
        """Liigutab Pac-Mani ja töötleb toidu söömise."""
        # Proovi soovitud suund, siis praegune
        for dr, dc in (self.want, self.dir):
            nr, nc = self.r + dr, (self.c + dc) % COLS
            if 0 <= nr < ROWS and maze[nr][nc] != 1:
                self.dir = (dr, dc)
                self.r, self.c = nr, nc
                break

        # Uuenda animatsioonikaadrit
        self.anim = (self.anim + 1) % len(MOUTH_FRAMES)

        # Söö pellet
        v = maze[self.r][self.c]
        if v == 2:
            maze[self.r][self.c] = 0
            self.score += 10
        elif v == 3:
            maze[self.r][self.c] = 0
            self.score += 50
            self.power = 30
        if self.power > 0:
            self.power -= 1

    def draw(self, surf):
        """Joonistab Pac-Mani animeeritud suuga kiilukaujuna."""
        cx = self.c * TILE + TILE // 2
        cy = self.r * TILE + TILE // 2
        mouth_deg = MOUTH_FRAMES[self.anim]
        draw_pacman_shape(surf, cx, cy, TILE // 2 - 1, self.dir, mouth_deg)


class Ghost:
    def __init__(self, r, c, color, predictive=False):
        self.r, self.c = r, c
        self.home = (r, c)
        self.color = color
        self.predictive = predictive
        self.scared = 0
        self.timer = 0

    def move(self, maze, pac):
        """Liigutab kummitust – hirmunud: juhuslik, normaalne: BFS."""
        self.timer += 1
        if self.timer < 2:
            return
        self.timer = 0

        if self.scared > 0:
            self.scared -= 1
            # Hirmunud: juhuslik liikumine
            opts = [(self.r+dr, self.c+dc)
                    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1))
                    if 0<=self.r+dr<ROWS and 0<=self.c+dc<COLS
                    and maze[self.r+dr][self.c+dc] != 1]
            if opts:
                self.r, self.c = random.choice(opts)
            return

        # Sihtmärk: Pinky sihib 3 sammu ette, Blinky otse mängijat
        if self.predictive:
            gr = max(0, min(ROWS-1, pac.r + pac.dir[0]*3))
            gc = max(0, min(COLS-1, pac.c + pac.dir[1]*3))
            goal = (gr, gc)
        else:
            goal = (pac.r, pac.c)

        nxt = bfs_next(maze, (self.r, self.c), goal)
        if nxt:
            self.r, self.c = nxt

    def draw(self, surf):
        """Joonistab kummituse – sinine kui hirmul, muidu oma värv."""
        x, y = self.c*TILE + TILE//2, self.r*TILE + TILE//2
        col = SCARED if self.scared > 0 else self.color
        # Keha – ümar ülaosa
        pygame.draw.circle(surf, col, (x, y-2), TILE//2-2)
        # Ristkülikukujuline alakeha
        pygame.draw.rect(surf, col, (x-TILE//2+2, y, TILE-4, TILE//2-2))
        # "Seelikusakid" – kolm väikest poolkaart allservas
        sakk_r = (TILE-4) // 6
        for i in range(3):
            sx = x - TILE//2 + 2 + sakk_r + i * sakk_r * 2
            sy = y + TILE//2 - 2
            pygame.draw.circle(surf, BLACK, (sx, sy), sakk_r)
        # Silmad (ainult normaalne olek)
        if self.scared == 0:
            for ex in (-4, 4):
                pygame.draw.circle(surf, WHITE, (x+ex, y-4), 3)
                pygame.draw.circle(surf, BLACK, (x+ex, y-4), 2)


def draw_maze(surf, maze):
    """Joonistab labiirindi seinad, pelletid ja power-upid."""
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c*TILE, r*TILE
            v = maze[r][c]
            if v == 1:
                pygame.draw.rect(surf, BLUE, (x,y,TILE,TILE))
                pygame.draw.rect(surf, (0,0,100), (x+2,y+2,TILE-4,TILE-4))
            elif v == 2:
                pygame.draw.circle(surf, DOT_C, (x+TILE//2, y+TILE//2), 3)
            elif v == 3:
                pygame.draw.circle(surf, ORANGE, (x+TILE//2, y+TILE//2), 7)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("PAC-MAN")
    clock    = pygame.time.Clock()
    font     = pygame.font.SysFont("Arial", 20, bold=True)
    font_big = pygame.font.SysFont("Arial", 40, bold=True)

    def reset():
        """Lähtestab mänguseisundi."""
        maze, g_pos = build_maze()
        pac = Pacman()
        g1 = g_pos[0] if len(g_pos) > 0 else (7, 8)
        g2 = g_pos[-1] if len(g_pos) > 1 else (7, 10)
        ghosts = [Ghost(g1[0], g1[1], RED),
                  Ghost(g2[0], g2[1], PINK, predictive=True)]
        return maze, pac, ghosts

    maze, pac, ghosts = reset()
    state = "play"

    while True:
        clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                pac.handle(ev.key)
                if ev.key == pygame.K_r and state != "play":
                    maze, pac, ghosts = reset()
                    state = "play"

        if state == "play":
            pac.move(maze)
            for g in ghosts:
                if pac.power > 0:
                    g.scared = max(g.scared, 20)
                g.move(maze, pac)
                # Kokkupõrge kummitusega
                if g.r == pac.r and g.c == pac.c:
                    if g.scared > 0:
                        # Pac-Man sööb kummituse – tagasi koju
                        g.r, g.c = g.home
                        g.scared = 0
                        pac.score += 200
                    else:
                        # Kaotab elu
                        pac.lives -= 1
                        pac.r, pac.c = 17, 10
                        pac.dir = pac.want = (0, 1)
                        if pac.lives <= 0:
                            state = "lose"
            # Võit: kõik pelletid ja power-upid söödud
            if all(v not in (2, 3) for row in maze for v in row):
                state = "win"

        # --- Joonistamine ---
        screen.fill(BLACK)
        draw_maze(screen, maze)
        pac.draw(screen)
        for g in ghosts:
            g.draw(screen)

        # HUD – skoor ja elud
        pygame.draw.rect(screen, BLACK, (0, ROWS*TILE, W, 48))
        screen.blit(font.render(f"Skoor: {pac.score}", True, WHITE), (10, ROWS*TILE+12))
        screen.blit(font.render("♥ " * pac.lives, True, RED), (W-130, ROWS*TILE+12))

        # Mängu lõpu sõnum
        if state != "play":
            msg = "VÕIT!" if state == "win" else "MÄNG LÄBI"
            col = YELLOW if state == "win" else RED
            t = font_big.render(msg, True, col)
            s = font.render(f"Skoor: {pac.score}  |  R = uuesti", True, WHITE)
            screen.blit(t, (W//2 - t.get_width()//2, H//2 - 40))
            screen.blit(s, (W//2 - s.get_width()//2, H//2 + 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()

# Allikad:
# https://www.pygame.org/docs/ref/draw.html   – polygon ja math kasutus kuju jaoks
# https://justtothepoint.com/code/pacman/     – suuna-põhine joonistusviis
# https://github.com/hbokmann/Pacman          – animatsiooni lähenemine