"""Sky Defense - click to intercept incoming missiles. Mouse aim + click, Esc quits."""
import pygame
import random
import math
from . import back
from .palette import BLACK, WHITE, GREEN, RED, YELLOW, CYAN, BROWN


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    cities = [pygame.Rect(x, h - 40, 60, 30) for x in range(60, w - 60, (w - 120) // 5)][:6]
    bases = [(w // 2, h - 20)]
    incoming = []
    outgoing = []
    explosions = []
    tick = 0
    score = 0
    spawn = 60
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if back.clicked(e, screen):
                return
            if e.type == pygame.MOUSEBUTTONDOWN and not back.rect(screen).collidepoint(e.pos):
                tx, ty = e.pos
                bx, by = bases[0]
                dx, dy = tx - bx, ty - by
                d = max(1, math.hypot(dx, dy))
                outgoing.append([bx, by, dx / d * 9, dy / d * 9, tx, ty])
        tick += 1
        spawn -= 1
        if spawn <= 0 and cities:
            spawn = random.randint(40, 90)
            sx = random.uniform(0, w)
            target = random.choice(cities + bases if isinstance(bases, list) else cities)
            tx = target.centerx if hasattr(target, "centerx") else target[0]
            ty = target.centery if hasattr(target, "centery") else target[1]
            dx, dy = tx - sx, ty
            d = max(1, math.hypot(dx, dy))
            incoming.append([sx, 0, dx / d * 2, dy / d * 2, tx, ty])
        for m in incoming:
            m[0] += m[2]
            m[1] += m[3]
        for m in outgoing[:]:
            m[0] += m[2]
            m[1] += m[3]
            if (m[0] - m[4]) ** 2 + (m[1] - m[5]) ** 2 < 100:
                explosions.append([m[4], m[5], 5, 30])
                outgoing.remove(m)
        for ex in explosions[:]:
            ex[2] += 2
            ex[3] -= 1
            if ex[3] <= 0:
                explosions.remove(ex)
        remaining = []
        for m in incoming:
            hit = False
            for ex in explosions:
                if (m[0] - ex[0]) ** 2 + (m[1] - ex[1]) ** 2 < ex[2] ** 2:
                    hit = True
                    score += 25
                    break
            if hit:
                continue
            if m[1] >= h - 40:
                explosions.append([m[0], m[1], 5, 20])
                cities = [c for c in cities if not c.collidepoint(m[0], m[1])]
                continue
            remaining.append(m)
        incoming = remaining
        if not cities:
            return
        screen.fill(BLACK)
        pygame.draw.rect(screen, BROWN, (0, h - 20, w, 20))
        for c in cities:
            pygame.draw.rect(screen, CYAN, c)
        pygame.draw.polygon(screen, GREEN, [(bases[0][0] - 20, h - 20), (bases[0][0] + 20, h - 20), (bases[0][0], h - 40)])
        for m in incoming:
            trail_start = (m[0] - m[2] * 5, m[1] - m[3] * 5)
            pygame.draw.line(screen, RED, trail_start, (m[0], m[1]), 2)
        for m in outgoing:
            pygame.draw.line(screen, YELLOW, (bases[0][0], bases[0][1]), (m[0], m[1]), 1)
            pygame.draw.circle(screen, WHITE, (int(m[0]), int(m[1])), 2)
        for ex in explosions:
            pygame.draw.circle(screen, YELLOW, (int(ex[0]), int(ex[1])), int(ex[2]), 2)
        screen.blit(font.render(f"Score {score}   Cities {len(cities)}", 1, WHITE), (10, 10))
        back.draw(screen)
        pygame.display.flip()
        clock.tick(60)
