"""
Expert Knowledge Modules for Wave-based Cognition
Plug-and-play expertise modules that integrate with the Wave engine core.
"""

from .base_expert import BaseExpertModule
from .logic_expert import LogicExpertModule
from .math_expert import MathExpertModule
from .registry import ExpertRegistry
from .vision_experts import DCTDigitExpert
from .vision_experts import PixelPrototypeDigitExpert
from .vision_experts import PCAPrototypeDigitExpert

__all__ = [
    'BaseExpertModule',
    'LogicExpertModule', 
    'MathExpertModule',
    'DCTDigitExpert',
    'PixelPrototypeDigitExpert',
    'PCAPrototypeDigitExpert',
    'ExpertRegistry'
] 