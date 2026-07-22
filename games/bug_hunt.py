"""Bug Hunt - shoot the segmented bug as it snakes down. Arrows to move, Space fire, Esc quits."""
import pygame
from .palette import BLACK, WHITE, GREEN, RED, YELLOW, ORANGE


CELL = 20


def run(screen, clock):
    w, h = screen.get_size()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    cols = w // CELL
    rows = h // CELL
    player = pygame.Rect(w // 2, h - 3 * CELL, CELL - 2, CELL - 2)
    bullets = []
    bug = [[x, 0] for x in range(10)]
    bug_dir = 1
    score = 0
    cooldown = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE and cooldown == 0:
                    bullets.append(pygame.Rect(player.centerx - 2, player.top, 4, 12))
                    cooldown = 10
        if cooldown > 0:
            cooldown -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < w:
            player.x += 5
        if keys[pygame.K_UP] and player.top > h - 5 * CELL:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.bottom < h:
            player.y += 5
        for b in bullets:
            b.y -= 10
        bullets = [b for b in bullets if b.bottom > 0]
        if pygame.time.get_ticks() % 4 == 0:
            for seg in bug:
                seg[0] += bug_dir
            if bug and (bug[-1][0] >= cols - 1 or bug[0][0] <= 0):
                bug_dir = -bug_dir
                for seg in bug:
                    seg[1] += 1
        new_bug = []
        for seg in bug:
            hit = False
            seg_rect = pygame.Rect(seg[0] * CELL, seg[1] * CELL, CELL, CELL)
            for b in bullets[:]:
                if seg_rect.colliderect(b):
                    bullets.remove(b)
                    score += 15
                    hit = True
                    break
            if not hit:
                new_bug.append(seg)
        bug = new_bug
        for seg in bug:
            seg_rect = pygame.Rect(seg[0] * CELL, seg[1] * CELL, CELL, CELL)
            if seg_rect.colliderect(player):
                return
            if seg[1] >= rows - 1:
                return
        if not bug:
            return
        screen.fill(BLACK)
        pygame.draw.rect(screen, YELLOW, player)
        for b in bullets:
            pygame.draw.rect(screen, WHITE, b)
        for i, seg in enumerate(bug):
            color = RED if i == 0 else (ORANGE if i % 2 else GREEN)
            pygame.draw.rect(screen, color, (seg[0] * CELL, seg[1] * CELL, CELL - 1, CELL - 1))
        screen.blit(font.render(f"Score {score}", 1, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)
