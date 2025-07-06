"""
Enhanced Wave Engine with Expert Module Integration
Combines the temporal cognition engine with plug-and-play expert modules.
"""

import time
from typing import Dict, List, Any, Optional
from src.temporal_cognition import TemporalCognitionEngine, ExperienceFrame
from expert_modules.registry import ExpertRegistry
from expert_modules.logic_expert import LogicExpertModule
from expert_modules.base_expert import ExpertResponse


class EnhancedWaveEngine:
    """
    Enhanced Wave engine that combines temporal cognition with expert modules.
    
    This engine provides:
    - Core Wave-based temporal cognition
    - Plug-and-play expert modules for specialized reasoning
    - Seamless integration between Wave dynamics and expert knowledge
    """
    
    def __init__(self):
        # Initialize core Wave engine
        self.wave_engine = TemporalCognitionEngine()
        
        # Initialize expert registry
        self.expert_registry = ExpertRegistry()
        
        # Register default experts
        self._register_default_experts()
        
        # Integration parameters
        self.expert_wave_integration_strength = 0.7
        self.wave_expert_feedback_strength = 0.5
        
        # Performance tracking
        self.query_count = 0
        self.total_processing_time = 0.0
        self.wave_expert_synergy_scores = []
        
    def _register_default_experts(self):
        """Register default expert modules."""
        # Register Logic Expert for LogicBench
        logic_expert = LogicExpertModule()
        self.expert_registry.register_expert(logic_expert)
        
        # Register Math Expert for mathematical reasoning
        from expert_modules.math_expert import MathExpertModule
        math_expert = MathExpertModule()
        self.expert_registry.register_expert(math_expert)
        
        print("[BRAIN] Enhanced Wave Engine initialized with expert modules")
        print(f"   [+] {len(self.expert_registry.experts)} experts registered")
    
    def process_query(self, query: str, context: Dict[str, Any] = None, 
                     use_wave_cognition: bool = True, 
                     use_expert_modules: bool = True) -> Dict[str, Any]:
        """
        Process a query using both Wave cognition and expert modules.
        
        Args:
            query: The question/task to process
            context: Additional context information
            use_wave_cognition: Whether to use Wave-based temporal cognition
            use_expert_modules: Whether to use expert modules
            
        Returns:
            Complete processing result with both Wave and expert insights
        """
        start_time = time.time()
        self.query_count += 1
        
        result = {
            'query': query,
            'context': context,
            'timestamp': start_time,
            'wave_response': None,
            'expert_response': None,
            'integrated_response': None,
            'processing_time': 0.0,
            'synergy_score': 0.0
        }
        
        # Step 1: Wave-based temporal cognition
        if use_wave_cognition:
            wave_response = self._process_with_wave_cognition(query, context)
            result['wave_response'] = wave_response
        
        # Step 2: Expert module processing
        if use_expert_modules:
            expert_response = self.expert_registry.process_query(query, context)
            result['expert_response'] = expert_response
        
        # Step 3: Integrate Wave and Expert responses
        if use_wave_cognition and use_expert_modules and result['wave_response'] and result['expert_response']:
            integrated_response = self._integrate_wave_expert_responses(
                result['wave_response'], result['expert_response']
            )
            result['integrated_response'] = integrated_response
            
            # Calculate synergy score
            synergy_score = self._calculate_synergy_score(
                result['wave_response'], result['expert_response'], integrated_response
            )
            result['synergy_score'] = synergy_score
            self.wave_expert_synergy_scores.append(synergy_score)
        
        # Final response selection
        result['final_answer'] = self._select_final_answer(result)
        
        # Update performance metrics
        processing_time = time.time() - start_time
        result['processing_time'] = processing_time
        self.total_processing_time += processing_time
        
        return result
    
    def _process_with_wave_cognition(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process query using Wave-based temporal cognition."""
        # Convert query and context to Wave experience
        visual_symbols = self._extract_visual_symbols(query, context)
        auditory_symbols = self._extract_auditory_symbols(query, context)
        goals = self._extract_goals(query, context)
        
        # Process through Wave engine
        wave_result = self.wave_engine.live_experience(
            visual=visual_symbols,
            auditory=auditory_symbols,
            goals=goals,
            mood=0.0,
            arousal=0.7,
            attention=0.9,
            satisfaction=0.5
        )
        
        # Generate Wave-based answer
        wave_answer = self._generate_wave_answer(wave_result, query, context)
        
        return {
            'activation_field': wave_result['activation_field'],
            'resonance_patterns': wave_result['recent_resonance'],
            'wave_answer': wave_answer,
            'confidence': self._calculate_wave_confidence(wave_result),
            'reasoning': self._generate_wave_reasoning(wave_result, query)
        }
    
    def _extract_visual_symbols(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        """Extract visual symbols from query and context."""
        symbols = []
        
        # Extract key words from query
        words = query.lower().split()
        symbols.extend([word for word in words if len(word) > 2])
        
        # Extract from context
        if context:
            if 'context' in context:
                context_words = context['context'].lower().split()
                symbols.extend([word for word in context_words if len(word) > 2])
            
            if 'type' in context:
                symbols.append(context['type'])
            
            if 'axiom' in context:
                symbols.append(context['axiom'])
        
        return list(set(symbols))
    
    def _extract_auditory_symbols(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        """Extract auditory symbols (question type indicators)."""
        symbols = ['question']
        
        # Add question type indicators
        if '?' in query:
            symbols.append('inquiry')
        
        if any(word in query.lower() for word in ['does', 'is', 'are', 'will', 'can']):
            symbols.append('verification')
        
        if any(word in query.lower() for word in ['entail', 'imply', 'mean']):
            symbols.append('logical_inference')
        
        return symbols
    
    def _extract_goals(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        """Extract goals from query."""
        goals = ['answer', 'reason']
        
        # Add domain-specific goals
        if context and context.get('type') in ['propositional_logic', 'first_order_logic', 'nm_logic']:
            goals.append('logical_reasoning')
        
        return goals
    
    def _generate_wave_answer(self, wave_result: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> str:
        """Generate answer based on Wave activation patterns."""
        activation_field = wave_result['activation_field']
        
        # Look for strong positive or negative activations
        positive_activations = {k: v for k, v in activation_field.items() if v > 0.5}
        negative_activations = {k: v for k, v in activation_field.items() if v < -0.5}
        
        # Simple heuristic for yes/no questions
        if context and any('answer' in qa.get('question', '').lower() for qa in context.get('qa_pairs', [])):
            if len(positive_activations) > len(negative_activations):
                return "yes"
            else:
                return "no"
        
        # For other questions, return most activated concept
        if activation_field:
            max_activation = max(activation_field.items(), key=lambda x: abs(x[1]))
            return max_activation[0]
        
        return "unknown"
    
    def _calculate_wave_confidence(self, wave_result: Dict[str, Any]) -> float:
        """Calculate confidence based on Wave activation strength."""
        activation_field = wave_result['activation_field']
        
        if not activation_field:
            return 0.1
        
        # Calculate confidence based on activation strength
        activations = list(activation_field.values())
        max_activation = max(abs(a) for a in activations)
        avg_activation = sum(abs(a) for a in activations) / len(activations)
        
        # Normalize confidence
        confidence = min(1.0, (max_activation + avg_activation) / 2.0)
        return max(0.1, confidence)
    
    def _generate_wave_reasoning(self, wave_result: Dict[str, Any], query: str) -> str:
        """Generate reasoning explanation based on Wave patterns."""
        activation_field = wave_result['activation_field']
        resonance_patterns = wave_result['recent_resonance']
        
        reasoning_parts = []
        
        # Explain strongest activations
        if activation_field:
            strong_activations = {k: v for k, v in activation_field.items() if abs(v) > 0.5}
            if strong_activations:
                reasoning_parts.append(f"Strong Wave activations: {list(strong_activations.keys())}")
        
        # Explain resonance patterns
        if resonance_patterns:
            reasoning_parts.append(f"Resonance patterns detected: {len(resonance_patterns)}")
        
        reasoning_parts.append("Wave-based temporal cognition applied")
        
        return " | ".join(reasoning_parts)
    
    def _integrate_wave_expert_responses(self, wave_response: Dict[str, Any], 
                                       expert_response: ExpertResponse) -> Dict[str, Any]:
        """Integrate Wave and Expert responses into a unified response."""
        # Weight responses based on confidence
        wave_confidence = wave_response['confidence']
        expert_confidence = expert_response.confidence
        
        total_confidence = wave_confidence + expert_confidence
        if total_confidence > 0:
            wave_weight = wave_confidence / total_confidence
            expert_weight = expert_confidence / total_confidence
        else:
            wave_weight = expert_weight = 0.5
        
        # Integrate answers
        integrated_answer = self._integrate_answers(
            wave_response['wave_answer'], expert_response.answer,
            wave_weight, expert_weight
        )
        
        # Combine wave patterns
        combined_patterns = dict(wave_response['activation_field'])
        for pattern, strength in expert_response.wave_patterns.items():
            if pattern in combined_patterns:
                combined_patterns[pattern] = (combined_patterns[pattern] + strength) / 2
            else:
                combined_patterns[pattern] = strength
        
        # Integrate confidence
        integrated_confidence = wave_confidence * wave_weight + expert_confidence * expert_weight
        
        # Combine reasoning
        integrated_reasoning = (
            f"Wave reasoning: {wave_response['reasoning']} | "
            f"Expert reasoning: {expert_response.reasoning}"
        )
        
        return {
            'answer': integrated_answer,
            'confidence': integrated_confidence,
            'reasoning': integrated_reasoning,
            'wave_patterns': combined_patterns,
            'wave_weight': wave_weight,
            'expert_weight': expert_weight,
            'integration_method': 'weighted_confidence'
        }
    
    def _integrate_answers(self, wave_answer: str, expert_answer: str, 
                          wave_weight: float, expert_weight: float) -> str:
        """Integrate answers from Wave and Expert responses."""
        # For categorical answers (yes/no), use weighted voting
        if wave_answer in ['yes', 'no'] and expert_answer in ['yes', 'no']:
            if wave_answer == expert_answer:
                return wave_answer  # Agreement
            else:
                # Disagreement - use higher weight
                return wave_answer if wave_weight > expert_weight else expert_answer
        
        # For other answers, prefer expert if confidence is high
        if expert_weight > 0.7:
            return expert_answer
        elif wave_weight > 0.7:
            return wave_answer
        else:
            return expert_answer  # Default to expert
    
    def _calculate_synergy_score(self, wave_response: Dict[str, Any], 
                               expert_response: ExpertResponse, 
                               integrated_response: Dict[str, Any]) -> float:
        """Calculate synergy score between Wave and Expert responses."""
        synergy_factors = []
        
        # Agreement factor
        if wave_response['wave_answer'] == expert_response.answer:
            synergy_factors.append(0.5)  # Strong agreement
        else:
            synergy_factors.append(0.1)  # Disagreement
        
        # Confidence correlation
        conf_correlation = min(wave_response['confidence'], expert_response.confidence)
        synergy_factors.append(conf_correlation * 0.3)
        
        # Wave pattern integration
        wave_patterns = set(wave_response['activation_field'].keys())
        expert_patterns = set(expert_response.wave_patterns.keys())
        pattern_overlap = len(wave_patterns.intersection(expert_patterns))
        if wave_patterns or expert_patterns:
            pattern_synergy = pattern_overlap / len(wave_patterns.union(expert_patterns))
            synergy_factors.append(pattern_synergy * 0.2)
        
        return sum(synergy_factors)
    
    def _select_final_answer(self, result: Dict[str, Any]) -> str:
        """Select the final answer from available responses."""
        # Prefer integrated response if available
        if result['integrated_response']:
            return result['integrated_response']['answer']
        
        # Fall back to expert response
        if result['expert_response']:
            return result['expert_response'].answer
        
        # Fall back to wave response
        if result['wave_response']:
            return result['wave_response']['wave_answer']
        
        return "unknown"
    
    def register_expert(self, expert):
        """Register a new expert module."""
        self.expert_registry.register_expert(expert)
    
    def provide_feedback(self, query: str, expected_answer: str, actual_answer: str, success: bool):
        """Provide feedback to improve performance."""
        self.expert_registry.provide_feedback(query, expected_answer, actual_answer, success)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary of the enhanced engine."""
        avg_processing_time = self.total_processing_time / max(1, self.query_count)
        avg_synergy_score = sum(self.wave_expert_synergy_scores) / max(1, len(self.wave_expert_synergy_scores))
        
        return {
            'queries_processed': self.query_count,
            'average_processing_time': avg_processing_time,
            'average_synergy_score': avg_synergy_score,
            'expert_registry_summary': self.expert_registry.get_registry_summary(),
            'wave_engine_state': self.wave_engine.get_cognitive_state()
        }
    
    def optimize_performance(self):
        """Optimize performance based on feedback."""
        # Optimize expert thresholds
        self.expert_registry.optimize_expert_thresholds()
        
        # Adjust integration parameters based on synergy scores
        if self.wave_expert_synergy_scores:
            avg_synergy = sum(self.wave_expert_synergy_scores) / len(self.wave_expert_synergy_scores)
            
            if avg_synergy > 0.8:
                # High synergy - increase integration strength
                self.expert_wave_integration_strength = min(1.0, self.expert_wave_integration_strength + 0.05)
            elif avg_synergy < 0.4:
                # Low synergy - decrease integration strength
                self.expert_wave_integration_strength = max(0.3, self.expert_wave_integration_strength - 0.05)
    
    def __str__(self):
        return f"EnhancedWaveEngine(experts: {len(self.expert_registry.experts)}, queries: {self.query_count})"
    
    def __repr__(self):
        return self.__str__() 