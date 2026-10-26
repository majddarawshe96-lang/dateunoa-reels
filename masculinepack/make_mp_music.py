"""Original, royalty-free masculine music beds for @masculinepack quote reels.

Usage: python3 masculinepack/make_mp_music.py masculinepack/music
Writes masculinepack/music/<mood>/<mood>_NN.m4a (24 s each, loudness-normalised), 3 variations per mood:
  dark    half-time trap/phonk feel: minor piano, sliding 808, rolling hats   (harsh truths, discipline, "nobody is coming")
  epic    cinematic war drums, low string drone, rising brass swell            (purpose, mission, power, legacy)
  stoic   solemn minor piano, low cello, heartbeat kick                       (calm, frame, loneliness, reflection)
  grind   driving minor beat, plucked arps, synth bass                         (gym, work, money, building)
Everything is synthesized with numpy, so there is no copyright or licensing issue.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from make_music import SR, midi, env, epiano, lowpass, highpass, reverb  # noqa: E402

DUR = 24.0
N = int(DUR * SR)

C = {"Am": [45, 48, 52], "F": [41, 45, 48], "E": [40, 44, 47], "Dm": [38, 41, 45], "Bb": [46, 50, 53],
     "C": [48, 52, 55], "G": [43, 47, 50], "Em": [40, 43, 47], "Cm": [48, 51, 55], "Ab": [44, 48, 51],
     "Eb": [51, 55, 58], "Gm": [43, 46, 50], "Fm": [41, 44, 48], "Bm": [47, 50, 54], "D": [50, 54, 57],
     "A": [45, 49, 52], "Db": [49, 53, 56], "Bbm": [46, 49, 53]}

MOODS = {
    "dark": [(140, ["Am", "F", "Dm", "E"]), (136, ["Cm", "Ab", "Fm", "G"]), (144, ["Em", "C", "Am", "Bm"])],
    "epic": [(84, ["Dm", "Bb", "C", "A"]), (80, ["Cm", "Ab", "Eb", "G"]), (88, ["Em", "C", "D", "Bm"])],
    "stoic": [(60, ["Am", "Em", "F", "E"]), (56, ["Dm", "Am", "Bb", "A"]), (62, ["Cm", "Gm", "Ab", "G"])],
    "grind": [(100, ["Am", "Am", "F", "G"]), (104, ["Dm", "Dm", "Bb", "C"]), (98, ["Fm", "Fm", "Db", "Eb"])],
}


def add(out, x, start):
    s = int(start * SR)
    if s >= len(out):
        return
    e = min(len(out), s + len(x))
    out[s:e] += x[: e - s]


def t_(n):
    return np.arange(n) / SR


def kick(n, vel=1.0, f0=48, sweep=110, decay=6.0):
    t = t_(n)
    ph = 2 * np.pi * np.cumsum(f0 + sweep * np.exp(-t * 28)) / SR
    return vel * np.sin(ph) * np.exp(-t * decay)


def noise(n, rng, decay, vel, hp=3000, lp=None):
    x = highpass(rng.standard_normal(n), hp)
    if lp:
        x = lowpass(x, lp)
    return vel * x * np.exp(-t_(n) / decay)


def snare(n, rng, vel=0.8):
    t = t_(n)
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    return vel * (0.5 * body + noise(n, rng, 0.09, 1.0, 1200, 9000))


def b808(freq, n, vel=0.9, glide_from=None):
    t = t_(n)
    f = np.full(n, freq) if glide_from is None else freq + (glide_from - freq) * np.exp(-t * 12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(2.2 * np.sin(ph)) * np.minimum(1, t / 0.004) * np.exp(-t * 1.6)
    return vel * x


def saw(freq, n, harm=14):
    t = t_(n)
    return sum(((-1) ** (k + 1)) * np.sin(2 * np.pi * k * freq * t) / k for k in range(1, harm))


def strings(freq, n, vel=0.18, fc=900):
    x = sum(saw(freq * (1 + d), n, 10) for d in (-0.005, 0.0, 0.006))
    a = np.clip(np.minimum(t_(n) / 1.0, (n / SR - t_(n)) / 0.8), 0, 1)
    return vel * lowpass(x, fc) * a


def piano(freq, n, vel=0.3):
    return epiano(freq, n, vel)


def render(mood, bpm, prog, seed):
    rng = np.random.default_rng(seed)
    beat = 60 / bpm
    music, drums = np.zeros(N), np.zeros(N)
    if mood == "dark":  # half-time: one chord per bar of 4 beats at bpm, snare on beat 3
        bar = 4 * beat
        nb = int(DUR / bar) + 1
        for k in range(nb):
            ch = C[prog[k % len(prog)]]
            t0 = k * bar
            for j, m in enumerate([ch[0] + 24, ch[2] + 12, ch[1] + 24, ch[2] + 12]):  # sparse minor bell-piano
                add(music, piano(midi(m), int(1.4 * SR), 0.13), t0 + j * beat)
            add(music, strings(midi(ch[0]), int((bar + 0.6) * SR), 0.07, 700), t0)
            add(drums, kick(int(0.3 * SR), 0.6), t0)
            prev = C[prog[(k - 1) % len(prog)]][0] - 24
            add(music, b808(midi(ch[0] - 24), int(bar * 0.95 * SR), 0.55, midi(prev) if k % 2 else None), t0)
            add(drums, snare(int(0.35 * SR), rng, 0.7), t0 + 2 * beat)
            for h in range(16):  # hats with occasional rolls
                vel = 0.10 if h % 2 else 0.14
                add(drums, noise(int(0.04 * SR), rng, 0.012, vel, 7000), t0 + h * beat / 4)
                if h in (13, 14) and rng.random() > 0.4:
                    for r in range(3):
                        add(drums, noise(int(0.03 * SR), rng, 0.008, 0.08, 7000), t0 + (h + r / 3) * beat / 4)
        wet, dmix = 0.25, 0.55
    elif mood == "epic":
        bar = 4 * beat
        nb = int(DUR / bar) + 1
        for k in range(nb):
            ch = C[prog[k % len(prog)]]
            t0 = k * bar
            L = int((bar + 0.8) * SR)
            for m in ch:
                add(music, strings(midi(m), L, 0.11, 1100 + 120 * k), t0)
            add(music, strings(midi(ch[0] - 12), L, 0.12, 500), t0)
            if k >= 2:  # brass swell (opening filter)
                n2 = int(bar * SR)
                sw = saw(midi(ch[0] + 12), n2, 12)
                swell = lowpass(sw * np.linspace(0.02, 0.16, n2), 1800) * np.minimum(1, t_(n2) / 0.3)
                add(music, swell, t0)
            for b, v in ((0, 1.0), (1.5, 0.6), (2, 0.85), (3, 0.5), (3.5, 0.7)):  # war drums
                add(drums, kick(int(0.9 * SR), v, 42, 70, 3.2), t0 + b * beat)
                add(drums, noise(int(0.25 * SR), rng, 0.05, 0.25 * v, 200, 2500), t0 + b * beat)
            add(drums, snare(int(0.5 * SR), rng, 0.35), t0 + 3 * beat)
        wet, dmix = 0.35, 0.6
    elif mood == "stoic":
        bar = 4 * beat
        nb = int(DUR / bar) + 1
        for k in range(nb):
            ch = C[prog[k % len(prog)]]
            t0 = k * bar
            add(music, piano(midi(ch[0]), int(3.5 * SR), 0.2), t0)
            add(music, piano(midi(ch[0] + 12), int(3.5 * SR), 0.12), t0 + 0.01)
            for j, m in enumerate([ch[1] + 12, ch[2] + 12, ch[0] + 24]):
                add(music, piano(midi(m), int(2.4 * SR), 0.09 + 0.03 * rng.random()), t0 + (1 + j) * beat)
            add(music, strings(midi(ch[0] - 12), int((bar + 1) * SR), 0.16, 450), t0)
            for b in (0, 2):  # heartbeat
                add(drums, kick(int(0.4 * SR), 0.7, 44, 50, 9), t0 + b * beat)
                add(drums, kick(int(0.4 * SR), 0.45, 44, 50, 9), t0 + b * beat + 0.22)
        wet, dmix = 0.42, 0.35
    else:  # grind
        bar = 4 * beat
        nb = int(DUR / bar) + 1
        for k in range(nb):
            ch = C[prog[k % len(prog)]]
            t0 = k * bar
            for j in range(16):
                m = ch[[0, 2, 1, 2][j % 4]] + 24
                add(music, lowpass(np.sign(np.sin(2 * np.pi * midi(m) * t_(int(0.15 * SR)))), 3000) * 0.07 * np.exp(-t_(int(0.15 * SR)) * 18), t0 + j * beat / 4)
            for j in range(8):
                nb2 = int(beat / 2 * SR)
                add(music, 0.32 * lowpass(saw(midi(ch[0] - 12), nb2, 8), 380) * np.exp(-t_(nb2) * 5), t0 + j * beat / 2)
            add(music, strings(midi(ch[0] + 12), int((bar + 0.4) * SR), 0.05, 1400), t0)
            for b in range(4):
                add(drums, kick(int(0.35 * SR), 1.0 if b in (0, 2) else 0.0), t0 + b * beat)
                if b in (1, 3):
                    add(drums, snare(int(0.3 * SR), rng, 0.8), t0 + b * beat)
                for h in (0, 0.5):
                    add(drums, noise(int(0.04 * SR), rng, 0.012, 0.12, 7000), t0 + (b + h) * beat)
            add(drums, kick(int(0.3 * SR), 0.7), t0 + 2.75 * beat)
        wet, dmix = 0.15, 0.6
    mix = reverb(lowpass(music, 7000), 2.8, wet)
    if np.max(np.abs(drums)) > 0:
        mix += drums / np.max(np.abs(drums)) * dmix
    f = int(0.05 * SR)
    mix[:f] *= np.linspace(0, 1, f)
    mix[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))
    return np.tanh(1.3 * mix / (np.max(np.abs(mix)) + 1e-9)) * 0.8


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "masculinepack/music")
    for mood, variants in MOODS.items():
        d = root / mood
        d.mkdir(parents=True, exist_ok=True)
        for i, (bpm, prog) in enumerate(variants, 1):
            x = render(mood, bpm, prog, seed=1000 + 17 * i + len(mood))
            stereo = np.stack([x, np.roll(x, int(0.012 * SR))], axis=1)
            wav = d / f"{mood}_{i:02d}.wav"
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(2)
                w.setsampwidth(2)
                w.setframerate(SR)
                w.writeframes((np.clip(stereo, -1, 1) * 32767).astype(np.int16).tobytes())
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", "loudnorm=I=-15:TP=-1.5",
                            "-c:a", "aac", "-b:a", "160k", str(d / f"{mood}_{i:02d}.m4a")], check=True)
            wav.unlink()
            print("wrote", d / f"{mood}_{i:02d}.m4a")


if __name__ == "__main__":
    main()
