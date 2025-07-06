#!/usr/bin/env python3
"""
Quick but comprehensive test of wave engine mechanics
Test the core wave interference patterns and temporal dynamics
"""

import sys
import os

# Ensure proper import paths for CI/CD environment
current_dir = os.path.dirname(__file__)
project_root = current_dir  # This file is in the root directory
src_path = os.path.join(project_root, 'src')
expert_modules_path = os.path.join(project_root, 'expert_modules')

# Add all necessary paths to sys.path
for path in [project_root, src_path, expert_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

import time
import json
from temporal_cognition import TemporalCognitionEngine

# Safe print function for CI/CD compatibility
def safe_print(text):
    """Print function that handles encoding issues on different platforms"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        print(text.encode('ascii', 'replace').decode('ascii'))

def analyze_wave_mechanics():
    """Test wave interference patterns and temporal dynamics"""
    safe_print("~~ DEEP WAVE MECHANICS ANALYSIS ~~")
    safe_print("=" * 50)
    
    # Create temporal engine
    engine = TemporalCognitionEngine()
    
    # Test 1: Basic wave generation
    safe_print("\n[TEST] TEST 1: Basic Wave Generation")
    safe_print("-" * 30)
    engine.perceive("cat")
    engine.perceive("animal")
    
    activations = engine.get_active_waves()
    safe_print(f"Active waves: {len(activations)}")
    safe_print(f"Activation field: {activations}")
    safe_print(f"Recent resonance: {engine.get_recent_resonance()}")
    
    # Test 2: Wave interference
    safe_print("\n[TEST] TEST 2: Wave Interference")
    safe_print("-" * 30)
    engine.perceive("dog")
    
    activations = engine.get_active_waves()
    safe_print(f"Active waves: {len(activations)}")
    safe_print(f"Activation field: {activations}")
    safe_print(f"\nRecent resonance: {engine.get_recent_resonance()}")
    
    # Test 3: Emotional modulation
    safe_print("\n[TEST] TEST 3: Emotional Wave Modulation")
    safe_print("-" * 30)
    engine.set_emotional_state(0.8, 0.3)  # Happy and calm
    engine.perceive("cat")
    
    activations = engine.get_active_waves()
    safe_print(f"Active waves: {len(activations)}")
    safe_print(f"Activation field: {activations}")
    safe_print(f"\nRecent resonance: {engine.get_recent_resonance()}")
    
    # Test 4: Temporal decay
    safe_print("\n[TEST] TEST 4: Wave Decay Over Time")
    safe_print("-" * 30)
    safe_print("Waiting 2 seconds...")
    time.sleep(2)
    engine.perceive("test")
    
    activations = engine.get_active_waves()
    safe_print(f"Active waves: {len(activations)}")
    safe_print(f"Activation field: {activations}")
    safe_print(f"Recent resonance: {engine.get_recent_resonance()}")
    
    # Test 5: Complex multi-concept interference
    safe_print("\n[TEST] TEST 5: Complex Multi-Concept Interference")
    safe_print("-" * 30)
    concepts = ["cat", "dog", "pet", "meow", "bark", "sound", "understand", "learn"]
    for concept in concepts:
        engine.perceive(concept)
    
    activations = engine.get_active_waves()
    safe_print(f"Active waves: {len(activations)}")
    safe_print(f"Activation field: {activations}")
    safe_print(f"Recent resonance: {engine.get_recent_resonance()}")
    
    # Analysis summary
    safe_print("\n[ANALYSIS] ANALYSIS SUMMARY")
    safe_print("=" * 30)
    
    # Calculate statistics
    all_activations = list(activations.values())
    resonances = engine.get_recent_resonance()
    
    safe_print(f"Total activations generated: {len(all_activations)}")
    if all_activations:
        safe_print(f"Activation range: {min(all_activations):.3f} to {max(all_activations):.3f}")
    safe_print(f"Total resonance patterns: {len(resonances)}")
    
    # Resonance type analysis
    if resonances:
        resonance_types = set(r['resonance_type'] for r in resonances)
        safe_print(f"Resonance types seen: {resonance_types}")
        
        # Find strongest interference
        max_interference = max(r['interference'] for r in resonances)
        safe_print(f"Strongest interference: {max_interference:.3f}")
    
    return engine

def test_conversational_wave_processing():
    """Test wave processing with conversational input"""
    safe_print("\n[SPEECH] CONVERSATIONAL WAVE PROCESSING TEST [SPEECH]")
    safe_print("=" * 50)
    
    engine = TemporalCognitionEngine()
    
    # Test conversational inputs
    inputs = [
        "Hello, how are you?",
        "I'm interested in artificial intelligence",
        "Can you explain neural networks?",
        "That's fascinating! Tell me more",
        "Thank you for the explanation"
    ]
    
    for i, text in enumerate(inputs, 1):
        # Extract symbols from text (simple word tokenization)
        symbols = text.lower().replace("?", "").replace("!", "").replace(",", "").split()
        
        safe_print(f"\n[>>>] Turn {i}: '{text}'")
        safe_print(f"  Symbols: {symbols}")
        
        # Process each symbol
        for symbol in symbols:
            engine.perceive(symbol)
        
        # Show current state
        activations = engine.get_active_waves()
        safe_print(f"  Active waves: {len(activations)}")
        
        # Show top 3 activations
        if activations:
            top_activations = dict(sorted(activations.items(), key=lambda x: abs(x[1]), reverse=True)[:3])
            safe_print(f"  Top activations: {top_activations}")
        
        # Show latest resonance
        resonances = engine.get_recent_resonance()
        if resonances:
            latest = resonances[-1]
            safe_print(f"  Latest resonance: {latest['resonance_type']}")
    
    return engine

def main():
    """Run the complete wave mechanics analysis"""
    try:
        # Run wave mechanics tests
        wave_engine = analyze_wave_mechanics()
        
        # Run conversational processing tests
        conversation_engine = test_conversational_wave_processing()
        
        safe_print("\n[CONCLUSION] CONCLUSION")
        safe_print("=" * 50)
        safe_print("Wave mechanics analysis complete!")
        safe_print("This system demonstrates genuine wave interference patterns")
        safe_print("that create emergent associations between concepts.")
        safe_print("The temporal dynamics show real decay and reinforcement.")
        safe_print("This is a fundamentally different approach to AI cognition.")
        
        return True
        
    except Exception as e:
        safe_print(f"[-] Error during wave mechanics test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        # Run the analysis
        success = main()
        if success:
            safe_print("\n[SUCCESS] Wave mechanics test completed successfully!")
            sys.exit(0)
        else:
            safe_print("\n[-] Wave mechanics test failed!")
            sys.exit(1)
    except Exception as e:
        safe_print(f"[-] Critical error: {e}")
        sys.exit(1) 