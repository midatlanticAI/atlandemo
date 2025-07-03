import time
from typing import Dict, Any, Literal


class ReinforcementEngine:
    """
    Controls the strengthening and weakening of symbolic nodes over time.
    Nodes evolve based on experience, repetition, and decay thresholds.
    """

    def __init__(self, decay_threshold: float = 0.2, retention_window: int = 7 * 86400):
        """
        Initialize the reinforcement engine.

        Args:
            decay_threshold: Minimum reinforcement value before considering decay
            retention_window: Time in seconds before inactive nodes are considered for decay
        """
        self.decay_threshold = decay_threshold
        self.retention_window = retention_window  # 7 days by default
        self.op_counts: Dict[str, int] = {
            "strengthen": 0,
            "weaken": 0,
            "decay_check": 0,
            "decay_applied": 0
        }

    def strengthen(self, node: Dict[str, Any], amount: float = 0.1) -> None:
        """
        Increase node reinforcement and update access timestamp.

        Args:
            node: Memory node to strengthen
            amount: Amount to increase reinforcement by
        """
        node["reinforcement"] = round(node["reinforcement"] + amount, 3)
        node["last_accessed"] = time.time()
        self.op_counts["strengthen"] += 1

    def weaken(self, node: Dict[str, Any], amount: float = 0.05) -> None:
        """
        Decrease node reinforcement.

        Args:
            node: Memory node to weaken
            amount: Amount to decrease reinforcement by
        """
        node["reinforcement"] = round(max(0.0, node["reinforcement"] - amount), 3)
        self.op_counts["weaken"] += 1

    def should_decay(self, node: Dict[str, Any]) -> bool:
        """
        Check if a node should be decayed based on reinforcement and last access time.

        Args:
            node: Memory node to check

        Returns:
            True if node should be decayed, False otherwise
        """
        self.op_counts["decay_check"] += 1

        # If no last_accessed timestamp exists, use created_at or current time
        last_access = node.get("last_accessed", node.get("created_at", time.time()))
        time_since_access = time.time() - last_access

        if node["reinforcement"] < self.decay_threshold and time_since_access > self.retention_window:
            return True
        return False

    def apply_decay(self, node: Dict[str, Any], soft: bool = True) -> Literal["retain", "retire"]:
        """
        Apply passive decay to reinforcement.

        Args:
            node: Memory node to apply decay to
            soft: If True, just weaken the node; if False, may trigger retirement

        Returns:
            'retain' if node should be kept, 'retire' if node should be removed
        """
        if self.should_decay(node):
            if soft:
                self.weaken(node, amount=0.05)
                self.op_counts["decay_applied"] += 1
                return "retain"
            else:
                self.op_counts["decay_applied"] += 1
                return "retire"
        return "retain"

    def get_stats(self) -> Dict[str, int]:
        """Return operation statistics."""
        return self.op_counts.copy() 