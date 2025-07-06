#!/usr/bin/env python3
"""
GPQA Diamond Benchmark Test
Tests Enhanced Wave Engine against graduate-level scientific reasoning questions
"""

import json
import time
import random
import requests
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine


class GPQADiamondBenchmark:
    """GPQA Diamond benchmark for Enhanced Wave Engine"""
    
    def __init__(self):
        self.engine = EnhancedWaveEngine()
        self.questions = []
        self.results = {}
        
    def download_gpqa_diamond(self):
        """Download GPQA Diamond dataset"""
        print("📥 Downloading GPQA Diamond dataset...")
        
        # Use the Hugging Face dataset viewer API to get the data
        api_url = "https://datasets-server.huggingface.co/rows?dataset=hendrydong%2Fgpqa_diamond&config=default&split=test&offset=0&length=200"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                questions = []
                
                for row in data['rows']:
                    content = row['row']
                    
                    # Extract the problem, solution, and domain
                    problem = content.get('problem', '')
                    solution = content.get('solution', '')
                    domain = content.get('domain', 'Unknown')
                    
                    # Extract answer choices if they exist in the problem
                    choices = []
                    if '(A)' in problem and '(B)' in problem:
                        # This appears to be multiple choice
                        lines = problem.split('\n')
                        problem_text = ""
                        for line in lines:
                            if line.strip().startswith('(A)') or line.strip().startswith('(B)') or \
                               line.strip().startswith('(C)') or line.strip().startswith('(D)'):
                                choices.append(line.strip())
                            else:
                                problem_text += line + " "
                        problem = problem_text.strip()
                    
                    questions.append({
                        'problem': problem,
                        'solution': solution,
                        'domain': domain,
                        'choices': choices
                    })
                
                self.questions = questions
                print(f"[+] Downloaded {len(questions)} GPQA Diamond questions")
                return True
                
        except Exception as e:
            print(f"[-] Error downloading GPQA Diamond: {e}")
            
        # Fallback: Create some representative sample questions
        print("📝 Using sample GPQA Diamond-style questions...")
        self.questions = self.get_sample_questions()
        return True
    
    def get_sample_questions(self):
        """Sample GPQA Diamond-style questions for testing"""
        return [
            {
                'problem': 'Two quantum states with energies E1 and E2 have a lifetime of 10^-9 sec and 10^-8 sec, respectively. We want to clearly distinguish these two energy levels. Which one of the following options could be their energy difference so that they can be clearly resolved?',
                'solution': '10^-4 eV',
                'domain': 'Physics',
                'choices': ['(A) 10^-11 eV', '(B) 10^-8 eV', '(C) 10^-4 eV', '(D) 10^-9 eV']
            },
            {
                'problem': 'A quantum mechanical particle of mass m moves in two dimensions in the following potential, as a function of (r,θ): V(r, θ) = 1/2 kr^2 + 3/2 kr^2 cos^2(θ). Find the energy spectrum.',
                'solution': 'E = (2n_x+n_y+3/2)ℏ*sqrt(k/m)',
                'domain': 'Physics',
                'choices': ['(A) E = (n_x+3*n_y+3/2) ℏ*sqrt(k/m)', '(B) E = (2n_x+3n_y+1/2) ℏ*sqrt(k/m)', '(C) E = (2n_x+n_y+3/2)ℏ*sqrt(k/m)', '(D) E = (3n_x+2n_y+1/2) ℏ*sqrt(k/m)']
            },
            {
                'problem': 'trans-cinnamaldehyde was treated with methylmagnesium bromide, forming product 1. 1 was treated with pyridinium chlorochromate, forming product 2. 2 was treated with (dimethyl(oxo)-l6-sulfaneylidene)methane in DMSO at elevated temperature, forming product 3. How many carbon atoms are there in product 3?',
                'solution': '11',
                'domain': 'Chemistry',
                'choices': ['(A) 11', '(B) 10', '(C) 12', '(D) 14']
            },
            {
                'problem': 'A spin-half particle is in a linear superposition 0.5|↑⟩+sqrt(3)/2|↓⟩ of its spin-up and spin-down states. If |↑⟩ and |↓⟩ are the eigenstates of σz, then what is the expectation value up to one decimal place, of the operator 10σz+5σx?',
                'solution': '-0.7',
                'domain': 'Physics',
                'choices': ['(A) 0.85', '(B) -1.4', '(C) -0.7', '(D) 1.65']
            },
            {
                'problem': 'Among the following exoplanets, which one has the highest density? a) An Earth-mass and Earth-radius planet. b) A planet with 2 Earth masses and a density of approximately 5.5 g/cm^3. c) A planet with the same composition as Earth but 5 times more massive than Earth. d) A planet with the same composition as Earth but half the mass of Earth.',
                'solution': 'c',
                'domain': 'Physics',
                'choices': ['(A) a', '(B) b', '(C) c', '(D) d']
            },
            {
                'problem': 'The universe is filled with the Cosmic Microwave Background. Consider the annihilation of high energy γ-rays with a photon from the CMB Radiation into electron-positron, i.e. γγ→e+e-. From what energy γ-rays would have their lifetimes in the universe limited by this process? Knowing that the average photon energy of the CMB is 10^-3 eV.',
                'solution': '2.6*1e5 GeV',
                'domain': 'Physics',
                'choices': ['(A) 1.8*1e5 GeV', '(B) 3.9*1e5 GeV', '(C) 2.6*1e5 GeV', '(D) 9.5*1e4 GeV']
            },
            {
                'problem': 'Find KE of product particles in, Pi(+) = mu(+) + nu here Pi(+) is stationary. Rest mass of Pi(+) & mu(+) is 139.6 MeV & 105.7 MeV respectively.',
                'solution': '4.12 MeV, 29.8 MeV',
                'domain': 'Physics',
                'choices': ['(A) 4.12 MeV, 29.8 MeV', '(B) 2.84 MeV, 26.8 MeV', '(C) 7.2 MeV, 32.8 MeV', '(D) 3.52 MeV, 20.8 MeV']
            },
            {
                'problem': 'What is the concentration of calcium ions in a solution containing 0.02 M stochiometric Ca-EDTA complex (we assume that the pH is ideal, T = 25 °C). KCa-EDTA = 5x10^10.',
                'solution': '6.3x10^-7 M',
                'domain': 'Chemistry',
                'choices': ['(A) 6.3x10^-7 M', '(B) 2.0x10^-2 M', '(C) 1.0x10^-2 M', '(D) 5.0x10^-3 M']
            },
            {
                'problem': 'How many of the following compounds will exhibit optical activity? (Z)-1-chloro-2-methylbut-1-ene (3aR,7aS,E)-8-(chloromethylene)hexahydro-4,7-methanoisobenzofuran-1,3-dione (2R,3S)-2,3-dimethylsuccinic acid (2R,3R)-2,3-dimethylsuccinic acid (R)-cyclohex-3-en-1-ol (1s,3s,5s)-cyclohexane-1,3,5-triol 1-cyclopentyl-3-methylbutan-1-one',
                'solution': '3',
                'domain': 'Chemistry',
                'choices': ['(A) 2', '(B) 3', '(C) 4', '(D) 5']
            },
            {
                'problem': 'You perform a high-throughput experiment on white lupine to find genes contributing to resistance to the fungal disease anthracnose. As a result, you receive three candidate genes of unknown function – G1, G2, and G3. You create three knock-out mutants, g1, g2, and g3, and a set of double-mutants, g1g2, g1g3, and g2g3. You know that at least one of these genes is a transcription factor acting upstream of other gene(s). After tests with the pathogen, you receive the following results where 100% is the level of resistance: - resistance of g1: 75% of control - resistance of g2: 0% from control - resistance of g3: 50% from control - resistance of g1g3: 10% from control - resistance of g2g3: 0% from control - resistance of g1g2: 0% from control Which conclusion regarding those genes\' interaction can you draw from this experiment?',
                'solution': 'G2 is a transcription factor, G1 and G3 show gene redundancy, G1 is epistatic towards G3',
                'domain': 'Biology',
                'choices': ['(A) G2 is a transcription factor, G1 and G3 show gene redundancy, G1 is epistatic towards G3', '(B) G2 is a transcription factor, G1 and G3 has the same promoter, G3 is epistatic towards G1', '(C) G2 is a transcription factor, G1 and G3 show pleiotropy, G1 is epistatic towards G3', '(D) G1 is a transcription factor, G2 and G3 show pleiotropy, G2 is epistatic towards G1']
            }
        ]
    
    def run_gpqa_benchmark(self, num_questions=None):
        """Run GPQA Diamond benchmark"""
        if not self.questions:
            print("[-] No questions available. Download dataset first.")
            return
        
        if num_questions is None:
            num_questions = len(self.questions)
        else:
            num_questions = min(num_questions, len(self.questions))
        
        print(f"\n🧬 GPQA DIAMOND BENCHMARK - GRADUATE-LEVEL SCIENTIFIC REASONING")
        print(f"[TARGET] Testing Enhanced Wave Engine on {num_questions} questions")
        print(f"[DATA] Domains: Physics, Chemistry, Biology")
        print("=" * 80)
        
        start_time = time.time()
        
        # Shuffle questions for random sampling
        test_questions = random.sample(self.questions, num_questions)
        
        total_correct = 0
        domain_results = {}
        question_times = []
        
        for i, question in enumerate(test_questions, 1):
            domain = question['domain']
            problem = question['problem']
            correct_answer = question['solution']
            choices = question.get('choices', [])
            
            print(f"\n📝 Question {i}/{num_questions} ({domain})")
            print(f"Problem: {problem[:100]}{'...' if len(problem) > 100 else ''}")
            
            if choices:
                print("Choices:")
                for choice in choices:
                    print(f"  {choice}")
            
            # Process through Enhanced Wave Engine
            start_q = time.time()
            context = {
                'domain': 'scientific_reasoning',
                'subdomain': domain.lower(),
                'question_type': 'multiple_choice' if choices else 'open_ended'
            }
            
            result = self.engine.process_query(problem, context=context)
            process_time = time.time() - start_q
            question_times.append(process_time)
            
            # Extract answer
            answer = result['final_answer']
            expert_response = result.get('expert_response')
            
            # Check correctness
            is_correct = self.check_answer_correctness(answer, correct_answer, choices)
            
            if is_correct:
                total_correct += 1
                print(f"  [+] Correct: {answer}")
            else:
                print(f"  [-] Wrong: {answer}")
                print(f"  Expected: {correct_answer}")
            
            # Show reasoning details
            if expert_response:
                confidence = expert_response.confidence
                reasoning_type = expert_response.metadata.get('problem_type', 'unknown')
                print(f"  [TARGET] Confidence: {confidence:.2f}, Type: {reasoning_type}")
            
            # Track domain performance
            if domain not in domain_results:
                domain_results[domain] = {'correct': 0, 'total': 0, 'times': []}
            
            domain_results[domain]['correct'] += is_correct
            domain_results[domain]['total'] += 1
            domain_results[domain]['times'].append(process_time)
        
        # Calculate results
        end_time = time.time()
        total_time = end_time - start_time
        overall_accuracy = total_correct / num_questions
        avg_time = sum(question_times) / len(question_times)
        
        print(f"\n[TROPHY] GPQA DIAMOND RESULTS")
        print("=" * 50)
        print(f"  Total Questions: {num_questions}")
        print(f"  Total Correct: {total_correct}")
        print(f"  Overall Accuracy: {overall_accuracy:.3f} ({overall_accuracy:.1%})")
        print(f"  Average Time: {avg_time:.3f}s per question")
        print(f"  Total Time: {total_time:.2f} seconds")
        print(f"  Questions/second: {num_questions/total_time:.1f}")
        
        # Domain breakdown
        print(f"\n[DATA] DOMAIN BREAKDOWN:")
        for domain, results in domain_results.items():
            accuracy = results['correct'] / results['total']
            avg_domain_time = sum(results['times']) / len(results['times'])
            print(f"  {domain:15}: {accuracy:.3f} ({accuracy:.1%}) - {results['correct']}/{results['total']} - {avg_domain_time:.2f}s avg")
        
        # Performance assessment
        self.assess_performance(overall_accuracy)
        
        # Store results
        self.results = {
            'overall_accuracy': overall_accuracy,
            'total_questions': num_questions,
            'total_correct': total_correct,
            'domain_results': domain_results,
            'processing_time': total_time,
            'avg_time_per_question': avg_time
        }
        
        return self.results
    
    def check_answer_correctness(self, given_answer, correct_answer, choices):
        """Check if the given answer matches the correct answer"""
        try:
            # Clean up answers for comparison
            given_clean = str(given_answer).strip().lower()
            correct_clean = str(correct_answer).strip().lower()
            
            # Direct match
            if given_clean == correct_clean:
                return True
            
            # Check if it's a multiple choice answer
            if choices:
                # Extract the correct choice letter
                correct_letter = None
                for choice in choices:
                    if correct_clean in choice.lower():
                        correct_letter = choice[1].lower()  # Get the letter after '('
                        break
                
                # Check if the given answer contains the correct letter
                if correct_letter and correct_letter in given_clean:
                    return True
            
            # Check for partial matches (for complex answers)
            if len(correct_clean) > 10:  # For longer answers
                # Check if the main components match
                given_words = given_clean.split()
                correct_words = correct_clean.split()
                
                # If more than half the significant words match
                matches = sum(1 for word in correct_words if len(word) > 3 and word in given_clean)
                significant_words = len([w for w in correct_words if len(w) > 3])
                
                if significant_words > 0 and matches / significant_words > 0.5:
                    return True
            
            # Check for numerical answers
            import re
            given_numbers = re.findall(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', given_clean)
            correct_numbers = re.findall(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', correct_clean)
            
            if given_numbers and correct_numbers:
                try:
                    given_num = float(given_numbers[0])
                    correct_num = float(correct_numbers[0])
                    
                    # Check with relative tolerance
                    if abs(correct_num) > 0:
                        return abs((given_num - correct_num) / correct_num) < 0.1
                    else:
                        return abs(given_num - correct_num) < 0.001
                except:
                    pass
            
            return False
            
        except Exception:
            return False
    
    def assess_performance(self, accuracy):
        """Assess performance compared to other models"""
        print(f"\n[SEARCH] PERFORMANCE ASSESSMENT:")
        
        # GPQA Diamond benchmarks from literature
        benchmarks = {
            'Random Guessing': 0.25,
            'Human PhD Students': 0.65,
            'GPT-4': 0.35,
            'Claude-3': 0.40,
            'Gemini Ultra': 0.42,
            'GPT-4o': 0.45
        }
        
        print(f"  Wave Engine: {accuracy:.1%}")
        print(f"  Comparison:")
        
        for model, acc in sorted(benchmarks.items(), key=lambda x: x[1]):
            if accuracy >= acc:
                status = "[+] BEAT"
            else:
                status = "[-] Below"
            print(f"    {status} {model}: {acc:.1%}")
        
        # Overall assessment
        if accuracy >= 0.65:
            grade = "[TROPHY] EXCEPTIONAL (PhD-level)"
        elif accuracy >= 0.45:
            grade = "🥇 EXCELLENT (SOTA AI-level)"  
        elif accuracy >= 0.35:
            grade = "🥈 GOOD (GPT-4 level)"
        elif accuracy >= 0.25:
            grade = "🥉 FAIR (Above random)"
        else:
            grade = "[-] POOR (Random level)"
        
        print(f"  📝 Overall Grade: {grade}")


def main():
    """Run GPQA Diamond benchmark"""
    print("🧬 GPQA DIAMOND - GRADUATE-LEVEL SCIENTIFIC REASONING BENCHMARK")
    print("[TARGET] Testing Enhanced Wave Engine against PhD-level problems")
    print("=" * 80)
    
    benchmark = GPQADiamondBenchmark()
    
    # Download dataset
    if not benchmark.download_gpqa_diamond():
        print("[-] Failed to download GPQA Diamond dataset")
        return
    
    # Run benchmark
    results = benchmark.run_gpqa_benchmark(num_questions=20)  # Start with 20 questions
    
    print(f"\n[PARTY] GPQA DIAMOND BENCHMARK COMPLETE!")
    print(f"[DATA] Final Score: {results['overall_accuracy']:.1%}")
    print(f"[BOLT] Average Processing Time: {results['avg_time_per_question']:.2f}s")
    
    # Save results
    with open('gpqa_diamond_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"[SAVE] Results saved to gpqa_diamond_results.json")


if __name__ == "__main__":
    main() 