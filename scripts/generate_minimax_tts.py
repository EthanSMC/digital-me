#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_API_URL = "https://api.minimaxi.com/v1/t2a_v2"


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Text file is empty: {path}")
    return text


def generate_tts(
    *,
    api_key: str,
    text: str,
    out: Path,
    model: str,
    voice_id: str,
    speed: float,
    pitch: int,
    vol: float,
    api_url: str,
) -> None:
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "language_boost": "Chinese",
        "output_format": "hex",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        api_url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    context = None
    try:
        import certifi  # type: ignore

        context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        context = None

    try:
        with urllib.request.urlopen(request, timeout=120, context=context) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MiniMax API HTTP {exc.code}: {detail}") from exc

    data = json.loads(raw.decode("utf-8"))
    base = data.get("base_resp") or {}
    if base.get("status_code") not in (0, "0", None):
        raise RuntimeError(f"MiniMax API error: {base}")

    audio_hex = ((data.get("data") or {}).get("audio") or "").strip()
    if not audio_hex:
        raise RuntimeError(f"MiniMax response did not include audio data. Keys: {sorted(data.keys())}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(bytes.fromhex(audio_hex))
    info = data.get("extra_info") or {}
    print(
        json.dumps(
            {
                "out": str(out),
                "voice_id": voice_id,
                "model": model,
                "audio_format": info.get("audio_format"),
                "audio_length": info.get("audio_length"),
                "usage_characters": info.get("usage_characters"),
            },
            ensure_ascii=False,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MiniMax TTS from a local text file.")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default="speech-2.8-hd")
    parser.add_argument("--voice-id", default="Chinese (Mandarin)_Sincere_Adult")
    parser.add_argument("--speed", type=float, default=0.98)
    parser.add_argument("--pitch", type=int, default=0)
    parser.add_argument("--vol", type=float, default=1.0)
    parser.add_argument("--api-url", default=os.environ.get("MINIMAX_API_URL", DEFAULT_API_URL))
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        print("MINIMAX_API_KEY is not set.", file=sys.stderr)
        raise SystemExit(2)

    generate_tts(
        api_key=api_key,
        text=read_text(args.text),
        out=args.out,
        model=args.model,
        voice_id=args.voice_id,
        speed=args.speed,
        pitch=args.pitch,
        vol=args.vol,
        api_url=args.api_url,
    )


if __name__ == "__main__":
    main()
