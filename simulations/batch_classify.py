import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulations.continuous_acoustic_simulation import run_pipeline  # type: ignore


def classify(summary: Dict[str, float]) -> str:
    """Very simple heuristic classifier for Cardinal, Blue Jay, Humpback."""
    up = summary.get("upward_sweeps", 0) or 0
    down = summary.get("downward_sweeps", 0) or 0
    pulses = summary.get("pulses", 0) or 0
    median_f = summary.get("median_dom_freq", 0) or 0

    if median_f < 1000:
        return "Humpback"
    if up > down:
        return "Cardinal"
    if down >= up:
        return "BlueJay"
    return "Unknown"


def process_file(path: Path, args) -> Dict[str, float]:
    summary = run_pipeline(
        kind="bird",  # ignored
        duration=5.0,
        frame_size=args.frame_size,
        hop_size=args.hop_size,
        top_k=args.top_k,
        detect_sweeps=True,
        detect_down_sweeps=True,
        detect_pulses=True,
        # The run_pipeline inside simulation expects synthetic generation unless we bypass; we'll call custom pipeline inside file mode below.
    )
    # Note: easier is to shell out to script with json-out, but importing run_pipeline won't load file.
    return summary


def shell_call(file_path: Path, args) -> Dict[str, float]:
    from subprocess import run, PIPE
    json_out = Path("temp_summary.json")
    cmd = [
        "py", "-3", "simulations/continuous_acoustic_simulation.py",
        "--file", str(file_path),
        "--frame-size", str(args.frame_size),
        "--hop-size", str(args.hop_size),
        "--top-k", str(args.top_k),
        "--detect-sweeps", "--detect-down-sweeps", "--detect-pulses",
        "--json-out", str(json_out)
    ]
    run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    with open(json_out, "r", encoding="utf-8") as fp:
        summary = json.load(fp)
    json_out.unlink(missing_ok=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Batch classify WAV clips with wave-engine symbolic cues")
    parser.add_argument("directory", help="Directory containing WAV clips")
    parser.add_argument("--frame-size", type=int, default=1024)
    parser.add_argument("--hop-size", type=int, default=512)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    clips = list(Path(args.directory).glob("*.wav"))
    if not clips:
        print("No WAV files found in", args.directory)
        return

    print("file,up_sweeps,down_sweeps,pulses,predicted")
    for clip in clips:
        summary = shell_call(clip, args)
        label = classify(summary)
        print(f"{clip.name},{summary.get('upward_sweeps')},{summary.get('downward_sweeps')},{summary.get('pulses')},{label}")


if __name__ == "__main__":
    main() 