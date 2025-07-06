#!/usr/bin/env python3
"""
Quick diagnostic to debug the logic expert module issues
"""

from enhanced_wave_engine import EnhancedWaveEngine
from expert_modules.logic_expert import LogicExpertModule
import json

def debug_logic_expert():
    """Debug the logic expert module"""
    
    print("🔍 LOGIC EXPERT DIAGNOSTIC")
    print("=" * 50)
    
    # Initialize components
    engine = EnhancedWaveEngine()
    expert = LogicExpertModule()
    
    # Test cases that should be simple
    test_cases = [
        {
            "context": "if tired then rest",
            "question": "Jack is tired. Will he rest?",
            "expected": "yes",
            "description": "Simple modus ponens"
        },
        {
            "context": "if tired then rest",
            "question": "Jack is tired. Won't he rest?",
            "expected": "no", 
            "description": "Negated modus ponens"
        },
        {
            "context": "if good grades then no TV",
            "question": "Can we say at least one of the following must always be true? (a) he will get good grades. and (b) he doesn't watch too much tv.",
            "expected": "yes",
            "description": "Bidirectional dilemma - should be yes"
        },
        {
            "context": "if good grades then no TV",
            "question": "Can we say at least one of the following must always be true? (a) he won't get good grades. and (b) he watches too much tv.",
            "expected": "no",
            "description": "Bidirectional dilemma - should be no"
        }
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n📋 TEST {i+1}: {test['description']}")
        print(f"Context: {test['context']}")
        print(f"Question: {test['question']}")
        print(f"Expected: {test['expected']}")
        
        # Check if expert can handle this
        can_handle = expert.can_handle(test['question'])
        print(f"Can handle: {can_handle}")
        
        if can_handle:
            # Process the query
            context_dict = {
                'context': test['context'],
                'premises': test['context']
            }
            
            result = expert.process_query(test['question'], context_dict)
            print(f"Result: {result}")
            
            # Check wave patterns
            wave_patterns = result.wave_patterns if hasattr(result, 'wave_patterns') else {}
            print(f"Wave patterns detected: {wave_patterns}")
            
            # Check logical structure
            logical_structure = result.metadata.get('logical_structure', {}) if hasattr(result, 'metadata') else {}
            print(f"Logical structure: {logical_structure}")
            
            # Check negation detection (simple check)
            has_negation = any(neg in test['question'].lower() for neg in ['won\'t', 'will not', 'doesn\'t', 'does not', 'isn\'t', 'is not'])
            print(f"Negation detected: {has_negation}")
            
            correct = result.answer == test['expected']
            print(f"✅ CORRECT" if correct else f"❌ WRONG ({result.answer} != {test['expected']})")
        else:
            print("❌ CANNOT HANDLE")
        
        print("-" * 40)
    
    print("\n🔧 DEBUGGING WAVE FREQUENCIES:")
    print("Logic frequencies:")
    for concept, freq in expert.wave_frequencies.items():
        print(f"  {concept}: {freq}Hz")
    
    print(f"\nConfidence threshold: {expert.confidence_threshold}")
    print(f"Current performance: {expert.performance_history}")

if __name__ == "__main__":
    debug_logic_expert() 