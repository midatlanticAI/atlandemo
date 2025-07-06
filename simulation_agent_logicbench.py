#!/usr/bin/env python3
"""
SIMULATION-BASED WAVE AGENT SYSTEM
Agents that mentally model and observe scenarios
"""

import json
import time
import random
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine

class ScenarioSimulator:
    """Agent that can simulate logical scenarios and observe outcomes"""
    
    def __init__(self, agent_id, role):
        self.agent_id = agent_id
        self.role = role
        self.engine = None  # Will be set by committee
        self.observations = []
        
    def simulate_scenario(self, context, conditions):
        """Mentally simulate a scenario and observe what happens"""
        simulation = {
            'context': context,
            'conditions': conditions,
            'outcomes': [],
            'contradictions': [],
            'possibilities': []
        }
        
        # Parse the scenario from context
        scenario_elements = self.extract_scenario_elements(context)
        
        # Run mental simulation
        for condition in conditions:
            outcome = self.imagine_outcome(scenario_elements, condition)
            simulation['outcomes'].append(outcome)
            
            # Check for contradictions
            contradiction = self.check_contradiction(scenario_elements, condition, outcome)
            if contradiction:
                simulation['contradictions'].append(contradiction)
        
        self.observations.append(simulation)
        return simulation
    
    def extract_scenario_elements(self, context):
        """Extract key elements from the scenario"""
        import re
        
        elements = {
            'characters': [],
            'actions': [],
            'conditions': [],
            'relationships': []
        }
        
        context_lower = context.lower()
        
        # Extract characters (basic name detection)
        names = re.findall(r'\b[A-Z][a-z]+\b', context)
        elements['characters'] = list(set(names))
        
        # Extract conditional relationships
        if 'if' in context_lower and 'then' in context_lower:
            elements['relationships'].append('conditional')
        
        # Extract actions
        action_words = ['go', 'buy', 'eat', 'drink', 'take', 'leave', 'stay', 'work', 'sleep']
        for word in action_words:
            if word in context_lower:
                elements['actions'].append(word)
        
        return elements
    
    def imagine_outcome(self, scenario_elements, condition):
        """Imagine what would happen given a condition"""
        # This is where the "mental simulation" happens using Wave Engine
        outcome = {
            'condition': condition,
            'predicted_result': None,
            'confidence': 0.0,
            'reasoning': ""
        }
        
        # Use Wave Engine to simulate the scenario
        simulation_prompt = f"""
        Imagine this scenario with these elements:
        Characters: {scenario_elements.get('characters', [])}
        Actions: {scenario_elements.get('actions', [])}
        Relationships: {scenario_elements.get('relationships', [])}
        
        Now imagine what happens when: {condition}
        
        What would you predict occurs?
        """
        
        try:
            # Get Wave Engine's prediction
            wave_response = self.engine.process_input(simulation_prompt)
            
            # Extract confidence and reasoning from Wave response
            if 'yes' in wave_response.lower() or 'true' in wave_response.lower() or 'follows' in wave_response.lower():
                outcome['predicted_result'] = 'consequent_follows'
                outcome['confidence'] = 0.75
            elif 'no' in wave_response.lower() or 'false' in wave_response.lower() or 'not' in wave_response.lower():
                outcome['predicted_result'] = 'no_consequence'  
                outcome['confidence'] = 0.75
            else:
                outcome['predicted_result'] = 'uncertain'
                outcome['confidence'] = 0.5
                
            outcome['reasoning'] = wave_response[:100]  # Truncate for brevity
            
        except:
            # Fallback to simple logic if Wave Engine fails
            if 'conditional' in scenario_elements.get('relationships', []):
                if self.condition_matches_antecedent(condition, scenario_elements):
                    outcome['predicted_result'] = 'consequent_follows'
                    outcome['confidence'] = 0.6
                    outcome['reasoning'] = "Conditional logic suggests consequent should follow"
                else:
                    outcome['predicted_result'] = 'no_consequence'
                    outcome['confidence'] = 0.6
                    outcome['reasoning'] = "Antecedent not met, no forced consequence"
        
        return outcome
    
    def condition_matches_antecedent(self, condition, elements):
        """Check if condition matches the antecedent of a conditional"""
        # Simplified matching logic
        return any(action in condition.lower() for action in elements.get('actions', []))
    
    def check_contradiction(self, scenario_elements, condition, outcome):
        """Check if the imagined outcome contradicts known facts"""
        # Look for logical contradictions
        contradictions = []
        
        # Example: If we predict something should happen but it doesn't
        if outcome['predicted_result'] == 'consequent_follows':
            # Check against negative statements in condition
            if any(neg in condition.lower() for neg in ['not', "didn't", "doesn't", "won't"]):
                contradictions.append({
                    'type': 'logical_contradiction',
                    'description': 'Predicted outcome contradicts stated fact'
                })
        
        return contradictions[0] if contradictions else None


class SimulationBasedCommittee:
    """Committee of agents that simulate scenarios and observe outcomes"""
    
    def __init__(self):
        self.agents = []
        self.shared_engine = EnhancedWaveEngine()  # Shared Wave Engine
        self.synthesis_engine = EnhancedWaveEngine()  # Separate synthesis engine
        self.setup_specialized_agents()
    
    def setup_specialized_agents(self):
        """Create specialized simulation agents"""
        roles = [
            "Scenario_Modeler",      # Models the initial scenario
            "Condition_Tester",      # Tests different conditions
            "Outcome_Observer",      # Observes what happens
            "Contradiction_Checker", # Looks for logical inconsistencies
            "Logic_Validator"        # Validates overall logical flow
        ]
        
        print("🧠 SPAWNING SIMULATION AGENTS")
        for i, role in enumerate(roles):
            agent = ScenarioSimulator(i, role)
            agent.engine = self.shared_engine  # Share engine instead of creating new ones
            self.agents.append(agent)
            print(f"   Agent {i}: {role}")
    
    def collaborative_reasoning(self, question, context, logic_type, axiom):
        """Have agents collaboratively simulate and reason about the scenario"""
        
        # Step 1: Model the scenario
        modeler = self.agents[0]  # Scenario_Modeler
        scenario_elements = modeler.extract_scenario_elements(context)
        
        # Step 2: Extract conditions from the question
        conditions = self.extract_question_conditions(question)
        
        # Step 3: Each agent simulates their part
        simulations = []
        for agent in self.agents[1:4]:  # Condition_Tester, Outcome_Observer, Contradiction_Checker
            sim = agent.simulate_scenario(context, conditions)
            simulations.append(sim)
        
        # Step 4: Logic validator makes final decision
        validator = self.agents[4]  # Logic_Validator
        final_answer = self.synthesize_observations(simulations, question, logic_type, axiom, self.synthesis_engine)
        
        return final_answer
    
    def extract_question_conditions(self, question):
        """Extract testable conditions from the question"""
        import re
        
        conditions = []
        question_lower = question.lower()
        
        # For entailment questions
        if 'entail' in question_lower or 'imply' in question_lower:
            # Extract what's being tested for entailment
            # Look for "that X" patterns
            that_match = re.search(r'that (.+?)(?:\?|$)', question_lower)
            if that_match:
                conditions.append(that_match.group(1))
        
        # For bidirectional dilemma questions
        if 'at least one' in question_lower:
            # Extract the options being tested
            options_match = re.search(r'\(a\)\s*([^)]+?)\s*(?:and|\.)\s*\(b\)\s*([^)]+?)(?:\?|$)', question)
            if options_match:
                conditions.append(options_match.group(1))
                conditions.append(options_match.group(2))
        
        return conditions if conditions else ['default_condition']
    
    def synthesize_observations(self, simulations, question, logic_type, axiom, synthesis_engine):
        """Synthesize all observations into a final answer using Wave Engine"""
        self.synthesis_engine = synthesis_engine
        
        # Prepare synthesis prompt for Wave Engine
        synthesis_prompt = f"""
        Based on these simulation observations:
        
        Question: {question}
        Logic Type: {logic_type}
        Axiom: {axiom}
        
        Observations from mental simulations:
        """
        
        # Add simulation details
        total_contradictions = sum(len(sim['contradictions']) for sim in simulations)
        positive_outcomes = 0
        negative_outcomes = 0
        
        for i, sim in enumerate(simulations):
            synthesis_prompt += f"\n  Simulation {i+1}: {len(sim['outcomes'])} outcomes"
            for outcome in sim['outcomes']:
                if outcome['predicted_result'] == 'consequent_follows':
                    positive_outcomes += 1
                    synthesis_prompt += f"\n    - Predicted: follows ({outcome['confidence']:.1f} confidence)"
                else:
                    negative_outcomes += 1
                    synthesis_prompt += f"\n    - Predicted: no consequence ({outcome['confidence']:.1f} confidence)"
        
        if total_contradictions > 0:
            synthesis_prompt += f"\n  Found {total_contradictions} logical contradictions"
        
        synthesis_prompt += f"\n\nBased on these observations, what should the answer be? Answer only 'yes' or 'no'."
        
        # Let Wave Engine make the final decision
        try:
            # Use the shared synthesis engine
            wave_decision = self.synthesis_engine.process_input(synthesis_prompt)
            
            # Extract yes/no from Wave response
            if 'yes' in wave_decision.lower():
                return "yes"
            elif 'no' in wave_decision.lower():
                return "no"
            else:
                # Fallback to observation-based logic
                return self.fallback_synthesis(simulations, question, logic_type, axiom)
                
        except:
            # Fallback if Wave Engine fails
            return self.fallback_synthesis(simulations, question, logic_type, axiom)
    
    def fallback_synthesis(self, simulations, question, logic_type, axiom):
        """Fallback synthesis logic if Wave Engine synthesis fails"""
        # Count contradictions found
        total_contradictions = sum(len(sim['contradictions']) for sim in simulations)
        
        # Count positive vs negative outcomes
        positive_outcomes = 0
        negative_outcomes = 0
        
        for sim in simulations:
            for outcome in sim['outcomes']:
                if outcome['predicted_result'] == 'consequent_follows':
                    positive_outcomes += 1
                else:
                    negative_outcomes += 1
        
        # Decision logic based on observations
        if total_contradictions > 0:
            # If we observed contradictions, the answer is usually "no" for entailment
            return "no"
        
        # For bidirectional dilemma, if we can imagine scenarios where both could be false
        if 'at least one' in question.lower():
            # If simulations show both conditions can realistically happen, answer "yes"
            if positive_outcomes >= negative_outcomes:
                return "yes"
            else:
                return "no"
        
        # For entailment questions, if simulation supports the conclusion
        if 'entail' in question.lower() or 'imply' in question.lower():
            # Check if simulations consistently support the entailment
            has_negation = any(neg in question.lower() for neg in ['not', "don't", "doesn't", "won't"])
            
            if positive_outcomes > negative_outcomes:
                return "no" if has_negation else "yes"
            else:
                return "yes" if has_negation else "no"
        
        # Default fallback
        return "yes" if positive_outcomes >= negative_outcomes else "no"


class SimulationLogicBench:
    """LogicBench benchmark using simulation-based reasoning"""
    
    def __init__(self):
        self.committee = SimulationBasedCommittee()
        self.total_questions = 0
        self.total_correct = 0
    
    def run_simulation_benchmark(self, max_files=25, questions_per_file=40):
        """Run benchmark with simulation-based reasoning"""
        print(f"\n🎭 SIMULATION-BASED LOGICBENCH BENCHMARK")
        print(f"💭 Agents mentally simulate scenarios and observe outcomes")
        print(f"🎯 Target: Beat 65% through imagination and observation!")
        
        start_time = time.time()
        
        # Find files
        all_files = self.find_all_logicbench_files()
        if not all_files:
            print("❌ No LogicBench files found!")
            return None
        
        # Sample files
        if len(all_files) > max_files:
            test_files = random.sample(all_files, max_files)
        else:
            test_files = all_files
        
        print(f"🧩 Simulating scenarios from {len(test_files)} files...")
        
        all_results = []
        logic_type_summary = {}
        
        for file_path, logic_type, axiom in test_files:
            result = self.process_file_with_simulation(file_path, logic_type, axiom, questions_per_file)
            
            if result:
                all_results.append(result)
                self.total_questions += result['total_questions']
                self.total_correct += result['correct_answers']
                
                # Track by logic type
                if logic_type not in logic_type_summary:
                    logic_type_summary[logic_type] = {'total_questions': 0, 'correct_answers': 0}
                
                logic_type_summary[logic_type]['total_questions'] += result['total_questions']
                logic_type_summary[logic_type]['correct_answers'] += result['correct_answers']
        
        # Calculate accuracies
        for logic_type in logic_type_summary:
            total = logic_type_summary[logic_type]['total_questions']
            correct = logic_type_summary[logic_type]['correct_answers']
            logic_type_summary[logic_type]['accuracy'] = correct / total if total > 0 else 0
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        overall_accuracy = self.total_correct / self.total_questions if self.total_questions > 0 else 0
        
        # Print results
        print(f"\n🎭 SIMULATION RESULTS:")
        print(f"   Total Questions: {self.total_questions}")
        print(f"   Correct Answers: {self.total_correct}")
        print(f"   Simulation Accuracy: {overall_accuracy:.3f} ({overall_accuracy:.1%})")
        print(f"   Processing Time: {elapsed_time:.2f} seconds")
        print(f"   Questions/second: {self.total_questions/elapsed_time:.1f}")
        
        # Performance comparison
        print(f"\n🧠 SIMULATION VS SINGLE AGENT:")
        baseline = 0.652  # Single-agent baseline
        if overall_accuracy > baseline:
            improvement = (overall_accuracy - baseline) * 100
            print(f"   ✅ SIMULATION WINS! (+{improvement:.1f} percentage points)")
        else:
            decline = (baseline - overall_accuracy) * 100
            print(f"   ❌ Single agent better (-{decline:.1f} percentage points)")
        
        if overall_accuracy > 0.69:
            print(f"   🎉 BEAT 69% BENCHMARK!")
        
        # Logic type breakdown
        print(f"\n💭 SIMULATION LOGIC BREAKDOWN:")
        for logic_type, summary in logic_type_summary.items():
            accuracy = summary['accuracy']
            print(f"   {logic_type}: {accuracy:.3f} ({accuracy:.1%})")
        
        return {
            'overall_accuracy': overall_accuracy,
            'total_questions': self.total_questions,
            'total_correct': self.total_correct,
            'processing_time': elapsed_time,
            'logic_type_summary': logic_type_summary
        }
    
    def find_all_logicbench_files(self):
        """Find all LogicBench test files"""
        files = []
        base_path = Path("logicbench/LogicBench(Eval)/BQA")
        
        if not base_path.exists():
            return files
            
        for logic_type_dir in base_path.iterdir():
            if logic_type_dir.is_dir():
                logic_type = logic_type_dir.name
                for axiom_dir in logic_type_dir.iterdir():
                    if axiom_dir.is_dir():
                        axiom = axiom_dir.name
                        data_file = axiom_dir / "data_instances.json"
                        if data_file.exists():
                            files.append((str(data_file), logic_type, axiom))
        
        return files
    
    def process_file_with_simulation(self, file_path, logic_type, axiom, sample_size=40):
        """Process file with simulation-based reasoning"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract questions
            all_qa_pairs = []
            samples = data.get('samples', [])
            
            for sample in samples:
                context = sample.get('context', '')
                qa_pairs = sample.get('qa_pairs', [])
                
                for qa_pair in qa_pairs:
                    all_qa_pairs.append({
                        'context': context,
                        'question': qa_pair.get('question', ''),
                        'answer': qa_pair.get('answer', '')
                    })
            
            # Sample questions
            if len(all_qa_pairs) > sample_size:
                sampled_data = random.sample(all_qa_pairs, sample_size)
            else:
                sampled_data = all_qa_pairs
            
            correct_count = 0
            
            for item in sampled_data:
                context = item['context']
                question = item['question']
                answer = item['answer']
                
                # Simulation-based reasoning
                predicted_answer = self.committee.collaborative_reasoning(question, context, logic_type, axiom)
                
                if predicted_answer.lower() == answer.lower():
                    correct_count += 1
            
            return {
                'logic_type': logic_type,
                'axiom': axiom,
                'total_questions': len(sampled_data),
                'correct_answers': correct_count,
                'accuracy': correct_count / len(sampled_data) if sampled_data else 0
            }
            
        except Exception as e:
            print(f"❌ Simulation failed on {file_path}: {e}")
            return None


def main():
    """Run the simulation-based benchmark"""
    print("🎭 WAVE AGENT SIMULATION EXPERIMENT 🎭")
    print("💭 Mental simulation and observation approach")
    print("=" * 60)
    
    benchmark = SimulationLogicBench()
    results = benchmark.run_simulation_benchmark()
    
    if results:
        print(f"\n🎯 SIMULATION EXPERIMENT COMPLETE!")
        print(f"   Through mental simulation and observation:")
        print(f"   Accuracy: {results['overall_accuracy']:.1%}")
        print(f"   Speed: {results['total_questions']/results['processing_time']:.1f} q/s")


if __name__ == "__main__":
    main() 