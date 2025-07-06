#!/usr/bin/env python3
"""
ATLAN BIOINTELLIGENCE - PHYSICS REGION
[BRAIN] Physics processing region that flows through central brain
"""

import re
import math
from typing import Dict, Any, Optional, List
from core.agent import AtlanAgent

class PhysicsRegion:
    """
    [BRAIN] Physics specialized brain region  
    ALL processing flows through central AtlanAgent - no bypassing allowed!
    """
    
    def __init__(self, central_brain: AtlanAgent):
        """
        Initialize physics region with central brain
        
        Args:
            central_brain: The AtlanAgent central executive
        """
        self.central_brain = central_brain
        self.physics_constants = {
            'c': 299792458,  # Speed of light (m/s)
            'g': 9.81,       # Gravitational acceleration (m/s²)
            'h': 6.626e-34,  # Planck constant
            'G': 6.674e-11,  # Gravitational constant
            'e': 1.602e-19,  # Elementary charge
        }
        
        self.physics_formulas = {
            'kinetic_energy': {'formula': '0.5 * m * v^2', 'vars': ['m', 'v']},
            'potential_energy': {'formula': 'm * g * h', 'vars': ['m', 'h']},
            'force': {'formula': 'm * a', 'vars': ['m', 'a']},
            'momentum': {'formula': 'm * v', 'vars': ['m', 'v']},
            'work': {'formula': 'F * d', 'vars': ['F', 'd']},
            'power': {'formula': 'W / t', 'vars': ['W', 't']},
        }
        
    def process_through_brain(self, query: str, brain_result: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [BRAIN] Process physics query through central brain
        
        Args:
            query: Physics query to process
            brain_result: Central brain's initial processing
            context: Additional context
            
        Returns:
            Physics processing result integrated with brain
        """
        # The central brain has already processed this - we build on that
        brain_confidence = brain_result.get("brain_state", {}).get("confidence_level", 0.5)
        
        # Let brain update its physics domain expertise
        self.central_brain.domain_expertise["physics"] += 0.02
        
        try:
            # Attempt physics processing
            physics_result = self._analyze_physics_problem(query)
            
            if physics_result["success"]:
                # Brain learns from successful physics processing
                success_phrase = f"Successfully analyzed physics: {query}"
                self.central_brain.process_input(success_phrase, domain="physics")
                
                return {
                    "success": True,
                    "response": physics_result["response"],
                    "confidence": min(1.0, brain_confidence + 0.2),
                    "physics_details": physics_result["details"],
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
            else:
                # Brain learns from physics challenges
                challenge_phrase = f"Physics challenge encountered: {query}"
                self.central_brain.process_input(challenge_phrase, domain="physics")
                
                return {
                    "success": False,
                    "response": f"I need to analyze this physics problem further: {query}",
                    "confidence": brain_confidence * 0.8,
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
                
        except Exception as e:
            # Brain processes the error for learning
            error_phrase = f"Physics processing error: {str(e)}"
            self.central_brain.process_input(error_phrase, domain="physics")
            
            return {
                "success": False,
                "response": "I encountered a physics processing challenge.",
                "confidence": brain_confidence * 0.5,
                "error": str(e),
                "brain_integration": "complete",
                "learning_occurred": True
            }
    
    def _analyze_physics_problem(self, query: str) -> Dict[str, Any]:
        """
        [BRAIN] Analyze physics problems and concepts
        
        Args:
            query: Physics query
            
        Returns:
            Physics analysis result
        """
        query_lower = query.lower().strip()
        
        # Check for physics concepts
        if any(concept in query_lower for concept in ['energy', 'kinetic', 'potential']):
            return self._handle_energy_concepts(query_lower)
        
        elif any(concept in query_lower for concept in ['force', 'newton', 'acceleration']):
            return self._handle_force_concepts(query_lower)
            
        elif any(concept in query_lower for concept in ['momentum', 'velocity', 'mass']):
            return self._handle_momentum_concepts(query_lower)
            
        elif any(concept in query_lower for concept in ['gravity', 'gravitational', 'weight']):
            return self._handle_gravity_concepts(query_lower)
            
        elif any(concept in query_lower for concept in ['wave', 'frequency', 'wavelength']):
            return self._handle_wave_concepts(query_lower)
            
        elif any(concept in query_lower for concept in ['light', 'photon', 'speed of light']):
            return self._handle_light_concepts(query_lower)
        
        else:
            return {
                "success": False,
                "response": "I don't recognize this physics concept yet.",
                "details": {"query": query, "available_topics": ["energy", "force", "momentum", "gravity", "waves", "light"]}
            }
    
    def _handle_energy_concepts(self, query: str) -> Dict[str, Any]:
        """Handle energy-related physics concepts"""
        if 'kinetic' in query:
            return {
                "success": True,
                "response": "Kinetic energy is the energy of motion, calculated as KE = ½mv². It depends on mass and velocity squared.",
                "details": {
                    "concept": "kinetic_energy",
                    "formula": "KE = ½mv²",
                    "units": "Joules (J)",
                    "variables": {"m": "mass (kg)", "v": "velocity (m/s)"}
                }
            }
        elif 'potential' in query:
            return {
                "success": True,  
                "response": "Gravitational potential energy is stored energy due to position, calculated as PE = mgh.",
                "details": {
                    "concept": "potential_energy",
                    "formula": "PE = mgh",
                    "units": "Joules (J)",
                    "variables": {"m": "mass (kg)", "g": "acceleration due to gravity (9.81 m/s²)", "h": "height (m)"}
                }
            }
        else:
            return {
                "success": True,
                "response": "Energy is the capacity to do work. It comes in many forms: kinetic, potential, thermal, chemical, etc.",
                "details": {"concept": "energy", "conservation": "Energy cannot be created or destroyed, only transformed"}
            }
    
    def _handle_force_concepts(self, query: str) -> Dict[str, Any]:
        """Handle force-related physics concepts"""
        return {
            "success": True,
            "response": "Force is a push or pull that can change an object's motion. Newton's second law: F = ma.",
            "details": {
                "concept": "force",
                "formula": "F = ma",
                "units": "Newtons (N)",
                "variables": {"m": "mass (kg)", "a": "acceleration (m/s²)"}
            }
        }
    
    def _handle_momentum_concepts(self, query: str) -> Dict[str, Any]:
        """Handle momentum-related physics concepts"""
        return {
            "success": True,
            "response": "Momentum is the quantity of motion, calculated as p = mv. It's conserved in isolated systems.",
            "details": {
                "concept": "momentum",
                "formula": "p = mv",
                "units": "kg⋅m/s",
                "variables": {"m": "mass (kg)", "v": "velocity (m/s)"},
                "conservation": "Total momentum is conserved in collisions"
            }
        }
    
    def _handle_gravity_concepts(self, query: str) -> Dict[str, Any]:
        """Handle gravity-related physics concepts"""
        return {
            "success": True,
            "response": f"Gravity is a fundamental force. On Earth, g = {self.physics_constants['g']} m/s². Universal gravitation: F = Gm₁m₂/r².",
            "details": {
                "concept": "gravity",
                "earth_acceleration": f"{self.physics_constants['g']} m/s²",
                "universal_formula": "F = Gm₁m₂/r²",
                "constant_G": f"{self.physics_constants['G']} N⋅m²/kg²"
            }
        }
    
    def _handle_wave_concepts(self, query: str) -> Dict[str, Any]:
        """Handle wave-related physics concepts"""
        return {
            "success": True,
            "response": "Waves transfer energy without transferring matter. Key relationship: v = fλ (velocity = frequency × wavelength).",
            "details": {
                "concept": "waves",
                "formula": "v = fλ",
                "variables": {"v": "velocity (m/s)", "f": "frequency (Hz)", "λ": "wavelength (m)"}
            }
        }
    
    def _handle_light_concepts(self, query: str) -> Dict[str, Any]:
        """Handle light-related physics concepts"""
        return {
            "success": True,
            "response": f"Light is electromagnetic radiation. In vacuum, it travels at c = {self.physics_constants['c']:,} m/s.",
            "details": {
                "concept": "light",
                "speed_of_light": f"{self.physics_constants['c']:,} m/s",
                "nature": "electromagnetic radiation",
                "properties": ["wave-particle duality", "constant speed in vacuum"]
            }
        } 