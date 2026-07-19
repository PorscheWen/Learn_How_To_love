"""Aggressive chroma cleanup for FLUX dog poses painted on green.

FLUX 2 Pro paints shadows and canvas-texture strokes on the requested
chroma-green backdrop; the strict key in remove_char_bg.py leaves those
dark-green / teal blobs behind. This pass:

1. runs the strict boundary chroma key (same rule as remove_char_bg.py),
2. grows the transparent region into loosely greenish/teal pixels,
3. keeps only the largest opaque component (drops stray paint scratches),
4. decontaminates the one-pixel green fringe.

Honey-tan / cream / dark-brown dog fur is red-dominant or neutral, so the
loose green test never reaches inside the puppy.
"""

from collections import deque
from pathlib import Path
import sys

from PIL import Image


def is_strict_chroma(r: int, g: int, b: int) -> bool:
    return (
        g >= 105
        and g - r >= 34
        and g - b >= 34
        and g >= int(max(r, b) * 1.22)
    )


def is_loose_greenish(r: int, g: int, b: int) -> bool:
    # Dark painterly green shadows and teal strokes: green (or blue-green)
    # clearly dominates red. Fur is red-dominant, so this stays outside.
    if g >= r + 12 and g >= 30:
        return True
    if b >= r + 22 and g >= r + 6:
        return True
    return False


def clean(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    pixels = image.load()
    width, height = image.size
    total = width * height

    visited = bytearray(total)
    queue: deque[tuple[int, int]] = deque()

    def enqueue_strict(x: int, y: int) -> None:
        index = y * width + x
        if visited[index]:
            return
        r, g, b, a = pixels[x, y]
        if a > 0 and is_strict_chroma(r, g, b):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue_strict(x, 0)
        enqueue_strict(x, height - 1)
    for y in range(height):
        enqueue_strict(0, y)
        enqueue_strict(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                enqueue_strict(nx, ny)

    # Enclosed strict-chroma pockets.
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if not visited[index]:
                r, g, b, a = pixels[x, y]
                if a > 0 and is_strict_chroma(r, g, b):
                    visited[index] = 1

    for y in range(height):
        for x in range(width):
            if visited[y * width + x]:
                r, g, b, _ = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)

    # Grow transparency into loosely greenish/teal shadow strokes.
    grow: deque[tuple[int, int]] = deque()
    seen = bytearray(total)
    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] == 0:
                seen[y * width + x] = 1
                grow.append((x, y))
    removed_loose = 0
    while grow:
        x, y = grow.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            index = ny * width + nx
            if seen[index]:
                continue
            r, g, b, a = pixels[nx, ny]
            if a > 0 and is_loose_greenish(r, g, b):
                seen[index] = 1
                pixels[nx, ny] = (r, g, b, 0)
                removed_loose += 1
                grow.append((nx, ny))

    # Keep only the largest opaque component (the puppy).
    labels = [0] * total
    current = 0
    sizes = {}
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if labels[index] or pixels[x, y][3] == 0:
                continue
            current += 1
            labels[index] = current
            component = deque([(x, y)])
            size = 0
            while component:
                cx, cy = component.popleft()
                size += 1
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    nindex = ny * width + nx
                    if labels[nindex] == 0 and pixels[nx, ny][3] > 0:
                        labels[nindex] = current
                        component.append((nx, ny))
            sizes[current] = size

    removed_blobs = 0
    if sizes:
        keep = max(sizes, key=sizes.get)
        for y in range(height):
            for x in range(width):
                index = y * width + x
                if labels[index] and labels[index] != keep:
                    r, g, b, _ = pixels[x, y]
                    pixels[x, y] = (r, g, b, 0)
                    removed_blobs += 1

    # Decontaminate the green fringe touching transparency.
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            r, g, b, a = pixels[x, y]
            if a == 0 or g <= max(r, b) + 10:
                continue
            touches = any(
                pixels[x + dx, y + dy][3] == 0
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
            )
            if touches:
                pixels[x, y] = (r, min(g, max(r, b) + 6), b, a)

    image.save(destination)
    print(
        f"OK {source.name} -> {destination.name}: "
        f"loose_removed={removed_loose}, stray_blobs={removed_blobs}",
        flush=True,
    )


def main() -> None:
    dog_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parents[1] / "assets" / "dog"
    )
    sources = sorted(dog_dir.glob("dog-*-green.png"))
    if not sources:
        raise SystemExit(f"No dog-*-green.png in {dog_dir}")
    for source in sources:
        clean(source, source.with_name(source.name.replace("-green.png", ".png")))


if __name__ == "__main__":
    main()
