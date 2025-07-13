from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Schema:
    """A consolidated recurring resonance pattern.

    Attributes
    ----------
    symbols : Tuple[str, str]
        The pair of symbols that frequently co-activate (sorted for stability).
    count : int
        How many times this pattern has been observed.
    cumulative_strength : float
        Sum of the absolute interference values observed for this pair.
    last_seen : float
        Unix timestamp of the most recent observation.
    """

    symbols: Tuple[str, str]
    count: int = 0
    cumulative_strength: float = 0.0
    last_seen: float = field(default_factory=time.time)

    # ---------------------------------------------------------------------
    # Convenience helpers
    # ---------------------------------------------------------------------
    @property
    def avg_strength(self) -> float:
        """Return the average interference strength for this schema."""
        return self.cumulative_strength / self.count if self.count else 0.0

    def register_observation(self, strength: float, ts: float):
        """Update the schema with a new observation."""
        self.count += 1
        self.cumulative_strength += abs(float(strength))
        self.last_seen = ts

    # -----------------------------------------------------------------
    # (De)serialization helpers
    # -----------------------------------------------------------------
    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation."""
        return {
            "symbols": list(self.symbols),
            "count": self.count,
            "cumulative_strength": self.cumulative_strength,
            "last_seen": self.last_seen,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Schema":
        """Create a Schema from the dictionary produced by `to_dict`."""
        return cls(
            symbols=tuple(d["symbols"]),
            count=int(d.get("count", 0)),
            cumulative_strength=float(d.get("cumulative_strength", 0.0)),
            last_seen=float(d.get("last_seen", 0.0)),
        ) 