"""Build compositions/captions.html: one word on screen at a time, timed from assets/transcript.json.

Whisper mishears a few words of the synthetic voice; FIXES maps transcript index -> the scripted word(s).
A list splits one timed entry into several words (time spread by character count); None drops the entry.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXES = {
    36: "a",
    37: ["les", "fonds"],
    40: "l'auto-garde",
    63: "restaures",
    83: "malware",
    84: None,  # merged into 83
    112: "matériel",
    118: "brûlent",
    119: "se",
    120: "mouillent",
    122: "volent",
    159: "passphrase",
    164: None,  # spurious "au"
    169: "passphrase",
    186: "vole",
}

data = json.loads((ROOT / "assets/transcript.json").read_text())
words = data if isinstance(data, list) else data["words"]

entries = []
for i, w in enumerate(words):
    start, end = w["start"], w["end"]
    if i == 83:
        end = words[84]["end"]
    fix = FIXES.get(i, w["text"])
    if fix is None:
        continue
    parts = fix if isinstance(fix, list) else [fix]
    total = sum(len(p) for p in parts)
    t = start
    for p in parts:
        d = (end - start) * len(p) / total
        entries.append([p, t, t + d])
        t += d

for e in entries:
    e[0] = e[0].strip(",.?!:;").upper()

# The exploded-view recap (54.0-58.3 s) labels each part in 3D; captions there would repeat it.
entries = [e for e in entries if not (53.9 <= e[1] < 58.3)]

# One word visible at a time: hold each word until the next starts, at most 0.6 s past its end.
items = []
for k, (text, start, end) in enumerate(entries):
    start = max(start, 0.15)
    nxt = entries[k + 1][1] if k + 1 < len(entries) else end + 0.6
    stop = min(nxt, end + 0.6)
    items.append((k, text, round(start, 3), round(stop - start, 3)))

def size(text):
    # Below y=840 TikTok's action rail narrows the safe band to x 120-780; Archivo Black caps run ~0.82 em wide.
    px = min(104, int(630 / (0.82 * len(text))))
    return "" if px >= 104 else f' style="font-size: {px}px"'


total = json.loads((ROOT / "assets/beats.json").read_text())["duration"]
rows = "\n".join(
    f'    <div id="cw-{k:03d}" class="clip cw" data-start="{s}" data-duration="{d}"><span class="cw-in"{size(t)}>{t}</span></div>'
    for k, t, s, d in items
)
tweens = "\n".join(
    f'    tl.fromTo("#cw-{k:03d} .cw-in", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.12, ease: "back.out(2)" }}, {s});'
    for k, t, s, d in items
)

html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    #root .cw {{
      position: absolute; left: 120px; width: 660px; top: 1090px; height: 140px;
      display: flex; align-items: flex-end; justify-content: center;
    }}
    #root .cw-in {{
      display: inline-block;
      font-family: "Archivo Black", sans-serif; font-size: 104px; line-height: 1; color: #ffffff;
      -webkit-text-stroke: 10px #1e1a16; paint-order: stroke fill; letter-spacing: 0.01em;
      transform-origin: 50% 80%;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{total}">
{rows}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{tweens}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
(ROOT / "compositions").mkdir(exist_ok=True)
(ROOT / "compositions/captions.html").write_text(html)
print(len(items), "words; last ends", round(items[-1][2] + items[-1][3], 2))
