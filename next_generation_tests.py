#!/usr/bin/env python3
"""
NEXT-GENERATION WAVE COGNITION EXPERIMENTS
Following ChatGPT's scientific guidance to understand what actually drives internal dynamics
"""

import random
import json
import statistics
import math
from src.temporal_cognition import TemporalCognitionEngine
import time

def calculate_entropy(activation_field):
    """Calculate Shannon entropy of activation field"""
    activations = [abs(v) for v in activation_field.values() if v != 0]
    if not activations:
        return 0
    
    total = sum(activations)
    if total == 0:
        return 0
    
    probs = [a/total for a in activations]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    return entropy

def calculate_semantic_distance(prompt1, prompt2):
    """Simple semantic distance based on word overlap (placeholder for better metric)"""
    words1 = set(prompt1)
    words2 = set(prompt2)
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return 1 - (intersection / union if union > 0 else 0)

def experiment_1_novelty_receptors(n_trials=20):
    """
    Experiment 1: What drives internal surprise?
    Vary semantic distance, emotional valence, sensory channels
    """
    print('🧪 EXPERIMENT 1: IDENTIFYING NOVELTY RECEPTORS')
    print('='*60)
    print('Testing what actually drives internal surprise scores...')
    print()
    
    # Test conditions with varying properties
    test_conditions = [
        # Semantic distance variations
        (['cat', 'dog', 'pet'], 'low_semantic_distance', 'neutral'),
        (['volcano', 'mathematics', 'purple'], 'high_semantic_distance', 'neutral'),
        
        # Emotional valence variations  
        (['love', 'joy', 'peace'], 'medium_semantic_distance', 'positive'),
        (['hate', 'fear', 'death'], 'medium_semantic_distance', 'negative'),
        
        # Abstract vs concrete
        (['chair', 'table', 'book'], 'concrete', 'neutral'),
        (['truth', 'justice', 'beauty'], 'abstract', 'neutral'),
    ]
    
    results = []
    baseline_prompt = ['normal', 'expected', 'continue']
    
    for prompt_words, condition_type, valence in test_conditions:
        print(f'Testing {condition_type} ({valence}): {prompt_words}')
        
        for trial in range(3):  # Multiple trials per condition
            engine = TemporalCognitionEngine()
            
            # Baseline
            baseline_result = engine.live_experience(
                visual=baseline_prompt,
                auditory=['baseline'],
                mood=0.5, arousal=0.5, attention=0.5,
                goals=['understand'],
                satisfaction=0.7
            )
            
            baseline_state = engine.get_cognitive_state()
            baseline_entropy = calculate_entropy(baseline_result['activation_field'])
            
            # Test condition
            test_result = engine.live_experience(
                visual=prompt_words,
                auditory=['test'],
                mood=0.0 if valence == 'negative' else 0.5 if valence == 'neutral' else 1.0,
                arousal=0.7, attention=0.8,
                goals=['process'],
                satisfaction=0.5
            )
            
            test_state = engine.get_cognitive_state()
            test_entropy = calculate_entropy(test_result['activation_field'])
            
            # Calculate metrics
            semantic_distance = calculate_semantic_distance(baseline_prompt, prompt_words)
            symbol_change = abs(test_state.get('active_symbol_count', 0) - baseline_state.get('active_symbol_count', 0))
            entropy_change = test_entropy - baseline_entropy
            
            # Internal surprise calculation
            internal_surprise = 0
            for symbol in test_result['activation_field']:
                if symbol in baseline_result['activation_field']:
                    surprise_delta = abs(test_result['activation_field'][symbol] - baseline_result['activation_field'][symbol])
                    internal_surprise += surprise_delta
            
            normalized_surprise = internal_surprise / max(symbol_change, 1)
            
            results.append({
                'condition_type': condition_type,
                'valence': valence,
                'prompt_words': prompt_words,
                'semantic_distance': semantic_distance,
                'symbol_change': symbol_change,
                'entropy_change': entropy_change,
                'internal_surprise': internal_surprise,
                'normalized_surprise': normalized_surprise
            })
    
    # Analyze correlations
    print('\n📊 NOVELTY RECEPTOR ANALYSIS:')
    print('='*40)
    
    # Group by condition
    by_condition = {}
    for result in results:
        condition = result['condition_type']
        if condition not in by_condition:
            by_condition[condition] = []
        by_condition[condition].append(result)
    
    for condition, group in by_condition.items():
        norm_surprises = [r['normalized_surprise'] for r in group]
        semantic_distances = [r['semantic_distance'] for r in group]
        entropy_changes = [r['entropy_change'] for r in group]
        
        print(f"\n{condition}:")
        print(f"  Normalized Surprise: μ={statistics.mean(norm_surprises):.3f}")
        print(f"  Semantic Distance: μ={statistics.mean(semantic_distances):.3f}")
        print(f"  Entropy Change: μ={statistics.mean(entropy_changes):.3f}")
    
    return results

def experiment_2_habituation_test(n_repetitions=10):
    """
    Experiment 2: Clean habituation test
    Repeat same prompt, then switch to new prompt
    """
    print('\n🧪 EXPERIMENT 2: HABITUATION & ADAPTATION')
    print('='*60)
    print('Testing adaptation to repeated stimuli...')
    print()
    
    engine = TemporalCognitionEngine()  # Single engine instance
    
    # Phase 1: Repeat same chaos prompt
    chaos_prompt = ['volcano', 'dreams', 'mathematics']
    habituation_results = []
    
    print('Phase 1: Repeating same prompt to test habituation...')
    for i in range(n_repetitions):
        result = engine.live_experience(
            visual=chaos_prompt,
            auditory=['repetition', f'trial_{i+1}'],
            mood=0.3, arousal=0.7, attention=0.8,
            goals=['process'],
            surprise=0.8,
            satisfaction=0.5
        )
        
        state = engine.get_cognitive_state()
        entropy = calculate_entropy(result['activation_field'])
        
        # Calculate surprise vs baseline (first trial)
        if i == 0:
            baseline_field = result['activation_field']
            baseline_entropy = entropy
            surprise_vs_baseline = 0
        else:
            surprise_vs_baseline = sum(abs(result['activation_field'].get(s, 0) - baseline_field.get(s, 0)) 
                                     for s in set(result['activation_field']) | set(baseline_field))
        
        habituation_results.append({
            'trial': i + 1,
            'entropy': entropy,
            'entropy_vs_baseline': entropy - baseline_entropy,
            'surprise_vs_baseline': surprise_vs_baseline,
            'active_symbols': state.get('active_symbol_count', 0)
        })
        
        print(f'  Trial {i+1}: entropy={entropy:.3f}, symbols={state.get("active_symbol_count", 0)}')
    
    # Phase 2: Switch to novel prompt
    print('\nPhase 2: Switching to novel prompt...')
    novel_prompt = ['earthquake', 'poetry', 'quantum']
    
    novel_result = engine.live_experience(
        visual=novel_prompt,
        auditory=['novel', 'switch'],
        mood=0.3, arousal=0.7, attention=0.8,
        goals=['process'],
        surprise=0.8,
        satisfaction=0.5
    )
    
    novel_state = engine.get_cognitive_state()
    novel_entropy = calculate_entropy(novel_result['activation_field'])
    novel_surprise_vs_baseline = sum(abs(novel_result['activation_field'].get(s, 0) - baseline_field.get(s, 0)) 
                                   for s in set(novel_result['activation_field']) | set(baseline_field))
    
    print(f'  Novel: entropy={novel_entropy:.3f}, symbols={novel_state.get("active_symbol_count", 0)}')
    
    # Analyze habituation pattern
    print('\n📊 HABITUATION ANALYSIS:')
    print('='*30)
    
    entropies = [r['entropy'] for r in habituation_results]
    surprises = [r['surprise_vs_baseline'] for r in habituation_results]
    
    # Check for declining trend (habituation)
    first_half = entropies[:len(entropies)//2]
    second_half = entropies[len(entropies)//2:]
    
    decline = statistics.mean(first_half) - statistics.mean(second_half)
    print(f'Entropy decline (habituation): {decline:.3f}')
    
    # Check for rebound with novel stimulus
    final_entropy = entropies[-1]
    rebound = novel_entropy - final_entropy
    print(f'Entropy rebound (novel stimulus): {rebound:.3f}')
    
    if decline > 0.1 and rebound > 0.1:
        print('✅ HABITUATION DETECTED: System adapts to repeated stimuli and rebounds with novelty')
    elif decline > 0.1:
        print('🤔 PARTIAL HABITUATION: System adapts but no clear rebound')
    else:
        print('❌ NO HABITUATION: System does not adapt to repeated stimuli')
    
    return habituation_results, novel_result

def experiment_3_decision_making_test():
    """
    Experiment 3: Does surprise affect decision-making?
    After high surprise, does system favor exploration?
    """
    print('\n🧪 EXPERIMENT 3: SURPRISE → DECISION MAKING')
    print('='*60)
    print('Testing if surprise affects goal selection...')
    print()
    
    results = []
    
    for condition in ['low_surprise', 'high_surprise']:
        print(f'Testing {condition} condition...')
        
        engine = TemporalCognitionEngine()
        
        # Induce surprise condition
        if condition == 'low_surprise':
            surprise_result = engine.live_experience(
                visual=['normal', 'expected', 'calm'],
                auditory=['routine'],
                mood=0.5, arousal=0.5, attention=0.6,
                goals=['routine'],
                surprise=0.1,
                satisfaction=0.8
            )
        else:
            surprise_result = engine.live_experience(
                visual=['volcano', 'dreams', 'mathematics'],
                auditory=['chaos'],
                mood=0.2, arousal=0.9, attention=0.9,
                goals=['chaos'],
                surprise=0.95,
                satisfaction=0.2
            )
        
        # Present choice: explore vs exploit
        choice_result = engine.live_experience(
            visual=['choice', 'decide', 'select'],
            auditory=['explore', 'exploit'],  # Two options
            mood=0.5, arousal=0.6, attention=0.9,
            goals=['choose', 'decide'],
            satisfaction=0.5
        )
        
        # Measure choice preference
        field = choice_result['activation_field']
        explore_activation = field.get('explore', 0)
        exploit_activation = field.get('exploit', 0)
        
        choice_preference = explore_activation - exploit_activation
        
        results.append({
            'condition': condition,
            'explore_activation': explore_activation,
            'exploit_activation': exploit_activation,
            'choice_preference': choice_preference  # Positive = explore bias
        })
        
        print(f'  Explore: {explore_activation:.3f}, Exploit: {exploit_activation:.3f}')
        print(f'  Preference: {choice_preference:.3f} (+ = explore bias)')
    
    # Compare conditions
    print('\n📊 DECISION ANALYSIS:')
    print('='*25)
    
    low_surprise_pref = [r['choice_preference'] for r in results if r['condition'] == 'low_surprise'][0]
    high_surprise_pref = [r['choice_preference'] for r in results if r['condition'] == 'high_surprise'][0]
    
    surprise_effect = high_surprise_pref - low_surprise_pref
    
    print(f'Low surprise preference: {low_surprise_pref:.3f}')
    print(f'High surprise preference: {high_surprise_pref:.3f}')
    print(f'Surprise effect on exploration: {surprise_effect:.3f}')
    
    if surprise_effect > 0.2:
        print('✅ EXPLORATION BIAS: High surprise increases exploration tendency')
    elif surprise_effect < -0.2:
        print('🔄 EXPLOITATION BIAS: High surprise increases exploitation tendency')
    else:
        print('🤷 NO CLEAR BIAS: Surprise does not affect exploration/exploitation')
    
    return results

def run_next_generation_experiments():
    """Run all next-generation experiments"""
    print('🌊 NEXT-GENERATION WAVE COGNITION EXPERIMENTS')
    print('='*70)
    print('Following ChatGPT\'s scientific guidance...')
    print()
    
    # Run experiments
    novelty_results = experiment_1_novelty_receptors()
    habituation_results, novel_result = experiment_2_habituation_test()
    decision_results = experiment_3_decision_making_test()
    
    # Summary
    print('\n🎯 EXPERIMENT SUMMARY:')
    print('='*30)
    print('✅ Novelty Receptors: Tested semantic distance, valence, abstraction')
    print('✅ Habituation: Tested adaptation to repeated stimuli')
    print('✅ Decision Making: Tested surprise → exploration link')
    
    return {
        'novelty_results': novelty_results,
        'habituation_results': habituation_results,
        'novel_result': novel_result,
        'decision_results': decision_results
    }

if __name__ == "__main__":
    print("🔬 Running next-generation experiments based on ChatGPT's guidance...")
    print("Focus: Understanding what actually drives wave engine dynamics")
    print()
    
    results = run_next_generation_experiments()
    
    # Save results
    with open('next_generation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to 'next_generation_results.json'")
    print("🌊 Building on solid scientific foundations!")
    print("🎯 Focus: What we can prove, not what we hoped to prove") 