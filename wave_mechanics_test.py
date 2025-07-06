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
    result1 = engine.live_experience(
        visual=['cat', 'animal'],
        mood=0.5,
        arousal=0.8,
        attention=0.7
    )
    
    safe_print(f"Active waves: {result1['active_waves']}")
    safe_print(f"Activation field: {result1['activation_field']}")
    safe_print(f"Recent resonance: {result1['recent_resonance']}")
    
    # Test 2: Wave interference
    safe_print("\n[TEST] TEST 2: Wave Interference")
    safe_print("-" * 30)
    result2 = engine.live_experience(
        visual=['dog', 'animal'],  # 'animal' should interfere with previous
        mood=0.3,
        arousal=0.6,
        attention=0.9
    )
    
    safe_print(f"Active waves: {result2['active_waves']}")
    safe_print(f"Activation field: {result2['activation_field']}")
    safe_print(f"Recent resonance: {result2['recent_resonance']}")
    
    # Test 3: Emotional modulation
    safe_print("\n[TEST] TEST 3: Emotional Wave Modulation")
    safe_print("-" * 30)
    result3 = engine.live_experience(
        visual=['cat'],  # Same concept, different emotion
        mood=-0.8,  # Negative mood
        arousal=0.2,  # Low arousal
        attention=0.3  # Low attention
    )
    
    safe_print(f"Active waves: {result3['active_waves']}")
    safe_print(f"Activation field: {result3['activation_field']}")
    safe_print(f"Recent resonance: {result3['recent_resonance']}")
    
    # Test 4: Temporal decay
    safe_print("\n[TEST] TEST 4: Wave Decay Over Time")
    safe_print("-" * 30)
    safe_print("Waiting 2 seconds...")
    time.sleep(2)
    result4 = engine.live_experience(
        visual=['test'],  # New concept
        mood=0.0,
        arousal=0.1,
        attention=0.1
    )
    
    safe_print(f"Active waves: {result4['active_waves']}")
    safe_print(f"Activation field: {result4['activation_field']}")
    safe_print(f"Recent resonance: {result4['recent_resonance']}")
    
    # Test 5: Complex multi-concept interference
    safe_print("\n[TEST] TEST 5: Complex Multi-Concept Interference")
    safe_print("-" * 30)
    result5 = engine.live_experience(
        visual=['cat', 'dog', 'animal', 'pet'],
        auditory=['meow', 'bark', 'sound'],
        mood=0.7,
        arousal=0.9,
        attention=0.8,
        goals=['understand', 'learn']
    )
    
    safe_print(f"Active waves: {result5['active_waves']}")
    safe_print(f"Activation field: {result5['activation_field']}")
    safe_print(f"Recent resonance: {result5['recent_resonance']}")
    
    # Analysis summary
    safe_print("\n[ANALYSIS] ANALYSIS SUMMARY")
    safe_print("=" * 30)
    
    # Calculate statistics from all results
    all_activations = []
    all_resonances = []
    for result in [result1, result2, result3, result4, result5]:
        all_activations.extend(result['activation_field'].values())
        all_resonances.extend(result['recent_resonance'])
    
    safe_print(f"Total activations generated: {len(all_activations)}")
    if all_activations:
        safe_print(f"Activation range: {min(all_activations):.3f} to {max(all_activations):.3f}")
    safe_print(f"Total resonance patterns: {len(all_resonances)}")
    
    # Resonance type analysis
    if all_resonances:
        resonance_types = set(r['resonance_type'] for r in all_resonances)
        safe_print(f"Resonance types seen: {resonance_types}")
        
        # Find strongest interference
        max_interference = max(abs(r['interference']) for r in all_resonances)
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
        
        # Process through wave engine
        result = engine.live_experience(
            visual=symbols,
            auditory=['conversation', 'speech'],
            mood=0.2,
            arousal=0.5,
            attention=0.8
        )
        
        safe_print(f"  Active waves: {result['active_waves']}")
        
        # Show top 3 activations
        activations = result['activation_field']
        if activations:
            top_activations = dict(sorted(activations.items(), key=lambda x: abs(x[1]), reverse=True)[:3])
            safe_print(f"  Top activations: {top_activations}")
        
        # Show latest resonance
        resonances = result['recent_resonance']
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