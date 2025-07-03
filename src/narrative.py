import time
from typing import Dict, List, Tuple, Any, Optional

from .perception import DriftTracker, ToneEngine


class NarrativeNode:
    """
    Tracks mood history and infers a symbolic narrative about the user or agent.
    Used to construct memory arcs and emotional profiles over time.
    """

    def __init__(self, entity_id: str, drift_tracker: Optional[DriftTracker] = None, tone_engine: Optional[ToneEngine] = None):
        """
        Initialize the narrative node.

        Args:
            entity_id: Identifier for the entity (user, agent, etc.)
            drift_tracker: Optional existing drift tracker to use
            tone_engine: Optional existing tone engine to use
        """
        self.entity_id = entity_id
        self.drift_tracker = drift_tracker if drift_tracker else DriftTracker()
        self.tone_engine = tone_engine if tone_engine else ToneEngine()
        self.personality_flags: List[str] = []
        self.summary_log: List[Dict[str, Any]] = []
        self.last_narrative: Optional[Dict[str, Any]] = None

    def add_mood(self, mood_score: float) -> None:
        """
        Add a mood score to the tracker.

        Args:
            mood_score: Mood value between -1.0 and 1.0
        """
        self.drift_tracker.add_mood(mood_score)

    def build_narrative(self) -> Dict[str, Any]:
        """
        Analyze current mood trends and build a narrative summary.

        Returns:
            Summary dictionary with mood metrics and personality label
        """
        avg = self.drift_tracker.avg_mood()
        drift = self.drift_tracker.drift()
        volatility = self.drift_tracker.volatility()

        label = self._classify_personality(drift, volatility)
        summary = {
            "timestamp": time.time(),
            "avg_mood": avg,
            "drift": drift,
            "volatility": volatility,
            "label": label
        }

        self.summary_log.append(summary)
        self.personality_flags.append(label)
        self.last_narrative = summary

        return summary

    def _classify_personality(self, drift: float, volatility: float) -> str:
        """
        Classify personality based on mood drift and volatility.

        Args:
            drift: Current mood drift value
            volatility: Current mood volatility

        Returns:
            Personality label as string
        """
        if drift > 0.3 and volatility < 0.2:
            return "resilient"
        elif drift < -0.3 and volatility < 0.2:
            return "discouraged"
        elif volatility >= 0.4:
            return "emotionally_volatile"
        elif drift < 0 and volatility > 0.2:
            return "fragile"
        else:
            return "stable"

    def evolve_personality(self) -> List[str]:
        """
        Aggregate narrative into simplified personality traits.

        Returns:
            List of top personality traits
        """
        trait_count: Dict[str, int] = {}
        for label in self.personality_flags:
            trait_count[label] = trait_count.get(label, 0) + 1

        if not trait_count:
            return ["unknown"]
        
        sorted_traits = sorted(trait_count.items(), key=lambda x: x[1], reverse=True)
        top_traits = [t[0] for t in sorted_traits[:2]]
        return top_traits

    def get_current_narrative(self) -> Dict[str, Any]:
        """
        Get the most recent narrative summary.

        Returns:
            Latest narrative summary or empty dict if none exists
        """
        return self.last_narrative or {} 