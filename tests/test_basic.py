"""
Basic integration tests for VTRFM (Atlan) Symbolic Cognitive Engine
"""

import sys
import os

# Ensure proper import paths for CI/CD environment
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
expert_modules_path = os.path.join(project_root, 'expert_modules')

# Add all necessary paths to sys.path
for path in [project_root, src_path, expert_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

from src import AtlanAgent


def test_agent_creation():
    """Test basic agent creation and initialization."""
    agent = AtlanAgent(agent_id="test_agent")
    assert agent.agent_id == "test_agent"
    assert agent.memory is not None
    assert agent.tone_engine is not None
    assert agent.drift_tracker is not None
    assert agent.belief_system is not None
    assert agent.dreamspace is not None
    assert agent.anchor is not None
    assert agent.narrator is not None


def test_input_processing():
    """Test basic input processing functionality."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Process a positive input
    result = agent.process_input("I feel great about this project!", label="positive")
    
    assert "input_phrase" in result
    assert "mood_score" in result
    assert "vector" in result
    assert "memory_interaction" in result
    assert "drift" in result
    assert "personality" in result
    
    # Mood score should be positive for positive input
    assert result["mood_score"] > 0
    
    # Memory should have added the input
    assert result["memory_interaction"]["status"] in ["added", "reinforced"]


def test_action_selection():
    """Test action selection functionality."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Add some input to establish state
    agent.process_input("I need to make a decision", label="neutral")
    
    # Choose an action
    action = agent.choose_action()
    
    # Should return a valid action string
    assert isinstance(action, str)
    assert len(action) > 0
    assert action in agent.dreamspace.action_templates


def test_outcome_recording():
    """Test outcome recording and belief updates."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Process input and choose action
    agent.process_input("I need to follow up on this", label="task")
    action = agent.choose_action()
    
    # Record a positive outcome
    feedback = agent.record_outcome(action, actual_outcome=0.8)
    
    assert "action" in feedback
    assert "feedback" in feedback
    assert "alignment" in feedback
    assert "projected" in feedback
    assert "actual" in feedback
    
    assert feedback["action"] == action
    assert feedback["actual"] == 0.8


def test_reflection():
    """Test self-reflection functionality."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Add some experiences
    agent.process_input("This is working well", label="positive")
    action = agent.choose_action()
    agent.record_outcome(action, actual_outcome=0.6)
    
    # Trigger reflection
    reflection = agent.reflect()
    
    assert "timestamp" in reflection
    assert "belief_revisions" in reflection
    assert "drift" in reflection
    assert "avg_mood" in reflection
    assert "volatility" in reflection
    assert "recent_feedback" in reflection


def test_state_retrieval():
    """Test agent state retrieval."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Add some state
    agent.process_input("Building up state", label="test")
    
    # Get state
    state = agent.get_state(include_memory_sample=1)
    
    assert "agent_id" in state
    assert "uptime" in state
    assert "drift_state" in state
    assert "beliefs" in state
    assert "memory_stats" in state
    assert "personality" in state
    assert "config" in state
    assert "memory_sample" in state
    
    assert state["agent_id"] == "test_agent"
    assert len(state["memory_sample"]) <= 1


def test_response_template():
    """Test response template generation."""
    agent = AtlanAgent(agent_id="test_agent")
    
    # Add some mood data
    agent.process_input("I'm feeling positive today", label="mood")
    
    # Get response template
    template = agent.get_response_template()
    
    assert isinstance(template, str)
    assert len(template) > 0


if __name__ == "__main__":
    # Run basic tests when executed directly (not through pytest)
    import sys
    try:
        test_agent_creation()
        test_input_processing()
        test_action_selection()
        test_outcome_recording()
        test_reflection()
        test_state_retrieval()
        test_response_template()
        
        print("All basic tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        sys.exit(1) 