"""Construit index.html : personnages SVG au trait, plans, sous-titres mot à mot, bouche synchro.

Usage : python3 scripts/build.py   (lit assets/timing.json, écrit index.html)
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.load(open(ROOT / "assets/timing.json"))
LINES = T["lines"]
DURATION = 23.6
INK = "#111"
CARROT = "#F28C28"

# ---------------------------------------------------------------- dessin

def eye(cx, cy, rx, ry, kind, look):
    px, py = cx + look * rx * 0.38, cy + ry * 0.12
    if kind == "open":
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff"/>'
                f'<circle cx="{px}" cy="{py}" r="{rx*0.42}" fill="{INK}" stroke="none"/>')
    if kind == "wide":
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*1.18}" ry="{ry*1.18}" fill="#fff"/>'
                f'<circle cx="{cx + look*rx*0.3}" cy="{cy}" r="{rx*0.24}" fill="{INK}" stroke="none"/>')
    if kind == "happy":
        return f'<path d="M{cx-rx},{cy+ry*0.25} Q{cx},{cy-ry*1.1} {cx+rx},{cy+ry*0.25}" fill="none"/>'
    if kind == "closed":
        return f'<path d="M{cx-rx},{cy} Q{cx},{cy+ry*0.7} {cx+rx},{cy}" fill="none"/>'
    if kind in ("half", "angry"):
        # paupière : la moitié haute de l'oeil est couverte
        tilt = 0 if kind == "half" else (ry * 0.35 if cx < 0 else -ry * 0.35)
        lid = (f'M{cx-rx-2},{cy - tilt} L{cx-rx-2},{cy-ry-4} L{cx+rx+2},{cy-ry-4} '
               f'L{cx+rx+2},{cy + tilt} Z')
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff"/>'
                f'<circle cx="{px}" cy="{cy+ry*0.4}" r="{rx*0.42}" fill="{INK}" stroke="none"/>'
                f'<path d="{lid}" fill="#fff" stroke="none"/>'
                f'<path d="M{cx-rx},{cy - tilt} L{cx+rx},{cy + tilt}" fill="none"/>')
    raise ValueError(kind)


def brow(cx, cy, rx, ry, kind):
    by = cy - ry - 16
    inner = 1 if cx < 0 else -1  # côté du nez
    if kind == "neutral":
        return f'<path d="M{cx-rx},{by} Q{cx},{by-12} {cx+rx},{by}" fill="none"/>'
    if kind == "up":
        return f'<path d="M{cx-rx},{by-16} Q{cx},{by-32} {cx+rx},{by-16}" fill="none"/>'
    a, b = (cx - rx, cx + rx)
    if kind == "angry":
        ya, yb = (by - 12, by + 14) if inner == 1 else (by + 14, by - 12)
    elif kind == "worried":
        ya, yb = (by + 6, by - 16) if inner == 1 else (by - 16, by + 6)
    else:
        raise ValueError(kind)
    return f'<path d="M{a},{ya} L{b},{yb}" fill="none"/>'


def mouth(mx, my, w, kind):
    if kind == "smile":
        return f'<path d="M{mx-w},{my} Q{mx},{my+w*0.6} {mx+w},{my}" fill="none"/>'
    if kind == "flat":
        return f'<path d="M{mx-w*0.6},{my+4} L{mx+w*0.6},{my+4}" fill="none"/>'
    if kind == "frown":
        return f'<path d="M{mx-w*0.6},{my+12} Q{mx},{my-10} {mx+w*0.6},{my+12}" fill="none"/>'
    if kind == "big":
        return (f'<path d="M{mx-w*1.25},{my-6} Q{mx},{my+w*1.5} {mx+w*1.25},{my-6} Z" fill="{INK}"/>'
                f'<path d="M{mx-w*0.5},{my+w*0.75} Q{mx},{my+w*0.4} {mx+w*0.5},{my+w*0.75}" '
                f'fill="#fff" stroke="none"/>')
    if kind == "bigopen":
        return (f'<path d="M{mx-w*1.3},{my-10} Q{mx},{my+w*2.0} {mx+w*1.3},{my-10} Z" fill="{INK}"/>'
                f'<ellipse cx="{mx}" cy="{my+w*0.75}" rx="{w*0.5}" ry="{w*0.2}" fill="#fff" stroke="none"/>')
    if kind == "open":
        return f'<ellipse cx="{mx}" cy="{my+10}" rx="{w*0.55}" ry="{w*0.42}" fill="{INK}"/>'
    if kind == "o":
        return f'<ellipse cx="{mx}" cy="{my+8}" rx="{w*0.25}" ry="{w*0.32}" fill="{INK}"/>'
    if kind in ("grimace", "grimaceopen"):
        h = w * (0.55 if kind == "grimace" else 0.85)
        x0, x1 = mx - w * 1.1, mx + w * 1.1
        teeth = "".join(f'<path d="M{mx + k*w*0.36},{my-h/2} L{mx + k*w*0.36},{my+h/2}" fill="none"/>'
                        for k in (-2, -1, 0, 1, 2))
        return (f'<rect x="{x0}" y="{my-h/2}" width="{x1-x0}" height="{h}" rx="{h*0.45}" fill="#fff"/>'
                f'<path d="M{x0+4},{my} L{x1-4},{my}" fill="none"/>' + teeth)
    raise ValueError(kind)


TALK = {"smile": "open", "big": "bigopen", "grimace": "grimaceopen", "flat": "open",
        "frown": "open", "o": "open", "open": "open"}


def face(spec, e, uid, talking):
    cx, cy, rx, ry, mx, my, mw = spec
    look = e.get("look", 0)
    s = ""
    for side in (-1, 1):
        s += eye(side * cx, cy, rx, ry, e["eyes"], look)
        s += brow(side * cx, cy, rx, ry, e.get("brows", "neutral"))
    s += f'<g id="{uid}-mc">{mouth(mx, my, mw, e["mouth"])}</g>'
    if talking:
        s += f'<g id="{uid}-mo" opacity="0">{mouth(mx, my, mw, TALK[e["mouth"]])}</g>'
    return s


def cake(y):
    """Plat + gâteau aux carottes, tenu à hauteur de poitrine (repère local)."""
    return (f'<ellipse cx="0" cy="{y}" rx="165" ry="30" fill="#fff"/>'
            f'<path d="M-115,{y-6} L-110,{y-92} Q0,{y-120} 110,{y-92} L115,{y-6} Q0,{y+18} -115,{y-6} Z" fill="#fff"/>'
            f'<path d="M-110,{y-92} Q-90,{y-62} -70,{y-90} Q-50,{y-60} -30,{y-92} Q-10,{y-62} 10,{y-94} '
            f'Q30,{y-62} 50,{y-92} Q70,{y-60} 90,{y-90} Q100,{y-70} 110,{y-92}" fill="none"/>'
            # carotte décorative posée sur la face avant (seule touche de couleur)
            f'<path d="M-46,{y-44} L40,{y-58} L44,{y-34} Z" fill="{CARROT}" stroke-width="5"/>'
            f'<path d="M42,{y-46} L70,{y-66} M42,{y-46} L74,{y-46} M42,{y-46} L68,{y-28}" '
            f'fill="none" stroke-width="5"/>'
            f'<circle cx="-160" cy="{y-4}" r="24" fill="#fff"/><circle cx="160" cy="{y-4}" r="24" fill="#fff"/>')


ADULT_BODY = ('<path d="M-42,138 C-112,150 -152,192 -158,262 L-170,760 L170,760 L158,262 '
              'C152,192 112,150 42,138 Z" fill="#fff"/>'
              '<path d="M-36,96 L-42,142 M36,96 L42,142" fill="none"/>')
ADULT_ARMS = ('<path d="M-152,270 C-176,390 -176,500 -162,600" fill="none"/>'
              '<path d="M152,270 C176,390 176,500 162,600" fill="none"/>')
HOLD_ARMS = ('<path d="M-152,270 C-176,300 -180,320 -166,338" fill="none"/>'
             '<path d="M152,270 C176,300 180,320 166,338" fill="none"/>')


def bernard(e, uid, talking=False):
    s = ADULT_BODY + (HOLD_ARMS if e.get("cake", True) else ADULT_ARMS)
    s += '<ellipse cx="-104" cy="12" rx="18" ry="28" fill="#fff"/><ellipse cx="104" cy="12" rx="18" ry="28" fill="#fff"/>'
    s += '<ellipse cx="0" cy="0" rx="104" ry="122" fill="#fff"/>'
    # couronne de cheveux + trois mèches sur le dessus
    s += ('<path d="M-98,-28 C-118,-58 -104,-92 -80,-98 M98,-28 C118,-58 104,-92 80,-98" fill="none"/>'
          '<path d="M-14,-121 C-10,-150 8,-158 20,-146 M6,-122 C14,-146 32,-150 40,-136" fill="none"/>')
    s += face((40, -6, 15, 19, 0, 82, 30), e, uid, talking)
    # lunettes rondes, nez, moustache
    s += ('<circle cx="-40" cy="-6" r="34" fill="none"/><circle cx="40" cy="-6" r="34" fill="none"/>'
          '<path d="M-6,-8 Q0,-14 6,-8 M-74,-10 L-102,-18 M74,-10 L102,-18" fill="none"/>'
          '<path d="M0,10 C-14,34 -12,44 8,44" fill="none"/>'
          f'<path d="M-52,62 C-32,42 -10,46 0,54 C10,46 32,42 52,62 C32,70 10,66 0,60 C-10,66 -32,70 -52,62 Z" fill="{INK}"/>')
    if e.get("cake", True):
        s += cake(345)
    return s


def mere(e, uid, talking=False):
    s = (f'<path d="M-128,-30 C-150,-170 150,-170 128,-30 L138,210 C100,226 64,212 52,180 '
         f'L-52,180 C-64,212 -100,226 -138,210 Z" fill="{INK}"/>')  # cheveux (arrière)
    s += ADULT_BODY + ADULT_ARMS
    s += '<ellipse cx="0" cy="0" rx="100" ry="118" fill="#fff"/>'
    s += face((38, 4, 16, 21, 0, 72, 30), e, uid, talking)
    # cils, nez, frange
    s += ('<path d="M-56,-10 L-66,-20 M56,-10 L66,-20" fill="none"/>'
          '<path d="M2,22 C-8,40 -4,46 10,44" fill="none"/>'
          f'<path d="M-102,-34 C-84,-136 70,-150 106,-44 C64,-92 10,-100 -30,-70 C-50,-56 -80,-44 -102,-34 Z" fill="{INK}"/>')
    if e.get("sweat"):
        s += '<path d="M128,-70 C116,-46 116,-32 128,-28 C140,-32 140,-46 128,-70 Z" fill="#fff" stroke-width="5"/>'
    return s


def leo(e, uid, talking=False):
    s = ('<path d="M-46,96 C-112,106 -132,152 -136,212 L-142,560 L142,560 L136,212 '
         'C132,152 112,106 46,96 Z" fill="#fff"/>')
    if e.get("arms_up"):
        s += ('<path d="M-126,200 C-190,140 -214,60 -206,-10" fill="none"/>'
              '<path d="M126,200 C190,140 214,60 206,-10" fill="none"/>'
              '<circle cx="-206" cy="-34" r="26" fill="#fff"/><circle cx="206" cy="-34" r="26" fill="#fff"/>')
    else:
        s += ('<path d="M-128,214 C-148,300 -150,380 -140,450" fill="none"/>'
              '<path d="M128,214 C148,300 150,380 140,450" fill="none"/>')
    s += '<ellipse cx="-114" cy="10" rx="18" ry="26" fill="#fff"/><ellipse cx="114" cy="10" rx="18" ry="26" fill="#fff"/>'
    s += '<ellipse cx="0" cy="0" rx="116" ry="110" fill="#fff"/>'
    s += (f'<path d="M-110,-30 L-100,-84 L-72,-66 L-58,-118 L-26,-88 L0,-134 L22,-90 L52,-120 '
          f'L64,-72 L96,-86 L110,-30 C60,-70 -60,-70 -110,-30 Z" fill="{INK}"/>')
    s += face((42, -4, 24, 30, 0, 62, 28), e, uid, talking)
    s += ('<path d="M0,18 C-8,30 -4,36 6,34" fill="none"/>'
          f'<g fill="{INK}" stroke="none"><circle cx="-70" cy="34" r="4"/><circle cx="-58" cy="44" r="4"/>'
          '<circle cx="-80" cy="46" r="4"/><circle cx="70" cy="34" r="4"/><circle cx="58" cy="44" r="4"/>'
          '<circle cx="80" cy="46" r="4"/></g>')
    return s


DRAW = {"bernard": bernard, "mere": mere, "leo": leo}


def place(who, x, y, scale, e, uid, talking=False):
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{INK}" '
            f'stroke-width="{7/scale*1.4:.2f}" stroke-linecap="round" stroke-linejoin="round">'
            f'{DRAW[who](e, uid, talking)}</g>')

# ---------------------------------------------------------------- plans

L = {i: l for i, l in enumerate(LINES)}
# (id, début, fin, personnages [(qui, x, y, échelle, expression, réplique parlée ou None)], caméra)
SHOTS = [
    ("s1", 0.0, 4.15, [("bernard", 540, 390, 1.5, dict(eyes="happy", brows="up", mouth="big"), 0)], "pop"),
    ("s2", 4.15, 7.65, [("mere", 380, 420, 1.45, dict(eyes="happy", brows="up", mouth="big"), 1),
                         ("leo", 830, 720, 1.05, dict(eyes="open", mouth="smile", look=-1), None)], "pop"),
    ("s3", 7.65, 10.5, [("leo", 540, 470, 1.9, dict(eyes="open", mouth="flat", look=1), 2)], "pop"),
    ("s4", 10.5, 11.0, [("bernard", 540, 430, 1.8, dict(eyes="wide", brows="up", mouth="o"), None)], "snap"),
    ("s5", 11.0, 12.6, [("mere", 380, 420, 1.45, dict(eyes="open", brows="worried", mouth="grimace",
                                                     look=1, sweat=True), 3),
                         ("leo", 830, 720, 1.05, dict(eyes="open", mouth="flat", look=-1), None)], "pop"),
    ("s6", 12.6, 15.9, [("leo", 540, 470, 1.9, dict(eyes="closed", brows="up", mouth="smile"), 4)], "pop"),
    ("s7", 15.9, 17.3, [("bernard", 540, 400, 1.6, dict(eyes="half", mouth="flat"), None)], "push"),
    ("s8", 17.3, 19.15, [("mere", 470, 470, 1.75, dict(eyes="angry", brows="angry", mouth="frown",
                                                      look=1), 5),
                          ("leo", 1000, 1060, 1.2, dict(eyes="open", mouth="flat", look=-1), None)], "pop"),
    ("s9", 19.15, 22.4, [("leo", 540, 500, 1.75, dict(eyes="happy", brows="up", mouth="big",
                                                     arms_up=True), 6)], "pop"),
    ("s10", 22.4, DURATION, [("bernard", 540, 400, 1.6, dict(eyes="half", brows="worried",
                                                            mouth="frown"), None)], "push"),
]

shots_html, tweens = [], []
for sid, a, b, chars, cam in SHOTS:
    svg = ""
    for k, (who, x, y, sc, e, line) in enumerate(chars):
        uid = f"{sid}-{who}"
        svg += place(who, x, y, sc, e, uid, talking=line is not None)
        if line is not None:
            l = L[line]
            step = 1 / l["mouth_fps"]
            prev = 0
            for f, m in enumerate(l["mouth"]):
                if m != prev:
                    t = round(l["start"] + f * step, 3)
                    tweens.append(f'tl.set("#{uid}-mo",{{opacity:{m}}},{t});'
                                  f'tl.set("#{uid}-mc",{{opacity:{1-m}}},{t});')
                    prev = m
            if prev:
                tweens.append(f'tl.set("#{uid}-mo",{{opacity:0}},{l["end"]});'
                              f'tl.set("#{uid}-mc",{{opacity:1}},{l["end"]});')
    extra = ""
    if sid == "s7":  # « ... » silencieux de Bernard
        extra = ('<div class="dots" id="s7-dots"><span id="s7-d0">•</span><span id="s7-d1">•</span>'
                 '<span id="s7-d2">•</span></div>')
        for k in range(3):
            tweens.append(f'tl.fromTo("#s7-d{k}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.15}},{a+0.25+k*0.3});')
    shots_html.append(
        f'<section id="{sid}" class="clip shot" data-start="{a}" data-duration="{round(b-a,3)}" '
        f'data-track-index="1"><div class="cam" id="{sid}-cam">'
        f'<svg viewBox="0 0 1080 1040" width="1080" height="1040" data-layout-allow-overflow>{svg}</svg></div>{extra}</section>')
    if cam == "pop":
        tweens.append(f'tl.fromTo("#{sid}-cam",{{scale:1.06}},{{scale:1,duration:0.35,ease:"power2.out"}},{a});')
    elif cam == "snap":
        tweens.append(f'tl.fromTo("#{sid}-cam",{{scale:1.12,rotation:-1.5}},{{scale:1.15,rotation:-1.5,duration:{b-a}}},{a});')
    else:
        tweens.append(f'tl.fromTo("#{sid}-cam",{{scale:1}},{{scale:1.12,duration:{round(b-a,3)},ease:"none"}},{a});')

# sous-titres mot à mot
caps = []
for i, l in enumerate(LINES):
    ws = []
    for w in l["words"]:  # « ! » et « ? » isolés (typo française) : recollés au mot précédent
        if ws and not any(ch.isalnum() for ch in w["w"]):
            ws[-1] = dict(ws[-1], w=ws[-1]["w"] + "\u00a0" + w["w"])
        else:
            ws.append(w)
    for j, w in enumerate(ws):
        cid = f"w{i}-{j}"
        end = ws[j + 1]["s"] if j + 1 < len(ws) else l["end"] + 0.2
        text = w["w"].upper().replace("...", "…")
        caps.append(f'<div class="word" id="{cid}"><span>{text}</span></div>')
        tweens.append(f'tl.set("#{cid}",{{opacity:1}},{w["s"]});'
                      f'tl.fromTo("#{cid} span",{{scale:0.8}},{{scale:1,duration:0.12,ease:"back.out(3)"}},{w["s"]});'
                      f'tl.set("#{cid}",{{opacity:0}},{round(end,3)});')

HTML = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Le gâteau du voisin</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000;
               font-family: Montserrat, sans-serif; }}
      #banner {{ position: absolute; left: 60px; right: 60px; top: 250px; height: 150px;
                 display: flex; align-items: center; justify-content: center; text-align: center;
                 color: #fff; font-weight: 900; font-size: 54px; line-height: 1.2; }}
      #panel {{ position: absolute; left: 0; top: 440px; width: 1080px; height: 1040px;
                background: #fff; overflow: hidden; }}
      .shot {{ position: absolute; inset: 0; background: #fff; }}
      .cam {{ position: absolute; inset: 0; width: 1080px; height: 1040px; transform-origin: 50% 40%; }}
      .cam svg {{ display: block; }}
      .dots {{ position: absolute; left: 720px; top: 120px; display: flex; gap: 18px;
               font-size: 90px; color: #111; font-weight: 900; }}
      .dots span {{ display: block; opacity: 0; }}
      #captions {{ position: absolute; left: 0; top: 1300px; width: 1080px; height: 140px; }}
      .word {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
               opacity: 0; }}
      .word span {{ display: block; padding: 8px 30px 12px; border-radius: 22px; background: #111;
                    color: #fff; font-weight: 900; font-size: 84px; letter-spacing: 1px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}"
         data-width="1080" data-height="1920">
      <div id="banner">Quand ton fils est un peu trop honnête 😅</div>
      <div id="panel">
        {"".join(shots_html)}
      </div>
      <div id="captions">{"".join(caps)}</div>
      <audio id="dialogue" src="assets/audio/dialogue.wav" data-start="0" data-duration="{T['total']}"
             data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + t for t in tweens).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(HTML)
print("index.html écrit,", len(tweens), "instructions de timeline")
