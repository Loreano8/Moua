"""Original afrobeat-inspired groove for the Creator Network video (no deps).

108 BPM, Dm - Bb - F - C. Log-drum bass, syncopated kick, rimshot clap on
2 and 4, 16th-note shaker with accents, 3-2 clave and a marimba riff.
Intro (first INTRO seconds) is shaker + marimba only; the full groove drops
after. Writes assets/audio/bgm.wav; encode to bgm.m4a afterwards.
"""
import math, struct, wave, os

SR, BPM = 44100, 108
BEAT = 60 / BPM
DUR = 44 * BEAT          # 24.44 s
INTRO = 8 * BEAT         # groove drops on scene 2
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")

def midi(n): return 440 * 2 ** ((n - 69) / 12)

CHORDS = [[62, 65, 69], [58, 62, 65], [53, 57, 60], [60, 64, 67]]   # Dm Bb F C
# 16th-step patterns over one bar (16 steps)
KICK  = [1,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,0]
CLAP  = [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0]
CLAVE = [1,0,0,1, 0,0,1,0, 0,0,1,0, 1,0,0,0]
SHAKE_ACC = [1,0,0.5,0, 1,0,0.5,0.3, 1,0,0.5,0, 1,0.3,0.5,0]
LOG   = [1,0,0,1, 0,0,1,0, 0,1,0,0, 1,0,0,0]   # log-drum bass hits
MARIMBA = [0,None,2,1, None,0,None,2, 1,None,0,2, None,1,2,None]  # chord-tone index per 16th

seed = 4242
def noise():
    global seed
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed / 0x3FFFFFFF - 1.0

S16 = BEAT / 4
L = [0.0] * N; R = [0.0] * N
hin = hout = 0.0
for i in range(N):
    t = i / SR
    full = t >= INTRO
    step = int(t / S16); ts = t - step * S16; s = step % 16
    bar = step // 16
    chord = CHORDS[bar % 4]
    n = noise(); hp = 0.9 * (hout + n - hin); hin, hout = n, hp
    # shaker: every 16th, accented
    sh = hp * math.exp(-ts * 70) * (0.35 + 0.65 * SHAKE_ACC[s])
    # marimba riff
    mar = 0.0
    if MARIMBA[s] is not None:
        f = midi(chord[MARIMBA[s]] + 12)
        mar = (math.sin(2 * math.pi * f * ts) + 0.25 * math.sin(2 * math.pi * f * 4 * ts)) * math.exp(-ts * 16)
    l = 0.10 * sh + 0.20 * mar
    r = 0.10 * sh + 0.20 * mar
    if full:
        kk = math.sin(2 * math.pi * (50 * ts + 90 * (1 - math.exp(-ts * 35)) / 35)) * math.exp(-ts * 10) if KICK[s] else 0.0
        cl = (0.7 * n * math.exp(-ts * 30) + 0.4 * math.sin(2 * math.pi * 1800 * ts) * math.exp(-ts * 60)) if CLAP[s] else 0.0
        cv = math.sin(2 * math.pi * 2500 * ts) * math.exp(-ts * 90) if CLAVE[s] else 0.0
        # log drum: pitched sine that bends down, on the chord root
        lg = 0.0
        if LOG[s]:
            f0 = midi(chord[0] - 12)
            lg = math.sin(2 * math.pi * (f0 * 1.5 * ts - f0 * 0.5 * (1 - math.exp(-ts * 12)) / 12)) * math.exp(-ts * 5)
        c = 0.50 * kk + 0.34 * lg + 0.16 * cl
        l += c + 0.10 * cv
        r += c + 0.07 * cv
    L[i] = l; R[i] = r

peak = max(max(map(abs, L)), max(map(abs, R)))
g = 10 ** (-1 / 20) / peak
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    fr = bytearray()
    for i in range(N):
        t = i / SR
        fade = min(1.0, t / 0.05, (DUR - t) / 1.2)
        for smp in (L[i], R[i]):
            fr += struct.pack("<h", int(max(-1, min(1, smp * g * fade)) * 32767))
    w.writeframes(bytes(fr))
print("wrote", os.path.normpath(OUT), round(DUR, 3), "s")
