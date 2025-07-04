"""
Base Expert Module Architecture
Defines the interface for plug-and-play expertise modules in the Wave engine.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time
import numpy as np


@dataclass
class ExpertResponse:
    """Response from an expert module."""
    confidence: float           # 0.0 to 1.0 - how confident the expert is
    reasoning: str             # Natural language explanation of reasoning
    answer: Any                # The actual answer/result
    wave_patterns: Dict[str, float]  # Wave activations this expert generates
    metadata: Dict[str, Any]   # Additional context/debug info
    processing_time: float     # Time taken to process


class BaseExpertModule(ABC):
    """
    Base class for all expert modules that can plug into the Wave engine.
    
    Expert modules provide specialized knowledge and reasoning capabilities
    that integrate with the Wave engine's temporal resonance patterns.
    """
    
    def __init__(self, name: str, domain: str, version: str = "1.0"):
        """Initialize the expert module."""
        self.name = name
        self.domain = domain
        self.version = version
        self.activation_threshold = 0.5
        self.confidence_threshold = 0.7
        self.wave_frequencies = self._define_wave_frequencies()
        self.last_activation_time = 0.0
        self.processing_history = []
        
    @abstractmethod
    def _define_wave_frequencies(self) -> Dict[str, float]:
        """Define the wave frequencies this expert operates on."""
        pass
        
    @abstractmethod
    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        """
        Determine if this expert can handle a given query.
        
        Args:
            query: The question/task to evaluate
            context: Additional context information
            
        Returns:
            Float 0.0-1.0 indicating confidence in handling this query
        """
        pass
        
    @abstractmethod
    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        """
        Process a query using this expert's knowledge.
        
        Args:
            query: The question/task to process
            context: Additional context information
            
        Returns:
            ExpertResponse with the result and reasoning
        """
        pass
        
    def generate_wave_patterns(self, concepts: List[str], strength: float = 1.0) -> Dict[str, float]:
        """
        Generate wave activation patterns for given concepts.
        
        This allows the expert to influence the Wave engine's temporal dynamics.
        """
        patterns = {}
        
        for concept in concepts:
            # Generate frequency based on concept and expert's frequency map
            base_freq = self.wave_frequencies.get(concept, 1.0)
            
            # Create wave activation with proper amplitude and phase
            activation = strength * np.sin(2 * np.pi * base_freq * time.time())
            patterns[concept] = activation
            
        return patterns
        
    def resonance_filter(self, wave_field: Dict[str, float]) -> Dict[str, float]:
        """
        Filter wave field through this expert's resonance patterns.
        
        This allows the expert to amplify or dampen certain wave patterns
        based on its knowledge domain.
        """
        filtered_field = {}
        
        for concept, activation in wave_field.items():
            if concept in self.wave_frequencies:
                # Apply resonance amplification
                expert_freq = self.wave_frequencies[concept]
                resonance_factor = 1.0 + (expert_freq / 10.0)  # Normalize
                filtered_field[concept] = activation * resonance_factor
            else:
                # Pass through unchanged
                filtered_field[concept] = activation
                
        return filtered_field
        
    def update_from_feedback(self, query: str, expected: Any, actual: Any, success: bool):
        """
        Update expert knowledge based on feedback.
        
        This allows the expert to learn and improve over time.
        """
        feedback_entry = {
            'timestamp': time.time(),
            'query': query,
            'expected': expected,
            'actual': actual,
            'success': success
        }
        
        self.processing_history.append(feedback_entry)
        
        # Adjust confidence threshold based on success rate
        if len(self.processing_history) >= 10:
            recent_success = sum(1 for entry in self.processing_history[-10:] if entry['success'])
            success_rate = recent_success / 10.0
            
            if success_rate > 0.8:
                self.confidence_threshold = max(0.5, self.confidence_threshold - 0.05)
            elif success_rate < 0.6:
                self.confidence_threshold = min(0.9, self.confidence_threshold + 0.05)
    
    def get_expertise_summary(self) -> Dict[str, Any]:
        """Get a summary of this expert's capabilities and performance."""
        total_queries = len(self.processing_history)
        if total_queries > 0:
            success_rate = sum(1 for entry in self.processing_history if entry['success']) / total_queries
            avg_processing_time = np.mean([entry.get('processing_time', 0) for entry in self.processing_history])
        else:
            success_rate = 0.0
            avg_processing_time = 0.0
            
        return {
            'name': self.name,
            'domain': self.domain,
            'version': self.version,
            'total_queries_processed': total_queries,
            'success_rate': success_rate,
            'avg_processing_time': avg_processing_time,
            'confidence_threshold': self.confidence_threshold,
            'wave_frequencies': self.wave_frequencies,
            'last_activation': self.last_activation_time
        }
        
    def __str__(self):
        return f"ExpertModule({self.name}, {self.domain}, v{self.version})"
        
    def __repr__(self):
        return self.__str__() 