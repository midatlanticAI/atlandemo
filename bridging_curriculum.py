#!/usr/bin/env python3
"""
Bridging Mathematical Curriculum
Focus on the critical transition from kindergarten facts to first grade operations.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def bridge_to_first_grade(engine):
    """Bridge from kindergarten facts to first grade through systematic scaffolding."""
    print("🌉 BRIDGING TO FIRST GRADE MATHEMATICS")
    print("=" * 50)
    
    # Phase 1: Reinforce kindergarten facts with different representations
    print("\n📚 Reinforcing kindergarten facts...")
    reinforcement_experiences = [
        # 1+1=2 in multiple ways
        (["1", "+", "1", "=", "2"], ["one", "plus", "one", "equals", "two"], "1+1=2 with numerals"),
        (["finger"] + ["finger"], ["one", "plus", "one", "equals", "two"], "1+1=2 with fingers"),
        
        # 2+1=3 in multiple ways
        (["2", "+", "1", "=", "3"], ["two", "plus", "one", "equals", "three"], "2+1=3 with numerals"),
        (["finger", "finger"] + ["finger"], ["two", "plus", "one", "equals", "three"], "2+1=3 with fingers"),
        
        # 1+2=3 in multiple ways
        (["1", "+", "2", "=", "3"], ["one", "plus", "two", "equals", "three"], "1+2=3 with numerals"),
        (["finger"] + ["finger", "finger"], ["one", "plus", "two", "equals", "three"], "1+2=3 with fingers"),
        
        # 2+2=4 in multiple ways
        (["2", "+", "2", "=", "4"], ["two", "plus", "two", "equals", "four"], "2+2=4 with numerals"),
        (["finger", "finger"] + ["finger", "finger"], ["two", "plus", "two", "equals", "four"], "2+2=4 with fingers"),
        
        # 3+2=5 in multiple ways
        (["3", "+", "2", "=", "5"], ["three", "plus", "two", "equals", "five"], "3+2=5 with numerals"),
        (["finger", "finger", "finger"] + ["finger", "finger"], ["three", "plus", "two", "equals", "five"], "3+2=5 with fingers"),
        
        # 2+3=5 in multiple ways
        (["2", "+", "3", "=", "5"], ["two", "plus", "three", "equals", "five"], "2+3=5 with numerals"),
        (["finger", "finger"] + ["finger", "finger", "finger"], ["two", "plus", "three", "equals", "five"], "2+3=5 with fingers"),
    ]
    
    for i, (visual, auditory, description) in enumerate(reinforcement_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["reinforce", "known"],
            auditory=auditory + ["reinforce", "known"],
            mood=0.8, arousal=0.5, attention=0.9,
            goals=["reinforce", "strengthen"], surprise=0.1, satisfaction=0.9
        )
        time.sleep(0.02)
    
    # Phase 2: Introduce facts that make 6 (building on 5)
    print("\n📚 Building facts that make 6...")
    facts_to_6 = [
        # Start with what they know: 5+1=6
        (["5", "+", "1", "=", "6"], ["five", "plus", "one", "equals", "six"], "5+1=6 (building on 5)"),
        (["dot"] * 5 + ["plus"] + ["dot"] + ["equals"] + ["dot"] * 6, ["five", "plus", "one", "equals", "six"], "5+1=6 with dots"),
        
        # Then 1+5=6
        (["1", "+", "5", "=", "6"], ["one", "plus", "five", "equals", "six"], "1+5=6 (same as 5+1)"),
        (["dot"] + ["plus"] + ["dot"] * 5 + ["equals"] + ["dot"] * 6, ["one", "plus", "five", "equals", "six"], "1+5=6 with dots"),
        
        # 4+2=6 (building on 4)
        (["4", "+", "2", "=", "6"], ["four", "plus", "two", "equals", "six"], "4+2=6 (building on 4)"),
        (["dot"] * 4 + ["plus"] + ["dot"] * 2 + ["equals"] + ["dot"] * 6, ["four", "plus", "two", "equals", "six"], "4+2=6 with dots"),
        
        # 2+4=6
        (["2", "+", "4", "=", "6"], ["two", "plus", "four", "equals", "six"], "2+4=6 (same as 4+2)"),
        (["dot"] * 2 + ["plus"] + ["dot"] * 4 + ["equals"] + ["dot"] * 6, ["two", "plus", "four", "equals", "six"], "2+4=6 with dots"),
        
        # 3+3=6
        (["3", "+", "3", "=", "6"], ["three", "plus", "three", "equals", "six"], "3+3=6 (doubles)"),
        (["dot"] * 3 + ["plus"] + ["dot"] * 3 + ["equals"] + ["dot"] * 6, ["three", "plus", "three", "equals", "six"], "3+3=6 with dots"),
    ]
    
    for i, (visual, auditory, description) in enumerate(facts_to_6, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["new", "six"],
            auditory=auditory + ["new", "six"],
            mood=0.6, arousal=0.6, attention=0.9,
            goals=["learn", "six"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.02)
    
    # Phase 3: Introduce facts that make 7 (building on 6)
    print("\n📚 Building facts that make 7...")
    facts_to_7 = [
        # Start with what they know: 6+1=7
        (["6", "+", "1", "=", "7"], ["six", "plus", "one", "equals", "seven"], "6+1=7 (building on 6)"),
        (["dot"] * 6 + ["plus"] + ["dot"] + ["equals"] + ["dot"] * 7, ["six", "plus", "one", "equals", "seven"], "6+1=7 with dots"),
        
        # 1+6=7
        (["1", "+", "6", "=", "7"], ["one", "plus", "six", "equals", "seven"], "1+6=7 (same as 6+1)"),
        (["dot"] + ["plus"] + ["dot"] * 6 + ["equals"] + ["dot"] * 7, ["one", "plus", "six", "equals", "seven"], "1+6=7 with dots"),
        
        # 5+2=7 (building on 5)
        (["5", "+", "2", "=", "7"], ["five", "plus", "two", "equals", "seven"], "5+2=7 (building on 5)"),
        (["dot"] * 5 + ["plus"] + ["dot"] * 2 + ["equals"] + ["dot"] * 7, ["five", "plus", "two", "equals", "seven"], "5+2=7 with dots"),
        
        # 2+5=7
        (["2", "+", "5", "=", "7"], ["two", "plus", "five", "equals", "seven"], "2+5=7 (same as 5+2)"),
        (["dot"] * 2 + ["plus"] + ["dot"] * 5 + ["equals"] + ["dot"] * 7, ["two", "plus", "five", "equals", "seven"], "2+5=7 with dots"),
        
        # 4+3=7 (building on 4)
        (["4", "+", "3", "=", "7"], ["four", "plus", "three", "equals", "seven"], "4+3=7 (building on 4)"),
        (["dot"] * 4 + ["plus"] + ["dot"] * 3 + ["equals"] + ["dot"] * 7, ["four", "plus", "three", "equals", "seven"], "4+3=7 with dots"),
        
        # 3+4=7
        (["3", "+", "4", "=", "7"], ["three", "plus", "four", "equals", "seven"], "3+4=7 (same as 4+3)"),
        (["dot"] * 3 + ["plus"] + ["dot"] * 4 + ["equals"] + ["dot"] * 7, ["three", "plus", "four", "equals", "seven"], "3+4=7 with dots"),
    ]
    
    for i, (visual, auditory, description) in enumerate(facts_to_7, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["new", "seven"],
            auditory=auditory + ["new", "seven"],
            mood=0.6, arousal=0.6, attention=0.9,
            goals=["learn", "seven"], surprise=0.4, satisfaction=0.7
        )
        time.sleep(0.02)
    
    # Phase 4: Strategy instruction - counting on
    print("\n📚 Learning counting on strategy...")
    counting_on_experiences = [
        # Start with easy ones
        (["5", "+", "1"], ["five", "six"], "5+1: start at 5, count on 1"),
        (["5", "+", "2"], ["five", "six", "seven"], "5+2: start at 5, count on 2"),
        (["6", "+", "1"], ["six", "seven"], "6+1: start at 6, count on 1"),
        (["6", "+", "2"], ["six", "seven", "eight"], "6+2: start at 6, count on 2"),
        (["4", "+", "3"], ["four", "five", "six", "seven"], "4+3: start at 4, count on 3"),
        (["3", "+", "4"], ["three", "four", "five", "six", "seven"], "3+4: start at 3, count on 4"),
        
        # Practice with larger numbers
        (["7", "+", "1"], ["seven", "eight"], "7+1: start at 7, count on 1"),
        (["6", "+", "3"], ["six", "seven", "eight", "nine"], "6+3: start at 6, count on 3"),
        (["5", "+", "3"], ["five", "six", "seven", "eight"], "5+3: start at 5, count on 3"),
    ]
    
    for i, (visual, auditory, description) in enumerate(counting_on_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["count", "on", "strategy"],
            auditory=auditory + ["count", "on", "strategy"],
            mood=0.5, arousal=0.7, attention=0.9,
            goals=["strategy", "count", "on"], surprise=0.5, satisfaction=0.8
        )
        time.sleep(0.03)
    
    print(f"\n[+] Bridging curriculum completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")


def test_bridging_success(engine):
    """Test the bridging curriculum effectiveness."""
    print(f"\n\n[SEARCH] TESTING BRIDGING SUCCESS")
    print("=" * 50)
    
    test_cases = [
        # Kindergarten level (should be solid)
        (["1", "+", "1", "=", "?"], "K: 1+1=?", "two"),
        (["2", "+", "2", "=", "?"], "K: 2+2=?", "four"),
        (["3", "+", "2", "=", "?"], "K: 3+2=?", "five"),
        
        # Bridge level (facts to 6 and 7)
        (["5", "+", "1", "=", "?"], "Bridge: 5+1=?", "six"),
        (["3", "+", "3", "=", "?"], "Bridge: 3+3=?", "six"),
        (["4", "+", "2", "=", "?"], "Bridge: 4+2=?", "six"),
        (["6", "+", "1", "=", "?"], "Bridge: 6+1=?", "seven"),
        (["3", "+", "4", "=", "?"], "Bridge: 3+4=?", "seven"),
        (["5", "+", "2", "=", "?"], "Bridge: 5+2=?", "seven"),
        
        # First grade level (using strategies)
        (["5", "+", "3", "=", "?"], "1st: 5+3=? (count on)", "eight"),
        (["6", "+", "3", "=", "?"], "1st: 6+3=? (count on)", "nine"),
        (["7", "+", "2", "=", "?"], "1st: 7+2=? (count on)", "nine"),
        (["4", "+", "5", "=", "?"], "1st: 4+5=? (count on)", "nine"),
        (["6", "+", "4", "=", "?"], "1st: 6+4=? (count on)", "ten"),
        (["7", "+", "3", "=", "?"], "1st: 7+3=? (count on)", "ten"),
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


def run_bridging_curriculum():
    """Run the bridging curriculum experiment."""
    print("🌉 BRIDGING MATHEMATICAL CURRICULUM")
    print("=" * 70)
    print("Systematic scaffolding from kindergarten to first grade")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Start with basic kindergarten foundation
    print("🎒 ESTABLISHING KINDERGARTEN FOUNDATION")
    print("=" * 50)
    
    # Quick kindergarten foundation
    k_foundation = [
        (["1", "+", "1", "=", "2"], ["one", "plus", "one", "equals", "two"], "1+1=2"),
        (["2", "+", "1", "=", "3"], ["two", "plus", "one", "equals", "three"], "2+1=3"),
        (["1", "+", "2", "=", "3"], ["one", "plus", "two", "equals", "three"], "1+2=3"),
        (["2", "+", "2", "=", "4"], ["two", "plus", "two", "equals", "four"], "2+2=4"),
        (["3", "+", "1", "=", "4"], ["three", "plus", "one", "equals", "four"], "3+1=4"),
        (["1", "+", "3", "=", "4"], ["one", "plus", "three", "equals", "four"], "1+3=4"),
        (["2", "+", "3", "=", "5"], ["two", "plus", "three", "equals", "five"], "2+3=5"),
        (["3", "+", "2", "=", "5"], ["three", "plus", "two", "equals", "five"], "3+2=5"),
        (["4", "+", "1", "=", "5"], ["four", "plus", "one", "equals", "five"], "4+1=5"),
        (["1", "+", "4", "=", "5"], ["one", "plus", "four", "equals", "five"], "1+4=5"),
    ]
    
    for i, (visual, auditory, description) in enumerate(k_foundation, 1):
        print(f"   Foundation {i}: {description}")
        engine.live_experience(
            visual=visual + ["foundation"],
            auditory=auditory + ["foundation"],
            mood=0.8, arousal=0.5, attention=0.9,
            goals=["foundation", "establish"], surprise=0.2, satisfaction=0.8
        )
        time.sleep(0.02)
    
    # Run bridging curriculum
    bridge_to_first_grade(engine)
    
    # Test results
    results = test_bridging_success(engine)
    
    end_time = time.time()
    
    # Analysis
    print("\n\n[DATA] BRIDGING CURRICULUM RESULTS")
    print("=" * 70)
    
    # Categorize results
    k_results = [r for r in results if r[0].startswith("K:")]
    bridge_results = [r for r in results if r[0].startswith("Bridge:")]
    first_results = [r for r in results if r[0].startswith("1st:")]
    
    print(f"\n🎒 KINDERGARTEN FOUNDATION:")
    k_correct = sum(1 for _, success, _ in k_results if success)
    if k_results:
        print(f"   Correct: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
        for desc, success, activation in k_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n🌉 BRIDGE CONCEPTS:")
    bridge_correct = sum(1 for _, success, _ in bridge_results if success)
    if bridge_results:
        print(f"   Correct: {bridge_correct}/{len(bridge_results)} ({bridge_correct/len(bridge_results)*100:.1f}%)")
        for desc, success, activation in bridge_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n📚 FIRST GRADE STRATEGIES:")
    first_correct = sum(1 for _, success, _ in first_results if success)
    if first_results:
        print(f"   Correct: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
        for desc, success, activation in first_results:
            status = "[+]" if success else "[-]"
            print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = sum(1 for _, success, _ in results if success)
    total_tests = len(results)
    
    print(f"\n[TARGET] OVERALL BRIDGING PERFORMANCE:")
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
        print(f"\n[PARTY] EXCELLENT: Bridging curriculum achieves outstanding results!")
        print(f"   Systematic scaffolding approach works brilliantly!")
    elif total_correct/total_tests >= 0.8:
        print(f"\n[STAR] VERY GOOD: Bridging curriculum shows strong performance")
        print(f"   Careful step-by-step progression is highly effective")
    elif total_correct/total_tests >= 0.7:
        print(f"\n👍 GOOD: Bridging curriculum shows solid improvement")
        print(f"   Scaffolding approach is effective")
    elif total_correct/total_tests >= 0.6:
        print(f"\n🤔 MODERATE: Some improvement with bridging")
        print(f"   Scaffolding helps but needs refinement")
    else:
        print(f"\n[WARN] LIMITED: Bridging approach needs adjustment")
    
    # Progression analysis
    print(f"\n[CHART] BRIDGING ANALYSIS:")
    if k_results:
        print(f"   Foundation mastery: {k_correct}/{len(k_results)} ({k_correct/len(k_results)*100:.1f}%)")
    if bridge_results:
        print(f"   Bridge mastery: {bridge_correct}/{len(bridge_results)} ({bridge_correct/len(bridge_results)*100:.1f}%)")
    if first_results:
        print(f"   Strategy mastery: {first_correct}/{len(first_results)} ({first_correct/len(first_results)*100:.1f}%)")
    
    # Success pattern analysis
    if k_results and bridge_results and first_results:
        k_rate = k_correct/len(k_results) if k_results else 0
        bridge_rate = bridge_correct/len(bridge_results) if bridge_results else 0
        first_rate = first_correct/len(first_results) if first_results else 0
        
        print(f"\n[SEARCH] LEARNING PROGRESSION:")
        print(f"   Foundation → Bridge: {k_rate:.1%} → {bridge_rate:.1%}")
        print(f"   Bridge → Strategy: {bridge_rate:.1%} → {first_rate:.1%}")
        
        if bridge_rate > k_rate and first_rate > bridge_rate:
            print(f"   [TARGET] IDEAL: Smooth progression across all levels")
        elif bridge_rate > k_rate:
            print(f"   [CHART] GOOD: Strong bridge building, strategy needs work")
        elif first_rate > bridge_rate:
            print(f"   🤔 MIXED: Foundation to bridge gap, but strategy improvement")
        else:
            print(f"   [WARN] CHALLENGE: Difficulty with complexity transitions")


if __name__ == "__main__":
    run_bridging_curriculum() 