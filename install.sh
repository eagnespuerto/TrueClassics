#!/usr/bin/env bash
# TrueClassics installer for Raspberry Pi OS.
set -euo pipefail

echo "==> Installing system dependencies (python3-pygame)"
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-pygame

echo "==> TrueClassics is ready. Launch with: python3 trueclassics.py"
