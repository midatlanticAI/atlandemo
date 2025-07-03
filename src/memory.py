import time
import uuid
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any, Union

# Import modules from our package
from .utils import _enhanced_vector
from .similarity import resonance_score
from .reinforcement import ReinforcementEngine


class SymbolicNode:
    """Represents a basic symbolic memory node with vector and reinforcement."""
    
    def __init__(self, phrase: str, label: str = None):
        self.node_id = str(uuid.uuid4())
        self.phrase = phrase
        self.label = label or "unlabeled"
        self.vector = _enhanced_vector(phrase)
        self.reinforcement = 1.0
        self.created_at = time.time()
        self.last_accessed = self.created_at
        self.metadata = {}

    def reinforce(self, amount: float = 0.1):
        """Increases the reinforcement score of the node."""
        self.reinforcement = round(self.reinforcement + amount, 3)
        self.last_accessed = time.time()

    def weaken(self, amount: float = 0.05):
        """Decreases reinforcement slightly."""
        self.reinforcement = round(max(0.0, self.reinforcement - amount), 3)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the node to a dictionary representation."""
        return {
            "node_id": self.node_id,
            "phrase": self.phrase,
            "label": self.label,
            "vector": self.vector,
            "reinforcement": self.reinforcement,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "metadata": self.metadata
        }

    def __repr__(self) -> str:
        return f"<SymbolicNode '{self.phrase[:20]}...' Vec:{self.vector} Reinf:{self.reinforcement:.2f}>"


class RCoreMemoryIndex:
    """Indexed memory store for fast symbolic retrieval and management."""
    
    def __init__(self, max_memory_size: int = 1000, config: Optional[Dict[str, Any]] = None):
        # Core storage
        self.memory: List[Dict] = []  # Stores node data as dictionaries
        self.index: Dict[int, List[int]] = defaultdict(list)  # hash -> list of memory indices
        
        # Configuration
        self.config = config or {}
        self.max_memory_size = max_memory_size
        
        # Performance optimization
        self.cache_last_vector: Optional[List[int]] = None
        self.cache_last_results: List[Tuple[int, float]] = []
        self.op_counts: Dict[str, int] = defaultdict(int)
        
        # Helper components
        self.reinforcer = ReinforcementEngine(
            decay_threshold=self.config.get('decay_threshold', 0.2),
            retention_window=self.config.get('retention_window', 7 * 86400)
        )

    def _vector_hash(self, vector: List[int]) -> int:
        """Calculates a simple hash for a vector."""
        # Using a prime modulus might improve distribution
        return sum((v * (i + 1)) for i, v in enumerate(vector)) % 10007

    def add(self, phrase: str, vector: Optional[List[int]] = None, label: Optional[str] = None) -> int:
        """
        Adds a new node to memory and updates the index.

        Args:
            phrase: The text content of the node
            vector: Optional pre-computed vector (will calculate if None)
            label: Optional category label for the node

        Returns:
            Index of the newly added node
        """
        if vector is None:
            vector = _enhanced_vector(phrase)

        node = {
            "node_id": str(uuid.uuid4()),
            "phrase": phrase,
            "vector": vector,
            "label": label or "generic",
            "reinforcement": 1.0,
            "access_count": 0,
            "created_at": time.time(),
            "last_accessed": time.time(),
            "metadata": {}
        }

        # Check if we need to prune memory before adding
        if len(self.memory) >= self.max_memory_size:
            self._prune_memory()

        node_id = len(self.memory)
        self.memory.append(node)
        self.index[self._vector_hash(vector)].append(node_id)
        self.op_counts['add'] += 1
        return node_id

    def search(self, vector: List[int], top_k: int = 1) -> List[Tuple[int, float]]:
        """
        Searches the index for nodes matching the vector, returning top_k (index, score) tuples.

        Args:
            vector: Vector to search for
            top_k: Number of top matches to return

        Returns:
            List of (index, score) tuples for the top matches
        """
        # Check cache first
        if self.cache_last_vector == vector:
            self.op_counts['search_cache_hit'] += 1
            return self.cache_last_results

        self.op_counts['search'] += 1
        candidates = []
        vector_key = self._vector_hash(vector)
        candidate_indices = self.index.get(vector_key, [])
        self.op_counts['search_candidates_found'] += len(candidate_indices)

        resonance_calculations = 0
        for idx in candidate_indices:
            # Check if index is still valid (e.g., after pruning)
            if idx < len(self.memory):
                node = self.memory[idx]
                score = resonance_score(
                    node["vector"],
                    vector,
                    reinforcement_value=node["reinforcement"],
                    reinforcement_weight=self.config.get('reinforcement_weight', 0.05)
                )
                resonance_calculations += 1
                candidates.append((idx, score))

        self.op_counts['search_resonance_calcs'] += resonance_calculations
        # Sort by score (descending), then index (ascending) as tie-breaker
        sorted_hits = sorted(candidates, key=lambda x: (-x[1], x[0]))[:top_k]

        # Update access count for retrieved nodes
        for idx, _ in sorted_hits:
            if idx < len(self.memory):
                self.memory[idx]["access_count"] += 1
                self.memory[idx]["last_accessed"] = time.time()
                self.op_counts['search_node_accessed'] += 1

        # Update cache
        self.cache_last_vector = vector
        self.cache_last_results = sorted_hits
        return sorted_hits

    def reinforce_by_index(self, node_index: int, amount: float = 0.1) -> bool:
        """
        Directly reinforces a node by its index in the memory list.

        Args:
            node_index: Index of the node to reinforce
            amount: Amount to increase reinforcement by

        Returns:
            True if reinforcement was successful, False otherwise
        """
        if 0 <= node_index < len(self.memory):
            node = self.memory[node_index]
            self.reinforcer.strengthen(node, amount)
            self.op_counts['reinforce'] += 1
            return True
        return False

    def get_node(self, node_index: int) -> Optional[Dict[str, Any]]:
        """
        Get a node by its index.

        Args:
            node_index: Index of the node to retrieve

        Returns:
            Node dictionary or None if index is invalid
        """
        if 0 <= node_index < len(self.memory):
            return self.memory[node_index]
        return None

    def _prune_memory(self) -> int:
        """
        Removes low-reinforcement nodes when memory hits capacity.

        Returns:
            Number of nodes removed
        """
        if not self.memory:
            return 0

        # Find candidates for removal (low reinforcement and old access time)
        to_remove = []
        for idx, node in enumerate(self.memory):
            if self.reinforcer.should_decay(node):
                to_remove.append((idx, node["reinforcement"], node["last_accessed"]))

        # Sort candidates by reinforcement (ascending) and last accessed (ascending)
        to_remove.sort(key=lambda x: (x[1], x[2]))

        # Remove up to 10% of memory or at least 1 node
        removal_count = max(1, int(len(self.memory) * 0.1))
        removed = 0

        # Only proceed if we have candidates
        if to_remove:
            # Get indices to remove (in descending order to avoid index shifting issues)
            indices_to_remove = sorted([x[0] for x in to_remove[:removal_count]], reverse=True)
            
            # Remove nodes
            for idx in indices_to_remove:
                del self.memory[idx]
                removed += 1

            # Rebuild index after pruning
            self._rebuild_index()

        self.op_counts['pruned'] = self.op_counts.get('pruned', 0) + removed
        return removed

    def _rebuild_index(self) -> None:
        """Rebuilds the entire index after pruning."""
        self.index = defaultdict(list)
        for idx, node in enumerate(self.memory):
            self.index[self._vector_hash(node["vector"])].append(idx)
        self.op_counts['index_rebuild'] = self.op_counts.get('index_rebuild', 0) + 1

    def get_stats(self) -> Dict[str, int]:
        """Returns a dictionary of operation counts."""
        stats = {
            "memory_size": len(self.memory),
            "adds": self.op_counts.get('add', 0),
            "searches": self.op_counts.get('search', 0),
            "reinforcements": self.op_counts.get('reinforce', 0),
            "search_cache_hits": self.op_counts.get('search_cache_hit', 0),
            "search_candidates_found": self.op_counts.get('search_candidates_found', 0),
            "search_resonance_calcs": self.op_counts.get('search_resonance_calcs', 0),
            "search_nodes_accessed": self.op_counts.get('search_node_accessed', 0),
            "index_rebuilds": self.op_counts.get('index_rebuild', 0),
            "nodes_pruned": self.op_counts.get('pruned', 0)
        }
        # Add reinforcement stats
        stats.update({f"reinforcer_{k}": v for k, v in self.reinforcer.get_stats().items()})
        return stats 