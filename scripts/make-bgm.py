"""Generate the promo's original music bed (deterministic, no dependencies).

120 BPM electronic loop in A minor: kick, off-beat hats, pad chords and a
pluck arpeggio. Output: assets/audio/bgm.wav (8.5 s, 44.1 kHz stereo).
Replace the file with a licensed track to swap the music.
"""
import math, struct, wave, os

SR, DUR, BPM = 44100, 8.5, 120
BEAT = 60 / BPM
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm.wav")  # encode to bgm.m4a afterwards

def midi(n): return 440 * 2 ** ((n - 69) / 12)

# Am - F - C - G, one bar (4 beats) each, repeated
CHORDS = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]
ARP = [0, 1, 2, 1, 2, 1, 0, 2]

seed = 12345
def noise():
    global seed
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed / 0x3FFFFFFF - 1.0

L = [0.0] * N; R = [0.0] * N
hp_prev_in = hp_prev_out = 0.0
for i in range(N):
    t = i / SR
    beat_pos = t / BEAT
    b = int(beat_pos); tb = t - b * BEAT
    bar = (b // 4) % 4
    chord = CHORDS[bar]
    # kick on every beat
    k = math.sin(2 * math.pi * (45 * tb + 75 * (1 - math.exp(-tb * 30)) / 30)) * math.exp(-tb * 9)
    # hats on off-beats (crude high-pass on noise)
    n = noise()
    hp = 0.95 * (hp_prev_out + n - hp_prev_in); hp_prev_in, hp_prev_out = n, hp
    th = t - (b + 0.5) * BEAT
    hat = hp * math.exp(-th * 45) if th >= 0 else 0.0
    # pad: detuned sines, slow swell per bar
    tbar = t - (b // 4) * 4 * BEAT
    swell = min(1.0, tbar / 0.6) * (0.75 + 0.25 * math.sin(2 * math.pi * t * 0.5))
    padl = padr = 0.0
    for j, note in enumerate(chord):
        f = midi(note)
        padl += math.sin(2 * math.pi * f * 0.998 * t + j) + 0.3 * math.sin(4 * math.pi * f * t)
        padr += math.sin(2 * math.pi * f * 1.002 * t + j * 2) + 0.3 * math.sin(4 * math.pi * f * t)
    # pluck arp: eighth notes, one octave up
    step = int(beat_pos * 2); ts = t - step * BEAT / 2
    f = midi(chord[ARP[step % 8]] + 12)
    env = math.exp(-ts * 14)
    pl = (math.sin(2 * math.pi * f * t) + 0.4 * math.sin(4 * math.pi * f * t)) * env
    pan = 0.5 + 0.35 * math.sin(step * 1.7)
    # bass on the root, following the kick
    bass = math.sin(2 * math.pi * midi(chord[0] - 24) * t) * min(1, tb * 40) * math.exp(-tb * 2.5)
    mixc = 0.55 * k + 0.30 * bass
    L[i] = mixc + 0.10 * hat + 0.06 * padl + 0.16 * pl * (1 - pan)
    R[i] = mixc + 0.10 * hat + 0.06 * padr + 0.16 * pl * pan

# master: fade in 0.05 s, fade out over the last 1.2 s, normalize to -1 dBFS
peak = max(max(abs(x) for x in L), max(abs(x) for x in R))
g = 10 ** (-1 / 20) / peak
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    frames = bytearray()
    for i in range(N):
        t = i / SR
        fade = min(1.0, t / 0.05, (DUR - t) / 1.2)
        for s in (L[i], R[i]):
            frames += struct.pack("<h", int(max(-1, min(1, s * g * fade)) * 32767))
    w.writeframes(bytes(frames))
print("wrote", os.path.normpath(OUT))
