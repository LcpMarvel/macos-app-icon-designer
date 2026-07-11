#!/usr/bin/env python3
"""Render a compact multi-background, multi-size macOS icon QA sheet."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="PNG icon master")
    parser.add_argument("--output", type=Path, required=True, help="Preview sheet PNG")
    args = parser.parse_args()
    if shutil.which("magick") is None:
        parser.error("ImageMagick is required")
    if not args.source.is_file() or args.source.suffix.lower() != ".png":
        parser.error("source must be an existing PNG")
    if args.output.suffix.lower() != ".png":
        parser.error("--output must be a PNG")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    backgrounds = ["#f4f4f5", "#17181b", "#7e8791", "gradient:#7f9f8f-#d9c7a5"]
    sizes = [256, 128, 64, 32, 16]
    row_height = 246
    command = ["magick", "-size", "1280x1152", "xc:#202226"]
    for row, background in enumerate(backgrounds):
        y = 24 + row * 276
        if background.startswith("gradient:"):
            colors = background.removeprefix("gradient:")
            tile = f"gradient:{colors}"
        else:
            tile = f"xc:{background}"
        command += ["(", "-size", f"1232x{row_height}", tile, ")", "-geometry", f"+24+{y}", "-composite"]
        x = 54
        for size in sizes:
            command += [
                "(", str(args.source), "-resize", f"{size}x{size}", ")",
                "-geometry", f"+{x}+{y + (row_height - size) // 2}", "-composite",
            ]
            x += max(size + 52, 185)
    command.append(str(args.output))
    subprocess.run(command, check=True)
    print(f"Created {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
