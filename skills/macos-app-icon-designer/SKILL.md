---
name: macos-app-icon-designer
description: Design, critique, refine, validate, integrate, and package production-ready macOS application and menu bar icons. Use for macOS App Icon concepts, 1024px masters, layered Icon Composer artwork, Liquid Glass variants, Xcode AppIcon catalogs, Tauri or Electron desktop apps, legacy .iconset/.icns export, Finder/Dock previews, status item or tray template images, small-size legibility checks, or reviews against Apple guidance.
---

# macOS App Icon Designer

Create a recognizable icon as a system asset, not merely an attractive square illustration. Separate concept design, Apple-platform treatment, technical packaging, and visual QA.

## Workflow

1. Inspect the app before drawing. Read its name, purpose, audience, personality, existing brand assets, target macOS/Xcode version, delivery format, and every icon surface: Finder/Dock, menu bar, notifications, documents, and in-app branding. If context is missing, infer reversible visual directions and label the assumptions.
2. Read `references/design-and-delivery.md`. If current platform behavior matters, verify the linked Apple documentation because icon tooling and appearances evolve.
3. Write a compact brief with one core metaphor, silhouette, palette, layer plan, and explicit exclusions. Offer 2-3 meaningfully different directions when the user has not selected one.
4. Produce artwork with `$imagegen` when a raster illustration is appropriate. Request separate square, unmasked layers when the target is Icon Composer. Use SVG or native design tooling for geometric marks that need deterministic edges.
5. Match the artwork treatment to the delivery path. Keep modern Icon Composer layers square and unmasked; for flattened legacy `.icns`, provide the finished icon silhouette, transparent outer corners, and optical canvas padding because Finder and Dock don't reliably create that shape for you.
6. Review at 1024, 256, 64, 32, and 16 px. Also compare the icon at its intended Dock size beside at least three neighboring app icons. Use the user's Dock screenshot when supplied; otherwise capture the packaged app in Dock. Judge the outer tile's apparent size and the foreground's apparent size separately. Revise an inset card, second neutral backplate, or undersized subject even when the standalone preview looks good. If a real Dock capture is unavailable, label any composited comparison as a simulation.
7. Deliver the format appropriate to the project:
   - Prefer an Icon Composer file and source layers for current Xcode/Liquid Glass workflows.
   - Use the existing `AppIcon.appiconset` wells when the project uses an asset catalog.
   - Create `.iconset` and `.icns` when required by a Tauri, Electron, legacy, or other non-Icon-Composer workflow.
8. Show preview sheets on light, dark, neutral, and wallpaper-like backgrounds. For a packaged `.app`, verify the configured icon, bundled resource, and source artifact agree, then inspect that build in Finder and Dock before calling the icon finished. Check for stale icon caches when the displayed result differs from the bundle. If the target cannot be launched or inspected, deliver a review draft and name the missing check.

## Generation rules

- Start from a single memorable idea with a strong silhouette and few shapes.
- Prefer illustration over photography or UI screenshots.
- Avoid text unless it is essential to the brand; verify readability and localization consequences.
- Never reproduce Apple hardware or Apple-owned marks.
- Keep foreground edges clean and layer boundaries intentional.
- Evaluate optical centering, not only geometric centering.
- Use one clear container silhouette. Transparent padding, a baked inner tile, and a system-provided backplate can read as nested cards in Dock; inspect the rendered result instead of trusting the source canvas.
- Preserve editable source layers and color profiles. Prefer sRGB for predictable delivery unless Display P3 is deliberate and tested.
- Do not claim exact unofficial safe-zone percentages as Apple requirements. Use Apple's production grid and mask previews.
- Treat "macOS style" as a platform fit, not as mandatory gradients, excessive gloss, or a generic squircle.
- Never assume macOS masks a flattened `.icns`. Reject full-bleed legacy masters unless the caller explicitly accepts a square silhouette.
- Never shrink a colorful App Icon into the menu bar. Design a separate monochrome template glyph with a tight optical bounding box and transparent background, then enable template-image behavior so macOS controls its color.

## Packaging helper

For a flattened legacy master, run:

```bash
python3 scripts/build_iconset.py path/to/icon-1024.png --output path/to/AppIcon.iconset --icns path/to/AppIcon.icns
```

The script rejects non-square or undersized sources and, when ImageMagick is available, rejects opaque corners, edge-touching flattened artwork, and artwork whose substantially opaque bounds occupy less than 85% of either canvas axis. That last check is a review heuristic to catch excess transparent padding, not an Apple safe-zone rule or a substitute for the Dock comparison. It uses macOS `sips` for canonical sizes and `iconutil` for `.icns`.

Use `--preserve-existing` after hand-tuning small variants. Use `--compile-only` to compile an existing iconset without regenerating it. Use `--allow-full-bleed` only when a square legacy silhouette is intentional. Use `--allow-small-artwork` only after comparing the deliberately compact artwork in Dock context. Do not use this helper to flatten an Icon Composer design.

Generate the required visual QA sheet:

```bash
python3 scripts/render_preview_sheet.py path/to/icon-1024.png --output path/to/icon-preview.png
```

## Completion checklist

Report the chosen concept, source/master files, appearance variants, package format, sizes reviewed, Dock-context comparison, preview sheet, tools/tests actually run, target integration changes, and any remaining manual Xcode/Icon Composer/Finder verification. Do not state that an icon is production-ready if it has only been viewed in a preview sheet or its packaged Finder/Dock appearance has not been inspected.
