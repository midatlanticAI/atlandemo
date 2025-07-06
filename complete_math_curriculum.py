#!/usr/bin/env python3
"""
Complete Mathematical Curriculum
Following the complete natural development sequence from pre-K through 2nd grade.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def pre_k_math(engine):
    """Pre-K: Basic concepts of quantity and one-to-one correspondence."""
    print("🧸 PRE-K MATHEMATICS")
    print("=" * 50)
    
    # Phase 1: One-to-one correspondence
    print("\n📚 Learning one-to-one correspondence...")
    correspondence_experiences = [
        (["child", "cup"], ["one", "child", "one", "cup"], "one child gets one cup"),
        (["child", "child", "cup", "cup"], ["each", "child", "one", "cup"], "each child gets one cup"),
        (["toy", "box"], ["one", "toy", "one", "box"], "one toy in one box"),
        (["toy", "toy", "toy", "box", "box", "box"], ["each", "toy", "one", "box"], "each toy in one box"),
        (["finger", "dot"], ["one", "finger", "one", "dot"], "one finger touches one dot"),
        (["finger", "finger", "dot", "dot"], ["each", "finger", "one", "dot"], "each finger touches one dot"),
    ]
    
    for i, (visual, auditory, description) in enumerate(correspondence_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["match", "correspond"],
            auditory=auditory + ["match", "correspond"],
            mood=0.8, arousal=0.5, attention=0.9,
            goals=["match", "correspond"], surprise=0.3, satisfaction=0.8
        )
        time.sleep(0.03)
    
    # Phase 2: More vs Less
    print("\n📚 Learning more vs less...")
    comparison_experiences = [
        (["dot", "dot", "dot"], ["dot"], ["three", "more", "than", "one"], "three is more than one"),
        (["dot"], ["dot", "dot", "dot"], ["one", "less", "than", "three"], "one is less than three"),
        (["dot", "dot"], ["dot", "dot", "dot", "dot"], ["two", "less", "than", "four"], "two is less than four"),
        (["dot", "dot", "dot", "dot"], ["dot", "dot"], ["four", "more", "than", "two"], "four is more than two"),
        (["star", "star", "star", "star", "star"], ["star"], ["five", "more", "than", "one"], "five is more than one"),
        (["circle"], ["circle", "circle", "circle"], ["one", "less", "than", "three"], "one is less than three"),
    ]
    
    for i, (group1, group2, auditory, description) in enumerate(comparison_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["compare"] + group2,
            auditory=auditory + ["compare"],
            mood=0.7, arousal=0.6, attention=0.8,
            goals=["compare", "understand"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Phase 3: Basic shapes and patterns
    print("\n📚 Learning basic shapes and patterns...")
    pattern_experiences = [
        (["circle", "square", "circle", "square"], ["pattern", "repeat"], "circle square pattern"),
        (["red", "blue", "red", "blue"], ["pattern", "color"], "red blue pattern"),
        (["big", "small", "big", "small"], ["pattern", "size"], "big small pattern"),
        (["dot", "dot", "line", "dot", "dot", "line"], ["pattern", "group"], "two dots line pattern"),
    ]
    
    for i, (visual, auditory, description) in enumerate(pattern_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["pattern", "sequence"],
            auditory=auditory + ["pattern", "sequence"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["pattern", "sequence"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.03)
    
    print(f"\n[+] Pre-K math completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")


def kindergarten_math_extended(engine):
    """Extended Kindergarten: More thorough subitizing and counting."""
    print("\n\n🎒 KINDERGARTEN MATHEMATICS (EXTENDED)")
    print("=" * 50)
    
    # Phase 1: Extensive subitizing practice
    print("\n📚 Extensive subitizing practice...")
    subitizing_extended = [
        # Different arrangements of same quantity
        (["dot"], "one", "one dot"),
        (["star"], "one", "one star"),
        (["circle"], "one", "one circle"),
        (["dot", "dot"], "two", "two dots side by side"),
        (["dot", "dot"], "two", "two dots vertical"),
        (["star", "star"], "two", "two stars"),
        (["dot", "dot", "dot"], "three", "three dots in line"),
        (["dot", "dot", "dot"], "three", "three dots in triangle"),
        (["star", "star", "star"], "three", "three stars"),
        (["circle", "circle", "circle"], "three", "three circles"),
        (["dot", "dot", "dot", "dot"], "four", "four dots in line"),
        (["dot", "dot", "dot", "dot"], "four", "four dots in square"),
        (["star", "star", "star", "star"], "four", "four stars"),
        (["dot", "dot", "dot", "dot", "dot"], "five", "five dots in line"),
        (["dot", "dot", "dot", "dot", "dot"], "five", "five dots scattered"),
        (["star", "star", "star", "star", "star"], "five", "five stars"),
    ]
    
    for i, (visual, number, description) in enumerate(subitizing_extended, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["instant", "see", "count"],
            auditory=[number, "instant", "recognize"],
            mood=0.7, arousal=0.6, attention=0.9,
            goals=["instant", "recognize"], surprise=0.2, satisfaction=0.8
        )
        time.sleep(0.02)
    
    # Phase 2: Counting with different objects
    print("\n📚 Counting with different objects...")
    counting_objects = [
        (["apple"], ["one"], "count one apple"),
        (["apple", "apple"], ["one", "two"], "count two apples"),
        (["apple", "apple", "apple"], ["one", "two", "three"], "count three apples"),
        (["ball"], ["one"], "count one ball"),
        (["ball", "ball"], ["one", "two"], "count two balls"),
        (["ball", "ball", "ball"], ["one", "two", "three"], "count three balls"),
        (["book"], ["one"], "count one book"),
        (["book", "book"], ["one", "two"], "count two books"),
        (["book", "book", "book"], ["one", "two", "three"], "count three books"),
        (["toy"], ["one"], "count one toy"),
        (["toy", "toy"], ["one", "two"], "count two toys"),
        (["toy", "toy", "toy"], ["one", "two", "three"], "count three toys"),
    ]
    
    for i, (visual, auditory, description) in enumerate(counting_objects, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["count", "objects"],
            auditory=auditory + ["count", "objects"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["count", "objects"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.02)
    
    # Phase 3: Number recognition
    print("\n📚 Number recognition...")
    number_recognition = [
        (["1"], ["one"], "recognize number 1"),
        (["2"], ["two"], "recognize number 2"),
        (["3"], ["three"], "recognize number 3"),
        (["4"], ["four"], "recognize number 4"),
        (["5"], ["five"], "recognize number 5"),
        (["1", "dot"], ["one", "dot"], "1 means one dot"),
        (["2", "dot", "dot"], ["two", "dots"], "2 means two dots"),
        (["3", "dot", "dot", "dot"], ["three", "dots"], "3 means three dots"),
        (["4", "dot", "dot", "dot", "dot"], ["four", "dots"], "4 means four dots"),
        (["5", "dot", "dot", "dot", "dot", "dot"], ["five", "dots"], "5 means five dots"),
    ]
    
    for i, (visual, auditory, description) in enumerate(number_recognition, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["number", "symbol"],
            auditory=auditory + ["number", "symbol"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["recognize", "symbol"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.02)
    
    # Phase 4: Addition facts to 5 (extensive practice)
    print("\n📚 Addition facts to 5 (extensive practice)...")
    addition_facts_extended = [
        # 1+1=2 in different contexts
        (["dot"], ["dot"], ["dot", "dot"], ["one", "plus", "one", "equals", "two"], "1+1=2 with dots"),
        (["apple"], ["apple"], ["apple", "apple"], ["one", "plus", "one", "equals", "two"], "1+1=2 with apples"),
        (["toy"], ["toy"], ["toy", "toy"], ["one", "plus", "one", "equals", "two"], "1+1=2 with toys"),
        
        # 2+1=3 in different contexts
        (["dot", "dot"], ["dot"], ["dot", "dot", "dot"], ["two", "plus", "one", "equals", "three"], "2+1=3 with dots"),
        (["apple", "apple"], ["apple"], ["apple", "apple", "apple"], ["two", "plus", "one", "equals", "three"], "2+1=3 with apples"),
        
        # 1+2=3 in different contexts
        (["dot"], ["dot", "dot"], ["dot", "dot", "dot"], ["one", "plus", "two", "equals", "three"], "1+2=3 with dots"),
        (["toy"], ["toy", "toy"], ["toy", "toy", "toy"], ["one", "plus", "two", "equals", "three"], "1+2=3 with toys"),
        
        # 2+2=4 in different contexts
        (["dot", "dot"], ["dot", "dot"], ["dot", "dot", "dot", "dot"], ["two", "plus", "two", "equals", "four"], "2+2=4 with dots"),
        (["apple", "apple"], ["apple", "apple"], ["apple", "apple", "apple", "apple"], ["two", "plus", "two", "equals", "four"], "2+2=4 with apples"),
        
        # 3+1=4 and 1+3=4
        (["dot", "dot", "dot"], ["dot"], ["dot", "dot", "dot", "dot"], ["three", "plus", "one", "equals", "four"], "3+1=4 with dots"),
        (["dot"], ["dot", "dot", "dot"], ["dot", "dot", "dot", "dot"], ["one", "plus", "three", "equals", "four"], "1+3=4 with dots"),
        
        # Facts that make 5
        (["dot"], ["dot", "dot", "dot", "dot"], ["dot"] * 5, ["one", "plus", "four", "equals", "five"], "1+4=5"),
        (["dot", "dot"], ["dot", "dot", "dot"], ["dot"] * 5, ["two", "plus", "three", "equals", "five"], "2+3=5"),
        (["dot", "dot", "dot"], ["dot", "dot"], ["dot"] * 5, ["three", "plus", "two", "equals", "five"], "3+2=5"),
        (["dot", "dot", "dot", "dot"], ["dot"], ["dot"] * 5, ["four", "plus", "one", "equals", "five"], "4+1=5"),
    ]
    
    for i, (group1, group2, total, auditory, description) in enumerate(addition_facts_extended, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + total,
            auditory=auditory + ["addition", "fact"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["learn", "addition"], surprise=0.2, satisfaction=0.8
        )
        time.sleep(0.02)
    
    print(f"\n[+] Extended kindergarten math completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_comprehensive_math(engine):
    """Comprehensive testing across all levels."""
    print(f"\n\n[SEARCH] COMPREHENSIVE MATHEMATICS TESTING")
    print("=" * 50)
    
    test_cases = [
        # Pre-K level
        (["dot", "dot", "dot"], "Pre-K: instant recognition", "three"),
        (["star", "star"], "Pre-K: instant recognition", "two"),
        
        # Kindergarten level
        (["dot"] + ["plus"] + ["dot"] + ["equals"] + ["?"], "K: 1+1=?", "two"),
        (["dot", "dot"] + ["plus"] + ["dot"] + ["equals"] + ["?"], "K: 2+1=?", "three"),
        (["dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "K: 1+2=?", "three"),
        (["dot", "dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "K: 2+2=?", "four"),
        (["dot", "dot", "dot"] + ["plus"] + ["dot", "dot"] + ["equals"] + ["?"], "K: 3+2=?", "five"),
        
        # First grade level
        (["dot"] * 3 + ["plus"] + ["dot"] * 4 + ["equals"] + ["?"], "1st: 3+4=?", "seven"),
        (["dot"] * 5 + ["plus"] + ["dot"] * 3 + ["equals"] + ["?"], "1st: 5+3=?", "eight"),
        (["dot"] * 4 + ["plus"] + ["dot"] * 5 + ["equals"] + ["?"], "1st: 4+5=?", "nine"),
        (["dot"] * 6 + ["plus"] + ["dot"] * 4 + ["equals"] + ["?"], "1st: 6+4=?", "ten"),
        
        # Subtraction
        (["dot"] * 5 + ["minus"] + ["dot"] * 2 + ["equals"] + ["?"], "1st: 5-2=?", "three"),
        (["dot"] * 7 + ["minus"] + ["dot"] * 3 + ["equals"] + ["?"], "1st: 7-3=?", "four"),
        (["dot"] * 8 + ["minus"] + ["dot"] * 3 + ["equals"] + ["?"], "1st: 8-3=?", "five"),
        (["dot"] * 9 + ["minus"] + ["dot"] * 4 + ["equals"] + ["?"], "1st: 9-4=?", "five"),
        (["dot"] * 10 + ["minus"] + ["dot"] * 2 + ["equals"] + ["?"], "1st: 10-2=?", "eight"),
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
            print(f"   [+] CORRECT: {description}")
        else:
            print(f"   [-] INCORRECT: {description}")
    
    return results


def run_complete_curriculum():
    """Run the complete mathematical curriculum."""
    print("🎓 COMPLETE MATHEMATICAL CURRICULUM")
    print("=" * 70)
    print("Following complete natural development from pre-K through 1st grade")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Pre-K curriculum
    pre_k_math(engine)
    
    # Extended kindergarten curriculum
    kindergarten_math_extended(engine)
    
    # Comprehensive testing
    results = test_comprehensive_math(engine)
    
    end_time = time.time()
    
    # Analysis
    print("\n\n[DATA] COMPLETE CURRICULUM RESULTS")
    print("=" * 70)
    
    # Categorize results
    pre_k_results = [r for r in results if r[0].startswith("Pre-K")]
    k_results = [r for r in results if r[0].startswith("K:")]
    first_results = [r for r in results if r[0].startswith("1st:")]
    
    print(f"\n🧸 PRE-K LEVEL:")
    pre_k_correct = sum(1 for _, success, _ in pre_k_results if success)
    if pre_k_results:
        print(f"   Correct: {pre_k_correct}/{len(pre_k_results)} ({pre_k_correct/len(pre_k_results)*100:.1f}%)")
        for desc, success, activation in pre_k_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n🎒 KINDERGARTEN LEVEL:")
    k_correct = sum(1 for _, success, _ in k_results if success)
    if k_results:
        print(f"   Correct: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
        for desc, success, activation in k_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n📚 FIRST GRADE LEVEL:")
    first_correct = sum(1 for _, success, _ in first_results if success)
    if first_results:
        print(f"   Correct: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
        for desc, success, activation in first_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = sum(1 for _, success, _ in results if success)
    total_tests = len(results)
    
    print(f"\n[TARGET] OVERALL CURRICULUM PERFORMANCE:")
    print(f"   Total correct: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print(f"   Learning time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n[BRAIN] FINAL COGNITIVE STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active symbols: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    # Assessment
    if total_correct/total_tests >= 0.9:
        print(f"\n[PARTY] EXCELLENT: Complete curriculum achieves outstanding results!")
        print(f"   Thorough step-by-step learning following natural development works!")
    elif total_correct/total_tests >= 0.8:
        print(f"\n[STAR] VERY GOOD: Complete curriculum shows strong performance")
        print(f"   Comprehensive foundation building is highly effective")
    elif total_correct/total_tests >= 0.7:
        print(f"\n👍 GOOD: Complete curriculum shows solid improvement")
        print(f"   Systematic learning approach is effective")
    elif total_correct/total_tests >= 0.6:
        print(f"\n🤔 MODERATE: Some improvement with complete curriculum")
        print(f"   Foundation building helps but needs refinement")
    else:
        print(f"\n[WARN] LIMITED: Curriculum approach needs significant adjustment")
    
    # Detailed analysis
    print(f"\n[CHART] DETAILED CURRICULUM ANALYSIS:")
    if pre_k_results:
        print(f"   Pre-K mastery: {pre_k_correct}/{len(pre_k_results)} ({pre_k_correct/len(pre_k_results)*100:.1f}%)")
    if k_results:
        print(f"   Kindergarten mastery: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
    if first_results:
        print(f"   First grade mastery: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
    
    # Performance progression analysis
    if pre_k_results and k_results and first_results:
        pre_k_rate = pre_k_correct/len(pre_k_results) if pre_k_results else 0
        k_rate = k_correct/len(k_results) if k_results else 0
        first_rate = first_correct/len(first_results) if first_results else 0
        
        print(f"\n[DATA] LEARNING PROGRESSION:")
        print(f"   Pre-K → K: {pre_k_rate:.1%} → {k_rate:.1%}")
        print(f"   K → 1st: {k_rate:.1%} → {first_rate:.1%}")
        
        if k_rate > pre_k_rate and first_rate > k_rate:
            print(f"   [CHART] Pattern: Consistent improvement across grade levels")
        elif k_rate > pre_k_rate:
            print(f"   [CHART] Pattern: Strong foundation building, complexity challenges")
        elif first_rate > k_rate:
            print(f"   [CHART] Pattern: Building momentum with practice")
        else:
            print(f"   [DATA] Pattern: Uneven development, needs targeted intervention")


if __name__ == "__main__":
    run_complete_curriculum() 