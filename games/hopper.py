"""Hopper - cross the road and river. Arrows to move, Esc quits."""
import pygame
import random
from .palette import BLACK, WHITE, GREEN, LIME, RED, YELLOW, BLUE, BROWN, GRAY


CELL = 32


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    cols = w // CELL
    rows = 15
    ox = (w - cols * CELL) // 2
    oy = (h - rows * CELL) // 2
    px, py = cols // 2, rows - 1
    cars = []
    logs = []
    for row in range(9, 13):
        speed = random.choice([-1, 1]) * random.randint(2, 4)
        for i in range(3):
            cars.append([row, i * (cols * CELL // 3), speed])
    for row in range(3, 7):
        speed = random.choice([-1, 1]) * random.randint(1, 3)
        for i in range(2):
            logs.append([row, i * (cols * CELL // 2), speed, 3 * CELL])
    score = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_LEFT and px > 0:
                    px -= 1
                if e.key == pygame.K_RIGHT and px < cols - 1:
                    px += 1
                if e.key == pygame.K_UP:
                    py -= 1
                    score += 10
                if e.key == pygame.K_DOWN and py < rows - 1:
                    py += 1
        for c in cars:
            c[1] = (c[1] + c[2]) % (cols * CELL)
        for lg in logs:
            lg[1] = (lg[1] + lg[2]) % (cols * CELL)
        player_px = px * CELL
        player_py = py * CELL
        for row, x, spd in cars:
            if row == py and x <= player_px < x + CELL:
                return
        on_log = False
        for row, x, spd, length in logs:
            if row == py:
                if x <= player_px < x + length or (x + length > cols * CELL and player_px < (x + length) % (cols * CELL)):
                    on_log = True
                    px = int(((player_px + spd) % (cols * CELL)) // CELL)
                    break
        if 3 <= py <= 6 and not on_log:
            return
        if py < 0:
            return
        if py == 0:
            score += 100
            py = rows - 1
        screen.fill(BLACK)
        for y in range(rows):
            rect = (ox, oy + y * CELL, cols * CELL, CELL)
            if y == 0:
                pygame.draw.rect(screen, GREEN, rect)
            elif 3 <= y <= 6:
                pygame.draw.rect(screen, BLUE, rect)
            elif y == 7 or y == 8:
                pygame.draw.rect(screen, LIME, rect)
            elif 9 <= y <= 12:
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, LIME, rect)
        for row, x, spd, length in logs:
            pygame.draw.rect(screen, BROWN, (ox + x, oy + row * CELL + 4, length, CELL - 8))
            if x + length > cols * CELL:
                pygame.draw.rect(screen, BROWN, (ox, oy + row * CELL + 4, (x + length) % (cols * CELL), CELL - 8))
        for row, x, spd in cars:
            pygame.draw.rect(screen, RED if spd > 0 else YELLOW, (ox + x, oy + row * CELL + 4, CELL - 4, CELL - 8))
        pygame.draw.rect(screen, LIME, (ox + px * CELL + 4, oy + py * CELL + 4, CELL - 8, CELL - 8))
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(30)
