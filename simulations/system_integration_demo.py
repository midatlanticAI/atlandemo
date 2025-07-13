"""system_integration_demo.py
Run a few real workloads (acoustic sims + LogicBench) and feed their
symbolic summaries into the TemporalCognitionEngine.  Observe which
schemas are consolidated.

Usage (from project root):

    py simulations\system_integration_demo.py --reset --backend json

Options
-------
--reset      Delete the schema store before running.
--backend    json | sqlite (default json)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import json

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cog_config import CogConfig
from src.temporal_cognition import TemporalCognitionEngine
from src.temporal_cognition import ExperienceFrame  # for type hints

# Import heavy workloads lazily
import simulations.continuous_acoustic_simulation as cas

# Provide a lightweight analyse_file wrapper if the module lacks one
if not hasattr(cas, "analyse_file"):
    import librosa  # type: ignore

    def _analyse_file(path: str, **kwargs):
        signal, sr_in = librosa.load(path, sr=None, mono=True)
        return cas.run_pipeline(
            kind="file",
            duration=len(signal) / sr_in,
            frame_size=kwargs.get("frame_size", 2048),
            hop_size=kwargs.get("hop_size", 1024),
            top_k=kwargs.get("top_k", 6),
            detect_sweeps=True,
            detect_down_sweeps=True,
            detect_pulses=True,
        )

    cas.analyse_file = _analyse_file  # type: ignore[attr-defined]

from wave_logicbench_full_benchmark import WaveLogicBenchBenchmark


def feed_acoustic(engine: TemporalCognitionEngine, wav_path: str):
    summary = cas.analyse_file(
        wav_path,
        frame_size=2048,
        hop_size=1024,
        top_k=6,
        detect_sweeps=True,
        detect_down_sweeps=True,
        detect_pulses=True,
    )

    auditory = []
    if summary["upward_sweeps"]:
        auditory.append("up_sweep")
    if summary["downward_sweeps"]:
        auditory.append("down_sweep")
    if summary["pulses"]:
        auditory.append("pulse")

    engine.live_experience(
        visual=[Path(wav_path).stem],
        auditory=auditory,
        goals=["audio_analysis"],
        context=[f"k{summary['top_k']}"]
    )


def feed_logicbench(engine: TemporalCognitionEngine, max_q: int = 300):
    bench = WaveLogicBenchBenchmark()
    bench.run()
    acc = bench.results.get("accuracy", 0.0)

    # Single summary frame (could be more granular)
    engine.live_experience(
        visual=["logicbench"],
        auditory=[f"accuracy_{int(acc*100)}"],
        goals=["benchmark"],
        context=["eval"],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--backend", choices=["json", "sqlite"], default="json")
    args = parser.parse_args()

    store_path = "schemas_system.db" if args.backend == "sqlite" else "schemas_system.json"
    if args.reset and Path(store_path).exists():
        Path(store_path).unlink()

    cfg = CogConfig(store_backend=args.backend, store_path=store_path)
    engine = TemporalCognitionEngine(cfg)

    # --- Acoustic workloads ---
    feed_acoustic(engine, "samples/humpback4.wav")
    feed_acoustic(engine, "samples/BlueJay.wav")

    # --- LogicBench workload summary ---
    feed_logicbench(engine)

    # Persist schemas
    engine.experience_stream.store.save(engine.experience_stream.schemas)

    print("\n=== Top Schemas After Workload ===")
    for item in engine.experience_stream.get_schema_summary(min_count=1, top_k=15):
        print(item)


if __name__ == "__main__":
    main()