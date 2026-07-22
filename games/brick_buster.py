"""Brick Buster - break the bricks. Left/Right move, Space launches ball, Esc quits.

Ball starts glued to the paddle so the player can position first. Three lives:
each miss re-attaches the ball; running out of lives ends the round.
"""
import pygame
from . import back
from .palette import BLACK, WHITE, GRAY, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE


PADDLE_W, PADDLE_H = 100, 12
BALL_SIZE = 10
BALL_SPEED = 5
PADDLE_SPEED = 8


def _spawn_bricks(w):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE]
    bricks = []
    bw = (w - 40) // 10
    bh = 20
    for row in range(6):
        for col in range(10):
            bricks.append((pygame.Rect(20 + col * bw, 50 + row * bh, bw - 2, bh - 2),
                           colors[row]))
    return bricks


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 18, bold=True)
    big_font = pygame.font.SysFont("monospace", 22, bold=True)

    paddle = pygame.Rect(w // 2 - PADDLE_W // 2, h - 30, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
    vx, vy = BALL_SPEED, -BALL_SPEED
    stuck = True
    lives = 3
    score = 0
    bricks = _spawn_bricks(w)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if back.clicked(e, screen):
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE and stuck:
                    stuck = False
                    vx, vy = BALL_SPEED, -BALL_SPEED

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < w:
            paddle.x += PADDLE_SPEED

        if stuck:
            ball.centerx = paddle.centerx
            ball.bottom = paddle.top - 1
        else:
            ball.x += vx
            ball.y += vy
            if ball.left <= 0:
                ball.left = 0
                vx = -vx
            if ball.right >= w:
                ball.right = w
                vx = -vx
            if ball.top <= 0:
                ball.top = 0
                vy = -vy
            if ball.colliderect(paddle) and vy > 0:
                vy = -vy
                offset = (ball.centerx - paddle.centerx) / (PADDLE_W / 2)
                vx = int(BALL_SPEED * max(-1.0, min(1.0, offset)) * 1.2)
                if vx == 0:
                    vx = 1 if offset >= 0 else -1
            for i, (rect, _) in enumerate(bricks):
                if ball.colliderect(rect):
                    bricks.pop(i)
                    vy = -vy
                    score += 10
                    break
            if ball.top > h:
                lives -= 1
                stuck = True
                paddle.x = w // 2 - PADDLE_W // 2

        if lives <= 0 or not bricks:
            return

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.rect(screen, WHITE, ball)
        for rect, color in bricks:
            pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(f"Score {score}   Lives {lives}", True, WHITE), (10, 10))
        if stuck:
            msg = big_font.render("Press SPACE to launch", True, YELLOW)
            screen.blit(msg, ((w - msg.get_width()) // 2, h // 2))
            hint = font.render("Left / Right to move paddle", True, GRAY)
            screen.blit(hint, ((w - hint.get_width()) // 2, h // 2 + 30))
        back.draw(screen)
        pygame.display.flip()
        clock.tick(60)
