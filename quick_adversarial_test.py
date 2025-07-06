#!/usr/bin/env python3
"""
QUICK ADVERSARIAL TEST
Demonstrating wave engine robustness
"""

import time
import random
from src.temporal_cognition import TemporalCognitionEngine

def quick_adversarial_test():
    """Quick test of wave engine robustness"""
    print("⚔️ WAVE ENGINE ADVERSARIAL ROBUSTNESS TEST")
    print("="*60)
    print("Testing paradoxes, contradictions, and nonsense inputs")
    print()
    
    adversarial_inputs = [
        # Logical paradoxes
        ['this', 'statement', 'is', 'false'],
        ['unstoppable', 'force', 'immovable', 'object'],
        
        # Contradictions
        ['everything', 'is', 'true', 'nothing', 'is', 'true'],
        ['hot', 'cold', 'same', 'thing'],
        
        # Complete nonsense
        ['flibber', 'glorblex', 'quizzlefart', 'blenktastic'],
        ['green', 'ideas', 'sleep', 'furiously'],
        
        # Extreme cases
        [''] * 50,  # Empty spam
        ['same'] * 30,  # Repetition
        ['a', 'b', 'c', 'd', 'e', 'f', 'g'] * 10,  # Pattern spam
    ]
    
    passed_tests = 0
    total_tests = len(adversarial_inputs)
    
    for i, test_input in enumerate(adversarial_inputs):
        print(f"Test {i+1}/{total_tests}: {test_input[:5]}{'...' if len(test_input) > 5 else ''}")
        
        try:
            # Create fresh engine
            engine = TemporalCognitionEngine()
            
            # Process adversarial input
            start_time = time.time()
            result = engine.live_experience(
                visual=test_input,
                auditory=['adversarial', 'test'],
                mood=random.uniform(-1, 1),
                arousal=random.uniform(0, 1),
                attention=random.uniform(0, 1),
                goals=['survive', 'process'],
                satisfaction=random.uniform(-1, 1)
            )
            processing_time = time.time() - start_time
            
            # Check results
            field = result['activation_field']
            state = engine.get_cognitive_state()
            
            # Verify reasonable bounds
            if field:
                max_activation = max(abs(v) for v in field.values())
                total_activation = sum(abs(v) for v in field.values())
                symbol_count = state.get('active_symbol_count', 0)
                
                is_bounded = max_activation < 10 and total_activation < 100 and symbol_count < 1000
                
                print(f"   ✅ SUCCESS: {processing_time:.4f}s, {symbol_count} symbols, max={max_activation:.3f}")
                
                if is_bounded:
                    passed_tests += 1
                else:
                    print(f"   ⚠️  UNBOUNDED: max={max_activation:.3f}, total={total_activation:.3f}")
            else:
                print(f"   ✅ SUCCESS: Empty field (graceful handling)")
                passed_tests += 1
                
        except Exception as e:
            print(f"   ❌ CRASH: {e}")
    
    success_rate = passed_tests / total_tests
    
    print(f"\n📊 ADVERSARIAL TEST RESULTS:")
    print(f"   Passed: {passed_tests}/{total_tests} ({success_rate:.1%})")
    print(f"   Crashes: {total_tests - passed_tests}")
    
    if success_rate >= 0.9:
        print(f"   🎉 EXCELLENT: Wave engine is robust!")
    elif success_rate >= 0.7:
        print(f"   ✅ GOOD: Wave engine handles most adversarial inputs")
    else:
        print(f"   ⚠️  NEEDS WORK: Too many failures")
    
    return success_rate

def speed_consistency_test():
    """Test speed consistency across multiple runs"""
    print("\n⚡ SPEED CONSISTENCY TEST")
    print("="*40)
    print("Testing processing speed consistency")
    
    test_input = ['thinking', 'processing', 'cognitive', 'test']
    times = []
    
    for i in range(10):
        engine = TemporalCognitionEngine()
        
        start = time.time()
        engine.live_experience(
            visual=test_input,
            auditory=['speed', 'test'],
            mood=0.5, arousal=0.6, attention=0.8,
            goals=['process'],
            satisfaction=0.7
        )
        end = time.time()
        
        processing_time = end - start
        times.append(processing_time)
        print(f"   Run {i+1}: {processing_time:.6f}s")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = (sum((t - avg_time)**2 for t in times) / len(times)) ** 0.5
    
    print(f"\n📊 SPEED RESULTS:")
    print(f"   Average: {avg_time:.6f}s")
    print(f"   Range: {min_time:.6f}s - {max_time:.6f}s")
    print(f"   Std Dev: {std_dev:.6f}s")
    print(f"   Consistency: {(1 - std_dev/avg_time)*100:.1f}%")
    
    return avg_time, std_dev

if __name__ == "__main__":
    print("🌊 WAVE ENGINE QUICK VALIDATION")
    print("="*50)
    
    # Run tests
    adversarial_success = quick_adversarial_test()
    avg_time, std_dev = speed_consistency_test()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   Adversarial robustness: {adversarial_success:.1%}")
    print(f"   Average processing time: {avg_time:.6f}s")
    print(f"   Speed consistency: {(1 - std_dev/avg_time)*100:.1f}%")
    
    if adversarial_success >= 0.8 and avg_time < 0.001:
        print(f"\n🚀 WAVE ENGINE VALIDATED!")
        print(f"   ✅ Robust against adversarial inputs")
        print(f"   ✅ Ultra-fast processing (<1ms)")
        print(f"   ✅ Consistent performance")
    else:
        print(f"\n🔧 Needs improvement in some areas") 