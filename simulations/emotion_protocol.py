"""emotion_protocol.py

Empirical falsification protocol for testing whether the Wave-Engine encodes
emotional valence and arousal in its resonance patterns.

The script runs three experiments (E1–E3 from documentation):
    E1 – Direct mapping accuracy between injected mood/arousal and decoded values.
    E2 – Phase-cancellation test using opposite-sign mood inputs.
    E3 – Temporal priming drift on a neutral stimulus.

Results are printed to stdout and stored to JSON (emotion_protocol_results.json).
"""

from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

# Ensure project root on sys.path
import sys, os, pathlib as _pl
_PROJECT_ROOT = _pl.Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.temporal_cognition import TemporalCognitionEngine

# -----------------------------------------------------------------------------
# Emotion prototypes (valence = mood, arousal)
# -----------------------------------------------------------------------------

EMOTIONS: Dict[str, Dict[str, object]] = {
    "joy":      {"mood": 0.8,  "arousal": 0.7, "symbols": ["joy", "delight", "laughter"]},
    "sadness":  {"mood": -0.8, "arousal": 0.3, "symbols": ["sorrow", "grief", "tears"]},
    "anger":    {"mood": -0.6, "arousal": 0.8, "symbols": ["rage", "anger", "irritation"]},
    "calm":     {"mood": 0.4,  "arousal": 0.2, "symbols": ["calm", "relaxation", "peace"]},
    "fear":     {"mood": -0.9, "arousal": 0.9, "symbols": ["fear", "panic", "danger"]},
}

NOISE_WORDS = [
    "object", "value", "system", "state", "symbol", "node", "input", "output", "data",
    "wave", "phase", "frequency", "logic", "memory",
]

# -----------------------------------------------------------------------------
# Utility: decoder from activation field → (valence_hat, arousal_hat)
# -----------------------------------------------------------------------------

def decode_emotion(activation_field: Dict[str, float]) -> Tuple[float, float]:
    if not activation_field:
        return 0.0, 0.0
    positives = [v for v in activation_field.values() if v > 0]
    negatives = [-v for v in activation_field.values() if v < 0]
    pos_sum = float(sum(positives))
    neg_sum = float(sum(negatives))
    total = pos_sum + neg_sum + 1e-9
    valence_hat = (pos_sum - neg_sum) / total  # range roughly [-1,1]
    arousal_hat = total / (len(activation_field) + 1e-9)  # crude intensity measure
    return valence_hat, arousal_hat


# -----------------------------------------------------------------------------
# Experiment helpers
# -----------------------------------------------------------------------------

RNG = random.Random(123)

def random_noise(n: int = 3) -> List[str]:
    return RNG.sample(NOISE_WORDS, n)


def inject_frame(engine: TemporalCognitionEngine, visual_syms: List[str], *, mood: float, arousal: float):
    """Convenience wrapper around engine.live_experience (wave-only)."""
    result = engine.live_experience(
        visual=visual_syms,
        auditory=[],
        kinesthetic=[],
        mood=mood,
        arousal=arousal,
        attention=0.7,
        goals=[],
        context=[],
        surprise=0.0,
        satisfaction=0.0,
    )
    return result["activation_field"]  # Dict[str,float]


# -----------------------------------------------------------------------------
# Experiments
# -----------------------------------------------------------------------------

RESULTS: Dict[str, object] = {}

# E1 – direct mapping
SAMPLES_PER_EMOTION = 100
val_true: List[float] = []
val_pred: List[float] = []  # instantaneous
val_int: List[float] = []   # integrated
aro_true: List[float] = []
aro_pred: List[float] = []  # instantaneous
aro_int: List[float] = []

engine = TemporalCognitionEngine()

for label, proto in EMOTIONS.items():
    mood = float(proto["mood"])  # type: ignore
    arousal = float(proto["arousal"])  # type: ignore
    base_symbols = list(proto["symbols"])  # type: ignore

    for _ in range(SAMPLES_PER_EMOTION):
        visual = base_symbols + random_noise()
        res = engine.live_experience(visual=visual, auditory=[], kinesthetic=[], mood=mood, arousal=arousal,
                                     attention=0.7, goals=[], context=[], surprise=0.0, satisfaction=0.0)
        act_field = res["activation_field"]
        v_i = res["valence_integrated"]
        a_i = res["arousal_integrated"]
        v_hat, a_hat = decode_emotion(act_field)
        val_true.append(mood)
        val_pred.append(v_hat)
        val_int.append(v_i)
        aro_true.append(arousal)
        aro_pred.append(a_hat)
        aro_int.append(a_i)

# Correlations
val_r = float(np.corrcoef(val_true, val_pred)[0, 1]) if len(val_true) > 1 else 0.0
aro_r = float(np.corrcoef(aro_true, aro_pred)[0, 1]) if len(aro_true) > 1 else 0.0

val_int_r = float(np.corrcoef(val_true, val_int)[0,1])
aro_int_r = float(np.corrcoef(aro_true, aro_int)[0,1])

RESULTS["E1"] = {
    "samples": len(val_true),
    "pearson_valence_instant": val_r,
    "pearson_arousal_instant": aro_r,
    "pearson_valence_integrated": val_int_r,
    "pearson_arousal_integrated": aro_int_r,
}

# E2 – phase-cancellation
CANCELLATION_PAIRS = 100
abs_val_after: List[float] = []

engine_phase = TemporalCognitionEngine()

symbols_pair = ["paradox"]  # arbitrary
for _ in range(CANCELLATION_PAIRS):
    # positive frame
    inject_frame(engine_phase, symbols_pair, mood=+0.8, arousal=0.5)
    # negative frame (opposite mood)
    act_field = inject_frame(engine_phase, symbols_pair, mood=-0.8, arousal=0.5)
    v_hat, _ = decode_emotion(act_field)
    abs_val_after.append(abs(v_hat))

mean_abs_val = float(np.mean(abs_val_after))
RESULTS["E2"] = {
    "pairs": CANCELLATION_PAIRS,
    "mean_abs_valence_after_cancel": mean_abs_val,
}

# E3 – temporal priming drift
PRIMING_STEPS = 20
blue_vals: List[float] = []
blue_moods: List[float] = []
engine_drift = TemporalCognitionEngine()

for step in range(PRIMING_STEPS):
    mood = 0.8 if step % 2 == 0 else -0.8
    blue_moods.append(mood)
    act = inject_frame(engine_drift, ["blue_light"], mood=mood, arousal=0.5)
    blue_vals.append(act.get("blue_light", 0.0))

drift_corr = float(np.corrcoef(blue_moods, blue_vals)[0, 1]) if PRIMING_STEPS > 2 else 0.0
RESULTS["E3"] = {
    "steps": PRIMING_STEPS,
    "pearson_mood_vs_activation": drift_corr,
}

# E4 – Integration advantage
inst_corr = val_r
int_corr = val_int_r
integration_gain = int_corr - inst_corr
RESULTS["E4"] = {
    "pearson_valence_instant": inst_corr,
    "pearson_valence_integrated": int_corr,
    "gain": integration_gain,
}

# -----------------------------------------------------------------------------
# Persist and print
# -----------------------------------------------------------------------------

json_path = Path("emotion_protocol_results.json")
json_path.write_text(json.dumps(RESULTS, indent=2))

print("\n=== Emotion-Falsification Results ===")
for k, v in RESULTS.items():
    print(f"[{k}] -> {v}")
print(f"Results written to {json_path.resolve()}") 