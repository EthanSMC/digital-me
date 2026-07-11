#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


WIDTH = 1080
HEIGHT = 1920
FPS = 30
BLACK = "#222222"
PALETTE = {
    "black": BLACK,
    "blue": "#2f6fed",
    "orange": "#ff6827",
    "red": "#d93824",
    "white": "#ffffff",
}
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)


def resolve_path(project_dir: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = project_dir / path
    return path


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    configured = os.environ.get("DIGITAL_ME_FONT")
    candidates = ([configured] if configured else []) + FONT_CANDIDATES
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def color(value: str | None) -> str:
    if not value:
        return BLACK
    return PALETTE.get(value, value)


def wrap_text(text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    if not text:
        return []
    lines: list[str] = []
    current = ""
    probe = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(probe)
    for char in text:
        candidate = current + char
        bbox = draw.textbbox((0, 0), candidate, font=fnt)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def draw_center(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, fill: str, bold: bool = True) -> None:
    fnt = font(size, bold)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, fill=fill, font=fnt)


def draw_pill(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, fill: str) -> None:
    fnt = font(size, True)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (WIDTH - text_w) // 2
    pad_x = 22
    pad_y = 12
    draw.rounded_rectangle(
        (x - pad_x, y - pad_y, x + text_w + pad_x, y + text_h + pad_y),
        radius=20,
        fill="white",
    )
    draw.text((x, y), text, fill=fill, font=fnt)


def draw_subtitles(draw: ImageDraw.ImageDraw, lines: list[str]) -> None:
    fnt = font(34, True)
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(wrap_text(line, fnt, 900))
    wrapped = wrapped[:3]
    if not wrapped:
        return
    line_h = 46
    box_h = 42 + line_h * len(wrapped)
    y1 = HEIGHT - box_h - 34
    draw.rounded_rectangle((70, y1, WIDTH - 70, HEIGHT - 34), radius=24, fill="white")
    y = y1 + 22
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        x = (WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=BLACK, font=fnt)
        y += line_h


def load_canvas(image_path: Path, fit: str) -> Image.Image:
    img = Image.open(image_path).convert("RGB")
    if fit == "stretch":
        return img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    if fit == "crop":
        return ImageOps.fit(img, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    contained = ImageOps.contain(img, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "white")
    canvas.paste(contained, ((WIDTH - contained.width) // 2, (HEIGHT - contained.height) // 2))
    return canvas


def as_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def bake_frame(shot: dict[str, Any], project_dir: Path, out: Path, fit: str) -> None:
    source = resolve_path(project_dir, str(shot["image"]))
    if not source.exists():
        raise FileNotFoundError(source)
    canvas = load_canvas(source, fit)
    draw = ImageDraw.Draw(canvas)

    for item in shot.get("top", []):
        text = str(item["text"])
        draw_center(
            draw,
            int(item.get("y", 76)),
            text,
            int(item.get("size", 48)),
            color(item.get("color")),
            bool(item.get("bold", True)),
        )

    for item in shot.get("bottom", []):
        draw_pill(
            draw,
            int(item.get("y", 1640)),
            str(item["text"]),
            int(item.get("size", 38)),
            color(item.get("color")),
        )

    draw_subtitles(draw, as_lines(shot.get("subtitle")))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=95)


def write_narration(shots: list[dict[str, Any]], out: Path) -> None:
    parts: list[str] = []
    for shot in shots:
        parts.extend(as_lines(shot.get("subtitle")))
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(part.strip() for part in parts if part.strip())
    out.write_text(f"{text}\n" if text else "", encoding="utf-8")


def render_clip(frame: Path, duration: float, out: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-t",
            str(duration),
            "-i",
            str(frame),
            "-vf",
            f"scale={WIDTH}:{HEIGHT},format=yuv420p",
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(out),
        ]
    )


def render_video(frame_paths: list[Path], shots: list[dict[str, Any]], audio: Path | None, out: Path, work_dir: Path) -> None:
    clip_dir = work_dir / "clips"
    clip_dir.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    for idx, (frame, shot) in enumerate(zip(frame_paths, shots), start=1):
        clip = clip_dir / f"{idx:02d}_{frame.stem}.mp4"
        render_clip(frame, float(shot.get("duration", 4)), clip)
        clip_paths.append(clip)

    concat = clip_dir / "concat.txt"
    concat.write_text("".join(f"file '{path}'\n" for path in clip_paths), encoding="utf-8")
    combined = clip_dir / "combined.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(combined)])

    out.parent.mkdir(parents=True, exist_ok=True)
    if audio:
        if not audio.exists():
            raise FileNotFoundError(audio)
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(combined),
                "-i",
                str(audio),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-shortest",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-movflags",
                "+faststart",
                str(out),
            ]
        )
    else:
        run(["ffmpeg", "-y", "-i", str(combined), "-c", "copy", "-movflags", "+faststart", str(out)])


def load_shots(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("Shot plan must be a non-empty JSON array.")
    for idx, shot in enumerate(data, start=1):
        if "image" not in shot:
            raise ValueError(f"Shot {idx} is missing image.")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a vertical still-frame social video from a JSON shot plan.")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--shots", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--fit", choices=["contain", "crop", "stretch"], default="contain")
    parser.add_argument("--frames-only", action="store_true")
    parser.add_argument("--narration-out", type=Path)
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    shots = load_shots(args.shots)
    out = resolve_path(project_dir, str(args.out))
    work_dir = resolve_path(project_dir, str(args.work_dir)) if args.work_dir else out.parent / f"{out.stem}_render"
    frame_dir = work_dir / "frames"
    frame_paths: list[Path] = []

    for idx, shot in enumerate(shots, start=1):
        frame = frame_dir / f"{idx:02d}.png"
        bake_frame(shot, project_dir, frame, args.fit)
        frame_paths.append(frame)

    if args.narration_out:
        write_narration(shots, resolve_path(project_dir, str(args.narration_out)))

    if not args.frames_only:
        audio = resolve_path(project_dir, str(args.audio)) if args.audio else None
        render_video(frame_paths, shots, audio, out, work_dir)

    print(
        json.dumps(
            {
                "frames": [str(path) for path in frame_paths],
                "out": str(out) if not args.frames_only else None,
                "duration_seconds": sum(float(shot.get("duration", 4)) for shot in shots),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
