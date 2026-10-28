"""Write the two strategy set-up scenes (s3 covered call, s5 cash-secured put).

Each scene: label + title, a 3D illustration, then one row per step. A row slides in
when the voiceover starts the step and its value tag pops on the spoken number
(times are local to the scene, taken from assets/vo/transcript.json).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "compositions")

SCENES = [
    {
        "id": "s3-cc", "dur": 7.6, "label": "STRATEGY 1", "title": ["Covered", "Call"], "title_at": 0.45,
        "img": "assets/img/i-shares.jpg", "alt": "A stack of golden share certificates locked with a padlock",
        "img_box": (300, 300, 480), "row_top": 840, "row_h": 150, "row_gap": 170,
        "rows": [
            ("You own the stock", "$100", "#f5f1e6", 3.0, 3.14),
            ("You sell a call at", "$110", "#f0b90b", 4.3, 5.17),
            ("You collect a premium", "+$3", "#3ddc84", 6.1, 6.78),
        ],
        "note": "Your shares stay set aside as collateral until the option closes, expires or is assigned.",
        "note_at": 6.95,
    },
    {
        "id": "s5-csp", "dur": 11.3, "label": "STRATEGY 2", "title": ["Cash-Secured", "Put"], "title_at": 0.4,
        "img": "assets/img/i-vault.jpg", "alt": "A black and gold vault holding stacks of stablecoins",
        "img_box": (380, 420, 320), "row_top": 770, "row_h": 136, "row_gap": 152,
        "rows": [
            ("The stock trades at", "$100", "#f5f1e6", 2.8, 3.37),
            ("You'd rather buy at", "$90", "#f0b90b", 4.55, 5.26),
            ("You set aside USDC", "LOCKED", "#7fb2ff", 6.2, 7.4),
            ("You sell a put at", "$90", "#f0b90b", 7.85, 8.85),
            ("You collect a premium", "+$3", "#3ddc84", 10.0, 10.73),
        ],
        "note": "Enough USDC to cover the full purchase stays frozen in your Funding Wallet.",
        "note_at": 10.9,
    },
]

TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
        #root {{ position: absolute; inset: 0; background: #0c0b09; overflow: hidden; }}
        .w {{ display: inline-block; opacity: 0; will-change: transform; }}
        .y {{ color: #f0b90b; }}
        .label {{ font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 32px; letter-spacing: 0.18em; color: #f0b90b; }}
        .grid {{ position: absolute; inset: -120px; background-image: linear-gradient(rgba(240, 185, 11, 0.07) 2px, transparent 2px), linear-gradient(90deg, rgba(240, 185, 11, 0.07) 2px, transparent 2px); background-size: 120px 120px; }}
        #{p}-label {{ position: absolute; left: 80px; top: 140px; opacity: 0; }}
        #{p}-ttl {{ position: absolute; left: 80px; right: 80px; top: 190px; font-family: "Archivo Black", sans-serif; font-size: 104px; line-height: 1.0; letter-spacing: -0.045em; color: #f5f1e6; }}
        #{p}-glow {{ position: absolute; left: {gx}px; top: {gy}px; width: {gs}px; height: {gs}px; border-radius: 50%; background: radial-gradient(circle, rgba(240,185,11,0.3) 0%, rgba(240,185,11,0) 65%); opacity: 0; }}
        #{p}-art {{ position: absolute; left: {ix}px; top: {iy}px; width: {isz}px; height: {isz}px; opacity: 0; will-change: transform; }}
        #{p}-img {{ display: block; width: 100%; height: 100%; -webkit-mask-image: radial-gradient(circle at 50% 50%, #000 50%, transparent 70%); mask-image: radial-gradient(circle at 50% 50%, #000 50%, transparent 70%); }}
        .row {{ position: absolute; left: 70px; right: 70px; height: {rh}px; padding: 0 36px; border-radius: 26px; background: #1c1a15; border: 3px solid #2e2b24; display: flex; align-items: center; gap: 30px; opacity: 0; will-change: transform; }}
        .num {{ flex: none; width: 68px; height: 68px; border-radius: 50%; background: #f0b90b; color: #0c0b09; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 34px; display: flex; align-items: center; justify-content: center; }}
        .rt {{ flex: 1; font-family: "Archivo Black", sans-serif; font-size: 46px; letter-spacing: -0.02em; color: #f5f1e6; white-space: nowrap; }}
        .rv {{ font-family: "Archivo Black", sans-serif; font-size: 64px; letter-spacing: -0.03em; white-space: nowrap; opacity: 0; will-change: transform; }}
        #{p}-note {{ position: absolute; left: 80px; right: 80px; top: {nt}px; font-family: "JetBrains Mono", monospace; font-size: 30px; line-height: 1.45; color: #cfc8b8; opacity: 0; }}
      </style>
      <div id="root" data-composition-id="{id}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
        <div id="{p}-grid" class="grid" data-layout-allow-overflow></div>
        <div id="{p}-label" class="label">{label}</div>
        <div id="{p}-ttl"><span class="w">{t1}</span> <span class="w y">{t2}</span></div>
        <div id="{p}-glow"></div>
        <div id="{p}-art"><img id="{p}-img" src="{img}" alt="{alt}" /></div>
{rows}
        <div id="{p}-note">{note}</div>
      </div>
      <script>
        (() => {{
          const tl = gsap.timeline({{ paused: true }});
          function waterfall(sel, t0, maxSpan) {{
            const words = gsap.utils.toArray(sel + " .w");
            const step = Math.min(0.13, maxSpan / words.length);
            words.forEach((el, i) => {{
              const heavy = i === 0 || i === words.length - 1;
              const t = t0 + i * step;
              tl.set(el, {{ opacity: 1, y: heavy ? 80 : 45 }}, t);
              tl.to(el, {{ y: 0, duration: heavy ? 0.18 : 0.15, ease: "power4.out" }}, t);
            }});
          }}
          tl.fromTo("#{p}-grid", {{ y: 0 }}, {{ y: -140, duration: {dur}, ease: "none" }}, 0);
          tl.fromTo("#{p}-label", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.15);
          waterfall("#{p}-ttl", {title_at}, 0.2);
          tl.fromTo("#{p}-glow", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1.1, duration: 1, ease: "power2.out" }}, 0.3);
          tl.fromTo("#{p}-art", {{ opacity: 0, scale: 0.6, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.5)" }}, 0.35);
          tl.to("#{p}-art", {{ y: -18, duration: {float_d}, ease: "sine.inOut" }}, 1.05);
{row_tweens}
          tl.fromTo("#{p}-note", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, {note_at});
          tl.to("#{p}-ttl, #{p}-label, #{p}-art, #{p}-glow, .row, #{p}-note", {{ opacity: 0, y: -40, duration: 0.18, ease: "power3.in" }}, {exit_at});
          window.__timelines["{id}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""

for s in SCENES:
    p = s["id"].split("-")[0]
    ix, iy, isz = s["img_box"]
    rows, tweens = [], []
    for i, (text, val, color, t_row, t_val) in enumerate(s["rows"]):
        top = s["row_top"] + i * s["row_gap"]
        size = "" if len(val) <= 4 else ";font-size:46px"
        rows.append(f'        <div class="row" id="{p}-r{i}" style="top:{top}px"><div class="num">{i + 1}</div><div class="rt">{text}</div><div class="rv" id="{p}-v{i}" style="color:{color}{size}">{val}</div></div>')
        tweens.append(f'          tl.fromTo("#{p}-r{i}", {{ opacity: 0, x: -140 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, {t_row});')
        tweens.append(f'          tl.fromTo("#{p}-v{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }}, {t_val});')
    last_top = s["row_top"] + (len(s["rows"]) - 1) * s["row_gap"] + s["row_h"]
    html = TEMPLATE.format(
        p=p, id=s["id"], dur=s["dur"], label=s["label"], t1=s["title"][0], t2=s["title"][1], title_at=s["title_at"],
        img=s["img"], alt=s["alt"], ix=ix, iy=iy, isz=isz, gx=ix - 60, gy=iy - 60, gs=isz + 120,
        rh=s["row_h"], rows="\n".join(rows), row_tweens="\n".join(tweens), note=s["note"], note_at=s["note_at"],
        nt=last_top + 40, float_d=round(s["dur"] - 1.3, 2), exit_at=round(s["dur"] - 0.2, 2))
    open(os.path.join(OUT, f"{s['id']}.html"), "w").write(html)
    print("wrote", s["id"])
