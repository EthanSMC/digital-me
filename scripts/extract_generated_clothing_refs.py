#!/usr/bin/env python3
"""Extract clothing refs from successful generated character variants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFont


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def figure_bbox(image: Image.Image, threshold: int = 240) -> tuple[int, int, int, int]:
    red, green, blue = image.convert("RGB").split()
    darkest_channel = ImageChops.darker(ImageChops.darker(red, green), blue)
    foreground = darkest_channel.point(lambda value: 255 if value < threshold else 0)
    detected = foreground.getbbox()
    if detected is None:
        return 0, 0, image.width, image.height

    x0, y0, x1, y1 = detected
    margin_x = int((x1 - x0) * 0.08)
    margin_y = int((y1 - y0) * 0.04)
    return (
        max(0, x0 - margin_x),
        max(0, y0 - margin_y),
        min(image.width, x1 + margin_x),
        min(image.height, y1 + margin_y),
    )


def rel_crop(image: Image.Image, bbox: tuple[int, int, int, int], rel: list[float]) -> Image.Image:
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    rx0, ry0, rx1, ry1 = rel
    box = (
        max(0, int(x0 + bw * rx0)),
        max(0, int(y0 + bh * ry0)),
        min(image.width, int(x0 + bw * rx1)),
        min(image.height, int(y0 + bh * ry1)),
    )
    return image.crop(box)


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_sheet(paths: list[Path], output: Path, cols: int = 4) -> None:
    if not paths:
        return

    thumb_w, thumb_h = 260, 230
    pad = 24
    label_h = 58
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    font_title = load_font(15)
    font_meta = load_font(12)

    for idx, path in enumerate(paths):
        row, col = divmod(idx, cols)
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + label_h + pad)
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (thumb_w, thumb_h), (250, 250, 248))
        tile.paste(img, ((thumb_w - img.width) // 2, (thumb_h - img.height) // 2))
        sheet.paste(tile, (x, y))
        draw.text((x, y + thumb_h + 10), path.stem[:32], fill=(34, 34, 34), font=font_title)
        draw.text((x, y + thumb_h + 32), path.parent.name, fill=(92, 92, 92), font=font_meta)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input-dir", type=Path, help="Directory containing generated variant images.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    input_dir = args.input_dir or Path(config.get("input_dir", "."))
    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "persona": config.get("persona", "personal-ip"),
        "source": "AI-generated character variants",
        "items": [],
    }
    category_paths: dict[str, list[Path]] = {}

    for variant in config.get("variants", []):
        image_path = input_dir / variant["file"]
        if not image_path.exists():
            raise FileNotFoundError(image_path)

        image = Image.open(image_path).convert("RGBA")
        bbox = figure_bbox(image, threshold=int(config.get("white_threshold", 240)))

        for piece in variant.get("pieces", []):
            category = piece["category"]
            filename = piece["filename"]
            target_dir = output / category
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / filename
            rel_crop(image, bbox, piece["box_rel"]).save(target)
            category_paths.setdefault(category, []).append(target)
            manifest["items"].append({
                "category": category,
                "file": str(target.relative_to(output)),
                "source_variant": variant["file"],
                "variant_id": variant.get("id", ""),
                "note": piece.get("note", ""),
            })

    contact_dir = output / "contact_sheets"
    for category, paths in category_paths.items():
        make_sheet(paths, contact_dir / f"{category}-contact-sheet.jpg", cols=3)
    make_sheet([Path(output / item["file"]) for item in manifest["items"]], output / "generated-clothing-contact-sheet.jpg")

    (output / "generated_clothing_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(output)
    print(f"extracted {len(manifest['items'])} generated clothing refs")


if __name__ == "__main__":
    main()
