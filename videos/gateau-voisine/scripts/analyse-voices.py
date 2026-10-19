"""Timing mot à mot (faster-whisper) et ouverture de bouche par image (enveloppe audio).

Écrit assets/timing.json : mots par réplique + liste des images où la bouche est ouverte.
"""
import json, pathlib, wave, re
import numpy as np
from faster_whisper import WhisperModel

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.load(open(ROOT / "assets/lines.json"))
with wave.open(str(ROOT / "assets/audio/dialogue.wav")) as w:
    sr = w.getframerate()
    pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

model = WhisperModel("small", compute_type="int8")
FPS = 15  # cadence du battement de bouche (style dessin animé)
for line in data["lines"]:
    a, b = int(line["start"] * sr), int(line["end"] * sr)
    clip = pcm[a:b]
    idx = np.arange(0, len(clip), sr / 16000)  # whisper attend du 16 kHz
    clip16 = np.interp(idx, np.arange(len(clip)), clip).astype(np.float32)
    segs, _ = model.transcribe(clip16, language="fr", word_timestamps=True,
                               initial_prompt=line["text"])
    heard = []
    for s in segs:
        for wd in s.words:  # whisper coupe « l'as » en « l » + « 'as » : on recolle
            if heard and wd.word.strip()[:1] in "'’":
                heard[-1] = type("W", (), dict(word=heard[-1].word + wd.word.strip(),
                                              start=heard[-1].start, end=wd.end))
            else:
                heard.append(wd)
    line["heard"] = " ".join(wd.word.strip() for wd in heard)
    # on garde le texte écrit, et on cale ses mots sur les timings entendus
    words = line["text"].split()
    if len(heard) == len(words):
        times = [(line["start"] + wd.start, line["start"] + wd.end) for wd in heard]
    else:  # repli : répartition proportionnelle au nombre de lettres
        n = [len(re.sub(r"\W", "", x)) + 1 for x in words]
        tot, acc, times = sum(n), 0, []
        span = line["end"] - line["start"]
        for k in n:
            times.append((line["start"] + span * acc / tot, line["start"] + span * (acc + k) / tot))
            acc += k
    line["words"] = [dict(w=x, s=round(s, 3), e=round(e, 3)) for x, (s, e) in zip(words, times)]
    # bouche : RMS par tranche de 1/FPS s
    hop = sr // FPS
    seg = pcm[a:b]
    rms = [float(np.sqrt(np.mean(seg[i:i + hop] ** 2))) for i in range(0, len(seg) - hop, hop)]
    thr = 0.25 * max(rms)
    line["mouth"] = [1 if r > thr else 0 for r in rms]
    line["mouth_fps"] = FPS
    print(line["who"], "|", line["text"], "\n   entendu:", line["heard"], "| aligné:", len(heard) == len(words))
json.dump(data, open(ROOT / "assets/timing.json", "w"), ensure_ascii=False, indent=1)
