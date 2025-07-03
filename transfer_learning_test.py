#!/usr/bin/env python3
"""
Transfer Learning Test
Testing if the adaptive system's foundation breakthrough can transfer to new concepts
and enable advancement to higher mathematical thinking.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def establish_foundation(engine):
    """Quickly establish the foundation that worked in adaptive system."""
    print("🔄 ESTABLISHING PROVEN FOUNDATION")
    print("=" * 50)
    
    # The exact foundation that achieved 100% success
    foundation_experiences = [
        # Basic establishment
        (["2", "+", "1", "=", "3"], ["foundation"], "2+1=3"),
        (["3", "+", "2", "=", "5"], ["foundation"], "3+2=5"),
        (["4", "+", "1", "=", "5"], ["foundation"], "4+1=5"),
        (["5", "-", "2", "=", "3"], ["foundation"], "5-2=3"),
        
        # Concrete remediation that worked
        (["•", "•", "•"] + ["•", "•"], ["three", "plus", "two", "equals", "five"], "3+2=5 concrete"),
        (["★", "★", "★"] + ["★", "★"], ["three", "plus", "two", "equals", "five"], "3+2=5 stars"),
        (["○", "○", "○"] + ["○", "○"], ["three", "plus", "two", "equals", "five"], "3+2=5 circles"),
        (["•", "•", "•", "•"] + ["•", "•", "•", "•"], ["four", "plus", "four", "equals", "eight"], "4+4=8 concrete"),
        (["★", "★", "★", "★"] + ["★", "★", "★", "★"], ["four", "plus", "four", "equals", "eight"], "4+4=8 stars"),
        
        # Automaticity that partially worked
        (["6", "+", "4", "=", "10"], ["instant", "automatic"], "6+4=10 automatic"),
        (["10", "-", "4", "=", "6"], ["instant", "automatic"], "10-4=6 automatic"),
        (["5", "+", "5", "=", "10"], ["instant", "automatic"], "5+5=10 automatic"),
        (["10", "-", "5", "=", "5"], ["instant", "automatic"], "10-5=5 automatic"),
        (["7", "+", "3", "=", "10"], ["instant", "automatic"], "7+3=10 automatic"),
        (["10", "-", "3", "=", "7"], ["instant", "automatic"], "10-3=7 automatic"),
    ]
    
    for i, (visual, auditory, description) in enumerate(foundation_experiences, 1):
        print(f"   Foundation {i}: {description}")
        engine.live_experience(
            visual=visual + ["solid", "foundation"],
            auditory=auditory + ["solid", "foundation"],
            mood=0.8, arousal=0.4, attention=0.9,
            goals=["solid", "foundation"], surprise=0.1, satisfaction=0.9
        )
        time.sleep(0.02)
    
    print(f"\n✅ Foundation established")


def test_immediate_transfer(engine):
    """Test if foundation knowledge transfers to similar problems."""
    print("\n\n🔄 IMMEDIATE TRANSFER TEST")
    print("=" * 50)
    
    transfer_tests = [
        # Direct transfer - same facts in different format
        (["3", "+", "2", "=", "?"], "Direct transfer: 3+2", "five"),
        (["4", "+", "4", "=", "?"], "Direct transfer: 4+4", "eight"),
        (["7", "-", "3", "=", "?"], "Direct transfer: 7-3", "four"),
        
        # Near transfer - similar facts
        (["2", "+", "3", "=", "?"], "Near transfer: 2+3", "five"),
        (["5", "-", "1", "=", "?"], "Near transfer: 5-1", "four"),
        (["6", "+", "2", "=", "?"], "Near transfer: 6+2", "eight"),
        
        # Pattern transfer - applying learned patterns
        (["1", "+", "4", "=", "?"], "Pattern transfer: 1+4", "five"),
        (["8", "-", "4", "=", "?"], "Pattern transfer: 8-4", "four"),
        (["3", "+", "5", "=", "?"], "Pattern transfer: 3+5", "eight"),
    ]
    
    transfer_results = []
    for i, (visual, description, expected) in enumerate(transfer_tests, 1):
        print(f"\n🧪 Transfer Test {i}: {description}")
        
        result = engine.live_experience(
            visual=visual,
            auditory=["transfer", "test"],
            mood=0.6, arousal=0.5, attention=0.9,
            goals=["transfer", "apply"], surprise=0.3, satisfaction=0.0
        )
        
        activation = result['activation_field'].get(expected, 0)
        success = abs(activation) > 0.5
        transfer_results.append((description, success, activation))
        
        if success:
            print(f"   ✅ TRANSFER SUCCESS: {activation:.3f}")
        else:
            print(f"   ❌ TRANSFER FAILED: {activation:.3f}")
            # Show what activated instead
            strong_activations = [(k, v) for k, v in result['activation_field'].items() 
                                if abs(v) > 0.5 and k != expected]
            if strong_activations:
                print(f"   Instead activated: {strong_activations[:3]}")
    
    return transfer_results


def test_new_concept_learning(engine):
    """Test if the system can learn new concepts building on foundation."""
    print("\n\n🆕 NEW CONCEPT LEARNING TEST")
    print("=" * 50)
    
    # Introduce subtraction as "take away" - new concept
    print("\n📚 Teaching 'take away' concept...")
    take_away_lessons = [
        # Start with concrete
        (["•", "•", "•", "•", "•"], ["take", "away", "•", "•"], ["•", "•", "•"], ["five", "take", "away", "two", "leaves", "three"], "5 take away 2 = 3"),
        (["★", "★", "★", "★"], ["take", "away", "★"], ["★", "★", "★"], ["four", "take", "away", "one", "leaves", "three"], "4 take away 1 = 3"),
        (["○", "○", "○", "○", "○", "○"], ["take", "away", "○", "○", "○"], ["○", "○", "○"], ["six", "take", "away", "three", "leaves", "three"], "6 take away 3 = 3"),
        
        # Connect to minus symbol
        (["5", "-", "2"], ["take", "away", "two"], ["3"], ["five", "minus", "two", "means", "take", "away"], "5-2 means take away"),
        (["4", "-", "1"], ["take", "away", "one"], ["3"], ["four", "minus", "one", "means", "take", "away"], "4-1 means take away"),
        (["6", "-", "3"], ["take", "away", "three"], ["3"], ["six", "minus", "three", "means", "take", "away"], "6-3 means take away"),
    ]
    
    for i, (visual, action, result, auditory, description) in enumerate(take_away_lessons, 1):
        print(f"   Lesson {i}: {description}")
        engine.live_experience(
            visual=visual + action + ["="] + result,
            auditory=auditory + ["new", "concept"],
            mood=0.6, arousal=0.6, attention=0.9,
            goals=["new", "concept", "learn"], surprise=0.5, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Test new concept understanding
    print("\n🧪 Testing new concept understanding...")
    new_concept_tests = [
        (["7", "-", "2", "=", "?"], "New concept: 7-2", "five"),
        (["8", "-", "3", "=", "?"], "New concept: 8-3", "five"),
        (["9", "-", "4", "=", "?"], "New concept: 9-4", "five"),
    ]
    
    concept_results = []
    for i, (visual, description, expected) in enumerate(new_concept_tests, 1):
        print(f"\n🧪 Concept Test {i}: {description}")
        
        result = engine.live_experience(
            visual=visual,
            auditory=["new", "concept", "test"],
            mood=0.5, arousal=0.7, attention=0.9,
            goals=["new", "concept", "apply"], surprise=0.4, satisfaction=0.0
        )
        
        activation = result['activation_field'].get(expected, 0)
        success = abs(activation) > 0.5
        concept_results.append((description, success, activation))
        
        if success:
            print(f"   ✅ CONCEPT LEARNED: {activation:.3f}")
        else:
            print(f"   ❌ CONCEPT UNCLEAR: {activation:.3f}")
    
    return concept_results


def test_strategy_emergence(engine):
    """Test if strategies emerge from solid foundation."""
    print("\n\n🧠 STRATEGY EMERGENCE TEST")
    print("=" * 50)
    
    # Give strategy hints and see if they stick
    print("\n📚 Strategy instruction...")
    strategy_lessons = [
        # Counting on strategy
        (["6", "+", "2"], ["start", "at", "six", "count", "seven", "eight"], ["eight"], "6+2: count on from 6"),
        (["7", "+", "1"], ["start", "at", "seven", "count", "eight"], ["eight"], "7+1: count on from 7"),
        (["5", "+", "3"], ["start", "at", "five", "count", "six", "seven", "eight"], ["eight"], "5+3: count on from 5"),
        
        # Doubles strategy
        (["6", "+", "6"], ["double", "six", "equals", "twelve"], ["twelve"], "6+6: double 6"),
        (["7", "+", "7"], ["double", "seven", "equals", "fourteen"], ["fourteen"], "7+7: double 7"),
        (["8", "+", "8"], ["double", "eight", "equals", "sixteen"], ["sixteen"], "8+8: double 8"),
    ]
    
    for i, (problem, strategy, answer, description) in enumerate(strategy_lessons, 1):
        print(f"   Strategy {i}: {description}")
        engine.live_experience(
            visual=problem + strategy + ["="] + answer,
            auditory=["strategy", "method", "think"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["strategy", "method"], surprise=0.5, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Test strategy application
    print("\n🧪 Testing strategy application...")
    strategy_tests = [
        (["8", "+", "2", "=", "?"], "Count on strategy", "ten"),
        (["9", "+", "1", "=", "?"], "Count on strategy", "ten"),
        (["5", "+", "5", "=", "?"], "Double strategy", "ten"),
        (["4", "+", "6", "=", "?"], "Flexible strategy", "ten"),
    ]
    
    strategy_results = []
    for i, (visual, description, expected) in enumerate(strategy_tests, 1):
        print(f"\n🧪 Strategy Test {i}: {description}")
        
        result = engine.live_experience(
            visual=visual,
            auditory=["strategy", "test"],
            mood=0.4, arousal=0.8, attention=0.9,
            goals=["strategy", "apply"], surprise=0.4, satisfaction=0.0
        )
        
        activation = result['activation_field'].get(expected, 0)
        success = abs(activation) > 0.5
        strategy_results.append((description, success, activation))
        
        if success:
            print(f"   ✅ STRATEGY APPLIED: {activation:.3f}")
        else:
            print(f"   ❌ STRATEGY UNCLEAR: {activation:.3f}")
    
    return strategy_results


def run_transfer_test():
    """Run the complete transfer learning test."""
    print("🔬 TRANSFER LEARNING EXPERIMENT")
    print("=" * 70)
    print("Testing if foundation breakthrough enables genuine learning transfer")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create fresh engine
    engine = TemporalCognitionEngine()
    
    # Establish the proven foundation
    establish_foundation(engine)
    
    # Test immediate transfer
    transfer_results = test_immediate_transfer(engine)
    
    # Test new concept learning
    concept_results = test_new_concept_learning(engine)
    
    # Test strategy emergence
    strategy_results = test_strategy_emergence(engine)
    
    end_time = time.time()
    
    # Comprehensive analysis
    print("\n\n📊 TRANSFER LEARNING RESULTS")
    print("=" * 70)
    
    # Calculate success rates
    transfer_success = sum(1 for _, success, _ in transfer_results if success)
    concept_success = sum(1 for _, success, _ in concept_results if success)
    strategy_success = sum(1 for _, success, _ in strategy_results if success)
    
    transfer_rate = transfer_success / len(transfer_results) * 100
    concept_rate = concept_success / len(concept_results) * 100
    strategy_rate = strategy_success / len(strategy_results) * 100
    
    print(f"\n🔄 TRANSFER RESULTS:")
    print(f"   Immediate transfer: {transfer_success}/{len(transfer_results)} ({transfer_rate:.1f}%)")
    print(f"   New concept learning: {concept_success}/{len(concept_results)} ({concept_rate:.1f}%)")
    print(f"   Strategy emergence: {strategy_success}/{len(strategy_results)} ({strategy_rate:.1f}%)")
    
    overall_success = transfer_success + concept_success + strategy_success
    overall_total = len(transfer_results) + len(concept_results) + len(strategy_results)
    overall_rate = overall_success / overall_total * 100
    
    print(f"\n🎯 OVERALL TRANSFER LEARNING:")
    print(f"   Total success: {overall_success}/{overall_total} ({overall_rate:.1f}%)")
    print(f"   Learning time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n🧠 FINAL TRANSFER STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active concepts: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    # Transfer analysis
    print(f"\n🔬 TRANSFER ANALYSIS:")
    
    if overall_rate >= 75:
        print(f"   🎉 EXCELLENT TRANSFER LEARNING!")
        print(f"   Foundation breakthrough enabled genuine learning transfer!")
        print(f"   System shows authentic cognitive development!")
        
    elif overall_rate >= 60:
        print(f"   🌟 GOOD TRANSFER LEARNING!")
        print(f"   Foundation provides solid base for new learning!")
        print(f"   System demonstrates meaningful cognitive progress!")
        
    elif overall_rate >= 40:
        print(f"   📈 MODERATE TRANSFER LEARNING!")
        print(f"   Foundation helps but transfer is limited!")
        print(f"   System shows some cognitive development!")
        
    elif overall_rate >= 20:
        print(f"   🤔 LIMITED TRANSFER LEARNING!")
        print(f"   Foundation established but transfer is weak!")
        print(f"   System needs more consolidation time!")
        
    else:
        print(f"   ⚠️ MINIMAL TRANSFER LEARNING!")
        print(f"   Foundation may not be sufficiently solid!")
        print(f"   System needs deeper foundational work!")
    
    # Specific insights
    print(f"\n💡 KEY INSIGHTS:")
    if transfer_rate > concept_rate and transfer_rate > strategy_rate:
        print(f"   • Strongest at applying known patterns to similar problems")
        print(f"   • Needs more support for genuinely new concepts")
    elif concept_rate > transfer_rate and concept_rate > strategy_rate:
        print(f"   • Surprisingly good at learning new concepts!")
        print(f"   • Foundation enables conceptual understanding")
    elif strategy_rate > transfer_rate and strategy_rate > concept_rate:
        print(f"   • Excellent at developing strategic thinking!")
        print(f"   • Foundation enables higher-order reasoning")
    else:
        print(f"   • Balanced development across all areas")
        print(f"   • Foundation provides broad cognitive support")
    
    print(f"\n🎓 The foundation breakthrough test reveals:")
    print(f"   Whether solid foundations truly enable learning transfer,")
    print(f"   or if each concept must be learned independently.")
    print(f"   This is the essence of authentic intelligence! 🌟")


if __name__ == "__main__":
    run_transfer_test() 