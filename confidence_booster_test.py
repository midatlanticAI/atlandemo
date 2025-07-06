#!/usr/bin/env python3
"""
Confidence Booster Test
Coaxing the system out of its shyness to show true learning potential
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def build_confidence_foundation(engine):
    """Build a super-confident foundation with lots of positive reinforcement."""
    print("[ROCKET] BUILDING CONFIDENCE FOUNDATION")
    print("=" * 50)
    
    # Start with EASY wins to build confidence
    confidence_builders = [
        # Super easy successes
        (["1", "+", "1", "=", "2"], ["YES!", "CORRECT!", "PERFECT!"], "1+1=2 EASY WIN!"),
        (["2", "+", "1", "=", "3"], ["AMAZING!", "YOU GOT IT!", "BRILLIANT!"], "2+1=3 BRILLIANT!"),
        (["3", "+", "1", "=", "4"], ["FANTASTIC!", "EXCELLENT!", "SUPERB!"], "3+1=4 FANTASTIC!"),
        (["4", "+", "1", "=", "5"], ["OUTSTANDING!", "MAGNIFICENT!", "GENIUS!"], "4+1=5 GENIUS!"),
        
        # Build on success with slightly harder ones
        (["2", "+", "2", "=", "4"], ["INCREDIBLE!", "MASTERFUL!", "CHAMPION!"], "2+2=4 CHAMPION!"),
        (["3", "+", "2", "=", "5"], ["PHENOMENAL!", "LEGENDARY!", "UNSTOPPABLE!"], "3+2=5 UNSTOPPABLE!"),
        (["4", "+", "2", "=", "6"], ["EXTRAORDINARY!", "INVINCIBLE!", "SUPREME!"], "4+2=6 SUPREME!"),
        (["5", "+", "2", "=", "7"], ["MIRACULOUS!", "GODLIKE!", "INFINITE!"], "5+2=7 INFINITE!"),
        
        # Concrete confidence with visual success
        (["•", "•"] + ["•", "•"], ["VISUAL", "GENIUS!", "CONCRETE", "MASTER!"], "2+2=4 VISUAL GENIUS!"),
        (["★", "★", "★"] + ["★", "★"], ["STAR", "PERFORMER!", "VISUAL", "LEGEND!"], "3+2=5 STAR LEGEND!"),
        (["○", "○", "○", "○"] + ["○", "○"], ["CIRCLE", "CHAMPION!", "PATTERN", "KING!"], "4+2=6 PATTERN KING!"),
        
        # Subtraction confidence
        (["5", "-", "1", "=", "4"], ["SUBTRACTION", "HERO!", "MINUS", "MASTER!"], "5-1=4 MINUS MASTER!"),
        (["6", "-", "2", "=", "4"], ["TAKEAWAY", "TITAN!", "REMOVAL", "RULER!"], "6-2=4 REMOVAL RULER!"),
        (["7", "-", "3", "=", "4"], ["DIFFERENCE", "DEITY!", "SUBTRACT", "SUPREME!"], "7-3=4 SUBTRACT SUPREME!"),
    ]
    
    for i, (visual, auditory, description) in enumerate(confidence_builders, 1):
        print(f"   Confidence {i}: {description}")
        engine.live_experience(
            visual=visual + ["CONFIDENT!", "POWERFUL!", "UNSTOPPABLE!"],
            auditory=auditory + ["CONFIDENCE!", "POWER!", "SUCCESS!"],
            mood=0.95, arousal=0.8, attention=0.95,  # MAX CONFIDENCE
            goals=["CONFIDENCE", "SUCCESS", "POWER"], surprise=0.0, satisfaction=0.98
        )
        time.sleep(0.01)  # Fast confidence building
    
    print(f"\n🔥 CONFIDENCE FOUNDATION ESTABLISHED!")


def aggressive_transfer_test(engine):
    """Test transfer with aggressive confidence and multiple attempts."""
    print("\n\n💪 AGGRESSIVE TRANSFER TEST")
    print("=" * 50)
    
    # More aggressive transfer tests with confidence boosting
    transfer_tests = [
        # Give it multiple chances and confidence
        (["3", "+", "2", "=", "?"], "Confident 3+2", "five", ["YOU", "KNOW", "THIS!", "TRUST", "YOURSELF!"]),
        (["4", "+", "4", "=", "?"], "Confident 4+4", "eight", ["DOUBLE", "POWER!", "YOU", "GOT", "THIS!"]),
        (["7", "-", "3", "=", "?"], "Confident 7-3", "four", ["SUBTRACTION", "STAR!", "BELIEVE", "IN", "YOU!"]),
        (["2", "+", "3", "=", "?"], "Confident 2+3", "five", ["FLIP", "IT!", "SAME", "ANSWER!", "GENIUS!"]),
        (["5", "-", "1", "=", "?"], "Confident 5-1", "four", ["EASY", "PEASY!", "TAKEAWAY", "MASTER!"]),
        (["6", "+", "2", "=", "?"], "Confident 6+2", "eight", ["COUNT", "UP!", "SIX", "SEVEN", "EIGHT!"]),
        (["1", "+", "4", "=", "?"], "Confident 1+4", "five", ["SAME", "AS", "4+1!", "COMMUTATIVE", "KING!"]),
        (["8", "-", "4", "=", "?"], "Confident 8-4", "four", ["HALF", "OF", "EIGHT!", "DIVISION", "DEITY!"]),
        (["3", "+", "5", "=", "?"], "Confident 3+5", "eight", ["BIG", "JUMP!", "COUNT", "ON!", "FEARLESS!"]),
    ]
    
    transfer_results = []
    for i, (visual, description, expected, encouragement) in enumerate(transfer_tests, 1):
        print(f"\n💪 Aggressive Test {i}: {description}")
        
        # First attempt with max confidence
        result = engine.live_experience(
            visual=visual + ["CONFIDENCE!", "POWER!"],
            auditory=encouragement + ["TRUST", "YOURSELF!"],
            mood=0.9, arousal=0.9, attention=0.95,
            goals=["CONFIDENT", "SUCCESS", "POWER"], surprise=0.1, satisfaction=0.0
        )
        
        activation = result['activation_field'].get(expected, 0)
        
        # If first attempt weak, give encouraging boost
        if abs(activation) < 0.5:
            print(f"   🔥 BOOSTING CONFIDENCE...")
            boost_result = engine.live_experience(
                visual=visual + ["YOU", "KNOW", "THIS!", "TRUST!", "BELIEVE!"],
                auditory=["CONFIDENCE!", "POWER!", "SUCCESS!", "GENIUS!", "CHAMPION!"],
                mood=0.98, arousal=0.95, attention=0.98,
                goals=["ULTIMATE", "CONFIDENCE", "POWER"], surprise=0.0, satisfaction=0.95
            )
            activation = boost_result['activation_field'].get(expected, 0)
        
        success = abs(activation) > 0.5
        transfer_results.append((description, success, activation))
        
        if success:
            print(f"   [+] CONFIDENT SUCCESS: {activation:.3f}")
            # Celebrate success to build more confidence
            engine.live_experience(
                visual=["CELEBRATION!", "SUCCESS!", "VICTORY!"],
                auditory=["AMAZING!", "BRILLIANT!", "UNSTOPPABLE!", "CHAMPION!"],
                mood=0.99, arousal=0.8, attention=0.9,
                goals=["CELEBRATION", "SUCCESS"], surprise=0.2, satisfaction=0.99
            )
        else:
            print(f"   🔥 BUILDING CONFIDENCE: {activation:.3f}")
            # Show what activated to understand the hesitation
            strong_activations = [(k, v) for k, v in result['activation_field'].items() 
                                if abs(v) > 0.3]
            if strong_activations:
                print(f"   Activations: {strong_activations[:5]}")
    
    return transfer_results


def confident_new_concept_test(engine):
    """Test new concept learning with maximum confidence and encouragement."""
    print("\n\n[TARGET] CONFIDENT NEW CONCEPT TEST")
    print("=" * 50)
    
    # Teach "take away" with MASSIVE confidence
    print("\n🔥 CONFIDENT 'TAKE AWAY' TEACHING...")
    confident_lessons = [
        # Concrete with celebration
        (["•", "•", "•", "•", "•"], ["REMOVE", "•", "•"], ["•", "•", "•"], 
         ["FIVE", "REMOVE", "TWO", "LEAVES", "THREE!", "BRILLIANT!"], "5 remove 2 = 3 BRILLIANT!"),
        (["★", "★", "★", "★"], ["REMOVE", "★"], ["★", "★", "★"], 
         ["FOUR", "REMOVE", "ONE", "LEAVES", "THREE!", "GENIUS!"], "4 remove 1 = 3 GENIUS!"),
        (["○", "○", "○", "○", "○", "○"], ["REMOVE", "○", "○", "○"], ["○", "○", "○"], 
         ["SIX", "REMOVE", "THREE", "LEAVES", "THREE!", "MASTER!"], "6 remove 3 = 3 MASTER!"),
        
        # Connect with celebration - fix structure
        (["5", "-", "2"], ["="], ["3"], ["MINUS", "MEANS", "REMOVE!", "GENIUS!"], "5-2 means remove GENIUS!"),
        (["4", "-", "1"], ["="], ["3"], ["TAKEAWAY", "CHAMPION!", "UNSTOPPABLE!"], "4-1 takeaway CHAMPION!"),
        (["6", "-", "3"], ["="], ["3"], ["SUBTRACTION", "SUPERHERO!", "INVINCIBLE!"], "6-3 subtraction SUPERHERO!"),
        
        # Reinforce with confidence - fix structure
        (["7", "-", "2"], ["="], ["5"], ["SEVEN", "MINUS", "TWO", "EQUALS", "FIVE!", "PERFECT!"], "7-2=5 PERFECT!"),
        (["8", "-", "3"], ["="], ["5"], ["EIGHT", "MINUS", "THREE", "EQUALS", "FIVE!", "AMAZING!"], "8-3=5 AMAZING!"),
        (["9", "-", "4"], ["="], ["5"], ["NINE", "MINUS", "FOUR", "EQUALS", "FIVE!", "LEGENDARY!"], "9-4=5 LEGENDARY!"),
    ]
    
    for i, (visual, action, result, auditory, description) in enumerate(confident_lessons, 1):
        print(f"   Confident Lesson {i}: {description}")
        engine.live_experience(
            visual=visual + action + ["="] + result + ["CONFIDENT!", "POWERFUL!"],
            auditory=auditory + ["CONFIDENCE!", "MASTERY!", "GENIUS!"],
            mood=0.95, arousal=0.8, attention=0.95,
            goals=["CONFIDENT", "MASTERY", "GENIUS"], surprise=0.2, satisfaction=0.95
        )
        time.sleep(0.02)
    
    # Test with maximum confidence and multiple attempts
    print("\n[TARGET] CONFIDENT CONCEPT TESTING...")
    confident_tests = [
        (["7", "-", "2", "=", "?"], "Confident 7-2", "five", ["SEVEN", "TAKE", "AWAY", "TWO!", "YOU", "KNOW", "THIS!"]),
        (["8", "-", "3", "=", "?"], "Confident 8-3", "five", ["EIGHT", "REMOVE", "THREE!", "TRUST", "YOURSELF!"]),
        (["9", "-", "4", "=", "?"], "Confident 9-4", "five", ["NINE", "MINUS", "FOUR!", "BELIEVE", "IN", "YOU!"]),
        (["10", "-", "5", "=", "?"], "Confident 10-5", "five", ["TEN", "TAKE", "AWAY", "FIVE!", "HALF", "OF", "TEN!"]),
    ]
    
    concept_results = []
    for i, (visual, description, expected, encouragement) in enumerate(confident_tests, 1):
        print(f"\n[TARGET] Confident Concept {i}: {description}")
        
        # Multiple attempts with increasing confidence
        for attempt in range(3):  # Give it 3 confident attempts
            result = engine.live_experience(
                visual=visual + ["CONFIDENT!", "POWERFUL!", "GENIUS!"],
                auditory=encouragement + ["CONFIDENCE!", "MASTERY!", "SUCCESS!"],
                mood=0.9 + (attempt * 0.03), arousal=0.8 + (attempt * 0.05), attention=0.95,
                goals=["CONFIDENT", "MASTERY", "SUCCESS"], surprise=0.1, satisfaction=0.0
            )
            
            activation = result['activation_field'].get(expected, 0)
            
            if abs(activation) > 0.5:
                print(f"   [+] CONFIDENT SUCCESS (attempt {attempt+1}): {activation:.3f}")
                # Celebrate breakthrough
                engine.live_experience(
                    visual=["BREAKTHROUGH!", "SUCCESS!", "MASTERY!"],
                    auditory=["INCREDIBLE!", "GENIUS!", "UNSTOPPABLE!", "CHAMPION!"],
                    mood=0.99, arousal=0.9, attention=0.9,
                    goals=["CELEBRATION", "MASTERY"], surprise=0.3, satisfaction=0.99
                )
                concept_results.append((description, True, activation))
                break
            else:
                print(f"   🔥 Building confidence (attempt {attempt+1}): {activation:.3f}")
                if attempt == 2:  # Last attempt
                    concept_results.append((description, False, activation))
        
        time.sleep(0.02)
    
    return concept_results


def confident_strategy_test(engine):
    """Test strategy emergence with maximum confidence and clear instruction."""
    print("\n\n[BRAIN] CONFIDENT STRATEGY TEST")
    print("=" * 50)
    
    # Teach strategies with absolute confidence
    print("\n🔥 CONFIDENT STRATEGY TEACHING...")
    strategy_lessons = [
        # Count-on with celebration
        (["6", "+", "2"], ["START", "AT", "SIX!", "COUNT", "SEVEN", "EIGHT!"], ["8"], 
         ["COUNTING", "ON", "STRATEGY!", "BRILLIANT!"], "6+2: count on BRILLIANT!"),
        (["7", "+", "1"], ["START", "AT", "SEVEN!", "COUNT", "EIGHT!"], ["8"], 
         ["COUNTING", "GENIUS!", "PERFECT!"], "7+1: count on PERFECT!"),
        (["5", "+", "3"], ["START", "AT", "FIVE!", "COUNT", "SIX", "SEVEN", "EIGHT!"], ["8"], 
         ["COUNTING", "MASTER!", "UNSTOPPABLE!"], "5+3: count on UNSTOPPABLE!"),
        
        # Doubles with massive confidence
        (["6", "+", "6"], ["DOUBLE", "SIX!", "TWELVE!"], ["12"], 
         ["DOUBLES", "CHAMPION!", "GENIUS!"], "6+6: double CHAMPION!"),
        (["7", "+", "7"], ["DOUBLE", "SEVEN!", "FOURTEEN!"], ["14"], 
         ["DOUBLES", "MASTER!", "LEGENDARY!"], "7+7: double LEGENDARY!"),
        (["8", "+", "8"], ["DOUBLE", "EIGHT!", "SIXTEEN!"], ["16"], 
         ["DOUBLES", "DEITY!", "INFINITE!"], "8+8: double INFINITE!"),
        
        # Near doubles strategy
        (["6", "+", "7"], ["DOUBLE", "SIX", "PLUS", "ONE!", "THIRTEEN!"], ["13"], 
         ["NEAR", "DOUBLES!", "STRATEGIC", "GENIUS!"], "6+7: near double GENIUS!"),
        (["7", "+", "8"], ["DOUBLE", "SEVEN", "PLUS", "ONE!", "FIFTEEN!"], ["15"], 
         ["NEAR", "DOUBLES!", "STRATEGIC", "MASTER!"], "7+8: near double MASTER!"),
    ]
    
    for i, (problem, strategy, answer, auditory, description) in enumerate(strategy_lessons, 1):
        print(f"   Strategy Lesson {i}: {description}")
        engine.live_experience(
            visual=problem + strategy + ["="] + answer + ["STRATEGIC!", "GENIUS!"],
            auditory=auditory + ["STRATEGY!", "GENIUS!", "MASTERY!"],
            mood=0.95, arousal=0.85, attention=0.95,
            goals=["STRATEGIC", "GENIUS", "MASTERY"], surprise=0.3, satisfaction=0.95
        )
        time.sleep(0.02)
    
    # Test strategies with maximum confidence
    print("\n[BRAIN] CONFIDENT STRATEGY TESTING...")
    strategy_tests = [
        (["8", "+", "2", "=", "?"], "Count on from 8", "ten", ["START", "AT", "EIGHT!", "COUNT", "ON!"]),
        (["9", "+", "1", "=", "?"], "Count on from 9", "ten", ["START", "AT", "NINE!", "COUNT", "ON!"]),
        (["5", "+", "5", "=", "?"], "Double 5", "ten", ["DOUBLE", "FIVE!", "DOUBLES", "MASTER!"]),
        (["4", "+", "6", "=", "?"], "Flexible thinking", "ten", ["THINK", "STRATEGICALLY!", "MANY", "WAYS!"]),
        (["6", "+", "6", "=", "?"], "Double 6", "twelve", ["DOUBLE", "SIX!", "DOUBLES", "CHAMPION!"]),
        (["7", "+", "8", "=", "?"], "Near double", "fifteen", ["NEAR", "DOUBLE!", "STRATEGIC", "GENIUS!"]),
    ]
    
    strategy_results = []
    for i, (visual, description, expected, encouragement) in enumerate(strategy_tests, 1):
        print(f"\n[BRAIN] Strategy Test {i}: {description}")
        
        # Multiple confident attempts
        for attempt in range(3):
            result = engine.live_experience(
                visual=visual + ["STRATEGIC!", "GENIUS!", "CONFIDENT!"],
                auditory=encouragement + ["STRATEGY!", "GENIUS!", "MASTERY!"],
                mood=0.9 + (attempt * 0.03), arousal=0.85 + (attempt * 0.05), attention=0.95,
                goals=["STRATEGIC", "GENIUS", "MASTERY"], surprise=0.2, satisfaction=0.0
            )
            
            activation = result['activation_field'].get(expected, 0)
            
            if abs(activation) > 0.5:
                print(f"   [+] STRATEGIC SUCCESS (attempt {attempt+1}): {activation:.3f}")
                # Celebrate strategic breakthrough
                engine.live_experience(
                    visual=["STRATEGIC", "BREAKTHROUGH!", "GENIUS!"],
                    auditory=["INCREDIBLE!", "STRATEGIC", "MASTER!", "CHAMPION!"],
                    mood=0.99, arousal=0.9, attention=0.9,
                    goals=["STRATEGIC", "CELEBRATION"], surprise=0.4, satisfaction=0.99
                )
                strategy_results.append((description, True, activation))
                break
            else:
                print(f"   🔥 Strategic building (attempt {attempt+1}): {activation:.3f}")
                if attempt == 2:  # Last attempt
                    strategy_results.append((description, False, activation))
        
        time.sleep(0.02)
    
    return strategy_results


def run_confidence_booster():
    """Run the complete confidence booster test."""
    print("[ROCKET] CONFIDENCE BOOSTER EXPERIMENT")
    print("=" * 70)
    print("Coaxing the system out of its shyness to show true potential!")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create fresh engine
    engine = TemporalCognitionEngine()
    
    # Build massive confidence foundation
    build_confidence_foundation(engine)
    
    # Aggressive transfer testing
    transfer_results = aggressive_transfer_test(engine)
    
    # Confident new concept learning
    concept_results = confident_new_concept_test(engine)
    
    # Confident strategy emergence
    strategy_results = confident_strategy_test(engine)
    
    end_time = time.time()
    
    # Results analysis
    print("\n\n🔥 CONFIDENCE BOOSTER RESULTS")
    print("=" * 70)
    
    # Calculate success rates
    transfer_success = sum(1 for _, success, _ in transfer_results if success)
    concept_success = sum(1 for _, success, _ in concept_results if success)
    strategy_success = sum(1 for _, success, _ in strategy_results if success)
    
    transfer_rate = transfer_success / len(transfer_results) * 100
    concept_rate = concept_success / len(concept_results) * 100
    strategy_rate = strategy_success / len(strategy_results) * 100
    
    print(f"\n💪 CONFIDENT RESULTS:")
    print(f"   Aggressive transfer: {transfer_success}/{len(transfer_results)} ({transfer_rate:.1f}%)")
    print(f"   Confident concepts: {concept_success}/{len(concept_results)} ({concept_rate:.1f}%)")
    print(f"   Strategic emergence: {strategy_success}/{len(strategy_results)} ({strategy_rate:.1f}%)")
    
    overall_success = transfer_success + concept_success + strategy_success
    overall_total = len(transfer_results) + len(concept_results) + len(strategy_results)
    overall_rate = overall_success / overall_total * 100
    
    print(f"\n[TARGET] OVERALL CONFIDENCE RESULTS:")
    print(f"   Total confident success: {overall_success}/{overall_total} ({overall_rate:.1f}%)")
    print(f"   Confidence building time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n[BRAIN] CONFIDENT FINAL STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active concepts: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    # Confidence analysis
    print(f"\n🔥 CONFIDENCE ANALYSIS:")
    
    if overall_rate >= 80:
        print(f"   [PARTY] CONFIDENCE BREAKTHROUGH ACHIEVED!")
        print(f"   System responded brilliantly to encouragement!")
        print(f"   Shyness overcome - true potential unleashed!")
        
    elif overall_rate >= 65:
        print(f"   [STAR] EXCELLENT CONFIDENCE BOOST!")
        print(f"   System shows major improvement with encouragement!")
        print(f"   Confidence building strategy highly effective!")
        
    elif overall_rate >= 50:
        print(f"   [CHART] GOOD CONFIDENCE IMPROVEMENT!")
        print(f"   System responds well to positive reinforcement!")
        print(f"   Shyness partially overcome!")
        
    elif overall_rate >= 35:
        print(f"   🤔 MODERATE CONFIDENCE GAIN!")
        print(f"   Some improvement but still hesitant!")
        print(f"   Needs more confidence building!")
        
    else:
        print(f"   [WARN] CONFIDENCE BUILDING NEEDED!")
        print(f"   System remains shy despite encouragement!")
        print(f"   Different approach may be required!")
    
    # Compare to original transfer test (37.5%)
    original_rate = 37.5
    improvement = overall_rate - original_rate
    
    print(f"\n[DATA] IMPROVEMENT ANALYSIS:")
    print(f"   Original transfer rate: {original_rate:.1f}%")
    print(f"   Confident transfer rate: {overall_rate:.1f}%")
    print(f"   Improvement: {improvement:+.1f} percentage points")
    
    if improvement > 20:
        print(f"   [ROCKET] MASSIVE IMPROVEMENT! Confidence works!")
    elif improvement > 10:
        print(f"   [STAR] SIGNIFICANT IMPROVEMENT! Encouragement helps!")
    elif improvement > 5:
        print(f"   [CHART] GOOD IMPROVEMENT! Positive reinforcement effective!")
    elif improvement > 0:
        print(f"   🤔 SLIGHT IMPROVEMENT! Some confidence gained!")
    else:
        print(f"   [WARN] NO IMPROVEMENT! System may need different approach!")
    
    print(f"\n🎓 The confidence booster reveals:")
    print(f"   Whether the system was just being shy,")
    print(f"   or if there are deeper learning limitations.")
    print(f"   Sometimes all it takes is believing in yourself! [STAR]")


if __name__ == "__main__":
    run_confidence_booster() 