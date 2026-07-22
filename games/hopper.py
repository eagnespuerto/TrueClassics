"""Hopper - cross the road and river. Arrows to move, Esc quits."""
import pygame
import random
from . import back
from .palette import BLACK, WHITE, GREEN, LIME, RED, YELLOW, BLUE, BROWN, GRAY


ROWS = 15
HEADER = 40  # pixels reserved at the top for the score


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    cell = max(16, min(32, (h - HEADER) // ROWS))
    cols = w // cell
    board_w = cols * cell
    ox = (w - board_w) // 2
    oy = HEADER + (h - HEADER - ROWS * cell) // 2
    px, py = cols // 2, ROWS - 1
    cars = []
    logs = []
    for row in range(9, 13):
        speed = random.choice([-1, 1]) * random.randint(2, 4)
        for i in range(3):
            cars.append([row, i * (board_w // 3), speed])
    for row in range(3, 7):
        speed = random.choice([-1, 1]) * random.randint(1, 3)
        for i in range(2):
            logs.append([row, i * (board_w // 2), speed, 3 * cell])
    score = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if back.clicked(e, screen):
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_LEFT and px > 0:
                    px -= 1
                elif e.key == pygame.K_RIGHT and px < cols - 1:
                    px += 1
                elif e.key == pygame.K_UP and py > 0:
                    py -= 1
                    score += 10
                elif e.key == pygame.K_DOWN and py < ROWS - 1:
                    py += 1
        for c in cars:
            c[1] = (c[1] + c[2]) % board_w
        for lg in logs:
            lg[1] = (lg[1] + lg[2]) % board_w
        player_px = px * cell
        for row, x, spd in cars:
            if row == py and x <= player_px < x + cell:
                return
        on_log = False
        for row, x, spd, length in logs:
            if row != py:
                continue
            end = x + length
            if x <= player_px < end or (end > board_w and player_px < end % board_w):
                on_log = True
                px = int(((player_px + spd) % board_w) // cell)
                break
        if 3 <= py <= 6 and not on_log:
            return
        if py == 0:
            score += 100
            py = ROWS - 1
        screen.fill(BLACK)
        for y in range(ROWS):
            rect = (ox, oy + y * cell, board_w, cell)
            if y == 0:
                pygame.draw.rect(screen, GREEN, rect)
            elif 3 <= y <= 6:
                pygame.draw.rect(screen, BLUE, rect)
            elif y in (7, 8):
                pygame.draw.rect(screen, LIME, rect)
            elif 9 <= y <= 12:
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, LIME, rect)
        for row, x, spd, length in logs:
            pygame.draw.rect(screen, BROWN, (ox + x, oy + row * cell + 4, length, cell - 8))
            if x + length > board_w:
                pygame.draw.rect(screen, BROWN, (ox, oy + row * cell + 4, (x + length) % board_w, cell - 8))
        for row, x, spd in cars:
            pygame.draw.rect(screen, RED if spd > 0 else YELLOW,
                             (ox + x, oy + row * cell + 4, cell - 4, cell - 8))
        pygame.draw.rect(screen, LIME,
                         (ox + px * cell + 4, oy + py * cell + 4, cell - 8, cell - 8))
        screen.blit(font.render(f"Score {score}", True, WHITE), (10, 10))
        back.draw(screen)
        pygame.display.flip()
        clock.tick(30)
