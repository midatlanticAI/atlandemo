#!/usr/bin/env python3
"""
IMPROVED WAVE COGNITION EXPERIMENTS
Fixing the issues from the first attempt - proper metrics and timing
"""

import random
import json
import statistics
import math
import time
from src.temporal_cognition import TemporalCognitionEngine

def calculate_robust_surprise(baseline_field, test_field):
    """Calculate surprise as change in activation patterns"""
    all_symbols = set(baseline_field.keys()) | set(test_field.keys())
    
    if not all_symbols:
        return 0.0
    
    total_change = 0.0
    for symbol in all_symbols:
        baseline_val = baseline_field.get(symbol, 0)
        test_val = test_field.get(symbol, 0)
        change = abs(test_val - baseline_val)
        total_change += change
    
    return total_change / len(all_symbols)

def calculate_field_entropy(activation_field):
    """Calculate entropy of activation field"""
    if not activation_field:
        return 0.0
    
    # Get absolute values of all activations
    activations = [abs(v) for v in activation_field.values() if abs(v) > 0.001]
    
    if not activations:
        return 0.0
    
    # Normalize to probabilities
    total = sum(activations)
    if total == 0:
        return 0.0
    
    probs = [a/total for a in activations]
    
    # Calculate Shannon entropy
    entropy = 0.0
    for p in probs:
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def calculate_semantic_overlap(words1, words2):
    """Calculate semantic overlap (0=no overlap, 1=identical)"""
    set1, set2 = set(words1), set(words2)
    
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0

def experiment_1_improved_novelty_detection():
    """Improved novelty detection with proper timing and metrics"""
    print('🔬 EXPERIMENT 1: IMPROVED NOVELTY DETECTION')
    print('='*60)
    print('Taking time to properly test novelty responses...')
    print()
    
    # Better test conditions with overlapping baselines
    conditions = [
        # Low novelty (high overlap)
        {
            'name': 'low_novelty',
            'baseline': ['animal', 'pet', 'home'],
            'test': ['cat', 'dog', 'house'],
            'expected_overlap': 0.5  # some overlap
        },
        # Medium novelty 
        {
            'name': 'medium_novelty',  
            'baseline': ['music', 'sound', 'art'],
            'test': ['volcano', 'explosion', 'noise'],
            'expected_overlap': 0.17  # minimal overlap
        },
        # High novelty (minimal overlap)
        {
            'name': 'high_novelty',
            'baseline': ['normal', 'regular', 'typical'],
            'test': ['quantum', 'consciousness', 'infinity'],
            'expected_overlap': 0.0  # no overlap
        }
    ]
    
    results = []
    
    for condition in conditions:
        print(f"🧪 Testing {condition['name']}...")
        print(f"   Baseline: {condition['baseline']}")
        print(f"   Test: {condition['test']}")
        
        # Run multiple trials for statistical power
        for trial in range(3):
            print(f"   Trial {trial+1}... ", end='', flush=True)
            
            # Create fresh engine each time
            engine = TemporalCognitionEngine()
            
            # Baseline measurement (let it settle)
            time.sleep(0.1)  # Give time for processing
            baseline_result = engine.live_experience(
                visual=condition['baseline'],
                auditory=['baseline'],
                mood=0.5, arousal=0.5, attention=0.7,
                goals=['understand'],
                satisfaction=0.7
            )
            
            baseline_entropy = calculate_field_entropy(baseline_result['activation_field'])
            
            # Test stimulus (with slight delay)
            time.sleep(0.1)
            test_result = engine.live_experience(
                visual=condition['test'],
                auditory=['test'],
                mood=0.5, arousal=0.6, attention=0.8,
                goals=['process'],
                satisfaction=0.6
            )
            
            test_entropy = calculate_field_entropy(test_result['activation_field'])
            
            # Calculate metrics
            surprise = calculate_robust_surprise(
                baseline_result['activation_field'],
                test_result['activation_field']
            )
            
            entropy_change = test_entropy - baseline_entropy
            overlap = calculate_semantic_overlap(condition['baseline'], condition['test'])
            
            # Get system states
            baseline_state = engine.get_cognitive_state()
            test_state = engine.get_cognitive_state()
            
            results.append({
                'condition': condition['name'],
                'trial': trial + 1,
                'baseline_entropy': baseline_entropy,
                'test_entropy': test_entropy,
                'entropy_change': entropy_change,
                'robust_surprise': surprise,
                'semantic_overlap': overlap,
                'baseline_symbols': baseline_state.get('active_symbol_count', 0),
                'test_symbols': test_state.get('active_symbol_count', 0),
                'resonance_patterns': test_state.get('resonance_patterns', 0)
            })
            
            print(f"surprise={surprise:.3f}, entropy_Δ={entropy_change:.3f}")
    
    # Analyze results
    print('\n[DATA] NOVELTY DETECTION ANALYSIS:')
    print('='*40)
    
    by_condition = {}
    for result in results:
        condition = result['condition']
        if condition not in by_condition:
            by_condition[condition] = []
        by_condition[condition].append(result)
    
    for condition, trials in by_condition.items():
        surprises = [t['robust_surprise'] for t in trials]
        entropy_changes = [t['entropy_change'] for t in trials]
        overlaps = [t['semantic_overlap'] for t in trials]
        
        print(f"\n{condition}:")
        print(f"  Robust Surprise: μ={statistics.mean(surprises):.3f} ± {statistics.stdev(surprises) if len(surprises) > 1 else 0:.3f}")
        print(f"  Entropy Change: μ={statistics.mean(entropy_changes):.3f} ± {statistics.stdev(entropy_changes) if len(entropy_changes) > 1 else 0:.3f}")
        print(f"  Semantic Overlap: μ={statistics.mean(overlaps):.3f}")
    
    return results

def experiment_2_proper_habituation():
    """Proper habituation test with longer sequences"""
    print('\n🔬 EXPERIMENT 2: PROPER HABITUATION TEST')
    print('='*60)
    print('Testing adaptation over extended sequence...')
    print()
    
    # Use single engine instance to preserve memory
    engine = TemporalCognitionEngine()
    
    # Repeated stimulus
    repeated_stimulus = ['storm', 'lightning', 'thunder']
    
    habituation_data = []
    print("[CHART] Habituation sequence (15 trials):")
    
    for trial in range(15):
        print(f"  Trial {trial+1:2d}... ", end='', flush=True)
        
        # Add some variability to prevent exact repetition
        arousal = 0.7 + random.uniform(-0.1, 0.1)
        attention = 0.8 + random.uniform(-0.1, 0.1)
        
        time.sleep(0.05)  # Small delay between trials
        
        result = engine.live_experience(
            visual=repeated_stimulus,
            auditory=['repeat', f'trial_{trial+1}'],
            mood=0.4, arousal=arousal, attention=attention,
            goals=['process'],
            satisfaction=0.6
        )
        
        state = engine.get_cognitive_state()
        entropy = calculate_field_entropy(result['activation_field'])
        
        habituation_data.append({
            'trial': trial + 1,
            'entropy': entropy,
            'active_symbols': state.get('active_symbol_count', 0),
            'resonance_patterns': state.get('resonance_patterns', 0),
            'arousal': arousal,
            'attention': attention
        })
        
        print(f"entropy={entropy:.3f}, symbols={state.get('active_symbol_count', 0)}")
    
    # Novel stimulus
    print("\n🆕 Novel stimulus:")
    novel_stimulus = ['earthquake', 'volcano', 'eruption']
    
    time.sleep(0.1)
    novel_result = engine.live_experience(
        visual=novel_stimulus,
        auditory=['novel', 'different'],
        mood=0.4, arousal=0.8, attention=0.9,
        goals=['process'],
        satisfaction=0.5
    )
    
    novel_state = engine.get_cognitive_state()
    novel_entropy = calculate_field_entropy(novel_result['activation_field'])
    
    print(f"  Novel: entropy={novel_entropy:.3f}, symbols={novel_state.get('active_symbol_count', 0)}")
    
    # Analyze habituation pattern
    print('\n[DATA] HABITUATION ANALYSIS:')
    print('='*35)
    
    entropies = [d['entropy'] for d in habituation_data]
    
    # Check for trend
    early_trials = entropies[:5]
    late_trials = entropies[-5:]
    
    early_mean = statistics.mean(early_trials)
    late_mean = statistics.mean(late_trials)
    
    habituation_effect = early_mean - late_mean
    
    print(f"Early trials (1-5): μ={early_mean:.3f}")
    print(f"Late trials (11-15): μ={late_mean:.3f}")
    print(f"Habituation effect: {habituation_effect:.3f}")
    
    # Check novel stimulus response
    novel_boost = novel_entropy - late_mean
    print(f"Novel stimulus boost: {novel_boost:.3f}")
    
    if habituation_effect > 0.1:
        if novel_boost > 0.2:
            print("[+] CLEAR HABITUATION + NOVELTY RESPONSE")
        else:
            print("🤔 HABITUATION WITHOUT NOVELTY RESPONSE")
    else:
        print("[-] NO CLEAR HABITUATION DETECTED")
    
    return habituation_data, novel_result

def experiment_3_decision_timing():
    """Test if timing affects decision making"""
    print('\n🔬 EXPERIMENT 3: DECISION TIMING EFFECTS')
    print('='*60)
    print('Testing decision making with proper timing...')
    print()
    
    decision_results = []
    
    conditions = ['fast_decision', 'slow_decision']
    
    for condition in conditions:
        print(f"[TARGET] Testing {condition}...")
        
        for trial in range(5):  # Multiple trials
            print(f"   Trial {trial+1}... ", end='', flush=True)
            
            engine = TemporalCognitionEngine()
            
            # Setup context
            time.sleep(0.1)
            context_result = engine.live_experience(
                visual=['situation', 'choice', 'decide'],
                auditory=['thinking'],
                mood=0.5, arousal=0.6, attention=0.7,
                goals=['evaluate'],
                satisfaction=0.6
            )
            
            # Decision timing
            if condition == 'fast_decision':
                time.sleep(0.01)  # Quick decision
            else:
                time.sleep(0.2)   # Deliberate decision
            
            # Present choice
            choice_result = engine.live_experience(
                visual=['choose', 'option', 'select'],
                auditory=['explore', 'exploit'],  # Present both options
                mood=0.5, arousal=0.6, attention=0.9,
                goals=['choose'],
                satisfaction=0.5
            )
            
            # Measure choice
            field = choice_result['activation_field']
            explore_activation = field.get('explore', 0)
            exploit_activation = field.get('exploit', 0)
            
            choice_strength = abs(explore_activation - exploit_activation)
            preference = explore_activation - exploit_activation
            
            state = engine.get_cognitive_state()
            
            decision_results.append({
                'condition': condition,
                'trial': trial + 1,
                'explore_activation': explore_activation,
                'exploit_activation': exploit_activation,
                'choice_strength': choice_strength,
                'preference': preference,
                'active_symbols': state.get('active_symbol_count', 0)
            })
            
            print(f"explore={explore_activation:.3f}, exploit={exploit_activation:.3f}, pref={preference:.3f}")
    
    # Analyze decisions
    print('\n[DATA] DECISION ANALYSIS:')
    print('='*25)
    
    fast_decisions = [r for r in decision_results if r['condition'] == 'fast_decision']
    slow_decisions = [r for r in decision_results if r['condition'] == 'slow_decision']
    
    fast_prefs = [d['preference'] for d in fast_decisions]
    slow_prefs = [d['preference'] for d in slow_decisions]
    
    fast_strengths = [d['choice_strength'] for d in fast_decisions]
    slow_strengths = [d['choice_strength'] for d in slow_decisions]
    
    print(f"Fast decisions: μ={statistics.mean(fast_prefs):.3f} ± {statistics.stdev(fast_prefs) if len(fast_prefs) > 1 else 0:.3f}")
    print(f"Slow decisions: μ={statistics.mean(slow_prefs):.3f} ± {statistics.stdev(slow_prefs) if len(slow_prefs) > 1 else 0:.3f}")
    print(f"Fast strength: μ={statistics.mean(fast_strengths):.3f}")
    print(f"Slow strength: μ={statistics.mean(slow_strengths):.3f}")
    
    timing_effect = statistics.mean(slow_prefs) - statistics.mean(fast_prefs)
    print(f"Timing effect: {timing_effect:.3f}")
    
    if abs(timing_effect) > 0.1:
        print("[+] TIMING AFFECTS DECISION MAKING")
    else:
        print("[-] NO CLEAR TIMING EFFECT")
    
    return decision_results

def run_improved_experiments():
    """Run all improved experiments with proper timing"""
    print('[WAVE] IMPROVED WAVE COGNITION EXPERIMENTS')
    print('='*70)
    print('Taking time to do this right...')
    print()
    
    start_time = time.time()
    
    # Run experiments with proper timing
    novelty_results = experiment_1_improved_novelty_detection()
    habituation_data, novel_result = experiment_2_proper_habituation()
    decision_results = experiment_3_decision_timing()
    
    end_time = time.time()
    
    print(f'\n⏱️ Total runtime: {end_time - start_time:.2f} seconds')
    print('[TARGET] EXPERIMENTS COMPLETED WITH PROPER TIMING')
    
    return {
        'novelty_results': novelty_results,
        'habituation_data': habituation_data,
        'novel_result': novel_result,
        'decision_results': decision_results,
        'runtime_seconds': end_time - start_time
    }

if __name__ == "__main__":
    print("[BOLT] Running IMPROVED experiments...")
    print("🐌 Taking time to do proper measurements...")
    print()
    
    results = run_improved_experiments()
    
    # Save results
    with open('improved_experimental_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n[SAVE] Results saved to 'improved_experimental_results.json'")
    print("🔬 Proper scientific methodology with timing!") 