"""
LogicBench Test Runner for Enhanced Wave Engine
Tests the Wave engine with expert modules against LogicBench questions.
"""

import json
import os
import time
from typing import Dict, List, Any, Tuple
from enhanced_wave_engine import EnhancedWaveEngine
from expert_modules.logic_expert import LogicExpertModule


class LogicBenchTestRunner:
    """
    Test runner for LogicBench evaluation using the Enhanced Wave Engine.
    
    Supports testing against different logic types:
    - Propositional Logic
    - First-order Logic  
    - Non-monotonic Logic
    """
    
    def __init__(self, logicbench_path: str = "logicbench"):
        self.logicbench_path = logicbench_path
        self.wave_engine = EnhancedWaveEngine()
        self.results = {}
        self.test_stats = {
            'total_tests': 0,
            'correct_answers': 0,
            'total_time': 0.0,
            'accuracy_by_type': {},
            'accuracy_by_axiom': {}
        }
    
    def load_test_data(self, test_type: str, format_type: str = "BQA") -> Dict[str, Any]:
        """
        Load test data from LogicBench.
        
        Args:
            test_type: Type of logic test (propositional_logic, first_order_logic, nm_logic)
            format_type: Format (BQA for Boolean QA, MCQA for Multiple Choice)
        """
        test_data = {}
        
        base_path = os.path.join(self.logicbench_path, f"LogicBench(Eval)", format_type, test_type)
        
        if not os.path.exists(base_path):
            print(f"[-] Test data not found: {base_path}")
            return test_data
        
        for axiom_dir in os.listdir(base_path):
            axiom_path = os.path.join(base_path, axiom_dir)
            if os.path.isdir(axiom_path):
                data_file = os.path.join(axiom_path, "data_instances.json")
                if os.path.exists(data_file):
                    try:
                        with open(data_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            test_data[axiom_dir] = data
                        print(f"[+] Loaded {axiom_dir} test data")
                    except Exception as e:
                        print(f"[-] Error loading {axiom_dir}: {e}")
        
        return test_data
    
    def run_single_test(self, question: str, expected_answer: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test question through the Wave engine."""
        start_time = time.time()
        
        # Process query with Wave engine
        result = self.wave_engine.process_query(question, context)
        
        processing_time = time.time() - start_time
        
        # Check if answer is correct
        actual_answer = result['final_answer']
        correct = actual_answer.lower() == expected_answer.lower()
        
        return {
            'question': question,
            'expected_answer': expected_answer,
            'actual_answer': actual_answer,
            'correct': correct,
            'processing_time': processing_time,
            'wave_response': result.get('wave_response'),
            'expert_response': result.get('expert_response'),
            'integrated_response': result.get('integrated_response'),
            'synergy_score': result.get('synergy_score', 0.0)
        }
    
    def run_axiom_tests(self, axiom_data: Dict[str, Any], axiom_name: str) -> Dict[str, Any]:
        """Run tests for a specific logical axiom."""
        print(f"\n[BRAIN] Testing {axiom_name}...")
        
        axiom_results = {
            'axiom': axiom_name,
            'total_questions': 0,
            'correct_answers': 0,
            'accuracy': 0.0,
            'avg_processing_time': 0.0,
            'avg_synergy_score': 0.0,
            'test_details': []
        }
        
        # Extract test samples
        samples = axiom_data.get('samples', axiom_data.get('data_samples', []))
        
        total_time = 0.0
        total_synergy = 0.0
        
        for sample in samples:
            # Get context information
            context = {
                'type': axiom_data.get('type', 'unknown'),
                'axiom': axiom_data.get('axiom', axiom_name),
                'context': sample.get('context', '')
            }
            
            # Test each QA pair
            qa_pairs = sample.get('qa_pairs', [])
            for qa in qa_pairs:
                question = qa.get('question', '')
                expected_answer = qa.get('answer', '')
                
                if question and expected_answer:
                    test_result = self.run_single_test(question, expected_answer, context)
                    
                    axiom_results['test_details'].append(test_result)
                    axiom_results['total_questions'] += 1
                    
                    if test_result['correct']:
                        axiom_results['correct_answers'] += 1
                    
                    total_time += test_result['processing_time']
                    total_synergy += test_result['synergy_score']
                    
                    # Provide feedback to Wave engine
                    self.wave_engine.provide_feedback(
                        question, expected_answer, test_result['actual_answer'], test_result['correct']
                    )
        
        # Calculate statistics
        if axiom_results['total_questions'] > 0:
            axiom_results['accuracy'] = axiom_results['correct_answers'] / axiom_results['total_questions']
            axiom_results['avg_processing_time'] = total_time / axiom_results['total_questions']
            axiom_results['avg_synergy_score'] = total_synergy / axiom_results['total_questions']
        
        print(f"   [DATA] {axiom_name}: {axiom_results['accuracy']:.3f} accuracy "
              f"({axiom_results['correct_answers']}/{axiom_results['total_questions']})")
        
        return axiom_results
    
    def run_logic_type_tests(self, logic_type: str, format_type: str = "BQA") -> Dict[str, Any]:
        """Run tests for a specific logic type."""
        print(f"\n[SEARCH] Testing {logic_type} ({format_type} format)...")
        
        # Load test data
        test_data = self.load_test_data(logic_type, format_type)
        
        if not test_data:
            print(f"[-] No test data found for {logic_type}")
            return {}
        
        logic_results = {
            'logic_type': logic_type,
            'format_type': format_type,
            'axiom_results': {},
            'overall_accuracy': 0.0,
            'total_questions': 0,
            'correct_answers': 0,
            'avg_processing_time': 0.0,
            'avg_synergy_score': 0.0
        }
        
        total_time = 0.0
        total_synergy = 0.0
        
        # Test each axiom
        for axiom_name, axiom_data in test_data.items():
            axiom_results = self.run_axiom_tests(axiom_data, axiom_name)
            logic_results['axiom_results'][axiom_name] = axiom_results
            
            # Accumulate statistics
            logic_results['total_questions'] += axiom_results['total_questions']
            logic_results['correct_answers'] += axiom_results['correct_answers']
            total_time += axiom_results['avg_processing_time'] * axiom_results['total_questions']
            total_synergy += axiom_results['avg_synergy_score'] * axiom_results['total_questions']
        
        # Calculate overall statistics
        if logic_results['total_questions'] > 0:
            logic_results['overall_accuracy'] = logic_results['correct_answers'] / logic_results['total_questions']
            logic_results['avg_processing_time'] = total_time / logic_results['total_questions']
            logic_results['avg_synergy_score'] = total_synergy / logic_results['total_questions']
        
        print(f"[CHART] {logic_type} Overall: {logic_results['overall_accuracy']:.3f} accuracy "
              f"({logic_results['correct_answers']}/{logic_results['total_questions']})")
        
        return logic_results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive tests across all LogicBench categories."""
        print("[ROCKET] Starting Comprehensive LogicBench Test...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test different logic types
        logic_types = ['propositional_logic', 'first_order_logic', 'nm_logic']
        
        comprehensive_results = {
            'test_timestamp': start_time,
            'logic_type_results': {},
            'overall_statistics': {},
            'performance_summary': {}
        }
        
        total_questions = 0
        total_correct = 0
        total_processing_time = 0.0
        
        for logic_type in logic_types:
            logic_results = self.run_logic_type_tests(logic_type)
            if logic_results:
                comprehensive_results['logic_type_results'][logic_type] = logic_results
                
                # Accumulate overall statistics
                total_questions += logic_results['total_questions']
                total_correct += logic_results['correct_answers']
                total_processing_time += logic_results['avg_processing_time'] * logic_results['total_questions']
        
        # Calculate overall statistics
        overall_accuracy = total_correct / total_questions if total_questions > 0 else 0
        avg_processing_time = total_processing_time / total_questions if total_questions > 0 else 0
        
        comprehensive_results['overall_statistics'] = {
            'total_questions': total_questions,
            'total_correct': total_correct,
            'overall_accuracy': overall_accuracy,
            'avg_processing_time': avg_processing_time,
            'total_test_time': time.time() - start_time
        }
        
        # Get performance summary from Wave engine
        comprehensive_results['performance_summary'] = self.wave_engine.get_performance_summary()
        
        # Print final results
        print("\n" + "=" * 60)
        print("[TARGET] COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        print(f"Total Questions: {total_questions}")
        print(f"Total Correct: {total_correct}")
        print(f"Overall Accuracy: {overall_accuracy:.3f}")
        print(f"Average Processing Time: {avg_processing_time:.3f}s")
        print(f"Total Test Time: {comprehensive_results['overall_statistics']['total_test_time']:.1f}s")
        
        # Show accuracy by logic type
        print("\n[DATA] Accuracy by Logic Type:")
        for logic_type, results in comprehensive_results['logic_type_results'].items():
            print(f"  {logic_type}: {results['overall_accuracy']:.3f}")
        
        return comprehensive_results
    
    def run_specific_test(self, logic_type: str, axiom: str, question_index: int = 0) -> Dict[str, Any]:
        """Run a specific test for debugging."""
        print(f"[SEARCH] Running specific test: {logic_type} -> {axiom} -> question {question_index}")
        
        # Load test data
        test_data = self.load_test_data(logic_type)
        
        if axiom not in test_data:
            print(f"[-] Axiom {axiom} not found in {logic_type}")
            return {}
        
        axiom_data = test_data[axiom]
        samples = axiom_data.get('samples', axiom_data.get('data_samples', []))
        
        if question_index >= len(samples):
            print(f"[-] Question index {question_index} out of range")
            return {}
        
        sample = samples[question_index]
        context = {
            'type': axiom_data.get('type', logic_type),
            'axiom': axiom_data.get('axiom', axiom),
            'context': sample.get('context', '')
        }
        
        # Get first QA pair
        qa_pairs = sample.get('qa_pairs', [])
        if not qa_pairs:
            print("[-] No QA pairs found")
            return {}
        
        qa = qa_pairs[0]
        question = qa.get('question', '')
        expected_answer = qa.get('answer', '')
        
        print(f"Context: {context['context']}")
        print(f"Question: {question}")
        print(f"Expected: {expected_answer}")
        
        # Run test
        result = self.run_single_test(question, expected_answer, context)
        
        print(f"Actual: {result['actual_answer']}")
        print(f"Correct: {result['correct']}")
        print(f"Processing time: {result['processing_time']:.3f}s")
        
        if result['expert_response']:
            print(f"Expert confidence: {result['expert_response'].confidence:.3f}")
            print(f"Expert reasoning: {result['expert_response'].reasoning}")
        
        return result
    
    def save_results(self, results: Dict[str, Any], filename: str = "logicbench_results.json"):
        """Save test results to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"[+] Results saved to {filename}")
        except Exception as e:
            print(f"[-] Error saving results: {e}")
    
    def analyze_errors(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze common error patterns."""
        error_analysis = {
            'error_by_logic_type': {},
            'error_by_axiom': {},
            'common_error_patterns': [],
            'low_confidence_errors': [],
            'high_confidence_errors': []
        }
        
        for logic_type, logic_results in results.get('logic_type_results', {}).items():
            logic_errors = []
            
            for axiom, axiom_results in logic_results.get('axiom_results', {}).items():
                axiom_errors = []
                
                for test_detail in axiom_results.get('test_details', []):
                    if not test_detail['correct']:
                        error_info = {
                            'question': test_detail['question'],
                            'expected': test_detail['expected_answer'],
                            'actual': test_detail['actual_answer'],
                            'expert_confidence': test_detail.get('expert_response', {}).get('confidence', 0)
                        }
                        
                        axiom_errors.append(error_info)
                        logic_errors.append(error_info)
                        
                        # Categorize errors
                        if error_info['expert_confidence'] < 0.5:
                            error_analysis['low_confidence_errors'].append(error_info)
                        else:
                            error_analysis['high_confidence_errors'].append(error_info)
                
                if axiom_errors:
                    error_analysis['error_by_axiom'][axiom] = axiom_errors
            
            if logic_errors:
                error_analysis['error_by_logic_type'][logic_type] = logic_errors
        
        return error_analysis


def main():
    """Main function to run LogicBench tests."""
    print("[BRAIN] LogicBench Test Runner for Enhanced Wave Engine")
    print("=" * 60)
    
    # Initialize test runner
    runner = LogicBenchTestRunner()
    
    # Run comprehensive tests
    results = runner.run_comprehensive_test()
    
    # Save results
    runner.save_results(results)
    
    # Analyze errors
    error_analysis = runner.analyze_errors(results)
    
    print("\n[SEARCH] Error Analysis:")
    print(f"Low confidence errors: {len(error_analysis['low_confidence_errors'])}")
    print(f"High confidence errors: {len(error_analysis['high_confidence_errors'])}")
    
    # Optimize Wave engine performance
    print("\n[BOLT] Optimizing Wave Engine Performance...")
    runner.wave_engine.optimize_performance()
    
    print("\n[+] LogicBench testing completed!")


if __name__ == "__main__":
    main() 