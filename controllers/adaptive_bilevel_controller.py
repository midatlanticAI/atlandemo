from typing import Optional
import numpy as np


class AdaptiveBilevelController:
    """Bi-level CPAP controller with IPAP/EPAP, leak handling, and decay logic."""

    def __init__(
        self,
        baseline_epap: float = 5.0,
        delta_epap_ipap: float = 1.0,
        max_ipap: float = 20.0,
        min_epap: float = 4.0,
        incr_step: float = 0.5,
        decr_step: float = 0.5,
        max_delta_per_breath: float = 2.0,
        decay_breaths: int = 10,
        leak_threshold_lpm: float = 40.0,
        leak_breaths: int = 15,
    ):
        self.epap = baseline_epap
        self.ipap = baseline_epap + delta_epap_ipap
        self.baseline_epap = baseline_epap
        self.delta = delta_epap_ipap
        self.max_ipap = max_ipap
        self.min_epap = min_epap
        self.incr_step = incr_step
        self.decr_step = decr_step
        self.max_delta_per_breath = max_delta_per_breath
        self.decay_breaths = decay_breaths
        self._clear_counter = 0  # breaths since last obstruction
        self._leak_counter = 0   # consecutive breaths with excessive leak
        self.leak_threshold = leak_threshold_lpm
        self.leak_breaths = leak_breaths
        self.last_alarm: Optional[str] = None

    def update(self, event: str, leak_lpm: Optional[float] = 0.0):
        """Update pressures based on event classification and leak.

        Args:
            event: 'obstructive', 'central', 'clear', or other.
            leak_lpm: leak level in L/min; high leak reduces confidence.
        Returns:
            Tuple (ipap, epap)
        """
        # Leak handling
        if leak_lpm is not None and leak_lpm > self.leak_threshold:
            self._leak_counter += 1
            if self._leak_counter >= self.leak_breaths:
                # Reduce pressures to attempt leak mitigation
                prev_ipap, prev_epap = self.ipap, self.epap
                self.ipap = max(self.min_epap + self.delta, self.ipap - self.decr_step)
                self.epap = self.ipap - self.delta
                self.last_alarm = "leak_high"
                # Ensure delta limit per breath
                if abs(self.ipap - prev_ipap) > self.max_delta_per_breath:
                    self.ipap = prev_ipap - self.max_delta_per_breath
                    self.epap = self.ipap - self.delta
                return self.ipap, self.epap
            # If leak exists but not yet sustained threshold, keep pressures frozen
            self.last_alarm = None
            return self.ipap, self.epap
        else:
            # Leak resolved
            self._leak_counter = 0
            if self.last_alarm == "leak_high":
                self.last_alarm = None

        prev_ipap, prev_epap = self.ipap, self.epap

        if event == "obstructive":
            self.epap += self.incr_step
            self.ipap = self.epap + self.delta
            self._clear_counter = 0
        else:
            # central, clear, or unknown
            self._clear_counter += 1
            if self._clear_counter >= self.decay_breaths:
                self.epap -= self.decr_step
                self.ipap = self.epap + self.delta

        # Clamp values
        self.epap = float(np.clip(self.epap, self.min_epap, self.max_ipap - self.delta))
        self.ipap = float(np.clip(self.ipap, self.epap + self.delta, self.max_ipap))

        # Enforce max change per breath
        if abs(self.ipap - prev_ipap) > self.max_delta_per_breath:
            self.ipap = prev_ipap + np.sign(self.ipap - prev_ipap) * self.max_delta_per_breath
            self.epap = self.ipap - self.delta
        if abs(self.epap - prev_epap) > self.max_delta_per_breath:
            self.epap = prev_epap + np.sign(self.epap - prev_epap) * self.max_delta_per_breath
            self.ipap = self.epap + self.delta

        return self.ipap, self.epap

    def get_state(self):
        return {
            "ipap": self.ipap,
            "epap": self.epap,
            "clear_counter": self._clear_counter,
            "leak_counter": self._leak_counter,
            "alarm": self.last_alarm,
        } 