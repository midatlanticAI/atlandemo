from pathlib import Path
import os
import sys
from typing import List

# Ensure project and expert_modules are on sys.path when executed directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for p in [PROJECT_ROOT, PROJECT_ROOT / "expert_modules"]:
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

import numpy as np
import matplotlib.pyplot as plt

from expert_modules.registry import ExpertRegistry
from expert_modules.respiratory_flow_expert import RespiratoryFlowExpert
from simulations.apnea_replay import generate_trace, DEFAULT_SR


class AdaptivePressureController:
    """Deterministic CPAP controller: adjusts pressure based on event type."""

    def __init__(self, baseline: float = 5.0, incr: float = 0.5, decr: float = 0.2,
                 max_delta_per_breath: float = 2.0, p_min: float = 4.0, p_max: float = 20.0):
        self.pressure = baseline
        self.baseline = baseline
        self.incr = incr
        self.decr = decr
        self.max_delta = max_delta_per_breath
        self.p_min = p_min
        self.p_max = p_max

    def update(self, event: str):
        """Update pressure based on classified event."""
        prev = self.pressure
        if event == "obstructive":
            self.pressure = min(self.p_max, self.pressure + self.incr)
        elif event == "central":
            # For central events, do not increase; may decrease toward baseline
            self.pressure = max(self.p_min, self.pressure - self.decr)
        # Enforce max delta per breath
        delta = self.pressure - prev
        if abs(delta) > self.max_delta:
            self.pressure = prev + np.sign(delta) * self.max_delta
        return self.pressure


def run_closed_loop(duration_s: int = 300):
    flow, labels = generate_trace(duration_s)

    registry = ExpertRegistry()
    registry.register_expert(RespiratoryFlowExpert(name="resp_flow", domain="respiratory"))

    controller = AdaptivePressureController()

    pressures: List[float] = []
    classified: List[str] = []

    # process per breath ~ assume 2 second windows (for 25 Hz sr -> 50 samples)
    window_size = 50
    for i in range(0, len(flow), window_size):
        seg = flow[i:i + window_size]
        ctx = {"flow": seg, "sr": DEFAULT_SR}
        resp = registry.process_query("classify_airway_event", ctx)
        classified.append(resp.answer)
        p = controller.update(resp.answer)
        pressures.extend([p] * len(seg))

    pressures = np.array(pressures)

    # Plot for quick visual
    t = np.arange(len(flow)) / DEFAULT_SR
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, flow, label="Flow (L/s)")
    plt.title("Synthetic Flow Trace & Pressure")
    plt.ylabel("Flow")
    plt.subplot(2, 1, 2)
    plt.plot(t, pressures, label="Pressure (cmH2O)", color="orange")
    plt.ylabel("Pressure")
    plt.xlabel("Time (s)")
    plt.tight_layout()
    out_path = Path("data/closed_loop_result.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    print(f"Saved plot to {out_path}")

    return flow, labels, classified, pressures


if __name__ == "__main__":
    run_closed_loop() 