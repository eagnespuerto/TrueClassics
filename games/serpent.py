"""Serpent - eat the apple, don't hit yourself. Arrows to steer, Esc quits."""
import pygame
import random
from . import back
from .palette import BLACK, WHITE, GREEN, RED, DGRAY


CELL = 20


def run(screen, clock):
    w, h = screen.get_size()
    cols, rows = w // CELL, h // CELL
    font = pygame.font.SysFont("monospace", 20, bold=True)
    snake = [(cols // 2, rows // 2)]
    dx, dy = 1, 0
    apple = (random.randrange(cols), random.randrange(rows))
    tick = 0
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
                if e.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif e.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0
                elif e.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif e.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
        tick += 1
        if tick >= 8:
            tick = 0
            hx, hy = snake[0]
            nx, ny = (hx + dx) % cols, (hy + dy) % rows
            eating = (nx, ny) == apple
            # Tail vacates unless we're eating, so exclude it from the
            # self-collision check when it will be popped this tick.
            body = snake if eating else snake[:-1]
            if (nx, ny) in body:
                return
            snake.insert(0, (nx, ny))
            if eating:
                score += 1
                while True:
                    apple = (random.randrange(cols), random.randrange(rows))
                    if apple not in snake:
                        break
            else:
                snake.pop()
        screen.fill(BLACK)
        for x in range(0, w, CELL):
            pygame.draw.line(screen, DGRAY, (x, 0), (x, h))
        for y in range(0, h, CELL):
            pygame.draw.line(screen, DGRAY, (0, y), (w, y))
        pygame.draw.rect(screen, RED, (apple[0] * CELL, apple[1] * CELL, CELL - 1, CELL - 1))
        for i, (sx, sy) in enumerate(snake):
            pygame.draw.rect(screen, GREEN if i else WHITE, (sx * CELL, sy * CELL, CELL - 1, CELL - 1))
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        back.draw(screen)
        pygame.display.flip()
        clock.tick(60)
