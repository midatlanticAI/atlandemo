#!/usr/bin/env python3
"""
COMPREHENSIVE LOGICBENCH BENCHMARK TEST
Full evaluation across all logical reasoning types - no half measures!
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple
from enhanced_wave_engine import EnhancedWaveEngine


class ComprehensiveLogicBenchTest:
    """Comprehensive LogicBench benchmark evaluation."""
    
    def __init__(self):
        self.engine = EnhancedWaveEngine()
        self.results = {}
        self.total_questions = 0
        self.total_correct = 0
        
    def find_logicbench_files(self) -> List[Tuple[str, str]]:
        """Find all LogicBench test files."""
        logicbench_root = Path("logicbench/LogicBench(Eval)/BQA")
        
        if not logicbench_root.exists():
            print(f"[-] LogicBench directory not found: {logicbench_root}")
            return []
        
        test_files = []
        
        # Walk through all logic types
        for logic_type in logicbench_root.iterdir():
            if logic_type.is_dir():
                # Walk through all axioms in this logic type
                for axiom in logic_type.iterdir():
                    if axiom.is_dir():
                        data_file = axiom / "data_instances.json"
                        if data_file.exists():
                            test_files.append((str(logic_type.name), str(axiom.name)))
        
        return test_files
    
    def run_single_test_file(self, logic_type: str, axiom: str) -> Dict:
        """Run tests for a single LogicBench file."""
        file_path = f"logicbench/LogicBench(Eval)/BQA/{logic_type}/{axiom}/data_instances.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n🧪 Testing {logic_type} / {axiom}")
            print(f"   📁 File: {file_path}")
            
            samples = data.get('samples', [])
            print(f"   [DATA] Samples: {len(samples)}")
            
            correct = 0
            total = 0
            detailed_results = []
            
            for sample in samples:
                context = {
                    'type': logic_type,
                    'axiom': axiom,
                    'context': sample.get('context', '')
                }
                
                qa_pairs = sample.get('qa_pairs', [])
                for qa in qa_pairs:
                    question = qa.get('question', '')
                    expected = qa.get('answer', '')
                    
                    if question and expected:
                        # Process the question
                        result = self.engine.process_query(question, context)
                        actual = result['final_answer']
                        
                        is_correct = actual.lower() == expected.lower()
                        if is_correct:
                            correct += 1
                        
                        # Get expert confidence safely
                        expert_confidence = 0
                        if result.get('expert_response'):
                            expert_confidence = result['expert_response'].confidence
                        
                        detailed_results.append({
                            'question': question,
                            'expected': expected,
                            'actual': actual,
                            'correct': is_correct,
                            'expert_confidence': expert_confidence,
                            'processing_time': result.get('processing_time', 0)
                        })
                        
                        total += 1
            
            accuracy = correct / total if total > 0 else 0
            
            print(f"   [+] Correct: {correct}/{total}")
            print(f"   [CHART] Accuracy: {accuracy:.3f}")
            
            return {
                'logic_type': logic_type,
                'axiom': axiom,
                'total_questions': total,
                'correct_answers': correct,
                'accuracy': accuracy,
                'detailed_results': detailed_results
            }
            
        except Exception as e:
            print(f"   [-] Error: {e}")
            return {
                'logic_type': logic_type,
                'axiom': axiom,
                'total_questions': 0,
                'correct_answers': 0,
                'accuracy': 0,
                'error': str(e)
            }
    
    def run_comprehensive_benchmark(self) -> Dict:
        """Run the complete LogicBench benchmark."""
        print("[ROCKET] COMPREHENSIVE LOGICBENCH BENCHMARK")
        print("[BRAIN] Wave Engine with Logic Expert Module")
        print("[TARGET] Full evaluation across all logical reasoning types")
        print("=" * 80)
        
        # Find all test files
        test_files = self.find_logicbench_files()
        
        if not test_files:
            print("[-] No LogicBench files found!")
            return {}
        
        print(f"📁 Found {len(test_files)} test categories:")
        for logic_type, axiom in test_files:
            print(f"   • {logic_type} / {axiom}")
        
        print("\n🧪 Starting comprehensive evaluation...")
        
        # Run tests for each file
        all_results = []
        logic_type_summary = {}
        
        for logic_type, axiom in test_files:
            result = self.run_single_test_file(logic_type, axiom)
            all_results.append(result)
            
            # Update totals
            if 'error' not in result:
                self.total_questions += result['total_questions']
                self.total_correct += result['correct_answers']
                
                # Track by logic type
                if logic_type not in logic_type_summary:
                    logic_type_summary[logic_type] = {
                        'total_questions': 0,
                        'correct_answers': 0,
                        'axioms': []
                    }
                
                logic_type_summary[logic_type]['total_questions'] += result['total_questions']
                logic_type_summary[logic_type]['correct_answers'] += result['correct_answers']
                logic_type_summary[logic_type]['axioms'].append({
                    'axiom': axiom,
                    'accuracy': result['accuracy']
                })
        
        # Calculate accuracies
        for logic_type in logic_type_summary:
            total = logic_type_summary[logic_type]['total_questions']
            correct = logic_type_summary[logic_type]['correct_answers']
            logic_type_summary[logic_type]['accuracy'] = correct / total if total > 0 else 0
        
        overall_accuracy = self.total_correct / self.total_questions if self.total_questions > 0 else 0
        
        # Generate comprehensive report
        return {
            'overall_accuracy': overall_accuracy,
            'total_questions': self.total_questions,
            'total_correct': self.total_correct,
            'logic_type_summary': logic_type_summary,
            'detailed_results': all_results,
            'test_files_count': len(test_files)
        }
    
    def print_comprehensive_report(self, results: Dict):
        """Print a comprehensive benchmark report."""
        print("\n" + "=" * 80)
        print("[TARGET] COMPREHENSIVE LOGICBENCH BENCHMARK RESULTS")
        print("=" * 80)
        
        overall_accuracy = results['overall_accuracy']
        total_questions = results['total_questions']
        total_correct = results['total_correct']
        
        print(f"[DATA] OVERALL PERFORMANCE:")
        print(f"   Total Questions: {total_questions}")
        print(f"   Correct Answers: {total_correct}")
        print(f"   Overall Accuracy: {overall_accuracy:.3f}")
        
        # Performance grade
        if overall_accuracy >= 0.9:
            grade = "🥇 EXCELLENT"
        elif overall_accuracy >= 0.8:
            grade = "🥈 VERY GOOD"
        elif overall_accuracy >= 0.7:
            grade = "🥉 GOOD"
        elif overall_accuracy >= 0.6:
            grade = "[WARN] FAIR"
        else:
            grade = "[-] NEEDS IMPROVEMENT"
        
        print(f"   Grade: {grade}")
        
        # Logic type breakdown
        print(f"\n📋 LOGIC TYPE BREAKDOWN:")
        logic_type_summary = results['logic_type_summary']
        
        for logic_type, summary in logic_type_summary.items():
            accuracy = summary['accuracy']
            total = summary['total_questions']
            correct = summary['correct_answers']
            
            print(f"\n   [BRAIN] {logic_type.upper()}:")
            print(f"      Questions: {total}")
            print(f"      Correct: {correct}")
            print(f"      Accuracy: {accuracy:.3f}")
            
            # Show axiom breakdown
            print(f"      Axioms tested:")
            for axiom_result in summary['axioms']:
                axiom = axiom_result['axiom']
                axiom_accuracy = axiom_result['accuracy']
                status = "[+]" if axiom_accuracy >= 0.8 else "[WARN]" if axiom_accuracy >= 0.6 else "[-]"
                print(f"        {status} {axiom}: {axiom_accuracy:.3f}")
        
        # Best and worst performing areas
        print(f"\n[TROPHY] BEST PERFORMING AREAS:")
        best_axioms = []
        worst_axioms = []
        
        for result in results['detailed_results']:
            if 'error' not in result:
                axiom_name = f"{result['logic_type']}/{result['axiom']}"
                accuracy = result['accuracy']
                best_axioms.append((axiom_name, accuracy))
                worst_axioms.append((axiom_name, accuracy))
        
        best_axioms.sort(key=lambda x: x[1], reverse=True)
        worst_axioms.sort(key=lambda x: x[1])
        
        print(f"   Top 3 axioms:")
        for i, (axiom, accuracy) in enumerate(best_axioms[:3]):
            print(f"      {i+1}. {axiom}: {accuracy:.3f}")
        
        print(f"\n[TOOL] AREAS FOR IMPROVEMENT:")
        print(f"   Bottom 3 axioms:")
        for i, (axiom, accuracy) in enumerate(worst_axioms[:3]):
            print(f"      {i+1}. {axiom}: {accuracy:.3f}")
        
        # Final verdict
        print(f"\n[TARGET] FINAL VERDICT:")
        if overall_accuracy >= 0.85:
            print("   [ROCKET] VICTORY! Wave Engine dominates LogicBench!")
            print("   [+] Ready for production logical reasoning tasks")
        elif overall_accuracy >= 0.75:
            print("   [STAR] STRONG PERFORMANCE! Wave Engine shows excellent promise")
            print("   [+] Competitive with state-of-the-art logical reasoning systems")
        elif overall_accuracy >= 0.65:
            print("   💪 SOLID FOUNDATION! Wave Engine demonstrates core capabilities")
            print("   [TOOL] Some fine-tuning needed for expert-level performance")
        else:
            print("   [TOOL] DEVELOPMENT STAGE! Wave Engine needs significant improvement")
            print("   📚 Focus on core logical reasoning patterns")
        
        print(f"\n[BRAIN] WAVE ENGINE VERDICT:")
        print(f"   [WAVE] Temporal cognition + Expert modules = {overall_accuracy:.1%} accuracy")
        print(f"   [BOT] Logic expert module functioning at {overall_accuracy:.1%} effectiveness")
        print(f"   [BOLT] Wave interference patterns enabling logical reasoning")
        
        return results

    def save_results(self, results: Dict, filename: str = "comprehensive_logicbench_results.json"):
        """Save comprehensive results to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n[SAVE] Results saved to: {filename}")
        except Exception as e:
            print(f"[-] Error saving results: {e}")


def main():
    """Run the comprehensive LogicBench benchmark."""
    print("[ROCKET] LAUNCHING COMPREHENSIVE LOGICBENCH BENCHMARK")
    print("[WAVE] Wave Engine + Logic Expert Module")
    print("[TARGET] Full evaluation - no half measures!")
    
    # Create test instance
    test_runner = ComprehensiveLogicBenchTest()
    
    # Run comprehensive benchmark
    start_time = time.time()
    results = test_runner.run_comprehensive_benchmark()
    end_time = time.time()
    
    if results:
        # Add timing information
        results['total_time'] = end_time - start_time
        if results['total_questions'] > 0 and (end_time - start_time) > 0:
            results['questions_per_second'] = results['total_questions'] / (end_time - start_time)
        else:
            results['questions_per_second'] = 0
        
        # Print comprehensive report
        test_runner.print_comprehensive_report(results)
        
        # Save results
        test_runner.save_results(results)
        
        print(f"\n⏱️ PERFORMANCE METRICS:")
        print(f"   Total time: {results['total_time']:.2f} seconds")
        print(f"   Questions/second: {results['questions_per_second']:.1f}")
        if results['total_questions'] > 0:
            print(f"   Avg time per question: {results['total_time']/results['total_questions']:.3f}s")
        else:
            print(f"   Avg time per question: N/A (no questions processed)")
        
        print("\n[PARTY] COMPREHENSIVE LOGICBENCH BENCHMARK COMPLETE!")
        
    else:
        print("[-] Benchmark failed to run!")


if __name__ == "__main__":
    main() 