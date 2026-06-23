#!/usr/bin/env python3
"""Split hero cat.png into body and animated tail-tip layers."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "static/img/hero/cat.png"
OUTPUT_DIR = ROOT / "static/img/hero"

# Tail-tip polygon on the full 1536x1024 canvas (last ~30% of the curled tail).
TAIL_TIP_POLYGON: tuple[tuple[int, int], ...] = (
    (868, 826),
    (944, 812),
    (1016, 844),
    (1068, 892),
    (1085, 914),
    (1076, 952),
    (1036, 982),
    (952, 986),
    (896, 968),
    (862, 922),
    (854, 872),
)

# Pivot for CSS transform-origin (percent of canvas).
PIVOT_X_PERCENT = 59.0
PIVOT_Y_PERCENT = 80.0


def polygon_mask(size: tuple[int, int], polygon: tuple[tuple[int, int], ...]) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    return mask


def save_webp(image: Image.Image, path: Path) -> None:
    image.save(path, format="WEBP", quality=88, method=6)


def main() -> None:
    source = Image.open(INPUT_PATH).convert("RGBA")
    size = source.size
    tip_mask = polygon_mask(size, TAIL_TIP_POLYGON)

    source_alpha = source.getchannel("A")
    outside_tip = tip_mask.point(lambda value: 255 - value)

    tail_mask = ImageChops.multiply(tip_mask, source_alpha)

    body = source.copy()
    body.putalpha(ImageChops.multiply(source_alpha, outside_tip))

    tail = Image.new("RGBA", size, (0, 0, 0, 0))
    tail.paste(source, mask=tail_mask)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    body_path = OUTPUT_DIR / "cat-body.png"
    tail_path = OUTPUT_DIR / "cat-tail-tip.png"
    body.save(body_path, optimize=True)
    tail.save(tail_path, optimize=True)
    save_webp(body, OUTPUT_DIR / "cat-body.webp")
    save_webp(tail, OUTPUT_DIR / "cat-tail-tip.webp")

    # Debug overlay for manual mask tuning.
    preview = source.copy()
    overlay = Image.new("RGBA", size, (255, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.polygon(TAIL_TIP_POLYGON, outline=(255, 64, 64, 220), fill=(255, 64, 64, 72))
    pivot_x = int(size[0] * PIVOT_X_PERCENT / 100)
    pivot_y = int(size[1] * PIVOT_Y_PERCENT / 100)
    overlay_draw.ellipse(
        (pivot_x - 8, pivot_y - 8, pivot_x + 8, pivot_y + 8),
        fill=(64, 128, 255, 255),
    )
    preview = Image.alpha_composite(preview, overlay)
    preview.save(OUTPUT_DIR / "cat-tail-split-preview.png")

    body_arr = body.getchannel("A")
    tail_arr = tail.getchannel("A")
    body_pixels = sum(1 for alpha in body_arr.get_flattened_data() if alpha > 0)
    tail_pixels = sum(1 for alpha in tail_arr.get_flattened_data() if alpha > 0)
    print(f"Saved {body_path} ({body_pixels} opaque px)")
    print(f"Saved {tail_path} ({tail_pixels} opaque px)")
    print(f"Pivot CSS: {PIVOT_X_PERCENT}% {PIVOT_Y_PERCENT}%")


if __name__ == "__main__":
    main()
