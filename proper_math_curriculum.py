#!/usr/bin/env python3
"""
Proper Mathematical Curriculum
Teaching math the way humans actually learn: step by step, grade by grade.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def kindergarten_math(engine):
    """Kindergarten: Basic quantities, counting, and simple addition facts."""
    print("🎒 KINDERGARTEN MATHEMATICS")
    print("=" * 50)
    
    # Phase 1: Subitizing (instant recognition of small quantities)
    print("\n📚 Learning subitizing (instant recognition)...")
    subitizing_experiences = [
        (["dot"], "one", "instantly see one"),
        (["dot", "dot"], "two", "instantly see two"),
        (["dot", "dot", "dot"], "three", "instantly see three"),
        (["dot", "dot", "dot", "dot"], "four", "instantly see four"),
        # Practice with different objects
        (["star"], "one", "one star"),
        (["star", "star"], "two", "two stars"),
        (["circle"], "one", "one circle"),
        (["circle", "circle", "circle"], "three", "three circles"),
    ]
    
    for i, (visual, number, description) in enumerate(subitizing_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["instant", "recognize"],
            auditory=[number, "quick"],
            mood=0.7, arousal=0.6, attention=0.9,
            goals=["recognize", "instant"], surprise=0.2, satisfaction=0.8
        )
        time.sleep(0.03)
    
    # Phase 2: Counting sequence to 10
    print("\n📚 Learning counting sequence to 10...")
    counting_experiences = [
        (["finger"], ["one"], "count one"),
        (["finger", "finger"], ["one", "two"], "count to two"),
        (["finger", "finger", "finger"], ["one", "two", "three"], "count to three"),
        (["finger", "finger", "finger", "finger"], ["one", "two", "three", "four"], "count to four"),
        (["finger"] * 5, ["one", "two", "three", "four", "five"], "count to five"),
        (["finger"] * 6, ["one", "two", "three", "four", "five", "six"], "count to six"),
        (["finger"] * 7, ["one", "two", "three", "four", "five", "six", "seven"], "count to seven"),
        (["finger"] * 8, ["one", "two", "three", "four", "five", "six", "seven", "eight"], "count to eight"),
        (["finger"] * 9, ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], "count to nine"),
        (["finger"] * 10, ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"], "count to ten"),
    ]
    
    for i, (visual, auditory, description) in enumerate(counting_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["counting", "sequence"],
            auditory=auditory + ["count", "order"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["count", "sequence"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Phase 3: Addition facts to 5 (concrete)
    print("\n📚 Learning addition facts to 5...")
    addition_facts_5 = [
        # Facts that make 2
        (["dot"], ["dot"], ["dot", "dot"], ["one", "plus", "one", "equals", "two"], "1+1=2"),
        
        # Facts that make 3
        (["dot"], ["dot", "dot"], ["dot", "dot", "dot"], ["one", "plus", "two", "equals", "three"], "1+2=3"),
        (["dot", "dot"], ["dot"], ["dot", "dot", "dot"], ["two", "plus", "one", "equals", "three"], "2+1=3"),
        
        # Facts that make 4
        (["dot"], ["dot", "dot", "dot"], ["dot", "dot", "dot", "dot"], ["one", "plus", "three", "equals", "four"], "1+3=4"),
        (["dot", "dot"], ["dot", "dot"], ["dot", "dot", "dot", "dot"], ["two", "plus", "two", "equals", "four"], "2+2=4"),
        (["dot", "dot", "dot"], ["dot"], ["dot", "dot", "dot", "dot"], ["three", "plus", "one", "equals", "four"], "3+1=4"),
        
        # Facts that make 5
        (["dot"], ["dot", "dot", "dot", "dot"], ["dot"] * 5, ["one", "plus", "four", "equals", "five"], "1+4=5"),
        (["dot", "dot"], ["dot", "dot", "dot"], ["dot"] * 5, ["two", "plus", "three", "equals", "five"], "2+3=5"),
        (["dot", "dot", "dot"], ["dot", "dot"], ["dot"] * 5, ["three", "plus", "two", "equals", "five"], "3+2=5"),
        (["dot", "dot", "dot", "dot"], ["dot"], ["dot"] * 5, ["four", "plus", "one", "equals", "five"], "4+1=5"),
    ]
    
    for i, (group1, group2, total, auditory, description) in enumerate(addition_facts_5, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + total,
            auditory=auditory + ["fact", "memorize"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn", "fact"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.03)
    
    print(f"\n✅ Kindergarten math completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")


def first_grade_math(engine):
    """1st Grade: Addition facts to 10, counting strategies, subtraction."""
    print("\n\n📚 FIRST GRADE MATHEMATICS")
    print("=" * 50)
    
    # Phase 1: Addition facts to 10 (systematic)
    print("\n📚 Learning all addition facts to 10...")
    addition_facts_10 = [
        # Facts that make 6
        (["dot"] * 1, ["dot"] * 5, ["dot"] * 6, ["one", "plus", "five", "equals", "six"], "1+5=6"),
        (["dot"] * 2, ["dot"] * 4, ["dot"] * 6, ["two", "plus", "four", "equals", "six"], "2+4=6"),
        (["dot"] * 3, ["dot"] * 3, ["dot"] * 6, ["three", "plus", "three", "equals", "six"], "3+3=6"),
        (["dot"] * 4, ["dot"] * 2, ["dot"] * 6, ["four", "plus", "two", "equals", "six"], "4+2=6"),
        (["dot"] * 5, ["dot"] * 1, ["dot"] * 6, ["five", "plus", "one", "equals", "six"], "5+1=6"),
        
        # Facts that make 7
        (["dot"] * 1, ["dot"] * 6, ["dot"] * 7, ["one", "plus", "six", "equals", "seven"], "1+6=7"),
        (["dot"] * 2, ["dot"] * 5, ["dot"] * 7, ["two", "plus", "five", "equals", "seven"], "2+5=7"),
        (["dot"] * 3, ["dot"] * 4, ["dot"] * 7, ["three", "plus", "four", "equals", "seven"], "3+4=7"),
        (["dot"] * 4, ["dot"] * 3, ["dot"] * 7, ["four", "plus", "three", "equals", "seven"], "4+3=7"),
        (["dot"] * 5, ["dot"] * 2, ["dot"] * 7, ["five", "plus", "two", "equals", "seven"], "5+2=7"),
        (["dot"] * 6, ["dot"] * 1, ["dot"] * 7, ["six", "plus", "one", "equals", "seven"], "6+1=7"),
        
        # Facts that make 8
        (["dot"] * 1, ["dot"] * 7, ["dot"] * 8, ["one", "plus", "seven", "equals", "eight"], "1+7=8"),
        (["dot"] * 2, ["dot"] * 6, ["dot"] * 8, ["two", "plus", "six", "equals", "eight"], "2+6=8"),
        (["dot"] * 3, ["dot"] * 5, ["dot"] * 8, ["three", "plus", "five", "equals", "eight"], "3+5=8"),
        (["dot"] * 4, ["dot"] * 4, ["dot"] * 8, ["four", "plus", "four", "equals", "eight"], "4+4=8"),
        (["dot"] * 5, ["dot"] * 3, ["dot"] * 8, ["five", "plus", "three", "equals", "eight"], "5+3=8"),
        (["dot"] * 6, ["dot"] * 2, ["dot"] * 8, ["six", "plus", "two", "equals", "eight"], "6+2=8"),
        (["dot"] * 7, ["dot"] * 1, ["dot"] * 8, ["seven", "plus", "one", "equals", "eight"], "7+1=8"),
        
        # Facts that make 9
        (["dot"] * 1, ["dot"] * 8, ["dot"] * 9, ["one", "plus", "eight", "equals", "nine"], "1+8=9"),
        (["dot"] * 2, ["dot"] * 7, ["dot"] * 9, ["two", "plus", "seven", "equals", "nine"], "2+7=9"),
        (["dot"] * 3, ["dot"] * 6, ["dot"] * 9, ["three", "plus", "six", "equals", "nine"], "3+6=9"),
        (["dot"] * 4, ["dot"] * 5, ["dot"] * 9, ["four", "plus", "five", "equals", "nine"], "4+5=9"),
        (["dot"] * 5, ["dot"] * 4, ["dot"] * 9, ["five", "plus", "four", "equals", "nine"], "5+4=9"),
        (["dot"] * 6, ["dot"] * 3, ["dot"] * 9, ["six", "plus", "three", "equals", "nine"], "6+3=9"),
        (["dot"] * 7, ["dot"] * 2, ["dot"] * 9, ["seven", "plus", "two", "equals", "nine"], "7+2=9"),
        (["dot"] * 8, ["dot"] * 1, ["dot"] * 9, ["eight", "plus", "one", "equals", "nine"], "8+1=9"),
        
        # Facts that make 10
        (["dot"] * 1, ["dot"] * 9, ["dot"] * 10, ["one", "plus", "nine", "equals", "ten"], "1+9=10"),
        (["dot"] * 2, ["dot"] * 8, ["dot"] * 10, ["two", "plus", "eight", "equals", "ten"], "2+8=10"),
        (["dot"] * 3, ["dot"] * 7, ["dot"] * 10, ["three", "plus", "seven", "equals", "ten"], "3+7=10"),
        (["dot"] * 4, ["dot"] * 6, ["dot"] * 10, ["four", "plus", "six", "equals", "ten"], "4+6=10"),
        (["dot"] * 5, ["dot"] * 5, ["dot"] * 10, ["five", "plus", "five", "equals", "ten"], "5+5=10"),
        (["dot"] * 6, ["dot"] * 4, ["dot"] * 10, ["six", "plus", "four", "equals", "ten"], "6+4=10"),
        (["dot"] * 7, ["dot"] * 3, ["dot"] * 10, ["seven", "plus", "three", "equals", "ten"], "7+3=10"),
        (["dot"] * 8, ["dot"] * 2, ["dot"] * 10, ["eight", "plus", "two", "equals", "ten"], "8+2=10"),
        (["dot"] * 9, ["dot"] * 1, ["dot"] * 10, ["nine", "plus", "one", "equals", "ten"], "9+1=10"),
    ]
    
    for i, (group1, group2, total, auditory, description) in enumerate(addition_facts_10, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + total,
            auditory=auditory + ["fact", "automatic"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["memorize", "automatic"], surprise=0.2, satisfaction=0.8
        )
        time.sleep(0.02)
    
    # Phase 2: Counting strategies
    print("\n📚 Learning counting strategies...")
    counting_strategies = [
        # Count up from larger number
        (["seven", "count", "up", "two", "more"], ["seven", "eight", "nine"], "7+2 by counting up"),
        (["six", "count", "up", "three", "more"], ["six", "seven", "eight", "nine"], "6+3 by counting up"),
        (["eight", "count", "up", "one", "more"], ["eight", "nine"], "8+1 by counting up"),
        (["five", "count", "up", "four", "more"], ["five", "six", "seven", "eight", "nine"], "5+4 by counting up"),
        
        # Count back for subtraction
        (["nine", "count", "back", "two"], ["nine", "eight", "seven"], "9-2 by counting back"),
        (["eight", "count", "back", "three"], ["eight", "seven", "six", "five"], "8-3 by counting back"),
        (["ten", "count", "back", "one"], ["ten", "nine"], "10-1 by counting back"),
        (["seven", "count", "back", "four"], ["seven", "six", "five", "four", "three"], "7-4 by counting back"),
    ]
    
    for i, (visual, auditory, description) in enumerate(counting_strategies, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["strategy", "counting"],
            auditory=auditory + ["strategy", "method"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["strategy", "method"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Phase 3: Subtraction as inverse
    print("\n📚 Learning subtraction as inverse of addition...")
    subtraction_inverse = [
        # If 2+3=5, then 5-3=2 and 5-2=3
        (["two", "plus", "three", "equals", "five"], ["five", "minus", "three", "equals", "two"], "2+3=5, so 5-3=2"),
        (["three", "plus", "two", "equals", "five"], ["five", "minus", "two", "equals", "three"], "3+2=5, so 5-2=3"),
        (["four", "plus", "one", "equals", "five"], ["five", "minus", "one", "equals", "four"], "4+1=5, so 5-1=4"),
        (["three", "plus", "four", "equals", "seven"], ["seven", "minus", "four", "equals", "three"], "3+4=7, so 7-4=3"),
        (["five", "plus", "two", "equals", "seven"], ["seven", "minus", "two", "equals", "five"], "5+2=7, so 7-2=5"),
        (["four", "plus", "four", "equals", "eight"], ["eight", "minus", "four", "equals", "four"], "4+4=8, so 8-4=4"),
        (["six", "plus", "three", "equals", "nine"], ["nine", "minus", "three", "equals", "six"], "6+3=9, so 9-3=6"),
        (["five", "plus", "five", "equals", "ten"], ["ten", "minus", "five", "equals", "five"], "5+5=10, so 10-5=5"),
    ]
    
    for i, (addition, subtraction, description) in enumerate(subtraction_inverse, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=addition + ["inverse"] + subtraction,
            auditory=["inverse", "opposite", "related"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["understand", "relate"], surprise=0.4, satisfaction=0.8
        )
        time.sleep(0.03)
    
    print(f"\n✅ First grade math completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_grade_level_math(engine, grade_level):
    """Test mathematical understanding at specific grade level."""
    print(f"\n\n🔍 TESTING {grade_level.upper()} LEVEL MATHEMATICS")
    print("=" * 50)
    
    if grade_level == "kindergarten":
        test_cases = [
            # Subitizing tests
            (["dot", "dot", "dot"], "instant recognition", "three"),
            (["star", "star"], "instant recognition", "two"),
            
            # Basic addition facts to 5
            (["dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "1+2=?", "three"),
            (["dot", "dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "2+2=?", "four"),
            (["dot", "dot", "dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "3+2=?", "five"),
        ]
    
    elif grade_level == "first_grade":
        test_cases = [
            # Addition facts to 10
            (["dot"] * 6 + ["plus"] + ["dot"] * 3 + ["equals"] + ["?"], "6+3=?", "nine"),
            (["dot"] * 7 + ["plus"] + ["dot"] * 2 + ["equals"] + ["?"], "7+2=?", "nine"),
            (["dot"] * 4 + ["plus"] + ["dot"] * 6 + ["equals"] + ["?"], "4+6=?", "ten"),
            
            # Subtraction
            (["dot"] * 8 + ["minus"] + ["dot"] * 3 + ["equals"] + ["?"], "8-3=?", "five"),
            (["dot"] * 9 + ["minus"] + ["dot"] * 4 + ["equals"] + ["?"], "9-4=?", "five"),
            (["dot"] * 10 + ["minus"] + ["dot"] * 2 + ["equals"] + ["?"], "10-2=?", "eight"),
        ]
    
    results = []
    for i, (visual, description, expected) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {description}")
        
        result = engine.live_experience(
            visual=visual,
            auditory=["test", "solve"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["solve", "recall"], surprise=0.5, satisfaction=0.0
        )
        
        field = result['activation_field']
        expected_activation = field.get(expected, 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        
        # Show other strong activations
        strong_activations = [(k, v) for k, v in field.items() if abs(v) > 0.5 and k != expected]
        if strong_activations:
            print(f"   Other activations: {strong_activations[:3]}")
        
        success = abs(expected_activation) > 0.5
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   ✅ CORRECT: {description}")
        else:
            print(f"   ❌ INCORRECT: {description}")
    
    return results


def run_proper_curriculum():
    """Run the complete proper mathematical curriculum."""
    print("🎓 PROPER MATHEMATICAL CURRICULUM")
    print("=" * 70)
    print("Teaching math following actual child development stages")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Kindergarten curriculum
    kindergarten_math(engine)
    k_results = test_grade_level_math(engine, "kindergarten")
    
    # First grade curriculum
    first_grade_math(engine)
    first_results = test_grade_level_math(engine, "first_grade")
    
    end_time = time.time()
    
    # Analysis
    print("\n\n📊 CURRICULUM RESULTS")
    print("=" * 70)
    
    print(f"\n🎒 KINDERGARTEN LEVEL:")
    k_correct = sum(1 for _, success, _ in k_results if success)
    print(f"   Correct: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
    for desc, success, activation in k_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n📚 FIRST GRADE LEVEL:")
    first_correct = sum(1 for _, success, _ in first_results if success)
    print(f"   Correct: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
    for desc, success, activation in first_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = k_correct + first_correct
    total_tests = len(k_results) + len(first_results)
    
    print(f"\n🎯 OVERALL CURRICULUM PERFORMANCE:")
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
    if total_correct/total_tests >= 0.9:
        print(f"\n🎉 EXCELLENT: Proper curriculum achieves outstanding results!")
        print(f"   Step-by-step learning following natural development works!")
    elif total_correct/total_tests >= 0.7:
        print(f"\n👍 GOOD: Proper curriculum shows strong improvement")
        print(f"   Systematic learning approach is effective")
    elif total_correct/total_tests >= 0.5:
        print(f"\n🤔 MODERATE: Some improvement with proper curriculum")
        print(f"   Foundation building helps but needs refinement")
    else:
        print(f"\n⚠️ LIMITED: Curriculum approach needs adjustment")
    
    print(f"\n📈 CURRICULUM ANALYSIS:")
    print(f"   Kindergarten mastery: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
    print(f"   First grade mastery: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
    
    if k_correct/len(k_results) > first_correct/len(first_results):
        print(f"   📝 Pattern: Strong foundation, complexity challenges")
    elif first_correct/len(first_results) > k_correct/len(k_results):
        print(f"   📝 Pattern: Building momentum with advanced concepts")
    else:
        print(f"   📝 Pattern: Consistent performance across grade levels")


if __name__ == "__main__":
    run_proper_curriculum() 