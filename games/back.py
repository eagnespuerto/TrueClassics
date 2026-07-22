"""Shared Back button widget for game screens.

Every game renders a small "< Back" chip in its top-right corner and
returns from `run()` when it is clicked, so touch/mouse users have a
visible exit path in addition to the Esc key.
"""
import pygame
from .palette import WHITE, DGRAY, GRAY


WIDTH = 66
HEIGHT = 22
MARGIN = 6
_font = None


def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont("monospace", 14, bold=True)
    return _font


def rect(screen):
    w, _ = screen.get_size()
    return pygame.Rect(w - WIDTH - MARGIN, MARGIN, WIDTH, HEIGHT)


def draw(screen):
    r = rect(screen)
    pygame.draw.rect(screen, DGRAY, r)
    pygame.draw.rect(screen, GRAY, r, 1)
    label = _get_font().render("< Back", True, WHITE)
    screen.blit(label,
                (r.centerx - label.get_width() // 2,
                 r.centery - label.get_height() // 2))


def clicked(event, screen):
    return (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and rect(screen).collidepoint(event.pos))
