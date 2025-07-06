#!/usr/bin/env python3
"""
ATLAN BIOINTELLIGENCE - MATHEMATICS REGION
[BRAIN] Mathematics processing region that flows through central brain
"""

import re
import math
from typing import Dict, Any, Optional, List
from core.agent import AtlanAgent

class MathematicsRegion:
    """
    [BRAIN] Mathematics specialized brain region
    ALL processing flows through central AtlanAgent - no bypassing allowed!
    """
    
    def __init__(self, central_brain: AtlanAgent):
        """
        Initialize mathematics region with central brain
        
        Args:
            central_brain: The AtlanAgent central executive
        """
        self.central_brain = central_brain
        self.math_patterns = {
            'basic_arithmetic': r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)',
            'percentage': r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)',
            'square_root': r'sqrt\((\d+(?:\.\d+)?)\)',
            'power': r'(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)',
            'factorial': r'(\d+)!',
        }
        
    def process_through_brain(self, query: str, brain_result: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [BRAIN] Process mathematics query through central brain
        
        Args:
            query: Mathematics query to process
            brain_result: Central brain's initial processing
            context: Additional context
            
        Returns:
            Mathematics processing result integrated with brain
        """
        # The central brain has already processed this - we build on that
        brain_confidence = brain_result.get("brain_state", {}).get("confidence_level", 0.5)
        
        # Let brain update its mathematical domain expertise
        self.central_brain.domain_expertise["mathematics"] += 0.02
        
        try:
            # Attempt mathematical processing
            math_result = self._solve_mathematical_expression(query)
            
            if math_result["success"]:
                # Brain learns from successful math processing
                success_phrase = f"Successfully solved: {query}"
                self.central_brain.process_input(success_phrase, domain="mathematics")
                
                return {
                    "success": True,
                    "response": math_result["response"],
                    "confidence": min(1.0, brain_confidence + 0.2),
                    "mathematical_details": math_result["details"],
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
            else:
                # Brain learns from math challenges
                challenge_phrase = f"Mathematical challenge encountered: {query}"
                self.central_brain.process_input(challenge_phrase, domain="mathematics")
                
                return {
                    "success": False,
                    "response": f"I need to analyze this mathematical problem further: {query}",
                    "confidence": brain_confidence * 0.8,
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
                
        except Exception as e:
            # Brain processes the error for learning
            error_phrase = f"Mathematics processing error: {str(e)}"
            self.central_brain.process_input(error_phrase, domain="mathematics")
            
            return {
                "success": False,
                "response": "I encountered a mathematical processing challenge.",
                "confidence": brain_confidence * 0.5,
                "error": str(e),
                "brain_integration": "complete",
                "learning_occurred": True
            }
    
    def _solve_mathematical_expression(self, query: str) -> Dict[str, Any]:
        """
        [BRAIN] Solve mathematical expressions
        
        Args:
            query: Mathematical query
            
        Returns:
            Mathematical solution result
        """
        query_lower = query.lower().strip()
        
        # Basic arithmetic
        arithmetic_match = re.search(self.math_patterns['basic_arithmetic'], query)
        if arithmetic_match:
            try:
                num1 = float(arithmetic_match.group(1))
                operator = arithmetic_match.group(2)
                num2 = float(arithmetic_match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return {"success": False, "error": "Division by zero"}
                    result = num1 / num2
                
                return {
                    "success": True,
                    "response": f"{num1} {operator} {num2} = {result}",
                    "details": {"operation": operator, "operands": [num1, num2], "result": result}
                }
            except ValueError:
                return {"success": False, "error": "Invalid number format"}
        
        # Percentage calculation
        percentage_match = re.search(self.math_patterns['percentage'], query)
        if percentage_match:
            try:
                percentage = float(percentage_match.group(1))
                value = float(percentage_match.group(2))
                result = (percentage / 100) * value
                
                return {
                    "success": True,
                    "response": f"{percentage}% of {value} = {result}",
                    "details": {"percentage": percentage, "value": value, "result": result}
                }
            except ValueError:
                return {"success": False, "error": "Invalid percentage format"}
        
        # Square root
        sqrt_match = re.search(self.math_patterns['square_root'], query)
        if sqrt_match:
            try:
                number = float(sqrt_match.group(1))
                if number < 0:
                    return {"success": False, "error": "Cannot calculate square root of negative number"}
                result = math.sqrt(number)
                
                return {
                    "success": True,
                    "response": f"√{number} = {result}",
                    "details": {"operation": "square_root", "input": number, "result": result}
                }
            except ValueError:
                return {"success": False, "error": "Invalid square root format"}
        
        # Power calculation
        power_match = re.search(self.math_patterns['power'], query)
        if power_match:
            try:
                base = float(power_match.group(1))
                exponent = float(power_match.group(2))
                result = base ** exponent
                
                return {
                    "success": True,
                    "response": f"{base}^{exponent} = {result}",
                    "details": {"base": base, "exponent": exponent, "result": result}
                }
            except ValueError:
                return {"success": False, "error": "Invalid power format"}
        
        # Factorial
        factorial_match = re.search(self.math_patterns['factorial'], query)
        if factorial_match:
            try:
                number = int(factorial_match.group(1))
                if number < 0:
                    return {"success": False, "error": "Cannot calculate factorial of negative number"}
                if number > 20:
                    return {"success": False, "error": "Factorial too large (limit: 20!)"}
                
                result = math.factorial(number)
                
                return {
                    "success": True,
                    "response": f"{number}! = {result}",
                    "details": {"operation": "factorial", "input": number, "result": result}
                }
            except ValueError:
                return {"success": False, "error": "Invalid factorial format"}
        
        # No mathematical pattern found
        return {
            "success": False,
            "response": "I don't recognize this mathematical expression pattern yet.",
            "details": {"query": query, "patterns_checked": list(self.math_patterns.keys())}
        } 