#!/usr/bin/env python3
"""
Flavored — Coffeehouse asset generator.

Produces the raster assets used by the Astro build:

    src/assets/bg/coffee-bokeh.jpg      2400x1600 heavily blurred bokeh backdrop
    src/assets/cups/hero-heart.png      top-down cup + saucer, two cocoa hearts
    src/assets/cups/americano.png       top-down cup, rosetta / leaf latte art
    src/assets/cups/cappuccino-bear.png top-down cup, bear-face latte art
    src/assets/cups/rosetta-large.png   big top-down latte, white tulip art
    src/assets/cups/latte-small.png     small top-down latte, rosetta art

Everything is deterministic (fixed seed) so re-running produces identical files.
These are placeholders with the correct silhouette / palette / framing: drop real
photography in over the same filenames and nothing else has to change. If a file
is missing the site still renders, because every cup falls back to CupArt.astro.

    python scripts/generate-assets.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BG_OUT = ROOT / "src" / "assets" / "bg"
CUP_OUT = ROOT / "src" / "assets" / "cups"

SS = 3  # supersample factor for the cup art


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def radial(size: int, inner: tuple[int, int, int], outer: tuple[int, int, int],
           cx: float = 0.5, cy: float = 0.5, r: float = 0.5,
           falloff: float = 1.0) -> Image.Image:
    """Radial gradient RGBA image of `size` x `size`, transparent beyond r*size."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    dist = np.sqrt((xx / size - cx) ** 2 + (yy / size - cy) ** 2)
    d = np.clip(dist / r, 0.0, 1.0) ** falloff
    inner_a = np.array(inner, np.float32)
    outer_a = np.array(outer, np.float32)
    rgb = inner_a[None, None, :] * (1 - d[..., None]) + outer_a[None, None, :] * d[..., None]
    alpha = np.where(dist <= r, 255.0, 0.0)
    out = np.concatenate([rgb, alpha[..., None]], axis=2).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def sheen(size: int, cx: float, cy: float, r: float, color, peak: int = 26) -> Image.Image:
    """Very soft off-centre highlight — stops the crema reading as a 3D sphere."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    dist = np.sqrt((xx / size - cx) ** 2 + (yy / size - cy) ** 2) / r
    a = np.clip(1.0 - dist, 0.0, 1.0) ** 2 * peak
    rgb = np.array(color, np.float32)[None, None, :]
    out = np.concatenate([np.broadcast_to(rgb, (size, size, 3)), a[..., None]], axis=2)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def soft_mask(w: int, h: int, cx: float, cy: float, r: float, blur: float) -> Image.Image:
    """Anti-aliased circular alpha mask. `cx`/`cy`/`r` are in pixels."""
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))


def circle_layer(w: int, h: int, cx: float, cy: float, r: float, color,
                 blur: float = 1.0) -> Image.Image:
    """RGBA layer with a soft-edged filled circle at pixel coords."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", (w, h), color), (0, 0),
                soft_mask(w, h, cx, cy, r, blur))
    return layer


def disc(size: int, cx: float, cy: float, r: float, color, blur: float = 1.0) -> Image.Image:
    """Square-layer convenience wrapper using normalised (0..1) coordinates."""
    return circle_layer(size, size, cx * size, cy * size, r * size, color, blur)


def ring_layer(w: int, h: int, cx: float, cy: float, r: float, width: float,
               color, blur: float = 1.0) -> Image.Image:
    """RGBA ring (annulus) outline at pixel coords."""
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse(
        [cx - r + width / 2, cy - r + width / 2, cx + r - width / 2, cy + r - width / 2],
        outline=255, width=max(1, int(width)),
    )
    m = m.filter(ImageFilter.GaussianBlur(blur))
    layer = Image.new("RGBA", (w, h), color)
    layer.putalpha(m.point(lambda v, a=color[3]: int(v * a / 255)))
    return layer


def crema_texture(size: int, cx: float, cy: float, r: float, seed: int,
                  strength: float = 26.0) -> Image.Image:
    """Low-frequency mottling so the crema reads as liquid, not a shaded sphere."""
    rnd = np.random.default_rng(seed)
    small = max(4, size // 110)
    n = rnd.random((small, small)).astype(np.float32)
    n = np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((size, size),
                                                                    Image.BICUBIC), np.float32)
    n = n / 255.0 - 0.5
    a = np.clip(np.abs(n) * strength * 2.0, 0, 255)
    tone = np.where(n[..., None] > 0, 255.0, 30.0)
    rgb = np.broadcast_to(tone, (size, size, 3))
    tex = np.concatenate([rgb, a[..., None]], axis=2).astype(np.uint8)
    img = Image.fromarray(tex, "RGBA")
    mask = soft_mask(size, size, cx, cy, r, size * 0.012)
    return Image.composite(img, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)


def paste(base: Image.Image, layer: Image.Image) -> Image.Image:
    return Image.alpha_composite(base, layer)


def powder(layer: Image.Image, amount: float = 0.45, seed: int = 5,
           scale: float = 1.6) -> Image.Image:
    """Break up a solid fill so it reads as stencilled cocoa powder, not paint."""
    w, h = layer.size
    small = (max(2, int(w / scale)), max(2, int(h / scale)))
    rnd = np.random.default_rng(seed)
    noise = rnd.random(small).astype(np.float32)
    noise = np.array(Image.fromarray((noise * 255).astype(np.uint8)).resize((w, h),
                                                                            Image.BILINEAR),
                     np.float32) / 255.0
    a = np.array(layer.getchannel("A"), np.float32)
    a = a * (1.0 - amount) + a * noise * amount
    layer.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8), "L"))
    return layer


def grain(img: Image.Image, amount: float = 5.0, seed: int = 7) -> Image.Image:
    """Subtle photographic grain so the placeholder art is not banded."""
    rnd = np.random.default_rng(seed)
    a = np.array(img, np.float32)
    n = rnd.normal(0.0, amount, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


# --------------------------------------------------------------------------- #
# latte art
# --------------------------------------------------------------------------- #
def _rot(vx: float, vy: float, ang: float) -> tuple[float, float]:
    c, s = math.cos(ang), math.sin(ang)
    return vx * c - vy * s, vx * s + vy * c


def _leaf(base: tuple[float, float], axis: tuple[float, float], length: float,
          width: float, steps: int = 22) -> list[tuple[float, float]]:
    """A tapered almond/leaf outline from `base` along `axis`."""
    ax, ay = axis
    px, py = -ay, ax
    up, dn = [], []
    for i in range(steps + 1):
        u = i / steps
        h = width * math.sin(math.pi * (u ** 0.82))
        cxx, cyy = base[0] + ax * length * u, base[1] + ay * length * u
        up.append((cxx + px * h, cyy + py * h))
        dn.append((cxx - px * h, cyy - py * h))
    return up + dn[::-1]


def draw_rosetta(draw: ImageDraw.ImageDraw, size: int, cx: float, cy: float, r: float,
                 color=(255, 248, 234, 255), leaves: int = 7) -> None:
    """Classic rosetta: tapered leaves fanning off a central stem."""
    sx, sy, rr = cx * size, cy * size, r * size
    ang = math.radians(-74)                      # stem runs up, tipped slightly right
    ax, ay = math.cos(ang), math.sin(ang)
    nx, ny = -ay, ax
    span = rr * 1.30
    x0, y0 = sx - ax * span * 0.44, sy - ay * span * 0.44

    for i in range(leaves):
        t = i / (leaves - 1)
        bx, by = x0 + ax * span * t, y0 + ay * span * t
        length = rr * (0.58 - 0.26 * t)
        width = rr * (0.130 - 0.042 * t)
        for sgn in (-1, 1):
            # Leaves fan out from the pour point. `spread` is measured off the
            # stem's normal, so 0 would point straight sideways and 90 straight
            # along the stem — at the old 78..48 the leaves all but merged into
            # the stem and the whole rosetta read as one blob.
            spread = math.radians(sgn * (30 + 34 * t))
            fax, fay = _rot(nx * sgn, ny * sgn, spread)
            draw.polygon(_leaf((bx, by), (fax, fay), length, width), fill=color)

    # stem
    draw.line([(x0, y0), (x0 + ax * span * 1.04, y0 + ay * span * 1.04)],
              fill=color, width=max(3, int(rr * 0.062)), joint="curve")


def draw_tulip(draw: ImageDraw.ImageDraw, size: int, cx: float, cy: float, r: float,
               color=(255, 248, 236, 255)) -> None:
    """Tulip: stacked hearts, wide at the bottom, pointed at the top."""
    sx = cx * size
    sy = cy * size
    rr = r * size
    for i, (scale, dy) in enumerate([(1.00, 0.44), (0.78, 0.00), (0.55, -0.42)]):
        w = rr * 0.80 * scale
        h = rr * 0.62 * scale
        y = sy + rr * dy
        pts = [
            (sx - w / 2, y - h * 0.10),
            (sx - w / 2, y + h * 0.42),
            (sx, y + h * 0.86),
            (sx + w / 2, y + h * 0.42),
            (sx + w / 2, y - h * 0.10),
        ]
        draw.polygon(pts, fill=color)
        draw.ellipse([sx - w / 2, y - h * 0.62, sx, y + h * 0.22], fill=color)
        draw.ellipse([sx, y - h * 0.62, sx + w / 2, y + h * 0.22], fill=color)
        if i == 0:
            # pull-through stem
            draw.line([(sx, y + h * 0.86), (sx, y - h * 0.95)], fill=color,
                      width=max(2, int(rr * 0.05)))


def draw_bear(draw: ImageDraw.ImageDraw, size: int, cx: float, cy: float, r: float,
              color=(255, 244, 228, 255)) -> None:
    """Bear face: two ears, two eyes, muzzle + nose."""
    sx, sy, rr = cx * size, cy * size, r * size
    for sgn in (-1, 1):
        ex, ey = sx + sgn * rr * 0.44, sy - rr * 0.46
        draw.ellipse([ex - rr * 0.20, ey - rr * 0.20, ex + rr * 0.20, ey + rr * 0.20], fill=color)
        draw.ellipse([ex - rr * 0.10, ey - rr * 0.10, ex + rr * 0.10, ey + rr * 0.10],
                     fill=(150, 92, 46, 255))
    for sgn in (-1, 1):
        ex, ey = sx + sgn * rr * 0.24, sy - rr * 0.14
        draw.ellipse([ex - rr * 0.075, ey - rr * 0.085, ex + rr * 0.075, ey + rr * 0.085], fill=color)
    # muzzle
    draw.ellipse([sx - rr * 0.30, sy + rr * 0.02, sx + rr * 0.30, sy + rr * 0.46], fill=color)
    draw.ellipse([sx - rr * 0.11, sy + rr * 0.08, sx + rr * 0.11, sy + rr * 0.26],
                 fill=(150, 92, 46, 255))
    draw.arc([sx - rr * 0.16, sy + rr * 0.16, sx, sy + rr * 0.40], 0, 160,
             fill=(150, 92, 46, 255), width=max(2, int(rr * 0.035)))
    draw.arc([sx, sy + rr * 0.16, sx + rr * 0.16, sy + rr * 0.40], 20, 180,
             fill=(150, 92, 46, 255), width=max(2, int(rr * 0.035)))


def heart_points(sx: float, sy: float, w: float, h: float) -> list[tuple[float, float]]:
    pts = []
    for i in range(180):
        t = 2 * math.pi * i / 180
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((sx + x * w / 34.0, sy + y * h / 34.0))
    return pts


def draw_hearts(draw: ImageDraw.ImageDraw, size: int, cx: float, cy: float, r: float) -> None:
    """Two cocoa-powder hearts — lighter upper-right, darker lower-left.

    Anchors/sizes read off the reference: the upper heart is centred ~0.44r
    above the crema centre and the lower one ~0.34r to the left, and both are
    the same height (~0.95r) with the darker one overlapping the lighter.
    """
    sx, sy, rr = cx * size, cy * size, r * size
    # lighter, upper-right
    draw.polygon(heart_points(sx - rr * 0.02, sy - rr * 0.60, rr * 0.71, rr * 0.95),
                 fill=(146, 92, 50, 205))
    # darker, lower-left — drawn last so it sits on top where they meet
    draw.polygon(heart_points(sx - rr * 0.34, sy - rr * 0.11, rr * 0.63, rr * 0.95),
                 fill=(84, 44, 20, 248))


# --------------------------------------------------------------------------- #
# cup renderers
# --------------------------------------------------------------------------- #
def ellipse_mask(w: int, h: int, cx: float, cy: float, rx: float, ry: float,
                 blur: float) -> Image.Image:
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))


def ellipse_layer(w: int, h: int, cx: float, cy: float, rx: float, ry: float,
                  color, blur: float = 1.0) -> Image.Image:
    layer = Image.new("RGBA", (w, h), color)
    layer.putalpha(ellipse_mask(w, h, cx, cy, rx, ry, blur).point(
        lambda v, a=color[3]: int(v * a / 255)))
    return layer


def ring_ellipse_layer(w: int, h: int, cx: float, cy: float, rx: float, ry: float,
                       width: float, color, blur: float = 1.0) -> Image.Image:
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse(
        [cx - rx + width / 2, cy - ry + width / 2,
         cx + rx - width / 2, cy + ry - width / 2],
        outline=255, width=max(1, int(width)),
    )
    m = m.filter(ImageFilter.GaussianBlur(blur))
    layer = Image.new("RGBA", (w, h), color)
    layer.putalpha(m.point(lambda v, a=color[3]: int(v * a / 255)))
    return layer


def render_hero_cup(path: Path, size: int, seed: int = 11) -> None:
    """The hero cup — a top-down latte on a saucer, two cocoa hearts.

    Proportions were read straight off the reference at a 1440px viewport: the
    saucer measures x 772..1183 by y 242..654, i.e. 412 x 413 — circular, and
    centred on (977, 448). The cup ring is ~0.83 of the saucer and the crema
    ~0.67, with the cup sitting a little left of and below the saucer centre.

        saucer rx .480   ry .480   centre (.500, .500)
        cup    r  .371             centre (.476, .512)
        crema  r  .321             centre (.476, .512)

    Everything is expressed as a fraction of the square canvas, so the caller
    only has to size the canvas: saucer_px = canvas * 0.960.
    """
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    SAUCER_RX, SAUCER_RY = 0.480, 0.480
    CUP_C = (0.476, 0.512)
    CUP_R = 0.371
    CREMA_R = 0.303

    scx, scy = 0.5 * S, 0.5 * S
    srx, sry = SAUCER_RX * S, SAUCER_RY * S
    ccx, ccy = CUP_C[0] * S, CUP_C[1] * S
    cup_px = CUP_R * S
    crema_px = CREMA_R * S

    # --- saucer -----------------------------------------------------------
    # radial shading: bright at the rim, a touch darker in the well
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.sqrt(((xx - scx) / srx) ** 2 + ((yy - scy) / sry) ** 2)
    t = np.clip(d, 0, 1) ** 1.7
    inner = np.array((255, 255, 255), np.float32)
    outer = np.array((241, 237, 230), np.float32)
    rgb = inner[None, None, :] * (1 - t[..., None]) + outer[None, None, :] * t[..., None]
    a = np.where(d <= 1.0, 255.0, 0.0)
    # soften the very edge so the disc does not alias
    a = np.clip((1.0 - d) * S * 0.06, 0, 1) * 255.0
    saucer = Image.fromarray(
        np.concatenate([rgb, a[..., None]], axis=2).clip(0, 255).astype(np.uint8), "RGBA")
    img = paste(img, saucer)
    # a faint step just inside the rim — reads as the saucer's upturned edge
    img = paste(img, ring_ellipse_layer(S, S, scx, scy, srx * 0.955, sry * 0.955,
                                        S * 0.012, (188, 180, 168, 120), S * 0.005))
    img = paste(img, ring_ellipse_layer(S, S, scx, scy, srx * 0.995, sry * 0.995,
                                        S * 0.008, (255, 255, 255, 200), S * 0.004))

    # contact shadow the cup casts on the saucer
    img = paste(img, ellipse_layer(S, S, ccx + S * 0.010, ccy + S * 0.018,
                                   cup_px * 1.03, cup_px * 1.00,
                                   (132, 120, 106, 120), S * 0.022))

    # --- handle — a porcelain nub at ~25deg, overhanging the saucer rim ----
    h = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(h)
    hd.arc([ccx - cup_px * 1.30, ccy - cup_px * 1.30, ccx + cup_px * 1.30,
            ccy + cup_px * 1.30], start=-4, end=54,
           fill=(252, 250, 247, 255), width=int(cup_px * 0.34))
    h = h.filter(ImageFilter.GaussianBlur(S * 0.003))
    img = paste(img, ellipse_layer(S, S, ccx + S * 0.010, ccy + S * 0.014,
                                   cup_px * 1.02, cup_px * 0.99,
                                   (128, 116, 102, 110), S * 0.018))
    img = paste(img, h)

    # --- cup --------------------------------------------------------------
    img = paste(img, disc(S, CUP_C[0], CUP_C[1], CUP_R, (255, 253, 250, 255),
                          blur=S * 0.0035))
    # rim shading: the porcelain falls away toward the cup's outer edge
    img = paste(img, ring_layer(S, S, ccx, ccy, cup_px * 0.995, S * 0.026,
                                (196, 187, 174, 150), blur=S * 0.008))
    img = paste(img, ring_layer(S, S, ccx, ccy, cup_px * 0.965, S * 0.014,
                                (236, 232, 226, 200), blur=S * 0.005))
    # shadow the rim throws onto the crema
    img = paste(img, ring_layer(S, S, ccx, ccy, crema_px * 1.055, S * 0.020,
                                (150, 116, 78, 110), blur=S * 0.010))

    # --- coffee surface ---------------------------------------------------
    img = paste(img, radial(S, (250, 241, 224), (219, 194, 163),
                            cx=CUP_C[0] - 0.030, cy=CUP_C[1] - 0.030,
                            r=CREMA_R, falloff=2.1))
    img = paste(img, crema_texture(S, ccx, ccy, crema_px, seed + 17))
    img = paste(img, sheen(S, CUP_C[0] - 0.185, CUP_C[1] - 0.205, CREMA_R * 1.55,
                           (255, 247, 232), peak=30))
    img = paste(img, ring_layer(S, S, ccx, ccy, crema_px * 0.995, S * 0.007,
                                (124, 80, 40, 130), blur=S * 0.006))

    # --- cocoa hearts -----------------------------------------------------
    art_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ad = ImageDraw.Draw(art_layer)
    draw_hearts(ad, S, CUP_C[0], CUP_C[1], CREMA_R)
    art_layer = art_layer.filter(ImageFilter.GaussianBlur(S * 0.0045))
    art_layer = powder(art_layer, 0.55, seed + 3, scale=1.0)
    clip = soft_mask(S, S, ccx, ccy, crema_px * 0.97, S * 0.003)
    img = paste(img, Image.composite(art_layer, Image.new("RGBA", (S, S), (0, 0, 0, 0)), clip))

    img = grain(img, 2.6, seed)
    img = img.resize((size, size), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    print("wrote", path.relative_to(ROOT), img.size)


def render_cup(path: Path, size: int, *, crema, rim: float, art: str, seed: int,
               art_color=(255, 248, 236, 255), art_scale: float = 1.0,
               leaves: int = 6) -> None:
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    cup_c = (0.5, 0.5)
    cup_r = 0.492
    cx, cy = cup_c[0] * S, cup_c[1] * S
    cup_px = cup_r * S
    inner_r = cup_r - rim
    inner_px = inner_r * S

    # contact shadow so the cup does not float on a transparent background
    img = paste(img, disc(S, cup_c[0] + 0.006, cup_c[1] + 0.014, cup_r * 1.015,
                          (96, 78, 62, 90), blur=S * 0.020))

    # cup body
    img = paste(img, disc(S, cup_c[0], cup_c[1], cup_r, (255, 253, 250, 255), blur=S * 0.004))
    img = paste(img, ring_layer(S, S, cx, cy, cup_px, S * 0.010, (198, 189, 176, 105),
                                blur=S * 0.006))

    # coffee surface — flat-ish crema, off-centre sheen, liquid mottling
    img = paste(img, radial(S, crema[0], crema[1], cx=cup_c[0] - 0.035, cy=cup_c[1] - 0.035,
                            r=inner_r, falloff=2.0))
    img = paste(img, crema_texture(S, cx, cy, inner_px, seed + 17))
    img = paste(img, sheen(S, cup_c[0] - 0.20, cup_c[1] - 0.24, inner_r * 1.5,
                           (255, 246, 228), peak=34))

    # meniscus — faint darker line where the crema meets the porcelain
    img = paste(img, ring_layer(S, S, cx, cy, inner_px * 0.99, S * 0.008,
                                (122, 78, 38, 120), blur=S * 0.007))

    # latte art
    art_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ad = ImageDraw.Draw(art_layer)
    if art == "rosetta":
        draw_rosetta(ad, S, cup_c[0] - 0.005, cup_c[1] + 0.015, inner_r * 0.86 * art_scale,
                     color=art_color, leaves=leaves)
    elif art == "tulip":
        draw_tulip(ad, S, cup_c[0], cup_c[1] + 0.02, inner_r * 0.84 * art_scale,
                   color=art_color)
    elif art == "bear":
        draw_bear(ad, S, cup_c[0], cup_c[1], inner_r * 0.86 * art_scale, color=art_color)
    elif art == "hearts":
        draw_hearts(ad, S, cup_c[0], cup_c[1], inner_r * 0.92 * art_scale)
    art_layer = art_layer.filter(ImageFilter.GaussianBlur(S * 0.0035))
    if art in ("hearts", "bear"):
        art_layer = powder(art_layer, 0.5, seed + 3, scale=1.1)
    # keep the art inside the cup (pixel-space mask!)
    clip = soft_mask(S, S, cx, cy, inner_px * 0.965, S * 0.003)
    img = paste(img, Image.composite(art_layer, Image.new("RGBA", (S, S), (0, 0, 0, 0)), clip))

    img = grain(img, 3.0, seed)
    img = img.resize((size, size), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    print("wrote", path.relative_to(ROOT), img.size)


# --------------------------------------------------------------------------- #
# background
# --------------------------------------------------------------------------- #
def render_bg(path: Path) -> None:
    """The fixed bokeh backdrop behind the glass shell.

    The reference shows clearly readable out-of-focus discs with plenty of
    warm tonal variation — light cream highlights up top, deep coffee browns
    through the middle and bottom. An earlier pass used low alphas plus a 38px
    global blur, which flattened the whole thing into a smooth gradient and
    left the page looking pale and dead.
    """
    W, H = 2400, 1600
    base = Image.new("RGB", (W, H), (178, 164, 146))

    # broad tonal masses — mirrors the CSS fallback gradient stack
    layers = [
        ((0.08, 0.58), 0.78, (66, 40, 36), 190),
        ((0.00, 0.66), 0.55, (128, 54, 52), 150),
        ((1.00, 0.40), 0.74, (54, 44, 40), 195),
        ((0.46, 0.14), 0.64, (228, 219, 204), 175),
        ((0.66, 0.88), 0.72, (108, 94, 80), 185),
        ((0.30, 0.96), 0.60, (86, 70, 58), 150),
        ((0.86, 0.78), 0.50, (196, 176, 150), 120),
    ]
    for (fx, fy), r, col, alpha in layers:
        d = max(W, H) * r * 2
        blob = radial(d, col, col, r=0.5)
        blob.putalpha(blob.getchannel("A").point(lambda v, a=alpha: int(v * a / 255)))
        base.paste(blob, (int(fx * W - d / 2), int(fy * H - d / 2)), blob)

    # warm bokeh discs — these carry most of the reference's texture
    rnd = random.Random(20240919)
    bokeh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _ in range(230):
        r = rnd.randint(46, 300)
        x = rnd.uniform(-r, W + r)
        y = rnd.uniform(-r, H + r)
        tone = rnd.choice([
            (244, 234, 216), (218, 198, 168), (176, 146, 112),
            (112, 84, 62), (238, 222, 198), (146, 110, 80),
            (92, 66, 50), (204, 178, 142),
        ])
        a = rnd.randint(46, 138)
        bokeh = paste(bokeh, circle_layer(W, H, x, y, r, (*tone, a), blur=r * 0.13))
    base = Image.alpha_composite(base.convert("RGBA"), bokeh)

    # only a light global softening; the discs must stay readable
    base = base.filter(ImageFilter.GaussianBlur(11))
    base = grain(base.convert("RGBA"), 3.0, 3)
    path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(path, quality=88, optimize=True, progressive=True)
    print("wrote", path.relative_to(ROOT), base.size)


def main() -> None:
    render_bg(BG_OUT / "coffee-bokeh.jpg")

    render_hero_cup(CUP_OUT / "hero-heart.png", 900, seed=11)

    # The two showcase drinks are dark-roast pours: an espresso-brown surface
    # with cream latte art, exactly as they read on the reference.
    render_cup(CUP_OUT / "americano.png", 640, crema=((132, 86, 48), (72, 40, 20)),
               rim=0.040, art="rosetta", seed=21, leaves=8, art_scale=1.14)

    render_cup(CUP_OUT / "cappuccino-bear.png", 640, crema=((120, 74, 40), (62, 34, 16)),
               rim=0.040, art="bear", seed=31, art_scale=1.08)

    # The feature latte is a light, saturated orange pour with white art.
    render_cup(CUP_OUT / "rosetta-large.png", 900, crema=((242, 200, 138), (204, 134, 58)),
               rim=0.020, art="rosetta", seed=41, leaves=9, art_scale=1.16)

    render_cup(CUP_OUT / "latte-small.png", 256, crema=((236, 196, 142), (196, 130, 66)),
               rim=0.032, art="rosetta", seed=51, leaves=5)


if __name__ == "__main__":
    main()
