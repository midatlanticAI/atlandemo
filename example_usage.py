#!/usr/bin/env python3
"""
VTRFM (Atlan) Symbolic Cognitive Engine - Example Usage
Demonstrates the key features of the cognitive architecture.
"""

import time
import json
from src import AtlanAgent


def demonstrate_basic_functionality():
    """Demonstrates basic agent functionality."""
    print("=== VTRFM (Atlan) Cognitive Engine Demo ===\n")
    
    # Create an agent with custom configuration
    config = {
        'memory': {'max_size': 100},
        'drift_window': 20,
        'match_threshold': 0.9,
        'initial_beliefs': {
            'helping_others_is_rewarding': 0.8,
            'patience_leads_to_better_outcomes': 0.7,
            'quick_action_prevents_problems': 0.6
        },
        'action_effects': {
            'listen_carefully': 0.4,
            'provide_support': 0.5,
            'ask_clarifying_questions': 0.3,
            'offer_encouragement': 0.6
        }
    }
    
    agent = AtlanAgent(agent_id="demo_agent", config=config)
    print(f"Created agent: {agent.agent_id}")
    print(f"Initial beliefs: {agent.belief_system.audit_beliefs()}")
    print()
    
    return agent


def simulate_conversation_sequence(agent):
    """Simulates a sequence of interactions to show learning."""
    print("=== Simulating Conversation Sequence ===\n")
    
    # Sequence of inputs representing a conversation
    conversation = [
        ("I'm feeling really stressed about this project deadline", "concern"),
        ("The requirements keep changing and I'm falling behind", "frustration"),
        ("I don't know if I can deliver on time", "anxiety"),
        ("Maybe I should ask for help from my team", "consideration"),
        ("Actually, talking about it makes me feel a bit better", "relief"),
        ("I think I can break this down into smaller tasks", "planning"),
        ("Thanks for listening, I feel more confident now", "gratitude")
    ]
    
    for i, (phrase, label) in enumerate(conversation, 1):
        print(f"Input {i}: \"{phrase}\" (label: {label})")
        
        # Process the input
        result = agent.process_input(phrase, label=label)
        print(f"  Mood score: {result['mood_score']}")
        print(f"  Memory: {result['memory_interaction']['status']}")
        print(f"  Current drift: {result['drift']}")
        
        # Choose an action
        action = agent.choose_action()
        print(f"  Chosen action: {action}")
        
        # Simulate outcome based on the context
        if i <= 3:  # Early conversation - more tentative outcomes
            outcome = 0.3 + (i * 0.1)
        else:  # Later conversation - better outcomes as trust builds
            outcome = 0.6 + (i * 0.05)
        
        # Record the outcome
        feedback = agent.record_outcome(action, actual_outcome=outcome)
        print(f"  Outcome: {outcome:.2f} (feedback: {feedback['feedback']})")
        
        # Get response template
        template = agent.get_response_template()
        print(f"  Response tone: {template}")
        print()
        
        # Brief pause to simulate time passing
        time.sleep(0.1)


def demonstrate_reflection_and_learning(agent):
    """Shows how the agent reflects and updates beliefs."""
    print("=== Reflection and Learning ===\n")
    
    # Trigger reflection
    reflection = agent.reflect()
    print("Reflection results:")
    print(f"  Belief revisions: {len(reflection['belief_revisions'])}")
    if reflection['belief_revisions']:
        for old_belief, new_belief in reflection['belief_revisions']:
            print(f"    Revised: {old_belief[:50]}... -> {new_belief[:50]}...")
    
    print(f"  Current drift: {reflection['drift']}")
    print(f"  Average mood: {reflection['avg_mood']}")
    print(f"  Volatility: {reflection['volatility']}")
    
    # Show updated beliefs
    print(f"  Updated beliefs: {agent.belief_system.audit_beliefs()}")
    
    # Show personality evolution
    personality = agent.narrator.evolve_personality()
    print(f"  Personality traits: {personality}")
    print()


def demonstrate_state_monitoring(agent):
    """Shows comprehensive state monitoring."""
    print("=== Agent State Monitoring ===\n")
    
    # Get comprehensive state
    state = agent.get_state(include_memory_sample=3)
    
    print(f"Agent ID: {state['agent_id']}")
    print(f"Uptime: {state['uptime']:.2f} seconds")
    print(f"Memory size: {state['memory_stats']['memory_size']}")
    print(f"Total searches: {state['memory_stats']['searches']}")
    print(f"Cache hits: {state['memory_stats']['search_cache_hits']}")
    print(f"Current personality: {state['personality']}")
    
    print("\nDrift state:")
    for key, value in state['drift_state'].items():
        print(f"  {key}: {value}")
    
    print("\nRecent memory sample:")
    for i, memory in enumerate(state['memory_sample'][-3:], 1):
        print(f"  {i}. \"{memory['phrase'][:50]}...\" (reinforcement: {memory['reinforcement']})")
    
    print()


def demonstrate_persistence(agent):
    """Shows state saving and loading."""
    print("=== State Persistence ===\n")
    
    # Save state
    filename = "demo_agent_state.json"
    success = agent.save_state(filename)
    print(f"State saved to {filename}: {success}")
    
    if success:
        # Show what was saved
        try:
            with open(filename, 'r') as f:
                saved_state = json.load(f)
            print(f"Saved state contains {len(saved_state)} top-level keys")
            print(f"Serialization timestamp: {saved_state.get('_serialized_at')}")
            print(f"Version: {saved_state.get('_version')}")
        except Exception as e:
            print(f"Error reading saved state: {e}")
    
    print()


def run_advanced_scenario(agent):
    """Runs a more complex scenario showing emergent behavior."""
    print("=== Advanced Scenario: Emergent Behavior ===\n")
    
    # Simulate a challenging situation with mixed outcomes
    scenarios = [
        # Scenario 1: Initial optimism
        ("I'm excited to start this new project", "enthusiasm", 0.8),
        ("The team seems really capable", "confidence", 0.7),
        ("I think we can deliver something amazing", "optimism", 0.9),
        
        # Scenario 2: Challenges emerge
        ("We're running into some technical difficulties", "concern", 0.3),
        ("The client wants changes to the requirements", "frustration", 0.2),
        ("I'm worried we might not meet the deadline", "anxiety", 0.1),
        
        # Scenario 3: Problem-solving and adaptation
        ("Let me think about alternative approaches", "reflection", 0.5),
        ("I'll reach out to experts for advice", "resourcefulness", 0.6),
        ("The team is working together to find solutions", "collaboration", 0.8),
        
        # Scenario 4: Resolution and learning
        ("We found a creative solution to the technical issue", "breakthrough", 0.9),
        ("The client is happy with our revised approach", "satisfaction", 0.8),
        ("I learned a lot from this challenging experience", "growth", 0.9)
    ]
    
    print("Processing complex scenario with changing emotional states...\n")
    
    for i, (phrase, context, outcome) in enumerate(scenarios, 1):
        print(f"Step {i}: {context.title()}")
        print(f"  Input: \"{phrase}\"")
        
        # Process input
        result = agent.process_input(phrase, label=context)
        
        # Choose and execute action
        action = agent.choose_action()
        feedback = agent.record_outcome(action, actual_outcome=outcome)
        
        print(f"  Action: {action}")
        print(f"  Outcome: {outcome} (feedback: {feedback['feedback']})")
        print(f"  Mood drift: {result['drift']}")
        
        # Periodic reflection
        if i % 4 == 0:
            reflection = agent.reflect()
            print(f"  Reflection: {len(reflection['belief_revisions'])} belief revisions")
            personality = agent.narrator.evolve_personality()
            print(f"  Personality: {personality}")
        
        print()


def main():
    """Main demonstration function."""
    try:
        # Create and configure agent
        agent = demonstrate_basic_functionality()
        
        # Run demonstration scenarios
        simulate_conversation_sequence(agent)
        demonstrate_reflection_and_learning(agent)
        demonstrate_state_monitoring(agent)
        demonstrate_persistence(agent)
        run_advanced_scenario(agent)
        
        # Final state summary
        print("=== Final Agent State ===")
        final_state = agent.get_state()
        print(f"Total memories: {final_state['memory_stats']['memory_size']}")
        print(f"Total interactions: {final_state['memory_stats']['adds']}")
        print(f"Final personality: {final_state['personality']}")
        print(f"Final beliefs: {final_state['beliefs']}")
        
        print("\n=== Demo Complete ===")
        print("The VTRFM (Atlan) Cognitive Engine has demonstrated:")
        print("- Symbolic memory formation and reinforcement")
        print("- Emotional perception and drift tracking")
        print("- Belief evolution based on experience")
        print("- Personality development through interaction")
        print("- Self-reflection and adaptive behavior")
        print("- State persistence and monitoring")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 