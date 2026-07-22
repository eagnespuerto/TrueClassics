# TrueClassics

**Category:** Games
**Platform:** Raspberry Pi OS (PiOS) / any Linux, macOS, or Windows with Python 3
**Storage footprint:** ~40 KB of code, no bundled art — everything drawn at runtime in a **16-color RGB565-safe palette** (16-bit colors) to keep the app tiny.

A launcher plus **10 original takes on classic arcade games**. Names are original to avoid trademark trouble, but the gameplay will feel familiar.

| # | TrueClassics name | Inspired by |
|---|-------------------|-------------|
| 1 | Paddle Duel       | Bat & ball duel |
| 2 | Brick Buster      | Brick-breaking paddle game |
| 3 | Blockfall         | Falling-tetromino puzzle |
| 4 | Serpent           | Grow-longer snake game |
| 5 | Alien Assault     | Marching-alien shooter |
| 6 | Chomper           | Dot-eating maze chase |
| 7 | Rock Storm        | Rotating-ship asteroid shooter |
| 8 | Hopper            | Cross-the-road-and-river hop |
| 9 | Bug Hunt          | Segmented-bug descending shooter |
| 10 | Sky Defense      | Point-and-click missile interception |

## Install

### Quick install (Raspberry Pi OS)

```bash
git clone https://github.com/eagnespuerto/TrueClassics.git
cd TrueClassics
chmod +x install.sh
./install.sh
python3 trueclassics.py
```

### Manual install (any OS with Python 3.9+)

```bash
git clone https://github.com/eagnespuerto/TrueClassics.git
cd TrueClassics
python3 -m pip install -r requirements.txt
python3 trueclassics.py
```

### Add to the PiOS Games menu

`./install.sh` already does this — it writes a `trueclassics.desktop` entry into `~/.local/share/applications/` with the absolute path filled in, so **Menu → Games → TrueClassics** just works.

To install the menu entry by hand instead, edit the shipped [`trueclassics.desktop`](trueclassics.desktop), replace `__INSTALL_DIR__` with the absolute path to your clone (e.g. `/home/pi/TrueClassics`), then:

```bash
mkdir -p ~/.local/share/applications
cp trueclassics.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications 2>/dev/null || true
```

## Controls

**Launcher:** `↑` / `↓` to select, `Enter` or `Space` to play, `Esc` to quit.
Inside any game, `Esc` returns to the launcher.

| Game | Controls |
|------|----------|
| Paddle Duel   | Left paddle `W`/`S`, right paddle `↑`/`↓` |
| Brick Buster  | `←` `→` move paddle, `Space` launches the ball (3 lives) |
| Blockfall     | `←` `→` move, `↑` rotate, `↓` soft-drop |
| Serpent       | Arrow keys to steer |
| Alien Assault | `←` `→` move, `Space` fire |
| Chomper       | Arrow keys to move |
| Rock Storm    | `←` `→` turn, `↑` thrust, `Space` fire |
| Hopper        | Arrow keys — hop up, down, left, right |
| Bug Hunt      | Arrow keys move, `Space` fire |
| Sky Defense   | Mouse aim + click to launch interceptor |

## Why 16-bit color?

The whole palette lives in [`games/palette.py`](games/palette.py) as 16 constants whose RGB triples are quantized to the RGB565 format (5 bits red, 6 bits green, 5 bits blue). No sprites, no textures, no audio files — every visual is a `pygame.draw.*` call. The result: the entire game collection is tens of kilobytes of Python and runs comfortably on a Raspberry Pi Zero.

## Project layout

```
TrueClassics/
├── trueclassics.py         # Launcher / main menu
├── games/
│   ├── palette.py          # 16 RGB565-safe colors
│   ├── paddle_duel.py
│   ├── brick_buster.py
│   ├── blockfall.py
│   ├── serpent.py
│   ├── alien_assault.py
│   ├── chomper.py
│   ├── rock_storm.py
│   ├── hopper.py
│   ├── bug_hunt.py
│   └── sky_defense.py
├── install.sh              # PiOS one-shot installer
├── trueclassics.desktop    # Desktop menu entry
├── requirements.txt
└── LICENSE
```

## Requirements

- Python 3.9+
- `pygame` 2.5+ (installed via `apt` on PiOS, `pip` elsewhere)

## License

MIT — see [LICENSE](LICENSE).
