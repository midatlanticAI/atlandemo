#!/usr/bin/env python3

import json

def analyze_results():
    with open('self_surprise_results.json', 'r') as f:
        results = json.load(f)
    
    print('🔍 DETAILED ANALYSIS OF PREDICTION ACCURACY ISSUE:')
    print('='*50)
    
    # Check what symbols were actually predicted vs actual
    print('CHAOS TESTS:')
    for i, result in enumerate(results['chaos_results']):
        print(f'Chaos Test {i+1}:')
        print(f'  Predicted: {result["prediction_symbols"]}')
        print(f'  Actual: {result["actual_symbols"]}')
        print(f'  Accuracy: {result["prediction_accuracy"]:.3f}')
        print()
    
    print('CONTROL TESTS:')
    for i, result in enumerate(results['control_results']):
        print(f'Control Test {i+1}:')
        print(f'  Predicted: {result["prediction_symbols"]}')
        print(f'  Actual: {result["actual_symbols"]}')
        print(f'  Accuracy: {result["prediction_accuracy"]:.3f}')
        print()
    
    # Summary
    print('🎯 SUMMARY:')
    print(f'Effect Size: {results["effect_size"]:.3f}')
    print(f'Consistency Rate: {results["consistency_rate"]:.1%}')
    print(f'Evidence Strength: {results["evidence_count"]}/3')

if __name__ == "__main__":
    analyze_results() 