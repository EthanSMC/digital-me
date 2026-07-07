#!/usr/bin/env python3
"""Export a square avatar as a transparent circular PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


def export_circle_avatar(input_path: Path, out_path: Path, size: int) -> None:
    if size <= 0:
        raise ValueError("size must be positive")
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    source = Image.open(input_path).convert("RGBA")
    avatar = ImageOps.fit(
        source,
        (size, size),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    mask_scale = 4
    mask_size = size * mask_scale
    mask = Image.new("L", (mask_size, mask_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask_size - 1, mask_size - 1), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(0.2))

    output = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    output.paste(avatar, (0, 0), mask)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--size", type=int, default=1024)
    args = parser.parse_args()

    export_circle_avatar(args.input, args.out, args.size)
    print(args.out)


if __name__ == "__main__":
    main()
