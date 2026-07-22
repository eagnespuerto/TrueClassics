#!/usr/bin/env bash
# TrueClassics installer for Raspberry Pi OS.
set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing system dependencies (python3-pygame)"
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-pygame

echo "==> Installing desktop menu entry"
APPS_DIR="${HOME}/.local/share/applications"
mkdir -p "${APPS_DIR}"
cat > "${APPS_DIR}/trueclassics.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=TrueClassics
Comment=10 classic-style arcade games in 16-bit color
Exec=sh -c 'cd "${INSTALL_DIR}" && python3 trueclassics.py'
Path=${INSTALL_DIR}
Icon=applications-games
Terminal=false
Categories=Game;ArcadeGame;
StartupNotify=false
EOF
chmod +x "${APPS_DIR}/trueclassics.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APPS_DIR}" >/dev/null 2>&1 || true
fi

echo "==> TrueClassics installed."
echo "    Menu:     look under Games -> TrueClassics"
echo "    Terminal: cd ${INSTALL_DIR} && python3 trueclassics.py"
