from typing import Dict, Any
import time
import numpy as np

from .base_expert import BaseExpertModule, ExpertResponse


class RespiratoryFlowExpert(BaseExpertModule):
    """Classifies respiratory events (obstructive vs. central) from flow signal."""

    def _define_wave_frequencies(self) -> Dict[str, float]:
        # Map conceptual events to arbitrary resonance frequencies (Hz)
        return {
            "obstructive": 0.3,
            "central": 0.7,
        }

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "classify_airway_event" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "flow" not in context or "sr" not in context:
            raise ValueError("RespiratoryFlowExpert requires 'flow' (np.ndarray) and 'sr' (sample rate) in context")

        flow: np.ndarray = context["flow"]  # shape: (n_samples,)
        sr: int = int(context["sr"])

        if flow.ndim != 1:
            raise ValueError("'flow' must be 1-D array of respiratory airflow samples")

        start_t = time.perf_counter()

        # Hanning window to reduce spectral leakage
        windowed = flow * np.hanning(len(flow))
        fft = np.fft.rfft(windowed)
        psd = np.abs(fft) ** 2
        freqs = np.fft.rfftfreq(len(flow), 1.0 / sr)

        def band_energy(low: float, high: float) -> float:
            idx = np.logical_and(freqs >= low, freqs <= high)
            if not np.any(idx):  # edge case: no bins in range
                return 0.0
            return float(np.mean(psd[idx]))

        # Empirical bands (Hz) for apnea classification
        low_band = band_energy(0.0, 0.5)   # Breath hold / minimal effort
        mid_band = band_energy(0.5, 2.0)   # Typical snore / obstructive oscillations

        total_power = low_band + mid_band

        # Absolute low-power quiet breathing implies central/clear
        power_threshold = 5e-3  # adjusted for synthetic signal levels

        # Ratio > threshold also suggests central events (lack of turbulent mid-band energy)
        ratio = (low_band + 1e-9) / (mid_band + 1e-9)
        ratio_threshold = context.get("ratio_threshold", 1.0)

        if total_power < power_threshold or ratio > ratio_threshold or mid_band < 0.5 * low_band:
            event = "central"
        else:
            event = "obstructive"

        processing_time = time.perf_counter() - start_t

        # Confidence grows as ratio deviates from threshold or low total power
        if total_power < power_threshold:
            confidence = 0.9
        else:
            confidence = max(0.2, min(1.0, abs(np.log10(ratio / ratio_threshold))))
        confidence = float(confidence)

        return ExpertResponse(
            confidence=confidence,
            reasoning=f"Band-energy ratio={ratio:.3f} (threshold={ratio_threshold})",
            answer=event,
            wave_patterns=self.generate_wave_patterns([event], strength=confidence),
            metadata={
                "ratio": ratio,
                "low_band_energy": low_band,
                "mid_band_energy": mid_band,
                "threshold": ratio_threshold,
            },
            processing_time=processing_time,
        ) 