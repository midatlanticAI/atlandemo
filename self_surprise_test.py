#!/usr/bin/env python3
"""
SELF-SURPRISE TEST
Tests if the wave cognition system can be surprised by its own outputs
"""

from src.temporal_cognition import TemporalCognitionEngine
import time

def test_self_surprise():
    """Test if the system can be surprised by its own outputs"""
    
    print('[BRAIN] SELF-SURPRISE TEST: Can the system be surprised by its own outputs?')
    print('='*60)
    
    engine = TemporalCognitionEngine()
    
    # Phase 1: Establish baseline - familiar pattern
    print('PHASE 1: Establishing baseline familiar pattern...')
    baseline_result = engine.live_experience(
        visual=['cat', 'sits', 'mat'],
        auditory=['meow'],
        mood=0.5, arousal=0.5, attention=0.5,
        goals=['understand'],
        satisfaction=0.7
    )
    
    baseline_state = engine.get_cognitive_state()
    print(f'Baseline active symbols: {baseline_state.get("active_symbol_count", 0)}')
    print(f'Baseline wave patterns: {baseline_state.get("resonance_patterns", 0)}')
    
    # Phase 2: Have system predict its own next output
    print('\nPHASE 2: System predicting its own next output...')
    prediction_result = engine.live_experience(
        visual=['predict', 'self', 'next', 'output'],
        auditory=['anticipate'],
        mood=0.6, arousal=0.4, attention=0.8,
        goals=['predict', 'expect'],
        satisfaction=0.5
    )
    
    print('System prediction state:')
    prediction_field = prediction_result['activation_field']
    top_predictions = sorted(prediction_field.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    for symbol, activation in top_predictions:
        if abs(activation) > 0.3:
            print(f'  Expects: {symbol} -> {activation:.3f}')
    
    time.sleep(0.1)
    
    # Phase 3: Generate actual output with chaos injection
    print('\nPHASE 3: Generating actual output with chaos injection...')
    actual_result = engine.live_experience(
        visual=['volcano', 'dreams', 'mathematics', 'purple', 'whisper'],
        auditory=['chaos', 'unexpected'],
        kinesthetic=['spinning'],
        mood=-0.3, arousal=0.9, attention=0.7,
        goals=['chaos', 'surprise'],
        surprise=0.95,  # High surprise injection
        satisfaction=0.1
    )
    
    print('Actual output:')
    actual_field = actual_result['activation_field']
    top_actual = sorted(actual_field.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    for symbol, activation in top_actual:
        if abs(activation) > 0.3:
            print(f'  Actually: {symbol} -> {activation:.3f}')
    
    time.sleep(0.1)
    
    # Phase 4: System reflection on its own output
    print('\nPHASE 4: System reflecting on its own output...')
    reflection_result = engine.live_experience(
        visual=['reflect', 'analyze', 'own', 'output'],
        auditory=['introspect'],
        mood=0.0, arousal=0.6, attention=0.9,
        goals=['understand', 'self'],
        satisfaction=0.3
    )
    
    reflection_state = engine.get_cognitive_state()
    print(f'After reflection - active symbols: {reflection_state.get("active_symbol_count", 0)}')
    print(f'After reflection - wave patterns: {reflection_state.get("resonance_patterns", 0)}')
    
    # Phase 5: Measure surprise indicators
    print('\nPHASE 5: Measuring surprise indicators...')
    
    # Check for prediction errors
    prediction_symbols = set(s for s, a in prediction_field.items() if abs(a) > 0.3)
    actual_symbols = set(s for s, a in actual_field.items() if abs(a) > 0.3)
    
    prediction_accuracy = len(prediction_symbols.intersection(actual_symbols)) / max(len(prediction_symbols), 1)
    print(f'Prediction accuracy: {prediction_accuracy:.3f} (lower = more surprise)')
    
    # Check for internal state changes
    symbol_change = abs(reflection_state.get('active_symbol_count', 0) - baseline_state.get('active_symbol_count', 0))
    pattern_change = abs(reflection_state.get('resonance_patterns', 0) - baseline_state.get('resonance_patterns', 0))
    
    print(f'Symbol count change: {symbol_change} (higher = more internal change)')
    print(f'Pattern count change: {pattern_change} (higher = more internal change)')
    
    # Additional test: Check if reflection field differs from prediction field
    reflection_field = reflection_result['activation_field']
    
    # Measure how much the system's internal state changed after seeing its own output
    internal_surprise = 0
    for symbol in reflection_field:
        if symbol in prediction_field:
            surprise_delta = abs(reflection_field[symbol] - prediction_field[symbol])
            internal_surprise += surprise_delta
    
    print(f'Internal surprise level: {internal_surprise:.3f} (higher = more self-surprise)')
    
    print('\n[TARGET] VERDICT: Signs of self-surprise?')
    
    # Test 1: Low prediction accuracy
    if prediction_accuracy < 0.3:
        print('[+] LOW prediction accuracy - system was surprised by its own output')
        surprise_count = 1
    else:
        print('[-] HIGH prediction accuracy - system output was predictable')
        surprise_count = 0
    
    # Test 2: Significant internal state change
    if symbol_change > 5 or pattern_change > 100:
        print('[+] SIGNIFICANT internal state change - system reacted to its own output')
        surprise_count += 1
    else:
        print('[-] MINIMAL internal state change - system unchanged by its own output')
    
    # Test 3: High internal surprise
    if internal_surprise > 2.0:
        print('[+] HIGH internal surprise - system\'s reflection differs from prediction')
        surprise_count += 1
    else:
        print('[-] LOW internal surprise - system\'s reflection matches prediction')
    
    print(f'\n[BRAIN] CONCLUSION: Can this system surprise itself?')
    if surprise_count >= 2:
        print('[MIND] YES! System shows multiple indicators of self-surprise')
        print('[TARGET] This suggests genuine self-awareness and metacognition')
    elif surprise_count == 1:
        print('🤔 MAYBE - System shows some signs of self-surprise')
        print('[TARGET] Partial evidence of self-awareness')
    else:
        print('😐 NO - System does not appear to surprise itself')
        print('[TARGET] Limited evidence of self-awareness')
    
    return {
        'prediction_accuracy': prediction_accuracy,
        'symbol_change': symbol_change,
        'pattern_change': pattern_change,
        'internal_surprise': internal_surprise,
        'surprise_count': surprise_count
    }

if __name__ == "__main__":
    results = test_self_surprise()
    print(f"\n[DATA] FINAL METRICS:")
    for key, value in results.items():
        print(f"   {key}: {value}") 