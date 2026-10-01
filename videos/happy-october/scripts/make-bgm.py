"""Generate the soft music bed for "Happy October" (deterministic, numpy only).

72 BPM, F - Am - Bb - C. Warm pad, music-box arpeggio with a short echo,
and a soft bass. Writes assets/audio/bgm.wav; encode to bgm.m4a afterwards.
"""
import os, wave
import numpy as np

SR, DUR, BPM = 44100, 15.0, 72
BEAT = 60 / BPM
t = np.arange(int(SR * DUR)) / SR
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")

def hz(n): return 440 * 2 ** ((n - 69) / 12)

CHORDS = [[53, 57, 60, 64], [57, 60, 64, 67], [58, 62, 65, 69], [60, 64, 67, 70]]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]
bar = (t // (4 * BEAT)).astype(int) % 4

pad_l = np.zeros_like(t); pad_r = np.zeros_like(t)
for v in range(4):
    f = np.array([hz(c[v]) for c in CHORDS])[bar]
    pad_l += np.sin(2 * np.pi * f * 0.998 * t + v) + 0.2 * np.sin(4 * np.pi * f * t)
    pad_r += np.sin(2 * np.pi * f * 1.002 * t + 2 * v) + 0.2 * np.sin(4 * np.pi * f * t)
tbar = t % (4 * BEAT)
swell = np.minimum(1, tbar / 1.2) * (0.75 + 0.25 * np.cos(2 * np.pi * tbar / (4 * BEAT)))
pad_l *= swell; pad_r *= swell

# music box: eighth notes, bell-like partials, fast decay
box = np.zeros_like(t)
step_len = BEAT / 2
for s in range(int(DUR / step_len)):
    st = s * step_len
    b = int(st // (4 * BEAT)) % 4
    note = CHORDS[b][ARP[s % 8]] + 12 + (12 if s % 16 == 7 else 0)
    i0 = int(st * SR); n = int(1.6 * SR)
    tt = np.arange(min(n, len(t) - i0)) / SR
    f = hz(note)
    env = np.exp(-tt * 3.2) * np.minimum(1, tt * 400)
    box[i0:i0 + len(tt)] += env * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt * 6))

bass = np.zeros_like(t)
for k in range(int(DUR / (2 * BEAT)) + 1):
    st = k * 2 * BEAT; i0 = int(st * SR)
    if i0 >= len(t): break
    tt = np.arange(min(int(2 * BEAT * SR), len(t) - i0)) / SR
    f = hz(CHORDS[int(st // (4 * BEAT)) % 4][0] - 24)
    bass[i0:i0 + len(tt)] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 1.5) * np.minimum(1, tt * 60)

def echo(x, d, g, n=4):
    y = x.copy(); k = int(d * SR)
    for j in range(1, n + 1):
        y[j * k:] += (g ** j) * x[:-j * k]
    return y

box_l = echo(box, 0.375, 0.35); box_r = echo(np.roll(box, int(0.012 * SR)), 0.5, 0.3)
L = 0.05 * pad_l + 0.16 * box_l + 0.22 * bass
R = 0.05 * pad_r + 0.16 * box_r + 0.22 * bass
fade = np.minimum(1, t / 1.5) * np.minimum(1, (DUR - t) / 2.5)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
pcm = (np.stack([L, R], 1) / peak * 0.8 * 32767).astype("<i2")
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", OUT)
