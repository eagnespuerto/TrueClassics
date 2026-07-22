"""Paddle Duel - two-paddle bouncing ball. W/S left, Up/Down right. Esc quits."""
import pygame
from .palette import BLACK, WHITE, CYAN, RED


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 28, bold=True)
    left = pygame.Rect(20, h // 2 - 40, 8, 80)
    right = pygame.Rect(w - 28, h // 2 - 40, 8, 80)
    ball = pygame.Rect(w // 2 - 4, h // 2 - 4, 8, 8)
    vx, vy = 4, 3
    ls, rs = 0, 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left.top > 0:
            left.y -= 6
        if keys[pygame.K_s] and left.bottom < h:
            left.y += 6
        if keys[pygame.K_UP] and right.top > 0:
            right.y -= 6
        if keys[pygame.K_DOWN] and right.bottom < h:
            right.y += 6
        ball.x += vx
        ball.y += vy
        if ball.top <= 0 or ball.bottom >= h:
            vy = -vy
        if ball.colliderect(left) and vx < 0:
            vx = -vx
        if ball.colliderect(right) and vx > 0:
            vx = -vx
        if ball.left <= 0:
            rs += 1
            ball.center = (w // 2, h // 2)
            vx = 4
        if ball.right >= w:
            ls += 1
            ball.center = (w // 2, h // 2)
            vx = -4
        screen.fill(BLACK)
        pygame.draw.rect(screen, CYAN, left)
        pygame.draw.rect(screen, RED, right)
        pygame.draw.rect(screen, WHITE, ball)
        for y in range(0, h, 20):
            pygame.draw.rect(screen, WHITE, (w // 2 - 1, y, 2, 10))
        screen.blit(font.render(f"{ls}", 1, WHITE), (w // 4, 10))
        screen.blit(font.render(f"{rs}", 1, WHITE), (3 * w // 4, 10))
        pygame.display.flip()
        clock.tick(60)
