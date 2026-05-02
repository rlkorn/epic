"""Generate the social share image (og-image.png) for the EPIC coming soon page.

Produces a 1200x630 PNG with the EPIC logo centered above the tagline and a
"Coming 2026" eyebrow — matching the on-page composition so the share preview
feels continuous with the destination.
"""
from PIL import Image, ImageDraw, ImageFont

NAVY = (13, 34, 64, 255)
INK = (26, 26, 26, 255)
MUTED = (95, 100, 112, 255)
WHITE = (255, 255, 255, 255)

WIDTH, HEIGHT = 1200, 630
LOGO_PATH = "/Users/ryan/Desktop/epic-coming-soon-page/EPIC_Logo_1600px.png"
OUT_PATH = "/Users/ryan/Desktop/epic-coming-soon-page/og-image.png"

GEORGIA_ITALIC = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
HELVETICA_NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def main() -> None:
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(canvas)

    # Logo: paste centered, sized to ~360px tall (square logo)
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 360
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_x = (WIDTH - logo_size) // 2
    logo_y = 70
    canvas.paste(logo, (logo_x, logo_y), logo)

    # Tagline (italic serif), centered beneath the logo
    tagline = "Nonpartisan ideas for a new era of civic progress."
    tagline_font = ImageFont.truetype(GEORGIA_ITALIC, 34)
    tw = text_width(draw, tagline, tagline_font)
    tagline_y = logo_y + logo_size + 36
    draw.text(((WIDTH - tw) // 2, tagline_y), tagline, font=tagline_font, fill=INK)

    # "COMING 2026" eyebrow with thin navy rules on either side
    eyebrow = "COMING  2026"  # double space to mimic letter-spacing
    eyebrow_font = ImageFont.truetype(HELVETICA_NEUE, 18, index=2)  # index 2 ≈ Bold
    # Add tracking by inserting hair spaces between characters
    spaced = " ".join(eyebrow)
    ew = text_width(draw, spaced, eyebrow_font)
    eyebrow_y = tagline_y + 60
    eyebrow_x = (WIDTH - ew) // 2
    draw.text((eyebrow_x, eyebrow_y), spaced, font=eyebrow_font, fill=NAVY)

    # Rules to the left and right of the eyebrow text
    rule_len = 60
    rule_gap = 20
    rule_y = eyebrow_y + 12  # vertical center of caps
    draw.rectangle(
        (eyebrow_x - rule_gap - rule_len, rule_y, eyebrow_x - rule_gap, rule_y + 1),
        fill=NAVY,
    )
    draw.rectangle(
        (eyebrow_x + ew + rule_gap, rule_y, eyebrow_x + ew + rule_gap + rule_len, rule_y + 1),
        fill=NAVY,
    )

    canvas.convert("RGB").save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
