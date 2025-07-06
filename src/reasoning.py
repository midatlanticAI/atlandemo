import random
from typing import List, Dict, Tuple, Union, Optional


class BeliefSystem:
    """Manages agent beliefs, confidence, and revision based on feedback."""
    
    def __init__(self, initial_beliefs: Optional[Dict[str, float]] = None):
        # Default beliefs linked to potential Dreamspace actions
        default_beliefs = {
            "follow_up_now improves outcome": 0.8,
            "wait might resolve things": 0.6,
            "escalate is risky but sometimes needed": 0.5,
            "send_gentle_reminder is safe": 0.7
        }
        
        # Store beliefs as: statement -> {"confidence": float, "fail_count": int}
        self.beliefs: Dict[str, Dict[str, Union[float, int]]] = {}
        beliefs_to_init = initial_beliefs if initial_beliefs is not None else default_beliefs
        
        for statement, confidence in beliefs_to_init.items():
            # Validate initial confidence
            conf = max(0.0, min(1.0, float(confidence)))
            self.beliefs[statement] = {"confidence": conf, "fail_count": 0}
        
        # Configuration for revision
        self.revision_threshold: float = 0.3
        self.max_failures: int = 3
        self.revision_counter: int = 0

    def audit_beliefs(self) -> Dict[str, float]:
        """Returns a dictionary of current belief statements and their confidence levels."""
        return {stmt: data["confidence"] for stmt, data in self.beliefs.items()}

    def reinforce_belief(self, statement: str, amount: float = 0.05):
        """Increases confidence in a belief, optionally resetting failure count."""
        if statement in self.beliefs:
            data = self.beliefs[statement]
            data["confidence"] = round(min(1.0, data["confidence"] + amount), 2)
            # Optional: Reset fail_count on reinforcement
            # data["fail_count"] = 0

    def degrade_belief(self, statement: str, amount: float = 0.1):
        """Decreases confidence in a belief and increments failure count."""
        if statement in self.beliefs:
            data = self.beliefs[statement]
            data["confidence"] = round(max(0.0, data["confidence"] - amount), 2)
            data["fail_count"] += 1

    def revise_beliefs(self) -> List[Tuple[str, str]]:
        """Identifies and revises beliefs that fall below threshold after repeated failures."""
        revised_list = []
        statements_to_revise = []
        
        # Iterate over a copy of keys for safe dictionary modification
        for stmt in list(self.beliefs.keys()):
            if stmt in self.beliefs:  # Check if not already revised in this pass
                data = self.beliefs[stmt]
                if data["confidence"] < self.revision_threshold and data["fail_count"] >= self.max_failures:
                    statements_to_revise.append(stmt)
        
        for old_stmt in statements_to_revise:
            self.revision_counter += 1
            # Create a new revised statement name
            new_stmt = f"[REVISED_{self.revision_counter}] {old_stmt[:50]}..."
            # Remove old belief and add the revised one with reset confidence/fail count
            belief_data = self.beliefs.pop(old_stmt)
            self.beliefs[new_stmt] = {"confidence": 0.6, "fail_count": 0}
            revised_list.append((old_stmt, new_stmt))
        
        return revised_list

    def get_belief(self, statement: str) -> Optional[Dict]:
        """Retrieves the data for a specific belief."""
        return self.beliefs.get(statement)


class DreamspaceSimulator:
    """Simulates potential outcomes of actions to aid decision-making."""
    
    def __init__(self, action_effects: Optional[Dict[str, float]] = None):
        default_action_effects = {
            "follow_up_now": 0.3,
            "wait": 0.1,
            "escalate": -0.2,
            "send_gentle_reminder": 0.2,
            "do_nothing": 0.0
        }
        self.action_templates = action_effects if action_effects is not None else default_action_effects

    def simulate_resonance_projection(self, current_drift: float = 0.0, avg_reinforcement: float = 1.0) -> Tuple[str, float, List[Dict]]:
        """Projects resonance outcomes for available actions based on internal state."""
        projections = []
        
        # Check if action_templates is usable
        if not self.action_templates or not isinstance(self.action_templates, dict):
            # Return default action if templates are invalid
            return "do_nothing", 0.0, []

        # Calculate projections for all actions
        for action, base_effect in self.action_templates.items():
            noise = random.uniform(-0.05, 0.05)
            projection = base_effect + noise
            projections.append({
                "action": action,
                "projected_resonance": round(projection, 3)
            })
        
        # Ensure projections list is not empty before proceeding
        if not projections:
            return "do_nothing", 0.0, []
        
        # --- Action Selection Logic --- #
        positive_projections = [p for p in projections if p["projected_resonance"] >= 0]
        
        if positive_projections:
            # Choose the action with the highest positive projection
            best_choice = max(positive_projections, key=lambda x: x["projected_resonance"])
        else:
            # If all projections are negative, choose the least negative one
            best_choice = max(projections, key=lambda x: x["projected_resonance"])
        
        # Extract results from the chosen projection
        chosen_action = best_choice["action"]
        projected_outcome = best_choice["projected_resonance"]
        
        # Return statement correctly placed at the end of the method
        return chosen_action, projected_outcome, projections

    def learn_from_outcome(self, projected_outcome: float, actual_outcome: float) -> Tuple[str, float]:
        """Compares projected vs actual outcome and generates a feedback signal."""
        alignment = round(actual_outcome - projected_outcome, 3)
        
        # Determine feedback signal based on alignment thresholds
        if alignment > 0.1:
            feedback_signal = "reinforce"
        elif alignment < -0.2:
            feedback_signal = "contradict"
        else:
            feedback_signal = "neutral"
        
        # Return statement correctly placed at the end of the method
        return feedback_signal, alignment 