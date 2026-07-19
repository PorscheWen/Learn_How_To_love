#!/usr/bin/env python3
"""Remove complex painted backgrounds from generated character/dog sprites."""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from rembg import remove


def decontaminate_green_spill(data: bytes) -> bytes:
    """Neutralize neon chroma spill left on semi-transparent painted edges."""
    image = Image.open(BytesIO(data)).convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            excess = g - max(r, b)
            if a and excess > 30 and (a < 245 or excess > 40):
                pixels[x, y] = (r, max(r, b) + 8, b, a)

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: remove_ai_bg.py INPUT OUTPUT [INPUT OUTPUT ...]")
    args = sys.argv[1:]
    if len(args) % 2:
        raise SystemExit("Inputs and outputs must be supplied in pairs.")

    for source_arg, destination_arg in zip(args[::2], args[1::2]):
        source = Path(source_arg)
        destination = Path(destination_arg)
        destination.parent.mkdir(parents=True, exist_ok=True)
        keyed = remove(source.read_bytes())
        destination.write_bytes(decontaminate_green_spill(keyed))
        print(f"OK {source.name} -> {destination.name} ({destination.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
