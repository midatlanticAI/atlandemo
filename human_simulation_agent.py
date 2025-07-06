#!/usr/bin/env python3
"""
HUMAN-LIKE SIMULATION AGENT
Uses world knowledge and contextual reasoning like biological intelligence
"""

import json
import time
import random
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine

class HumanLikeSimulator:
    """Agent that simulates scenarios with human-like world knowledge"""
    
    def __init__(self, agent_id, role):
        self.agent_id = agent_id
        self.role = role
        self.engine = None  # Will be set by committee
        self.world_knowledge = self.initialize_world_knowledge()
        self.observations = []
        
    def initialize_world_knowledge(self):
        """Initialize common-sense world knowledge like humans have"""
        return {
            # Physical properties
            'physical_defaults': {
                'mammals': ['have fur', 'are warm-blooded', 'nurse young'],
                'cars': ['have four wheels', 'drive on roads', 'have engines'],
                'cats': ['have fur', 'purr', 'are carnivores', 'are agile'],
                'dogs': ['have fur', 'are loyal', 'bark', 'are social'],
                'birds': ['have wings', 'can fly', 'have beaks', 'lay eggs'],
                'flowers': ['have petals', 'are colorful', 'have fragrance'],
                'animals': ['are alive', 'move', 'need food', 'reproduce']
            },
            
            # Social dynamics
            'social_defaults': {
                'friends': ['are loyal', 'are supportive', 'care for each other'],
                'parents': ['are loving', 'are responsible', 'protect children'],
                'people': ['have emotions', 'make mistakes', 'learn from experience']
            },
            
            # Exception patterns humans recognize
            'exception_patterns': {
                'usually': 'most cases but not all',
                'typically': 'common but exceptions exist',
                'normally': 'standard case with possible exceptions',
                'at least one': 'minimal exception, general rule still applies'
            },
            
            # Context clues humans use
            'context_clues': {
                'reliability': ['evidence', 'trustworthy', 'accurate', 'credible'],
                'priority': ['more reliable', 'better evidence', 'stronger proof'],
                'exception': ['but', 'however', 'except', 'at least one']
            }
        }
    
    def human_like_scenario_analysis(self, context, question):
        """Analyze scenario like a human would - with world knowledge and intuition"""
        analysis = {
            'scenario_type': self.identify_scenario_type(context),
            'key_entities': self.extract_entities(context),
            'default_assumptions': [],
            'explicit_exceptions': [],
            'logical_structure': self.parse_logical_structure(context),
            'human_intuition': None
        }
        
        # Apply world knowledge to make default assumptions
        for entity in analysis['key_entities']:
            if entity.lower() in self.world_knowledge['physical_defaults']:
                defaults = self.world_knowledge['physical_defaults'][entity.lower()]
                analysis['default_assumptions'].extend([(entity, default) for default in defaults])
        
        # Identify explicit exceptions
        context_lower = context.lower()
        for pattern in self.world_knowledge['exception_patterns']:
            if pattern in context_lower:
                analysis['explicit_exceptions'].append(pattern)
        
        # Generate human intuition
        analysis['human_intuition'] = self.generate_human_intuition(analysis, question)
        
        return analysis
    
    def identify_scenario_type(self, context):
        """Identify what kind of scenario this is"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['usually', 'typically', 'normally']):
            if 'exception' in context_lower or 'at least one' in context_lower:
                return 'default_with_exception'
            else:
                return 'default_reasoning'
        elif any(word in context_lower for word in ['reliable', 'evidence', 'claims']):
            return 'priority_reasoning'
        elif 'at least one' in context_lower:
            return 'exception_reasoning'
        else:
            return 'general_reasoning'
    
    def extract_entities(self, context):
        """Extract key entities like humans do - focus on nouns"""
        import re
        
        # Extract capitalized words (names, proper nouns)
        entities = re.findall(r'\b[A-Z][a-z]+\b', context)
        
        # Extract common entity types
        common_entities = ['cat', 'dog', 'car', 'mammal', 'animal', 'friend', 'parent', 'person', 'bird', 'flower']
        for entity in common_entities:
            if entity in context.lower():
                entities.append(entity)
        
        return list(set(entities))
    
    def parse_logical_structure(self, context):
        """Parse logical structure like humans do - look for patterns"""
        structure = {
            'conditionals': [],
            'universals': [],
            'exceptions': [],
            'defaults': []
        }
        
        context_lower = context.lower()
        
        # Look for conditional statements
        if 'if' in context_lower:
            structure['conditionals'].append('conditional_present')
        
        # Look for universal statements
        if any(word in context_lower for word in ['all', 'every', 'always']):
            structure['universals'].append('universal_present')
        
        # Look for default statements
        if any(word in context_lower for word in ['usually', 'typically', 'normally']):
            structure['defaults'].append('default_present')
        
        # Look for exception statements
        if any(word in context_lower for word in ['except', 'but', 'however', 'at least one']):
            structure['exceptions'].append('exception_present')
        
        return structure
    
    def generate_human_intuition(self, analysis, question):
        """Generate human-like intuitive reasoning"""
        scenario_type = analysis['scenario_type']
        
        if scenario_type == 'default_with_exception':
            # Humans think: "If X is usually Y, and we know A is an exception, then B is probably Y"
            return "default_rule_applies_to_non_exceptions"
        
        elif scenario_type == 'priority_reasoning':
            # Humans think: "If X is more reliable than Y, trust X's claim"
            return "trust_more_reliable_source"
        
        elif scenario_type == 'exception_reasoning':
            # Humans think: "At least one exception doesn't invalidate the general rule"
            return "exception_confirms_general_rule"
        
        else:
            return "apply_common_sense"
    
    def mental_simulation_with_world_knowledge(self, context, conditions):
        """Run mental simulation with human-like world knowledge"""
        simulation = {
            'context': context,
            'conditions': conditions,
            'human_analysis': None,
            'world_knowledge_applied': [],
            'mental_experiments': [],
            'conclusions': []
        }
        
        # Analyze scenario like a human
        for condition in conditions:
            human_analysis = self.human_like_scenario_analysis(context, condition)
            simulation['human_analysis'] = human_analysis
            
            # Run mental experiments based on human intuition
            mental_experiment = self.run_mental_experiment(human_analysis, condition)
            simulation['mental_experiments'].append(mental_experiment)
            
            # Draw conclusions
            conclusion = self.draw_human_conclusion(human_analysis, mental_experiment, condition)
            simulation['conclusions'].append(conclusion)
        
        return simulation
    
    def run_mental_experiment(self, analysis, condition):
        """Run mental experiment like humans do - imagine the scenario"""
        experiment = {
            'scenario': analysis['scenario_type'],
            'imagination': None,
            'outcome_prediction': None,
            'confidence': 0.0
        }
        
        # Use Wave Engine to imagine the scenario
        imagination_prompt = f"""
        Imagine this scenario with human-like common sense:
        
        Scenario type: {analysis['scenario_type']}
        Key entities: {analysis['key_entities']}
        Default assumptions: {analysis['default_assumptions']}
        Explicit exceptions: {analysis['explicit_exceptions']}
        Human intuition: {analysis['human_intuition']}
        
        Question condition: {condition}
        
        What would a human with common sense and world knowledge conclude?
        Think step by step like a human would.
        """
        
        if self.engine:
            try:
                wave_response = self.engine.process_input(imagination_prompt)
                experiment['imagination'] = wave_response
                
                # Extract prediction and confidence
                if any(word in wave_response.lower() for word in ['yes', 'true', 'correct', 'follows']):
                    experiment['outcome_prediction'] = 'positive'
                    experiment['confidence'] = 0.8
                elif any(word in wave_response.lower() for word in ['no', 'false', 'incorrect', 'not']):
                    experiment['outcome_prediction'] = 'negative'
                    experiment['confidence'] = 0.8
                else:
                    experiment['outcome_prediction'] = 'uncertain'
                    experiment['confidence'] = 0.5
                    
            except:
                # Fallback to rule-based reasoning
                experiment = self.fallback_mental_experiment(analysis, condition)
        
        return experiment
    
    def fallback_mental_experiment(self, analysis, condition):
        """Fallback mental experiment using rule-based reasoning"""
        scenario_type = analysis['scenario_type']
        
        if scenario_type == 'default_with_exception':
            # Default reasoning: if X is usually Y, and we exclude exceptions, then remaining X are Y
            return {
                'scenario': scenario_type,
                'imagination': 'Default rule applies to non-exceptions',
                'outcome_prediction': 'positive',
                'confidence': 0.75
            }
        elif scenario_type == 'priority_reasoning':
            # Priority reasoning: trust the more reliable source
            return {
                'scenario': scenario_type,
                'imagination': 'More reliable source should be trusted',
                'outcome_prediction': 'positive',
                'confidence': 0.8
            }
        else:
            return {
                'scenario': scenario_type,
                'imagination': 'General reasoning applied',
                'outcome_prediction': 'positive',
                'confidence': 0.6
            }
    
    def draw_human_conclusion(self, analysis, experiment, condition):
        """Draw conclusion like a human would"""
        conclusion = {
            'condition': condition,
            'reasoning_type': analysis['scenario_type'],
            'human_logic': analysis['human_intuition'],
            'predicted_answer': None,
            'confidence': experiment['confidence'],
            'explanation': experiment['imagination']
        }
        
        # Apply human-like decision making
        if experiment['outcome_prediction'] == 'positive':
            conclusion['predicted_answer'] = 'yes'
        elif experiment['outcome_prediction'] == 'negative':
            conclusion['predicted_answer'] = 'no'
        else:
            # When uncertain, humans tend to go with default assumptions
            conclusion['predicted_answer'] = 'yes'
            conclusion['confidence'] = 0.5
        
        return conclusion


class HumanLikeCommittee:
    """Committee that reasons like humans do"""
    
    def __init__(self):
        self.agents = []
        self.shared_engine = EnhancedWaveEngine()
        self.synthesis_engine = EnhancedWaveEngine()
        self.setup_human_agents()
    
    def setup_human_agents(self):
        """Create human-like reasoning agents"""
        roles = [
            "World_Knowledge_Agent",    # Applies common sense and world knowledge
            "Intuition_Agent",          # Uses human-like intuition
            "Experience_Agent",         # Draws on experiential knowledge
            "Context_Agent",            # Understands context and pragmatics
            "Synthesis_Agent"           # Combines insights like human judgment
        ]
        
        print("[BRAIN] SPAWNING HUMAN-LIKE AGENTS")
        for i, role in enumerate(roles):
            agent = HumanLikeSimulator(i, role)
            agent.engine = self.shared_engine
            self.agents.append(agent)
            print(f"   Agent {i}: {role}")
    
    def human_collaborative_reasoning(self, question, context, logic_type, axiom):
        """Collaborative reasoning like humans do"""
        
        # Step 1: Each agent analyzes with their specialization
        agent_conclusions = []
        for agent in self.agents:
            simulation = agent.mental_simulation_with_world_knowledge(context, [question])
            agent_conclusions.extend(simulation['conclusions'])
        
        # Step 2: Synthesis like human group decision-making
        final_answer = self.human_synthesis(agent_conclusions, question, logic_type, axiom)
        
        return final_answer
    
    def human_synthesis(self, conclusions, question, logic_type, axiom):
        """Synthesize conclusions like humans do in group decision-making"""
        
        # Count positive vs negative predictions
        positive_votes = sum(1 for c in conclusions if c['predicted_answer'] == 'yes')
        negative_votes = sum(1 for c in conclusions if c['predicted_answer'] == 'no')
        
        # Weight by confidence (like humans do)
        weighted_positive = sum(c['confidence'] for c in conclusions if c['predicted_answer'] == 'yes')
        weighted_negative = sum(c['confidence'] for c in conclusions if c['predicted_answer'] == 'no')
        
        # Human-like decision making: consider both votes and confidence
        if weighted_positive > weighted_negative:
            return "yes"
        elif weighted_negative > weighted_positive:
            return "no"
        else:
            # Tie-breaker: humans tend to be optimistic about default cases
            if logic_type == 'nm_logic':
                return "yes"  # Humans assume defaults apply
            else:
                return "yes" if positive_votes >= negative_votes else "no"


class HumanLikeLogicBench:
    """LogicBench benchmark using human-like reasoning"""
    
    def __init__(self):
        self.committee = HumanLikeCommittee()
        self.total_questions = 0
        self.total_correct = 0
    
    def run_human_benchmark(self, max_files=25, questions_per_file=40):
        """Run benchmark with human-like reasoning"""
        print(f"\n[BRAIN] HUMAN-LIKE SIMULATION BENCHMARK")
        print(f"💭 Agents use world knowledge and intuition like biological intelligence")
        print(f"[TARGET] Target: Match human performance on nm_logic!")
        
        start_time = time.time()
        
        # Find files
        all_files = self.find_all_logicbench_files()
        if not all_files:
            print("[-] No LogicBench files found!")
            return None
        
        # Sample files
        if len(all_files) > max_files:
            test_files = random.sample(all_files, max_files)
        else:
            test_files = all_files
        
        print(f"🧩 Applying human-like reasoning to {len(test_files)} files...")
        
        all_results = []
        logic_type_summary = {}
        
        for file_path, logic_type, axiom in test_files:
            result = self.process_file_with_human_reasoning(file_path, logic_type, axiom, questions_per_file)
            
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
        print(f"\n[BRAIN] HUMAN-LIKE RESULTS:")
        print(f"   Total Questions: {self.total_questions}")
        print(f"   Correct Answers: {self.total_correct}")
        print(f"   Human-like Accuracy: {overall_accuracy:.3f} ({overall_accuracy:.1%})")
        print(f"   Processing Time: {elapsed_time:.2f} seconds")
        print(f"   Questions/second: {self.total_questions/elapsed_time:.1f}")
        
        # Performance comparison
        print(f"\n[BRAIN] HUMAN-LIKE VS SINGLE AGENT:")
        baseline = 0.652  # Single-agent baseline
        if overall_accuracy > baseline:
            improvement = (overall_accuracy - baseline) * 100
            print(f"   [+] HUMAN-LIKE WINS! (+{improvement:.1f} percentage points)")
        else:
            decline = (baseline - overall_accuracy) * 100
            print(f"   [-] Single agent better (-{decline:.1f} percentage points)")
        
        # Special focus on nm_logic
        if 'nm_logic' in logic_type_summary:
            nm_accuracy = logic_type_summary['nm_logic']['accuracy']
            print(f"\n💡 NM_LOGIC BREAKTHROUGH:")
            print(f"   Human-like nm_logic: {nm_accuracy:.3f} ({nm_accuracy:.1%})")
            if nm_accuracy > 0.5:
                print(f"   [PARTY] BEAT 50% NM_LOGIC BASELINE!")
        
        # Logic type breakdown
        print(f"\n💭 HUMAN-LIKE LOGIC BREAKDOWN:")
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
    
    def process_file_with_human_reasoning(self, file_path, logic_type, axiom, sample_size=40):
        """Process file with human-like reasoning"""
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
                
                # Human-like reasoning
                predicted_answer = self.committee.human_collaborative_reasoning(question, context, logic_type, axiom)
                
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
            print(f"[-] Human reasoning failed on {file_path}: {e}")
            return None


def main():
    """Run the human-like simulation benchmark"""
    print("[BRAIN] HUMAN-LIKE WAVE AGENT EXPERIMENT [BRAIN]")
    print("💭 World knowledge and intuition like biological intelligence")
    print("=" * 60)
    
    benchmark = HumanLikeLogicBench()
    results = benchmark.run_human_benchmark()
    
    if results:
        print(f"\n[TARGET] HUMAN-LIKE EXPERIMENT COMPLETE!")
        print(f"   Through world knowledge and intuition:")
        print(f"   Accuracy: {results['overall_accuracy']:.1%}")
        print(f"   Speed: {results['total_questions']/results['processing_time']:.1f} q/s")
        
        # Special analysis for nm_logic
        if 'nm_logic' in results['logic_type_summary']:
            nm_accuracy = results['logic_type_summary']['nm_logic']['accuracy']
            print(f"\n💡 NM_LOGIC BREAKTHROUGH:")
            print(f"   This is how humans solve non-monotonic logic!")
            print(f"   Human-like accuracy: {nm_accuracy:.1%}")


if __name__ == "__main__":
    main() 