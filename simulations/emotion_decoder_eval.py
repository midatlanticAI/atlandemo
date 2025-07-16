"""emotion_decoder_eval.py

Train a simple linear regression decoder on Wave-Engine activation features to
predict injected valence (mood) and arousal.  Eighty percent of synthetic data
are used for training, 20 % for testing.  R² scores are reported.

Features per sample
-------------------
1. v_marker  = activation['valence_positive'] − activation['valence_negative']
2. balance   = Σ positive − Σ negative activations
3. intensity = mean absolute activation over symbols

No external ML packages required; closed-form linear regression via numpy.
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

import sys, pathlib as _pl
_PROJECT_ROOT = _pl.Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.temporal_cognition import TemporalCognitionEngine

EMOTIONS = {
    "joy":      {"mood": 0.8,  "arousal": 0.7, "symbols": ["joy", "delight", "laughter"]},
    "sadness":  {"mood": -0.8, "arousal": 0.3, "symbols": ["sorrow", "grief", "tears"]},
    "anger":    {"mood": -0.6, "arousal": 0.8, "symbols": ["rage", "anger", "irritation"]},
    "calm":     {"mood": 0.4,  "arousal": 0.2, "symbols": ["calm", "relaxation", "peace"]},
    "fear":     {"mood": -0.9, "arousal": 0.9, "symbols": ["fear", "panic", "danger"]},
}

NOISE = [
    "object", "value", "system", "state", "symbol", "node", "input", "output", "data",
    "wave", "phase", "frequency", "logic", "memory",
]
_rng = random.Random(123)


def inject(engine: TemporalCognitionEngine, symbols: List[str], mood: float, arousal: float) -> Dict[str, float]:
    res = engine.live_experience(visual=symbols, auditory=[], kinesthetic=[], mood=mood,
                                 arousal=arousal, attention=0.7, goals=[], context=[], surprise=0.0, satisfaction=0.0)
    return res["activation_field"]


def features(act: Dict[str, float]) -> Tuple[float, float, float]:
    pos = [v for v in act.values() if v > 0]
    neg = [v for v in act.values() if v < 0]
    balance = sum(pos) - sum(abs(v) for v in neg)
    intensity = (sum(abs(v) for v in act.values()) / len(act)) if act else 0.0
    v_marker = act.get("valence_positive", 0.0) - act.get("valence_negative", 0.0)
    return v_marker, balance, intensity


def linreg_train(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    # Add bias term
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    w = np.linalg.pinv(Xb.T @ Xb) @ Xb.T @ y
    return w


def linreg_predict(X: np.ndarray, w: np.ndarray) -> np.ndarray:
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    return Xb @ w


def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def main():
    engine = TemporalCognitionEngine()
    samples: List[Tuple[Dict[str, float], float, float]] = []  # activation dict, valence, arousal
    SAMPLES = 100

    for proto in EMOTIONS.values():
        mood = proto["mood"]
        arousal = proto["arousal"]
        base = proto["symbols"]
        for _ in range(SAMPLES):
            syms = base + _rng.sample(NOISE, 3)
            act = inject(engine, syms, mood, arousal)
            samples.append((act, mood, arousal))

    # Build symbol vocabulary
    X = np.zeros((len(samples), 4), dtype=np.float64)  # [|val_marker|, |aro_marker|, val_mag, aro_mag]
    y_val = np.zeros(len(samples), dtype=np.float64)
    y_ar = np.zeros(len(samples), dtype=np.float64)

    for i, (act, val, ar) in enumerate(samples):
        X[i, 0] = abs(act.get("valence_marker", 0.0))
        X[i, 1] = abs(act.get("arousal_marker", 0.0))
        X[i, 2] = act.get("valence_mag", 0.0)
        X[i, 3] = act.get("arousal_mag", 0.0)
        y_val[i] = val
        y_ar[i] = ar

    vocab = ["|valence_marker|", "|arousal_marker|", "val_mag", "arousal_mag"]

    # shuffle consistently
    perm = np.arange(len(samples))
    _rng.shuffle(perm.tolist())
    X = X[perm]
    y_val = y_val[perm]
    y_ar = y_ar[perm]

    split = int(0.8 * len(samples))
    X_train, X_test = X[:split], X[split:]
    yv_train, yv_test = y_val[:split], y_val[split:]
    ya_train, ya_test = y_ar[:split], y_ar[split:]

    # standardise features column-wise (mean 0, std 1) to improve conditioning
    mu = X_train.mean(axis=0)
    sigma = X_train.std(axis=0) + 1e-6
    X_train_std = (X_train - mu) / sigma
    X_test_std = (X_test - mu) / sigma

    w_val = linreg_train(X_train_std, yv_train)
    w_ar = linreg_train(X_train_std, ya_train)

    val_pred = linreg_predict(X_test_std, w_val)
    ar_pred = linreg_predict(X_test_std, w_ar)

    r2_val = r2(yv_test, val_pred)
    r2_ar = r2(ya_test, ar_pred)

    print("\n=== Linear decoder evaluation ===")
    print(f"R² valence : {r2_val:.3f}")
    print(f"R² arousal : {r2_ar:.3f}")
    print(f"Features: {len(vocab)} symbols")


if __name__ == "__main__":
    main() 