#!/usr/bin/env python3
"""
Advanced Mathematical Scaling Test
Push the quantity-grounded system to complex mathematical reasoning.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def teach_larger_quantities(engine):
    """Extend quantity recognition to larger numbers."""
    print("🔢 SCALING: LARGER QUANTITIES (6-10)")
    print("=" * 50)
    
    # Teach six through ten
    larger_quantities = [
        (["object"] * 6, "six", "six objects"),
        (["block"] * 6, "six", "six blocks"),
        (["object"] * 7, "seven", "seven objects"),
        (["block"] * 7, "seven", "seven blocks"),
        (["object"] * 8, "eight", "eight objects"),
        (["block"] * 8, "eight", "eight blocks"),
        (["object"] * 9, "nine", "nine objects"),
        (["block"] * 9, "nine", "nine blocks"),
        (["object"] * 10, "ten", "ten objects"),
        (["block"] * 10, "ten", "ten blocks"),
    ]
    
    print("\n📚 Learning larger quantities...")
    for i, (visual, number, description) in enumerate(larger_quantities, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=[number],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Larger quantities learned")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def teach_advanced_addition(engine):
    """Teach addition with larger numbers and carrying."""
    print("\n\n🧮 SCALING: ADVANCED ADDITION")
    print("=" * 50)
    
    # Advanced addition experiences
    advanced_additions = [
        # Single digit to larger numbers
        (["object"] * 5, ["object"] * 1, ["object"] * 6, ["five", "add", "one", "makes", "six"], "5+1=6"),
        (["object"] * 4, ["object"] * 2, ["object"] * 6, ["four", "add", "two", "makes", "six"], "4+2=6"),
        (["object"] * 3, ["object"] * 4, ["object"] * 7, ["three", "add", "four", "makes", "seven"], "3+4=7"),
        (["object"] * 5, ["object"] * 2, ["object"] * 7, ["five", "add", "two", "makes", "seven"], "5+2=7"),
        (["object"] * 4, ["object"] * 4, ["object"] * 8, ["four", "add", "four", "makes", "eight"], "4+4=8"),
        (["object"] * 5, ["object"] * 3, ["object"] * 8, ["five", "add", "three", "makes", "eight"], "5+3=8"),
        (["object"] * 6, ["object"] * 2, ["object"] * 8, ["six", "add", "two", "makes", "eight"], "6+2=8"),
        (["object"] * 4, ["object"] * 5, ["object"] * 9, ["four", "add", "five", "makes", "nine"], "4+5=9"),
        (["object"] * 6, ["object"] * 3, ["object"] * 9, ["six", "add", "three", "makes", "nine"], "6+3=9"),
        (["object"] * 5, ["object"] * 5, ["object"] * 10, ["five", "add", "five", "makes", "ten"], "5+5=10"),
    ]
    
    print("\n📚 Learning advanced addition...")
    for i, (group1, group2, combined, auditory, description) in enumerate(advanced_additions, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + combined,
            auditory=auditory + ["addition"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["combine", "add"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Advanced addition learned")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def teach_subtraction(engine):
    """Teach subtraction through removal experience."""
    print("\n\n➖ SCALING: SUBTRACTION OPERATIONS")
    print("=" * 50)
    
    # Subtraction experiences
    subtraction_experiences = [
        # Simple subtractions
        (["object"] * 3, ["object"] * 1, ["object"] * 2, ["three", "take", "one", "leaves", "two"], "3-1=2"),
        (["object"] * 4, ["object"] * 1, ["object"] * 3, ["four", "take", "one", "leaves", "three"], "4-1=3"),
        (["object"] * 5, ["object"] * 1, ["object"] * 4, ["five", "take", "one", "leaves", "four"], "5-1=4"),
        (["object"] * 4, ["object"] * 2, ["object"] * 2, ["four", "take", "two", "leaves", "two"], "4-2=2"),
        (["object"] * 5, ["object"] * 2, ["object"] * 3, ["five", "take", "two", "leaves", "three"], "5-2=3"),
        (["object"] * 6, ["object"] * 2, ["object"] * 4, ["six", "take", "two", "leaves", "four"], "6-2=4"),
        (["object"] * 5, ["object"] * 3, ["object"] * 2, ["five", "take", "three", "leaves", "two"], "5-3=2"),
        (["object"] * 6, ["object"] * 3, ["object"] * 3, ["six", "take", "three", "leaves", "three"], "6-3=3"),
        (["object"] * 7, ["object"] * 3, ["object"] * 4, ["seven", "take", "three", "leaves", "four"], "7-3=4"),
        (["object"] * 8, ["object"] * 3, ["object"] * 5, ["eight", "take", "three", "leaves", "five"], "8-3=5"),
    ]
    
    print("\n📚 Learning subtraction through removal...")
    for i, (start, remove, result, auditory, description) in enumerate(subtraction_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=start + ["minus"] + remove + ["equals"] + result,
            auditory=auditory + ["subtraction"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["remove", "subtract"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Subtraction learned")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def teach_word_problems(engine):
    """Teach mathematical word problems."""
    print("\n\n📝 SCALING: WORD PROBLEMS")
    print("=" * 50)
    
    # Word problem experiences
    word_problems = [
        # Simple story problems
        (["sarah", "has", "three", "apples", "gets", "two", "more", "total", "five"], "Sarah has 3, gets 2 more"),
        (["john", "has", "four", "toys", "gets", "one", "more", "total", "five"], "John has 4, gets 1 more"),
        (["mary", "has", "two", "books", "gets", "three", "more", "total", "five"], "Mary has 2, gets 3 more"),
        (["tom", "has", "five", "balls", "loses", "two", "left", "three"], "Tom has 5, loses 2"),
        (["lisa", "has", "six", "coins", "loses", "one", "left", "five"], "Lisa has 6, loses 1"),
        (["bob", "has", "seven", "cards", "loses", "three", "left", "four"], "Bob has 7, loses 3"),
    ]
    
    print("\n📚 Learning word problems...")
    for i, (story, description) in enumerate(word_problems, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=story + ["story", "problem"],
            auditory=["word", "problem", "solve"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["understand", "solve"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Word problems learned")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_advanced_scaling(engine):
    """Test the engine on advanced mathematical problems."""
    print("\n\n🔍 TESTING ADVANCED MATHEMATICAL SCALING")
    print("=" * 50)
    
    test_cases = [
        # Advanced addition
        {
            "input": (["object"] * 6, ["object"] * 3, "6+3=?"),
            "expected": "nine",
            "type": "Advanced Addition"
        },
        {
            "input": (["object"] * 7, ["object"] * 2, "7+2=?"),
            "expected": "nine", 
            "type": "Advanced Addition"
        },
        {
            "input": (["object"] * 4, ["object"] * 6, "4+6=?"),
            "expected": "ten",
            "type": "Advanced Addition"
        },
        
        # Subtraction
        {
            "input": (["object"] * 8, ["object"] * 2, "8-2=?"),
            "expected": "six",
            "type": "Subtraction"
        },
        {
            "input": (["object"] * 7, ["object"] * 4, "7-4=?"),
            "expected": "three",
            "type": "Subtraction"
        },
        {
            "input": (["object"] * 9, ["object"] * 3, "9-3=?"),
            "expected": "six",
            "type": "Subtraction"
        },
        
        # Word problems
        {
            "input": (["anna", "has", "four", "flowers", "gets", "three", "more", "total", "?"], "Anna word problem"),
            "expected": "seven",
            "type": "Word Problem"
        },
        {
            "input": (["mike", "has", "eight", "stickers", "loses", "two", "left", "?"], "Mike word problem"),
            "expected": "six",
            "type": "Word Problem"
        },
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        if len(test_case["input"]) == 3:
            test_input1, test_input2, description = test_case["input"]
            test_input = (test_input1, test_input2)
        else:
            test_input, description = test_case["input"]
        expected = test_case["expected"]
        test_type = test_case["type"]
        
        print(f"\n🧪 Test {i} ({test_type}): {description}")
        
        if test_type == "Word Problem":
            result = engine.live_experience(
                visual=test_input + ["story", "problem"],
                auditory=["solve", "calculate"],
                mood=0.4, arousal=0.7, attention=0.9,
                goals=["solve", "understand"], surprise=0.6, satisfaction=0.0
            )
        elif test_type == "Subtraction":
            result = engine.live_experience(
                visual=test_input[0] + ["minus"] + test_input[1] + ["equals"] + ["?"],
                auditory=["subtract", "take", "away"],
                mood=0.4, arousal=0.7, attention=0.9,
                goals=["subtract", "calculate"], surprise=0.5, satisfaction=0.0
            )
        else:  # Addition
            result = engine.live_experience(
                visual=test_input[0] + ["plus"] + test_input[1] + ["equals"] + ["?"],
                auditory=["add", "combine"],
                mood=0.4, arousal=0.7, attention=0.9,
                goals=["add", "calculate"], surprise=0.5, satisfaction=0.0
            )
        
        field = result['activation_field']
        expected_activation = field.get(expected, 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        
        # Show other relevant activations
        relevant_symbols = ['add', 'take', 'makes', 'leaves', 'total', 'left']
        for symbol in relevant_symbols:
            if symbol in field and abs(field[symbol]) > 0.5:
                print(f"   '{symbol}' activation: {field[symbol]:.3f}")
        
        success = abs(expected_activation) > 0.5
        results.append((description, test_type, success, expected_activation))
        
        if success:
            print(f"   ✅ CORRECT: {test_type} successful")
        else:
            print(f"   ❌ INCORRECT: {test_type} failed")
    
    return results


def run_advanced_scaling_test():
    """Run the complete advanced mathematical scaling test."""
    print("🚀 ADVANCED MATHEMATICAL SCALING TEST")
    print("=" * 70)
    print("Testing limits of quantity-grounded temporal wave cognition")
    print("=" * 70)
    
    start_time = time.time()
    
    # Start with the basic quantity-grounded foundation
    engine = TemporalCognitionEngine()
    
    # Quick foundation (abbreviated from previous success)
    print("🏗️ BUILDING FOUNDATION...")
    
    # Basic quantities 1-5 (abbreviated)
    for num, word in [(1, "one"), (2, "two"), (3, "three"), (4, "four"), (5, "five")]:
        engine.live_experience(
            visual=["object"] * num + ["quantity"],
            auditory=[word],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn"], surprise=0.3, satisfaction=0.7
        )
    
    # Basic addition (abbreviated)
    basic_additions = [
        (1, 1, 2), (2, 1, 3), (1, 2, 3), (2, 2, 4), (3, 1, 4), (3, 2, 5), (2, 3, 5)
    ]
    
    for a, b, c in basic_additions:
        num_words = ["", "one", "two", "three", "four", "five"]
        engine.live_experience(
            visual=["object"] * a + ["plus"] + ["object"] * b + ["equals"] + ["object"] * c,
            auditory=[num_words[a], "add", num_words[b], "makes", num_words[c]],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["add"], surprise=0.3, satisfaction=0.7
        )
    
    print("✅ Foundation established")
    
    # Now scale up
    teach_larger_quantities(engine)
    teach_advanced_addition(engine)
    teach_subtraction(engine)
    teach_word_problems(engine)
    
    # Test advanced capabilities
    results = test_advanced_scaling(engine)
    
    end_time = time.time()
    
    # Analysis
    print("\n\n📊 ADVANCED SCALING RESULTS")
    print("=" * 70)
    
    # Group results by type
    addition_results = [r for r in results if r[1] == "Advanced Addition"]
    subtraction_results = [r for r in results if r[1] == "Subtraction"]
    word_problem_results = [r for r in results if r[1] == "Word Problem"]
    
    print(f"\n🧮 ADVANCED ADDITION:")
    correct_addition = sum(1 for r in addition_results if r[2])
    print(f"   Correct: {correct_addition}/{len(addition_results)}")
    for desc, _, success, activation in addition_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n➖ SUBTRACTION:")
    correct_subtraction = sum(1 for r in subtraction_results if r[2])
    print(f"   Correct: {correct_subtraction}/{len(subtraction_results)}")
    for desc, _, success, activation in subtraction_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n📝 WORD PROBLEMS:")
    correct_word = sum(1 for r in word_problem_results if r[2])
    print(f"   Correct: {correct_word}/{len(word_problem_results)}")
    for desc, _, success, activation in word_problem_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = sum(1 for r in results if r[2])
    total_tests = len(results)
    
    print(f"\n🎯 OVERALL SCALING PERFORMANCE:")
    print(f"   Total correct: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print(f"   Learning time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n🧠 FINAL COGNITIVE STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active symbols: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    # Assessment
    if total_correct/total_tests >= 0.8:
        print(f"\n🎉 EXCELLENT SCALING: System handles advanced mathematical reasoning!")
    elif total_correct/total_tests >= 0.6:
        print(f"\n👍 GOOD SCALING: System shows promise for complex problems")
    elif total_correct/total_tests >= 0.4:
        print(f"\n🤔 PARTIAL SCALING: Some advanced capabilities emerging")
    else:
        print(f"\n⚠️ LIMITED SCALING: System struggles with complexity")
    
    print(f"\n📈 SCALING ANALYSIS:")
    print(f"   Addition scaling: {correct_addition}/{len(addition_results)} ({correct_addition/len(addition_results)*100:.1f}%)")
    print(f"   Subtraction scaling: {correct_subtraction}/{len(subtraction_results)} ({correct_subtraction/len(subtraction_results)*100:.1f}%)")
    print(f"   Word problem scaling: {correct_word}/{len(word_problem_results)} ({correct_word/len(word_problem_results)*100:.1f}%)")


if __name__ == "__main__":
    run_advanced_scaling_test() 