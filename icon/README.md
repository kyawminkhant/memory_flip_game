# Application icon

`logo.ico` is the Windows application icon loaded by `Memory Flip Game.py`.
It contains transparent 16, 24, 32, 48, 64, 128, and 256 pixel versions.
`logo.png` is the transparent source artwork, retained for future exports.
The main README displays this PNG. `images/Logo.png` contains the same artwork
for compatibility with existing links.

The custom matching-card artwork was created with OpenAI's built-in image
generation tool. No online images or third-party reference artwork were used.

## Background removal prompt

Use case: background-extraction. Edit the supplied memory flip game icon. Preserve the two overlapping ivory and mint cards, coral sparkle symbols, and curved ivory flip arrow, with the same shapes and placement. Remove ALL background: remove the entire teal backdrop, teal glow, haze, shadow outside the objects, and any opaque canvas. Only the two cards and arrow should remain, cleanly cut out with antialiased edges on a genuinely transparent alpha-channel PNG. The empty space between the arrow and cards must also be fully transparent. No colored background, no white rectangle, no checkerboard baked into image, no ground shadow. Preserve the artwork colors and do not add text or new elements.

## Edge cleanup prompt

Clean up this transparent app icon. Keep exactly the two cards, their coral symbols, and the curved arrow. Remove the stray white speckles and fringe around the arrow and card outlines. Make every edge crisp smooth antialiased, with completely transparent negative space everywhere outside the three objects, including under the arrow. True alpha transparency, no background color or shadow. Preserve composition and colors.

## Original generation prompt (background superseded by edits above)

Use case: logo-brand. Create an original square desktop application icon for a memory flip matching-card game. Two slightly overlapping rounded playing tiles, each showing the same simple coral four-point sparkle symbol, one tile ivory and the second pale mint, with a small curved flip arrow above them. Bold clean flat illustration with subtle depth, deep teal full-bleed background, strong silhouette readable at 16-32 pixels. Centered composition with generous safe margins. No text, letters, numbers, watermarks, brand logos, copyrighted characters, or references to any existing game or artwork. Custom geometric design made from scratch. Output one 1024x1024 image.
