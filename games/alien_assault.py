"""Alien Assault - shoot invaders. Arrows to move, Space to fire, Esc quits."""
import pygame
import random
from .palette import BLACK, WHITE, GREEN, YELLOW, CYAN


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    player = pygame.Rect(w // 2 - 20, h - 40, 40, 12)
    bullets, ebullets = [], []
    aliens = []
    for r in range(4):
        for c in range(10):
            aliens.append(pygame.Rect(60 + c * 55, 60 + r * 40, 30, 20))
    ax_dir = 1
    fall = 0
    score = 0
    cooldown = 0
    efire = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE and cooldown == 0:
                    bullets.append(pygame.Rect(player.centerx - 2, player.top, 4, 10))
                    cooldown = 15
        if cooldown > 0:
            cooldown -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 6
        if keys[pygame.K_RIGHT] and player.right < w:
            player.x += 6
        for b in bullets:
            b.y -= 8
        bullets = [b for b in bullets if b.bottom > 0]
        fall += 1
        if fall >= 30:
            fall = 0
            edge = False
            for a in aliens:
                a.x += ax_dir * 8
                if a.right >= w or a.left <= 0:
                    edge = True
            if edge:
                ax_dir = -ax_dir
                for a in aliens:
                    a.y += 12
        efire += 1
        if efire >= 45 and aliens:
            efire = 0
            shooter = random.choice(aliens)
            ebullets.append(pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 10))
        for b in ebullets:
            b.y += 5
        ebullets = [b for b in ebullets if b.top < h]
        for b in bullets[:]:
            for a in aliens[:]:
                if b.colliderect(a):
                    bullets.remove(b)
                    aliens.remove(a)
                    score += 10
                    break
        for b in ebullets:
            if b.colliderect(player):
                return
        for a in aliens:
            if a.bottom >= player.top:
                return
        if not aliens:
            return
        screen.fill(BLACK)
        pygame.draw.rect(screen, CYAN, player)
        for b in bullets:
            pygame.draw.rect(screen, WHITE, b)
        for b in ebullets:
            pygame.draw.rect(screen, YELLOW, b)
        for a in aliens:
            pygame.draw.rect(screen, GREEN, a)
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)
