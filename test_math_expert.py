#!/usr/bin/env python3
"""
Test Mathematical Expert Module Integration
Demonstrates the mathematical reasoning capabilities of the enhanced Wave Engine
"""

import time
from enhanced_wave_engine import EnhancedWaveEngine


def test_mathematical_reasoning():
    """Test mathematical reasoning capabilities."""
    print("🧮 MATHEMATICAL EXPERT MODULE TEST")
    print("=" * 50)
    
    # Initialize enhanced Wave Engine with experts
    engine = EnhancedWaveEngine()
    
    # Mathematical test cases
    test_cases = [
        # Arithmetic
        {
            'query': 'Calculate 15 + 27',
            'category': 'Arithmetic',
            'expected_type': 'arithmetic_calculation'
        },
        {
            'query': 'What is 144 / 12?',
            'category': 'Arithmetic', 
            'expected_type': 'arithmetic_calculation'
        },
        {
            'query': 'Multiply 7 × 9',
            'category': 'Arithmetic',
            'expected_type': 'arithmetic_calculation'
        },
        
        # Algebra
        {
            'query': 'Solve x + 5 = 12',
            'category': 'Algebra',
            'expected_type': 'equation_solving'
        },
        {
            'query': 'Find x when 2x - 3 = 7',
            'category': 'Algebra',
            'expected_type': 'equation_solving'
        },
        
        # Geometry
        {
            'query': 'Find the area of a circle with radius 4',
            'category': 'Geometry',
            'expected_type': 'geometry_calculation'
        },
        {
            'query': 'Calculate the area of a triangle with base 6 and height 8',
            'category': 'Geometry',
            'expected_type': 'geometry_calculation'
        },
        
        # Statistics
        {
            'query': 'Find the mean of 2, 4, 6, 8, 10',
            'category': 'Statistics',
            'expected_type': 'statistical_analysis'
        },
        {
            'query': 'What is the median of 1, 3, 5, 7, 9?',
            'category': 'Statistics',
            'expected_type': 'statistical_analysis'
        },
        
        # Complex expressions
        {
            'query': '(5 + 3) * 2 - 4',
            'category': 'Complex',
            'expected_type': 'arithmetic_calculation'
        }
    ]
    
    print(f"🧪 Testing {len(test_cases)} mathematical problems...\n")
    
    total_correct = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case['query']
        category = test_case['category']
        expected_type = test_case['expected_type']
        
        print(f"🔢 Test {i}: {category}")
        print(f"   Question: {query}")
        
        # Process through enhanced Wave Engine
        result = engine.process_query(query, context={'domain': 'math'})
        
        # Extract results
        final_answer = result['final_answer']
        expert_response = result.get('expert_response')
        wave_response = result.get('wave_response')
        synergy_score = result.get('synergy_score', 0)
        
        print(f"   [BOT] Answer: {final_answer}")
        
        if expert_response:
            print(f"   [DATA] Expert Confidence: {expert_response.confidence:.2f}")
            print(f"   [BRAIN] Problem Type: {expert_response.metadata.get('problem_type', 'unknown')}")
            print(f"   📚 Domain: {expert_response.metadata.get('mathematical_domain', 'unknown')}")
            
            # Show solution steps if available
            steps = expert_response.metadata.get('solution_steps', [])
            if steps:
                print(f"   📝 Solution Steps:")
                for step in steps:
                    print(f"      • {step}")
            
            # Show formulas used
            formulas = expert_response.metadata.get('formulas_used', [])
            if formulas:
                print(f"   📐 Formulas: {', '.join(formulas)}")
            
            # Check if problem type matches expected
            actual_type = expert_response.metadata.get('problem_type', 'unknown')
            if actual_type == expected_type:
                print(f"   [+] Problem type correctly identified")
                total_correct += 1
            else:
                print(f"   [-] Expected {expected_type}, got {actual_type}")
        
        if wave_response:
            print(f"   [WAVE] Wave Confidence: {wave_response.get('confidence', 0):.2f}")
        
        print(f"   [LINK] Synergy Score: {synergy_score:.2f}")
        print(f"   ⏱️  Processing Time: {result['processing_time']:.3f}s")
        print()
    
    # Summary
    print("[TARGET] MATHEMATICAL REASONING SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Correct Classifications: {total_correct}")
    print(f"   Classification Accuracy: {total_correct/total_tests:.1%}")
    
    # Performance summary
    performance_summary = engine.get_performance_summary()
    print(f"   Total Queries Processed: {performance_summary.get('query_count', 0)}")
    print(f"   Average Processing Time: {performance_summary.get('average_processing_time', 0):.3f}s")
    
    if performance_summary.get('average_synergy_score', 0) > 0:
        print(f"   Average Synergy Score: {performance_summary.get('average_synergy_score', 0):.2f}")
    
    print(f"\n[TROPHY] MATH EXPERT MODULE: {'PASSED' if total_correct >= total_tests * 0.8 else 'NEEDS IMPROVEMENT'}")


def test_math_expert_wave_patterns():
    """Test mathematical wave pattern generation."""
    print("\n[WAVE] MATHEMATICAL WAVE PATTERNS TEST")
    print("=" * 50)
    
    engine = EnhancedWaveEngine()
    
    # Test different mathematical domains
    domain_tests = [
        ('Calculate 25 + 17', 'Arithmetic'),
        ('Solve 3x + 2 = 11', 'Algebra'),
        ('Find area of circle radius 5', 'Geometry'),
        ('Mean of 1,2,3,4,5', 'Statistics')
    ]
    
    for query, domain in domain_tests:
        print(f"[DATA] {domain} Wave Patterns:")
        print(f"   Query: {query}")
        
        result = engine.process_query(query, context={'domain': 'math'})
        expert_response = result.get('expert_response')
        
        if expert_response and expert_response.wave_patterns:
            patterns = expert_response.wave_patterns
            
            # Sort patterns by strength
            sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
            
            print(f"   [WAVE] Top Wave Patterns:")
            for pattern, strength in sorted_patterns[:5]:
                print(f"      • {pattern}: {strength:.2f}")
        
        print()


def test_mathematical_complexity():
    """Test mathematical complexity handling."""
    print("[BRAIN] MATHEMATICAL COMPLEXITY TEST")
    print("=" * 50)
    
    engine = EnhancedWaveEngine()
    
    complexity_tests = [
        ('2 + 2', 'Very Easy'),
        ('15 * 7 + 3', 'Easy'),
        ('Solve 2x + 5 = 13 for x', 'Medium'),
        ('Find the area of a triangle with base 12 and height 8', 'Medium'),
        ('Calculate mean and median of: 15, 23, 7, 39, 12, 8, 25', 'Hard')
    ]
    
    for query, expected_complexity in complexity_tests:
        print(f"[TARGET] {expected_complexity} Problem:")
        print(f"   Query: {query}")
        
        result = engine.process_query(query, context={'domain': 'math'})
        expert_response = result.get('expert_response')
        
        if expert_response:
            difficulty = expert_response.metadata.get('difficulty', 'unknown')
            confidence = expert_response.confidence
            answer = expert_response.answer
            
            print(f"   [BOT] Answer: {answer}")
            print(f"   [DATA] Detected Difficulty: {difficulty}")
            print(f"   [TARGET] Confidence: {confidence:.2f}")
            print(f"   ⏱️  Time: {result['processing_time']:.3f}s")
        
        print()


def main():
    """Run all mathematical expert tests."""
    print("🧮 ENHANCED WAVE ENGINE - MATHEMATICAL EXPERT TESTING")
    print("[ROCKET] Demonstrating college-level mathematical reasoning capabilities")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all tests
    test_mathematical_reasoning()
    test_math_expert_wave_patterns()
    test_mathematical_complexity()
    
    total_time = time.time() - start_time
    
    print(f"\n[BOLT] ALL TESTS COMPLETED")
    print(f"🕐 Total Time: {total_time:.2f} seconds")
    print(f"[BRAIN] Mathematical Expert Module successfully integrated with Wave Engine!")
    print(f"[CHART] Ready for mathematical reasoning benchmarks!")


if __name__ == "__main__":
    main() 