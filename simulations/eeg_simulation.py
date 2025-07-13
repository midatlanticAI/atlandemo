import numpy as np
import time
import argparse
from typing import Dict

import os, sys, pathlib
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from expert_modules.brain_experts import RhythmPowerExpert, MuDropExpert


def generate_synthetic_eeg(duration: float = 12.0, sr: int = 256) -> np.ndarray:
    """Generate 1-channel synthetic EEG with an alpha drop (motor imagery) event."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    alpha_base = 50e-6  # 50 µV baseline alpha amplitude
    signal = alpha_base * np.sin(2 * np.pi * 10 * t)

    # Add beta component throughout
    signal += 20e-6 * np.sin(2 * np.pi * 20 * t)

    # Motor imagery event between 5–7 s: suppress alpha by 60 %
    mask = (t > 5) & (t < 7)
    signal[mask] *= 0.4

    # small noise
    signal += 5e-6 * np.random.randn(len(t))
    return signal.astype(np.float32)


def frame_signal(sig: np.ndarray, frame_size: int, hop: int) -> np.ndarray:
    n_frames = 1 + (len(sig) - frame_size) // hop
    idx = np.arange(n_frames)[:, None] * hop + np.arange(frame_size)
    return sig[idx]


def run_eeg_pipeline(duration: float = 12.0):
    sr = 256
    signal = generate_synthetic_eeg(duration, sr)
    frame_size = 256  # 1-s window
    hop = 64  # 250 ms step
    frames = frame_signal(signal, frame_size, hop)

    # Rhythm power
    rhythm_expert = RhythmPowerExpert("rhythm", "eeg")
    rhythm_resp = rhythm_expert.process_query("eeg_rhythm_power", {"frames": frames, "sr": sr})

    # Build alpha series for mu-drop expert (mean alpha power per frame)
    fft = np.fft.rfft(frames * np.hanning(frame_size), axis=1)
    psd = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(frame_size, 1 / sr)
    alpha_idx = np.logical_and(freqs >= 8, freqs <= 12)
    alpha_series = list(np.mean(psd[:, alpha_idx], axis=1))

    mu_expert = MuDropExpert("mu", "eeg")
    mu_resp = mu_expert.process_query("detect_mu_drop", {"alpha_series": alpha_series})

    summary: Dict[str, float] = {
        "frames": frames.shape[0],
        "alpha_power": rhythm_resp.answer["alpha"],
        "beta_power": rhythm_resp.answer["beta"],
        "theta_power": rhythm_resp.answer["theta"],
        "mu_drop_events": len(mu_resp.answer),
    }
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=12.0)
    args = parser.parse_args()

    summ = run_eeg_pipeline(args.duration)
    print("\n=== Synthetic EEG Simulation ===")
    for k, v in summ.items():
        print(f"{k:20}: {v}") 