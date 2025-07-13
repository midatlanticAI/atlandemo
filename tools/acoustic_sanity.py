"""acoustic_sanity.py
Quick-and-dirty acoustic sanity checker for a single WAV file containing dolphin whistles/clicks.

Usage (from repo root):
    python -m tools.acoustic_sanity --file samples/bottlenose.wav

The script prints basic stats (duration, sample rate) and attempts a very
simple click-train detection followed by inter-click-interval (ICI)
stats.  This is *not* production-ready detection—just enough to verify the
signal contains stereotyped dolphin acoustic events.
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, hilbert

# -------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("acoustic_sanity")

# -------------------------------------------------------------
# Dataclasses for results
# -------------------------------------------------------------

@dataclasses.dataclass
class BasicStats:
    sample_rate: int
    num_samples: int

    @property
    def duration_sec(self) -> float:
        return self.num_samples / self.sample_rate

    def to_string(self) -> str:
        return (
            f"Sample rate: {self.sample_rate} Hz\n"
            f"Number of samples: {self.num_samples} (≈ {self.duration_sec:.2f} s)"
        )


@dataclasses.dataclass
class ICIStats:
    num_peaks: int
    mean_ms: float | None
    median_ms: float | None
    min_ms: float | None
    max_ms: float | None

    def to_string(self) -> str:
        if self.num_peaks < 2:
            return "<Too few peaks to compute ICI stats>"
        return (
            f"Detected {self.num_peaks} peaks\n"
            f"ICI  mean: {self.mean_ms:.3f} ms | median: {self.median_ms:.3f} ms | "
            f"min: {self.min_ms:.3f} ms | max: {self.max_ms:.3f} ms"
        )


# -------------------------------------------------------------
# Signal-processing helpers
# -------------------------------------------------------------


def highpass(signal: np.ndarray, sr: int, cutoff: float = 1000.0, order: int = 4) -> np.ndarray:
    """Butterworth high-pass filter."""
    nyq = 0.5 * sr
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="high", analog=False)
    return filtfilt(b, a, signal)


def detect_click_peaks(
    signal: np.ndarray,
    sr: int,
    threshold_std: float = 4.0,
    refractory_ms: float = 1.0,
) -> np.ndarray:
    """Very naïve peak picking on the signal envelope.

    Parameters
    ----------
    signal: np.ndarray
        Audio signal (mono, float32/float64).
    sr: int
        Sample rate in Hz.
    threshold_std: float
        Envelope values above `threshold_std` * MAD will be counted as peaks.
    refractory_ms: float
        Minimum silence after a peak (ms) to avoid double-counting.
    """
    analytic = hilbert(signal)
    envelope = np.abs(analytic)

    # Robust threshold using median absolute deviation (MAD)
    mad = np.median(np.abs(envelope - np.median(envelope)))
    if mad == 0:
        logger.warning("MAD is zero—signal may be silent or constant.")
        return np.array([], dtype=int)

    thresh = threshold_std * mad
    peak_indices = np.where(envelope > thresh)[0]
    if peak_indices.size == 0:
        return np.array([], dtype=int)

    # Enforce refractory period
    refractory_samples = int(refractory_ms / 1000.0 * sr)
    cleaned_peaks = [peak_indices[0]]
    last_idx = peak_indices[0]
    for idx in peak_indices[1:]:
        if idx - last_idx >= refractory_samples:
            cleaned_peaks.append(idx)
            last_idx = idx
    return np.array(cleaned_peaks, dtype=int)


def compute_ici(peaks: np.ndarray, sr: int) -> np.ndarray:
    """Convert peak sample indices to millisecond ICIs."""
    if peaks.size < 2:
        return np.array([], dtype=float)
    diff_samples = np.diff(peaks)
    return diff_samples / sr * 1000.0  # convert to ms


# -------------------------------------------------------------
# Main analysis routine
# -------------------------------------------------------------


def analyze_wav(path: Path) -> None:
    if not path.exists():
        logger.error("File %s does not exist", path)
        sys.exit(1)

    logger.info("Loading WAV %s", path)
    sr, audio = wavfile.read(path)

    # Ensure mono float64
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    audio = audio.astype(np.float64)

    stats = BasicStats(sample_rate=sr, num_samples=len(audio))
    logger.info(stats.to_string())

    # High-pass to remove boat noise / flow noise
    filtered = highpass(audio, sr)

    # Peak detection on filtered signal
    peaks = detect_click_peaks(filtered, sr)
    icis_ms = compute_ici(peaks, sr)

    if icis_ms.size > 0:
        ici_stats = ICIStats(
            num_peaks=peaks.size,
            mean_ms=float(np.mean(icis_ms)),
            median_ms=float(np.median(icis_ms)),
            min_ms=float(np.min(icis_ms)),
            max_ms=float(np.max(icis_ms)),
        )
    else:
        ici_stats = ICIStats(num_peaks=0, mean_ms=None, median_ms=None, min_ms=None, max_ms=None)

    logger.info(ici_stats.to_string())


# -------------------------------------------------------------
# CLI glue
# -------------------------------------------------------------


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Quick sanity checker for dolphin acoustic files")
    p.add_argument("--file", type=str, required=True, help="Path to WAV file to analyze")
    return p


if __name__ == "__main__":
    parser = _build_arg_parser()
    args = parser.parse_args()
    analyze_wav(Path(args.file).expanduser()) 