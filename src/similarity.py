import math
from typing import List


def cosine_similarity(v1: List[int], v2: List[int]) -> float:
    """
    Measures directional similarity between two vectors.
    Values closer to 1 mean high structural alignment.
    """
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def euclidean_distance(v1: List[int], v2: List[int]) -> float:
    """
    Measures magnitude closeness (proximity).
    Lower values mean more similarity.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def resonance_score(v1: List[int], v2: List[int], reinforcement_weight: float = 0.05, reinforcement_value: float = 1.0) -> float:
    """
    Computes a composite symbolic resonance score using both cosine and Euclidean.
    Can be used to match input against symbolic memory nodes.
    """
    cos_sim = cosine_similarity(v1, v2)
    euc_dist = euclidean_distance(v1, v2)
    return round(cos_sim - (0.1 * euc_dist) + reinforcement_weight * reinforcement_value, 4) 