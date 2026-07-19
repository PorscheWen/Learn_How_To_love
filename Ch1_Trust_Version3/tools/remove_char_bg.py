"""Remove a chroma-green backdrop without erasing light character details.

The key targets only strongly green pixels, unlike the old cream threshold that
was too close to skin and clothing colors. Boundary-connected green is removed
first, then enclosed green-screen pockets between hair, arms and bags are keyed.
Input files end in ``-green.png``; final files drop that suffix.
"""

from collections import deque
from pathlib import Path

from PIL import Image


CHAR_DIR = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "char"
)


def is_chroma(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return (
        a > 0
        and g >= 105
        and g - r >= 34
        and g - b >= 34
        and g >= int(max(r, b) * 1.22)
    )


def remove_connected_chroma(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    pixels = image.load()
    width, height = image.size

    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def enqueue(x: int, y: int) -> None:
        index = y * width + x
        if visited[index] or not is_chroma(pixels[x, y]):
            return
        visited[index] = 1
        queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y > 0:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    # Green-screen pockets can be enclosed by hair, arms or a transparent bag
    # and therefore cannot be reached from the canvas boundary.
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if not visited[index] and is_chroma(pixels[x, y]):
                visited[index] = 1

    removed = 0
    for y in range(height):
        for x in range(width):
            if visited[y * width + x]:
                r, g, b, _ = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
                removed += 1

    # Decontaminate the one-pixel green fringe without changing alpha elsewhere.
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            r, g, b, a = pixels[x, y]
            if a == 0 or g <= max(r, b) + 16:
                continue
            touches_transparency = any(
                pixels[x + dx, y + dy][3] == 0
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
            )
            if touches_transparency:
                pixels[x, y] = (r, min(g, max(r, b) + 8), b, a)

    image.save(destination)
    print(
        f"OK {source.name} -> {destination.name}: "
        f"removed={removed}, size={width}x{height}"
    )


def main() -> None:
    import sys

    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else CHAR_DIR
    pattern = sys.argv[2] if len(sys.argv) > 2 else "char-*-green.png"
    sources = sorted(target_dir.glob(pattern))
    if not sources:
        raise SystemExit(f"No {pattern} inputs found in {target_dir}.")

    for source in sources:
        destination = source.with_name(source.name.replace("-green.png", ".png"))
        remove_connected_chroma(source, destination)


if __name__ == "__main__":
    main()
