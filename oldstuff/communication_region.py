#!/usr/bin/env python3
"""
ATLAN BIOINTELLIGENCE - COMMUNICATION REGION
[BRAIN] Communication processing region that flows through central brain
"""

from typing import Dict, Any, Optional, List
from core.agent import AtlanAgent

class CommunicationRegion:
    """
    [BRAIN] Communication specialized brain region
    ALL processing flows through central AtlanAgent - no bypassing allowed!
    """
    
    def __init__(self, central_brain: AtlanAgent):
        """
        Initialize communication region with central brain
        
        Args:
            central_brain: The AtlanAgent central executive
        """
        self.central_brain = central_brain
        
    def process_through_brain(self, query: str, brain_result: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [BRAIN] Process communication query through central brain
        
        Args:
            query: Communication query to process
            brain_result: Central brain's initial processing
            context: Additional context
            
        Returns:
            Communication processing result integrated with brain
        """
        # The central brain has already processed this - we build on that
        brain_confidence = brain_result.get("brain_state", {}).get("confidence_level", 0.5)
        mood_score = brain_result.get("mood_score", 0.0)
        
        # Let brain update its communication domain expertise
        self.central_brain.domain_expertise["language"] += 0.02
        
        try:
            # Attempt communication processing
            comm_result = self._analyze_communication_need(query, mood_score)
            
            if comm_result["success"]:
                # Brain learns from successful communication processing
                success_phrase = f"Successfully handled communication: {query}"
                self.central_brain.process_input(success_phrase, domain="communication")
                
                return {
                    "success": True,
                    "response": comm_result["response"],
                    "confidence": min(1.0, brain_confidence + 0.2),
                    "communication_details": comm_result["details"],
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
            else:
                # Brain learns from communication challenges
                challenge_phrase = f"Communication challenge encountered: {query}"
                self.central_brain.process_input(challenge_phrase, domain="communication")
                
                return {
                    "success": False,
                    "response": f"I need to understand this communication need better: {query}",
                    "confidence": brain_confidence * 0.8,
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
                
        except Exception as e:
            # Brain processes the error for learning
            error_phrase = f"Communication processing error: {str(e)}"
            self.central_brain.process_input(error_phrase, domain="communication")
            
            return {
                "success": False,
                "response": "I encountered a communication processing challenge.",
                "confidence": brain_confidence * 0.5,
                "error": str(e),
                "brain_integration": "complete",
                "learning_occurred": True
            }
    
    def _analyze_communication_need(self, query: str, mood_score: float) -> Dict[str, Any]:
        """
        [BRAIN] Analyze communication needs and respond appropriately
        
        Args:
            query: Communication query
            mood_score: Current mood context
            
        Returns:
            Communication analysis result
        """
        query_lower = query.lower().strip()
        
        # Determine communication type and respond with brain-integrated approach
        if any(keyword in query_lower for keyword in ['explain', 'describe', 'tell me about']):
            return self._handle_explanation_request(query, mood_score)
            
        elif any(keyword in query_lower for keyword in ['help', 'assist', 'support']):
            return self._handle_help_request(query, mood_score)
            
        elif any(keyword in query_lower for keyword in ['question', 'ask', 'wonder']):
            return self._handle_inquiry(query, mood_score)
            
        elif any(keyword in query_lower for keyword in ['discuss', 'talk about', 'conversation']):
            return self._handle_discussion(query, mood_score)
            
        elif any(keyword in query_lower for keyword in ['clarify', 'confused', 'unclear']):
            return self._handle_clarification(query, mood_score)
            
        else:
            return self._handle_general_communication(query, mood_score)
    
    def _handle_explanation_request(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle explanation requests"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        
        return {
            "success": True,
            "response": f"I understand you'd like an explanation. My brain processes information through multiple specialized regions while maintaining unified consciousness. Let me help clarify what you're looking for.",
            "details": {
                "communication_type": "explanation_request",
                "tone_detected": tone,
                "approach": "structured_explanation",
                "brain_processing": "Central brain coordinates explanation through appropriate specialized regions"
            }
        }
    
    def _handle_help_request(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle help requests"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        response_template = self.central_brain.tone_engine.get_response_template(tone)
        
        return {
            "success": True,
            "response": f"I'm here to help! My brain integrates multiple processing capabilities - mathematics, physics, logic, language, and reasoning. {response_template}",
            "details": {
                "communication_type": "help_request",
                "tone_detected": tone,
                "available_capabilities": ["mathematics", "physics", "logic", "language", "reasoning"],
                "approach": "supportive_assistance"
            }
        }
    
    def _handle_inquiry(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle inquiries and questions"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        
        return {
            "success": True,
            "response": "I welcome your inquiry! My brain processes questions through specialized regions while maintaining unified awareness. What specific aspect would you like to explore?",
            "details": {
                "communication_type": "inquiry",
                "tone_detected": tone,
                "approach": "inquisitive_engagement",
                "processing_method": "brain_guided_exploration"
            }
        }
    
    def _handle_discussion(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle discussion requests"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        
        return {
            "success": True,
            "response": "I'd enjoy discussing this topic with you. My brain creates a conversational experience by integrating emotional awareness, logical reasoning, and contextual understanding.",
            "details": {
                "communication_type": "discussion",
                "tone_detected": tone,
                "approach": "collaborative_dialogue",
                "brain_features": ["emotional_awareness", "logical_reasoning", "contextual_understanding"]
            }
        }
    
    def _handle_clarification(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle clarification requests"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        
        return {
            "success": True,
            "response": "Let me help clarify! My brain can break down complex information into clearer components. What specific part needs more explanation?",
            "details": {
                "communication_type": "clarification",
                "tone_detected": tone,
                "approach": "step_by_step_clarification",
                "brain_capability": "information_decomposition"
            }
        }
    
    def _handle_general_communication(self, query: str, mood_score: float) -> Dict[str, Any]:
        """Handle general communication"""
        tone = self.central_brain.tone_engine.infer_tone(mood_score)
        response_template = self.central_brain.tone_engine.get_response_template(tone)
        
        return {
            "success": True,
            "response": f"I'm engaging with your message through my unified brain consciousness. {response_template} How can I best assist you?",
            "details": {
                "communication_type": "general",
                "tone_detected": tone,
                "approach": "adaptive_response",
                "brain_state": "unified_consciousness_active"
            }
        } 