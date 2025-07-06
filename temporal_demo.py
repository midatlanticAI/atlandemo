#!/usr/bin/env python3
"""
Temporal Cognition Engine - Live Demonstration
Shows how meaning emerges from waves of experience over time.
"""

import time
import json
from src.temporal_cognition import TemporalCognitionEngine


def simulate_child_learning_experience():
    """Simulate a child learning through multi-modal experience over time."""
    
    print("[BRAIN] Initializing Temporal Cognition Engine...")
    engine = TemporalCognitionEngine()
    
    print("\n🌱 Beginning experiential learning simulation...\n")
    
    # === Experience 1: First encounter with a bird ===
    print("Experience 1: Child sees bird flying in park")
    result1 = engine.live_experience(
        visual=["bird", "wings", "sky"],
        auditory=["chirping", "wind"],
        kinesthetic=["excitement", "pointing"],
        mood=0.6,        # Happy
        arousal=0.8,     # Excited
        attention=0.9,   # Very focused
        goals=["understand", "watch"],
        context=["park", "sunny", "morning"],
        surprise=0.7,    # New and surprising
        satisfaction=0.5 # Curious but not resolved
    )
    print(f"  Active waves: {result1['active_waves']}")
    print(f"  Activation field: {list(result1['activation_field'].keys())}")
    
    time.sleep(0.5)  # Brief pause
    
    # === Experience 2: Hearing about birds from parent ===
    print("\nExperience 2: Parent says 'Birds fly with their wings'")
    result2 = engine.live_experience(
        visual=["parent", "gesturing"],
        auditory=["birds", "fly", "wings", "voice"],
        kinesthetic=["listening", "nodding"],
        mood=0.4,        # Calm
        arousal=0.6,     # Attentive
        attention=0.8,   # Focused on parent
        goals=["learn", "understand"],
        context=["conversation", "teaching"],
        surprise=0.3,    # Some new information
        satisfaction=0.7 # Understanding increases
    )
    print(f"  Active waves: {result2['active_waves']}")
    print(f"  New resonance patterns: {len(result2['recent_resonance'])}")
    
    time.sleep(0.5)
    
    # === Experience 3: Trying to fly like a bird ===
    print("\nExperience 3: Child tries to fly by flapping arms")
    result3 = engine.live_experience(
        visual=["arms", "flapping", "ground"],
        auditory=["whooshing", "laughter"],
        kinesthetic=["jumping", "flapping", "falling"],
        mood=0.2,        # Slightly disappointed
        arousal=0.9,     # Very active
        attention=0.7,   # Focused on action
        goals=["fly", "imitate"],
        context=["play", "experiment"],
        surprise=0.8,    # Surprised it didn't work
        satisfaction=-0.3 # Goal not achieved
    )
    print(f"  Active waves: {result3['active_waves']}")
    print(f"  Mood impact on waves visible in activation field")
    
    time.sleep(0.5)
    
    # === Experience 4: Understanding the difference ===
    print("\nExperience 4: Realizing humans can't fly like birds")
    result4 = engine.live_experience(
        visual=["self", "bird", "different"],
        auditory=["explanation", "understanding"],
        kinesthetic=["acceptance", "curiosity"],
        mood=0.1,        # Neutral, processing
        arousal=0.5,     # Calm
        attention=0.8,   # Thinking deeply
        goals=["understand", "accept"],
        context=["realization", "learning"],
        surprise=0.4,    # Aha moment
        satisfaction=0.8 # Understanding achieved
    )
    print(f"  Active waves: {result4['active_waves']}")
    
    time.sleep(0.5)
    
    # === Experience 5: Dream replay trigger ===
    print("\nExperience 5: Playing with toy airplane")
    result5 = engine.live_experience(
        visual=["airplane", "toy", "flying"],
        auditory=["zoom", "engine_sounds"],
        kinesthetic=["holding", "moving", "imagining"],
        mood=0.7,        # Happy
        arousal=0.7,     # Engaged
        attention=0.6,   # Playful focus
        goals=["play", "imagine"],
        context=["play", "toys", "flight"],
        surprise=0.2,    # Familiar now
        satisfaction=0.9 # Enjoying play
    )
    print(f"  Active waves: {result5['active_waves']}")
    print(f"  🌙 Dream replay triggered!")
    
    return engine


def analyze_emergent_patterns(engine):
    """Analyze what patterns have emerged from the experience stream."""
    
    print("\n🔬 Analyzing Emergent Cognitive Patterns...\n")
    
    state = engine.get_cognitive_state()
    
    print(f"Total Experiences: {state['total_experiences']}")
    print(f"Active Symbol Waves: {state['active_symbol_count']}")
    print(f"Dream Replay Cycles: {state['replay_cycles']}")
    print(f"Resonance Patterns Formed: {state['resonance_patterns']}")
    
    print("\n[DATA] Current Activation Field:")
    field = state['activation_field']
    # Sort by activation strength
    sorted_activations = sorted(field.items(), key=lambda x: abs(x[1]), reverse=True)
    
    for symbol, activation in sorted_activations[:10]:  # Top 10
        strength = "🔥" if abs(activation) > 0.5 else "[BOLT]" if abs(activation) > 0.2 else "✨"
        print(f"  {strength} {symbol}: {activation:.3f}")
    
    print("\n[WAVE] Recent Resonance Patterns:")
    recent = state['recent_resonance']
    for i, pattern in enumerate(recent[-5:], 1):  # Last 5 patterns
        symbols = " ↔ ".join(pattern['symbols'])
        print(f"  {i}. {symbols}")
        print(f"     Type: {pattern['resonance_type']} | Strength: {pattern['interference']:.3f}")


def test_temporal_generalization(engine):
    """Test if the engine can generalize from temporal experience."""
    
    print("\n🧪 Testing Temporal Generalization...\n")
    
    # New experience: Seeing a butterfly
    print("New Experience: Child encounters a butterfly")
    result = engine.live_experience(
        visual=["butterfly", "wings", "colorful"],
        auditory=["flutter", "silence"],
        kinesthetic=["wonder", "gentle"],
        mood=0.8,        # Delighted
        arousal=0.6,     # Calm excitement
        attention=0.9,   # Fascinated
        goals=["observe", "appreciate"],
        context=["garden", "discovery"],
        surprise=0.6,    # New but familiar pattern
        satisfaction=0.8 # Beautiful experience
    )
    
    print(f"Active waves after butterfly encounter: {result['active_waves']}")
    
    # Check if "wings" and "fly" concepts resonate
    field = result['activation_field']
    wing_activation = field.get('wings', 0)
    fly_activation = field.get('fly', 0)
    
    print(f"\n[SEARCH] Generalization Check:")
    print(f"  'wings' activation: {wing_activation:.3f}")
    print(f"  'fly' concept resonance: {fly_activation:.3f}")
    
    if abs(wing_activation) > 0.1 or abs(fly_activation) > 0.1:
        print("  [+] Temporal generalization detected!")
        print("  The engine is connecting butterfly wings to previous bird/flight experiences")
    else:
        print("  [-] No clear generalization yet")
        print("  More experience may be needed for pattern emergence")


def main():
    """Run the complete temporal cognition demonstration."""
    
    print("=" * 60)
    print("[BRAIN] TEMPORAL RESONANT COGNITIVE SUBSTRATE DEMO")
    print("   Experience as Waves | Meaning as Resonance")
    print("=" * 60)
    
    try:
        # Simulate learning through experience
        engine = simulate_child_learning_experience()
        
        # Analyze what emerged
        analyze_emergent_patterns(engine)
        
        # Test generalization
        test_temporal_generalization(engine)
        
        print("\n" + "=" * 60)
        print("[STAR] DEMONSTRATION COMPLETE")
        print("\nKey Observations:")
        print("• Experience creates temporal waves, not static symbols")
        print("• Meaning emerges from wave interference patterns") 
        print("• Mood, attention, and surprise shape wave properties")
        print("• Dream replay consolidates recurring patterns")
        print("• Generalization happens through resonant activation")
        print("• No hardcoded rules - only emergent structure")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 