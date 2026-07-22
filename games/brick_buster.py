"""Brick Buster - break the bricks. Arrow keys to move, Esc quits."""
import pygame
from .palette import BLACK, WHITE, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    paddle = pygame.Rect(w // 2 - 40, h - 30, 80, 10)
    ball = pygame.Rect(w // 2, h // 2, 8, 8)
    vx, vy = 4, -4
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE]
    bricks = []
    bw, bh = (w - 40) // 10, 20
    for row in range(6):
        for col in range(10):
            bricks.append((pygame.Rect(20 + col * bw, 40 + row * bh, bw - 2, bh - 2), colors[row]))
    score = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 7
        if keys[pygame.K_RIGHT] and paddle.right < w:
            paddle.x += 7
        ball.x += vx
        ball.y += vy
        if ball.left <= 0 or ball.right >= w:
            vx = -vx
        if ball.top <= 0:
            vy = -vy
        if ball.colliderect(paddle) and vy > 0:
            vy = -vy
        for i, (rect, _) in enumerate(bricks):
            if ball.colliderect(rect):
                bricks.pop(i)
                vy = -vy
                score += 10
                break
        if ball.top > h or not bricks:
            return
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.rect(screen, WHITE, ball)
        for rect, color in bricks:
            pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)
