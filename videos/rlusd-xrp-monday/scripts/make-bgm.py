"""Original sunny "Monday morning" groove for the RLUSD / XRP video (no deps).

120 BPM, C - G/B - Am7 - Fmaj7. Marimba-style plucks on a bouncy
off-beat pattern, warm pad, round bass, soft four-on-the-floor kick,
claps on 2 and 4, shaker 16ths and a bird-like chirp on the first bar.
Writes assets/audio/bgm.wav; encode to bgm.m4a afterwards.
"""
import math, struct, wave, os

SR, BPM = 44100, 120
BEAT = 60 / BPM
DUR = 41 * BEAT
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")

def midi(n): return 440 * 2 ** ((n - 69) / 12)

CHORDS = [[60, 64, 67, 72], [59, 62, 67, 71], [57, 60, 64, 67], [57, 60, 65, 69]]
ROOTS = [36, 35, 33, 29]
# marimba arpeggio: (beat in bar, chord tone index)
ARP = [(0, 0), (0.5, 2), (1, 1), (1.5, 3), (2, 2), (2.5, 1), (3, 3), (3.5, 2), (3.75, 0)]
BASS = [(0, 0), (1.5, 0), (2, 12), (3, 7)]

seed = 120
def noise():
    global seed
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed / 0x3FFFFFFF - 1.0

def marimba(f, t):
    if t < 0: return 0.0
    return (math.sin(2 * math.pi * f * t) * math.exp(-t * 7)
            + 0.3 * math.sin(2 * math.pi * f * 4 * t) * math.exp(-t * 30)) * min(1, t * 400)

L = [0.0] * N; R = [0.0] * N
hin = hout = 0.0; pad_lp = 0.0
for i in range(N):
    t = i / SR
    bar = int(t / (4 * BEAT)); bb = t / BEAT - bar * 4
    ci = bar % 4
    chord = CHORDS[ci]
    # marimba, panned by note
    ml = mr = 0.0
    for pos, idx in ARP:
        dt = (bb - pos) * BEAT
        if 0 <= dt < 0.6:
            v = marimba(midi(chord[idx] + 12), dt)
            pan = 0.3 + 0.4 * (idx / 3)
            ml += v * (1 - pan); mr += v * pan
    # pad: soft detuned saws approximated by a few partials, slow swell per bar
    sw = min(1, (bb * BEAT) / 0.6)
    pad = 0.0
    for n in chord:
        f = midi(n)
        for h in (1, 2, 3):
            pad += math.sin(2 * math.pi * f * h * t * (1.0 + 0.002 * h)) / (h * h)
    pad_lp += 0.08 * (pad * sw - pad_lp)
    # bass
    bs = 0.0
    for off, st in BASS:
        dt = (bb - off) * BEAT
        if 0 <= dt < 0.45:
            f = midi(ROOTS[ci] + st)
            bs += (math.sin(2 * math.pi * f * dt) + 0.2 * math.sin(4 * math.pi * f * dt)) * math.exp(-dt * 5) * min(1, dt * 80)
    n = noise()
    # kick on every beat (soft)
    dt = (bb % 1) * BEAT
    k = math.sin(2 * math.pi * (50 * dt + 90 * (1 - math.exp(-dt * 35)) / 35)) * math.exp(-dt * 11) if dt < 0.35 else 0.0
    # clap on 2 and 4
    cl = 0.0
    for cp in (1.0, 3.0):
        d = (bb - cp) * BEAT
        if 0 <= d < 0.2:
            cl += n * (math.exp(-d * 25) + 0.5 * math.exp(-max(0, d - 0.012) * 40))
    # shaker 16ths
    hp = 0.85 * (hout + n - hin); hin, hout = n, hp
    d16 = (bb * 4 % 1) * BEAT / 4
    sh = hp * math.exp(-d16 * 70) * (1.0 if int(bb * 4) % 2 else 0.5)
    # morning bird chirps in the first bar
    ch = 0.0
    for cpos in (0.5, 0.75, 2.5):
        d = t - cpos * BEAT
        if bar == 0 and 0 <= d < 0.12:
            ch += math.sin(2 * math.pi * (2600 + 9000 * d) * d) * math.sin(math.pi * d / 0.12)
    intro = 0.0 if bar == 0 else 1.0  # drums enter on bar 2
    l = 0.30 * ml + 0.05 * pad_lp + 0.32 * bs + intro * (0.45 * k + 0.16 * cl + 0.06 * sh) + 0.08 * ch
    r = 0.30 * mr + 0.05 * pad_lp + 0.32 * bs + intro * (0.45 * k + 0.16 * cl + 0.05 * sh) + 0.06 * ch
    L[i] = l; R[i] = r

peak = max(max(map(abs, L)), max(map(abs, R)))
g = 10 ** (-1.5 / 20) / peak
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    fr = bytearray()
    for i in range(N):
        t = i / SR
        fade = min(1.0, t / 0.05, (DUR - t) / 1.5)
        for smp in (L[i], R[i]):
            fr += struct.pack("<h", int(max(-1, min(1, smp * g * fade)) * 32767))
    w.writeframes(bytes(fr))
print("wrote", os.path.normpath(OUT), round(DUR, 3), "s")
