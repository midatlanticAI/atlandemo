import os
import sys
import time
import argparse
from typing import List, Dict, Tuple

import numpy as np

# Optional heavy dependencies for MFCC tokenisation – loaded lazily
try:
    import librosa  # type: ignore
except ModuleNotFoundError:
    librosa = None  # noqa: N818

try:
    from sklearn.cluster import KMeans  # type: ignore
except ModuleNotFoundError:
    KMeans = None

# Ensure we can import WaveEngine without installing the package
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from wave_engine_multi_lang.python.wave_engine import WaveEngine  # noqa: E402


def generate_synthetic_signal(kind: str, duration: float = 5.0, sr: int = 22_050) -> Tuple[np.ndarray, int]:
    """Generate a synthetic audio waveform for quick experimentation.

    Args:
        kind: One of 'bird', 'whale', 'wow', or 'noise'.
        duration: Signal length in seconds.
        sr: Sample rate.

    Returns:
        Tuple of (audio, sample_rate).
    """
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    if kind == "bird":
        # Rapid chirps around 4 kHz with amplitude modulation
        base = 4_000  # 4 kHz
        chirp = np.sin(2 * np.pi * base * t)
        envelope = 0.5 * (1 + np.sin(2 * np.pi * 3 * t))
        signal = envelope * chirp
    elif kind == "whale":
        # Low-frequency moan ~150 Hz with slow modulation
        base = 150  # 150 Hz
        moan = np.sin(2 * np.pi * base * t)
        envelope = 0.5 * (1 + np.sin(2 * np.pi * 0.3 * t))
        signal = 0.8 * envelope * moan
    elif kind == "wow":
        # Narrow-band burst emulating the 1977 "Wow!" signal (use 1.42 kHz here for Nyquist)
        freq = 1_420  # Hz
        signal = np.zeros_like(t)
        burst_mask = (t > 1.0) & (t < 1.2)
        signal[burst_mask] = 0.7 * np.sin(2 * np.pi * freq * t[burst_mask])
    else:  # 'noise'
        signal = 0.05 * np.random.randn(len(t))
    return signal.astype(np.float32), sr


def frame_signal(signal: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    """Convert 1-D signal to 2-D array of overlapping frames."""
    num_frames = 1 + (len(signal) - frame_size) // hop_size
    indices = np.arange(num_frames)[:, None] * hop_size + np.arange(frame_size)
    return signal[indices]


def tokenise_fft(frames: np.ndarray, sr: int) -> List[str]:
    """Dominant-frequency hash (baseline tokeniser)."""
    fft = np.fft.rfft(frames * np.hanning(frames.shape[1]), axis=1)
    mags = np.abs(fft)
    peak_bins = np.argmax(mags, axis=1)
    freqs = peak_bins * sr / frames.shape[1]
    return [f"FREQ_{int(f):04d}" for f in freqs]


def tokenise_mfcc(signal: np.ndarray, sr: int, frame_size: int, hop_size: int, n_mfcc: int = 20, n_clusters: int = 128) -> List[str]:
    """Tokenise using MFCC features + on-the-fly KMeans vector quantisation.

    Returns a list of symbolic labels (e.g., "MFCC_042").
    """
    if librosa is None or KMeans is None:
        raise ImportError("MFCC tokeniser requires 'librosa' and 'scikit-learn'. Please install them first.")

    mfcc = librosa.feature.mfcc(y=signal.astype(float), sr=sr, n_mfcc=n_mfcc, n_fft=frame_size, hop_length=hop_size)
    frames = mfcc.T  # shape: (num_frames, n_mfcc)

    # Fit KMeans on the current clip – fast for a few hundred frames
    kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=0)
    labels = kmeans.fit_predict(frames)
    return [f"MFCC_{label:03d}" for label in labels]


def run_pipeline(
    kind: str,
    duration: float = 5.0,
    frame_size: int = 1024,
    hop_size: int = 512,
    tokeniser: str = "fft",
    n_clusters: int = 128,
) -> Dict[str, float]:
    """Full pipeline: generate signal → frame → tokenise → WaveEngine."""
    wave_engine = WaveEngine()

    # 1. Generate / load audio
    start = time.perf_counter()
    signal, sr = generate_synthetic_signal(kind, duration)
    gen_time = time.perf_counter() - start

    # 2. Frame / Tokenise
    start = time.perf_counter()

    if tokeniser == "fft":
        frames = frame_signal(signal, frame_size, hop_size)
        tokens = tokenise_fft(frames, sr)
    elif tokeniser == "mfcc":
        tokens = tokenise_mfcc(signal, sr, frame_size, hop_size, n_clusters=n_clusters)
        frames = None  # not used for stats in this mode
    else:
        raise ValueError(f"Unknown tokeniser '{tokeniser}'. Choose 'fft' or 'mfcc'.")

    tok_time = time.perf_counter() - start

    # 4. WaveEngine processing
    start = time.perf_counter()
    activations = wave_engine.process(tokens)
    wave_time = time.perf_counter() - start

    # 5. Simple summary statistics
    unique_tokens = len(set(tokens))
    stats = {
        "signal_kind": kind,
        "duration_s": duration,
        "sample_rate": sr,
        "num_frames": len(tokens) if frames is None else len(frames),
        "unique_tokens": unique_tokens,
        "gen_time_s": round(gen_time, 6),
        "tokenisation_time_s": round(tok_time, 6),
        "wave_processing_time_s": round(wave_time, 6),
        "avg_wave_value_abs": float(np.mean(np.abs(list(activations.values())))),
        "tokeniser": tokeniser,
        "n_clusters": n_clusters if tokeniser == "mfcc" else None,
    }
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acoustic → Symbolic WaveEngine simulation")
    parser.add_argument("--kind", choices=["bird", "whale", "wow", "noise"], default="bird", help="Signal type to simulate")
    parser.add_argument("--duration", type=float, default=5.0, help="Duration of the synthetic signal in seconds")
    parser.add_argument("--frame-size", type=int, default=1024, help="Frame size for FFT / STFT")
    parser.add_argument("--hop-size", type=int, default=512, help="Hop size between frames")
    parser.add_argument("--tokeniser", choices=["fft", "mfcc"], default="fft", help="Tokenisation method")
    parser.add_argument("--clusters", type=int, default=128, help="Number of KMeans clusters if tokeniser=mfcc")
    args = parser.parse_args()

    summary = run_pipeline(
        args.kind,
        args.duration,
        frame_size=args.frame_size,
        hop_size=args.hop_size,
        tokeniser=args.tokeniser,
        n_clusters=args.clusters,
    )

    print("\n=== Simulation Summary ===")
    for k, v in summary.items():
        print(f"{k:25}: {v}")
    print("==========================\n") 