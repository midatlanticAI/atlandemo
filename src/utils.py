from typing import List


def _enhanced_vector(phrase: str) -> List[int]:
    """Encodes a phrase into a 4D vector using ASCII sum, length, unique chars, and trigram hash."""
    ascii_sum = sum(ord(c) for c in phrase)
    length = len(phrase)
    unique_chars = len(set(phrase))
    
    # Basic trigram hash (can be improved)
    trigram_sum = sum([ord(phrase[i]) * ord(phrase[i+1]) * ord(phrase[i+2]) 
                      for i in range(len(phrase) - 2)]) % 10000 if len(phrase) > 2 else 0
    
    return [ascii_sum, length, unique_chars, trigram_sum]


# Add other utility functions here if needed in the future 