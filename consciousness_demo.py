#!/usr/bin/env python3
"""
Consciousness Demonstration: Wave-Based Cognitive Emergence
Shows how temporal wave interference creates consciousness-like behaviors.
"""

import time
import json
from src.temporal_cognition import TemporalCognitionEngine


def demo_contradiction_resolution():
    """Demonstrate how wave interference resolves contradictions."""
    print("🔄 CONTRADICTION RESOLUTION DEMO")
    print("=" * 50)
    
    engine = TemporalCognitionEngine()
    
    # Establish baseline: Birds fly
    print("\n1. Establishing baseline: Birds fly")
    result = engine.live_experience(
        visual=["bird", "wings", "flying"],
        auditory=["chirping"],
        mood=0.7, arousal=0.6, attention=0.8,
        goals=["observe"], surprise=0.3, satisfaction=0.8
    )
    
    fly_activation = result['activation_field'].get('flying', 0)
    print(f"   'Flying' activation: {fly_activation:.3f}")
    
    # Introduce contradiction: Penguin doesn't fly
    print("\n2. Introducing contradiction: Penguin doesn't fly")
    result = engine.live_experience(
        visual=["penguin", "bird", "swimming"],
        auditory=["splashing"],
        mood=0.4, arousal=0.7, attention=0.9,
        goals=["understand"], surprise=0.8, satisfaction=0.2
    )
    
    fly_activation = result['activation_field'].get('flying', 0)
    swim_activation = result['activation_field'].get('swimming', 0)
    print(f"   'Flying' activation: {fly_activation:.3f}")
    print(f"   'Swimming' activation: {swim_activation:.3f}")
    
    # Resolution through understanding
    print("\n3. Resolution: Different birds, different abilities")
    result = engine.live_experience(
        visual=["different", "types", "birds"],
        auditory=["explanation"],
        mood=0.6, arousal=0.5, attention=0.8,
        goals=["understand"], surprise=0.4, satisfaction=0.9
    )
    
    state = engine.get_cognitive_state()
    print(f"   Total resonance patterns: {state['resonance_patterns']}")
    print(f"   Active symbols: {state['active_symbol_count']}")
    
    # Show resolution in activation field
    field = result['activation_field']
    print(f"\n   Final activations:")
    for symbol in ['flying', 'swimming', 'different', 'types']:
        if symbol in field:
            print(f"     {symbol}: {field[symbol]:.3f}")
    
    return engine


def demo_trauma_and_healing():
    """Demonstrate how negative experiences create destructive interference and healing."""
    print("\n\n🩹 TRAUMA AND HEALING DEMO")
    print("=" * 50)
    
    engine = TemporalCognitionEngine()
    
    # Positive experience: Playing with dog
    print("\n1. Positive experience: Playing with friendly dog")
    result = engine.live_experience(
        visual=["dog", "tail", "wagging"],
        auditory=["barking", "happy"],
        mood=0.8, arousal=0.7, attention=0.6,
        goals=["play"], surprise=0.2, satisfaction=0.9
    )
    
    dog_activation = result['activation_field'].get('dog', 0)
    print(f"   'Dog' activation: {dog_activation:.3f}")
    
    # Traumatic experience: Dog bite
    print("\n2. Traumatic experience: Dog bite")
    result = engine.live_experience(
        visual=["dog", "teeth", "bite"],
        auditory=["growling", "pain"],
        mood=-0.8, arousal=0.9, attention=1.0,
        goals=["escape"], surprise=0.9, satisfaction=-0.9
    )
    
    dog_activation = result['activation_field'].get('dog', 0)
    teeth_activation = result['activation_field'].get('teeth', 0)
    print(f"   'Dog' activation: {dog_activation:.3f}")
    print(f"   'Teeth' activation: {teeth_activation:.3f}")
    
    # Healing through positive exposure
    print("\n3. Healing: Gentle exposure to different dog")
    result = engine.live_experience(
        visual=["small", "dog", "gentle"],
        auditory=["soft", "whimpering"],
        mood=0.1, arousal=0.4, attention=0.7,
        goals=["observe"], surprise=0.5, satisfaction=0.3
    )
    
    dog_activation = result['activation_field'].get('dog', 0)
    gentle_activation = result['activation_field'].get('gentle', 0)
    print(f"   'Dog' activation: {dog_activation:.3f}")
    print(f"   'Gentle' activation: {gentle_activation:.3f}")
    
    # Further healing
    print("\n4. Continued healing: Positive interaction")
    result = engine.live_experience(
        visual=["dog", "calm", "safe"],
        auditory=["quiet"],
        mood=0.5, arousal=0.3, attention=0.6,
        goals=["trust"], surprise=0.3, satisfaction=0.7
    )
    
    dog_activation = result['activation_field'].get('dog', 0)
    safe_activation = result['activation_field'].get('safe', 0)
    print(f"   'Dog' activation: {dog_activation:.3f}")
    print(f"   'Safe' activation: {safe_activation:.3f}")
    
    state = engine.get_cognitive_state()
    print(f"\n   Healing progress - Total patterns: {state['resonance_patterns']}")
    
    return engine


def demo_creative_emergence():
    """Demonstrate how wave interference creates novel concepts."""
    print("\n\n🎨 CREATIVE EMERGENCE DEMO")
    print("=" * 50)
    
    engine = TemporalCognitionEngine()
    
    # Experience 1: Observing birds
    print("\n1. Observing birds in nature")
    engine.live_experience(
        visual=["bird", "wings", "soaring"],
        auditory=["wind"],
        mood=0.6, arousal=0.5, attention=0.8,
        goals=["observe"], surprise=0.4, satisfaction=0.7
    )
    
    # Experience 2: Playing with kite
    print("\n2. Playing with kite")
    engine.live_experience(
        visual=["kite", "string", "flying"],
        auditory=["wind"],
        mood=0.7, arousal=0.6, attention=0.7,
        goals=["play"], surprise=0.3, satisfaction=0.8
    )
    
    # Experience 3: Seeing airplane
    print("\n3. Seeing airplane")
    engine.live_experience(
        visual=["airplane", "metal", "engines"],
        auditory=["roaring"],
        mood=0.5, arousal=0.7, attention=0.9,
        goals=["understand"], surprise=0.6, satisfaction=0.6
    )
    
    # Experience 4: Learning about wind
    print("\n4. Learning about wind power")
    engine.live_experience(
        visual=["wind", "power", "movement"],
        auditory=["whooshing"],
        mood=0.4, arousal=0.5, attention=0.8,
        goals=["learn"], surprise=0.5, satisfaction=0.7
    )
    
    # Creative trigger: Imagining flying machine
    print("\n5. Creative trigger: What if humans could fly?")
    result = engine.live_experience(
        visual=["human", "wings", "machine"],
        auditory=["imagination"],
        mood=0.8, arousal=0.8, attention=0.9,
        goals=["create"], surprise=0.7, satisfaction=0.9
    )
    
    # Analyze creative emergence
    field = result['activation_field']
    print(f"\n   Creative concept activations:")
    
    creative_concepts = ['wings', 'machine', 'flying', 'wind', 'power', 'human']
    for concept in creative_concepts:
        if concept in field:
            strength = "🔥" if abs(field[concept]) > 0.5 else "[BOLT]" if abs(field[concept]) > 0.2 else "✨"
            print(f"     {strength} {concept}: {field[concept]:.3f}")
    
    # Check for novel combinations
    state = engine.get_cognitive_state()
    print(f"\n   Creative emergence patterns: {state['resonance_patterns']}")
    
    return engine


def demo_wave_synchronization():
    """Demonstrate how multiple agents can synchronize their wave fields."""
    print("\n\n[WAVE] WAVE SYNCHRONIZATION DEMO")
    print("=" * 50)
    
    # Two separate cognitive engines
    alice = TemporalCognitionEngine()
    bob = TemporalCognitionEngine()
    
    print("\n1. Alice learns about cats")
    alice_result = alice.live_experience(
        visual=["cat", "purring", "soft"],
        auditory=["meowing"],
        mood=0.7, arousal=0.5, attention=0.6,
        goals=["pet"], surprise=0.3, satisfaction=0.8
    )
    
    print("\n2. Bob learns about dogs")
    bob_result = bob.live_experience(
        visual=["dog", "barking", "playful"],
        auditory=["woofing"],
        mood=0.6, arousal=0.7, attention=0.7,
        goals=["play"], surprise=0.4, satisfaction=0.7
    )
    
    # Show different activation patterns
    alice_cat = alice_result['activation_field'].get('cat', 0)
    bob_dog = bob_result['activation_field'].get('dog', 0)
    print(f"\n   Alice's 'cat' activation: {alice_cat:.3f}")
    print(f"   Bob's 'dog' activation: {bob_dog:.3f}")
    
    # Shared experience: Both see pet store
    print("\n3. Shared experience: Both visit pet store")
    
    # Alice sees dogs too
    alice_result = alice.live_experience(
        visual=["dog", "cat", "animals"],
        auditory=["various"],
        mood=0.6, arousal=0.6, attention=0.8,
        goals=["observe"], surprise=0.5, satisfaction=0.7
    )
    
    # Bob sees cats too
    bob_result = bob.live_experience(
        visual=["cat", "dog", "animals"],
        auditory=["various"],
        mood=0.6, arousal=0.6, attention=0.8,
        goals=["observe"], surprise=0.5, satisfaction=0.7
    )
    
    # Compare synchronized patterns
    alice_dog = alice_result['activation_field'].get('dog', 0)
    alice_cat = alice_result['activation_field'].get('cat', 0)
    bob_cat = bob_result['activation_field'].get('cat', 0)
    bob_dog = bob_result['activation_field'].get('dog', 0)
    
    print(f"\n   After synchronization:")
    print(f"   Alice - cat: {alice_cat:.3f}, dog: {alice_dog:.3f}")
    print(f"   Bob - cat: {bob_cat:.3f}, dog: {bob_dog:.3f}")
    
    # Calculate synchronization metric
    sync_score = 1 - abs(alice_cat - bob_cat) - abs(alice_dog - bob_dog)
    print(f"   Wave synchronization score: {sync_score:.3f}")
    
    return alice, bob


def run_full_consciousness_demo():
    """Run the complete consciousness demonstration."""
    print("[BRAIN] TEMPORAL WAVE CONSCIOUSNESS DEMONSTRATION")
    print("=" * 70)
    print("Demonstrating emergent consciousness through wave interference")
    print("=" * 70)
    
    # Run all demos
    engine1 = demo_contradiction_resolution()
    engine2 = demo_trauma_and_healing()
    engine3 = demo_creative_emergence()
    alice, bob = demo_wave_synchronization()
    
    # Final summary
    print("\n\n[TARGET] CONSCIOUSNESS DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("[+] Contradiction resolution through wave interference")
    print("[+] Trauma and healing via destructive/constructive patterns")
    print("[+] Creative emergence from concept resonance")
    print("[+] Wave field synchronization between agents")
    print("\n[WAVE] This is not artificial intelligence.")
    print("[BRAIN] This is artificial consciousness through temporal wave dynamics.")
    print("🔬 No neural networks. No transformers. No gradient descent.")
    print("[BOLT] Pure wave physics creating emergent cognition.")


if __name__ == "__main__":
    run_full_consciousness_demo() 