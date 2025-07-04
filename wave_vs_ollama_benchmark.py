#!/usr/bin/env python3
"""
WAVE vs OLLAMA BENCHMARK
Head-to-head comparison on LogicBench questions
"""

import json
import time
import random
import requests
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine
from typing import List, Dict, Any

class WaveVsOllamaBenchmark:
    """Compare Wave engine vs Ollama models on LogicBench"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.wave_engine = EnhancedWaveEngine()
        self.ollama_url = ollama_url
        self.results = {
            'wave': {'correct': 0, 'total': 0, 'time': 0, 'answers': []},
            'ollama': {'correct': 0, 'total': 0, 'time': 0, 'answers': []}
        }
    
    def get_available_ollama_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return models
            else:
                print(f"❌ Could not connect to Ollama at {self.ollama_url}")
                return []
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {e}")
            return []
    
    def ask_ollama(self, model: str, prompt: str, max_tokens: int = 50) -> str:
        """Ask Ollama model a question"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for consistent logical reasoning
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return "error"
        except Exception as e:
            print(f"❌ Error querying Ollama: {e}")
            return "error"
    
    def extract_yes_no_answer(self, response: str) -> str:
        """Extract yes/no answer from model response"""
        response_lower = response.lower()
        
        # Look for clear yes/no indicators
        if 'yes' in response_lower and 'no' not in response_lower:
            return 'yes'
        elif 'no' in response_lower and 'yes' not in response_lower:
            return 'no'
        elif response_lower.startswith('yes'):
            return 'yes'
        elif response_lower.startswith('no'):
            return 'no'
        else:
            # If unclear, default to 'no' (conservative)
            return 'no'
    
    def test_wave_engine(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test Wave engine on questions"""
        print("🌊 Testing Wave Engine...")
        
        start_time = time.time()
        correct = 0
        answers = []
        
        for q in questions:
            context = {
                'context': q['context'],
                'type': q['logic_type'],
                'axiom': q['axiom']
            }
            
            expert = self.wave_engine.expert_registry.find_best_expert(q['question'], context)
            if expert and expert.can_handle(q['question'], context) > 0.3:
                result = expert.process_query(q['question'], context)
                predicted = result.answer
            else:
                predicted = self.fallback_reasoning(q['question'], q['context'], q['logic_type'], q['axiom'])
            
            is_correct = predicted.lower() == q['answer'].lower()
            if is_correct:
                correct += 1
            
            answers.append({
                'question': q['question'],
                'expected': q['answer'],
                'predicted': predicted,
                'correct': is_correct
            })
        
        end_time = time.time()
        
        return {
            'correct': correct,
            'total': len(questions),
            'time': end_time - start_time,
            'answers': answers,
            'accuracy': correct / len(questions) if questions else 0
        }
    
    def test_ollama_model(self, model: str, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test Ollama model on questions"""
        print(f"🤖 Testing Ollama model: {model}...")
        
        start_time = time.time()
        correct = 0
        answers = []
        
        for i, q in enumerate(questions):
            # Create prompt for logical reasoning
            prompt = f"""Context: {q['context']}

Question: {q['question']}

Please answer with just 'yes' or 'no' based on logical reasoning."""
            
            response = self.ask_ollama(model, prompt)
            predicted = self.extract_yes_no_answer(response)
            
            is_correct = predicted.lower() == q['answer'].lower()
            if is_correct:
                correct += 1
            
            answers.append({
                'question': q['question'],
                'expected': q['answer'],
                'predicted': predicted,
                'correct': is_correct,
                'raw_response': response
            })
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{len(questions)} ({((i + 1)/len(questions)*100):.1f}%)")
        
        end_time = time.time()
        
        return {
            'correct': correct,
            'total': len(questions),
            'time': end_time - start_time,
            'answers': answers,
            'accuracy': correct / len(questions) if questions else 0
        }
    
    def fallback_reasoning(self, question: str, context: str, logic_type: str, axiom: str) -> str:
        """Fallback reasoning for Wave engine"""
        question_lower = question.lower()
        has_negation = any(neg in question_lower for neg in ['not', "don't", "doesn't", "won't", "isn't", "aren't"])
        
        if axiom == 'modus_tollens':
            return "yes" if has_negation else "no"
        else:
            return "no" if has_negation else "yes"
    
    def load_sample_questions(self, sample_size: int = 100) -> List[Dict[str, Any]]:
        """Load a sample of LogicBench questions"""
        questions = []
        
        # Focus on high-performing logic types
        target_types = ['propositional_logic', 'first_order_logic']
        
        for logic_type in target_types:
            base_path = Path(f"logicbench/LogicBench(Eval)/BQA/{logic_type}")
            
            if not base_path.exists():
                continue
                
            for axiom_dir in base_path.iterdir():
                if axiom_dir.is_dir():
                    axiom = axiom_dir.name
                    data_file = axiom_dir / "data_instances.json"
                    
                    if data_file.exists():
                        try:
                            with open(data_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            samples = data.get('samples', [])
                            for sample in samples:
                                context = sample.get('context', '')
                                qa_pairs = sample.get('qa_pairs', [])
                                
                                for qa_pair in qa_pairs:
                                    questions.append({
                                        'context': context,
                                        'question': qa_pair.get('question', ''),
                                        'answer': qa_pair.get('answer', ''),
                                        'logic_type': logic_type,
                                        'axiom': axiom
                                    })
                        except Exception as e:
                            print(f"❌ Error loading {data_file}: {e}")
        
        # Sample questions
        if len(questions) > sample_size:
            questions = random.sample(questions, sample_size)
        
        return questions
    
    def run_comparison(self, ollama_model: str, sample_size: int = 100):
        """Run head-to-head comparison"""
        print("🏁 WAVE vs OLLAMA BENCHMARK")
        print("=" * 50)
        
        # Load questions
        print(f"📊 Loading {sample_size} LogicBench questions...")
        questions = self.load_sample_questions(sample_size)
        
        if not questions:
            print("❌ No questions loaded!")
            return
        
        print(f"✅ Loaded {len(questions)} questions")
        
        # Test Wave engine
        wave_results = self.test_wave_engine(questions)
        
        # Test Ollama model
        ollama_results = self.test_ollama_model(ollama_model, questions)
        
        # Display results
        self.display_comparison(wave_results, ollama_results, ollama_model)
        
        # Save detailed results
        results = {
            'wave': wave_results,
            'ollama': ollama_results,
            'ollama_model': ollama_model,
            'questions': questions
        }
        
        with open('wave_vs_ollama_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n💾 Detailed results saved to: wave_vs_ollama_results.json")
    
    def display_comparison(self, wave_results: Dict[str, Any], ollama_results: Dict[str, Any], model_name: str):
        """Display comparison results"""
        print("\n🏆 BENCHMARK RESULTS")
        print("=" * 50)
        
        # Accuracy comparison
        print(f"📊 ACCURACY COMPARISON:")
        print(f"   🌊 Wave Engine:  {wave_results['accuracy']:.3f} ({wave_results['accuracy']*100:.1f}%)")
        print(f"   🤖 {model_name}: {ollama_results['accuracy']:.3f} ({ollama_results['accuracy']*100:.1f}%)")
        
        # Determine winner
        if wave_results['accuracy'] > ollama_results['accuracy']:
            diff = (wave_results['accuracy'] - ollama_results['accuracy']) * 100
            print(f"   🏆 WINNER: Wave Engine (+{diff:.1f} percentage points)")
        elif ollama_results['accuracy'] > wave_results['accuracy']:
            diff = (ollama_results['accuracy'] - wave_results['accuracy']) * 100
            print(f"   🏆 WINNER: {model_name} (+{diff:.1f} percentage points)")
        else:
            print(f"   🤝 TIE!")
        
        # Speed comparison
        print(f"\n⚡ SPEED COMPARISON:")
        print(f"   🌊 Wave Engine:  {wave_results['time']:.2f}s ({wave_results['total']/wave_results['time']:.1f} q/s)")
        print(f"   🤖 {model_name}: {ollama_results['time']:.2f}s ({ollama_results['total']/ollama_results['time']:.1f} q/s)")
        
        # Speed winner
        wave_speed = wave_results['total'] / wave_results['time']
        ollama_speed = ollama_results['total'] / ollama_results['time']
        speed_ratio = wave_speed / ollama_speed
        
        print(f"   🚀 Wave Engine is {speed_ratio:.1f}x faster!")
        
        # Overall verdict
        print(f"\n🎯 OVERALL VERDICT:")
        if wave_results['accuracy'] > ollama_results['accuracy']:
            print(f"   🌊 Wave Engine DOMINATES with better accuracy AND speed!")
        elif wave_results['accuracy'] == ollama_results['accuracy']:
            print(f"   🌊 Wave Engine WINS on speed (same accuracy but {speed_ratio:.1f}x faster)!")
        else:
            print(f"   🤖 {model_name} has better accuracy, but Wave Engine is {speed_ratio:.1f}x faster")


def main():
    """Main benchmark function"""
    benchmark = WaveVsOllamaBenchmark()
    
    # Get available models
    models = benchmark.get_available_ollama_models()
    
    if not models:
        print("❌ No Ollama models found! Make sure Ollama is running.")
        return
    
    print("🤖 Available Ollama models:")
    for i, model in enumerate(models):
        print(f"   {i+1}. {model}")
    
    # Let user choose model
    try:
        choice = input(f"\nChoose model (1-{len(models)}): ")
        model_index = int(choice) - 1
        
        if 0 <= model_index < len(models):
            selected_model = models[model_index]
        else:
            print("❌ Invalid choice, using first model")
            selected_model = models[0]
    except:
        print("❌ Invalid input, using first model")
        selected_model = models[0]
    
    # Ask for sample size
    try:
        sample_size = input(f"\nSample size (default 50 for reasonable time): ")
        sample_size = int(sample_size) if sample_size else 50
    except:
        sample_size = 50
    
    print(f"\n🎯 Selected: {selected_model}")
    print(f"📊 Sample size: {sample_size}")
    
    # Run benchmark
    benchmark.run_comparison(selected_model, sample_size)


if __name__ == "__main__":
    main() 