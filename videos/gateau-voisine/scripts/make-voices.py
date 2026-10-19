"""Génère les répliques avec Piper puis les assemble en une piste de dialogue.

Usage : python make-voices.py <dossier_voix_piper>
Écrit assets/audio/dialogue.wav et assets/lines.json (débuts/fins de chaque réplique).
"""
import json, subprocess, sys, wave, pathlib

VOICES = pathlib.Path(sys.argv[1])
ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP = ROOT / ".hyperframes" / "voices"
TMP.mkdir(parents=True, exist_ok=True)

CAST = {
    "bernard": dict(model="fr_FR-tom-medium", speaker=None, semitones=-1.0, length=1.0),
    "mere": dict(model="fr_FR-siwis-medium", speaker=None, semitones=-1.0, length=1.0),
    "leo": dict(model="fr_FR-siwis-medium", speaker=None, semitones=5.5, length=0.88),
}

# (personnage, réplique, silence après en secondes)
LINES = [
    ("bernard", "Bonjour ! Je vous ai refait mon gâteau aux carottes !", 0.35),
    ("mere", "Oh, il ne fallait pas ! On l'adore, votre gâteau !", 0.3),
    ("leo", "Bah non. La dernière fois, tu l'as donné au chien.", 0.6),
    ("mere", "Euh... Il plaisante, hein !", 0.3),
    ("leo", "Non, c'est vrai. Même le chien, il l'a pas fini.", 1.6),
    ("mere", "Léo. Dans ta chambre.", 0.5),
    ("leo", "D'accord ! Je peux prendre le gâteau ? Pour le chien ?", 1.0),
]

RATE = 44100
parts, meta, t = [], [], 0.6  # petit blanc au début
for i, (who, text, gap) in enumerate(LINES):
    c = CAST[who]
    raw = TMP / f"{i}-raw.wav"
    out = TMP / f"{i}.wav"
    cmd = [sys.executable, "-m", "piper", "-m", str(VOICES / f"{c['model']}.onnx"),
           "--length-scale", str(c["length"]), "-f", str(raw)]
    if c["speaker"] is not None:
        cmd += ["-s", str(c["speaker"])]
    subprocess.run(cmd, input=text.encode(), check=True, capture_output=True)
    ratio = 2 ** (c["semitones"] / 12)
    with wave.open(str(raw)) as w:
        sr = w.getframerate()
    # changement de hauteur en gardant le tempo, puis coupe des blancs
    af = (f"asetrate={sr*ratio:.0f},aresample={RATE},atempo={1/ratio:.5f},"
          "silenceremove=start_periods=1:start_threshold=-45dB,"
          "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
          "loudnorm=I=-16:TP=-1.5")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af,
                    "-ar", str(RATE), "-ac", "1", str(out)], check=True)
    with wave.open(str(out)) as w:
        dur = w.getnframes() / w.getframerate()
    meta.append(dict(who=who, text=text, start=round(t, 3), end=round(t + dur, 3)))
    parts.append((out, t))
    t += dur + gap

total = t
inputs, filt = [], []
for k, (p, start) in enumerate(parts):
    inputs += ["-i", str(p)]
    filt.append(f"[{k}]adelay={int(start*1000)}:all=1[a{k}]")
filt.append("".join(f"[a{k}]" for k in range(len(parts))) +
            f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total:.3f}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt),
                "-map", "[out]", "-ar", str(RATE), str(ROOT / "assets/audio/dialogue.wav")], check=True)
json.dump(dict(total=round(total, 3), lines=meta), open(ROOT / "assets/lines.json", "w"),
          ensure_ascii=False, indent=2)
print(json.dumps(meta, ensure_ascii=False, indent=1), total)
