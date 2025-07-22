import argparse
import json
from pathlib import Path
from typing import Tuple, List

import numpy as np

DEFAULT_SR = 25  # Hz


def _central_flow_segment(duration_s: float, sr: int) -> np.ndarray:
    """Generate near-zero flow representing central apnea."""
    n = int(duration_s * sr)
    return 0.02 * np.random.randn(n)


def _obstructive_flow_segment(duration_s: float, sr: int, freq_hz: float = 1.0) -> np.ndarray:
    """Generate oscillatory flow with snore-like component representing obstructive apnea."""
    t = np.linspace(0, duration_s, int(duration_s * sr), endpoint=False)
    # 1 Hz breathing oscillation with snore harmonics (30 Hz bursty noise)
    base = 0.5 * np.sin(2 * np.pi * freq_hz * t)
    snore = 0.1 * np.sin(2 * np.pi * 30 * t) * (np.random.rand(len(t)) > 0.9)
    noise = 0.05 * np.random.randn(len(t))
    return base + snore + noise


def generate_trace(total_duration_s: int = 300, sr: int = DEFAULT_SR,
                   obstructive_len: float = 20.0, central_len: float = 20.0) -> Tuple[np.ndarray, List[str]]:
    """Generate alternating obstructive / central apnea flow trace.

    Returns
    -------
    flow : np.ndarray
        1-D array of length total_duration_s * sr.
    labels : list[str]
        Per-sample ground-truth labels ("obstructive" | "central").
    """
    segments = []
    labels = []
    time_left = total_duration_s
    toggle = True  # True => obstructive first
    while time_left > 0:
        seg_len = obstructive_len if toggle else central_len
        seg_len = min(seg_len, time_left)
        if toggle:
            seg = _obstructive_flow_segment(seg_len, sr)
            label = "obstructive"
        else:
            seg = _central_flow_segment(seg_len, sr)
            label = "central"
        segments.append(seg)
        labels.extend([label] * len(seg))
        time_left -= seg_len
        toggle = not toggle

    flow = np.concatenate(segments)
    return flow, labels


def save_trace(flow: np.ndarray, labels: List[str], out_prefix: Path):
    """Save flow to .npy and labels to .json/.csv for easy loading."""
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    np.save(out_prefix.with_suffix(".npy"), flow)
    # Store labels as json with run-length encoding to keep size small
    rle = []
    current = labels[0]
    count = 0
    for lbl in labels:
        if lbl == current:
            count += 1
        else:
            rle.append({"label": current, "count": count})
            current = lbl
            count = 1
    rle.append({"label": current, "count": count})
    label_path = out_prefix.parent / f"{out_prefix.stem}_labels.json"
    with open(label_path, "w") as fh:
        json.dump({"sr": DEFAULT_SR, "rle": rle}, fh, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic apnea flow trace.")
    parser.add_argument("--duration", type=int, default=300, help="Total duration in seconds (default: 300)")
    parser.add_argument("--sr", type=int, default=DEFAULT_SR, help="Sample rate in Hz (default: 25)")
    parser.add_argument("--out", type=str, default="data/synthetic_apnea", help="Output prefix path (no extension)")
    args = parser.parse_args()

    flow_arr, lbls = generate_trace(args.duration, args.sr)
    save_trace(flow_arr, lbls, Path(args.out))
    print(f"Saved flow .npy and label json to prefix {args.out}") 