#!/usr/bin/env python3
"""Publish validated dist files to the GitHub Pages repository root."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
LEGACY_FILES = ("style.css", "unnamed.jpg", "logo.png", "favicon.png")

if not (DIST / "index.html").is_file():
    raise SystemExit("dist is missing; run python3 build.py first")

for path in DIST.rglob("*"):
    relative = path.relative_to(DIST)
    target = ROOT / relative
    if path.is_dir():
        target.mkdir(parents=True, exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

for name in LEGACY_FILES:
    legacy = ROOT / name
    if legacy.exists():
        legacy.unlink()

print("Published dist to the repository root; unrelated directories were preserved.")
