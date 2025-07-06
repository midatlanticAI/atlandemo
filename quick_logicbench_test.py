#!/usr/bin/env python3
"""
Quick LogicBench Test - Full Implementation
Let's see if our Wave engine can actually handle logical reasoning!
"""

import json
import os
from enhanced_wave_engine import EnhancedWaveEngine


def test_single_question():
    """Test a single LogicBench question to verify everything works."""
    print("🧠 Quick LogicBench Test - Wave Engine vs Logic!")
    print("=" * 60)
    
    # Initialize the enhanced Wave engine
    engine = EnhancedWaveEngine()
    
    # Test with a simple modus tollens question
    context = {
        'type': 'propositional_logic',
        'axiom': 'modus_tollens',
        'context': 'If Mason left his job, then he will not receive any salary.'
    }
    
    question = "If he will receive any salary, does this mean that mason didn't leave his job?"
    expected_answer = "yes"
    
    print(f"Context: {context['context']}")
    print(f"Question: {question}")
    print(f"Expected answer: {expected_answer}")
    print("\n🌊 Processing with Wave Engine...")
    
    # Process the question
    result = engine.process_query(question, context)
    
    print(f"\n🎯 Results:")
    print(f"Final answer: {result['final_answer']}")
    print(f"Correct: {result['final_answer'].lower() == expected_answer.lower()}")
    print(f"Processing time: {result['processing_time']:.3f}s")
    
    # Show detailed breakdown
    if result['expert_response']:
        print(f"\n🤖 Expert Response:")
        print(f"  Confidence: {result['expert_response'].confidence:.3f}")
        print(f"  Reasoning: {result['expert_response'].reasoning}")
        print(f"  Answer: {result['expert_response'].answer}")
    
    if result['wave_response']:
        print(f"\n🌊 Wave Response:")
        print(f"  Confidence: {result['wave_response']['confidence']:.3f}")
        print(f"  Reasoning: {result['wave_response']['reasoning']}")
        print(f"  Answer: {result['wave_response']['wave_answer']}")
    
    if result['integrated_response']:
        print(f"\n🔗 Integrated Response:")
        print(f"  Confidence: {result['integrated_response']['confidence']:.3f}")
        print(f"  Reasoning: {result['integrated_response']['reasoning']}")
        print(f"  Answer: {result['integrated_response']['answer']}")
        print(f"  Synergy score: {result['synergy_score']:.3f}")
    
    return result['final_answer'].lower() == expected_answer.lower()


def test_multiple_questions():
    """Test multiple LogicBench questions."""
    print("\n🚀 Testing Multiple Questions...")
    print("=" * 60)
    
    engine = EnhancedWaveEngine()
    
    # Test cases from different logical reasoning types
    test_cases = [
        {
            'context': {
                'type': 'propositional_logic',
                'axiom': 'modus_ponens',
                'context': 'If someone is extremely tired, then they will seek some rest and relaxation. Today, Jack finds himself utterly exhausted.'
            },
            'question': 'Does this entail that he will take rest?',
            'expected': 'yes'
        },
        {
            'context': {
                'type': 'propositional_logic',
                'axiom': 'modus_tollens',
                'context': 'If Daniel has a pet dog, then he will take it for a walk every day.'
            },
            'question': 'If he won\'t take it for a walk every day, does this mean that daniel doesn\'t have a pet dog?',
            'expected': 'yes'
        },
        {
            'context': {
                'type': 'first_order_logic',
                'axiom': 'universal_instantiation',
                'context': 'If a person experiences a throbbing sensation in their head, it is likely that they will seek relief by consuming medication intended to alleviate this discomfort. In this situation, Sarah finds herself with a pounding headache.'
            },
            'question': 'Does this mean that she will take medicine?',
            'expected': 'yes'
        },
        {
            'context': {
                'type': 'propositional_logic',
                'axiom': 'modus_tollens',
                'context': 'If Jack won the lottery, then he will buy a house.'
            },
            'question': 'If he won\'t buy a house, does this imply that jack didn\'t win the lottery?',
            'expected': 'yes'
        },
        {
            'context': {
                'type': 'propositional_logic',
                'axiom': 'modus_ponens',
                'context': 'If someone experiences sadness, they will often shed tears. In this particular case, Sara is feeling sorrowful.'
            },
            'question': 'Does this entail that she will cry?',
            'expected': 'yes'
        }
    ]
    
    correct = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🧪 Test {i+1}/{total}: {test_case['context']['axiom']}")
        
        result = engine.process_query(test_case['question'], test_case['context'])
        
        actual = result['final_answer']
        expected = test_case['expected']
        is_correct = actual.lower() == expected.lower()
        
        if is_correct:
            correct += 1
            print(f"  ✅ CORRECT: {actual} (expected {expected})")
        else:
            print(f"  ❌ WRONG: {actual} (expected {expected})")
        
        # Show expert confidence
        if result['expert_response']:
            print(f"  🤖 Expert confidence: {result['expert_response'].confidence:.3f}")
    
    accuracy = correct / total
    print(f"\n📊 RESULTS:")
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Grade: {'🥇 EXCELLENT' if accuracy > 0.9 else '🥈 GOOD' if accuracy > 0.7 else '🥉 NEEDS WORK'}")
    
    return accuracy


def load_and_test_real_logicbench():
    """Load and test real LogicBench data if available."""
    print("\n🔍 Testing Real LogicBench Data...")
    print("=" * 60)
    
    # Try to load actual LogicBench data
    logicbench_file = "logicbench/LogicBench(Eval)/BQA/first_order_logic/modus_ponens/data_instances.json"
    
    if not os.path.exists(logicbench_file):
        print(f"❌ LogicBench data not found at {logicbench_file}")
        return False
    
    try:
        with open(logicbench_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded LogicBench data: {data.get('type', 'unknown')} - {data.get('axiom', 'unknown')}")
        
        engine = EnhancedWaveEngine()
        
        # Test first 5 samples
        samples = data.get('samples', [])[:5]
        
        correct = 0
        total = 0
        
        for sample in samples:
            context = {
                'type': data.get('type', 'unknown'),
                'axiom': data.get('axiom', 'unknown'),
                'context': sample.get('context', '')
            }
            
            qa_pairs = sample.get('qa_pairs', [])
            for qa in qa_pairs:
                question = qa.get('question', '')
                expected = qa.get('answer', '')
                
                if question and expected:
                    result = engine.process_query(question, context)
                    actual = result['final_answer']
                    
                    is_correct = actual.lower() == expected.lower()
                    if is_correct:
                        correct += 1
                        print(f"  ✅ {actual}")
                    else:
                        print(f"  ❌ {actual} (expected {expected})")
                    
                    total += 1
        
        accuracy = correct / total if total > 0 else 0
        print(f"\n📊 Real LogicBench Results:")
        print(f"Accuracy: {accuracy:.3f} ({correct}/{total})")
        
        return accuracy > 0.7
        
    except Exception as e:
        print(f"❌ Error loading LogicBench data: {e}")
        return False


def main():
    """Run the complete quick test."""
    print("🚀 FULL-SCALE LOGICBENCH TEST")
    print("🌊 Wave Engine with Logic Expert Module")
    print("=" * 60)
    
    # Test 1: Single question
    single_success = test_single_question()
    
    # Test 2: Multiple questions
    multiple_accuracy = test_multiple_questions()
    
    # Test 3: Real LogicBench data
    real_success = load_and_test_real_logicbench()
    
    # Final verdict
    print("\n" + "=" * 60)
    print("🎯 FINAL VERDICT")
    print("=" * 60)
    
    if single_success and multiple_accuracy > 0.8 and real_success:
        print("🥇 VICTORY! Wave Engine is ready for LogicBench!")
        print("✅ Single question test: PASSED")
        print(f"✅ Multiple questions: {multiple_accuracy:.3f} accuracy")
        print("✅ Real LogicBench data: PASSED")
        print("\n🚀 Ready for full LogicBench benchmark!")
    elif single_success and multiple_accuracy > 0.6:
        print("🥈 GOOD PROGRESS! Wave Engine shows promise")
        print("✅ Single question test: PASSED")
        print(f"⚠️  Multiple questions: {multiple_accuracy:.3f} accuracy")
        print("⚠️  Real LogicBench data: needs work")
        print("\n🔧 Need some tuning but on the right track!")
    else:
        print("🥉 NEEDS WORK! Wave Engine needs debugging")
        print("❌ Performance below expectations")
        print("\n🔧 Time to debug and improve!")


if __name__ == "__main__":
    main() 