#!/usr/bin/env python3
"""TrueClassics - a collection of 10 classic-style arcade games for PiOS.

Launcher: Up/Down to select, Enter to play, Esc to quit.
All rendering uses a 16-color RGB565-safe palette to keep storage minimal.
"""
import sys
import pygame

from games import (
    paddle_duel,
    brick_buster,
    blockfall,
    serpent,
    alien_assault,
    chomper,
    rock_storm,
    hopper,
    bug_hunt,
    sky_defense,
)
from games.palette import BLACK, WHITE, YELLOW, CYAN, GRAY


GAMES = [
    ("Paddle Duel",   paddle_duel),
    ("Brick Buster",  brick_buster),
    ("Blockfall",     blockfall),
    ("Serpent",       serpent),
    ("Alien Assault", alien_assault),
    ("Chomper",       chomper),
    ("Rock Storm",    rock_storm),
    ("Hopper",        hopper),
    ("Bug Hunt",      bug_hunt),
    ("Sky Defense",   sky_defense),
]


def draw_menu(screen, title_font, item_font, small_font, selected):
    w, h = screen.get_size()
    screen.fill(BLACK)
    title = title_font.render("TRUECLASSICS", True, YELLOW)
    screen.blit(title, ((w - title.get_width()) // 2, 30))
    sub = small_font.render("10 classic arcade games in 16-bit color", True, CYAN)
    screen.blit(sub, ((w - sub.get_width()) // 2, 90))
    for i, (name, _) in enumerate(GAMES):
        color = YELLOW if i == selected else WHITE
        prefix = "> " if i == selected else "  "
        surf = item_font.render(f"{prefix}{name}", True, color)
        screen.blit(surf, ((w - surf.get_width()) // 2, 150 + i * 36))
    help_line = small_font.render("Up/Down: select   Enter: play   Esc: quit", True, GRAY)
    screen.blit(help_line, ((w - help_line.get_width()) // 2, h - 40))
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("TrueClassics")
    screen = pygame.display.set_mode((800, 640), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("monospace", 48, bold=True)
    item_font = pygame.font.SysFont("monospace", 24, bold=True)
    small_font = pygame.font.SysFont("monospace", 16)
    selected = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(GAMES)
                if e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(GAMES)
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    result = GAMES[selected][1].run(screen, clock)
                    if result == "quit":
                        pygame.quit()
                        sys.exit(0)
        draw_menu(screen, title_font, item_font, small_font, selected)
        clock.tick(30)


if __name__ == "__main__":
    main()
