"""Generate favicons for EPIC coming soon page.

Uses the L-bracket motif from the EPIC logo, in white on a navy background
so it reads clearly in browser tabs and on dark/light themes.
"""
from PIL import Image, ImageDraw

NAVY = (13, 34, 64, 255)      # #0d2240
WHITE = (255, 255, 255, 255)


def make_icon(size: int, *, rounded: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if rounded:
        # Rounded square (Apple touch icon style)
        radius = int(size * 0.22)
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=NAVY)
    else:
        draw.rectangle((0, 0, size, size), fill=NAVY)

    # L-bracket: both arms run almost the full length of the icon, matching the
    # proportions of the logo's bracket — vertical arm reaches near the top edge,
    # horizontal arm reaches near the right edge, with equal inset from both.
    inset = max(2, int(size * 0.16))
    stroke = max(2, int(size * 0.10))

    # Vertical arm (left side, full height)
    draw.rectangle(
        (inset, inset, inset + stroke, size - inset),
        fill=WHITE,
    )
    # Horizontal arm (bottom side, full width)
    draw.rectangle(
        (inset, size - inset - stroke, size - inset, size - inset),
        fill=WHITE,
    )

    return img


def main() -> None:
    base_dir = "/Users/ryan/Desktop/epic-coming-soon-page"

    # Standard favicon sizes
    sizes = [16, 32, 48, 64, 180]
    images = {s: make_icon(s) for s in sizes}

    # ICO file (multi-resolution, contains 16/32/48)
    images[48].save(
        f"{base_dir}/favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    # PNG variants
    images[32].save(f"{base_dir}/favicon-32.png", format="PNG")
    images[16].save(f"{base_dir}/favicon-16.png", format="PNG")

    # Apple touch icon (rounded, larger)
    apple = make_icon(180, rounded=True)
    apple.save(f"{base_dir}/apple-touch-icon.png", format="PNG")

    print("favicon.ico, favicon-16.png, favicon-32.png, apple-touch-icon.png written")


if __name__ == "__main__":
    main()
