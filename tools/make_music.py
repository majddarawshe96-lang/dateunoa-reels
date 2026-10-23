"""Generate original, royalty-free background music beds for @dateunoa reels.

Usage: python3 tools/make_music.py <out_dir>
Writes music_01.m4a ... music_06.m4a (24 s each, loop-friendly, soft lo-fi / ambient).
Everything is synthesized here, so there is no copyright issue.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

SR = 44100
DUR = 24.0


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a=0.01, d=1.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / d)
    return e


def epiano(freq, n, vel=0.5):
    t = np.arange(n) / SR
    tone = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 3)
            + 0.12 * np.sin(2 * np.pi * 3.01 * freq * t) * np.exp(-t * 6))
    trem = 1 + 0.06 * np.sin(2 * np.pi * 4.5 * t)
    return vel * tone * trem * env(n, 0.008, 1.6)


def pad(freq, n):
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * freq * (1 + d) * t + p) for d, p in ((-0.004, 0), (0.0, 1.3), (0.005, 2.1)))
    a = np.minimum(1, t / 1.2) * np.minimum(1, (n / SR - t) / 1.0)
    return 0.12 * s * np.clip(a, 0, 1)


def lowpass(x, fc):
    b, a = butter(2, fc / (SR / 2))
    return lfilter(b, a, x)


def highpass(x, fc):
    b, a = butter(2, fc / (SR / 2), "high")
    return lfilter(b, a, x)


def reverb(x, secs=2.2, mix=0.3):
    n = int(secs * SR)
    rng = np.random.default_rng(7)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.0 / secs)
    ir = lowpass(ir, 5000)
    wet = fftconvolve(x, ir)[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return (1 - mix) * x / (np.max(np.abs(x)) + 1e-9) + mix * wet


# (bpm, progression as lists of midi notes, bass roots)
TRACKS = [
    (72, [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]], [45, 41, 36, 43]),   # Am7 Fmaj7 Cmaj7 G7
    (68, [[50, 53, 57, 60], [55, 58, 62, 65], [48, 52, 55, 58], [53, 57, 60, 64]], [38, 43, 36, 41]),   # Dm7 Gm7 C7 Fmaj7
    (76, [[52, 55, 59, 62], [48, 52, 55, 59], [45, 48, 52, 55], [47, 50, 54, 57]], [40, 36, 33, 35]),   # Em7 Cmaj7 Am7 Bm7
    (70, [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]], [41, 40, 38, 36]),   # Fmaj7 Em7 Dm7 Cmaj7
    (66, [[49, 52, 56, 59], [45, 49, 52, 56], [47, 51, 54, 57], [44, 47, 51, 54]], [37, 33, 35, 32]),   # C#m7 Amaj7 B7 G#m7
    (74, [[55, 59, 62, 66], [52, 55, 59, 62], [48, 52, 55, 59], [50, 54, 57, 60]], [43, 40, 36, 38]),   # Gmaj7 Em7 Cmaj7 D7
]


def track(i, bpm, prog, bass):
    n = int(DUR * SR)
    out = np.zeros(n)
    beat = 60 / bpm
    bar = 4 * beat
    rng = np.random.default_rng(100 + i)
    t0 = 0.0
    k = 0
    while t0 < DUR:
        chord = prog[k % len(prog)]
        root = bass[k % len(bass)]
        s = int(t0 * SR)
        L = min(int(bar * SR) + int(1.5 * SR), n - s)
        if L <= 0:
            break
        # pad
        for m in chord:
            out[s:s + L] += pad(midi(m), L)
        # piano: chord on beat 1, gentle arpeggio after
        for j, m in enumerate(chord):
            st = s + int(j * 0.012 * SR)
            LL = min(int(2.6 * SR), n - st)
            if LL > 0:
                out[st:st + LL] += epiano(midi(m + 12), LL, 0.18)
        arp = [chord[1] + 12, chord[2] + 12, chord[3] + 12, chord[2] + 12]
        for j, m in enumerate(arp):
            st = s + int((1 + j * 0.75) * beat * SR)
            LL = min(int(1.4 * SR), n - st)
            if LL > 0 and rng.random() > 0.2:
                out[st:st + LL] += epiano(midi(m), LL, 0.10 + 0.04 * rng.random())
        # bass
        for b in (0, 2.5):
            st = s + int(b * beat * SR)
            LL = min(int(1.6 * beat * SR), n - st)
            if LL > 0:
                tt = np.arange(LL) / SR
                out[st:st + LL] += 0.22 * np.sin(2 * np.pi * midi(root) * tt) * env(LL, 0.02, 0.9)
        t0 += bar
        k += 1
    # soft brushed hats + kick
    drums = np.zeros(n)
    for b in range(int(DUR / beat) + 1):
        st = int(b * beat * SR)
        if b % 4 in (0, 2) and st < n:
            LL = min(int(0.35 * SR), n - st)
            tt = np.arange(LL) / SR
            drums[st:st + LL] += 0.35 * np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 9)
        for off in (0.5,):
            hs = int((b + off) * beat * SR)
            if hs < n:
                LL = min(int(0.08 * SR), n - hs)
                drums[hs:hs + LL] += 0.03 * rng.standard_normal(LL) * np.exp(-np.arange(LL) / SR * 60)
    drums = highpass(drums, 40)
    crackle = (rng.random(n) > 0.9993) * rng.standard_normal(n) * 0.03 + 0.0008 * rng.standard_normal(n)
    crackle = lowpass(highpass(crackle, 800), 6000)
    mix = reverb(lowpass(out, 4200), 2.4, 0.32) + 0.5 * drums / (np.max(np.abs(drums)) + 1e-9) * 0.35 + crackle
    # fade in/out
    f = int(0.6 * SR)
    mix[:f] *= np.linspace(0, 1, f)
    mix[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))
    mix = mix / np.max(np.abs(mix)) * 0.6
    return mix


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for i, (bpm, prog, bass) in enumerate(TRACKS, 1):
        x = track(i, bpm, prog, bass)
        stereo = np.stack([x, np.roll(x, int(0.012 * SR))], axis=1)
        pcm = (stereo * 32767).astype(np.int16)
        wav = out / f"music_{i:02d}.wav"
        import wave
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", "loudnorm=I=-18:TP=-2",
                        "-c:a", "aac", "-b:a", "160k", str(out / f"music_{i:02d}.m4a")], check=True)
        wav.unlink()
        print("wrote", out / f"music_{i:02d}.m4a")


if __name__ == "__main__":
    main()
