#!/usr/bin/env python3
"""Build a simple contact sheet from image files or folders."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def collect_images(paths: Iterable[Path], recursive: bool) -> list[Path]:
    images: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            images.append(path)
        elif path.is_dir():
            pattern = "**/*" if recursive else "*"
            images.extend(
                p for p in path.glob(pattern)
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS
            )
    return sorted(images)


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def make_contact_sheet(
    images: list[Path],
    output: Path,
    cols: int,
    thumb_width: int,
    thumb_height: int,
    label_parent: bool,
) -> None:
    if not images:
        raise SystemExit("No images found.")

    pad = 24
    label_h = 64
    rows = (len(images) + cols - 1) // cols
    sheet_w = cols * thumb_width + (cols + 1) * pad
    sheet_h = rows * (thumb_height + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)
    font_title = load_font(16)
    font_meta = load_font(12)

    for idx, path in enumerate(images):
        row, col = divmod(idx, cols)
        x = pad + col * (thumb_width + pad)
        y = pad + row * (thumb_height + label_h + pad)

        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (thumb_width, thumb_height), (250, 250, 248))
        tile.paste(img, ((thumb_width - img.width) // 2, (thumb_height - img.height) // 2))
        sheet.paste(tile, (x, y))

        title = path.stem[:34]
        meta = path.parent.name if label_parent else ""
        draw.text((x, y + thumb_height + 10), title, fill=(34, 34, 34), font=font_title)
        if meta:
            draw.text((x, y + thumb_height + 34), meta, fill=(92, 92, 92), font=font_meta)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Image files or folders.")
    parser.add_argument("--output", "-o", required=True, type=Path)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=260)
    parser.add_argument("--thumb-height", type=int, default=230)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--label-parent", action="store_true")
    args = parser.parse_args()

    images = collect_images(args.paths, args.recursive)
    make_contact_sheet(
        images=images,
        output=args.output,
        cols=args.cols,
        thumb_width=args.thumb_width,
        thumb_height=args.thumb_height,
        label_parent=args.label_parent,
    )
    print(args.output)


if __name__ == "__main__":
    main()

