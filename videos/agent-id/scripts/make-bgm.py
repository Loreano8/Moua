"""Original upbeat electronic bed for the Agent ID video (numpy only).

120 BPM, A minor, Am - F - C - G (one chord per bar), 14 bars = 28 s.
Bars 0-1: filtered pad + pluck and a noise riser into the drop at 4 s.
Bars 2-13: four-on-the-floor kick, claps on 2 and 4, off-beat open hats,
16th closed hats, off-beat sub bass, sidechained pad and a 16th pluck
arpeggio. Writes assets/audio/bgm.wav; encode to bgm.m4a afterwards.
"""
import os, wave
import numpy as np

SR, BPM, BARS = 44100, 120, 14
BEAT = 60 / BPM
BAR = 4 * BEAT
DUR = BARS * BAR
N = int(SR * DUR)
t = np.arange(N) / SR
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")
rng = np.random.default_rng(120)

def midi(n): return 440.0 * 2 ** ((np.asarray(n) - 69) / 12)

CHORDS = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
ROOTS = [33, 29, 36, 31]
DROP = 2 * BAR

def onepole(x, cutoff):
    """Simple one-pole low-pass; cutoff may be an array (Hz)."""
    a = np.exp(-2 * np.pi * np.broadcast_to(cutoff, x.shape) / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s
        y[i] = s
    return y

def saw(f, ph=0.0, harm=14):
    out = np.zeros(N)
    for k in range(1, harm + 1):
        out += np.sin(2 * np.pi * f * k * t + ph * k) / k
    return out * 0.6

def env(start, length, attack=0.003, decay=None):
    e = np.zeros(N)
    i0, i1 = int(start * SR), min(N, int((start + length) * SR))
    if i0 >= N: return e
    x = (np.arange(i1 - i0) / SR)
    d = decay if decay is not None else length
    e[i0:i1] = np.minimum(1, x / attack) * np.exp(-x / d)
    return e

bar_idx = np.minimum((t // BAR).astype(int), BARS - 1)
chord_of = lambda b: CHORDS[b % 4]

# Sidechain: duck everything melodic on each kick after the drop
side = np.ones(N)
for b in range(int(DUR / BEAT)):
    st = b * BEAT
    if st < DROP: continue
    i0 = int(st * SR); i1 = min(N, int((st + BEAT) * SR))
    x = np.arange(i1 - i0) / SR
    side[i0:i1] = 0.35 + 0.65 * np.minimum(1, x / 0.18)

# Pad: three detuned saws per chord note, filter opens into the drop
pad = np.zeros(N)
for b in range(BARS):
    i0, i1 = int(b * BAR * SR), min(N, int((b + 1) * BAR * SR))
    seg = np.zeros(N)
    for n in chord_of(b):
        f = midi(n)
        for d in (-0.08, 0.0, 0.09):
            seg += np.sin(2 * np.pi * f * (1 + d / 100) * t) + 0.5 * np.sin(2 * np.pi * 2 * f * (1 + d / 100) * t) + 0.25 * np.sin(2 * np.pi * 3 * f * t)
    pad[i0:i1] += seg[i0:i1]
pad *= 0.06
cut = np.where(t < DROP, 600 + 2400 * (t / DROP) ** 2, 3200.0)
pad = onepole(pad, cut) * side

# Pluck arpeggio (16ths) over the chord, up an octave
arp = np.zeros(N)
pattern = [0, 1, 2, 1, 0, 2, 1, 2]
for s16 in range(int(DUR / (BEAT / 4))):
    st = s16 * BEAT / 4
    b = int(st // BAR)
    n = chord_of(b)[pattern[s16 % 8]] + 12
    e = env(st, 0.22, 0.002, 0.07)
    arp += e * (np.sin(2 * np.pi * midi(n) * t) + 0.3 * np.sin(2 * np.pi * 2 * midi(n) * t))
arp = onepole(arp * 0.11, np.where(t < DROP, 1800.0, 5000.0)) * side

# Sub bass: off-beat 8ths on the root after the drop
bass = np.zeros(N)
for e8 in range(int(DUR / (BEAT / 2))):
    st = e8 * BEAT / 2
    if st < DROP or e8 % 2 == 0: continue
    f = midi(ROOTS[int(st // BAR) % 4])
    e = env(st, BEAT / 2 * 0.95, 0.004, 0.25)
    bass += e * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t))
bass *= 0.32

# Drums
kick = np.zeros(N); clap = np.zeros(N); hats = np.zeros(N)
noise = rng.uniform(-1, 1, N)
hp = noise - onepole(noise, 6000.0)
for b in range(int(DUR / BEAT)):
    st = b * BEAT
    if st < DROP: continue
    i0 = int(st * SR); i1 = min(N, i0 + int(0.4 * SR))
    x = np.arange(i1 - i0) / SR
    kick[i0:i1] += np.sin(2 * np.pi * (45 * x + 110 * (1 - np.exp(-x * 28)) / 28)) * np.exp(-x * 7)
    if b % 2 == 1:
        j1 = min(N, i0 + int(0.25 * SR)); y = np.arange(j1 - i0) / SR
        burst = sum(np.exp(-np.maximum(0, y - o) * 60) * (y >= o) for o in (0, 0.011, 0.022))
        clap[i0:j1] += noise[i0:j1] * burst * np.exp(-y * 9)
    oh = st + BEAT / 2
    k0 = int(oh * SR); k1 = min(N, k0 + int(0.18 * SR))
    if k0 < N:
        z = np.arange(k1 - k0) / SR
        hats[k0:k1] += hp[k0:k1] * np.exp(-z * 22) * 0.9
for s16 in range(int(DUR / (BEAT / 4))):
    st = s16 * BEAT / 4
    if st < DROP: continue
    k0 = int(st * SR); k1 = min(N, k0 + int(0.04 * SR))
    z = np.arange(k1 - k0) / SR
    hats[k0:k1] += hp[k0:k1] * np.exp(-z * 90) * (0.5 if s16 % 2 else 0.3)
clap = onepole(clap, 2500.0)

# Riser into the drop and an impact on it
riser = np.zeros(N)
r0, r1 = int((DROP - 2 * BEAT) * SR), int(DROP * SR)
x = np.linspace(0, 1, r1 - r0)
riser[r0:r1] = noise[r0:r1] * x ** 2 * 0.5
riser = onepole(riser, np.where(t < DROP, 300 + 7000 * np.clip((t - (DROP - 2 * BEAT)) / (2 * BEAT), 0, 1), 300.0))
impact = env(DROP, 1.6, 0.002, 0.45) * (np.sin(2 * np.pi * 50 * t) * 0.8 + onepole(noise, 900.0) * 0.6)

mix = pad + arp + bass + 0.9 * kick + 0.38 * clap + 0.08 * hats + riser + 0.6 * impact
mix = np.tanh(mix * 1.3)
fade = np.minimum(1, t / 0.3) * np.minimum(1, (DUR - t) / 1.6)
mix *= fade
mix /= np.max(np.abs(mix)) / 10 ** (-1.0 / 20)
# small stereo width: delayed copy on the right
d = int(0.012 * SR)
L = mix; R = np.concatenate([mix[:d], mix[:-d]]) * 0.92 + mix * 0.08
pcm = (np.stack([L, R], axis=1) * 32767).astype("<i2")
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", os.path.normpath(OUT), round(DUR, 3), "s")
