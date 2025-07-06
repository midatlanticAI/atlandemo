#!/usr/bin/env python3
"""
Debug Wave Engine responses to understand accuracy issues
"""

from enhanced_wave_engine import EnhancedWaveEngine

def debug_wave_responses():
    """Debug what Wave Engine actually returns"""
    
    wave_engine = EnhancedWaveEngine()
    
    test_queries = [
        "If temperature is high and pressure is high, then what should happen?",
        "If patient has high blood pressure, then what alert level?",
        "If traffic light is red, then what should vehicle do?",
        "If room is empty, then how to save energy?",
        "If motion detected in secure area, then what action?"
    ]
    
    print("[SEARCH] DEBUGGING WAVE ENGINE RESPONSES")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        
        result = wave_engine.process_query(
            query, 
            context={
                'domain': 'safety_critical',
                'reasoning_type': 'conditional_logic',
                'expected_response': 'action_recommendation'
            }
        )
        
        print(f"Raw result keys: {list(result.keys())}")
        print(f"Final answer: '{result['final_answer']}'")
        print(f"Answer length: {len(result['final_answer'])}")
        print(f"Answer type: {type(result['final_answer'])}")
        
        # Check what we're actually getting
        answer = result['final_answer']
        print(f"Contains 'action': {'action' in answer.lower()}")
        print(f"Contains 'should': {'should' in answer.lower()}")
        print(f"Contains 'high': {'high' in answer.lower()}")
        print(f"Contains 'alert': {'alert' in answer.lower()}")
        print(f"Contains 'stop': {'stop' in answer.lower()}")
        print(f"Contains 'check': {'check' in answer.lower()}")
        print(f"Contains 'cannot solve': {'cannot solve' in answer.lower()}")
        print(f"Contains 'error': {'error' in answer.lower()}")
        print("-" * 40)

if __name__ == "__main__":
    debug_wave_responses() 