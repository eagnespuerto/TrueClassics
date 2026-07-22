"""Rock Storm - shoot the rocks in space. Left/Right turn, Up thrust, Space fire, Esc quits."""
import pygame
import math
import random
from . import back
from .palette import BLACK, WHITE, GRAY, YELLOW


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    ship = [w / 2, h / 2, 0.0, 0.0, 0.0]  # x, y, vx, vy, angle
    bullets = []
    rocks = []
    safe_dist = 120  # keep initial rocks clear of the ship spawn
    for _ in range(5):
        while True:
            rx, ry = random.uniform(0, w), random.uniform(0, h)
            if (rx - ship[0]) ** 2 + (ry - ship[1]) ** 2 >= safe_dist ** 2:
                break
        rocks.append([rx, ry,
                      random.uniform(-2, 2), random.uniform(-2, 2), 30])
    score = 0
    cooldown = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if back.clicked(e, screen):
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE and cooldown == 0:
                    bullets.append([ship[0], ship[1],
                                    math.cos(ship[4]) * 8, math.sin(ship[4]) * 8, 60])
                    cooldown = 12
        if cooldown > 0:
            cooldown -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship[4] -= 0.08
        if keys[pygame.K_RIGHT]:
            ship[4] += 0.08
        if keys[pygame.K_UP]:
            ship[2] += math.cos(ship[4]) * 0.15
            ship[3] += math.sin(ship[4]) * 0.15
        ship[0] = (ship[0] + ship[2]) % w
        ship[1] = (ship[1] + ship[3]) % h
        ship[2] *= 0.99
        ship[3] *= 0.99
        for b in bullets:
            b[0] = (b[0] + b[2]) % w
            b[1] = (b[1] + b[3]) % h
            b[4] -= 1
        bullets = [b for b in bullets if b[4] > 0]
        for r in rocks:
            r[0] = (r[0] + r[2]) % w
            r[1] = (r[1] + r[3]) % h
        new_rocks = []
        for r in rocks:
            hit = False
            for b in bullets[:]:
                if (b[0] - r[0]) ** 2 + (b[1] - r[1]) ** 2 < r[4] ** 2:
                    bullets.remove(b)
                    score += 20
                    hit = True
                    if r[4] > 15:
                        for _ in range(2):
                            new_rocks.append([r[0], r[1],
                                              random.uniform(-3, 3), random.uniform(-3, 3), r[4] // 2])
                    break
            if not hit:
                new_rocks.append(r)
        rocks = new_rocks
        for r in rocks:
            if (ship[0] - r[0]) ** 2 + (ship[1] - r[1]) ** 2 < (r[4] + 8) ** 2:
                return
        if not rocks:
            return
        screen.fill(BLACK)
        pts = []
        for a in (0, 2.4, -2.4):
            ang = ship[4] + a
            pts.append((ship[0] + math.cos(ang) * 12, ship[1] + math.sin(ang) * 12))
        pygame.draw.polygon(screen, WHITE, pts, 1)
        for b in bullets:
            pygame.draw.circle(screen, YELLOW, (int(b[0]), int(b[1])), 2)
        for r in rocks:
            pygame.draw.circle(screen, GRAY, (int(r[0]), int(r[1])), int(r[4]), 2)
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        back.draw(screen)
        pygame.display.flip()
        clock.tick(60)
