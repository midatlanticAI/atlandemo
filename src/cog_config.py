from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class CogConfig:
    """Configuration parameters for TemporalCognitionEngine & ExperienceStream."""

    # Consolidation & memory parameters
    consolidation_threshold: float = 0.7  # abs(interference) required to log a pattern
    schema_support_threshold: int = 3      # observations to promote to stable schema
    max_schemas: int = 100                # memory cap

    # Determinism & seeding
    deterministic: bool = False
    seed: Optional[int] = None            # RNG seed when deterministic

    # Persistence backend
    store_backend: str = "json"          # "json" or "sqlite"
    store_path: str = "schemas.json"      # file path for the backend
    save_frequency: int = 50              # persist after N consolidations

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "CogConfig":
        """Create a config from a plain dictionary, ignoring unknown keys."""
        valid = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in valid}
        return cls(**filtered)  # type: ignore[arg-type]

    def to_dict(self) -> dict:
        """Return a dict representation suitable for JSON/YAML."""
        return asdict(self) 