#!/usr/bin/env python3
"""Validate and build a flattened macOS .iconset and optional .icns."""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


FILES = {
    "icon_16x16.png": 16,
    "icon_16x16@2x.png": 32,
    "icon_32x32.png": 32,
    "icon_32x32@2x.png": 64,
    "icon_128x128.png": 128,
    "icon_128x128@2x.png": 256,
    "icon_256x256.png": 256,
    "icon_256x256@2x.png": 512,
    "icon_512x512.png": 512,
    "icon_512x512@2x.png": 1024,
}


def run(*args: str, capture: bool = False) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=capture)
    return result.stdout if capture else ""


def dimensions(source: Path) -> tuple[int, int]:
    out = run("sips", "-g", "pixelWidth", "-g", "pixelHeight", str(source), capture=True)
    values: dict[str, int] = {}
    for line in out.splitlines():
        if ":" in line:
            key, value = line.strip().split(":", 1)
            if value.strip().isdigit():
                values[key] = int(value.strip())
    return values.get("pixelWidth", 0), values.get("pixelHeight", 0)


def alpha_at(source: Path, x: int, y: int) -> float:
    value = run(
        "magick", str(source), "-alpha", "extract", "-format", f"%[fx:p{{{x},{y}}}]", "info:", capture=True
    ).strip()
    return float(value)


def validate_flattened_artwork(source: Path, width: int, allow_full_bleed: bool) -> None:
    if shutil.which("magick") is None:
        print("Warning: ImageMagick is unavailable; corner and boundary checks were skipped.", file=sys.stderr)
        return

    corners = [(0, 0), (width - 1, 0), (0, width - 1), (width - 1, width - 1)]
    opaque_corners = [point for point in corners if alpha_at(source, *point) > 0.02]
    bbox = run(
        "magick", str(source), "-alpha", "extract", "-threshold", "1", "-format", "%@", "info:", capture=True
    ).strip()
    match = re.fullmatch(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", bbox)
    touches_edge = False
    if match:
        box_w, box_h, x, y = map(int, match.groups())
        touches_edge = x <= 0 or y <= 0 or x + box_w >= width or y + box_h >= width

    if (opaque_corners or touches_edge) and not allow_full_bleed:
        details = []
        if opaque_corners:
            details.append(f"opaque corners: {opaque_corners}")
        if touches_edge:
            details.append(f"visible bounds touch the canvas edge ({bbox})")
        raise ValueError(
            "flattened legacy artwork appears full-bleed; Finder/Dock may show a square icon ("
            + "; ".join(details)
            + "). Add transparent outer padding or pass --allow-full-bleed when intentional."
        )


def compile_icns(iconset: Path, icns: Path) -> None:
    if shutil.which("iconutil") is None:
        raise ValueError("iconutil is required to create .icns")
    missing = sorted(set(FILES) - {path.name for path in iconset.glob("*.png")})
    if missing:
        raise ValueError("iconset is missing canonical files: " + ", ".join(missing))
    icns.parent.mkdir(parents=True, exist_ok=True)
    run("iconutil", "-c", "icns", str(iconset), "-o", str(icns))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, nargs="?", help="Square PNG master, at least 1024px")
    parser.add_argument("--output", type=Path, required=True, help="Output directory ending in .iconset")
    parser.add_argument("--icns", type=Path, help="Optional compiled .icns path")
    parser.add_argument("--preserve-existing", action="store_true", help="Keep existing canonical PNG variants")
    parser.add_argument("--compile-only", action="store_true", help="Compile the existing iconset without resizing")
    parser.add_argument("--allow-full-bleed", action="store_true", help="Allow opaque corners or edge-touching artwork")
    args = parser.parse_args()

    try:
        if args.output.suffix != ".iconset":
            raise ValueError("--output must end in .iconset")
        if args.compile_only:
            if args.source is not None:
                raise ValueError("omit source when using --compile-only")
            if not args.output.is_dir():
                raise ValueError("--output must be an existing iconset for --compile-only")
        else:
            if shutil.which("sips") is None:
                raise ValueError("sips is required; run this script on macOS")
            if args.source is None or not args.source.is_file() or args.source.suffix.lower() != ".png":
                raise ValueError("source must be an existing PNG")
            width, height = dimensions(args.source)
            if width != height or width < 1024:
                raise ValueError(f"source must be square and at least 1024px; got {width}x{height}")
            validate_flattened_artwork(args.source, width, args.allow_full_bleed)
            args.output.mkdir(parents=True, exist_ok=True)
            for name, size in FILES.items():
                destination = args.output / name
                if args.preserve_existing and destination.exists():
                    continue
                run("sips", "-z", str(size), str(size), str(args.source), "--out", str(destination), capture=True)

        if args.icns:
            compile_icns(args.output, args.icns)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

    print(f"Validated {args.output}" if args.compile_only else f"Created {args.output}")
    if args.icns:
        print(f"Created {args.icns}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
