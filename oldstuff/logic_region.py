#!/usr/bin/env python3
"""
ATLAN BIOINTELLIGENCE - LOGIC REGION
🧠 Logic processing region that flows through central brain
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from core.agent import AtlanAgent

class LogicRegion:
    """
    🧠 Logic specialized brain region
    ALL processing flows through central AtlanAgent - no bypassing allowed!
    """
    
    def __init__(self, central_brain: AtlanAgent):
        """
        Initialize logic region with central brain
        
        Args:
            central_brain: The AtlanAgent central executive
        """
        self.central_brain = central_brain
        self.logical_operators = {
            'and': lambda a, b: a and b,
            'or': lambda a, b: a or b,
            'not': lambda a: not a,
            'implies': lambda a, b: (not a) or b,
            'if_then': lambda a, b: (not a) or b,
            'equivalent': lambda a, b: a == b
        }
        
        self.fallacy_patterns = {
            'ad_hominem': ['attack the person', 'personal attack'],
            'straw_man': ['misrepresent', 'distort argument'],
            'false_dichotomy': ['only two options', 'either or'],
            'slippery_slope': ['leads to', 'will result in'],
            'circular_reasoning': ['because', 'proves itself']
        }
        
    def process_through_brain(self, query: str, brain_result: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        🧠 Process logic query through central brain
        
        Args:
            query: Logic query to process
            brain_result: Central brain's initial processing
            context: Additional context
            
        Returns:
            Logic processing result integrated with brain
        """
        # The central brain has already processed this - we build on that
        brain_confidence = brain_result.get("brain_state", {}).get("confidence_level", 0.5)
        
        # Let brain update its logic domain expertise
        self.central_brain.domain_expertise["logic"] += 0.02
        
        try:
            # Attempt logical processing
            logic_result = self._analyze_logical_structure(query)
            
            if logic_result["success"]:
                # Brain learns from successful logic processing
                success_phrase = f"Successfully analyzed logic: {query}"
                self.central_brain.process_input(success_phrase, domain="logic")
                
                return {
                    "success": True,
                    "response": logic_result["response"],
                    "confidence": min(1.0, brain_confidence + 0.2),
                    "logical_details": logic_result["details"],
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
            else:
                # Brain learns from logic challenges
                challenge_phrase = f"Logic challenge encountered: {query}"
                self.central_brain.process_input(challenge_phrase, domain="logic")
                
                return {
                    "success": False,
                    "response": f"I need to analyze this logical structure further: {query}",
                    "confidence": brain_confidence * 0.8,
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
                
        except Exception as e:
            # Brain processes the error for learning
            error_phrase = f"Logic processing error: {str(e)}"
            self.central_brain.process_input(error_phrase, domain="logic")
            
            return {
                "success": False,
                "response": "I encountered a logical processing challenge.",
                "confidence": brain_confidence * 0.5,
                "error": str(e),
                "brain_integration": "complete",
                "learning_occurred": True
            }
    
    def _analyze_logical_structure(self, query: str) -> Dict[str, Any]:
        """
        🧠 Analyze logical structures and arguments
        
        Args:
            query: Logic query
            
        Returns:
            Logical analysis result
        """
        query_lower = query.lower().strip()
        
        # Check for different types of logical analysis
        if any(keyword in query_lower for keyword in ['syllogism', 'premise', 'conclusion']):
            return self._analyze_syllogism(query)
            
        elif any(keyword in query_lower for keyword in ['if', 'then', 'implies']):
            return self._analyze_conditional(query_lower)
            
        elif any(keyword in query_lower for keyword in ['and', 'or', 'not']):
            return self._analyze_boolean_logic(query_lower)
            
        elif any(keyword in query_lower for keyword in ['valid', 'invalid', 'argument']):
            return self._analyze_argument_validity(query)
            
        elif any(keyword in query_lower for keyword in ['fallacy', 'error', 'mistake']):
            return self._detect_logical_fallacies(query)
            
        elif any(keyword in query_lower for keyword in ['contradiction', 'consistent']):
            return self._check_consistency(query)
            
        else:
            return self._general_logical_analysis(query)
    
    def _analyze_syllogism(self, query: str) -> Dict[str, Any]:
        """Analyze syllogistic reasoning"""
        return {
            "success": True,
            "response": "A syllogism consists of major premise, minor premise, and conclusion. Valid forms follow logical rules.",
            "details": {
                "structure": "Major premise → Minor premise → Conclusion",
                "example": "All humans are mortal (major) → Socrates is human (minor) → Socrates is mortal (conclusion)",
                "validity": "Depends on logical form, not truth of premises"
            }
        }
    
    def _analyze_conditional(self, query: str) -> Dict[str, Any]:
        """Analyze conditional statements (if-then)"""
        # Extract potential conditional structure
        if_match = re.search(r'if\s+(.*?)\s+then\s+(.*)', query)
        
        if if_match:
            antecedent = if_match.group(1).strip()
            consequent = if_match.group(2).strip()
            
            return {
                "success": True,
                "response": f"Conditional: If {antecedent}, then {consequent}. This is logically equivalent to: not({antecedent}) or {consequent}.",
                "details": {
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "logical_form": "P → Q ≡ ¬P ∨ Q",
                    "truth_conditions": "False only when antecedent is true and consequent is false"
                }
            }
        else:
            return {
                "success": True,
                "response": "Conditional statements have the form 'If P, then Q'. They're false only when P is true and Q is false.",
                "details": {
                    "logical_form": "P → Q",
                    "truth_table": "TT→T, TF→F, FT→T, FF→T"
                }
            }
    
    def _analyze_boolean_logic(self, query: str) -> Dict[str, Any]:
        """Analyze boolean logical operations"""
        operators_found = []
        
        if 'and' in query:
            operators_found.append('conjunction (AND)')
        if 'or' in query:
            operators_found.append('disjunction (OR)')  
        if 'not' in query:
            operators_found.append('negation (NOT)')
            
        return {
            "success": True,
            "response": f"Boolean logic operators detected: {', '.join(operators_found)}. These combine propositions logically.",
            "details": {
                "operators_found": operators_found,
                "conjunction": "A AND B - true only when both A and B are true",
                "disjunction": "A OR B - false only when both A and B are false",
                "negation": "NOT A - opposite truth value of A"
            }
        }
    
    def _analyze_argument_validity(self, query: str) -> Dict[str, Any]:
        """Analyze argument validity"""
        return {
            "success": True,
            "response": "Argument validity depends on logical form. Valid arguments preserve truth from premises to conclusion.",
            "details": {
                "validity": "If premises are true, conclusion must be true",
                "soundness": "Valid argument with true premises",
                "common_valid_forms": ["Modus ponens", "Modus tollens", "Hypothetical syllogism"],
                "common_invalid_forms": ["Affirming the consequent", "Denying the antecedent"]
            }
        }
    
    def _detect_logical_fallacies(self, query: str) -> Dict[str, Any]:
        """Detect potential logical fallacies"""
        detected_fallacies = []
        
        for fallacy, patterns in self.fallacy_patterns.items():
            if any(pattern in query.lower() for pattern in patterns):
                detected_fallacies.append(fallacy)
        
        if detected_fallacies:
            return {
                "success": True,
                "response": f"Potential logical fallacies detected: {', '.join(detected_fallacies)}.",
                "details": {
                    "detected_fallacies": detected_fallacies,
                    "note": "Fallacy detection is pattern-based and may need human verification"
                }
            }
        else:
            return {
                "success": True,
                "response": "No obvious logical fallacies detected, but thorough analysis may reveal subtle issues.",
                "details": {
                    "common_fallacies": list(self.fallacy_patterns.keys()),
                    "recommendation": "Consider premise truth, argument structure, and hidden assumptions"
                }
            }
    
    def _check_consistency(self, query: str) -> Dict[str, Any]:
        """Check logical consistency"""
        return {
            "success": True,
            "response": "Logical consistency means statements don't contradict each other. Inconsistent sets lead to paradoxes.",
            "details": {
                "consistency": "No statement contradicts another",
                "contradiction": "Statement and its negation both claimed true",
                "principle": "From contradiction, anything follows (principle of explosion)"
            }
        }
    
    def _general_logical_analysis(self, query: str) -> Dict[str, Any]:
        """General logical analysis for unclear queries"""
        return {
            "success": True,
            "response": "I can help analyze logical structures including: arguments, conditionals, syllogisms, boolean logic, and fallacies.",
            "details": {
                "capabilities": [
                    "Argument validity analysis",
                    "Conditional logic (if-then)",
                    "Boolean operations (and, or, not)",
                    "Syllogistic reasoning",
                    "Fallacy detection",
                    "Consistency checking"
                ],
                "query_examples": [
                    "Is this argument valid?",
                    "Analyze this conditional statement",
                    "Check for logical fallacies",
                    "Evaluate this syllogism"
                ]
            }
        } 