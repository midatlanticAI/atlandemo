#!/usr/bin/env python3
"""
Adaptive Learning System
Identifies current developmental stage and systematically builds missing foundations.
Overcomes learning obstacles through targeted remediation and gradual complexity increase.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def diagnose_learning_gaps(engine):
    """Diagnose specific learning gaps and readiness levels."""
    print("🔍 DIAGNOSTIC ASSESSMENT")
    print("=" * 50)
    
    diagnostic_tests = [
        # Foundation level
        ("Foundation", [
            (["3", "+", "2"], "Basic addition", "five"),
            (["7", "-", "3"], "Basic subtraction", "four"),
            (["4", "+", "4"], "Doubles", "eight"),
        ]),
        # Automaticity level  
        ("Automaticity", [
            (["6", "+", "4"], "Quick recall", "ten"),
            (["9", "-", "5"], "Quick recall", "four"),
            (["5", "+", "5"], "Quick recall", "ten"),
        ]),
        # Strategy level
        ("Strategy", [
            (["8", "+", "3"], "Count on", "eleven"),
            (["12", "-", "4"], "Count back", "eight"),
            (["6", "+", "5"], "Near double", "eleven"),
        ]),
    ]
    
    results = {}
    for level_name, tests in diagnostic_tests:
        print(f"\n📊 {level_name} Level Assessment")
        correct = 0
        total = len(tests)
        
        for visual, description, expected in tests:
            result = engine.live_experience(
                visual=visual + ["?"],
                auditory=["quick", "test"],
                mood=0.5, arousal=0.6, attention=0.9,
                goals=["test", "quick"], surprise=0.3, satisfaction=0.0
            )
            
            activation = result['activation_field'].get(expected, 0)
            success = abs(activation) > 0.5
            if success:
                correct += 1
                print(f"   ✅ {description}: {activation:.3f}")
            else:
                print(f"   ❌ {description}: {activation:.3f}")
        
        percentage = correct / total * 100
        results[level_name] = (correct, total, percentage)
        print(f"   {level_name}: {correct}/{total} ({percentage:.1f}%)")
    
    return results


def targeted_remediation(engine, gaps):
    """Provide targeted remediation for identified gaps."""
    print("\n\n🎯 TARGETED REMEDIATION")
    print("=" * 50)
    
    # If foundation is weak, focus there
    if gaps["Foundation"][2] < 80:
        print("\n📚 Intensive Foundation Building...")
        foundation_drill = [
            # Concrete experiences with immediate feedback
            (["•", "•", "•"] + ["•", "•"], ["three", "plus", "two", "equals", "five"], "3+2=5 concrete"),
            (["★", "★", "★"] + ["★", "★"], ["three", "plus", "two", "equals", "five"], "3+2=5 stars"),
            (["○", "○", "○"] + ["○", "○"], ["three", "plus", "two", "equals", "five"], "3+2=5 circles"),
            (["•", "•", "•", "•"] + ["•", "•", "•", "•"], ["four", "plus", "four", "equals", "eight"], "4+4=8 concrete"),
            (["★", "★", "★", "★"] + ["★", "★", "★", "★"], ["four", "plus", "four", "equals", "eight"], "4+4=8 stars"),
        ]
        
        for i, (visual, auditory, description) in enumerate(foundation_drill, 1):
            print(f"   Remediation {i}: {description}")
            engine.live_experience(
                visual=visual + ["concrete", "solid"],
                auditory=auditory + ["solid", "foundation"],
                mood=0.8, arousal=0.4, attention=0.9,
                goals=["solid", "foundation"], surprise=0.1, satisfaction=0.9
            )
            time.sleep(0.03)
    
    # If automaticity is weak, drill facts
    if gaps["Automaticity"][2] < 80:
        print("\n📚 Automaticity Development...")
        automaticity_drill = [
            # Rapid-fire fact practice
            (["6", "+", "4", "=", "10"], ["instant", "automatic"], "6+4=10 automatic"),
            (["10", "-", "4", "=", "6"], ["instant", "automatic"], "10-4=6 automatic"),
            (["5", "+", "5", "=", "10"], ["instant", "automatic"], "5+5=10 automatic"),
            (["10", "-", "5", "=", "5"], ["instant", "automatic"], "10-5=5 automatic"),
            (["7", "+", "3", "=", "10"], ["instant", "automatic"], "7+3=10 automatic"),
            (["10", "-", "3", "=", "7"], ["instant", "automatic"], "10-3=7 automatic"),
        ]
        
        for i, (visual, auditory, description) in enumerate(automaticity_drill, 1):
            print(f"   Automaticity {i}: {description}")
            engine.live_experience(
                visual=visual + ["fast", "automatic"],
                auditory=auditory + ["fast", "recall"],
                mood=0.7, arousal=0.6, attention=0.9,
                goals=["fast", "automatic"], surprise=0.1, satisfaction=0.8
            )
            time.sleep(0.02)
    
    # If strategy is weak, build step by step
    if gaps["Strategy"][2] < 80:
        print("\n📚 Strategy Development...")
        strategy_drill = [
            # Explicit strategy instruction
            (["8", "+", "3"], ["start", "at", "8", "count", "9", "10", "11"], "8+3 count on strategy"),
            (["7", "+", "4"], ["start", "at", "7", "count", "8", "9", "10", "11"], "7+4 count on strategy"),
            (["12", "-", "4"], ["start", "at", "12", "back", "11", "10", "9", "8"], "12-4 count back strategy"),
            (["6", "+", "5"], ["think", "5", "+", "5", "+", "1", "=", "11"], "6+5 near double strategy"),
            (["7", "+", "6"], ["think", "6", "+", "6", "+", "1", "=", "13"], "7+6 near double strategy"),
        ]
        
        for i, (problem, strategy, description) in enumerate(strategy_drill, 1):
            print(f"   Strategy {i}: {description}")
            engine.live_experience(
                visual=problem + strategy + ["strategy", "method"],
                auditory=["strategy", "method", "think"],
                mood=0.5, arousal=0.7, attention=0.9,
                goals=["strategy", "method"], surprise=0.4, satisfaction=0.7
            )
            time.sleep(0.03)


def gradual_complexity_increase(engine):
    """Gradually increase complexity based on demonstrated mastery."""
    print("\n\n📈 GRADUAL COMPLEXITY INCREASE")
    print("=" * 50)
    
    # Level 1: Single digit mastery
    print("\n📚 Level 1: Single digit mastery...")
    level1_problems = [
        (["5", "+", "4"], "5+4", "nine"),
        (["8", "+", "2"], "8+2", "ten"),
        (["9", "-", "3"], "9-3", "six"),
        (["7", "+", "3"], "7+3", "ten"),
    ]
    
    level1_success = 0
    for problem, description, expected in level1_problems:
        result = engine.live_experience(
            visual=problem + ["=", "?"],
            auditory=["solve", "level1"],
            mood=0.6, arousal=0.5, attention=0.9,
            goals=["solve", "master"], surprise=0.3, satisfaction=0.0
        )
        
        activation = result['activation_field'].get(expected, 0)
        if abs(activation) > 0.5:
            level1_success += 1
            print(f"   ✅ {description}: {activation:.3f}")
        else:
            print(f"   ❌ {description}: {activation:.3f}")
    
    level1_rate = level1_success / len(level1_problems)
    print(f"\nLevel 1 Mastery: {level1_success}/{len(level1_problems)} ({level1_rate*100:.1f}%)")
    
    # Only proceed if Level 1 is mastered
    if level1_rate >= 0.75:
        print("\n📚 Level 2: Bridge to teens...")
        level2_problems = [
            (["9", "+", "2"], "9+2", "eleven"),
            (["8", "+", "4"], "8+4", "twelve"),
            (["13", "-", "3"], "13-3", "ten"),
            (["6", "+", "5"], "6+5", "eleven"),
        ]
        
        level2_success = 0
        for problem, description, expected in level2_problems:
            result = engine.live_experience(
                visual=problem + ["=", "?"],
                auditory=["solve", "level2"],
                mood=0.5, arousal=0.6, attention=0.9,
                goals=["solve", "advance"], surprise=0.4, satisfaction=0.0
            )
            
            activation = result['activation_field'].get(expected, 0)
            if abs(activation) > 0.5:
                level2_success += 1
                print(f"   ✅ {description}: {activation:.3f}")
            else:
                print(f"   ❌ {description}: {activation:.3f}")
        
        level2_rate = level2_success / len(level2_problems)
        print(f"\nLevel 2 Mastery: {level2_success}/{len(level2_problems)} ({level2_rate*100:.1f}%)")
        
        return level1_rate, level2_rate
    
    return level1_rate, 0


def run_adaptive_system():
    """Run the complete adaptive learning system."""
    print("🧠 ADAPTIVE LEARNING SYSTEM")
    print("=" * 60)
    print("Identifying gaps and building systematic foundations")
    print("=" * 60)
    
    # Create fresh engine
    engine = TemporalCognitionEngine()
    
    # Quick foundation establishment
    foundation_facts = [
        (["2", "+", "1", "=", "3"], "2+1=3"),
        (["3", "+", "2", "=", "5"], "3+2=5"),
        (["4", "+", "1", "=", "5"], "4+1=5"),
        (["5", "-", "2", "=", "3"], "5-2=3"),
    ]
    
    for fact, description in foundation_facts:
        engine.live_experience(
            visual=fact,
            auditory=["foundation"],
            mood=0.8, arousal=0.4, attention=0.8,
            goals=["foundation"], surprise=0.1, satisfaction=0.9
        )
        time.sleep(0.01)
    
    # Diagnose current state
    gaps = diagnose_learning_gaps(engine)
    
    # Provide targeted remediation
    targeted_remediation(engine, gaps)
    
    # Test again after remediation
    print("\n\n🔄 POST-REMEDIATION ASSESSMENT")
    print("=" * 50)
    gaps_after = diagnose_learning_gaps(engine)
    
    # Show improvement
    print("\n📊 LEARNING PROGRESS")
    print("=" * 30)
    for level in ["Foundation", "Automaticity", "Strategy"]:
        before = gaps[level][2]
        after = gaps_after[level][2]
        improvement = after - before
        print(f"{level}: {before:.1f}% → {after:.1f}% (Δ{improvement:+.1f}%)")
    
    # Try gradual complexity increase
    level1_rate, level2_rate = gradual_complexity_increase(engine)
    
    # Final assessment
    final_state = engine.get_cognitive_state()
    print(f"\n🧠 FINAL ADAPTIVE STATE:")
    print(f"   Experiences: {final_state['total_experiences']}")
    print(f"   Active concepts: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    print(f"\n🎯 ADAPTIVE LEARNING RESULTS:")
    overall_improvement = sum(gaps_after[level][2] - gaps[level][2] for level in gaps) / len(gaps)
    print(f"   Average improvement: {overall_improvement:+.1f}%")
    print(f"   Level 1 mastery: {level1_rate*100:.1f}%")
    print(f"   Level 2 readiness: {level2_rate*100:.1f}%")
    
    if overall_improvement > 10:
        print(f"\n🎉 Significant learning progress achieved!")
        print(f"   Adaptive remediation successfully addressed gaps!")
    elif overall_improvement > 0:
        print(f"\n📈 Positive learning progress detected!")
        print(f"   Continue systematic foundation building!")
    else:
        print(f"\n🤔 Learning progress limited.")
        print(f"   May need more time or different approach.")


if __name__ == "__main__":
    run_adaptive_system() 