#!/usr/bin/env python3
"""Entrypoint for news-image-20261122.

Runs render.py (same directory) to draw entry.png, then copies the
result to the output directory as entry.png and verifies it: PNG,
1024x1024, at most 1 MiB. Standard library only.
"""
import hashlib
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "render.py")


def read_png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    subprocess.run([sys.executable, SRC], cwd=HERE, check=True)
    built = os.path.join(HERE, "entry.png")
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(built, target)
    size = os.path.getsize(target)
    width, height = read_png_size(target)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"bad size {width}x{height}, want 1024x1024")
    if size > 1048576:
        raise SystemExit(f"entry.png too large: {size} bytes")
    digest = hashlib.sha256(open(target, "rb").read()).hexdigest()
    print(f"entry.png {width}x{height} {size} bytes sha256={digest}")


if __name__ == "__main__":
    main()
