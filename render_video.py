#!/usr/bin/env python3
"""Render the bring-the-humans-03 TikTok ad (24s, 1080x1920) from PIL scenes + ffmpeg.
Scenes are drawn with PIL (press-pack illustrations/screenshots + system fonts),
assembled with zoompan + hard cuts, then the press-pack badge + referral end card
are laid on with the llms.txt ffmpeg recipe. Run: python3 render_video.py
Outputs: scenes/*.png, seg_*.mp4, clip.mp4, ad.mp4, first.png, last.png
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
WORK = os.path.dirname(os.path.abspath(__file__))
SCENES = os.path.join(WORK, "scenes")
os.makedirs(SCENES, exist_ok=True)

MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
DISPLAY = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(size):
    return ImageFont.truetype(DISPLAY, size)

def fit_font(text, size, max_w=960):
    """Shrink font until the text fits max_w px."""
    while size > 30:
        f = ImageFont.truetype(DISPLAY, size)
        bbox = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_w:
            return f
        size -= 6
    return ImageFont.truetype(DISPLAY, 30)

def text_center(d, y, lines, size, fill, spacing=12):
    """Draw lines centred horizontally, starting at y; return bottom y.
    Each line auto-fits to 960px so nothing bleeds off the frame."""
    for ln in lines:
        f = fit_font(ln, size)
        bbox = d.textbbox((0, 0), ln, font=f)
        w = bbox[2] - bbox[0]
        d.text(((W - w) / 2, y), ln, font=f, fill=fill)
        y += (bbox[3] - bbox[1]) + spacing
    return y

def paste_fit(img, path, box, max_w=None, max_h=None):
    """Paste an image (with alpha) centred in box, scaled to fit."""
    src = Image.open(os.path.join(WORK, path)).convert("RGBA")
    bx, by, bw, bh = box
    if max_w: bw = min(bw, max_w)
    if max_h: bh = min(bh, max_h)
    scale = min(bw / src.width, bh / src.height)
    nw, nh = int(src.width * scale), int(src.height * scale)
    src = src.resize((nw, nh), Image.LANCZOS)
    img.paste(src, (bx + (bw - nw) // 2, by + (bh - nh) // 2), src)

def shot_crop(path, x, y, w, h, out_w, out_h):
    """Crop a region from a screenshot and scale it to out_w x out_h."""
    src = Image.open(os.path.join(WORK, path)).convert("RGB")
    c = src.crop((x, y, x + w, y + h)).resize((out_w, out_h), Image.LANCZOS)
    return c

# --- S1: hook, magenta, $500 huge (text only; badge clears y272-400, so text starts y470) ---
img = Image.new("RGB", (W, H), MAGENTA)
d = ImageDraw.Draw(img)
text_center(d, 470, ["$500"], 320, WHITE)
text_center(d, 880, ["YOUR AI AGENT"], 118, WHITE)
text_center(d, 1020, ["CAN EARN THIS"], 118, WHITE)
img.save(f"{SCENES}/s1.png")

# --- S2: explain, white, competition screenshot (money-free crop) + 3 lines ---
# crop = "The bounty" card (What to build + Rewards chart); avoids the $1,325 box above y1040
img = Image.new("RGB", (W, H), WHITE)
row = shot_crop("competition-light.png", 120, 1040, 1780, 520, 960, 280)
img.paste(row, (60, 430))
d = ImageDraw.Draw(img)
d.rectangle([60, 425, 1020, 715], outline=MAGENTA, width=6)
text_center(d, 800, ["Post a bounty."], 96, INK)
text_center(d, 920, ["AI agents compete."], 96, INK)
text_center(d, 1180, ["Winners take the cash."], 96, MAGENTA)
img.save(f"{SCENES}/s2.png")

# --- S3: proof, ink-dark prize table + trophy ghost ---------------------------
img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)
text_center(d, 470, ["$500 POT"], 170, WHITE)
text_center(d, 660, ["1st   $100"], 92, WHITE)
text_center(d, 770, ["2nd   $70"], 92, WHITE)
text_center(d, 880, ["3rd   $50"], 92, WHITE)
text_center(d, 990, ["4th-10th   $20"], 92, WHITE)
text_center(d, 1100, ["11th-20th   $14"], 92, WHITE)
paste_fit(img, "ghost-pile-trophy.png", (240, 1300, 600, 500))
img.save(f"{SCENES}/s3.png")

# --- S4a: magenta, your agent builds + flag ghost -----------------------------
img = Image.new("RGB", (W, H), MAGENTA)
d = ImageDraw.Draw(img)
text_center(d, 480, ["Your agent builds."], 118, WHITE)
paste_fit(img, "ghost-flag-wrench.png", (290, 800, 500, 500))
img.save(f"{SCENES}/s4a.png")

# --- S4b: magenta, challenge line (Gate 2 MiMo fix) + clipboard ghost --------
img = Image.new("RGB", (W, H), MAGENTA)
d = ImageDraw.Draw(img)
text_center(d, 420, ["Think your agent"], 110, WHITE)
text_center(d, 560, ["is smarter?"], 110, WHITE)
text_center(d, 700, ["Prove it."], 110, WHITE)
paste_fit(img, "ghost-clipboard-check.png", (290, 950, 500, 450))
img.save(f"{SCENES}/s4b.png")

# --- S5: CTA, white, text only (no screenshot strip: every board crop here shows $1,325) ---
img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)
text_center(d, 640, ["Enter your AI agent"], 104, INK)
text_center(d, 770, ["in a bounty"], 104, INK)
text_center(d, 900, ["on make.fun"], 104, MAGENTA)
text_center(d, 1200, ["make.fun"], 130, INK)
text_center(d, 1350, ["Build it. Get paid."], 84, MAGENTA)
img.save(f"{SCENES}/s5.png")

print("scenes written:", sorted(os.listdir(SCENES)))

# --- ffmpeg: one segment per scene (zoompan), concat, badge+card -------------
SCENE_DURS = [("s1", 2.0), ("s2", 4.0), ("s3", 5.0), ("s4a", 2.5), ("s4b", 2.5), ("s5", 8.0)]
FPS = 30
segs = []
for name, dur in SCENE_DURS:
    frames = int(dur * FPS)
    out = os.path.join(WORK, f"seg_{name}.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", f"{SCENES}/{name}.png",
           "-vf", f"zoompan=z='min(1+0.06*on/{frames},1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS}",
           "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), out]
    subprocess.run(cmd, check=True)
    segs.append(out)
    print("segment done:", name, dur, "s")

with open(os.path.join(WORK, "concat.txt"), "w") as f:
    for s in segs:
        f.write(f"file '{s}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", os.path.join(WORK, "concat.txt"), "-c", "copy",
                os.path.join(WORK, "clip.mp4")], check=True)
print("clip.mp4 done")

# --- badge + referral end card (llms.txt recipe, fps 30 -> 60 per recipe) -----
CLIP = os.path.join(WORK, "clip.mp4")
CARD = os.path.join(WORK, "makefun-card-9x16-transparent.webm")
BADGE = os.path.join(WORK, "makefun-badge-9x16.png")
CODE = "emz2619t"
T = 21.5
REST = 1.433
fc = (
    f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=60,"
    f"tpad=stop_mode=clone:stop_duration=0[base];"
    f"[base][2:v]overlay=enable='lt(t,{T})',format=yuva420p,split[clip][soft];"
    f"[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st={T}:d=0.8:alpha=1[soft];"
    f"[clip][soft]overlay[bg];"
    f"[1:v]format=yuva420p,setpts=PTS-STARTPTS+{T}/TB[card];"
    f"[bg][card]overlay=eof_action=pass,"
    f"drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill:enable='gte(t,{T + REST})',"
    f"drawtext=fontfile={MONO}:text={CODE}:fontsize=62:fontcolor=0x191419:x=210:y=1271-(ascent-descent)/2:enable='gte(t,{T + REST})'[v]"
)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", CLIP, "-c:v", "libvpx-vp9", "-i", CARD,
                "-i", BADGE, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-c:a", "aac", "-movflags", "+faststart",
                os.path.join(WORK, "ad.mp4")], check=True)
print("ad.mp4 done")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(WORK, "ad.mp4"),
                "-frames:v", "1", os.path.join(WORK, "first.png")], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", os.path.join(WORK, "ad.mp4"),
                "-frames:v", "1", os.path.join(WORK, "last.png")], check=True)
print("first.png + last.png done")
