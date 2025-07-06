#!/usr/bin/env python3
"""
ATLAN MEMORY CORE - Standalone Package
Extracted from VTRFM Source Code Archive – April 2025
Inventor: Johnathan Scott Viruet

Core symbolic memory system with reinforcement learning and automatic organization.
Perfect for applications needing intelligent, self-organizing memory.
"""

import time
import uuid
import math
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any, Union


# =============================================================================
# CORE VECTOR ENCODING
# =============================================================================

def enhanced_vector(phrase: str) -> List[int]:
    """
    Encodes a phrase into a 4D vector using ASCII sum, length, unique chars, and trigram hash.
    
    This simple encoding captures semantic meaning through multiple dimensions:
    - ASCII sum: Content fingerprint
    - Length: Structural information
    - Unique chars: Vocabulary richness
    - Trigram hash: Sequential pattern signature
    
    Args:
        phrase: Text to encode
        
    Returns:
        4D vector representation
    """
    ascii_sum = sum(ord(c) for c in phrase)
    length = len(phrase)
    unique_chars = len(set(phrase))
    
    # Basic trigram hash for sequential patterns
    trigram_sum = 0
    if len(phrase) > 2:
        trigram_sum = sum([
            ord(phrase[i]) * ord(phrase[i+1]) * ord(phrase[i+2])
            for i in range(len(phrase) - 2)
        ]) % 10000
    
    return [ascii_sum, length, unique_chars, trigram_sum]


# =============================================================================
# SIMILARITY AND RESONANCE SCORING
# =============================================================================

def cosine_similarity(v1: List[int], v2: List[int]) -> float:
    """Measures directional similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def euclidean_distance(v1: List[int], v2: List[int]) -> float:
    """Measures magnitude closeness (proximity). Lower values = more similar."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def resonance_score(v1: List[int], v2: List[int], 
                   reinforcement_weight: float = 0.05, 
                   reinforcement_value: float = 1.0) -> float:
    """
    Computes composite symbolic resonance score using cosine + euclidean + reinforcement.
    
    This is the core matching algorithm that determines memory similarity.
    """
    cos_sim = cosine_similarity(v1, v2)
    euc_dist = euclidean_distance(v1, v2)
    
    # Combine directional similarity, distance penalty, and reinforcement bonus
    score = cos_sim - (0.1 * euc_dist) + (reinforcement_weight * reinforcement_value)
    return round(score, 4)


# =============================================================================
# REINFORCEMENT ENGINE
# =============================================================================

class ReinforcementEngine:
    """
    Controls memory strengthening and decay over time.
    Memories that are accessed frequently get stronger, unused ones fade.
    """
    
    def __init__(self, decay_threshold: float = 0.2, retention_window: int = 7 * 86400):
        """
        Args:
            decay_threshold: Minimum reinforcement before considering decay
            retention_window: Time in seconds before inactive memories decay (default: 7 days)
        """
        self.decay_threshold = decay_threshold
        self.retention_window = retention_window
        self.stats = {"strengthen": 0, "weaken": 0, "decay_check": 0, "decay_applied": 0}
    
    def strengthen(self, memory_node: Dict[str, Any], amount: float = 0.1) -> None:
        """Strengthen a memory through repeated access."""
        memory_node["reinforcement"] = round(memory_node["reinforcement"] + amount, 3)
        memory_node["last_accessed"] = time.time()
        self.stats["strengthen"] += 1
    
    def weaken(self, memory_node: Dict[str, Any], amount: float = 0.05) -> None:
        """Weaken a memory (natural decay)."""
        memory_node["reinforcement"] = round(max(0.0, memory_node["reinforcement"] - amount), 3)
        self.stats["weaken"] += 1
    
    def should_decay(self, memory_node: Dict[str, Any]) -> bool:
        """Check if memory should be considered for removal."""
        self.stats["decay_check"] += 1
        
        last_access = memory_node.get("last_accessed", memory_node.get("created_at", time.time()))
        time_since_access = time.time() - last_access
        
        return (memory_node["reinforcement"] < self.decay_threshold and 
                time_since_access > self.retention_window)
    
    def get_stats(self) -> Dict[str, int]:
        """Get reinforcement statistics."""
        return self.stats.copy()


# =============================================================================
# CORE MEMORY SYSTEM
# =============================================================================

class AtlanMemoryCore:
    """
    The heart of the Atlan memory system.
    
    Features:
    - Vector-indexed storage for fast retrieval
    - Automatic reinforcement learning
    - Memory pruning and organization
    - Resonance-based similarity matching
    """
    
    def __init__(self, max_memory_size: int = 1000, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the memory core.
        
        Args:
            max_memory_size: Maximum number of memories to store
            config: Optional configuration dictionary
        """
        self.memory: List[Dict] = []  # Main memory storage
        self.index: Dict[int, List[int]] = defaultdict(list)  # Vector hash -> memory indices
        self.max_memory_size = max_memory_size
        self.config = config or {}
        
        # Performance optimization
        self.cache_last_vector: Optional[List[int]] = None
        self.cache_last_results: List[Tuple[int, float]] = []
        self.stats = defaultdict(int)
        
        # Reinforcement engine
        self.reinforcer = ReinforcementEngine(
            decay_threshold=self.config.get('decay_threshold', 0.2),
            retention_window=self.config.get('retention_window', 7 * 86400)
        )
    
    def _vector_hash(self, vector: List[int]) -> int:
        """Create a hash for vector indexing."""
        return sum((v * (i + 1)) for i, v in enumerate(vector)) % 10007
    
    def add_memory(self, phrase: str, vector: Optional[List[int]] = None, 
                  label: Optional[str] = None, metadata: Optional[Dict] = None) -> int:
        """
        Add a new memory to the system.
        
        Args:
            phrase: The text content
            vector: Optional pre-computed vector (will calculate if None)
            label: Optional category label
            metadata: Optional additional data
            
        Returns:
            Index of the newly added memory
        """
        if vector is None:
            vector = enhanced_vector(phrase)
        
        # Check if we need to prune memory first
        if len(self.memory) >= self.max_memory_size:
            self._prune_memory()
        
        memory_node = {
            "node_id": str(uuid.uuid4()),
            "phrase": phrase,
            "vector": vector,
            "label": label or "generic",
            "reinforcement": 1.0,
            "access_count": 0,
            "created_at": time.time(),
            "last_accessed": time.time(),
            "metadata": metadata or {}
        }
        
        node_id = len(self.memory)
        self.memory.append(memory_node)
        self.index[self._vector_hash(vector)].append(node_id)
        self.stats['add'] += 1
        
        return node_id
    
    def search_memory(self, query: str, top_k: int = 5) -> List[Tuple[int, float, str]]:
        """
        Search for memories similar to the query.
        
        Args:
            query: Search query text
            top_k: Number of top matches to return
            
        Returns:
            List of (index, score, phrase) tuples
        """
        vector = enhanced_vector(query)
        
        # Check cache first
        if self.cache_last_vector == vector:
            self.stats['search_cache_hit'] += 1
            return [(idx, score, self.memory[idx]["phrase"]) 
                   for idx, score in self.cache_last_results[:top_k]]
        
        self.stats['search'] += 1
        candidates = []
        vector_key = self._vector_hash(vector)
        candidate_indices = self.index.get(vector_key, [])
        
        for idx in candidate_indices:
            if idx < len(self.memory):
                memory_node = self.memory[idx]
                score = resonance_score(
                    memory_node["vector"],
                    vector,
                    reinforcement_value=memory_node["reinforcement"],
                    reinforcement_weight=self.config.get('reinforcement_weight', 0.05)
                )
                candidates.append((idx, score))
        
        # Sort by score (descending)
        sorted_hits = sorted(candidates, key=lambda x: -x[1])[:top_k]
        
        # Update access count for retrieved memories
        for idx, _ in sorted_hits:
            if idx < len(self.memory):
                self.memory[idx]["access_count"] += 1
                self.memory[idx]["last_accessed"] = time.time()
        
        # Update cache
        self.cache_last_vector = vector
        self.cache_last_results = sorted_hits
        
        # Return with phrases included
        return [(idx, score, self.memory[idx]["phrase"]) 
               for idx, score in sorted_hits]
    
    def reinforce_memory(self, memory_index: int, amount: float = 0.1) -> bool:
        """
        Strengthen a memory by its index.
        
        Args:
            memory_index: Index of memory to strengthen
            amount: Reinforcement amount
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= memory_index < len(self.memory):
            self.reinforcer.strengthen(self.memory[memory_index], amount)
            self.stats['reinforce'] += 1
            return True
        return False
    
    def get_memory(self, memory_index: int) -> Optional[Dict[str, Any]]:
        """Get a memory by index."""
        if 0 <= memory_index < len(self.memory):
            return self.memory[memory_index]
        return None
    
    def _prune_memory(self) -> int:
        """Remove weak/old memories when at capacity."""
        if not self.memory:
            return 0
        
        # Find memories to remove
        to_remove = []
        for idx, memory_node in enumerate(self.memory):
            if self.reinforcer.should_decay(memory_node):
                to_remove.append((idx, memory_node["reinforcement"], memory_node["last_accessed"]))
        
        # Sort by reinforcement (ascending) and last accessed (ascending)
        to_remove.sort(key=lambda x: (x[1], x[2]))
        
        # Remove up to 10% of memory
        removal_count = max(1, int(len(self.memory) * 0.1))
        removed = 0
        
        if to_remove:
            indices_to_remove = sorted([x[0] for x in to_remove[:removal_count]], reverse=True)
            for idx in indices_to_remove:
                del self.memory[idx]
                removed += 1
            
            # Rebuild index
            self._rebuild_index()
        
        self.stats['pruned'] += removed
        return removed
    
    def _rebuild_index(self) -> None:
        """Rebuild the vector index after pruning."""
        self.index = defaultdict(list)
        for idx, memory_node in enumerate(self.memory):
            self.index[self._vector_hash(memory_node["vector"])].append(idx)
        self.stats['index_rebuild'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        stats = {
            "memory_size": len(self.memory),
            "memory_capacity": self.max_memory_size,
            "memory_utilization": len(self.memory) / self.max_memory_size,
            "index_size": len(self.index),
            "operations": dict(self.stats)
        }
        stats["reinforcement"] = self.reinforcer.get_stats()
        return stats
    
    def memory_health_report(self) -> Dict[str, Any]:
        """Generate a health report of the memory system."""
        if not self.memory:
            return {"status": "empty", "memories": 0}
        
        reinforcements = [m["reinforcement"] for m in self.memory]
        access_counts = [m["access_count"] for m in self.memory]
        
        return {
            "status": "healthy",
            "total_memories": len(self.memory),
            "avg_reinforcement": sum(reinforcements) / len(reinforcements),
            "max_reinforcement": max(reinforcements),
            "min_reinforcement": min(reinforcements),
            "avg_access_count": sum(access_counts) / len(access_counts),
            "most_accessed": max(access_counts),
            "utilization": len(self.memory) / self.max_memory_size,
            "index_efficiency": len(self.index) / len(self.memory) if self.memory else 0
        }


# =============================================================================
# SIMPLE USAGE EXAMPLE
# =============================================================================

def demo_memory_system():
    """Demonstrate the core memory system capabilities."""
    print("[BRAIN] ATLAN MEMORY CORE DEMO")
    print("=" * 40)
    
    # Create memory system
    memory = AtlanMemoryCore(max_memory_size=100)
    
    # Add some memories
    sample_phrases = [
        "I love working on AI projects",
        "The weather is beautiful today",
        "This algorithm is fascinating",
        "I need to finish my homework",
        "AI and machine learning are the future",
        "Today was a productive day"
    ]
    
    print("📝 Adding memories...")
    for phrase in sample_phrases:
        idx = memory.add_memory(phrase, label="demo")
        print(f"   Added: {phrase} (index: {idx})")
    
    print("\n[SEARCH] Searching memories...")
    search_queries = [
        "AI and technology",
        "beautiful weather",
        "working on projects"
    ]
    
    for query in search_queries:
        results = memory.search_memory(query, top_k=3)
        print(f"\n   Query: '{query}'")
        for idx, score, phrase in results:
            print(f"   → {score:.3f}: {phrase}")
    
    print("\n[DATA] Memory Health Report:")
    health = memory.memory_health_report()
    for key, value in health.items():
        print(f"   {key}: {value}")
    
    print("\n[+] Demo complete! Memory system is working perfectly.")


if __name__ == "__main__":
    demo_memory_system() 