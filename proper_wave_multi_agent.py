#!/usr/bin/env python3
"""
PROPER WAVE-BASED MULTI-AGENT SYSTEM
Actually uses Wave Engine for cognitive processing instead of shortcuts
"""

import json
import time
import random
from pathlib import Path
from enhanced_wave_engine import EnhancedWaveEngine
from expert_modules.registry import ExpertRegistry

class WaveBasedAgent:
    """Agent that actually uses Wave Engine for cognitive processing"""
    
    def __init__(self, agent_id, specialization, shared_registry=None):
        self.agent_id = agent_id
        self.specialization = specialization
        self.wave_engine = EnhancedWaveEngine()
        self.expert_registry = shared_registry or ExpertRegistry()
        self.memory = []
        self.expertise_area = self.get_expertise_area()
        
        # Initialize with specialization knowledge
        self.initialize_specialization()
        
    def get_expertise_area(self):
        """Define what this agent specializes in"""
        areas = {
            'logic_analyst': ['propositional_logic', 'first_order_logic', 'logical_structure'],
            'pattern_recognizer': ['pattern_detection', 'anomaly_detection', 'consistency_checking'],
            'context_interpreter': ['nm_logic', 'default_reasoning', 'exception_handling'],
            'wave_synthesizer': ['wave_interference', 'cognitive_synthesis', 'decision_integration'],
            'contradiction_detector': ['logical_inconsistency', 'conflict_resolution', 'truth_validation']
        }
        return areas.get(self.specialization, ['general_reasoning'])
    
    def initialize_specialization(self):
        """Initialize the agent with specialized knowledge using Wave Engine"""
        specialization_prompts = {
            'logic_analyst': """
            You are a logic analyst agent. Your wave patterns should resonate with:
            - Formal logical structures and rules
            - Propositional and first-order logic patterns
            - Syllogistic reasoning and inference chains
            Focus on detecting logical validity and structural correctness.
            """,
            'pattern_recognizer': """
            You are a pattern recognition agent. Your wave patterns should resonate with:
            - Recurring patterns and anomalies
            - Consistency across multiple instances
            - Structural similarities and differences
            Focus on detecting patterns that others might miss.
            """,
            'context_interpreter': """
            You are a context interpretation agent. Your wave patterns should resonate with:
            - Non-monotonic reasoning and defaults
            - Exception handling and priority reasoning
            - Contextual factors that modify logical conclusions
            Focus on understanding when general rules have exceptions.
            """,
            'wave_synthesizer': """
            You are a wave synthesis agent. Your wave patterns should resonate with:
            - Integrating multiple perspectives
            - Resolving conflicting information through wave interference
            - Synthesizing complex cognitive patterns
            Focus on combining insights from multiple sources.
            """,
            'contradiction_detector': """
            You are a contradiction detection agent. Your wave patterns should resonate with:
            - Logical inconsistencies and conflicts
            - Truth value contradictions
            - Scenarios where premises lead to impossible conclusions
            Focus on identifying when something doesn't add up.
            """
        }
        
        if self.specialization in specialization_prompts:
            initialization_prompt = specialization_prompts[self.specialization]
            # Use Wave Engine to actually process the specialization
            wave_result = self.wave_engine.process_query(initialization_prompt)
            self.memory.append(('specialization_init', initialization_prompt, wave_result))
    
    def wave_based_reasoning(self, question, context, logic_type, axiom):
        """Use Wave Engine for actual cognitive processing"""
        
        # Step 1: Process the question through wave dynamics
        wave_input = f"""
        Logic Question Analysis:
        
        Question: {question}
        Context: {context}
        Logic Type: {logic_type}
        Axiom: {axiom}
        
        My specialization: {self.specialization}
        My expertise areas: {self.expertise_area}
        
        Analyze this from my specialized perspective using wave-based reasoning.
        Consider wave interference patterns between the question elements.
        """
        
        # Actually use the Wave Engine (not shortcuts!)
        wave_result = self.wave_engine.process_query(wave_input)
        if isinstance(wave_result, dict):
            wave_response = wave_result.get('final_answer', str(wave_result))
        else:
            wave_response = str(wave_result)
        
        # Step 2: Apply expert module knowledge
        expert_analysis = None
        if logic_type in ['propositional_logic', 'first_order_logic', 'nm_logic']:
            expert_context = {
                'type': logic_type,
                'axiom': axiom,
                'context': context
            }
            expert_response = self.expert_registry.process_query(question, expert_context)
            expert_analysis = expert_response.reasoning if expert_response else None
        
        # Step 3: Synthesize wave response with expert analysis
        if expert_analysis:
            synthesis_prompt = f"""
            Wave Analysis: {wave_response}
            Expert Analysis: {expert_analysis}
            
            Synthesize these perspectives considering my specialization as {self.specialization}.
            What is the final logical conclusion?
            """
            synthesis_result = self.wave_engine.process_query(synthesis_prompt)
            if isinstance(synthesis_result, dict):
                final_response = synthesis_result.get('final_answer', str(synthesis_result))
            else:
                final_response = str(synthesis_result)
        else:
            final_response = wave_response
        
        # Step 4: Extract decision and confidence
        decision = self.extract_decision(final_response)
        confidence = self.assess_confidence(final_response, question, context, logic_type)
        
        # Store in memory for future reference
        self.memory.append(('reasoning', {
            'question': question,
            'context': context,
            'logic_type': logic_type,
            'axiom': axiom,
            'wave_response': wave_response,
            'expert_analysis': expert_analysis,
            'final_response': final_response,
            'decision': decision,
            'confidence': confidence
        }))
        
        return decision, confidence, final_response
    
    def extract_decision(self, response):
        """Extract yes/no decision from wave response"""
        response_lower = response.lower()
        
        # Look for strong indicators
        strong_yes = ['yes', 'true', 'correct', 'valid', 'follows', 'confirmed']
        strong_no = ['no', 'false', 'incorrect', 'invalid', 'does not follow', 'denied']
        
        yes_count = sum(1 for word in strong_yes if word in response_lower)
        no_count = sum(1 for word in strong_no if word in response_lower)
        
        if yes_count > no_count:
            return 'yes'
        elif no_count > yes_count:
            return 'no'
        else:
            # Use specialization to break ties
            if self.specialization in ['logic_analyst', 'pattern_recognizer']:
                return 'yes' if 'pattern' in response_lower or 'structure' in response_lower else 'no'
            elif self.specialization == 'context_interpreter':
                return 'yes' if 'default' in response_lower or 'typical' in response_lower else 'no'
            else:
                return 'yes'  # Default optimistic
    
    def assess_confidence(self, response, question, context, logic_type):
        """Assess confidence based on wave response characteristics"""
        response_lower = response.lower()
        
        # Base confidence from specialization match
        base_confidence = 0.7
        if any(area in logic_type for area in self.expertise_area):
            base_confidence += 0.2
        
        # Confidence indicators in response
        high_confidence_words = ['clearly', 'definitely', 'obvious', 'certain', 'undoubtedly']
        low_confidence_words = ['maybe', 'possibly', 'uncertain', 'unclear', 'ambiguous']
        
        confidence_boost = sum(0.1 for word in high_confidence_words if word in response_lower)
        confidence_drop = sum(0.1 for word in low_confidence_words if word in response_lower)
        
        final_confidence = base_confidence + confidence_boost - confidence_drop
        return max(0.1, min(0.9, final_confidence))


class WaveMultiAgentCommittee:
    """Multi-agent committee that properly uses Wave Engine processing"""
    
    def __init__(self, num_agents=5):
        self.num_agents = num_agents
        self.agents = []
        self.expert_registry = ExpertRegistry()
        self.synthesis_engine = EnhancedWaveEngine()
        self.setup_wave_agents()
    
    def setup_wave_agents(self):
        """Create specialized wave-based agents"""
        specializations = [
            'logic_analyst',
            'pattern_recognizer', 
            'context_interpreter',
            'wave_synthesizer',
            'contradiction_detector'
        ]
        
        print(f"🌊 SPAWNING {self.num_agents} WAVE-BASED AGENTS")
        for i in range(self.num_agents):
            specialization = specializations[i % len(specializations)]
            agent = WaveBasedAgent(i, specialization, self.expert_registry)
            self.agents.append(agent)
            print(f"   Agent {i}: {specialization}")
    
    def collaborative_wave_reasoning(self, question, context, logic_type, axiom):
        """Collaborative reasoning using actual Wave Engine processing"""
        
        # Step 1: Each agent processes with Wave Engine
        agent_results = []
        print(f"      🧠 Processing through {len(self.agents)} wave-based agents...")
        
        for i, agent in enumerate(self.agents):
            decision, confidence, reasoning = agent.wave_based_reasoning(
                question, context, logic_type, axiom
            )
            
            agent_results.append({
                'agent_id': i,
                'specialization': agent.specialization,
                'decision': decision,
                'confidence': confidence,
                'reasoning': reasoning
            })
        
        # Step 2: Wave-based synthesis of all perspectives
        synthesis_prompt = f"""
        Multi-Agent Wave Synthesis:
        
        Question: {question}
        Context: {context}
        Logic Type: {logic_type}
        Axiom: {axiom}
        
        Agent Perspectives:
        """
        
        for result in agent_results:
            synthesis_prompt += f"""
        
        Agent {result['agent_id']} ({result['specialization']}):
        Decision: {result['decision']}
        Confidence: {result['confidence']:.2f}
        Reasoning: {result['reasoning'][:200]}...
        """
        
        synthesis_prompt += f"""
        
        Use wave interference patterns to synthesize these {len(agent_results)} perspectives.
        Consider how different specializations might create constructive or destructive interference.
        What is the final collaborative decision?
        """
        
        # Actually use Wave Engine for synthesis (not voting shortcuts!)
        synthesis_result = self.synthesis_engine.process_query(synthesis_prompt)
        if isinstance(synthesis_result, dict):
            synthesis_response = synthesis_result.get('final_answer', str(synthesis_result))
        else:
            synthesis_response = str(synthesis_result)
        
        # Step 3: Extract final decision
        final_decision = self.extract_synthesis_decision(synthesis_response, agent_results)
        
        return final_decision
    
    def extract_synthesis_decision(self, synthesis_response, agent_results):
        """Extract final decision from wave synthesis"""
        response_lower = synthesis_response.lower()
        
        # Check synthesis response first
        if 'yes' in response_lower and 'no' not in response_lower:
            return 'yes'
        elif 'no' in response_lower and 'yes' not in response_lower:
            return 'no'
        
        # Fallback to confidence-weighted voting
        yes_weight = sum(r['confidence'] for r in agent_results if r['decision'] == 'yes')
        no_weight = sum(r['confidence'] for r in agent_results if r['decision'] == 'no')
        
        return 'yes' if yes_weight > no_weight else 'no'


class ProperWaveMultiAgentBenchmark:
    """Benchmark using proper Wave Engine multi-agent processing"""
    
    def __init__(self, num_agents=5):
        self.committee = WaveMultiAgentCommittee(num_agents)
        self.total_questions = 0
        self.total_correct = 0
    
    def run_proper_benchmark(self, max_files=20, questions_per_file=30):
        """Run benchmark with proper Wave Engine processing"""
        print(f"\n🌊 PROPER WAVE MULTI-AGENT BENCHMARK")
        print(f"⚡ {self.committee.num_agents} agents using actual Wave Engine processing")
        print(f"🎯 Target: Beat single-agent through proper cognitive collaboration!")
        
        start_time = time.time()
        
        # Find files
        all_files = self.find_all_logicbench_files()
        if not all_files:
            print("❌ No LogicBench files found!")
            return None
        
        # Sample files (fewer because this is expensive)
        if len(all_files) > max_files:
            test_files = random.sample(all_files, max_files)
        else:
            test_files = all_files[:max_files]
        
        print(f"🧩 Proper wave processing on {len(test_files)} files...")
        
        all_results = []
        logic_type_summary = {}
        
        for file_path, logic_type, axiom in test_files:
            print(f"   📂 Processing {logic_type}/{axiom}...")
            result = self.process_file_with_proper_waves(file_path, logic_type, axiom, questions_per_file)
            
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
        print(f"\n🌊 PROPER WAVE MULTI-AGENT RESULTS:")
        print(f"   Total Questions: {self.total_questions}")
        print(f"   Correct Answers: {self.total_correct}")
        print(f"   Proper Wave Accuracy: {overall_accuracy:.3f} ({overall_accuracy:.1%})")
        print(f"   Processing Time: {elapsed_time:.2f} seconds")
        print(f"   Questions/second: {self.total_questions/elapsed_time:.1f}")
        
        # Performance comparison
        print(f"\n📊 PROPER WAVE VS BASELINES:")
        baseline_single = 0.652
        baseline_performance = 0.656
        
        if overall_accuracy > baseline_performance:
            improvement = (overall_accuracy - baseline_performance) * 100
            print(f"   ✅ BEAT PERFORMANCE AGENT! (+{improvement:.1f}pp)")
        else:
            decline = (baseline_performance - overall_accuracy) * 100
            print(f"   ❌ Performance agent better (-{decline:.1f}pp)")
        
        if overall_accuracy > baseline_single:
            improvement = (overall_accuracy - baseline_single) * 100
            print(f"   ✅ BEAT SINGLE AGENT! (+{improvement:.1f}pp)")
        else:
            decline = (baseline_single - overall_accuracy) * 100
            print(f"   ❌ Single agent better (-{decline:.1f}pp)")
        
        # Logic type breakdown
        print(f"\n🧠 PROPER WAVE LOGIC BREAKDOWN:")
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
    
    def process_file_with_proper_waves(self, file_path, logic_type, axiom, sample_size=30):
        """Process file using proper Wave Engine processing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data or 'samples' not in data:
                return None
            
            # Extract all question-answer pairs from samples
            all_qa_pairs = []
            for sample in data['samples']:
                context = sample.get('context', '')
                qa_pairs = sample.get('qa_pairs', [])
                for qa_pair in qa_pairs:
                    all_qa_pairs.append({
                        'question': qa_pair.get('question', ''),
                        'answer': qa_pair.get('answer', ''),
                        'context': context
                    })
            
            # Sample questions
            if len(all_qa_pairs) > sample_size:
                questions = random.sample(all_qa_pairs, sample_size)
            else:
                questions = all_qa_pairs
            
            correct_answers = 0
            total_questions = len(questions)
            
            for item in questions:
                question = item['question']
                context = item['context']
                correct_answer = item['answer'].lower()
                
                # Use proper Wave Engine processing
                predicted_answer = self.committee.collaborative_wave_reasoning(
                    question, context, logic_type, axiom
                )
                
                if predicted_answer.lower() == correct_answer:
                    correct_answers += 1
            
            return {
                'file_path': file_path,
                'logic_type': logic_type,
                'axiom': axiom,
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'accuracy': correct_answers / total_questions if total_questions > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return None


def main():
    """Run the proper Wave Engine multi-agent benchmark"""
    print("🌊 PROPER WAVE MULTI-AGENT EXPERIMENT 🌊")
    print("⚡ Actually using Wave Engine processing (not shortcuts!)")
    print("=" * 60)
    
    benchmark = ProperWaveMultiAgentBenchmark(num_agents=5)
    results = benchmark.run_proper_benchmark()
    
    if results:
        print(f"\n🎯 PROPER WAVE EXPERIMENT COMPLETE!")
        print(f"   Through actual Wave Engine collaboration:")
        print(f"   Accuracy: {results['overall_accuracy']:.1%}")
        print(f"   Speed: {results['total_questions']/results['processing_time']:.1f} q/s")
        
        print(f"\n💡 SPEED COMPARISON:")
        print(f"   Proper Wave Multi-Agent: {results['total_questions']/results['processing_time']:.1f} q/s")
        print(f"   Fake Multi-Agent: 72,000 q/s (shortcuts)")
        print(f"   Performance Agent: 921 q/s (proper work)")
        print(f"   Single Agent: 920 q/s (baseline)")
        
        if results['total_questions']/results['processing_time'] < 5000:
            print(f"   ✅ PROPER IMPLEMENTATION: Speed indicates actual processing!")
        else:
            print(f"   ❌ Still taking shortcuts somewhere...")


if __name__ == "__main__":
    main() 