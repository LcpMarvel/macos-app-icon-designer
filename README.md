# macOS App Icon Designer

A production-focused agent skill for designing, reviewing, validating, packaging, and integrating macOS application icons and menu bar template images.

It helps Codex, Claude Code, Cursor, and other compatible coding agents treat an icon as a complete system asset rather than a standalone square illustration.

## What it covers

- Product-aware icon concepts and visual direction
- Apple Icon Composer and Liquid Glass workflows
- Xcode AppIcon asset catalogs
- Legacy `.iconset` and `.icns` packaging
- Transparent-corner and full-bleed validation
- Small-size legibility checks from 256 px down to 16 px
- Finder, Dock, and multi-background preview sheets
- Tauri, Electron, and plain macOS app bundle integration
- Dedicated monochrome menu bar and status item template images

The skill explicitly distinguishes modern, unmasked Icon Composer layers from flattened legacy `.icns` artwork. This prevents common production mistakes such as square Dock icons, double-rounded borders, oversized optical bounds, and colorful App Icons being reused as tiny menu bar icons.

## Install

Use the open [`skills`](https://github.com/vercel-labs/skills) CLI.

```bash
# Global installation: available in every project
npx skills add -g LcpMarvel/macos-app-icon-designer

# Project installation: available only in the current repository
npx skills add LcpMarvel/macos-app-icon-designer
```

List the skills in this repository without installing them:

```bash
npx skills add LcpMarvel/macos-app-icon-designer --list
```

Install only this skill for Codex without interactive confirmation:

```bash
npx skills add LcpMarvel/macos-app-icon-designer \
  --skill macos-app-icon-designer \
  --agent codex \
  -y
```

## Requirements

- macOS
- Python 3
- `sips` and `iconutil`, included with macOS
- ImageMagick's `magick` command for strict transparency checks and preview generation

Install ImageMagick with Homebrew:

```bash
brew install imagemagick
```

The core design guidance can be used on any platform. The legacy `.icns` packaging helper requires macOS system tools.

## Example prompts

```text
Use $macos-app-icon-designer to design and integrate a production-ready icon for this Tauri app.
```

```text
Review this existing macOS icon at Dock and menu bar sizes, then fix its packaging.
```

```text
Create separate App Icon and monochrome status item assets for this Electron app.
```

## Included tools

### Build a legacy iconset and ICNS file

```bash
python3 skills/macos-app-icon-designer/scripts/build_iconset.py \
  path/to/icon-1024.png \
  --output path/to/AppIcon.iconset \
  --icns path/to/AppIcon.icns
```

The helper rejects non-square or undersized sources. When ImageMagick is available, it also rejects opaque corners and unintended full-bleed artwork.

Useful options:

- `--preserve-existing`: keep hand-tuned small-size variants
- `--compile-only`: compile an existing iconset without regenerating images
- `--allow-full-bleed`: explicitly allow an intentional square silhouette

### Render a visual QA sheet

```bash
python3 skills/macos-app-icon-designer/scripts/render_preview_sheet.py \
  path/to/icon-1024.png \
  --output path/to/icon-preview.png
```

The preview sheet shows the icon at 256, 128, 64, 32, and 16 px on light, dark, neutral, and wallpaper-like backgrounds.

## Repository structure

```text
skills/macos-app-icon-designer/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   `-- design-and-delivery.md
`-- scripts/
    |-- build_iconset.py
    |-- render_preview_sheet.py
    `-- test_build_iconset.py
```

The `skills` CLI automatically discovers `skills/macos-app-icon-designer/SKILL.md`.

## Validate locally

Run the deterministic packaging tests:

```bash
python3 skills/macos-app-icon-designer/scripts/test_build_iconset.py
```

Verify skill discovery:

```bash
DISABLE_TELEMETRY=1 npx skills add . --list
```

## Authoritative references

The skill routes current platform-sensitive decisions to Apple's documentation:

- [Human Interface Guidelines: App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Creating your app icon using Icon Composer](https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer)
- [Configuring your app icon using an asset catalog](https://developer.apple.com/documentation/xcode/configuring-your-app-icon)
- [Apple Design Resources](https://developer.apple.com/design/resources/)

## License

MIT
