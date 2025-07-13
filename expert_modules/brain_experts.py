from typing import Dict, Any, List
import time
import numpy as np

from expert_modules.base_expert import BaseExpertModule, ExpertResponse


class RhythmPowerExpert(BaseExpertModule):
    """Compute average power in canonical EEG bands."""

    def _define_wave_frequencies(self):
        return {"alpha": 8.0, "beta": 20.0, "theta": 5.0}

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "eeg_rhythm_power" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "frames" not in context or "sr" not in context:
            raise ValueError("RhythmPowerExpert requires 'frames' and 'sr' in context")

        frames: np.ndarray = context["frames"]  # shape: (num_frames, frame_size)
        sr: int = context["sr"]

        start = time.perf_counter()
        fft = np.fft.rfft(frames * np.hanning(frames.shape[1]), axis=1)
        psd = np.abs(fft) ** 2
        freqs = np.fft.rfftfreq(frames.shape[1], 1 / sr)

        def band_power(low, high):
            idx = np.logical_and(freqs >= low, freqs <= high)
            return float(np.mean(psd[:, idx]))

        alpha = band_power(8, 12)
        beta = band_power(13, 30)
        theta = band_power(4, 7)

        processing_time = time.perf_counter() - start
        answer = {"alpha": alpha, "beta": beta, "theta": theta}

        return ExpertResponse(
            confidence=1.0,
            reasoning="Average band power computed",
            answer=answer,
            wave_patterns=self.generate_wave_patterns(["alpha", "beta", "theta"], strength=1.0),
            metadata=answer,
            processing_time=processing_time,
        )


class MuDropExpert(BaseExpertModule):
    """Detects >X% drop in 8–12 Hz power indicating motor imagery."""

    def _define_wave_frequencies(self):
        return {"mu_drop": 10.0}

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "detect_mu_drop" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "alpha_series" not in context:
            raise ValueError("MuDropExpert requires 'alpha_series' in context")

        alpha_series: List[float] = context["alpha_series"]
        threshold = context.get("drop_pct", 0.3)  # 30 % drop

        baseline = np.median(alpha_series[:10]) if len(alpha_series) >= 10 else np.median(alpha_series)
        events = []
        for idx, val in enumerate(alpha_series):
            if baseline > 0 and (baseline - val) / baseline >= threshold:
                events.append(idx)

        return ExpertResponse(
            confidence=1.0,
            reasoning=f"Detected {len(events)} mu-drop frames",
            answer=events,
            wave_patterns=self.generate_wave_patterns(["mu_drop"], strength=1.0),
            metadata={"baseline_alpha": baseline, "events": events},
            processing_time=0.0,
        ) 