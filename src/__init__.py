"""
VTRFM Source Code Archive – April 2025
Inventor: Johnathan Scott Viruet

Atlan Symbolic Cognitive Engine
A comprehensive framework for symbolic memory, perception, reasoning, and reflection.
"""

__version__ = "1.0.0"
__author__ = "Johnathan Scott Viruet"

from .agent import AtlanAgent
from .memory import RCoreMemoryIndex, SymbolicNode
from .perception import ToneEngine, DriftTracker
from .reasoning import BeliefSystem, DreamspaceSimulator
from .reflection import SelfAnchor
from .narrative import NarrativeNode
from .reinforcement import ReinforcementEngine
from .similarity import cosine_similarity, euclidean_distance, resonance_score
from .utils import _enhanced_vector

__all__ = [
    'AtlanAgent',
    'RCoreMemoryIndex',
    'SymbolicNode',
    'ToneEngine',
    'DriftTracker',
    'BeliefSystem',
    'DreamspaceSimulator',
    'SelfAnchor',
    'NarrativeNode',
    'ReinforcementEngine',
    'cosine_similarity',
    'euclidean_distance',
    'resonance_score',
    '_enhanced_vector'
] 