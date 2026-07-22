"""Chomper - eat dots in a maze, avoid ghosts. Arrows to move, Esc quits."""
import pygame
import random
from .palette import BLACK, WHITE, YELLOW, RED, PINK, CYAN, ORANGE, BLUE


CELL = 18

MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "     #.##          ##.#     ",
    "######.## ######## ##.######",
    "#........ #      # ........#",
    "######.## ######## ##.######",
    "     #.##          ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    grid = [list(row) for row in MAZE]
    rows, cols = len(grid), len(grid[0])
    ox = (w - cols * CELL) // 2
    oy = (h - rows * CELL) // 2 + 20
    px, py = 13, 15
    dx, dy = 0, 0
    ghosts = [(13, 9, RED), (14, 9, PINK), (13, 10, CYAN), (14, 10, ORANGE)]
    score = 0
    tick = 0
    gtick = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                if e.key == pygame.K_RIGHT:
                    dx, dy = 1, 0
                if e.key == pygame.K_UP:
                    dx, dy = 0, -1
                if e.key == pygame.K_DOWN:
                    dx, dy = 0, 1
        tick += 1
        if tick >= 8:
            tick = 0
            nx, ny = (px + dx) % cols, (py + dy) % rows
            if grid[ny][nx] != "#":
                px, py = nx, ny
                if grid[py][px] == ".":
                    grid[py][px] = " "
                    score += 10
        gtick += 1
        if gtick >= 12:
            gtick = 0
            new_ghosts = []
            for gx, gy, c in ghosts:
                choices = []
                for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = (gx + ddx) % cols, (gy + ddy) % rows
                    if grid[ny][nx] != "#":
                        choices.append((nx, ny))
                if choices:
                    if random.random() < 0.7:
                        choices.sort(key=lambda p: abs(p[0] - px) + abs(p[1] - py))
                        nx, ny = choices[0]
                    else:
                        nx, ny = random.choice(choices)
                    new_ghosts.append((nx, ny, c))
                else:
                    new_ghosts.append((gx, gy, c))
            ghosts = new_ghosts
        for gx, gy, _ in ghosts:
            if gx == px and gy == py:
                return
        if not any("." in row for row in grid):
            return
        screen.fill(BLACK)
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                rx, ry = ox + x * CELL, oy + y * CELL
                if ch == "#":
                    pygame.draw.rect(screen, BLUE, (rx, ry, CELL, CELL))
                elif ch == ".":
                    pygame.draw.circle(screen, WHITE, (rx + CELL // 2, ry + CELL // 2), 3)
        pygame.draw.circle(screen, YELLOW, (ox + px * CELL + CELL // 2, oy + py * CELL + CELL // 2), CELL // 2 - 2)
        for gx, gy, c in ghosts:
            pygame.draw.rect(screen, c, (ox + gx * CELL + 2, oy + gy * CELL + 2, CELL - 4, CELL - 4))
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)
