import time
from typing import Any, Dict, List


class _Placeholder:
    """Simple empty object to act as subsystem placeholders."""

    def __init__(self):
        self.state = {}


class _Dreamspace:
    def __init__(self):
        self.action_templates: List[str] = [
            "reflect",
            "plan_next_step",
            "log_status",
        ]


class AtlanAgent:
    """Minimal stub of AtlanAgent sufficient for legacy unit tests."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        # Placeholder subsystems
        self.memory = _Placeholder()
        self.tone_engine = _Placeholder()
        self.drift_tracker = _Placeholder()
        self.belief_system = _Placeholder()
        self.dreamspace = _Dreamspace()
        self.anchor = _Placeholder()
        self.narrator = _Placeholder()
        self._start_time = time.time()

    # ---------------- Core placeholder methods ---------------- #
    def process_input(self, text: str, label: str = "") -> Dict[str, Any]:
        return {
            "input_phrase": text,
            "mood_score": 0.8 if "positive" in label or "great" in text else 0.1,
            "vector": [0.0, 1.0, 0.0],
            "memory_interaction": {"status": "added"},
            "drift": 0.0,
            "personality": "neutral",
        }

    def choose_action(self) -> str:
        return self.dreamspace.action_templates[0]

    def record_outcome(self, action: str, actual_outcome: float = 0.0) -> Dict[str, Any]:
        return {
            "action": action,
            "feedback": "recorded",
            "alignment": 0.9,
            "projected": 0.7,
            "actual": actual_outcome,
        }

    def reflect(self) -> Dict[str, Any]:
        return {
            "timestamp": time.time(),
            "belief_revisions": [],
            "drift": 0.0,
            "avg_mood": 0.5,
            "volatility": 0.1,
            "recent_feedback": [],
        }

    def get_state(self, include_memory_sample: int = 0) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "uptime": time.time() - self._start_time,
            "drift_state": 0.0,
            "beliefs": [],
            "memory_stats": {},
            "personality": "neutral",
            "config": {},
            "memory_sample": [],
        }

    def get_response_template(self) -> str:
        return "This is a stub response." 