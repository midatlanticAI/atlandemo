from typing import Dict, Any
import time
import numpy as np

from .base_expert import BaseExpertModule, ExpertResponse


class AcousticSnoreExpert(BaseExpertModule):
    """Detects and quantifies snore events from short audio windows (0.5–2 s)."""

    def _define_wave_frequencies(self) -> Dict[str, float]:
        # Resonance tags for snore-related concepts
        return {"snore": 60.0, "breath": 20.0}

    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        return 1.0 if query == "detect_snore" else 0.0

    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        if context is None or "audio" not in context or "sr" not in context:
            raise ValueError("AcousticSnoreExpert requires 'audio' (np.ndarray) and 'sr' (sample rate) in context")

        audio: np.ndarray = context["audio"]  # mono PCM samples
        sr: int = int(context["sr"])

        if audio.ndim != 1:
            raise ValueError("'audio' must be 1-D array of PCM samples")

        start_t = time.perf_counter()

        # Band-pass (20–200 Hz) typical snore fundamental & harmonics
        fft = np.fft.rfft(audio * np.hanning(len(audio)))
        psd = np.abs(fft) ** 2
        freqs = np.fft.rfftfreq(len(audio), 1.0 / sr)

        snore_band = np.logical_and(freqs >= 20, freqs <= 200)
        breath_band = np.logical_and(freqs >= 200, freqs <= 1000)

        snore_power = float(np.mean(psd[snore_band]))
        breath_power = float(np.mean(psd[breath_band]))

        ratio = (snore_power + 1e-9) / (breath_power + 1e-9)

        # Absolute power gate to filter out very quiet signals
        power_thresh = 0.1  # increased threshold for clearer separation with FFT scaling

        if snore_power < power_thresh:
            snore_label = "no_snore"
            confidence = 0.2
        elif ratio > 3 and snore_power > 1.0:
            snore_label = "loud_snore"
            confidence = min(1.0, np.log10(ratio))
        elif ratio > 1:
            snore_label = "mild_snore"
            confidence = 0.5
        else:
            snore_label = "no_snore"
            confidence = 0.3

        processing_time = time.perf_counter() - start_t

        return ExpertResponse(
            confidence=confidence,
            reasoning=f"Snore-to-breath power ratio={ratio:.2f}",
            answer=snore_label,
            wave_patterns=self.generate_wave_patterns(["snore" if snore_label != "no_snore" else "breath"], strength=confidence),
            metadata={
                "snore_power": snore_power,
                "breath_power": breath_power,
                "ratio": ratio,
                "power_thresh": power_thresh,
            },
            processing_time=processing_time,
        ) 