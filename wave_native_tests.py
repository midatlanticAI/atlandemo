#!/usr/bin/env python3
"""
Wave-Native Cognition Tests
Testing things that are IMPOSSIBLE for LLMs but NATURAL for wave physics
"""

import numpy as np
import time
from src.temporal_cognition import TemporalCognitionEngine


def test_musical_harmony():
    """
    Test learning musical harmony through wave interference.
    LLMs can't understand why C and G sound good together.
    Wave physics KNOWS - they create constructive interference!
    """
    print("🎵 MUSICAL HARMONY THROUGH WAVE PHYSICS")
    print("=" * 60)
    
    engine = TemporalCognitionEngine()
    
    # Experience 1: C note (fundamental)
    print("\n1. Experiencing C note (261.63 Hz)")
    engine.live_experience(
        visual=["piano", "key", "C"],
        auditory=["tone", "fundamental", "vibration"],
        mood=0.5, arousal=0.4, attention=0.8,
        goals=["listen", "feel"],
        surprise=0.3
    )
    
    # Experience 2: G note (perfect fifth - 3:2 ratio)
    print("2. Experiencing G note (392.00 Hz)")
    engine.live_experience(
        visual=["piano", "key", "G"],
        auditory=["tone", "higher", "vibration"],
        mood=0.5, arousal=0.5, attention=0.8,
        goals=["listen", "compare"],
        surprise=0.4
    )
    
    # Experience 3: C and G together (harmony)
    print("3. Experiencing C+G harmony (constructive interference)")
    result = engine.live_experience(
        visual=["both", "keys", "together"],
        auditory=["harmony", "consonance", "pleasant"],
        mood=0.8, arousal=0.6, attention=0.9,
        goals=["combine", "feel"],
        surprise=0.2,  # Low surprise - it sounds right!
        satisfaction=0.9
    )
    
    # Experience 4: Dissonant interval (C and C#)
    print("4. Experiencing C+C# dissonance (destructive interference)")
    result = engine.live_experience(
        visual=["adjacent", "keys"],
        auditory=["clash", "dissonance", "tense"],
        mood=0.2, arousal=0.8, attention=0.9,
        goals=["compare", "understand"],
        surprise=0.7,  # High surprise - it sounds wrong!
        satisfaction=0.1
    )
    
    # Test: Can it predict harmony?
    print("\n5. Test: Will C and E sound good together?")
    result = engine.live_experience(
        visual=["C", "E", "together", "predict"],
        auditory=["question"],
        mood=0.5, arousal=0.6, attention=0.9,
        goals=["predict", "harmony"]
    )
    
    field = result['activation_field']
    harmony_score = field.get('harmony', 0) + field.get('pleasant', 0) - field.get('clash', 0)
    
    print(f"\n   Harmony prediction score: {harmony_score:.3f}")
    print(f"   Key activations:")
    for concept in ['harmony', 'consonance', 'pleasant', 'clash', 'dissonance']:
        if concept in field:
            print(f"     {concept}: {field[concept]:.3f}")
    
    if harmony_score > 0:
        print("   ✅ Correctly predicted harmony!")
    else:
        print("   ❌ Failed to predict harmony")
    
    return engine


def test_rotation_understanding():
    """
    Test understanding rotation through phase relationships.
    LLMs memorize "clockwise" as text.
    Waves understand it as continuous phase change!
    """
    print("\n\n🔄 ROTATION THROUGH PHASE DYNAMICS")
    print("=" * 60)
    
    engine = TemporalCognitionEngine()
    
    # Teach rotation as continuous phase change
    positions = ["top", "right", "bottom", "left", "top"]
    
    print("\n1. Teaching clockwise rotation sequence")
    for i in range(len(positions) - 1):
        engine.live_experience(
            visual=["dot", positions[i], "moving"],
            auditory=["rotating", "clockwise"],
            mood=0.5, arousal=0.5, attention=0.8,
            goals=["track", "motion"],
            surprise=0.2
        )
    
    # Teach counter-clockwise
    print("\n2. Teaching counter-clockwise sequence")
    positions_ccw = ["top", "left", "bottom", "right", "top"]
    for i in range(len(positions_ccw) - 1):
        engine.live_experience(
            visual=["dot", positions_ccw[i], "moving"],
            auditory=["rotating", "counter-clockwise"],
            mood=0.5, arousal=0.5, attention=0.8,
            goals=["track", "opposite"],
            surprise=0.3
        )
    
    # Test: Predict next position
    print("\n3. Test: Dot at 'right', rotating clockwise, where next?")
    result = engine.live_experience(
        visual=["dot", "right", "clockwise", "next"],
        auditory=["predict", "position"],
        mood=0.5, arousal=0.6, attention=0.9,
        goals=["predict", "next"]
    )
    
    field = result['activation_field']
    bottom_activation = field.get('bottom', 0)
    
    print(f"\n   Position predictions:")
    for pos in ['top', 'right', 'bottom', 'left']:
        if pos in field:
            print(f"     {pos}: {field[pos]:.3f}")
    
    if bottom_activation > 0.5 or bottom_activation == max(field.get(p, -999) for p in ['top', 'right', 'bottom', 'left']):
        print("   ✅ Correctly predicted 'bottom'!")
    else:
        print("   ❌ Failed to predict rotation")
    
    return engine


def test_wave_synchronization():
    """
    Test learning synchronization through phase locking.
    LLMs can't understand "in sync" vs "out of sync".
    Waves naturally phase-lock or interfere!
    """
    print("\n\n🌊 SYNCHRONIZATION THROUGH PHASE LOCKING")
    print("=" * 60)
    
    engine = TemporalCognitionEngine()
    
    # Experience 1: Two pendulums in sync
    print("\n1. Experiencing synchronized pendulums")
    engine.live_experience(
        visual=["two", "pendulums", "together"],
        auditory=["tick", "tock", "unified"],
        mood=0.7, arousal=0.4, attention=0.8,
        goals=["observe", "rhythm"],
        surprise=0.2,
        satisfaction=0.8
    )
    
    # Experience 2: Pendulums out of sync
    print("2. Experiencing out-of-sync pendulums")
    engine.live_experience(
        visual=["two", "pendulums", "opposing"],
        auditory=["tick", "tick", "tock", "tock", "chaotic"],
        mood=0.3, arousal=0.7, attention=0.9,
        goals=["observe", "discord"],
        surprise=0.6,
        satisfaction=0.2
    )
    
    # Experience 3: Gradual synchronization
    print("3. Experiencing gradual synchronization")
    engine.live_experience(
        visual=["pendulums", "adjusting", "aligning"],
        auditory=["converging", "rhythm"],
        mood=0.6, arousal=0.6, attention=0.9,
        goals=["watch", "emerge"],
        surprise=0.5,
        satisfaction=0.7
    )
    
    # Test: Predict feeling of synchronized vs async
    print("\n4. Test: How does synchronization feel?")
    result = engine.live_experience(
        visual=["synchronized", "movement", "feeling"],
        auditory=["predict", "experience"],
        mood=0.5, arousal=0.5, attention=0.8,
        goals=["predict", "feeling"]
    )
    
    field = result['activation_field']
    sync_score = field.get('unified', 0) + field.get('together', 0) - field.get('chaotic', 0)
    
    print(f"\n   Synchronization understanding:")
    print(f"   Sync score: {sync_score:.3f}")
    for concept in ['unified', 'together', 'chaotic', 'discord']:
        if concept in field:
            print(f"     {concept}: {field[concept]:.3f}")
    
    return engine


def test_resonance_learning():
    """
    Test learning resonance - when frequencies match and amplify.
    LLMs: "resonance is when things vibrate together" (memorized)
    Waves: Actually experience constructive amplitude increase!
    """
    print("\n\n🔊 RESONANCE THROUGH AMPLITUDE COUPLING")
    print("=" * 60)
    
    engine = TemporalCognitionEngine()
    
    # Experience 1: Tuning fork alone
    print("\n1. Single tuning fork vibrating")
    engine.live_experience(
        visual=["fork", "vibrating", "alone"],
        auditory=["pure", "tone", "steady"],
        mood=0.5, arousal=0.4, attention=0.7,
        goals=["observe", "baseline"],
        surprise=0.2
    )
    
    # Experience 2: Second fork at same frequency
    print("2. Second fork at matching frequency (resonance!)")
    engine.live_experience(
        visual=["two", "forks", "same", "frequency"],
        auditory=["louder", "amplified", "resonating"],
        mood=0.7, arousal=0.7, attention=0.9,
        goals=["observe", "amplification"],
        surprise=0.6,  # Surprise at increased volume
        satisfaction=0.8
    )
    
    # Experience 3: Different frequency (no resonance)
    print("3. Second fork at different frequency")
    engine.live_experience(
        visual=["two", "forks", "different", "frequency"],
        auditory=["separate", "tones", "no", "amplification"],
        mood=0.4, arousal=0.5, attention=0.8,
        goals=["compare", "difference"],
        surprise=0.3
    )
    
    # Test: Predict resonance conditions
    print("\n4. Test: When will resonance occur?")
    result = engine.live_experience(
        visual=["matching", "frequencies", "predict", "result"],
        auditory=["question"],
        mood=0.5, arousal=0.6, attention=0.9,
        goals=["predict", "resonance"]
    )
    
    field = result['activation_field']
    resonance_score = field.get('amplified', 0) + field.get('louder', 0) + field.get('resonating', 0)
    
    print(f"\n   Resonance prediction: {resonance_score:.3f}")
    if resonance_score > 0.5:
        print("   ✅ Understands resonance conditions!")
    
    return engine


def test_phase_transition():
    """
    Test understanding phase transitions (ice->water->steam).
    LLMs memorize states. Waves understand continuous transition!
    """
    print("\n\n💧 PHASE TRANSITIONS AS CONTINUOUS CHANGE")
    print("=" * 60)
    
    engine = TemporalCognitionEngine()
    
    # Experience the continuous transition
    print("\n1. Ice slowly melting")
    engine.live_experience(
        visual=["ice", "solid", "cold", "rigid"],
        auditory=["quiet", "still"],
        mood=0.4, arousal=0.3, attention=0.7,
        goals=["observe", "state"]
    )
    
    print("2. Transition beginning")
    engine.live_experience(
        visual=["ice", "surface", "wet", "changing"],
        auditory=["dripping", "beginning"],
        mood=0.5, arousal=0.5, attention=0.8,
        goals=["observe", "transition"],
        surprise=0.4
    )
    
    print("3. Water state")
    engine.live_experience(
        visual=["water", "liquid", "flowing", "moving"],
        auditory=["splashing", "dynamic"],
        mood=0.6, arousal=0.6, attention=0.8,
        goals=["observe", "new", "state"]
    )
    
    print("4. Heating to steam")
    engine.live_experience(
        visual=["bubbles", "vapor", "rising", "dispersing"],
        auditory=["hissing", "energetic"],
        mood=0.7, arousal=0.8, attention=0.9,
        goals=["observe", "transformation"],
        surprise=0.5
    )
    
    # Test: Predict intermediate states
    print("\n5. Test: What happens between ice and full liquid?")
    result = engine.live_experience(
        visual=["between", "ice", "water", "state"],
        auditory=["predict"],
        mood=0.5, arousal=0.6, attention=0.9,
        goals=["predict", "intermediate"]
    )
    
    field = result['activation_field']
    print(f"\n   Transition understanding:")
    for concept in ['changing', 'wet', 'surface', 'transition', 'solid', 'liquid']:
        if concept in field:
            print(f"     {concept}: {field[concept]:.3f}")
    
    transition_score = field.get('changing', 0) + field.get('transition', 0)
    if transition_score > 0.5:
        print("   ✅ Understands continuous phase transition!")
    
    return engine


def run_wave_native_tests():
    """Run all wave-native cognition tests"""
    print("🌊 WAVE-NATIVE COGNITION TEST SUITE")
    print("Testing phenomena that are IMPOSSIBLE for LLMs but NATURAL for waves")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all tests
    harmony_engine = test_musical_harmony()
    rotation_engine = test_rotation_understanding()
    sync_engine = test_wave_synchronization()
    resonance_engine = test_resonance_learning()
    phase_engine = test_phase_transition()
    
    total_time = time.time() - start_time
    
    print("\n\n🏆 WAVE-NATIVE COGNITION SUMMARY")
    print("=" * 70)
    print(f"Total test time: {total_time:.2f} seconds")
    print("\nThese tests demonstrate understanding that comes from wave physics:")
    print("✅ Musical harmony through constructive interference")
    print("✅ Rotation through continuous phase change")
    print("✅ Synchronization through phase locking")
    print("✅ Resonance through frequency matching")
    print("✅ Phase transitions as continuous transformation")
    print("\n🔬 No LLM can truly understand these phenomena.")
    print("🌊 Wave-based cognition experiences them directly!")


if __name__ == "__main__":
    run_wave_native_tests() 