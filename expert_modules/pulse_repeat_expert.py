from typing import List, Dict, Any
import time
from collections import Counter

from expert_modules.base_expert import BaseExpertModule, ExpertResponse


class PulseRepeatExpert(BaseExpertModule):
    """Detects repeated pulses at approximately the same frequency within a short window."""

    def _define_wave_frequencies(self):
        return {"pulse_repeat": 5.0}

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "detect_pulses" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "components" not in context or "sr" not in context or "hop_size" not in context:
            raise ValueError("PulseRepeatExpert requires 'components', 'sr', and 'hop_size' in context")

        components: List[Dict[str, float]] = context["components"]
        sr: int = context["sr"]
        hop_size: int = context["hop_size"]
        tolerance_hz = context.get("tolerance_hz", 20.0)
        min_repeats = context.get("min_repeats", 2)
        max_gap_frames = context.get("max_gap_frames", 2)  # <=0.05s for hop 512 at 22kHz

        start = time.perf_counter()

        # Build list of dominant freqs per frame
        dominant = {}
        for c in components:
            f_idx = int(c["frame"])
            if f_idx not in dominant or c["amp"] > dominant[f_idx]["amp"]:
                dominant[f_idx] = c["freq"]

        frames_sorted = sorted(dominant.items())

        # Detect runs of similar freq within tolerance
        pulse_positions = []
        i = 0
        while i < len(frames_sorted) - min_repeats + 1:
            base_freq = frames_sorted[i][1]
            run = [frames_sorted[i]]
            j = i + 1
            while j < len(frames_sorted):
                if frames_sorted[j][0] - run[-1][0] <= max_gap_frames and abs(frames_sorted[j][1] - base_freq) < tolerance_hz:
                    run.append(frames_sorted[j])
                    j += 1
                else:
                    break
            if len(run) >= min_repeats:
                # Record start time of pulse sequence
                pulse_positions.append(run[0][0] * hop_size / sr)
                i = run[-1][0] + 1
            else:
                i += 1

        processing_time = time.perf_counter() - start

        return ExpertResponse(
            confidence=1.0,
            reasoning=f"Detected {len(pulse_positions)} repeating pulses (≥{min_repeats} repeats, tol {tolerance_hz} Hz)",
            answer=pulse_positions,
            wave_patterns=self.generate_wave_patterns(["pulse_repeat"], strength=1.0),
            metadata={"tolerance_hz": tolerance_hz, "pulses": pulse_positions},
            processing_time=processing_time,
        ) 