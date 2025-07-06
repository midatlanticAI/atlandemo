#!/usr/bin/env python3
"""
Debug script for bidirectional dilemma parsing
"""

import re

def debug_bidirectional_parsing():
    """Debug the bidirectional dilemma parsing"""
    
    # Test cases
    test_cases = [
        {
            "query": "Can we say at least one of the following must always be true? (a) he will get good grades. and (b) he doesn't watch too much tv.",
            "expected": "yes",
            "description": "Should be yes - both positive"
        },
        {
            "query": "Can we say at least one of the following must always be true? (a) he won't get good grades. and (b) he watches too much tv.",
            "expected": "no", 
            "description": "Should be no - both negative"
        }
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n=== TEST {i+1}: {test['description']} ===")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected']}")
        
        # Test the regex parsing
        options_match = re.search(r'\(a\)\s*([^)]+?)\s*(?:and|\.)\s*\(b\)\s*([^)]+?)(?:\?|$)', test['query'], re.IGNORECASE)
        if options_match:
            option_a = options_match.group(1).strip()
            option_b = options_match.group(2).strip()
            
            print(f"Option A: '{option_a}'")
            print(f"Option B: '{option_b}'")
            
            # Test negation detection
            negation_patterns = [
                "won't", "will not", "doesn't", "does not", "isn't", "is not",
                "didn't", "did not", "hasn't", "has not", "haven't", "have not",
                "can't", "cannot", "shouldn't", "should not"
            ]
            
            option_a_negative = any(pattern in option_a.lower() for pattern in negation_patterns)
            option_b_negative = any(pattern in option_b.lower() for pattern in negation_patterns)
            
            print(f"Option A negative: {option_a_negative}")
            print(f"Option B negative: {option_b_negative}")
            
            # Apply the logic
            if not option_a_negative and not option_b_negative:
                result = "yes"
                explanation = "Both positive - P AND Q"
            elif option_a_negative and option_b_negative:
                result = "no"
                explanation = "Both negative - ¬P AND ¬Q"
            else:
                result = "no"
                explanation = "Mixed - inconsistent"
            
            print(f"Result: {result}")
            print(f"Explanation: {explanation}")
            print(f"Correct: {'[+]' if result == test['expected'] else '[-]'}")
        else:
            print("[-] REGEX FAILED TO MATCH")

if __name__ == "__main__":
    debug_bidirectional_parsing() 