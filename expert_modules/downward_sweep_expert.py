from typing import List, Dict, Any
import time

from expert_modules.base_expert import BaseExpertModule, ExpertResponse


class DownwardSweepExpert(BaseExpertModule):
    """Detects monotonic downward frequency sweeps."""

    def _define_wave_frequencies(self):
        return {"downward_sweep": 4.0}

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "detect_downward_sweeps" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "components" not in context or "sr" not in context or "hop_size" not in context:
            raise ValueError("DownwardSweepExpert requires 'components', 'sr', and 'hop_size' in context")

        components: List[Dict[str, float]] = context["components"]
        sr: int = context["sr"]
        hop_size: int = context["hop_size"]
        delta_hz = context.get("delta_hz", 20.0)

        start = time.perf_counter()

        dominant = {}
        for c in components:
            f_idx = int(c["frame"])
            if f_idx not in dominant or c["amp"] > dominant[f_idx]["amp"]:
                dominant[f_idx] = {"freq": c["freq"], "amp": c["amp"]}

        frames_sorted = sorted(dominant.items())
        freqs_seq = [item[1]["freq"] for item in frames_sorted]
        sweep_positions = []
        i = 0
        while i < len(freqs_seq) - 2:
            if freqs_seq[i+1] < freqs_seq[i] - delta_hz and freqs_seq[i+2] < freqs_seq[i+1] - delta_hz:
                t_sec = frames_sorted[i][0] * hop_size / sr
                sweep_positions.append(t_sec)
                i += 3
            else:
                i += 1

        processing_time = time.perf_counter() - start

        return ExpertResponse(
            confidence=1.0,
            reasoning=f"Detected {len(sweep_positions)} downward sweeps (Δ>{delta_hz} Hz)",
            answer=sweep_positions,
            wave_patterns=self.generate_wave_patterns(["downward_sweep"], strength=1.0),
            metadata={"delta_hz": delta_hz, "sweeps": sweep_positions},
            processing_time=processing_time,
        ) 