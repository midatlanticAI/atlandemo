import os
import sys
import time
import argparse
from typing import List, Dict, Tuple

import numpy as np
# Optional visualization
try:
    import matplotlib.pyplot as plt  # noqa: F401
except ModuleNotFoundError:
    plt = None

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --- Synthetic signal generation (same as in acoustic_simulation.py) ---------------------------

def generate_synthetic_signal(kind: str, duration: float = 5.0, sr: int = 22_050) -> Tuple[np.ndarray, int]:
    """Generate a synthetic audio waveform for experimentation."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    if kind == "bird":
        base = 4_000  # 4 kHz
        chirp = np.sin(2 * np.pi * base * t)
        envelope = 0.5 * (1 + np.sin(2 * np.pi * 3 * t))
        signal = envelope * chirp
    elif kind == "whale":
        base = 150  # 150 Hz
        moan = np.sin(2 * np.pi * base * t)
        envelope = 0.5 * (1 + np.sin(2 * np.pi * 0.3 * t))
        signal = 0.8 * envelope * moan
    elif kind == "wow":
        freq = 1_420  # Hz narrow-band burst
        signal = np.zeros_like(t)
        burst_mask = (t > 1.0) & (t < 1.2)
        signal[burst_mask] = 0.7 * np.sin(2 * np.pi * freq * t[burst_mask])
    else:  # noise
        signal = 0.05 * np.random.randn(len(t))
    return signal.astype(np.float32), sr


# --- Frame & spectral component extraction ----------------------------------------------------

def frame_signal(signal: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    """Convert 1-D signal to 2-D array of overlapping frames."""
    num_frames = 1 + (len(signal) - frame_size) // hop_size
    indices = np.arange(num_frames)[:, None] * hop_size + np.arange(frame_size)
    return signal[indices]


def extract_components(frames: np.ndarray, sr: int, top_k: int) -> List[Dict[str, float]]:
    """Extract top-k spectral components per frame.

    Returns a list of dicts: {freq, amp, phase}.
    """
    window = np.hanning(frames.shape[1])
    fft = np.fft.rfft(frames * window, axis=1)
    mags = np.abs(fft)
    phases = np.angle(fft)

    components: List[Dict[str, float]] = []
    bin_to_freq = sr / frames.shape[1]

    for frame_idx in range(frames.shape[0]):
        # Indices of top-k magnitudes (excluding DC)
        top_indices = np.argsort(mags[frame_idx])[::-1][1 : top_k + 1]
        for idx in top_indices:
            components.append(
                {
                    "frame": frame_idx,
                    "freq": idx * bin_to_freq,
                    "amp": mags[frame_idx, idx] / frames.shape[1],
                    "phase": phases[frame_idx, idx],
                }
            )
    return components


# --- Direct wave computation ------------------------------------------------------------------

def compute_wave_values(components: List[Dict[str, float]], base_time: float) -> List[float]:
    """Compute instantaneous wave values for each component at current time."""
    t = time.time() - base_time
    values = [c["amp"] * np.sin(2 * np.pi * c["freq"] * t + c["phase"]) for c in components]
    return values


# --- Pipeline ---------------------------------------------------------------------------------

def run_pipeline(
    kind: str,
    duration: float = 5.0,
    frame_size: int = 1024,
    hop_size: int = 512,
    top_k: int = 3,
    detect_sweeps: bool = False,
    detect_down_sweeps: bool = False,
    detect_pulses: bool = False,
) -> Dict[str, float]:
    start_global = time.perf_counter()

    # 1. Generate signal
    signal, sr = generate_synthetic_signal(kind, duration)

    # 2. Frame signal
    frames = frame_signal(signal, frame_size, hop_size)

    # 3. Extract components
    comp_start = time.perf_counter()
    components = extract_components(frames, sr, top_k)
    comp_time = time.perf_counter() - comp_start

    # Optional sweep detection
    sweep_count = None
    down_sweep_count = None
    pulse_count = None
    if detect_sweeps or detect_down_sweeps or detect_pulses:
        dominant = {}
        for c in components:
            f = c["frame"]
            # keep highest amp per frame
            if f not in dominant or c["amp"] > dominant[f]["amp"]:
                dominant[f] = {"freq": c["freq"], "amp": c["amp"]}

        # sort frames
        frames_sorted = sorted(dominant.items())
        freqs_seq = [item[1]["freq"] for item in frames_sorted]
        delta = 20.0  # Hz threshold for sweep step
        sweep_count = 0
        down_sweep_count = 0
        pulse_count = 0
        i = 0
        while i < len(freqs_seq) - 2:
            up_condition = freqs_seq[i+1] > freqs_seq[i] + delta and freqs_seq[i+2] > freqs_seq[i+1] + delta
            down_condition = freqs_seq[i+1] < freqs_seq[i] - delta and freqs_seq[i+2] < freqs_seq[i+1] - delta

            if detect_sweeps and up_condition:
                sweep_count += 1
                i += 3
                continue
            if detect_down_sweeps and down_condition:
                down_sweep_count += 1
                i += 3
                continue

            # Pulse detection: same freq within tolerance (< delta) for at least 2 consecutive frames
            if detect_pulses and abs(freqs_seq[i+1] - freqs_seq[i]) < delta and abs(freqs_seq[i+2] - freqs_seq[i+1]) < delta:
                pulse_count += 1
                i += 3
            else:
                i += 1

    # 4. Compute wave values once (snapshot)
    base_time = time.time()
    wave_values = compute_wave_values(components, base_time)

    # 5. Aggregate stats
    freqs = [c["freq"] for c in components]
    stats = {
        "signal_kind": kind,
        "duration_s": duration,
        "sample_rate": sr,
        "frames": frames.shape[0],
        "components": len(components),
        "unique_freqs": len(np.unique(np.round(freqs, 1))),
        "component_extraction_s": round(comp_time, 6),
        "avg_wave_value_abs": float(np.mean(np.abs(wave_values))),
        "frame_size": frame_size,
        "hop_size": hop_size,
        "top_k": top_k,
        "upward_sweeps": sweep_count,
        "downward_sweeps": down_sweep_count,
        "pulses": pulse_count,
    }
    stats["total_runtime_s"] = round(time.perf_counter() - start_global, 6)
    # For visualization, return frames and sr so caller can plot if needed
    stats["_frames_array"] = frames  # type: ignore
    stats["_sr"] = sr              # type: ignore
    return stats


# --- CLI --------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Continuous spectral component simulation")
    parser.add_argument("--kind", choices=["bird", "whale", "wow", "noise"], default="bird", help="Synthetic signal type (ignored if --file provided)")
    parser.add_argument("--file", type=str, default=None, help="Path to real audio file (wav/flac). Overrides --kind and --duration")
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--frame-size", type=int, default=1024)
    parser.add_argument("--hop-size", type=int, default=512)
    parser.add_argument("--top-k", type=int, default=3, help="Number of strongest peaks per frame to keep")
    parser.add_argument("--detect-sweeps", action="store_true", help="Detect simple upward frequency sweeps")
    parser.add_argument("--detect-down-sweeps", action="store_true", help="Detect downward frequency sweeps")
    parser.add_argument("--detect-pulses", action="store_true", help="Detect repeated pulses at same frequency")
    parser.add_argument("--visualize", action="store_true", help="Show spectrogram heatmap of the run")
    parser.add_argument("--json-out", type=str, default=None, help="Write summary to JSON file")
    args = parser.parse_args()

    if args.file:
        # Load real audio
        try:
            import librosa  # type: ignore
        except ModuleNotFoundError:
            print("librosa required to load audio files. Please install it.")
            sys.exit(1)

        signal, sr_in = librosa.load(args.file, sr=None, mono=True)
        target_sr = 22_050
        if sr_in != target_sr:
            signal = librosa.resample(signal, orig_sr=sr_in, target_sr=target_sr)
            sr_in = target_sr

        # Monkey-patch: call run_pipeline with custom signal
        def pipeline_from_signal(sig: np.ndarray, sr: int):
            frame_size = args.frame_size
            hop_size = args.hop_size
            frames = frame_signal(sig, frame_size, hop_size)
            components = extract_components(frames, sr, args.top_k)

            # sweep detection
            sweep_count = None
            down_sweep_count = None
            pulse_count = None
            if args.detect_sweeps or args.detect_down_sweeps or args.detect_pulses:
                dominant = {}
                for c in components:
                    f = c["frame"]
                    if f not in dominant or c["amp"] > dominant[f]["amp"]:
                        dominant[f] = {"freq": c["freq"], "amp": c["amp"]}
                seq = [item[1]["freq"] for item in sorted(dominant.items())]
                delta = 20.0
                sweep_count = 0
                down_sweep_count = 0
                pulse_count = 0
                i = 0
                while i < len(seq) - 2:
                    up_condition = seq[i+1] > seq[i] + delta and seq[i+2] > seq[i+1] + delta
                    down_condition = seq[i+1] < seq[i] - delta and seq[i+2] < seq[i+1] - delta

                    if args.detect_sweeps and up_condition:
                        sweep_count += 1
                        i += 3
                        continue
                    if args.detect_down_sweeps and down_condition:
                        down_sweep_count += 1
                        i += 3
                        continue

                    # Pulse detection: same freq within tolerance (< delta) for at least 2 consecutive frames
                    if args.detect_pulses and abs(seq[i+1] - seq[i]) < delta and abs(seq[i+2] - seq[i+1]) < delta:
                        pulse_count += 1
                        i += 3
                    else:
                        i += 1

            wave_vals = compute_wave_values(components, time.time())
            freqs = [c["freq"] for c in components]
            # Median dominant frequency for file mode
            dominant = {}
            for c in components:
                f_idx = int(c["frame"])
                if f_idx not in dominant or c["amp"] > dominant[f_idx][1]:
                    dominant[f_idx] = (c["freq"], c["amp"])
            median_dom = float(np.median([v[0] for v in dominant.values()])) if dominant else 0.0
            return {
                "signal_kind": f"file:{os.path.basename(args.file)}",
                "duration_s": round(len(sig) / sr, 3),
                "sample_rate": sr,
                "frames": frames.shape[0],
                "components": len(components),
                "unique_freqs": len(np.unique(np.round(freqs, 1))),
                "avg_wave_value_abs": float(np.mean(np.abs(wave_vals))),
                "frame_size": frame_size,
                "hop_size": hop_size,
                "top_k": args.top_k,
                "upward_sweeps": sweep_count,
                "downward_sweeps": down_sweep_count,
                "pulses": pulse_count,
                "median_dom_freq": median_dom,
            }

        summary = pipeline_from_signal(signal, sr_in)
    else:
        summary = run_pipeline(
            kind=args.kind,
            duration=args.duration,
            frame_size=args.frame_size,
            hop_size=args.hop_size,
            top_k=args.top_k,
            detect_sweeps=args.detect_sweeps,
            detect_down_sweeps=args.detect_down_sweeps,
            detect_pulses=args.detect_pulses,
        )

    print("\n=== Continuous Simulation Summary ===")
    for k, v in summary.items():
        print(f"{k:25}: {v}")
    print("=====================================\n")

    if args.json_out:
        import json, pathlib
        pathlib.Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        # Remove large arrays before saving
        summary_clean = {k: v for k, v in summary.items() if not k.startswith("_")}
        with open(args.json_out, "w", encoding="utf-8") as fp:
            json.dump(summary_clean, fp, indent=2)
        print(f"Summary written to {args.json_out}")

    if args.visualize:
        if plt is None:
            print("Matplotlib not installed. Please install it to use --visualize")
        else:
            frames = summary.pop("_frames_array")
            sr = summary.pop("_sr")
            window = np.hanning(frames.shape[1])
            mags = np.abs(np.fft.rfft(frames * window, axis=1))
            mags_db = 20 * np.log10(mags + 1e-6)
            freqs = np.linspace(0, sr / 2, mags.shape[1])
            times = np.arange(frames.shape[0]) * (args.hop_size / sr)

            plt.figure(figsize=(10, 4))
            plt.imshow(
                mags_db.T,
                origin="lower",
                aspect="auto",
                extent=[times[0], times[-1], freqs[0], freqs[-1]],
                cmap="magma",
            )
            plt.colorbar(label="Magnitude (dB)")
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            plt.title(f"Spectrogram ({args.kind})")
            plt.tight_layout()
            plt.show() 