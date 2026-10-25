import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P, FONT, SRC = sys.argv[1], sys.argv[2], sys.argv[3]
cover = Image.open(SRC).convert("RGB")
S = 1024
def bg(y0):
    return cover.crop((0, y0, S, y0 + S))
def letter(img, scale, fill=(21, 23, 21)):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, int(S * scale))
    l, t, r, b = d.textbbox((0, 0), "O", font=f)
    x = (S - (r - l)) / 2 - l; y = (S - (b - t)) / 2 - t
    # soft shadow for depth on the texture
    sh = Image.new("L", img.size, 0); ImageDraw.Draw(sh).text((x + 10, y + 14), "O", font=f, fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.paste((120, 45, 10), (0, 0), sh)
    d.text((x, y), "O", font=f, fill=fill)
    return img
for y0 in (0, 1366):
    letter(bg(y0), 0.78).save(f"{P}/try-{y0}.png")
base = bg(0)
# remove the green fleck inside the O: find greenish pixels and patch from texture 60px above
px = base.load(); pts = [(x, y) for y in range(450, 760) for x in range(380, 660) if px[x, y][1] > px[x, y][0] - 40]
print("fleck pixels:", len(pts))
if pts:
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    box = (min(xs) - 12, min(ys) - 12, max(xs) + 12, max(ys) + 12)
    h = box[3] - box[1]
    patch = base.crop((box[0], box[1] - h - 20, box[2], box[1] - 20))
    m = Image.new("L", patch.size, 0); ImageDraw.Draw(m).ellipse((0, 0, *patch.size), fill=255); m = m.filter(ImageFilter.GaussianBlur(4))
    base.paste(patch, box[:2], m)
icon = letter(base, 0.78)
icon.save(f"{P}/optimist-icon-1024.png")
for s in (512, 192, 180, 32):
    icon.resize((s, s), Image.LANCZOS).save(f"{P}/optimist-icon-{s}.png")
# preview: phone-style rounded corners at several sizes
prev = Image.new("RGB", (900, 300), (240, 240, 240)); x = 20
for s in (240, 120, 60, 29):
    t = icon.resize((s, s), Image.LANCZOS); m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .22), fill=255)
    prev.paste(t, (x, 30), m); x += s + 40
prev.save(f"{P}/preview.png")
