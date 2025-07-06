#!/usr/bin/env python3
"""
MathBench - Comprehensive Mathematical Reasoning Benchmark
Tests the MathExpert module across various mathematical domains and difficulty levels
"""

import json
import time
import random
import math
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine


class MathBenchmark:
    """Mathematical reasoning benchmark for the Enhanced Wave Engine"""
    
    def __init__(self):
        self.engine = EnhancedWaveEngine()
        self.total_questions = 0
        self.total_correct = 0
        self.domain_results = {}
        
    def run_math_benchmark(self, questions_per_domain=20):
        """Run comprehensive mathematical benchmark"""
        print(f"🧮 MATHBENCH - COMPREHENSIVE MATHEMATICAL REASONING BENCHMARK")
        print(f"🎯 Testing Enhanced Wave Engine mathematical capabilities")
        print(f"📊 {questions_per_domain} questions per domain")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test different mathematical domains
        domains = [
            ('arithmetic', self.generate_arithmetic_questions),
            ('algebra', self.generate_algebra_questions),
            ('geometry', self.generate_geometry_questions),
            ('statistics', self.generate_statistics_questions),
            ('word_problems', self.generate_word_problems),
            ('complex_expressions', self.generate_complex_expressions)
        ]
        
        for domain_name, question_generator in domains:
            print(f"\n🔢 TESTING {domain_name.upper()} DOMAIN")
            print("-" * 50)
            
            domain_correct = 0
            domain_total = questions_per_domain
            domain_times = []
            
            questions = question_generator(questions_per_domain)
            
            for i, (question, expected_answer, metadata) in enumerate(questions, 1):
                print(f"  Question {i}/{questions_per_domain}: {question}")
                
                # Process through Enhanced Wave Engine
                start_q = time.time()
                result = self.engine.process_query(question, context={'domain': 'math'})
                process_time = time.time() - start_q
                domain_times.append(process_time)
                
                # Extract answer
                answer = result['final_answer']
                expert_response = result.get('expert_response')
                
                # Check correctness
                is_correct = self.check_answer_correctness(answer, expected_answer, metadata)
                
                if is_correct:
                    domain_correct += 1
                    print(f"    ✅ Correct: {answer}")
                else:
                    print(f"    ❌ Wrong: {answer} (Expected: {expected_answer})")
                
                # Show confidence and problem type
                if expert_response:
                    confidence = expert_response.confidence
                    problem_type = expert_response.metadata.get('problem_type', 'unknown')
                    print(f"    🎯 Confidence: {confidence:.2f}, Type: {problem_type}")
            
            # Domain summary
            domain_accuracy = domain_correct / domain_total
            avg_time = sum(domain_times) / len(domain_times)
            
            print(f"\n  📊 {domain_name.upper()} RESULTS:")
            print(f"    Correct: {domain_correct}/{domain_total} ({domain_accuracy:.1%})")
            print(f"    Average Time: {avg_time:.3f}s")
            print(f"    Questions/sec: {1/avg_time:.1f}")
            
            # Store results
            self.domain_results[domain_name] = {
                'correct': domain_correct,
                'total': domain_total,
                'accuracy': domain_accuracy,
                'avg_time': avg_time,
                'questions': questions
            }
            
            self.total_correct += domain_correct
            self.total_questions += domain_total
        
        # Overall results
        end_time = time.time()
        total_time = end_time - start_time
        overall_accuracy = self.total_correct / self.total_questions
        
        print(f"\n🏆 MATHBENCH OVERALL RESULTS")
        print("=" * 50)
        print(f"  Total Questions: {self.total_questions}")
        print(f"  Total Correct: {self.total_correct}")
        print(f"  Overall Accuracy: {overall_accuracy:.3f} ({overall_accuracy:.1%})")
        print(f"  Total Time: {total_time:.2f} seconds")
        print(f"  Questions/second: {self.total_questions/total_time:.1f}")
        
        # Domain breakdown
        print(f"\n📊 DOMAIN BREAKDOWN:")
        for domain, results in self.domain_results.items():
            accuracy = results['accuracy']
            print(f"  {domain:20}: {accuracy:.3f} ({accuracy:.1%})")
        
        # Performance analysis
        self.analyze_performance()
        
        return {
            'overall_accuracy': overall_accuracy,
            'total_questions': self.total_questions,
            'total_correct': self.total_correct,
            'domain_results': self.domain_results,
            'processing_time': total_time
        }
    
    def generate_arithmetic_questions(self, count):
        """Generate arithmetic questions"""
        questions = []
        
        operations = [
            ('addition', lambda a, b: (f"{a} + {b}", a + b)),
            ('subtraction', lambda a, b: (f"{a} - {b}", a - b)),
            ('multiplication', lambda a, b: (f"{a} * {b}", a * b)),
            ('division', lambda a, b: (f"{a} / {b}", a / b if b != 0 else a)),
            ('mixed', lambda a, b: (f"({a} + {b}) * 2", (a + b) * 2))
        ]
        
        for i in range(count):
            op_name, op_func = random.choice(operations)
            
            if op_name == 'division':
                a = random.randint(2, 20) * random.randint(2, 12)  # Ensure clean division
                b = random.randint(2, 12)
            else:
                a = random.randint(1, 100)
                b = random.randint(1, 100)
            
            question, answer = op_func(a, b)
            questions.append((f"Calculate {question}", answer, {'type': 'arithmetic', 'operation': op_name}))
        
        return questions
    
    def generate_algebra_questions(self, count):
        """Generate algebra questions"""
        questions = []
        
        for i in range(count):
            # Linear equations: ax + b = c
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            x_value = random.randint(1, 15)
            c = a * x_value + b
            
            if random.choice([True, False]):
                question = f"Solve {a}x + {b} = {c}"
            else:
                question = f"Find x when {a}x + {b} = {c}"
            
            questions.append((question, x_value, {'type': 'linear_equation', 'coefficient': a}))
        
        return questions
    
    def generate_geometry_questions(self, count):
        """Generate geometry questions"""
        questions = []
        
        shape_generators = [
            self.generate_circle_area,
            self.generate_triangle_area,
            self.generate_rectangle_area,
            self.generate_circle_circumference
        ]
        
        for i in range(count):
            generator = random.choice(shape_generators)
            question, answer, metadata = generator()
            questions.append((question, answer, metadata))
        
        return questions
    
    def generate_circle_area(self):
        """Generate circle area question"""
        radius = random.randint(1, 15)
        area = math.pi * radius ** 2
        return (
            f"Find the area of a circle with radius {radius}",
            area,
            {'type': 'circle_area', 'radius': radius}
        )
    
    def generate_triangle_area(self):
        """Generate triangle area question"""
        base = random.randint(2, 20)
        height = random.randint(2, 15)
        area = 0.5 * base * height
        return (
            f"Calculate the area of a triangle with base {base} and height {height}",
            area,
            {'type': 'triangle_area', 'base': base, 'height': height}
        )
    
    def generate_rectangle_area(self):
        """Generate rectangle area question"""
        length = random.randint(2, 20)
        width = random.randint(2, 15)
        area = length * width
        return (
            f"Find the area of a rectangle with length {length} and width {width}",
            area,
            {'type': 'rectangle_area', 'length': length, 'width': width}
        )
    
    def generate_circle_circumference(self):
        """Generate circle circumference question"""
        radius = random.randint(1, 15)
        circumference = 2 * math.pi * radius
        return (
            f"Calculate the circumference of a circle with radius {radius}",
            circumference,
            {'type': 'circle_circumference', 'radius': radius}
        )
    
    def generate_statistics_questions(self, count):
        """Generate statistics questions"""
        questions = []
        
        for i in range(count):
            # Generate dataset
            data_size = random.randint(5, 10)
            dataset = [random.randint(1, 50) for _ in range(data_size)]
            
            stat_type = random.choice(['mean', 'median'])
            
            if stat_type == 'mean':
                answer = sum(dataset) / len(dataset)
                question = f"Find the mean of {', '.join(map(str, dataset))}"
            else:  # median
                sorted_data = sorted(dataset)
                n = len(sorted_data)
                if n % 2 == 0:
                    answer = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
                else:
                    answer = sorted_data[n//2]
                question = f"What is the median of {', '.join(map(str, dataset))}?"
            
            questions.append((question, answer, {'type': stat_type, 'dataset': dataset}))
        
        return questions
    
    def generate_word_problems(self, count):
        """Generate word problems"""
        questions = []
        
        problem_templates = [
            self.generate_age_problem,
            self.generate_distance_problem,
            self.generate_money_problem,
            self.generate_percentage_problem
        ]
        
        for i in range(count):
            generator = random.choice(problem_templates)
            question, answer, metadata = generator()
            questions.append((question, answer, metadata))
        
        return questions
    
    def generate_age_problem(self):
        """Generate age word problem"""
        current_age = random.randint(10, 40)
        years_future = random.randint(5, 15)
        future_age = current_age + years_future
        
        return (
            f"Sarah is {current_age} years old. How old will she be in {years_future} years?",
            future_age,
            {'type': 'age_problem', 'operation': 'addition'}
        )
    
    def generate_distance_problem(self):
        """Generate distance word problem"""
        speed = random.randint(30, 80)
        time = random.randint(2, 8)
        distance = speed * time
        
        return (
            f"A car travels at {speed} mph for {time} hours. What distance does it cover?",
            distance,
            {'type': 'distance_problem', 'operation': 'multiplication'}
        )
    
    def generate_money_problem(self):
        """Generate money word problem"""
        initial = random.randint(50, 200)
        spent = random.randint(10, initial - 10)
        remaining = initial - spent
        
        return (
            f"John has ${initial}. He spends ${spent}. How much money does he have left?",
            remaining,
            {'type': 'money_problem', 'operation': 'subtraction'}
        )
    
    def generate_percentage_problem(self):
        """Generate percentage word problem"""
        original = random.randint(100, 1000)
        percentage = random.choice([10, 20, 25, 50])
        result = original * (percentage / 100)
        
        return (
            f"What is {percentage}% of {original}?",
            result,
            {'type': 'percentage_problem', 'percentage': percentage}
        )
    
    def generate_complex_expressions(self, count):
        """Generate complex mathematical expressions"""
        questions = []
        
        for i in range(count):
            # Generate expressions like (a + b) * c - d
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            c = random.randint(2, 10)
            d = random.randint(1, 15)
            
            expression_types = [
                (f"({a} + {b}) * {c}", (a + b) * c),
                (f"({a} + {b}) * {c} - {d}", (a + b) * c - d),
                (f"{a} * {b} + {c} * {d}", a * b + c * d),
                (f"({a} - {b}) * ({c} + {d})", (a - b) * (c + d))
            ]
            
            expression, answer = random.choice(expression_types)
            questions.append((f"Calculate {expression}", answer, {'type': 'complex_expression'}))
        
        return questions
    
    def check_answer_correctness(self, given_answer, expected_answer, metadata):
        """Check if the given answer is correct"""
        try:
            # Handle string answers
            if isinstance(given_answer, str):
                if "Cannot solve" in given_answer or "Error" in given_answer:
                    return False
                
                # Try to extract number from answer
                import re
                numbers = re.findall(r'-?\d+\.?\d*', given_answer)
                if numbers:
                    given_answer = float(numbers[-1])  # Take the last number found
                else:
                    return False
            
            # Convert to float for comparison
            given = float(given_answer)
            expected = float(expected_answer)
            
            # Use relative tolerance for floating point comparison
            tolerance = 0.01  # 1% tolerance
            if abs(expected) > 0:
                return abs((given - expected) / expected) <= tolerance
            else:
                return abs(given - expected) <= 0.001
                
        except (ValueError, TypeError):
            return False
    
    def analyze_performance(self):
        """Analyze performance patterns"""
        print(f"\n🔍 PERFORMANCE ANALYSIS:")
        
        # Find strongest and weakest domains
        accuracies = [(domain, results['accuracy']) for domain, results in self.domain_results.items()]
        accuracies.sort(key=lambda x: x[1], reverse=True)
        
        best_domain, best_acc = accuracies[0]
        worst_domain, worst_acc = accuracies[-1]
        
        print(f"  🏆 Strongest Domain: {best_domain} ({best_acc:.1%})")
        print(f"  🎯 Weakest Domain: {worst_domain} ({worst_acc:.1%})")
        print(f"  📈 Performance Range: {(best_acc - worst_acc)*100:.1f} percentage points")
        
        # Speed analysis
        speeds = [(domain, 1/results['avg_time']) for domain, results in self.domain_results.items()]
        speeds.sort(key=lambda x: x[1], reverse=True)
        
        fastest_domain, fastest_speed = speeds[0]
        print(f"  ⚡ Fastest Domain: {fastest_domain} ({fastest_speed:.1f} q/s)")
        
        # Overall assessment
        overall_acc = self.total_correct / self.total_questions
        if overall_acc >= 0.9:
            grade = "EXCELLENT"
        elif overall_acc >= 0.8:
            grade = "GOOD"
        elif overall_acc >= 0.7:
            grade = "FAIR"
        else:
            grade = "NEEDS IMPROVEMENT"
        
        print(f"  📝 Overall Grade: {grade}")


def main():
    """Run the MathBench benchmark"""
    print("🧮 MATHBENCH - MATHEMATICAL REASONING BENCHMARK")
    print("🎯 Comprehensive evaluation of Enhanced Wave Engine math capabilities")
    print("=" * 70)
    
    benchmark = MathBenchmark()
    results = benchmark.run_math_benchmark(questions_per_domain=15)
    
    print(f"\n🎉 MATHBENCH COMPLETE!")
    print(f"📊 Overall Performance: {results['overall_accuracy']:.1%}")
    print(f"⚡ Processing Speed: {results['total_questions']/results['processing_time']:.1f} q/s")
    print(f"🧠 Mathematical Expert Module: {'PASSED' if results['overall_accuracy'] >= 0.75 else 'NEEDS WORK'}")


if __name__ == "__main__":
    main() 