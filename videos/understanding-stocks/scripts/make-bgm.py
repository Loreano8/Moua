"""Original lo-fi jazz / boom-bap bed for the Understanding Stocks video (no deps).

88 BPM, Dm9 - G13 - Cmaj9 - Am7 (ii-V-I-vi). Rhodes-style electric piano
with tremolo, soft walking bass, boom-bap kick and snare, swung 8th hats,
vinyl crackle and tape hiss. Writes assets/audio/bgm.wav; encode to
bgm.m4a afterwards.
"""
import math, struct, wave, os

SR, BPM = 44100, 88
BEAT = 60 / BPM
DUR = 46 * BEAT
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")

def midi(n): return 440 * 2 ** ((n - 69) / 12)

# voicings (Rhodes) and bass roots, one chord per bar
CHORDS = [[53, 57, 60, 64, 69], [53, 59, 64, 67, 71], [52, 55, 59, 62, 64], [55, 57, 60, 64, 67]]
ROOTS = [38, 43, 36, 45]
# chord hits within a bar, in beats (lazy, behind the beat)
HITS = [0.05, 1.55, 2.55, 3.3]
# walking bass: beat offsets and semitone steps from the root
BASS = [(0, 0), (1, 7), (2, 12), (3, 10)]
SWING = 0.62  # position of the off-beat 8th within a beat

seed = 88
def noise():
    global seed
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed / 0x3FFFFFFF - 1.0

def rhodes(f, t):
    if t < 0: return 0.0
    env = math.exp(-t * 1.6) * min(1, t * 200)
    tine = math.sin(2 * math.pi * f * 7.1 * t) * math.exp(-t * 18) * 0.25
    return (math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * f * 2 * t) + tine) * env

L = [0.0] * N; R = [0.0] * N
lp = 0.0; hin = hout = 0.0
for i in range(N):
    t = i / SR
    b = int(t / BEAT); tb = t - b * BEAT
    bar = b // 4; bb = t / BEAT - bar * 4           # beat position within bar
    ci = bar % 4
    chord = CHORDS[ci]
    # Rhodes: sum of recent chord hits (previous bar's last hit rings over)
    keys = 0.0
    for h in HITS:
        dt = (bb - h) * BEAT
        if dt < 0: dt = (bb + 4 - h) * BEAT if bar > 0 else -1
        if 0 <= dt < 2.5:
            for j, n in enumerate(chord):
                keys += rhodes(midi(n), dt + j * 0.004) * (0.9 if j else 1.0)
    trem = 1 + 0.18 * math.sin(2 * math.pi * 4.5 * t)
    # bass
    bs = 0.0
    for off, st in BASS:
        dt = (bb - off) * BEAT
        if 0 <= dt < BEAT:
            f = midi(ROOTS[ci] + st)
            bs += math.sin(2 * math.pi * f * dt) * math.exp(-dt * 3) * min(1, dt * 60)
    # drums (boom-bap): kick on 1 and the "and" of 2, snare on 2 and 4
    n = noise()
    k = 0.0
    for kp in (0.0, 1.62, 2.0):
        dt = (bb - kp) * BEAT
        if 0 <= dt < 0.5:
            k += math.sin(2 * math.pi * (48 * dt + 70 * (1 - math.exp(-dt * 30)) / 30)) * math.exp(-dt * 9)
    sn = 0.0
    for sp in (1.0, 3.0):
        dt = (bb - sp) * BEAT
        if 0 <= dt < 0.4:
            sn += (0.8 * n + 0.5 * math.sin(2 * math.pi * 190 * dt)) * math.exp(-dt * 16)
    lp += 0.25 * (sn - lp)                           # darken the snare
    hp = 0.9 * (hout + n - hin); hin, hout = n, hp
    hh = 0.0
    for hpos in (0.0, SWING):
        dt = (tb / BEAT - hpos) * BEAT
        if 0 <= dt < 0.12:
            hh += hp * math.exp(-dt * 60) * (1.0 if hpos == 0 else 0.6)
    # vinyl: sparse deterministic crackle + hiss
    crackle = (noise() * 0.9) if (seed % 5000) < 3 else 0.0
    hiss = n * 0.012
    l = 0.20 * keys * trem + 0.30 * bs + 0.50 * k + 0.30 * lp + 0.08 * hh + 0.05 * crackle + hiss
    r = 0.20 * keys * (2 - trem) + 0.30 * bs + 0.50 * k + 0.30 * lp + 0.06 * hh + 0.05 * crackle + hiss
    L[i] = l; R[i] = r

peak = max(max(map(abs, L)), max(map(abs, R)))
g = 10 ** (-1.5 / 20) / peak
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    fr = bytearray()
    for i in range(N):
        t = i / SR
        fade = min(1.0, t / 0.4, (DUR - t) / 1.5)
        for smp in (L[i], R[i]):
            fr += struct.pack("<h", int(max(-1, min(1, smp * g * fade)) * 32767))
    w.writeframes(bytes(fr))
print("wrote", os.path.normpath(OUT), round(DUR, 3), "s")
