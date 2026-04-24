"""Generate a single image via OpenAI gpt-image-2 and save to disk.

Usage:
    py scripts/gen_image.py <out_path> <prompt> [size] [quality]

Reads OPENAI_API_KEY from the User-scope Windows environment registry so
the key never needs to sit in the current shell or a project file.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


def get_api_key() -> str:
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "[Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    key = result.stdout.strip()
    if not key:
        raise SystemExit("OPENAI_API_KEY not found in User-scope environment")
    return key


def generate(out_path: Path, prompt: str, size: str, quality: str) -> None:
    payload = json.dumps(
        {"model": "gpt-image-1", "prompt": prompt, "size": size, "quality": quality, "n": 1}
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {get_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {detail}") from exc

    b64 = body["data"][0]["b64_json"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(b64))
    print(f"OK: {out_path} ({out_path.stat().st_size} bytes)")


def main(argv: list[str]) -> None:
    if len(argv) < 3:
        raise SystemExit("usage: gen_image.py <out_path> <prompt> [size] [quality]")
    out_path = Path(argv[1])
    prompt = argv[2]
    size = argv[3] if len(argv) > 3 else "1024x1024"
    quality = argv[4] if len(argv) > 4 else "medium"
    generate(out_path, prompt, size, quality)


if __name__ == "__main__":
    main(sys.argv)
