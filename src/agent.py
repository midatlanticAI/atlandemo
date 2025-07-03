import random
import time
import json
from typing import Dict, List, Tuple, Any, Optional, Union

# Import components from other modules within the package
from .memory import RCoreMemoryIndex, SymbolicNode
from .perception import ToneEngine, DriftTracker
from .reasoning import BeliefSystem, DreamspaceSimulator
from .reflection import SelfAnchor
from .narrative import NarrativeNode
from .utils import _enhanced_vector


class AtlanAgent:
    """Orchestrates the components of the Atlan symbolic cognitive engine."""

    def __init__(self, agent_id: str = "atlan_v1", config: Optional[Dict[str, Any]] = None):
        """Initializes the agent and its cognitive components."""
        self.agent_id = agent_id
        self._config = config if config else {}
        self._creation_time = time.time()

        # Memory configuration
        memory_config = self._config.get('memory', {})
        max_memory = memory_config.get('max_size', 1000)

        # Initialize components (allow passing custom configs/instances later)
        self.memory = RCoreMemoryIndex(
            max_memory_size=max_memory,
            config=memory_config
        )
        self.tone_engine = ToneEngine()
        self.drift_tracker = DriftTracker(max_window=self._config.get('drift_window', 30))

        # Narrative tracking
        self.narrator = NarrativeNode(
            entity_id=agent_id,
            drift_tracker=self.drift_tracker,
            tone_engine=self.tone_engine
        )

        # Reasoning components
        self.belief_system = BeliefSystem(initial_beliefs=self._config.get('initial_beliefs'))
        self.dreamspace = DreamspaceSimulator(action_effects=self._config.get('action_effects'))
        self.anchor = SelfAnchor(self.belief_system, self.drift_tracker)

        # State tracking
        self.last_input_phrase: Optional[str] = None
        self.last_chosen_action: Optional[str] = None
        self.last_reflection: Optional[Dict[str, Any]] = None
        self.last_narrative: Optional[Dict[str, Any]] = None
        self.projected_outcomes: Dict[str, float] = {}  # Store projections for actions

    def process_input(self, phrase: str, label: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes a new input phrase: encodes, perceives mood, updates memory.

        Args:
            phrase: The input text to process
            label: Optional category label for the memory

        Returns:
            Dictionary with processing results
        """
        self.last_input_phrase = phrase

        # 1. Encode input
        vector = _enhanced_vector(phrase)

        # 2. Perceive Mood & Update Drift
        mood_score = self.tone_engine.score_phrase(phrase)
        self.drift_tracker.add_mood(mood_score)

        # Update narrative tracking
        self.narrator.add_mood(mood_score)

        # 3. Memory Interaction (Search/Add/Reinforce)
        search_results = self.memory.search(vector, top_k=1)
        match_threshold = self._config.get('match_threshold', 0.95)
        match_info = {"status": "no_match", "reinforced_index": None, "score": None}

        if search_results and search_results[0][1] >= match_threshold:
            match_idx = search_results[0][0]
            self.memory.reinforce_by_index(match_idx)
            match_info = {"status": "reinforced", "reinforced_index": match_idx, "score": search_results[0][1]}
        else:
            new_idx = self.memory.add(phrase=phrase, vector=vector, label=label)
            match_info = {"status": "added", "added_index": new_idx}

        # 4. Potentially trigger narrative update (not every time)
        if random.random() < 0.2:  # 20% chance to update narrative
            self.last_narrative = self.narrator.build_narrative()

        return {
            "input_phrase": phrase,
            "mood_score": mood_score,
            "vector": vector,
            "memory_interaction": match_info,
            "drift": self.drift_tracker.drift(),
            "personality": self.narrator.evolve_personality() if self.last_narrative else []
        }

    def choose_action(self) -> str:
        """
        Uses Dreamspace to simulate and choose the best action based on current state.

        Returns:
            The chosen action string
        """
        current_drift = self.drift_tracker.drift()

        # Calculate average reinforcement from recent memories
        recent_memories = min(5, len(self.memory.memory))
        if recent_memories > 0:
            avg_reinforcement = sum(node.get("reinforcement", 1.0)
                                  for node in self.memory.memory[-recent_memories:]) / recent_memories
        else:
            avg_reinforcement = 1.0

        chosen_action, projected_resonance, projections = self.dreamspace.simulate_resonance_projection(
            current_drift, avg_reinforcement
        )

        # Store all projections for future reference
        self.projected_outcomes = {p["action"]: p["projected_resonance"] for p in projections}
        self.last_chosen_action = chosen_action
        return chosen_action

    def record_outcome(self, action: str, actual_outcome: float) -> Dict[str, Any]:
        """
        Records the actual outcome of an action and updates beliefs via SelfAnchor.

        Args:
            action: The action that was taken
            actual_outcome: The observed outcome value (-1.0 to 1.0)

        Returns:
            Dictionary with feedback results
        """
        # Find the projected outcome for the action taken
        projected_outcome = self.projected_outcomes.get(
            action,
            self.dreamspace.action_templates.get(action, 0.0)  # Fallback if no projection stored
        )

        # Get feedback signal (reinforce/contradict/neutral)
        feedback_signal, alignment = self.dreamspace.learn_from_outcome(projected_outcome, actual_outcome)

        # Record feedback and trigger belief updates
        self.anchor.record_action_feedback(action, feedback_signal, alignment)

        return {
            "action": action,
            "feedback": feedback_signal,
            "alignment": alignment,
            "projected": projected_outcome,
            "actual": actual_outcome
        }

    def reflect(self) -> Dict[str, Any]:
        """
        Triggers a self-reflection cycle to revise beliefs and analyze state.

        Returns:
            Reflection results
        """
        # First, update narrative if it hasn't been updated recently
        if not self.last_narrative or (time.time() - self.last_narrative.get("timestamp", 0)) > 3600:
            self.last_narrative = self.narrator.build_narrative()

        # Then perform belief reflection
        self.last_reflection = self.anchor.reflect()

        # Add narrative context to reflection
        if self.last_reflection and self.last_narrative:
            self.last_reflection["narrative_context"] = {
                "personality": self.narrator.evolve_personality(),
                "avg_mood": self.last_narrative["avg_mood"],
                "mood_label": self.last_narrative["label"]
            }

        return self.last_reflection

    def get_state(self, include_memory_sample: int = 0) -> Dict[str, Any]:
        """
        Returns a snapshot of the agent's current internal state.

        Args:
            include_memory_sample: Number of recent memory nodes to include (0 for none)

        Returns:
            Dictionary with agent state
        """
        state = {
            "agent_id": self.agent_id,
            "uptime": time.time() - self._creation_time,
            "drift_state": self.drift_tracker.get_state(),
            "beliefs": self.belief_system.audit_beliefs(),
            "memory_stats": self.memory.get_stats(),
            "last_reflection": self.last_reflection,
            "personality": self.narrator.evolve_personality(),
            "config": self._config
        }

        if include_memory_sample > 0:
            sample_size = min(include_memory_sample, len(self.memory.memory))
            # Get a sample of the most recently added memory nodes
            state["memory_sample"] = self.memory.memory[-sample_size:]

        return state

    def get_response_template(self) -> str:
        """
        Gets a tone-appropriate response template based on current mood state.

        Returns:
            Response template string
        """
        avg_mood = self.drift_tracker.avg_mood()
        tone = self.tone_engine.infer_tone(avg_mood)
        return self.tone_engine.get_response_template(tone)

    def save_state(self, filepath: str) -> bool:
        """
        Saves the agent's current state to a JSON file.

        Args:
            filepath: Path to save the state file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get full state without memory sample to keep file size reasonable
            state = self.get_state(include_memory_sample=0)

            # Add serialization-specific fields
            state["_serialized_at"] = time.time()
            state["_version"] = "1.0"

            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving state: {e}")
            return False

    def load_state(self, filepath: str) -> bool:
        """
        Loads agent state from a JSON file.

        Args:
            filepath: Path to the state file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)

            # Here you would restore the various components from the saved state
            # This would need a more detailed implementation to correctly restore
            # the full agent state with all its components
            return True
        except Exception as e:
            print(f"Error loading state: {e}")
            return False 