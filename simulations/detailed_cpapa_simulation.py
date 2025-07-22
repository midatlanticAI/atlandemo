from pathlib import Path
import sys
import os
from typing import List

import numpy as np
import matplotlib.pyplot as plt

# Ensure project roots in path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for p in [PROJECT_ROOT, PROJECT_ROOT / "expert_modules", PROJECT_ROOT / "controllers", PROJECT_ROOT / "simulations"]:
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

# Local imports (after sys.path update)
from expert_modules.registry import ExpertRegistry
from expert_modules.respiratory_flow_expert import RespiratoryFlowExpert
from expert_modules.acoustic_snore_expert import AcousticSnoreExpert
from controllers.adaptive_bilevel_controller import AdaptiveBilevelController
from simulations.apnea_replay import generate_trace, DEFAULT_SR as FLOW_SR

# Audio settings
AUDIO_SR = 2000  # Hz, synthetic microphone sample rate


def _generate_snore_audio(event: str, duration_s: float, sr: int = AUDIO_SR) -> np.ndarray:
    """Generate synthetic snore audio segment."""
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    if event == "obstructive":
        amp = 0.2  # loud
    elif event == "central":
        amp = 0.02  # no snore
    else:
        amp = 0.05  # mild
    fundamental = 100  # Hz
    audio = amp * np.sin(2 * np.pi * fundamental * t)
    # Add harmonics & noise
    audio += 0.5 * amp * np.sin(2 * np.pi * 2 * fundamental * t)
    audio += 0.3 * amp * np.random.randn(len(t))
    return audio.astype(np.float32)


def _simulate_leak(ipap: float) -> float:
    """Simple leak model: baseline 10 L/min + 2 L/min per cmH2O above 10."""
    baseline = 10.0
    extra = max(0.0, (ipap - 10.0) * 2.0)
    # Random fluctuation
    noise = np.random.normal(0, 2.0)
    return baseline + extra + noise


def run_detailed(duration_s: int = 300):
    flow, labels = generate_trace(duration_s)

    registry = ExpertRegistry()
    registry.register_expert(RespiratoryFlowExpert(name="resp_flow", domain="respiratory"))
    registry.register_expert(AcousticSnoreExpert(name="snore", domain="acoustic"))

    controller = AdaptiveBilevelController()

    ipap_list: List[float] = []
    epap_list: List[float] = []
    leak_list: List[float] = []
    classified_flow: List[str] = []
    snore_labels: List[str] = []

    window_size = 50  # 2 s windows at 25 Hz
    audio_win_size = int(AUDIO_SR * 2)

    for i in range(0, len(flow), window_size):
        seg_flow = flow[i:i + window_size]
        event_resp = registry.process_query("classify_airway_event", {"flow": seg_flow, "sr": FLOW_SR})
        classified_flow.append(event_resp.answer)

        # Generate snore audio for same window
        audio_seg = _generate_snore_audio(event_resp.answer, duration_s=2.0)
        snore_resp = registry.process_query("detect_snore", {"audio": audio_seg, "sr": AUDIO_SR})
        snore_labels.append(snore_resp.answer)

        # Simulate leak based on current IPAP after update
        ipap, epap = controller.update(event_resp.answer)
        leak = _simulate_leak(ipap)
        leak_list.extend([leak] * len(seg_flow))

        ipap_list.extend([ipap] * len(seg_flow))
        epap_list.extend([epap] * len(seg_flow))

    ipap_arr = np.array(ipap_list)
    epap_arr = np.array(epap_list)
    leak_arr = np.array(leak_list)

    # Plotting
    t = np.arange(len(flow)) / FLOW_SR
    plt.figure(figsize=(14, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, flow, label="Flow (L/s)")
    plt.ylabel("Flow")

    plt.subplot(3, 1, 2)
    plt.plot(t, ipap_arr, label="IPAP", color="orange")
    plt.plot(t, epap_arr, label="EPAP", color="green", linestyle="--")
    plt.ylabel("Pressure (cmH2O)")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(t, leak_arr, label="Leak (L/min)", color="red")
    plt.ylabel("Leak")
    plt.xlabel("Time (s)")
    plt.tight_layout()
    out_path = Path("data/detailed_closed_loop.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    print(f"Saved detailed plot to {out_path}")

    # Console metrics
    print("--- Simulation Summary ---")
    print(f"Duration: {duration_s} s, breaths processed: {len(ipap_arr) // window_size}")
    print(f"Obstructive events: {classified_flow.count('obstructive')}")
    print(f"Central events: {classified_flow.count('central')}")
    print(f"Avg IPAP: {np.mean(ipap_arr):.2f} cmH2O, Avg EPAP: {np.mean(epap_arr):.2f} cmH2O")
    print(f"Avg leak: {np.mean(leak_arr):.1f} L/min (max {np.max(leak_arr):.1f})")

    return {
        "flow": flow,
        "ipap": ipap_arr,
        "epap": epap_arr,
        "leak": leak_arr,
        "flow_labels": labels,
        "classified_flow": classified_flow,
        "snore_labels": snore_labels,
    }


if __name__ == "__main__":
    run_detailed() 