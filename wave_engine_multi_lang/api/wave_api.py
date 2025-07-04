#!/usr/bin/env python3
"""
Universal Wave Engine - Unified API Interface
High-level API for easy integration across applications
"""

import sys
import os
import json
import time
from typing import List, Dict, Union, Optional, Any
from dataclasses import dataclass

# Add the python module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))
from wave_engine import WaveEngine

@dataclass
class WaveResult:
    """Result object for wave processing operations"""
    symbols: List[str]
    activations: Dict[str, float]
    processing_time: float
    timestamp: float
    metadata: Dict[str, Any]

class UniversalWaveAPI:
    """
    Universal Wave Engine API
    Provides high-level interface for wave-based cognition
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Universal Wave API
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.engine = WaveEngine()
        self.session_id = f"wave_session_{int(time.time())}"
        self.history = []
        
    def process(self, input_data: Union[str, List[str]], 
                return_metadata: bool = True) -> WaveResult:
        """
        Process input through wave interference
        
        Args:
            input_data: String or list of strings to process
            return_metadata: Whether to include processing metadata
            
        Returns:
            WaveResult object with activations and metadata
        """
        start_time = time.time()
        
        # Convert single string to list
        if isinstance(input_data, str):
            symbols = [input_data]
        else:
            symbols = list(input_data)
        
        # Process through wave engine
        activations = self.engine.process(symbols)
        
        processing_time = time.time() - start_time
        
        result = WaveResult(
            symbols=symbols,
            activations=activations,
            processing_time=processing_time,
            timestamp=time.time(),
            metadata={
                'session_id': self.session_id,
                'engine_version': '1.0.0',
                'algorithm': 'wave_interference',
                'performance_class': 'sub_millisecond' if processing_time < 0.001 else 'fast'
            } if return_metadata else {}
        )
        
        # Store in history
        self.history.append(result)
        
        return result
    
    def reason(self, context: List[str], query: str) -> Dict[str, float]:
        """
        Perform reasoning using wave interference
        
        Args:
            context: List of context symbols
            query: Query symbol to reason about
            
        Returns:
            Dictionary of reasoning results
        """
        # Combine context and query
        all_symbols = context + [query]
        result = self.process(all_symbols)
        
        # Extract query activation relative to context
        query_activation = result.activations.get(query, 0.0)
        context_activations = {
            symbol: activation 
            for symbol, activation in result.activations.items() 
            if symbol in context
        }
        
        return {
            'query': query,
            'query_activation': query_activation,
            'context_activations': context_activations,
            'reasoning_confidence': abs(query_activation),
            'processing_time': result.processing_time
        }
    
    def detect_contradictions(self, statements: List[str]) -> Dict[str, Any]:
        """
        Detect contradictions using wave cancellation
        
        Args:
            statements: List of statements to check for contradictions
            
        Returns:
            Dictionary with contradiction analysis
        """
        result = self.process(statements)
        
        # Find opposing activations (likely contradictions)
        activations = list(result.activations.values())
        positive = [a for a in activations if a > 0]
        negative = [a for a in activations if a < 0]
        
        contradiction_score = 0.0
        if positive and negative:
            max_positive = max(positive)
            min_negative = min(negative)
            contradiction_score = abs(max_positive - min_negative)
        
        return {
            'contradiction_detected': contradiction_score > 0.5,
            'contradiction_score': contradiction_score,
            'statement_activations': result.activations,
            'positive_statements': [
                stmt for stmt, act in result.activations.items() if act > 0
            ],
            'negative_statements': [
                stmt for stmt, act in result.activations.items() if act < 0
            ],
            'processing_time': result.processing_time
        }
    
    def predict_patterns(self, sequence: List[str], 
                        predict_next: int = 1) -> Dict[str, Any]:
        """
        Predict patterns using wave propagation
        
        Args:
            sequence: Input sequence
            predict_next: Number of next items to predict
            
        Returns:
            Dictionary with pattern predictions
        """
        # Process sequence to get wave state
        result = self.process(sequence)
        
        # Use wave phases to predict temporal continuation
        predictions = []
        for i in range(predict_next):
            # Simulate temporal evolution
            next_time = result.timestamp + (i + 1) * 0.1
            predicted_activation = self.engine.get_activation(
                f"predicted_{i}", next_time
            )
            predictions.append({
                'prediction_id': i,
                'predicted_activation': predicted_activation,
                'confidence': abs(predicted_activation)
            })
        
        return {
            'sequence': sequence,
            'predictions': predictions,
            'sequence_activations': result.activations,
            'processing_time': result.processing_time
        }
    
    def batch_process(self, batch: List[Union[str, List[str]]]) -> List[WaveResult]:
        """
        Process multiple inputs in batch
        
        Args:
            batch: List of inputs to process
            
        Returns:
            List of WaveResult objects
        """
        results = []
        for item in batch:
            result = self.process(item)
            results.append(result)
        return results
    
    def export_session(self, format: str = 'json') -> str:
        """
        Export session history
        
        Args:
            format: Export format ('json', 'csv')
            
        Returns:
            Serialized session data
        """
        if format == 'json':
            session_data = {
                'session_id': self.session_id,
                'total_operations': len(self.history),
                'history': [
                    {
                        'symbols': result.symbols,
                        'activations': result.activations,
                        'processing_time': result.processing_time,
                        'timestamp': result.timestamp,
                        'metadata': result.metadata
                    }
                    for result in self.history
                ]
            }
            return json.dumps(session_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the session
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.history:
            return {'error': 'No operations performed yet'}
        
        processing_times = [result.processing_time for result in self.history]
        total_symbols = sum(len(result.symbols) for result in self.history)
        
        return {
            'total_operations': len(self.history),
            'total_symbols_processed': total_symbols,
            'avg_processing_time': sum(processing_times) / len(processing_times),
            'min_processing_time': min(processing_times),
            'max_processing_time': max(processing_times),
            'symbols_per_second': total_symbols / sum(processing_times) if sum(processing_times) > 0 else 0,
            'session_duration': time.time() - float(self.session_id.split('_')[-1])
        }

# Convenience functions for quick access
def wave_process(symbols: Union[str, List[str]]) -> Dict[str, float]:
    """Quick wave processing function"""
    api = UniversalWaveAPI()
    result = api.process(symbols)
    return result.activations

def wave_reason(context: List[str], query: str) -> Dict[str, Any]:
    """Quick reasoning function"""
    api = UniversalWaveAPI()
    return api.reason(context, query)

def wave_detect_contradictions(statements: List[str]) -> bool:
    """Quick contradiction detection"""
    api = UniversalWaveAPI()
    result = api.detect_contradictions(statements)
    return result['contradiction_detected']

# Main entry point
def main():
    """Demo the Wave API"""
    print("🌊 Universal Wave Engine API Demo")
    print("=" * 50)
    
    api = UniversalWaveAPI()
    
    # Demo 1: Basic processing
    print("\n1. Basic Processing:")
    result = api.process(["thinking", "mind", "consciousness"])
    print(f"Symbols: {result.symbols}")
    print(f"Activations: {result.activations}")
    print(f"Processing time: {result.processing_time:.6f}s")
    
    # Demo 2: Reasoning
    print("\n2. Reasoning:")
    reasoning = api.reason(["birds", "fly"], "penguins")
    print(f"Query: {reasoning['query']}")
    print(f"Confidence: {reasoning['reasoning_confidence']:.3f}")
    
    # Demo 3: Contradiction detection
    print("\n3. Contradiction Detection:")
    contradictions = api.detect_contradictions(["birds", "fly", "penguins", "cannot"])
    print(f"Contradiction detected: {contradictions['contradiction_detected']}")
    print(f"Score: {contradictions['contradiction_score']:.3f}")
    
    # Demo 4: Performance stats
    print("\n4. Performance Statistics:")
    stats = api.get_performance_stats()
    print(f"Operations: {stats['total_operations']}")
    print(f"Avg time: {stats['avg_processing_time']:.6f}s")
    print(f"Symbols/sec: {stats['symbols_per_second']:.0f}")

if __name__ == "__main__":
    main() 