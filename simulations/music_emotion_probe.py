### music_emotion_probe.py
"""Probe the Emotion Awareness Layer on arbitrary music files.

For each supplied audio file this script:
1. Loads the waveform (mono) using *librosa*.
2. Extracts the envelope of two band-pass regions:
   • θ-band 4-8 Hz → candidate **valence** driver.
   • γ-band 30-50 Hz → candidate **arousal** driver.
3. Computes a 20-frame (~1 s) moving-average over each envelope to match
   the in-engine integration window.
4. Normalises, clips to [-1, 1], and prints summary statistics plus an
   optional time-series plot.

The logic mirrors the Emotion Awareness Layer documented in README.md but
runs *offline* on standalone audio files, letting you estimate how the
engine would respond to different musical genres.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import librosa
import scipy.signal as sps
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("music_probe")

# ---------------------------------------------------------------------
# DSP helpers
# ---------------------------------------------------------------------

def _band_envelope(y: np.ndarray, sr: int, low: float, high: float) -> np.ndarray:
    """Return Hilbert-envelope of band-pass-filtered signal."""
    nyq = 0.5 * sr
    low_n, high_n = low / nyq, high / nyq
    b, a = sps.butter(4, [low_n, high_n], btype="bandpass")
    y_filt = sps.filtfilt(b, a, y)
    analytic = sps.hilbert(y_filt)
    env = np.abs(analytic)
    return env


def _moving_average(x: np.ndarray, window: int) -> np.ndarray:
    """Simple causal moving average (same length as x)."""
    if window <= 1:
        return x.copy()
    cumsum = np.cumsum(np.insert(x, 0, 0.0))
    ma = (cumsum[window:] - cumsum[:-window]) / window
    # pad front with first valid value to keep length
    pad = np.full(window - 1, ma[0])
    return np.concatenate([pad, ma])


# ---------------------------------------------------------------------
# Main analysis per file
# ---------------------------------------------------------------------

def analyse_file(path: Path, plot: bool = False) -> None:
    if not path.exists():
        logger.error("File %s does not exist", path)
        return

    logger.info("Loading %s", path)
    y, sr_orig = librosa.load(path, sr=None, mono=True)

    # Downsample to 200 Hz to make low-frequency band-pass filtering stable
    target_sr = 200  # Hz, sufficient for <= 50 Hz content
    if sr_orig != target_sr:
        # Use polyphase resampling to avoid external dependency
        import math
        gcd = math.gcd(sr_orig, target_sr)
        up = target_sr // gcd
        down = sr_orig // gcd
        y = sps.resample_poly(y, up, down)
        sr = target_sr
    else:
        sr = sr_orig

    # Extract band envelopes
    env_theta = _band_envelope(y, sr, 4.0, 8.0)  # theta band
    env_gamma = _band_envelope(y, sr, 30.0, 50.0)  # gamma band

    # Match engine's ~1 s integration window: with sr=200 Hz ⇒ 200 samples ≈ 1 s
    window_samples = sr  # 1-second window at downsampled rate
    env_theta_ma = _moving_average(env_theta, window=window_samples)
    env_gamma_ma = _moving_average(env_gamma, window=window_samples)

    # Robust scaling: divide by median absolute deviation to get dimensionless unit
    def _scale_clip(x: np.ndarray) -> np.ndarray:
        mad = np.median(np.abs(x - np.median(x))) or 1e-6
        z = (x - np.median(x)) / mad
        return np.clip(z / 10.0, -1.0, 1.0)  # empirical scaling factor

    valence = _scale_clip(env_theta_ma)
    arousal = _scale_clip(env_gamma_ma)

    logger.info(
        "Valence mean: %.3f | median: %.3f   ||   Arousal mean: %.3f | median: %.3f",
        float(np.mean(valence)),
        float(np.median(valence)),
        float(np.mean(arousal)),
        float(np.median(arousal)),
    )

    if plot:
        import matplotlib as mpl

        mpl.rcParams["figure.figsize"] = (12, 4)
        t = np.arange(len(valence)) / sr
        plt.plot(t, valence, label="valence", alpha=0.7)
        plt.plot(t, arousal, label="arousal", alpha=0.7)
        plt.hlines([0], t[0], t[-1], colors="k", linestyles="--", linewidth=0.5)
        plt.ylim(-1.05, 1.05)
        plt.xlabel("Time (s)")
        plt.ylabel("Scaled magnitude")
        plt.title(f"Emotion profile – {path.name}")
        plt.legend()
        plt.tight_layout()
        plt.show()


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Estimate valence/arousal response to music files.")
    p.add_argument("files", nargs="+", help="Audio file paths")
    p.add_argument("--plot", action="store_true", help="Show time-series plots")
    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    for f in args.files:
        analyse_file(Path(f), plot=args.plot)


if __name__ == "__main__":
    main() 