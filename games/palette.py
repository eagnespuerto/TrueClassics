"""16-bit RGB565-safe palette. All colors quantize cleanly to 5-6-5 bits."""


def _rgb565_safe(r, g, b):
    return (r & 0xF8, g & 0xFC, b & 0xF8)


BLACK   = _rgb565_safe(0,   0,   0)
WHITE   = _rgb565_safe(248, 252, 248)
GRAY    = _rgb565_safe(128, 128, 128)
DGRAY   = _rgb565_safe(56,  60,  56)
RED     = _rgb565_safe(248, 0,   0)
GREEN   = _rgb565_safe(0,   248, 0)
BLUE    = _rgb565_safe(0,   0,   248)
YELLOW  = _rgb565_safe(248, 252, 0)
CYAN    = _rgb565_safe(0,   252, 248)
MAGENTA = _rgb565_safe(248, 0,   248)
ORANGE  = _rgb565_safe(248, 128, 0)
PURPLE  = _rgb565_safe(128, 0,   248)
LIME    = _rgb565_safe(128, 248, 0)
PINK    = _rgb565_safe(248, 128, 128)
BROWN   = _rgb565_safe(128, 64,  0)
NAVY    = _rgb565_safe(0,   0,   128)

PALETTE = [BLACK, WHITE, GRAY, DGRAY, RED, GREEN, BLUE, YELLOW,
           CYAN, MAGENTA, ORANGE, PURPLE, LIME, PINK, BROWN, NAVY]
