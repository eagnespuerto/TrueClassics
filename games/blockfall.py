"""Blockfall - falling tetromino puzzle. Left/Right move, Up rotate, Down soft-drop, Esc quits."""
import pygame
import random
from .palette import BLACK, WHITE, GRAY, CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE


COLS, ROWS = 10, 20

SHAPES = [
    ([[1, 1, 1, 1]], CYAN),
    ([[1, 1], [1, 1]], YELLOW),
    ([[0, 1, 0], [1, 1, 1]], PURPLE),
    ([[0, 1, 1], [1, 1, 0]], GREEN),
    ([[1, 1, 0], [0, 1, 1]], RED),
    ([[1, 0, 0], [1, 1, 1]], BLUE),
    ([[0, 0, 1], [1, 1, 1]], ORANGE),
]


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def collide(grid, shape, ox, oy):
    for y, row in enumerate(shape):
        for x, v in enumerate(row):
            if not v:
                continue
            nx, ny = ox + x, oy + y
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return True
            if ny >= 0 and grid[ny][nx]:
                return True
    return False


def merge(grid, shape, ox, oy, color):
    for y, row in enumerate(shape):
        for x, v in enumerate(row):
            if v and oy + y >= 0:
                grid[oy + y][ox + x] = color


def clear_rows(grid):
    kept = [row for row in grid if not all(row)]
    cleared = ROWS - len(kept)
    for _ in range(cleared):
        kept.insert(0, [0] * COLS)
    return kept, cleared


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    # Adaptive cell size: leave a 40 px header for the score.
    CELL = max(8, min((h - 50) // ROWS, (w - 40) // (COLS + 6)))
    ox_board = (w - COLS * CELL) // 2
    oy_board = 40 + (h - 40 - ROWS * CELL) // 2
    grid = [[0] * COLS for _ in range(ROWS)]
    shape, color = random.choice(SHAPES)
    shape = [row[:] for row in shape]
    px, py = COLS // 2 - len(shape[0]) // 2, 0
    fall = 0
    score = 0
    while True:
        drop_speed = max(6, 30 - score // 200)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_LEFT and not collide(grid, shape, px - 1, py):
                    px -= 1
                if e.key == pygame.K_RIGHT and not collide(grid, shape, px + 1, py):
                    px += 1
                if e.key == pygame.K_UP:
                    ns = rotate(shape)
                    if not collide(grid, ns, px, py):
                        shape = ns
                if e.key == pygame.K_DOWN and not collide(grid, shape, px, py + 1):
                    py += 1
        fall += 1
        if fall >= drop_speed:
            fall = 0
            if not collide(grid, shape, px, py + 1):
                py += 1
            else:
                merge(grid, shape, px, py, color)
                grid, cleared = clear_rows(grid)
                score += [0, 40, 100, 300, 1200][cleared]
                shape, color = random.choice(SHAPES)
                shape = [row[:] for row in shape]
                px, py = COLS // 2 - len(shape[0]) // 2, 0
                if collide(grid, shape, px, py):
                    return
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, (ox_board - 2, oy_board - 2, COLS * CELL + 4, ROWS * CELL + 4), 2)
        for y in range(ROWS):
            for x in range(COLS):
                if grid[y][x]:
                    pygame.draw.rect(screen, grid[y][x], (ox_board + x * CELL, oy_board + y * CELL, CELL - 1, CELL - 1))
        for y, row in enumerate(shape):
            for x, v in enumerate(row):
                if v:
                    pygame.draw.rect(screen, color, (ox_board + (px + x) * CELL, oy_board + (py + y) * CELL, CELL - 1, CELL - 1))
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)
