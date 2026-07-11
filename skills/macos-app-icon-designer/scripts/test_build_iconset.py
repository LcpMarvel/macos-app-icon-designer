#!/usr/bin/env python3
"""Smoke tests for the legacy iconset helper."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("build_iconset.py")


@unittest.skipUnless(shutil.which("magick") and shutil.which("sips") and shutil.which("iconutil"), "macOS image tools required")
class BuildIconsetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def image(self, name: str, rounded: bool) -> Path:
        path = self.root / name
        if rounded:
            subprocess.run([
                "magick", "-size", "1024x1024", "xc:none", "-fill", "#258fbe",
                "-draw", "roundrectangle 82,82 941,941 185,185", str(path),
            ], check=True)
        else:
            subprocess.run(["magick", "-size", "1024x1024", "xc:#258fbe", str(path)], check=True)
        return path

    def test_rejects_full_bleed_by_default(self) -> None:
        result = subprocess.run([
            "python3", str(SCRIPT), str(self.image("square.png", False)),
            "--output", str(self.root / "AppIcon.iconset"),
        ], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full-bleed", result.stderr)

    def test_builds_and_compiles_rounded_source(self) -> None:
        iconset = self.root / "AppIcon.iconset"
        icns = self.root / "AppIcon.icns"
        subprocess.run([
            "python3", str(SCRIPT), str(self.image("rounded.png", True)),
            "--output", str(iconset), "--icns", str(icns),
        ], check=True)
        self.assertEqual(len(list(iconset.glob("*.png"))), 10)
        self.assertGreater(icns.stat().st_size, 0)

    def test_preserves_existing_variant(self) -> None:
        iconset = self.root / "AppIcon.iconset"
        iconset.mkdir()
        custom = iconset / "icon_16x16.png"
        custom.write_bytes(b"hand-tuned")
        subprocess.run([
            "python3", str(SCRIPT), str(self.image("rounded.png", True)),
            "--output", str(iconset), "--preserve-existing",
        ], check=True)
        self.assertEqual(custom.read_bytes(), b"hand-tuned")

    def test_compile_only_uses_existing_iconset(self) -> None:
        iconset = self.root / "AppIcon.iconset"
        subprocess.run([
            "python3", str(SCRIPT), str(self.image("rounded.png", True)),
            "--output", str(iconset),
        ], check=True)
        icns = self.root / "compiled.icns"
        subprocess.run([
            "python3", str(SCRIPT), "--output", str(iconset),
            "--compile-only", "--icns", str(icns),
        ], check=True)
        self.assertGreater(icns.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
