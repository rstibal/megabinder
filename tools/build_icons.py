"""Draws the home-screen icons (icon-192.png, icon-512.png, apple-touch-icon.png) as the
Poke Ball from the app header, on the app's background colour.

The ball keeps to the middle of the square so Android's maskable crop (circle, squircle,
rounded square: the safe zone is the central 80% circle) never cuts into it.
Run from the repo root:  python tools/build_icons.py
"""
from PIL import Image, ImageDraw

BG, RED, WHITE, DARK = '#0f172a', '#ef4444', '#ffffff', '#1e293b'
BALL = 0.64   # ball diameter as a share of the icon width
SS = 4        # supersampling for smooth edges


def icon(size):
    n = size * SS
    im = Image.new('RGB', (n, n), BG)
    d = ImageDraw.Draw(im)
    u = n * BALL / 24            # one unit of the header's 26×26 SVG (ball radius 12)
    cx = cy = n / 2
    box = lambda r: (cx - r * u, cy - r * u, cx + r * u, cy + r * u)
    d.ellipse(box(12), fill=WHITE)
    d.pieslice(box(12), 180, 360, fill=RED)                        # top half
    d.rectangle((cx - 12 * u, cy - 1.5 * u, cx + 12 * u, cy + 1.5 * u), fill=DARK)   # band
    mask = Image.new('L', (n, n), 0)                               # keep the band inside the ball
    ImageDraw.Draw(mask).ellipse(box(12), fill=255)
    base = Image.new('RGB', (n, n), BG)
    base.paste(im, mask=mask)
    d = ImageDraw.Draw(base)
    d.ellipse(box(5), fill=DARK)                                   # button ring (r=4, stroke 2)
    d.ellipse(box(3), fill=WHITE)
    return base.resize((size, size), Image.LANCZOS)


for name, size in (('icon-192.png', 192), ('icon-512.png', 512), ('apple-touch-icon.png', 180)):
    icon(size).save(name, optimize=True)
    print('wrote', name)
