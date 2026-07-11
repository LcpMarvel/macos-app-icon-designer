# Design and delivery reference

## Authoritative sources

- Apple HIG - App icons: https://developer.apple.com/design/human-interface-guidelines/app-icons
- Creating your app icon using Icon Composer: https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer
- Configuring your app icon using an asset catalog: https://developer.apple.com/documentation/xcode/configuring-your-app-icon
- Apple Design Resources: https://developer.apple.com/design/resources/

Consult these sources when exact current requirements affect the deliverable. Apple introduced layered Liquid Glass guidance in 2025 and refined it in 2026, so older tutorials may conflict with current Xcode.

## Current baseline

- Design modern macOS icon layers on a 1024x1024 square layout.
- Supply unmasked square layers; the system applies the rounded-rectangle mask.
- Use a background layer plus one or more foreground layers when targeting Icon Composer.
- Let the system provide dynamic highlights, translucency, blur, and layer effects unless intentional testing proves a custom effect is necessary.
- Check Default, Dark, and Mono appearances. Under Mono, also preview clear and tinted options when the toolchain supports them.
- Keep primary content centered and resilient to system masking.
- Test in Icon Composer and an actual Xcode build; static mockups cannot reproduce every system effect.

## Legacy flattened iconset

Treat a flattened icon as finished artwork. Unlike Icon Composer source layers, a legacy `.icns` must carry its own silhouette. Use transparent canvas corners and deliberate optical padding for a rounded icon; do not submit a full-bleed square and expect Finder or Dock to mask it. Avoid baking an additional dark rounded tile inside the silhouette, which produces a double-border effect.

Canonical files generated from a 1024px master:

| Filename | Pixels |
| --- | ---: |
| icon_16x16.png | 16 |
| icon_16x16@2x.png | 32 |
| icon_32x32.png | 32 |
| icon_32x32@2x.png | 64 |
| icon_128x128.png | 128 |
| icon_128x128@2x.png | 256 |
| icon_256x256.png | 256 |
| icon_256x256@2x.png | 512 |
| icon_512x512.png | 512 |
| icon_512x512@2x.png | 1024 |

Inspect duplicate-pixel-size files separately because their semantic point sizes differ. Custom small-size artwork can replace generated files before compiling with `iconutil`.

## Integration paths

- **Icon Composer/Xcode:** Add the `.icon` file to the project, match the target's App Icon name, and test Default, Dark, and Mono in a build. Current Xcode prefers the matching Icon Composer file over an existing asset catalog.
- **Asset catalog:** Fill the existing macOS `AppIcon.appiconset` wells and preserve its `Contents.json`. macOS requires assets for each configured size.
- **Tauri:** Generate the platform icon set, configure `bundle.icon`, build the `.app`, and compare the source `.icns` with `Contents/Resources/*.icns`.
- **Electron:** Configure the macOS `.icns` in the selected packager, rebuild the `.app`, and inspect its `Contents/Resources` and `Info.plist`.
- **Plain app bundle:** Check `CFBundleIconFile` or `CFBundleIconName`, verify the referenced resource exists, then test Finder and Dock. Account for icon caching when replacing an installed build.

## Menu bar and status item icons

Treat the menu bar icon as a separate asset family, not a reduced App Icon. A Dock icon can use color, depth, a container, and optical padding; a status item needs a compact monochrome glyph that remains legible against both light and dark menu bars.

- Draw a simplified silhouette or outline that preserves the brand's core cue without the App Icon background tile.
- Use transparent canvas pixels and a tight optical bounding box. Avoid carrying the Dock icon's large safety margin into the status item.
- Provide 1x and 2x raster assets when the framework requires them, and inspect them at their actual point size rather than only zoomed in.
- Mark the image as a macOS template image. For Tauri, use `icon_as_template(true)`; for AppKit, set the `NSImage` template property.
- Let the system choose black or white rendering. Do not encode brand colors, gradients, shadows, facial detail, or antialiased color fringes into the template glyph.
- Compare its apparent weight and height with adjacent native status items, then test on light, dark, and tinted wallpaper-backed menu bars.
- Keep platform-specific behavior: use the template glyph on macOS while retaining an appropriate colored tray icon on Windows or Linux when needed.

## Flattened-icon validation

- Confirm an alpha channel exists when the intended silhouette is not square.
- Confirm all four canvas corners are transparent.
- Confirm visible artwork does not touch the canvas boundary unintentionally.
- Compare the optical size with neighboring system and third-party icons; geometric canvas equality does not guarantee equal perceived size.
- Preview against light, dark, neutral, and textured backgrounds at 256, 128, 64, 32, and 16 px.
- Inspect the packaged application, not only the source PNG or `.icns`.

## Review rubric

Reject or revise when any of these fail:

- Purpose: the metaphor has no relationship to the product.
- Distinction: the icon is easily confused with a common system or competitor icon.
- Silhouette: the primary shape disappears at 32px.
- Hierarchy: more than one element competes as the focal point.
- Mask resilience: critical content touches or depends on rounded corners.
- Effects: baked highlights/shadows fight system-rendered effects.
- Contrast: foreground separates poorly in any supported appearance.
- Craft: edges, tangencies, gradients, and optical alignment look accidental.
- Packaging: required layers, sizes, filenames, color profile, or Xcode mapping are missing.
