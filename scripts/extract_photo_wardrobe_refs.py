#!/usr/bin/env python3
"""Extract wardrobe crops from user-provided source photos using a JSON config."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def crop_box(image: Image.Image, spec: dict[str, Any]) -> tuple[int, int, int, int]:
    if "box" in spec:
        x0, y0, x1, y1 = spec["box"]
        return int(x0), int(y0), int(x1), int(y1)
    if "box_rel" in spec:
        x0, y0, x1, y1 = spec["box_rel"]
        return (
            int(image.width * x0),
            int(image.height * y0),
            int(image.width * x1),
            int(image.height * y1),
        )
    raise ValueError("Crop must include either 'box' or 'box_rel'.")


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
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    output = args.output
    sources_dir = output / "sources"
    cropped_dir = output / "cropped"
    sources_dir.mkdir(parents=True, exist_ok=True)
    cropped_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "persona": config.get("persona", "personal-ip"),
        "source": "user-provided original photos",
        "items": [],
    }
    category_paths: dict[str, list[Path]] = {}

    for source in config.get("sources", []):
        source_path = Path(source["path"]).expanduser()
        if not source_path.exists():
            raise FileNotFoundError(source_path)

        source_name = source.get("copy_name") or f"{source['id']}{source_path.suffix.lower()}"
        copied_source = sources_dir / source_name
        if source.get("copy_source", True):
            shutil.copy2(source_path, copied_source)

        image = Image.open(source_path).convert("RGBA")
        for crop in source.get("crops", []):
            category = crop["category"]
            filename = crop["filename"]
            target_dir = cropped_dir / category
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / filename
            image.crop(crop_box(image, crop)).save(target)
            category_paths.setdefault(category, []).append(target)
            manifest["items"].append({
                "category": category,
                "file": str(target.relative_to(output)),
                "source_photo": str(copied_source.relative_to(output)) if copied_source.exists() else str(source_path),
                "note": crop.get("note", ""),
            })

    for category, paths in category_paths.items():
        make_sheet(paths, cropped_dir / category / "_contact-sheet.jpg", cols=3)
    make_sheet([Path(output / item["file"]) for item in manifest["items"]], output / "clothing-contact-sheet.jpg")

    (output / "wardrobe_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(output)
    print(f"extracted {len(manifest['items'])} wardrobe refs")


if __name__ == "__main__":
    main()

