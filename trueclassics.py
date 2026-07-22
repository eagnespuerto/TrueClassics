#!/usr/bin/env python3
"""TrueClassics - a collection of 10 classic-style arcade games for PiOS.

Launcher: arrows to select, Enter to play, Esc to quit.
Two-column menu + Help entry sized for the 800x480 landscape minimum
(the official 7" PiOS touch display and similar).
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


WIN_W, WIN_H = 800, 480

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

HELP_INDEX = len(GAMES)  # 10
COL_SIZE = 5

CONTROLS = [
    ("Paddle Duel",   "W / S = left paddle    Up / Down = right paddle"),
    ("Brick Buster",  "Left / Right move paddle    Space launch ball"),
    ("Blockfall",     "Left / Right move    Up rotate    Down soft-drop"),
    ("Serpent",       "Arrow keys to steer"),
    ("Alien Assault", "Left / Right move    Space fire"),
    ("Chomper",       "Arrow keys to move"),
    ("Rock Storm",    "Left / Right turn    Up thrust    Space fire"),
    ("Hopper",        "Arrow keys hop up / down / left / right"),
    ("Bug Hunt",      "Arrow keys move    Space fire"),
    ("Sky Defense",   "Mouse aim + click to launch interceptor"),
]


def move_selection(sel, key):
    if key == pygame.K_UP:
        if sel == HELP_INDEX:
            return COL_SIZE - 1
        col, row = sel // COL_SIZE, sel % COL_SIZE
        return col * COL_SIZE + (row - 1) % COL_SIZE
    if key == pygame.K_DOWN:
        if sel == HELP_INDEX:
            return 0
        col, row = sel // COL_SIZE, sel % COL_SIZE
        if row == COL_SIZE - 1:
            return HELP_INDEX
        return col * COL_SIZE + row + 1
    if key == pygame.K_LEFT:
        if sel == HELP_INDEX:
            return sel
        if sel >= COL_SIZE:
            return sel - COL_SIZE
        return sel
    if key == pygame.K_RIGHT:
        if sel == HELP_INDEX:
            return sel
        if sel < COL_SIZE:
            return sel + COL_SIZE
        return sel
    return sel


def draw_menu(screen, title_font, item_font, small_font, selected):
    w, h = screen.get_size()
    screen.fill(BLACK)
    title = title_font.render("TRUECLASSICS", True, YELLOW)
    screen.blit(title, ((w - title.get_width()) // 2, 15))
    sub = small_font.render("10 classic arcade games in 16-bit color", True, CYAN)
    screen.blit(sub, ((w - sub.get_width()) // 2, 60))

    col_w = w // 2
    col_x = [col_w // 2, col_w + col_w // 2]
    top = 100
    row_h = 34
    for i, (name, _) in enumerate(GAMES):
        col, row = i // COL_SIZE, i % COL_SIZE
        color = YELLOW if i == selected else WHITE
        prefix = "> " if i == selected else "  "
        surf = item_font.render(f"{prefix}{name}", True, color)
        x = col_x[col] - surf.get_width() // 2
        y = top + row * row_h
        screen.blit(surf, (x, y))

    help_y = top + COL_SIZE * row_h + 10
    color = YELLOW if selected == HELP_INDEX else CYAN
    prefix = "> " if selected == HELP_INDEX else "  "
    hs = item_font.render(f"{prefix}Help / Controls", True, color)
    screen.blit(hs, ((w - hs.get_width()) // 2, help_y))

    footer = small_font.render(
        "Arrows: select   Enter: play   Esc: quit", True, GRAY)
    screen.blit(footer, ((w - footer.get_width()) // 2, h - 25))
    pygame.display.flip()


def show_help(screen, clock, title_font, item_font, small_font):
    w, h = screen.get_size()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_BACKSPACE):
                return
        screen.fill(BLACK)
        title = title_font.render("HELP  -  CONTROLS", True, YELLOW)
        screen.blit(title, ((w - title.get_width()) // 2, 15))
        launcher = small_font.render(
            "Launcher: Arrows select, Enter play, Esc quit.  In any game, Esc returns here.",
            True, CYAN)
        screen.blit(launcher, ((w - launcher.get_width()) // 2, 60))
        top = 95
        row_h = 32
        for i, (name, ctrl) in enumerate(CONTROLS):
            name_surf = small_font.render(name, True, YELLOW)
            ctrl_surf = small_font.render(ctrl, True, WHITE)
            y = top + i * row_h
            screen.blit(name_surf, (40, y))
            screen.blit(ctrl_surf, (200, y))
        back = small_font.render("Press Esc or Enter to return", True, GRAY)
        screen.blit(back, ((w - back.get_width()) // 2, h - 25))
        pygame.display.flip()
        clock.tick(30)


def main():
    pygame.init()
    pygame.display.set_caption("TrueClassics")
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("monospace", 36, bold=True)
    item_font = pygame.font.SysFont("monospace", 22, bold=True)
    small_font = pygame.font.SysFont("monospace", 14)
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
                if e.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    selected = move_selection(selected, e.key)
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == HELP_INDEX:
                        result = show_help(screen, clock, title_font, item_font, small_font)
                    else:
                        result = GAMES[selected][1].run(screen, clock)
                    if result == "quit":
                        pygame.quit()
                        sys.exit(0)
        draw_menu(screen, title_font, item_font, small_font, selected)
        clock.tick(30)


if __name__ == "__main__":
    main()
