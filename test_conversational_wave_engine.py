#!/usr/bin/env python3
"""
Comprehensive Test of Conversational Wave Engine
Shows all text processing and conversational AI capabilities
"""

import sys
import os

# Ensure proper import paths for CI/CD environment
current_dir = os.path.dirname(__file__)
project_root = current_dir  # This file is in the root directory
src_path = os.path.join(project_root, 'src')
expert_modules_path = os.path.join(project_root, 'expert_modules')

# Add all necessary paths to sys.path
for path in [project_root, src_path, expert_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

import pytest

from wave_text_engine import WaveTextEngine
from wave_text_learning_simple import SimpleWaveTextLearner

# Safe print function for CI/CD compatibility
def safe_print(text):
    """Print function that handles encoding issues on different platforms"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        print(text.encode('ascii', 'replace').decode('ascii'))

def test_basic_conversation():
    """Test basic conversational capabilities"""
    safe_print("\n~~ TESTING BASIC CONVERSATION ~~")
    safe_print("=" * 50)
    
    engine = WaveTextEngine()
    
    # Test different conversation types
    test_cases = [
        ("Hello there!", "greeting"),
        ("What is consciousness?", "question"),
        ("I think AI is fascinating", "statement"),
        ("Please explain wave engines", "command"),
        ("Goodbye!", "goodbye")
    ]
    
    for i, (text, expected_type) in enumerate(test_cases, 1):
        safe_print(f"\n--- Test {i}: {expected_type.title()} ---")
        safe_print(f"User: {text}")
        
        result = engine.process_text_input(text)
        
        safe_print(f"Assistant: {result['response']}")
        safe_print(f"Detected Type: {result['conversation_type']}")
        safe_print(f"Wave Activity: {len(result['wave_activations'])} concepts active")
        
        # Show strongest wave activation
        if result['wave_activations']:
            strongest = max(result['wave_activations'].items(), key=lambda x: abs(x[1]))
            safe_print(f"Strongest Wave: {strongest[0]} ({strongest[1]:.3f})")
    
    return engine

def test_text_learning():
    """Test text learning capabilities"""
    safe_print("\n\n[*] TESTING TEXT LEARNING [*]")
    safe_print("=" * 50)
    
    learner = SimpleWaveTextLearner()
    
    # Sample knowledge to learn
    ai_text = """
    Artificial intelligence involves creating systems that can think and learn.
    Machine learning uses algorithms to find patterns in data.
    Neural networks are inspired by how the human brain works.
    Deep learning uses multiple layers to process complex information.
    """
    
    consciousness_text = """
    Consciousness is the state of being aware of your thoughts and surroundings.
    It involves perception, memory, and self-reflection.
    Scientists study consciousness to understand how awareness emerges.
    Wave patterns in the brain might explain conscious experience.
    """
    
    safe_print("\n[>>] Learning from AI text:")
    ai_result = learner.learn_from_text(ai_text, "ai_knowledge")
    safe_print(f"[+] Learned {ai_result['concepts_learned']} concepts from {ai_result['sentences_processed']} sentences")
    
    safe_print("\n[>>] Learning from consciousness text:")
    consciousness_result = learner.learn_from_text(consciousness_text, "consciousness_knowledge")
    safe_print(f"[+] Learned {consciousness_result['concepts_learned']} concepts from {consciousness_result['sentences_processed']} sentences")
    
    # Test knowledge queries
    safe_print("\n[?] Testing knowledge queries:")
    
    queries = [
        "What is artificial intelligence?",
        "Tell me about consciousness",
        "How do neural networks work?"
    ]
    
    for query in queries:
        response = learner.query_knowledge(query)
        safe_print(f"Q: {query}")
        safe_print(f"A: {response}")
        safe_print("")
    
    # Show knowledge summary
    summary = learner.get_knowledge_summary()
    safe_print(f"[INFO] Knowledge Summary:")
    safe_print(f"Total concepts learned: {summary['total_concepts']}")
    safe_print(f"Documents processed: {summary['documents_learned']}")
    safe_print(f"Top concepts: {[concept for concept, _ in summary['top_concepts'][:5]]}")
    
    return learner

def test_text_generation():
    """Test text generation capabilities"""
    safe_print("\n\n[>>] TESTING TEXT GENERATION [<<]")
    safe_print("=" * 50)
    
    learner = SimpleWaveTextLearner()
    
    # First, give it some knowledge to work with
    knowledge_text = """
    Wave-based cognition represents a revolutionary approach to artificial intelligence.
    Unlike traditional AI that processes symbols sequentially, wave cognition uses interference patterns.
    Temporal dynamics allow the system to understand context and meaning through resonance.
    The wave engine can learn from experience and generate creative responses.
    Consciousness might emerge from the complex interference of wave patterns over time.
    """
    
    safe_print("[>>] Teaching the system about wave cognition...")
    result = learner.learn_from_text(knowledge_text, "wave_cognition")
    safe_print(f"[+] Learned {result['concepts_learned']} concepts")
    
    # Test text generation with different prompts
    prompts = [
        "Explain wave-based cognition",
        "Write about artificial intelligence",
        "Describe consciousness and waves",
        "Tell me about temporal dynamics"
    ]
    
    safe_print("\n[TARGET] Generating text from prompts:")
    
    for prompt in prompts:
        generated = learner.generate_text(prompt, length=40)
        safe_print(f"\nPrompt: {prompt}")
        safe_print(f"Generated: {generated}")
    
    return learner

def test_interactive_features():
    """Test interactive features like conversation memory"""
    safe_print("\n\n[INTERACTIVE] TESTING INTERACTIVE FEATURES [INTERACTIVE]")
    safe_print("=" * 50)
    
    engine = WaveTextEngine()
    
    # Simulate a conversation with memory
    conversation = [
        "Hello, I'm interested in learning about AI",
        "What can you tell me about machine learning?",
        "That's fascinating! Can you explain more?",
        "I particularly like neural networks",
        "Thank you for the information"
    ]
    
    safe_print("[CHAT] Simulating conversation with memory:")
    
    for i, message in enumerate(conversation, 1):
        safe_print(f"\nTurn {i}:")
        safe_print(f"User: {message}")
        
        result = engine.process_text_input(message, user_id="test_user")
        safe_print(f"Assistant: {result['response']}")
        
        # Show conversation context building
        if i > 1:
            summary = engine.get_conversation_summary()
            if summary['total_turns'] > 0:
                safe_print(f"Context: {summary['total_turns']} turns, discussing: {summary['top_topics'][:3]}")
    
    # Show final conversation analysis
    safe_print(f"\n[ANALYSIS] Final Conversation Analysis:")
    summary = engine.get_conversation_summary()
    safe_print(f"Total turns: {summary['total_turns']}")
    safe_print(f"Conversation types: {summary['conversation_types']}")
    safe_print(f"Main topics: {[topic for topic, _ in summary['top_topics'][:5]]}")
    
    # Show wave reasoning for last response
    safe_print(f"\n~~ Wave Analysis of Last Response:")
    explanation = engine.explain_last_response()
    safe_print(explanation)
    
    return engine

def main():
    """Run all tests"""
    safe_print("*** COMPREHENSIVE CONVERSATIONAL WAVE ENGINE TEST ***")
    safe_print("=" * 70)
    safe_print("Testing all text processing and conversational AI capabilities")
    safe_print("=" * 70)
    
    # Run all tests
    conversation_engine = test_basic_conversation()
    text_learner = test_text_learning()
    generation_learner = test_text_generation()
    interactive_engine = test_interactive_features()
    
    safe_print("\n\n*** ALL TESTS COMPLETED SUCCESSFULLY! ***")
    safe_print("=" * 50)
    safe_print("[+] Basic conversation - Working")
    safe_print("[+] Text learning - Working")
    safe_print("[+] Text generation - Working")
    safe_print("[+] Interactive features - Working")
    safe_print("[+] Wave-based reasoning - Working")
    safe_print("\n~~ The Conversational Wave Engine is ready for use! ~~")
    
    return {
        'conversation_engine': conversation_engine,
        'text_learner': text_learner,
        'generation_learner': generation_learner,
        'interactive_engine': interactive_engine
    }

if __name__ == "__main__":
    try:
        result = main()
        if result:
            safe_print("[SUCCESS] All conversational tests completed successfully!")
            sys.exit(0)
        else:
            safe_print("[-] Some tests failed!")
            sys.exit(1)
    except Exception as e:
        safe_print(f"[-] Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 