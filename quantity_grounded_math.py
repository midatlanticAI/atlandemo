#!/usr/bin/env python3
"""
Quantity-Grounded Mathematical Learning
Teaching math the way children actually learn: quantities first, then symbols, then operations.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def teach_quantity_recognition(engine):
    """Phase 1: Teach quantity recognition through concrete experience."""
    print("🔢 PHASE 1: QUANTITY RECOGNITION")
    print("=" * 50)
    
    # Teach "one" through multiple concrete experiences
    one_experiences = [
        (["apple"], "one apple"),
        (["block"], "one block"),
        (["ball"], "one ball"),
        (["toy"], "one toy"),
        (["object"], "one object"),
    ]
    
    print("\n📚 Learning 'one' through concrete experiences...")
    for i, (visual, description) in enumerate(one_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["one"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    # Teach "two" through multiple concrete experiences
    two_experiences = [
        (["apple", "apple"], "two apples"),
        (["block", "block"], "two blocks"),
        (["ball", "ball"], "two balls"),
        (["toy", "toy"], "two toys"),
        (["object", "object"], "two objects"),
    ]
    
    print("\n📚 Learning 'two' through concrete experiences...")
    for i, (visual, description) in enumerate(two_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["two"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    # Teach "three" through multiple concrete experiences
    three_experiences = [
        (["apple", "apple", "apple"], "three apples"),
        (["block", "block", "block"], "three blocks"),
        (["ball", "ball", "ball"], "three balls"),
        (["toy", "toy", "toy"], "three toys"),
        (["object", "object", "object"], "three objects"),
    ]
    
    print("\n📚 Learning 'three' through concrete experiences...")
    for i, (visual, description) in enumerate(three_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["three"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    # Teach "four" and "five" similarly
    four_experiences = [
        (["apple", "apple", "apple", "apple"], "four apples"),
        (["block", "block", "block", "block"], "four blocks"),
        (["object", "object", "object", "object"], "four objects"),
    ]
    
    print("\n📚 Learning 'four' through concrete experiences...")
    for i, (visual, description) in enumerate(four_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["four"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    five_experiences = [
        (["apple", "apple", "apple", "apple", "apple"], "five apples"),
        (["block", "block", "block", "block", "block"], "five blocks"),
        (["object", "object", "object", "object", "object"], "five objects"),
    ]
    
    print("\n📚 Learning 'five' through concrete experiences...")
    for i, (visual, description) in enumerate(five_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["five"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["observe", "learn"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Quantity recognition phase completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")


def test_quantity_recognition(engine):
    """Test if the engine learned quantity recognition."""
    print("\n\n🔍 TESTING QUANTITY RECOGNITION")
    print("=" * 50)
    
    test_cases = [
        (["ball", "ball", "ball"], "three balls", "three"),
        (["toy", "toy"], "two toys", "two"),
        (["block", "block", "block", "block"], "four blocks", "four"),
        (["apple"], "one apple", "one"),
    ]
    
    results = []
    for visual, description, expected in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        result = engine.live_experience(
            visual=visual + ["quantity"],
            auditory=["how", "many"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["identify", "count"], surprise=0.4, satisfaction=0.0
        )
        
        field = result['activation_field']
        expected_activation = field.get(expected, 0)
        quantity_activation = field.get('quantity', 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        print(f"   'quantity' concept activation: {quantity_activation:.3f}")
        
        success = abs(expected_activation) > 0.5
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   ✅ CORRECT: Quantity recognized")
        else:
            print(f"   ❌ INCORRECT: Quantity not recognized")
    
    return results


def teach_counting_sequence(engine):
    """Phase 2: Teach counting as ordered sequence."""
    print("\n\n🔢 PHASE 2: COUNTING SEQUENCE")
    print("=" * 50)
    
    # Teach counting through progressive building
    counting_experiences = [
        # Start with one
        (["object"], ["one"], "counting one"),
        
        # Add second object
        (["object", "object"], ["one", "two"], "counting to two"),
        
        # Add third object
        (["object", "object", "object"], ["one", "two", "three"], "counting to three"),
        
        # Add fourth object
        (["object", "object", "object", "object"], ["one", "two", "three", "four"], "counting to four"),
        
        # Add fifth object
        (["object", "object", "object", "object", "object"], ["one", "two", "three", "four", "five"], "counting to five"),
        
        # Practice different starting points
        (["object", "object"], ["one", "two"], "counting two"),
        (["object", "object", "object"], ["one", "two", "three"], "counting three"),
        (["object", "object", "object", "object"], ["one", "two", "three", "four"], "counting four"),
    ]
    
    print("\n📚 Learning counting sequence...")
    for i, (visual, auditory, description) in enumerate(counting_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual + ["counting", "sequence"],
            auditory=auditory + ["count"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["count", "sequence"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Counting sequence phase completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def teach_quantity_relationships(engine):
    """Phase 3: Teach relationships between quantities."""
    print("\n\n📊 PHASE 3: QUANTITY RELATIONSHIPS")
    print("=" * 50)
    
    # Teach more/less relationships
    relationship_experiences = [
        # More relationships
        (["object", "object", "object"], ["object", "object"], ["three", "more", "two"], "three more than two"),
        (["object", "object", "object", "object"], ["object", "object"], ["four", "more", "two"], "four more than two"),
        (["object", "object", "object", "object"], ["object", "object", "object"], ["four", "more", "three"], "four more than three"),
        (["object", "object", "object", "object", "object"], ["object", "object", "object"], ["five", "more", "three"], "five more than three"),
        
        # Less relationships
        (["object", "object"], ["object", "object", "object"], ["two", "less", "three"], "two less than three"),
        (["object", "object"], ["object", "object", "object", "object"], ["two", "less", "four"], "two less than four"),
        (["object", "object", "object"], ["object", "object", "object", "object"], ["three", "less", "four"], "three less than four"),
        
        # Equal relationships
        (["object", "object"], ["block", "block"], ["two", "same", "two"], "two same as two"),
        (["object", "object", "object"], ["block", "block", "block"], ["three", "same", "three"], "three same as three"),
    ]
    
    print("\n📚 Learning quantity relationships...")
    for i, (visual1, visual2, auditory, description) in enumerate(relationship_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=visual1 + ["compare"] + visual2,
            auditory=auditory + ["relationship"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["compare", "understand"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Quantity relationships phase completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def teach_quantity_operations(engine):
    """Phase 4: Teach operations on quantities."""
    print("\n\n🧮 PHASE 4: QUANTITY OPERATIONS")
    print("=" * 50)
    
    # Teach addition through concrete combination
    addition_experiences = [
        # Start with simple combinations
        (["object"], ["object"], ["object", "object"], ["one", "add", "one", "makes", "two"], "1+1=2"),
        (["object", "object"], ["object"], ["object", "object", "object"], ["two", "add", "one", "makes", "three"], "2+1=3"),
        (["object"], ["object", "object"], ["object", "object", "object"], ["one", "add", "two", "makes", "three"], "1+2=3"),
        (["object", "object"], ["object", "object"], ["object", "object", "object", "object"], ["two", "add", "two", "makes", "four"], "2+2=4"),
        (["object", "object", "object"], ["object"], ["object", "object", "object", "object"], ["three", "add", "one", "makes", "four"], "3+1=4"),
        (["object", "object", "object"], ["object", "object"], ["object", "object", "object", "object", "object"], ["three", "add", "two", "makes", "five"], "3+2=5"),
        (["object", "object"], ["object", "object", "object"], ["object", "object", "object", "object", "object"], ["two", "add", "three", "makes", "five"], "2+3=5"),
    ]
    
    print("\n📚 Learning addition through concrete combination...")
    for i, (group1, group2, combined, auditory, description) in enumerate(addition_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + combined,
            auditory=auditory + ["addition"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["combine", "add"], surprise=0.3, satisfaction=0.7
        )
        time.sleep(0.05)
    
    print(f"\n✅ Quantity operations phase completed")
    state = engine.get_cognitive_state()
    print(f"   Resonance patterns: {state['resonance_patterns']}")


def test_quantity_operations(engine):
    """Test if the engine learned quantity-based operations."""
    print("\n\n🔍 TESTING QUANTITY OPERATIONS")
    print("=" * 50)
    
    test_cases = [
        # Addition tests with concrete quantities
        (["object", "object", "object"], ["object"], "3+1=?", "four"),
        (["object"], ["object", "object", "object"], "1+3=?", "four"),
        (["object", "object"], ["object", "object", "object"], "2+3=?", "five"),
        (["object", "object", "object", "object"], ["object"], "4+1=?", "five"),
    ]
    
    results = []
    for group1, group2, description, expected in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        result = engine.live_experience(
            visual=group1 + ["plus"] + group2 + ["equals"] + ["?"],
            auditory=["how", "many", "total"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["add", "calculate"], surprise=0.5, satisfaction=0.0
        )
        
        field = result['activation_field']
        expected_activation = field.get(expected, 0)
        add_activation = field.get('add', 0)
        makes_activation = field.get('makes', 0)
        
        print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
        print(f"   'add' operation activation: {add_activation:.3f}")
        print(f"   'makes' result activation: {makes_activation:.3f}")
        
        success = abs(expected_activation) > 0.5
        results.append((description, success, expected_activation))
        
        if success:
            print(f"   ✅ CORRECT: Quantity addition successful")
        else:
            print(f"   ❌ INCORRECT: Quantity addition failed")
    
    return results


def run_quantity_grounded_learning():
    """Run the complete quantity-grounded learning sequence."""
    print("🧠 QUANTITY-GROUNDED MATHEMATICAL LEARNING")
    print("=" * 70)
    print("Teaching math through natural developmental sequence")
    print("=" * 70)
    
    start_time = time.time()
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Phase 1: Quantity recognition
    teach_quantity_recognition(engine)
    quantity_results = test_quantity_recognition(engine)
    
    # Phase 2: Counting sequence
    teach_counting_sequence(engine)
    
    # Phase 3: Quantity relationships
    teach_quantity_relationships(engine)
    
    # Phase 4: Quantity operations
    teach_quantity_operations(engine)
    operation_results = test_quantity_operations(engine)
    
    end_time = time.time()
    
    # Analysis
    print("\n\n📊 QUANTITY-GROUNDED LEARNING RESULTS")
    print("=" * 70)
    
    print(f"\n🔢 QUANTITY RECOGNITION:")
    correct_quantity = sum(1 for _, success, _ in quantity_results if success)
    print(f"   Correct: {correct_quantity}/{len(quantity_results)}")
    for desc, success, activation in quantity_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    print(f"\n🧮 QUANTITY OPERATIONS:")
    correct_operations = sum(1 for _, success, _ in operation_results if success)
    print(f"   Correct: {correct_operations}/{len(operation_results)}")
    for desc, success, activation in operation_results:
        status = "✅" if success else "❌"
        print(f"   {status} {desc}: {activation:.3f}")
    
    # Overall assessment
    total_correct = correct_quantity + correct_operations
    total_tests = len(quantity_results) + len(operation_results)
    
    print(f"\n🎯 OVERALL PERFORMANCE:")
    print(f"   Total correct: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print(f"   Learning time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n🧠 FINAL COGNITIVE STATE:")
    print(f"   Total experiences: {final_state['total_experiences']}")
    print(f"   Active symbols: {final_state['active_symbol_count']}")
    print(f"   Resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Dream cycles: {final_state['replay_cycles']}")
    
    # Show top symbol activations
    print(f"\n📊 TOP SYMBOL ACTIVATIONS:")
    field = engine.experience_stream.get_current_activation_field()
    if field:
        sorted_field = sorted(field.items(), key=lambda x: abs(x[1]), reverse=True)
        for symbol, activation in sorted_field[:10]:
            strength = "🔥" if abs(activation) > 1.0 else "⚡" if abs(activation) > 0.5 else "✨"
            print(f"   {strength} {symbol}: {activation:.3f}")
    
    if total_correct/total_tests > 0.7:
        print(f"\n🎉 BREAKTHROUGH: Quantity-grounded learning achieved!")
        print(f"   Engine learned mathematics through natural developmental sequence")
        print(f"   Concrete quantities → Abstract numbers → Operations")
    else:
        print(f"\n🤔 PROGRESS: Quantity grounding showing promise")
        print(f"   Natural learning sequence partially working")


if __name__ == "__main__":
    run_quantity_grounded_learning() 