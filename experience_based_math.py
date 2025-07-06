#!/usr/bin/env python3
"""
Experience-Based Mathematical Learning
Let the engine discover mathematical operations through repeated experience.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def teach_addition_through_experience(engine):
    """Teach addition by experiencing the operation repeatedly."""
    print("🧮 TEACHING ADDITION THROUGH EXPERIENCE")
    print("=" * 50)
    
    # Multiple addition experiences - let the engine discover the pattern
    addition_experiences = [
        (["two", "combine", "three", "result", "five"], "2+3=5"),
        (["one", "combine", "four", "result", "five"], "1+4=5"),
        (["three", "combine", "two", "result", "five"], "3+2=5"),
        (["one", "combine", "one", "result", "two"], "1+1=2"),
        (["two", "combine", "one", "result", "three"], "2+1=3"),
        (["three", "combine", "one", "result", "four"], "3+1=4"),
        (["four", "combine", "one", "result", "five"], "4+1=5"),
        (["two", "combine", "two", "result", "four"], "2+2=4"),
        (["three", "combine", "three", "result", "six"], "3+3=6"),
    ]
    
    print("\n📚 Learning through repeated addition experiences...")
    for i, (experience, description) in enumerate(addition_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=experience,
            auditory=["operation", "mathematics"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn", "understand"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)  # Small delay to separate experiences
    
    print(f"\n[+] Addition experiences completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")


def test_addition_discovery(engine):
    """Test if the engine discovered addition through experience."""
    print("\n\n[SEARCH] TESTING ADDITION DISCOVERY")
    print("=" * 50)
    
    # Test problems the engine hasn't seen before
    test_cases = [
        (["four", "combine", "two", "result", "?"], "4+2=?", "six"),
        (["five", "combine", "one", "result", "?"], "5+1=?", "six"),
        (["two", "combine", "four", "result", "?"], "2+4=?", "six"),
        (["one", "combine", "three", "result", "?"], "1+3=?", "four"),
    ]
    
    results = []
    for test_input, description, expected in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        result = engine.live_experience(
            visual=test_input,
            auditory=["test", "problem"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["solve", "apply"], surprise=0.6, satisfaction=0.0
        )
        
        field = result['activation_field']
        
        # Check if expected answer is activated
        expected_activation = field.get(expected, 0)
        combine_activation = field.get('combine', 0)
        result_activation = field.get('result', 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        print(f"   'combine' operation activation: {combine_activation:.3f}")
        print(f"   'result' concept activation: {result_activation:.3f}")
        
        # Success if expected answer is strongly activated
        success = abs(expected_activation) > 0.3
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   [+] CORRECT: Strong activation for '{expected}'")
        else:
            print(f"   [-] INCORRECT: Weak activation for '{expected}'")
    
    return results


def teach_sequence_through_experience(engine):
    """Teach sequence patterns through repeated experience."""
    print("\n\n🔢 TEACHING SEQUENCES THROUGH EXPERIENCE")
    print("=" * 50)
    
    # Multiple sequence experiences
    sequence_experiences = [
        # Even numbers
        (["two", "next", "four", "next", "six"], "even sequence"),
        (["four", "next", "six", "next", "eight"], "even sequence"),
        (["six", "next", "eight", "next", "ten"], "even sequence"),
        
        # Odd numbers  
        (["one", "next", "three", "next", "five"], "odd sequence"),
        (["three", "next", "five", "next", "seven"], "odd sequence"),
        (["five", "next", "seven", "next", "nine"], "odd sequence"),
        
        # Simple counting
        (["one", "next", "two", "next", "three"], "counting"),
        (["two", "next", "three", "next", "four"], "counting"),
        (["three", "next", "four", "next", "five"], "counting"),
    ]
    
    print("\n📚 Learning through repeated sequence experiences...")
    for i, (experience, description) in enumerate(sequence_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=experience,
            auditory=["sequence", "pattern"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn", "pattern"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n[+] Sequence experiences completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_sequence_discovery(engine):
    """Test if the engine discovered sequence patterns."""
    print("\n\n[SEARCH] TESTING SEQUENCE DISCOVERY")
    print("=" * 50)
    
    test_cases = [
        (["eight", "next", "ten", "next", "?"], "8,10,?", "twelve"),
        (["seven", "next", "nine", "next", "?"], "7,9,?", "eleven"),
        (["four", "next", "five", "next", "?"], "4,5,?", "six"),
    ]
    
    results = []
    for test_input, description, expected in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        result = engine.live_experience(
            visual=test_input,
            auditory=["test", "sequence"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["predict", "continue"], surprise=0.6, satisfaction=0.0
        )
        
        field = result['activation_field']
        
        # Check activations
        expected_activation = field.get(expected, 0)
        next_activation = field.get('next', 0)
        pattern_activation = field.get('pattern', 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        print(f"   'next' operation activation: {next_activation:.3f}")
        print(f"   'pattern' concept activation: {pattern_activation:.3f}")
        
        success = abs(expected_activation) > 0.3
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   [+] CORRECT: Pattern recognition successful")
        else:
            print(f"   [-] INCORRECT: Pattern not recognized")
    
    return results


def teach_comparison_through_experience(engine):
    """Teach comparison operations through experience."""
    print("\n\n[DATA] TEACHING COMPARISON THROUGH EXPERIENCE")
    print("=" * 50)
    
    comparison_experiences = [
        (["five", "greater", "three", "true"], "5>3"),
        (["seven", "greater", "four", "true"], "7>4"),
        (["nine", "greater", "six", "true"], "9>6"),
        (["ten", "greater", "eight", "true"], "10>8"),
        (["two", "greater", "five", "false"], "2>5 (false)"),
        (["three", "greater", "seven", "false"], "3>7 (false)"),
        (["four", "greater", "nine", "false"], "4>9 (false)"),
        (["six", "equal", "six", "true"], "6=6"),
        (["five", "equal", "five", "true"], "5=5"),
        (["four", "equal", "seven", "false"], "4=7 (false)"),
    ]
    
    print("\n📚 Learning through repeated comparison experiences...")
    for i, (experience, description) in enumerate(comparison_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=experience,
            auditory=["comparison", "logic"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn", "compare"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n[+] Comparison experiences completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_comparison_discovery(engine):
    """Test if the engine discovered comparison operations."""
    print("\n\n[SEARCH] TESTING COMPARISON DISCOVERY")
    print("=" * 50)
    
    test_cases = [
        (["twelve", "greater", "nine", "?"], "12>9", "true"),
        (["four", "greater", "eight", "?"], "4>8", "false"),
        (["seven", "equal", "seven", "?"], "7=7", "true"),
        (["five", "equal", "three", "?"], "5=3", "false"),
    ]
    
    results = []
    for test_input, description, expected in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        result = engine.live_experience(
            visual=test_input,
            auditory=["test", "comparison"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["evaluate", "judge"], surprise=0.6, satisfaction=0.0
        )
        
        field = result['activation_field']
        
        expected_activation = field.get(expected, 0)
        greater_activation = field.get('greater', 0)
        equal_activation = field.get('equal', 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        print(f"   'greater' operation activation: {greater_activation:.3f}")
        print(f"   'equal' operation activation: {equal_activation:.3f}")
        
        success = abs(expected_activation) > 0.3
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   [+] CORRECT: Comparison reasoning successful")
        else:
            print(f"   [-] INCORRECT: Comparison reasoning failed")
    
    return results


def run_experience_based_learning():
    """Run the complete experience-based learning demonstration."""
    print("[BRAIN] EXPERIENCE-BASED MATHEMATICAL LEARNING")
    print("=" * 70)
    print("Teaching mathematical operations through repeated experience")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Teach operations through experience
    teach_addition_through_experience(engine)
    addition_results = test_addition_discovery(engine)
    
    teach_sequence_through_experience(engine)
    sequence_results = test_sequence_discovery(engine)
    
    teach_comparison_through_experience(engine)
    comparison_results = test_comparison_discovery(engine)
    
    end_time = time.time()
    
    # Analysis
    print("\n\n[DATA] EXPERIENCE-BASED LEARNING RESULTS")
    print("=" * 70)
    
    print(f"\n🧮 ADDITION DISCOVERY:")
    correct_addition = sum(1 for _, success, _ in addition_results if success)
    print(f"   Correct: {correct_addition}/{len(addition_results)}")
    for desc, success, activation in addition_results:
        status = "[+]" if success else "[-]"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n🔢 SEQUENCE DISCOVERY:")
    correct_sequence = sum(1 for _, success, _ in sequence_results if success)
    print(f"   Correct: {correct_sequence}/{len(sequence_results)}")
    for desc, success, activation in sequence_results:
        status = "[+]" if success else "[-]"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n[DATA] COMPARISON DISCOVERY:")
    correct_comparison = sum(1 for _, success, _ in comparison_results if success)
    print(f"   Correct: {correct_comparison}/{len(comparison_results)}")
    for desc, success, activation in comparison_results:
        status = "[+]" if success else "[-]"
        print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = correct_addition + correct_sequence + correct_comparison
    total_tests = len(addition_results) + len(sequence_results) + len(comparison_results)
    
    print(f"\n[TARGET] OVERALL PERFORMANCE:")
    print(f"   Total correct: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print(f"   Learning time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n[BRAIN] FINAL COGNITIVE STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active symbols: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    if total_correct/total_tests > 0.5:
        print(f"\n[PARTY] SUCCESS: Engine discovered mathematical operations through experience!")
        print(f"   Wave interference learned operational patterns from repeated exposure")
    else:
        print(f"\n🤔 PARTIAL SUCCESS: Some operational discovery, but needs refinement")
        print(f"   Wave patterns forming but not yet stable enough for consistent reasoning")


if __name__ == "__main__":
    run_experience_based_learning() 