"""Generate original, royalty-free music beds by MOOD for @dateunoa quote reels.

Usage: python3 tools/make_mood_music.py tools/music
Writes tools/music/<mood>/<mood>_NN.m4a (24 s each, loudness-normalised), 3 variations per mood:
  tender      warm slow piano + pads, major 7ths          (love, what real interest looks like)
  melancholy  sparse minor piano, low strings             (heartbreak, walking away, being left on read)
  playful     bouncy plucks, snaps, walking bass          (funny / relatable texting, he says/she says)
  confident   punchy beat, synth bass, minor groove       (standards, self-respect, "Men: ...")
  hopeful     rising arpeggios, light percussion, major   (moving on, soft pitch, new beginnings)
Everything is synthesized here (numpy), so there is no copyright or licensing issue.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from make_music import SR, midi, env, epiano, pad, lowpass, highpass, reverb  # noqa: E402

DUR = 24.0
N = int(DUR * SR)

C = {  # chord shapes (midi), named for readability
    "Cmaj7": [48, 52, 55, 59], "Am7": [45, 48, 52, 55], "Fmaj7": [41, 45, 48, 52], "G6": [43, 47, 50, 52],
    "Dm7": [50, 53, 57, 60], "Em7": [52, 55, 59, 62], "G": [43, 47, 50, 55], "Am": [45, 48, 52, 57],
    "F": [41, 45, 48, 53], "C": [48, 52, 55, 60], "E": [40, 44, 47, 52], "Dm": [50, 53, 57, 62],
    "Bb": [46, 50, 53, 58], "Gm": [43, 46, 50, 55], "Ebmaj7": [51, 55, 58, 62], "Abmaj7": [44, 48, 51, 55],
    "Fm7": [41, 44, 48, 51], "Bbm7": [46, 49, 53, 56], "D": [50, 54, 57, 62], "Bm": [47, 50, 54, 59],
    "A": [45, 49, 52, 57], "Gmaj7": [43, 47, 50, 54], "Em": [40, 43, 47, 52],
}

MOODS = {
    "tender": [(66, ["Cmaj7", "Am7", "Fmaj7", "G6"]), (62, ["Fmaj7", "Em7", "Dm7", "Cmaj7"]), (70, ["Gmaj7", "Em7", "Cmaj7", "D"])],
    "melancholy": [(60, ["Am", "F", "C", "E"]), (58, ["Dm", "Bb", "F", "A"]), (62, ["Em", "C", "G", "Bm"])],
    "playful": [(104, ["C", "F", "G", "C"]), (110, ["G", "C", "D", "G"]), (100, ["F", "Bb", "C", "F"])],
    "confident": [(92, ["Am", "Am", "F", "G"]), (96, ["Dm", "Dm", "Bb", "C"]), (90, ["Em", "Em", "C", "D"])],
    "hopeful": [(84, ["C", "G", "Am", "F"]), (80, ["F", "C", "Dm", "Bb"]), (88, ["G", "D", "Em", "C"])],
}


def pluck(freq, n, vel=0.3, decay=0.25):
    t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * freq * t)) * 0.3 + np.sin(2 * np.pi * freq * t)
    return vel * lowpass(s, min(6000, freq * 6)) * np.exp(-t / decay) * np.minimum(1, t / 0.003)


def kick(n, vel=0.9):
    t = np.arange(n) / SR
    return vel * np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 7)


def noise_hit(n, rng, decay, vel, hp=3000):
    return vel * highpass(rng.standard_normal(n), hp) * np.exp(-np.arange(n) / SR / decay)


def add(out, x, start):
    s = int(start * SR)
    if s >= len(out):
        return
    e = min(len(out), s + len(x))
    out[s:e] += x[: e - s]


def render(mood, bpm, prog, seed):
    rng = np.random.default_rng(seed)
    beat = 60 / bpm
    bar = 4 * beat
    music = np.zeros(N)
    drums = np.zeros(N)
    nbars = int(DUR / bar) + 1
    for k in range(nbars):
        ch = C[prog[k % len(prog)]]
        t0 = k * bar
        L = int((bar + 1.2) * SR)
        if mood in ("tender", "melancholy", "hopeful"):
            for m in ch:
                add(music, pad(midi(m), L) * (0.8 if mood == "melancholy" else 1.0), t0)
        if mood == "tender":
            for j, m in enumerate(ch):
                add(music, epiano(midi(m + 12), int(2.8 * SR), 0.16), t0 + j * 0.015)
            for j, m in enumerate([ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 24]):
                if rng.random() > 0.25:
                    add(music, epiano(midi(m), int(1.6 * SR), 0.09), t0 + (1 + j * 0.75) * beat)
            add(music, 0.2 * np.sin(2 * np.pi * midi(ch[0] - 12) * np.arange(int(bar * SR)) / SR) * env(int(bar * SR), 0.05, 2.0), t0)
        elif mood == "melancholy":
            add(music, epiano(midi(ch[0] + 12), int(3 * SR), 0.15), t0)
            for j, m in enumerate([ch[2] + 12, ch[1] + 24, ch[3] + 12]):
                add(music, epiano(midi(m), int(2.2 * SR), 0.08 + 0.03 * rng.random()), t0 + (1.5 + j) * beat)
            cello = np.sin(2 * np.pi * midi(ch[0] - 12) * np.arange(L) / SR) * 0.14
            add(music, cello * np.minimum(1, np.arange(L) / SR / 0.8) * np.exp(-np.arange(L) / SR / 3), t0)
        elif mood == "hopeful":
            seq = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 24, ch[3] + 12, ch[1] + 24, ch[2] + 12]
            for j, m in enumerate(seq):
                add(music, epiano(midi(m), int(1.2 * SR), 0.09), t0 + j * beat / 2)
            add(music, 0.2 * np.sin(2 * np.pi * midi(ch[0] - 12) * np.arange(int(bar * SR)) / SR) * env(int(bar * SR), 0.05, 1.5), t0)
            for b in range(4):
                add(drums, noise_hit(int(0.06 * SR), rng, 0.02, 0.05), t0 + (b + 0.5) * beat)
            add(drums, kick(int(0.4 * SR), 0.5), t0)
            add(drums, kick(int(0.4 * SR), 0.4), t0 + 2.5 * beat)
        elif mood == "playful":
            pattern = [0, 2, 1, 3, 2, 1, 3, 2]
            for j, p in enumerate(pattern):
                if rng.random() > 0.15:
                    add(music, pluck(midi(ch[p] + 12), int(0.4 * SR), 0.22, 0.18), t0 + j * beat / 2)
            for b in range(4):  # walking bass
                add(music, pluck(midi(ch[b % 3] - 12), int(beat * SR), 0.35, 0.2), t0 + b * beat)
                if b in (1, 3):  # finger snaps
                    add(drums, noise_hit(int(0.12 * SR), rng, 0.03, 0.25, 1500), t0 + b * beat)
        elif mood == "confident":
            for j in range(8):
                m = ch[[0, 2, 1, 3, 0, 2, 3, 1][j]] + 12
                add(music, pluck(midi(m), int(0.3 * SR), 0.16, 0.12), t0 + j * beat / 2)
            for j in range(8):  # synth bass on eighths
                if j not in (3, 7) or rng.random() > 0.5:
                    nb = int(beat / 2 * SR)
                    tt = np.arange(nb) / SR
                    add(music, 0.3 * lowpass(np.sign(np.sin(2 * np.pi * midi(ch[0] - 12) * tt)), 400) * np.exp(-tt * 6), t0 + j * beat / 2)
            for b in range(4):
                if b in (0, 2):
                    add(drums, kick(int(0.45 * SR), 1.0), t0 + b * beat)
                else:
                    add(drums, noise_hit(int(0.2 * SR), rng, 0.06, 0.5, 900) + kick(int(0.2 * SR), 0.2), t0 + b * beat)
                for h in (0, 0.5):
                    add(drums, noise_hit(int(0.05 * SR), rng, 0.015, 0.12), t0 + (b + h) * beat)
    wetmix = {"tender": 0.32, "melancholy": 0.4, "hopeful": 0.3, "playful": 0.15, "confident": 0.12}[mood]
    mix = reverb(lowpass(music, 6500 if mood in ("playful", "confident") else 4500), 2.6, wetmix)
    if np.max(np.abs(drums)) > 0:
        mix += drums / np.max(np.abs(drums)) * {"hopeful": 0.25, "playful": 0.35, "confident": 0.6}.get(mood, 0)
    mix += lowpass(highpass(0.0006 * rng.standard_normal(N), 800), 6000)  # a touch of tape air
    f = int(0.4 * SR)
    mix[:f] *= np.linspace(0, 1, f)
    mix[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))
    return mix / (np.max(np.abs(mix)) + 1e-9) * 0.7


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "tools/music")
    for mood, variants in MOODS.items():
        d = root / mood
        d.mkdir(parents=True, exist_ok=True)
        for i, (bpm, prog) in enumerate(variants, 1):
            x = render(mood, bpm, prog, seed=hash((mood, i)) % 1000)
            stereo = np.stack([x, np.roll(x, int(0.011 * SR))], axis=1)
            wav = d / f"{mood}_{i:02d}.wav"
            with wave.open(str(wav), "wb") as w:
                w.setnchannels(2)
                w.setsampwidth(2)
                w.setframerate(SR)
                w.writeframes((stereo * 32767).astype(np.int16).tobytes())
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5",
                            "-c:a", "aac", "-b:a", "160k", str(d / f"{mood}_{i:02d}.m4a")], check=True)
            wav.unlink()
            print("wrote", d / f"{mood}_{i:02d}.m4a")


if __name__ == "__main__":
    main()
