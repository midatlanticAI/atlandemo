"""
Mathematical Expert Module for Wave-based Cognition
Provides comprehensive mathematical reasoning capabilities.
"""

import re
import math
import random
from typing import Dict, List, Any, Optional, Tuple
from .base_expert import BaseExpertModule, ExpertResponse


class MathExpertModule(BaseExpertModule):
    """
    Expert module for mathematical reasoning and problem solving.
    
    Covers:
    - Arithmetic and basic operations
    - Algebra and equation solving
    - Calculus concepts
    - Statistics and probability
    - Geometry and trigonometry
    - Mathematical reasoning patterns
    """
    
    def __init__(self):
        super().__init__(
            name="MathExpert",
            domain="mathematical_reasoning",
            version="1.0.0"
        )
        
        # Mathematical knowledge patterns
        self.math_patterns = {
            'arithmetic': {
                'addition': r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',
                'subtraction': r'(\d+(?:\.\d+)?)\s*[-−]\s*(\d+(?:\.\d+)?)',
                'multiplication': r'(\d+(?:\.\d+)?)\s*[×*]\s*(\d+(?:\.\d+)?)',
                'division': r'(\d+(?:\.\d+)?)\s*[÷/]\s*(\d+(?:\.\d+)?)',
                'percentage': r'(\d+(?:\.\d+)?)\s*%',
                'fraction': r'(\d+)/(\d+)'
            },
            'algebra': {
                'linear_equation': r'(\d*)\s*x\s*([+-])\s*(\d+)\s*=\s*(\d+)',
                'quadratic': r'(\d*)\s*x\s*\^\s*2|(\d*)\s*x\s*²',
                'variable': r'[a-zA-Z]\w*',
                'exponent': r'(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)',
                'logarithm': r'log\s*\(\s*(\d+(?:\.\d+)?)\s*\)',
                'square_root': r'sqrt\s*\(\s*(\d+(?:\.\d+)?)\s*\)|√\s*(\d+(?:\.\d+)?)'
            },
            'calculus': {
                'derivative': r'(d/dx|derivative of|differentiate)',
                'integral': r'(integral|integrate|∫)',
                'limit': r'limit\s*as\s*x\s*approaches|lim\s*x\s*→',
                'function': r'f\s*\(\s*x\s*\)\s*=|y\s*='
            },
            'geometry': {
                'area': r'area\s*of|A\s*=',
                'volume': r'volume\s*of|V\s*=',
                'perimeter': r'perimeter\s*of|P\s*=',
                'angle': r'angle|degrees?|°',
                'triangle': r'triangle|Δ',
                'circle': r'circle|radius|circumference|π'
            },
            'statistics': {
                'mean': r'average|mean|μ',
                'median': r'median',
                'mode': r'mode',
                'standard_deviation': r'standard deviation|σ',
                'probability': r'probability|chance|P\s*\(',
                'distribution': r'distribution|bell curve|normal'
            }
        }
        
        # Mathematical reasoning strategies
        self.reasoning_strategies = {
            'problem_decomposition': [
                'Break complex problems into smaller steps',
                'Identify what is given and what needs to be found',
                'Look for patterns and relationships',
                'Use systematic approaches'
            ],
            'algebraic_manipulation': [
                'Isolate variables step by step',
                'Use inverse operations',
                'Maintain equation balance',
                'Simplify expressions before solving'
            ],
            'geometric_reasoning': [
                'Visualize the problem',
                'Apply relevant formulas',
                'Use properties of shapes',
                'Check units and dimensions'
            ],
            'statistical_analysis': [
                'Examine data distribution',
                'Calculate central tendencies',
                'Consider variability',
                'Interpret results in context'
            ]
        }
        
        # Common mathematical knowledge
        self.math_knowledge = {
            'constants': {
                'pi': 3.14159265359,
                'e': 2.71828182846,
                'golden_ratio': 1.61803398875,
                'sqrt_2': 1.41421356237
            },
            'formulas': {
                'quadratic_formula': 'x = (-b ± √(b² - 4ac)) / 2a',
                'area_circle': 'A = πr²',
                'area_triangle': 'A = (1/2)bh',
                'pythagoras': 'a² + b² = c²',
                'distance_formula': 'd = √((x₂-x₁)² + (y₂-y₁)²)'
            },
            'sequences': {
                'fibonacci': [1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
                'primes': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
                'squares': [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                'cubes': [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
            }
        }
    
    def _define_wave_frequencies(self) -> Dict[str, float]:
        """Define wave frequencies for mathematical concepts."""
        return {
            # Arithmetic concepts
            'addition': 1.1,
            'subtraction': 1.2,
            'multiplication': 1.3,
            'division': 1.4,
            'percentage': 1.5,
            'fraction': 1.6,
            
            # Algebraic concepts
            'equation': 2.1,
            'variable': 2.2,
            'linear_equation': 2.3,
            'quadratic': 2.4,
            'exponent': 2.5,
            'logarithm': 2.6,
            'square_root': 2.7,
            
            # Geometric concepts
            'area': 3.1,
            'volume': 3.2,
            'perimeter': 3.3,
            'angle': 3.4,
            'triangle': 3.5,
            'circle': 3.6,
            
            # Calculus concepts
            'derivative': 4.1,
            'integral': 4.2,
            'limit': 4.3,
            'function': 4.4,
            
            # Statistical concepts
            'mean': 5.1,
            'median': 5.2,
            'mode': 5.3,
            'standard_deviation': 5.4,
            'probability': 5.5,
            'distribution': 5.6,
            
            # Mathematical operations
            'calculation': 6.1,
            'solving': 6.2,
            'analysis': 6.3,
            'reasoning': 6.4,
            
            # Problem types
            'arithmetic_calculation': 7.1,
            'equation_solving': 7.2,
            'geometry_calculation': 7.3,
            'statistical_analysis': 7.4,
            'calculus_problem': 7.5
        }
    
    def can_handle(self, query: str, context: Dict[str, Any] = None) -> float:
        """Determine if this expert can handle the mathematical query."""
        query_lower = query.lower()
        
        # Check for explicit mathematical terms
        math_terms = [
            'calculate', 'solve', 'find', 'compute', 'equation', 'formula',
            'sum', 'difference', 'product', 'quotient', 'fraction', 'decimal',
            'algebra', 'calculus', 'geometry', 'statistics', 'probability',
            'derivative', 'integral', 'limit', 'function', 'graph',
            'area', 'volume', 'perimeter', 'angle', 'triangle', 'circle',
            'mean', 'median', 'mode', 'variance', 'distribution'
        ]
        
        mathematical_score = sum(1 for term in math_terms if term in query_lower)
        
        # Check for mathematical patterns
        pattern_score = 0
        for category, patterns in self.math_patterns.items():
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, query):
                    pattern_score += 1
        
        # Check for numbers and mathematical symbols
        number_score = len(re.findall(r'\d+(?:\.\d+)?', query)) * 0.1
        symbol_score = len(re.findall(r'[+\-*/=<>^√∫∑π]', query)) * 0.2
        
        # Context-based scoring
        context_score = 0
        if context:
            if context.get('type') == 'mathematics':
                context_score += 0.5
            if context.get('domain') == 'math':
                context_score += 0.3
        
        # Calculate final confidence
        total_score = (
            mathematical_score * 0.3 +
            pattern_score * 0.2 +
            number_score +
            symbol_score +
            context_score
        )
        
        return min(1.0, total_score)
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> ExpertResponse:
        """Process a mathematical query."""
        start_time = self._get_time()
        
        # Analyze the mathematical problem
        problem_analysis = self._analyze_mathematical_problem(query, context)
        
        # Generate mathematical reasoning
        reasoning = self._generate_mathematical_reasoning(problem_analysis, query, context)
        
        # Solve if possible
        solution = self._attempt_mathematical_solution(problem_analysis, query, context)
        
        # Calculate confidence
        confidence = self._calculate_math_confidence(problem_analysis, solution, query, context)
        
        # Generate wave patterns
        wave_patterns = self._generate_math_wave_patterns(problem_analysis, solution, query)
        
        # Create response
        response = ExpertResponse(
            confidence=confidence,
            reasoning=reasoning,
            answer=solution['answer'] if solution else 'Unable to solve',
            wave_patterns=wave_patterns,
            metadata={
                'problem_type': problem_analysis['type'],
                'mathematical_domain': problem_analysis['domain'],
                'difficulty': problem_analysis['difficulty'],
                'solution_steps': solution['steps'] if solution else [],
                'formulas_used': solution['formulas'] if solution else []
            },
            processing_time=self._get_time() - start_time
        )
        
        return response
    
    def _analyze_mathematical_problem(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze the mathematical problem structure."""
        analysis = {
            'type': 'unknown',
            'domain': 'general',
            'difficulty': 'medium',
            'components': [],
            'numbers': [],
            'operations': [],
            'variables': [],
            'keywords': []
        }
        
        # Extract numbers
        numbers = re.findall(r'\d+(?:\.\d+)?', query)
        analysis['numbers'] = [float(n) for n in numbers]
        
        # Extract operations
        operations = re.findall(r'[+\-*/=<>^√∫∑]', query)
        analysis['operations'] = operations
        
        # Extract variables
        variables = re.findall(r'\b[a-zA-Z]\b', query)
        analysis['variables'] = variables
        
        # Determine problem type
        query_lower = query.lower()
        
        if any(pattern in query_lower for pattern in ['solve', 'equation', 'find x', 'find y']):
            analysis['type'] = 'equation_solving'
            analysis['domain'] = 'algebra'
        elif any(pattern in query_lower for pattern in ['area', 'volume', 'perimeter', 'angle']):
            analysis['type'] = 'geometry_calculation'
            analysis['domain'] = 'geometry'
        elif any(pattern in query_lower for pattern in ['derivative', 'integral', 'limit']):
            analysis['type'] = 'calculus_problem'
            analysis['domain'] = 'calculus'
        elif any(pattern in query_lower for pattern in ['mean', 'average', 'probability', 'statistics']):
            analysis['type'] = 'statistical_analysis'
            analysis['domain'] = 'statistics'
        elif any(pattern in query_lower for pattern in ['calculate', 'compute', '+', '-', '*', '/']):
            analysis['type'] = 'arithmetic_calculation'
            analysis['domain'] = 'arithmetic'
        
        # Determine difficulty
        if len(analysis['numbers']) <= 2 and len(analysis['operations']) <= 2:
            analysis['difficulty'] = 'easy'
        elif len(analysis['numbers']) <= 5 and len(analysis['operations']) <= 4:
            analysis['difficulty'] = 'medium'
        else:
            analysis['difficulty'] = 'hard'
        
        return analysis
    
    def _generate_mathematical_reasoning(self, analysis: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> str:
        """Generate mathematical reasoning explanation."""
        reasoning_parts = []
        
        # Problem identification
        reasoning_parts.append(f"Mathematical Problem Analysis:")
        reasoning_parts.append(f"- Type: {analysis['type']}")
        reasoning_parts.append(f"- Domain: {analysis['domain']}")
        reasoning_parts.append(f"- Difficulty: {analysis['difficulty']}")
        
        # Strategy selection
        domain = analysis['domain']
        if domain in self.reasoning_strategies:
            strategies = self.reasoning_strategies[domain]
            reasoning_parts.append(f"- Strategy: {random.choice(strategies)}")
        
        # Number and operation analysis
        if analysis['numbers']:
            reasoning_parts.append(f"- Numbers involved: {analysis['numbers']}")
        if analysis['operations']:
            reasoning_parts.append(f"- Operations detected: {analysis['operations']}")
        if analysis['variables']:
            reasoning_parts.append(f"- Variables: {analysis['variables']}")
        
        # Domain-specific reasoning
        if domain == 'algebra':
            reasoning_parts.append("- Algebraic approach: Isolate variables using inverse operations")
        elif domain == 'geometry':
            reasoning_parts.append("- Geometric approach: Apply relevant formulas and properties")
        elif domain == 'calculus':
            reasoning_parts.append("- Calculus approach: Use differentiation/integration rules")
        elif domain == 'statistics':
            reasoning_parts.append("- Statistical approach: Analyze data distribution and central tendencies")
        
        return "\n".join(reasoning_parts)
    
    def _attempt_mathematical_solution(self, analysis: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Attempt to solve the mathematical problem."""
        try:
            problem_type = analysis['type']
            numbers = analysis['numbers']
            
            if problem_type == 'arithmetic_calculation':
                return self._solve_arithmetic(query, numbers)
            elif problem_type == 'equation_solving':
                return self._solve_equation(query, analysis)
            elif problem_type == 'geometry_calculation':
                return self._solve_geometry(query, analysis)
            elif problem_type == 'statistical_analysis':
                return self._solve_statistics(query, numbers)
            else:
                return self._general_math_solution(query, analysis)
                
        except Exception as e:
            return {
                'answer': f'Error in calculation: {str(e)}',
                'steps': [f'Calculation error: {str(e)}'],
                'formulas': []
            }
    
    def _solve_arithmetic(self, query: str, numbers: List[float]) -> Dict[str, Any]:
        """Solve basic arithmetic problems."""
        steps = []
        formulas = []
        
        if '+' in query and len(numbers) >= 2:
            result = sum(numbers)
            steps.append(f"Add all numbers: {' + '.join(map(str, numbers))} = {result}")
            return {'answer': str(result), 'steps': steps, 'formulas': formulas}
        
        if '-' in query and len(numbers) >= 2:
            result = numbers[0] - sum(numbers[1:])
            steps.append(f"Subtract: {numbers[0]} - {' - '.join(map(str, numbers[1:]))} = {result}")
            return {'answer': str(result), 'steps': steps, 'formulas': formulas}
        
        if '*' in query or '×' in query and len(numbers) >= 2:
            result = 1
            for num in numbers:
                result *= num
            steps.append(f"Multiply: {' × '.join(map(str, numbers))} = {result}")
            return {'answer': str(result), 'steps': steps, 'formulas': formulas}
        
        if '/' in query or '÷' in query and len(numbers) >= 2:
            result = numbers[0]
            for num in numbers[1:]:
                if num != 0:
                    result /= num
            steps.append(f"Divide: {numbers[0]} ÷ {' ÷ '.join(map(str, numbers[1:]))} = {result}")
            return {'answer': str(result), 'steps': steps, 'formulas': formulas}
        
        return {'answer': 'Cannot solve arithmetic problem', 'steps': steps, 'formulas': formulas}
    
    def _solve_equation(self, query: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Solve algebraic equations."""
        steps = []
        formulas = []
        
        # Simple linear equation pattern: ax + b = c
        linear_match = re.search(r'(\d*)\s*x\s*([+-])\s*(\d+)\s*=\s*(\d+)', query)
        if linear_match:
            a = int(linear_match.group(1)) if linear_match.group(1) else 1
            sign = linear_match.group(2)
            b = int(linear_match.group(3))
            c = int(linear_match.group(4))
            
            if sign == '+':
                # ax + b = c -> x = (c - b) / a
                x = (c - b) / a
                steps.append(f"Starting equation: {a}x + {b} = {c}")
                steps.append(f"Subtract {b} from both sides: {a}x = {c - b}")
                steps.append(f"Divide by {a}: x = {x}")
            else:
                # ax - b = c -> x = (c + b) / a
                x = (c + b) / a
                steps.append(f"Starting equation: {a}x - {b} = {c}")
                steps.append(f"Add {b} to both sides: {a}x = {c + b}")
                steps.append(f"Divide by {a}: x = {x}")
            
            formulas.append("Linear equation: ax + b = c")
            return {'answer': f'x = {x}', 'steps': steps, 'formulas': formulas}
        
        return {'answer': 'Cannot solve this equation', 'steps': steps, 'formulas': formulas}
    
    def _solve_geometry(self, query: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Solve geometry problems."""
        steps = []
        formulas = []
        numbers = analysis['numbers']
        
        if 'area' in query.lower():
            if 'circle' in query.lower() and len(numbers) >= 1:
                # Area of circle: A = πr²
                radius = numbers[0]
                area = math.pi * radius ** 2
                steps.append(f"Formula: A = πr²")
                steps.append(f"Given radius: r = {radius}")
                steps.append(f"Area = π × {radius}² = {area:.2f}")
                formulas.append("Area of circle: A = πr²")
                return {'answer': f'{area:.2f}', 'steps': steps, 'formulas': formulas}
            
            elif 'triangle' in query.lower() and len(numbers) >= 2:
                # Area of triangle: A = (1/2)bh
                base = numbers[0]
                height = numbers[1]
                area = 0.5 * base * height
                steps.append(f"Formula: A = (1/2)bh")
                steps.append(f"Given base: b = {base}, height: h = {height}")
                steps.append(f"Area = (1/2) × {base} × {height} = {area}")
                formulas.append("Area of triangle: A = (1/2)bh")
                return {'answer': f'{area}', 'steps': steps, 'formulas': formulas}
        
        return {'answer': 'Cannot solve this geometry problem', 'steps': steps, 'formulas': formulas}
    
    def _solve_statistics(self, query: str, numbers: List[float]) -> Dict[str, Any]:
        """Solve statistics problems."""
        steps = []
        formulas = []
        
        if 'mean' in query.lower() or 'average' in query.lower():
            mean = sum(numbers) / len(numbers)
            steps.append(f"Numbers: {numbers}")
            steps.append(f"Mean = (sum of all numbers) / (count of numbers)")
            steps.append(f"Mean = {sum(numbers)} / {len(numbers)} = {mean}")
            formulas.append("Mean = Σx / n")
            return {'answer': f'{mean}', 'steps': steps, 'formulas': formulas}
        
        if 'median' in query.lower():
            sorted_numbers = sorted(numbers)
            n = len(sorted_numbers)
            if n % 2 == 0:
                median = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
            else:
                median = sorted_numbers[n//2]
            steps.append(f"Sorted numbers: {sorted_numbers}")
            steps.append(f"Median = middle value = {median}")
            formulas.append("Median = middle value when sorted")
            return {'answer': f'{median}', 'steps': steps, 'formulas': formulas}
        
        return {'answer': 'Cannot solve this statistics problem', 'steps': steps, 'formulas': formulas}
    
    def _general_math_solution(self, query: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """General mathematical solution attempt."""
        steps = []
        formulas = []
        
        # Try to evaluate simple expressions
        try:
            # Clean the query for evaluation
            cleaned_query = re.sub(r'[^\d+\-*/().\s]', '', query)
            if cleaned_query.strip():
                result = eval(cleaned_query)
                steps.append(f"Evaluating: {cleaned_query}")
                steps.append(f"Result: {result}")
                return {'answer': str(result), 'steps': steps, 'formulas': formulas}
        except:
            pass
        
        return {'answer': 'Cannot solve this mathematical problem', 'steps': steps, 'formulas': formulas}
    
    def _calculate_math_confidence(self, analysis: Dict[str, Any], solution: Optional[Dict[str, Any]], 
                                  query: str, context: Dict[str, Any] = None) -> float:
        """Calculate confidence in mathematical solution."""
        base_confidence = 0.5
        
        # Domain expertise confidence
        domain_confidence = {
            'arithmetic': 0.9,
            'algebra': 0.8,
            'geometry': 0.7,
            'statistics': 0.8,
            'calculus': 0.6
        }
        
        domain = analysis['domain']
        if domain in domain_confidence:
            base_confidence = domain_confidence[domain]
        
        # Adjust based on problem complexity
        difficulty = analysis['difficulty']
        if difficulty == 'easy':
            base_confidence += 0.1
        elif difficulty == 'hard':
            base_confidence -= 0.2
        
        # Adjust based on solution quality
        if solution:
            if solution['answer'] != 'Cannot solve' and 'Error' not in solution['answer']:
                base_confidence += 0.1
            if solution['steps']:
                base_confidence += 0.05
            if solution['formulas']:
                base_confidence += 0.05
        else:
            base_confidence -= 0.3
        
        return max(0.1, min(0.95, base_confidence))
    
    def _generate_math_wave_patterns(self, analysis: Dict[str, Any], solution: Optional[Dict[str, Any]], 
                                   query: str) -> Dict[str, float]:
        """Generate mathematical wave patterns."""
        patterns = {}
        
        # Domain-based patterns
        domain = analysis['domain']
        patterns[f'math_{domain}'] = 0.8
        
        # Problem type patterns
        problem_type = analysis['type']
        patterns[f'problem_{problem_type}'] = 0.7
        
        # Difficulty patterns
        difficulty = analysis['difficulty']
        patterns[f'difficulty_{difficulty}'] = 0.6
        
        # Solution patterns
        if solution:
            if 'Cannot solve' not in solution['answer']:
                patterns['solution_found'] = 0.9
                patterns['mathematical_success'] = 0.8
            else:
                patterns['solution_not_found'] = 0.8
                patterns['mathematical_challenge'] = 0.7
        
        # Number patterns
        if analysis['numbers']:
            patterns['numerical_analysis'] = 0.7
            if any(n > 100 for n in analysis['numbers']):
                patterns['large_numbers'] = 0.6
            if any(n < 1 for n in analysis['numbers']):
                patterns['small_numbers'] = 0.6
        
        # Operation patterns
        if analysis['operations']:
            patterns['mathematical_operations'] = 0.8
            for op in analysis['operations']:
                if op in ['+', '-']:
                    patterns['basic_arithmetic'] = 0.7
                elif op in ['*', '/']:
                    patterns['multiplication_division'] = 0.7
                elif op in ['^', '√']:
                    patterns['advanced_operations'] = 0.8
        
        return patterns
    
    def _get_time(self) -> float:
        """Get current time for performance tracking."""
        import time
        return time.time() 