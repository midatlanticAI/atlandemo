"""
Expert Registry for Wave-based Cognition
Manages and routes queries to appropriate expert modules.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from .base_expert import BaseExpertModule, ExpertResponse


class ExpertRegistry:
    """
    Registry that manages expert modules and routes queries to the most appropriate expert.
    
    Integrates with the Wave engine to provide specialized reasoning capabilities.
    """
    
    def __init__(self):
        self.experts: Dict[str, BaseExpertModule] = {}
        self.query_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, Dict[str, float]] = {}
        
    def register_expert(self, expert: BaseExpertModule):
        """Register a new expert module."""
        self.experts[expert.name] = expert
        self.performance_metrics[expert.name] = {
            'queries_handled': 0,
            'average_confidence': 0.0,
            'average_processing_time': 0.0,
            'success_rate': 0.0
        }
        print(f"✅ Registered expert: {expert.name} (domain: {expert.domain})")
    
    def unregister_expert(self, expert_name: str):
        """Unregister an expert module."""
        if expert_name in self.experts:
            del self.experts[expert_name]
            del self.performance_metrics[expert_name]
            print(f"❌ Unregistered expert: {expert_name}")
        else:
            print(f"⚠️  Expert {expert_name} not found")
    
    def find_best_expert(self, query: str, context: Dict[str, Any] = None) -> Optional[BaseExpertModule]:
        """Find the best expert to handle a given query."""
        if not self.experts:
            return None
        
        expert_scores = []
        
        for name, expert in self.experts.items():
            # Get expert's confidence in handling this query
            confidence = expert.can_handle(query, context)
            
            # Adjust based on performance history
            performance = self.performance_metrics[name]
            performance_factor = (
                performance['success_rate'] * 0.4 +
                performance['average_confidence'] * 0.3 +
                (1.0 - min(1.0, performance['average_processing_time'] / 5.0)) * 0.3
            )
            
            adjusted_score = confidence * (0.7 + 0.3 * performance_factor)
            expert_scores.append((name, expert, adjusted_score))
        
        # Sort by score and return best expert
        expert_scores.sort(key=lambda x: x[2], reverse=True)
        
        if expert_scores[0][2] > 0.3:  # Minimum threshold
            return expert_scores[0][1]
        
        return None
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        """Process a query using the best available expert."""
        start_time = time.time()
        
        # Find the best expert
        best_expert = self.find_best_expert(query, context)
        
        if not best_expert:
            # No expert available - return default response
            return ExpertResponse(
                confidence=0.1,
                reasoning="No expert available to handle this query",
                answer="unknown",
                wave_patterns={},
                metadata={'error': 'no_expert_available'},
                processing_time=time.time() - start_time
            )
        
        # Process with the selected expert
        response = best_expert.process_query(query, context)
        
        # Update performance metrics
        self._update_performance_metrics(best_expert.name, response)
        
        # Log the query
        self._log_query(query, context, best_expert.name, response)
        
        return response
    
    def process_query_with_multiple_experts(self, query: str, context: Dict[str, Any] = None, 
                                          max_experts: int = 3) -> List[ExpertResponse]:
        """Process a query with multiple experts and return all responses."""
        responses = []
        
        # Get top experts
        expert_scores = []
        for name, expert in self.experts.items():
            confidence = expert.can_handle(query, context)
            if confidence > 0.3:
                expert_scores.append((name, expert, confidence))
        
        expert_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Process with top experts
        for i, (name, expert, score) in enumerate(expert_scores[:max_experts]):
            response = expert.process_query(query, context)
            response.metadata['expert_rank'] = i + 1
            response.metadata['expert_score'] = score
            responses.append(response)
            
            # Update metrics
            self._update_performance_metrics(name, response)
        
        return responses
    
    def get_expert_consensus(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        """Get consensus from multiple experts on a query."""
        responses = self.process_query_with_multiple_experts(query, context)
        
        if not responses:
            return ExpertResponse(
                confidence=0.1,
                reasoning="No experts available",
                answer="unknown",
                wave_patterns={},
                metadata={'error': 'no_experts'},
                processing_time=0.0
            )
        
        # Calculate consensus
        answers = [r.answer for r in responses]
        confidences = [r.confidence for r in responses]
        
        # Simple voting for categorical answers
        if all(isinstance(ans, str) for ans in answers):
            from collections import Counter
            vote_counts = Counter(answers)
            most_common = vote_counts.most_common(1)[0]
            consensus_answer = most_common[0]
            consensus_confidence = sum(confidences) / len(confidences)
        else:
            # For non-categorical answers, use highest confidence
            best_response = max(responses, key=lambda r: r.confidence)
            consensus_answer = best_response.answer
            consensus_confidence = best_response.confidence
        
        # Combine wave patterns
        combined_patterns = {}
        for response in responses:
            for pattern, strength in response.wave_patterns.items():
                if pattern in combined_patterns:
                    combined_patterns[pattern] += strength
                else:
                    combined_patterns[pattern] = strength
        
        # Average the combined patterns
        for pattern in combined_patterns:
            combined_patterns[pattern] /= len(responses)
        
        # Generate consensus reasoning
        reasoning_parts = []
        for i, response in enumerate(responses):
            reasoning_parts.append(f"Expert {i+1}: {response.reasoning}")
        
        consensus_reasoning = f"Consensus from {len(responses)} experts: " + " | ".join(reasoning_parts)
        
        return ExpertResponse(
            confidence=consensus_confidence,
            reasoning=consensus_reasoning,
            answer=consensus_answer,
            wave_patterns=combined_patterns,
            metadata={
                'consensus_type': 'multi_expert',
                'num_experts': len(responses),
                'individual_responses': responses
            },
            processing_time=sum(r.processing_time for r in responses)
        )
    
    def _update_performance_metrics(self, expert_name: str, response: ExpertResponse):
        """Update performance metrics for an expert."""
        metrics = self.performance_metrics[expert_name]
        
        # Update query count
        metrics['queries_handled'] += 1
        
        # Update average confidence
        prev_avg_conf = metrics['average_confidence']
        n = metrics['queries_handled']
        metrics['average_confidence'] = (prev_avg_conf * (n-1) + response.confidence) / n
        
        # Update average processing time
        prev_avg_time = metrics['average_processing_time']
        metrics['average_processing_time'] = (prev_avg_time * (n-1) + response.processing_time) / n
        
        # Success rate will be updated when feedback is provided
    
    def _log_query(self, query: str, context: Dict[str, Any], expert_name: str, response: ExpertResponse):
        """Log a query for analysis and debugging."""
        log_entry = {
            'timestamp': time.time(),
            'query': query,
            'context': context,
            'expert_used': expert_name,
            'response': {
                'confidence': response.confidence,
                'answer': response.answer,
                'processing_time': response.processing_time
            }
        }
        
        self.query_history.append(log_entry)
        
        # Keep history manageable
        if len(self.query_history) > 10000:
            self.query_history = self.query_history[-5000:]
    
    def provide_feedback(self, query: str, expected_answer: Any, actual_answer: Any, success: bool):
        """Provide feedback on a query result to improve expert performance."""
        # Find the most recent query matching this one
        for log_entry in reversed(self.query_history):
            if log_entry['query'] == query:
                expert_name = log_entry['expert_used']
                
                # Update expert with feedback
                if expert_name in self.experts:
                    expert = self.experts[expert_name]
                    expert.update_from_feedback(query, expected_answer, actual_answer, success)
                
                # Update success rate
                metrics = self.performance_metrics[expert_name]
                current_success_rate = metrics['success_rate']
                n = metrics['queries_handled']
                
                if n > 0:
                    # Calculate new success rate
                    total_successes = current_success_rate * n
                    if success:
                        total_successes += 1
                    metrics['success_rate'] = total_successes / n
                
                break
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """Get a summary of the expert registry."""
        return {
            'total_experts': len(self.experts),
            'expert_names': list(self.experts.keys()),
            'total_queries_processed': len(self.query_history),
            'performance_metrics': self.performance_metrics,
            'expert_summaries': {name: expert.get_expertise_summary() 
                               for name, expert in self.experts.items()}
        }
    
    def get_expert_recommendations(self, query: str, context: Dict[str, Any] = None) -> List[Tuple[str, float]]:
        """Get recommendations for which experts could handle a query."""
        recommendations = []
        
        for name, expert in self.experts.items():
            confidence = expert.can_handle(query, context)
            if confidence > 0.1:
                recommendations.append((name, confidence))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations
    
    def optimize_expert_thresholds(self):
        """Optimize expert confidence thresholds based on performance."""
        for name, expert in self.experts.items():
            metrics = self.performance_metrics[name]
            
            # Adjust thresholds based on success rate
            if metrics['success_rate'] > 0.9 and metrics['queries_handled'] > 50:
                # High success rate - can be more aggressive
                expert.confidence_threshold = max(0.3, expert.confidence_threshold - 0.05)
            elif metrics['success_rate'] < 0.7 and metrics['queries_handled'] > 20:
                # Low success rate - be more conservative
                expert.confidence_threshold = min(0.9, expert.confidence_threshold + 0.05)
    
    def __str__(self):
        return f"ExpertRegistry({len(self.experts)} experts, {len(self.query_history)} queries processed)"
    
    def __repr__(self):
        return self.__str__() 