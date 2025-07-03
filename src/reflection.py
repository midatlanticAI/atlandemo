import time
from typing import Dict, List, Tuple

# Need to import the classes it depends on
# Assuming they are in the same package level
from .reasoning import BeliefSystem
from .perception import DriftTracker


class SelfAnchor:
    """Handles agent self-reflection, belief updates based on action feedback, and logging."""
    
    def __init__(self, belief_system: BeliefSystem, drift_tracker: DriftTracker):
        # Check if provided objects are of the expected type
        if not isinstance(belief_system, BeliefSystem):
            raise TypeError("belief_system must be an instance of BeliefSystem")
        if not isinstance(drift_tracker, DriftTracker):
            raise TypeError("drift_tracker must be an instance of DriftTracker")

        self.beliefs = belief_system
        self.tracker = drift_tracker
        self.reflection_log: List[Dict] = []  # Store reflection events
        self.action_feedback_log: List[Tuple[str, str, float]] = []  # Store (action, feedback_signal, alignment)

        # Simple mapping from actions (keywords) to related beliefs
        # This could be made more sophisticated
        self.action_to_belief_map = {
            "follow_up": "follow_up_now improves outcome",
            "wait": "wait might resolve things",
            "escalate": "escalate is risky but sometimes needed",
            "reminder": "send_gentle_reminder is safe"
            # Add more mappings as actions/beliefs evolve
        }

    def _find_related_belief(self, action: str) -> str | None:
        """Finds a belief statement related to the action performed."""
        action_lower = action.lower()
        for keyword, belief_statement in self.action_to_belief_map.items():
            if keyword in action_lower:
                return belief_statement
        return None  # No related belief found in the map

    def record_action_feedback(self, action: str, feedback_signal: str, alignment: float):
        """Records action outcome feedback and updates relevant beliefs."""
        self.action_feedback_log.append((action, feedback_signal, alignment))

        # Find the belief related to this action
        related_belief = self._find_related_belief(action)

        if related_belief:
            # Update the belief based on the feedback signal
            if feedback_signal == "reinforce":
                self.beliefs.reinforce_belief(related_belief)
            elif feedback_signal == "contradict":
                self.beliefs.degrade_belief(related_belief)
            # 'neutral' feedback currently doesn't change beliefs
        # else:
        #     # Optional: Log if no related belief was found for an action
        #     print(f"Debug: No belief found related to action '{action}'")

    def reflect(self) -> Dict:
        """Performs a reflection cycle: revises beliefs, assesses mood state."""
        # 1. Trigger belief revision process
        revisions_made = self.beliefs.revise_beliefs()

        # 2. Get current emotional state from DriftTracker
        current_drift = self.tracker.drift()
        avg_mood = self.tracker.avg_mood()
        volatility = self.tracker.volatility()

        # 3. Compile reflection data
        reflection_event = {
            "timestamp": time.time(),
            "belief_revisions": revisions_made,  # List of (old_stmt, new_stmt) tuples
            "drift": current_drift,
            "avg_mood": avg_mood,
            "volatility": volatility,
            # Include a sample of recent action feedback for context
            "recent_feedback": self.action_feedback_log[-5:]
        }

        # 4. Log the reflection event
        self.reflection_log.append(reflection_event)

        # 5. Return the details of this reflection cycle
        return reflection_event

    def get_reflection_history(self) -> List[Dict]:
        """Returns the entire log of reflection events."""
        return self.reflection_log 