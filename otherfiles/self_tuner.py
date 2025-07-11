"""WaveSelfTuner
================
A light-weight mix-in that lets any module with per-concept wave parameters
(phase φ, amplitude A, frequency f) self-adjust based on a scalar reward.

Intended use:
    class SomeExpert(BaseExpertModule, WaveSelfTuner):
        def __init__(...):
            BaseExpertModule.__init__(...)
            WaveSelfTuner.__init__(self, concepts=self.wave_frequencies.keys())

Inside the main loop:
    reward = compute_reward()
    expert.update_params(reward)

All updates are cheap and bounded—suitable for microcontrollers.
"""
from __future__ import annotations

import math
import random
import time
from typing import Dict, Iterable


class WaveSelfTuner:
    """Mix-in that provides self-tuning of φ, A, f for each concept."""

    def __init__(self, concepts: Iterable[str], *, f_min: float = 0.5, f_max: float = 10.0):
        now = time.time()
        self.params: Dict[str, Dict[str, float]] = {
            c: {
                "phi": random.uniform(0, 2 * math.pi),
                "amp": 0.5,
                "freq": random.uniform(f_min, f_max),
            }
            for c in concepts
        }
        self.f_min = f_min
        self.f_max = f_max
        # learning rates
        self.eta_phi = 1e-3
        self.eta_amp = 1e-3
        self.eta_freq = 1e-4

    # -------------------------------------------------------------
    def update_params(self, reward: float):
        """Nudge parameters using simple gradient-like rules based on reward."""
        for c, p in self.params.items():
            # current activation sign approximated by sin output
            act = math.sin(p["phi"]) * p["amp"]
            sign = 1.0 if act >= 0 else -1.0

            # Phase shift towards constructive interference if reward positive
            p["phi"] += self.eta_phi * reward * sign
            p["phi"] = p["phi"] % (2 * math.pi)

            # Amplitude adjustment (bounded 0-1)
            p["amp"] = min(1.0, max(0.0, p["amp"] + self.eta_amp * reward * act))

            # Frequency nudged toward small integer ratios (harmonic locking)
            # Calculate distance to nearest integer
            nearest_int = round(p["freq"])
            harmonic_grad = (nearest_int - p["freq"])
            p["freq"] += self.eta_freq * reward * harmonic_grad
            p["freq"] = min(self.f_max, max(self.f_min, p["freq"]))

    # -------------------------------------------------------------
    def get_param_snapshot(self) -> Dict[str, Dict[str, float]]:
        """Return a copy of current parameters for logging/inspection."""
        return {k: v.copy() for k, v in self.params.items()} 