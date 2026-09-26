"""Generate the original music bed for "The Group Chat" (deterministic, no deps).

96 BPM, C - G - Am - F. Sparse (pad, soft hats, half-time kick) under the
chat, then a full drop (kick every beat, bass, pluck arp) at DROP seconds for
the finale. Writes assets/audio/bgm.wav; encode to bgm.m4a afterwards.
"""
import math, struct, wave, os

SR, DUR, BPM, DROP = 44100, 34.5, 96, 25.0
BEAT = 60 / BPM
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")

def midi(n): return 440 * 2 ** ((n - 69) / 12)

CHORDS = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
ARP = [0, 1, 2, 1, 2, 1, 0, 2]

seed = 777
def noise():
    global seed
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed / 0x3FFFFFFF - 1.0

L = [0.0] * N; R = [0.0] * N
hin = hout = 0.0
for i in range(N):
    t = i / SR
    full = t >= DROP
    bp = t / BEAT; b = int(bp); tb = t - b * BEAT
    chord = CHORDS[(b // 4) % 4]
    # kick: half-time before the drop, every beat after
    k = 0.0
    if full or b % 2 == 0:
        k = math.sin(2 * math.pi * (45 * tb + 75 * (1 - math.exp(-tb * 30)) / 30)) * math.exp(-tb * 9)
    n = noise(); hp = 0.95 * (hout + n - hin); hin, hout = n, hp
    th = t - (b + 0.5) * BEAT
    hat = hp * math.exp(-th * 50) if th >= 0 else 0.0
    tbar = t - (b // 4) * 4 * BEAT
    swell = min(1.0, tbar / 0.8)
    pl_ = pr_ = 0.0
    for j, note in enumerate(chord):
        f = midi(note)
        pl_ += math.sin(2 * math.pi * f * 0.997 * t + j) + 0.25 * math.sin(4 * math.pi * f * t)
        pr_ += math.sin(2 * math.pi * f * 1.003 * t + 2 * j) + 0.25 * math.sin(4 * math.pi * f * t)
    step = int(bp * 2); ts = t - step * BEAT / 2
    f = midi(chord[ARP[step % 8]] + 12)
    arp = (math.sin(2 * math.pi * f * t) + 0.4 * math.sin(4 * math.pi * f * t)) * math.exp(-ts * 12)
    pan = 0.5 + 0.35 * math.sin(step * 1.7)
    bass = math.sin(2 * math.pi * midi(chord[0] - 24) * t) * min(1, tb * 40) * math.exp(-tb * 2.2)
    # short silence right before the drop so it lands
    gap = 0.0 if DROP - 0.25 <= t < DROP else 1.0
    if full:
        c = 0.55 * k + 0.32 * bass
        l = c + 0.09 * hat + 0.06 * pl_ * swell + 0.16 * arp * (1 - pan)
        r = c + 0.09 * hat + 0.06 * pr_ * swell + 0.16 * arp * pan
    else:
        c = 0.38 * k
        l = c + 0.05 * hat + 0.075 * pl_ * swell + 0.06 * arp * (1 - pan)
        r = c + 0.05 * hat + 0.075 * pr_ * swell + 0.06 * arp * pan
    L[i] = l * gap; R[i] = r * gap

peak = max(max(map(abs, L)), max(map(abs, R)))
g = 10 ** (-1 / 20) / peak
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    fr = bytearray()
    for i in range(N):
        t = i / SR
        fade = min(1.0, t / 0.5, (DUR - t) / 1.5)
        for s in (L[i], R[i]):
            fr += struct.pack("<h", int(max(-1, min(1, s * g * fade)) * 32767))
    w.writeframes(bytes(fr))
print("wrote", os.path.normpath(OUT))
