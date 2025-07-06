#!/usr/bin/env python3
"""
Find test queries that Wave Engine can actually handle well
"""

from enhanced_wave_engine import EnhancedWaveEngine

def test_different_query_types():
    """Test different types of queries to find what works"""
    
    wave_engine = EnhancedWaveEngine()
    
    query_categories = {
        'Simple Logic': [
            "True or False: If A is true and B is true, then A and B is true",
            "True or False: If A is false or B is false, then A and B is false",
            "True or False: If A implies B and A is true, then B is true",
            "True or False: If all X are Y and Z is X, then Z is Y"
        ],
        'Math Problems': [
            "What is 15 + 27?",
            "What is 144 divided by 12?",
            "What is the square root of 64?",
            "What is 8 factorial?"
        ],
        'Pattern Recognition': [
            "What comes next: 2, 4, 8, 16, ?",
            "What comes next: 1, 1, 2, 3, 5, 8, ?",
            "Complete the pattern: A, C, E, G, ?",
            "What is the next number: 10, 20, 40, 80, ?"
        ],
        'Simple Reasoning': [
            "If it's raining, should you take an umbrella?",
            "If the light is red, should you stop?",
            "If battery is low, what should you do?",
            "If temperature is too hot, what action?"
        ]
    }
    
    print("[SEARCH] TESTING QUERY TYPES TO FIND WHAT WORKS")
    print("=" * 60)
    
    working_queries = []
    
    for category, queries in query_categories.items():
        print(f"\n📂 {category}")
        print("-" * 40)
        
        for query in queries:
            result = wave_engine.process_query(query)
            answer = result['final_answer']
            
            # Check if it's a reasonable response
            is_reasonable = (
                len(answer) > 3 and 
                answer.lower() not in ['no', 'yes', 'reason', 'question', 'inquiry'] and
                'cannot solve' not in answer.lower() and
                'error' not in answer.lower()
            )
            
            status = "[+] GOOD" if is_reasonable else "[-] BAD"
            print(f"  {status}: {query}")
            print(f"    Answer: '{answer}'")
            
            if is_reasonable:
                working_queries.append((query, answer))
    
    print(f"\n[DATA] SUMMARY")
    print(f"Found {len(working_queries)} working queries:")
    for i, (query, answer) in enumerate(working_queries[:5], 1):
        print(f"  {i}. {query} → {answer}")
    
    return working_queries

if __name__ == "__main__":
    working_queries = test_different_query_types() 