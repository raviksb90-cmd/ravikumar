from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "static" / "images"
PROJECT_DIR = IMG_DIR / "projects"


def font(size=28, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def gradient(size, start, end):
    w, h = size
    img = Image.new("RGB", size, start)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / max(h - 1, 1)
        color = tuple(int(start[i] * (1 - ratio) + end[i] * ratio) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return img


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_window(draw, x, y, w, h, fill=(255, 255, 255), border=(226, 232, 240)):
    rounded(draw, (x, y, x + w, y + h), 20, fill, border, 2)
    draw.line((x, y + 54, x + w, y + 54), fill=border, width=2)
    for i, color in enumerate([(239, 68, 68), (245, 158, 11), (16, 185, 129)]):
        draw.ellipse((x + 24 + i * 28, y + 20, x + 38 + i * 28, y + 34), fill=color)


def card_asset(name, title, subtitle, start, end, accent):
    img = gradient((1200, 675), start, end).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(overlay)

    rounded(d, (84, 78, 1116, 594), 34, (255, 255, 255, 232), (226, 232, 240, 255), 2)
    draw_window(d, 150, 132, 520, 354)
    rounded(d, (720, 150, 1048, 224), 18, (*accent, 36), (*accent, 120), 2)
    rounded(d, (720, 256, 1048, 330), 18, (15, 23, 42, 12), (203, 213, 225, 255), 2)
    rounded(d, (720, 362, 1048, 436), 18, (15, 23, 42, 12), (203, 213, 225, 255), 2)

    for i in range(5):
        rounded(d, (190, 220 + i * 42, 590, 238 + i * 42), 9, (148, 163, 184, 80))
    for i, width in enumerate([360, 260, 410]):
        rounded(d, (192, 407 + i * 26, 192 + width, 419 + i * 26), 6, (*accent, 120))

    d.ellipse((822, 185, 946, 309), fill=(*accent, 42), outline=(*accent, 170), width=3)
    d.line((884, 212, 884, 282), fill=(*accent, 210), width=7)
    d.line((849, 247, 919, 247), fill=(*accent, 210), width=7)
    d.arc((806, 170, 962, 326), 28, 322, fill=(*accent, 150), width=6)

    d.text((150, 520), title, font=font(42, True), fill=(15, 23, 42, 255))
    d.text((152, 568), subtitle, font=font(24), fill=(71, 85, 105, 255))

    img = Image.alpha_composite(img, overlay).convert("RGB")
    img.save(PROJECT_DIR / name, quality=92)


def hero_asset():
    img = gradient((900, 900), (248, 250, 252), (219, 234, 254)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.ellipse((70, 64, 830, 824), fill=(255, 255, 255, 190), outline=(203, 213, 225, 255), width=3)
    draw_window(d, 170, 210, 560, 420)

    rounded(d, (235, 324, 455, 360), 12, (15, 118, 110, 56))
    rounded(d, (235, 384, 620, 410), 10, (100, 116, 139, 80))
    rounded(d, (235, 434, 560, 460), 10, (100, 116, 139, 60))
    rounded(d, (235, 484, 640, 510), 10, (100, 116, 139, 60))
    rounded(d, (235, 534, 520, 560), 10, (100, 116, 139, 60))

    d.arc((525, 318, 665, 458), 210, 510, fill=(14, 165, 233, 210), width=10)
    d.line((590, 380, 630, 420), fill=(14, 165, 233, 210), width=10)
    d.line((590, 380, 550, 422), fill=(14, 165, 233, 210), width=10)

    d.text((204, 684), "Full-Stack Web Developer", font=font(34, True), fill=(15, 23, 42, 255))
    d.text((262, 732), "SaaS | MERN | AI APIs | Electron", font=font(24), fill=(71, 85, 105, 255))
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=105, threshold=2)).convert("RGB")
    img.save(IMG_DIR / "developer-workspace.png", quality=94)


def favicon_asset():
    img = gradient((256, 256), (15, 118, 110), (14, 165, 233)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 238, 238), radius=44, outline=(255, 255, 255, 160), width=4)
    d.text((56, 78), "RK", font=font(78, True), fill=(255, 255, 255, 255))
    d.text((60, 154), "DEV", font=font(28, True), fill=(219, 234, 254, 255))
    img.convert("RGB").save(ROOT / "static" / "fav.png", quality=95)


def main():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    favicon_asset()
    hero_asset()
    cards = [
        ("product-platform.png", "Product Platforms", "SaaS, admin portals, payments", (236, 253, 245), (224, 242, 254), (15, 118, 110)),
        ("automation-desktop.png", "Desktop Automation", "Electron apps and report workflows", (241, 245, 249), (254, 243, 199), (217, 119, 6)),
        ("studio-booking.png", "Booking Systems", "Scheduling, payments, client flows", (239, 246, 255), (245, 243, 255), (79, 70, 229)),
        ("food-ordering.png", "Food Ordering", "QR menus and ordering platforms", (240, 253, 244), (255, 247, 237), (22, 163, 74)),
        ("real-time-chat.png", "Real-Time Apps", "Socket.io, WebRTC, video chat", (240, 249, 255), (224, 231, 255), (2, 132, 199)),
        ("ai-tools.png", "AI Applications", "OpenAI, Segmind, custom assistants", (250, 245, 255), (236, 254, 255), (124, 58, 237)),
        ("web-platforms.png", "Web Platforms", "React, PHP, Node.js, MySQL", (248, 250, 252), (226, 232, 240), (51, 65, 85)),
        ("mobile-tools.png", "Mobile Tools", "React Native, Firebase, APIs", (255, 251, 235), (240, 253, 250), (20, 184, 166)),
    ]
    for card in cards:
        card_asset(*card)


if __name__ == "__main__":
    main()
