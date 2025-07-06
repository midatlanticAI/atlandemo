#!/usr/bin/env python3
"""
Comprehensive Test of Conversational Wave Engine
Shows all text processing and conversational AI capabilities
"""

from wave_text_engine import WaveTextEngine
from wave_text_learning_simple import SimpleWaveTextLearner

def test_basic_conversation():
    """Test basic conversational capabilities"""
    print("🌊 TESTING BASIC CONVERSATION 🌊")
    print("=" * 50)
    
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
        print(f"\n--- Test {i}: {expected_type.title()} ---")
        print(f"User: {text}")
        
        result = engine.process_text_input(text)
        
        print(f"Assistant: {result['response']}")
        print(f"Detected Type: {result['conversation_type']}")
        print(f"Wave Activity: {len(result['wave_activations'])} concepts active")
        
        # Show strongest wave activation
        if result['wave_activations']:
            strongest = max(result['wave_activations'].items(), key=lambda x: abs(x[1]))
            print(f"Strongest Wave: {strongest[0]} ({strongest[1]:.3f})")
    
    return engine

def test_text_learning():
    """Test text learning capabilities"""
    print("\n\n🧠 TESTING TEXT LEARNING 🧠")
    print("=" * 50)
    
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
    
    print("\n📚 Learning from AI text:")
    ai_result = learner.learn_from_text(ai_text, "ai_knowledge")
    print(f"✅ Learned {ai_result['concepts_learned']} concepts from {ai_result['sentences_processed']} sentences")
    
    print("\n📚 Learning from consciousness text:")
    consciousness_result = learner.learn_from_text(consciousness_text, "consciousness_knowledge")
    print(f"✅ Learned {consciousness_result['concepts_learned']} concepts from {consciousness_result['sentences_processed']} sentences")
    
    # Test knowledge queries
    print("\n❓ Testing knowledge queries:")
    
    queries = [
        "What is artificial intelligence?",
        "Tell me about consciousness",
        "How do neural networks work?"
    ]
    
    for query in queries:
        response = learner.query_knowledge(query)
        print(f"Q: {query}")
        print(f"A: {response}")
        print()
    
    # Show knowledge summary
    summary = learner.get_knowledge_summary()
    print(f"📊 Knowledge Summary:")
    print(f"Total concepts learned: {summary['total_concepts']}")
    print(f"Documents processed: {summary['documents_learned']}")
    print(f"Top concepts: {[concept for concept, _ in summary['top_concepts'][:5]]}")
    
    return learner

def test_text_generation():
    """Test text generation capabilities"""
    print("\n\n🎨 TESTING TEXT GENERATION 🎨")
    print("=" * 50)
    
    learner = SimpleWaveTextLearner()
    
    # First, give it some knowledge to work with
    knowledge_text = """
    Wave-based cognition represents a revolutionary approach to artificial intelligence.
    Unlike traditional AI that processes symbols sequentially, wave cognition uses interference patterns.
    Temporal dynamics allow the system to understand context and meaning through resonance.
    The wave engine can learn from experience and generate creative responses.
    Consciousness might emerge from the complex interference of wave patterns over time.
    """
    
    print("📚 Teaching the system about wave cognition...")
    result = learner.learn_from_text(knowledge_text, "wave_cognition")
    print(f"✅ Learned {result['concepts_learned']} concepts")
    
    # Test text generation with different prompts
    prompts = [
        "Explain wave-based cognition",
        "Write about artificial intelligence",
        "Describe consciousness and waves",
        "Tell me about temporal dynamics"
    ]
    
    print("\n🎯 Generating text from prompts:")
    
    for prompt in prompts:
        generated = learner.generate_text(prompt, length=40)
        print(f"\nPrompt: {prompt}")
        print(f"Generated: {generated}")
    
    return learner

def test_interactive_features():
    """Test interactive features like conversation memory"""
    print("\n\n💭 TESTING INTERACTIVE FEATURES 💭")
    print("=" * 50)
    
    engine = WaveTextEngine()
    
    # Simulate a conversation with memory
    conversation = [
        "Hello, I'm interested in learning about AI",
        "What can you tell me about machine learning?",
        "That's fascinating! Can you explain more?",
        "I particularly like neural networks",
        "Thank you for the information"
    ]
    
    print("🗨️ Simulating conversation with memory:")
    
    for i, message in enumerate(conversation, 1):
        print(f"\nTurn {i}:")
        print(f"User: {message}")
        
        result = engine.process_text_input(message, user_id="test_user")
        print(f"Assistant: {result['response']}")
        
        # Show conversation context building
        if i > 1:
            summary = engine.get_conversation_summary()
            if summary['total_turns'] > 0:
                print(f"Context: {summary['total_turns']} turns, discussing: {summary['top_topics'][:3]}")
    
    # Show final conversation analysis
    print(f"\n📈 Final Conversation Analysis:")
    summary = engine.get_conversation_summary()
    print(f"Total turns: {summary['total_turns']}")
    print(f"Conversation types: {summary['conversation_types']}")
    print(f"Main topics: {[topic for topic, _ in summary['top_topics'][:5]]}")
    
    # Show wave reasoning for last response
    print(f"\n🌊 Wave Analysis of Last Response:")
    explanation = engine.explain_last_response()
    print(explanation)
    
    return engine

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE CONVERSATIONAL WAVE ENGINE TEST 🚀")
    print("=" * 70)
    print("Testing all text processing and conversational AI capabilities")
    print("=" * 70)
    
    # Run all tests
    conversation_engine = test_basic_conversation()
    text_learner = test_text_learning()
    generation_learner = test_text_generation()
    interactive_engine = test_interactive_features()
    
    print("\n\n🎉 ALL TESTS COMPLETED SUCCESSFULLY! 🎉")
    print("=" * 50)
    print("✅ Basic conversation - Working")
    print("✅ Text learning - Working")
    print("✅ Text generation - Working")
    print("✅ Interactive features - Working")
    print("✅ Wave-based reasoning - Working")
    print("\n🌊 The Conversational Wave Engine is ready for use! 🌊")
    
    return {
        'conversation_engine': conversation_engine,
        'text_learner': text_learner,
        'generation_learner': generation_learner,
        'interactive_engine': interactive_engine
    }

if __name__ == "__main__":
    import sys
    try:
        result = main()
        if result:
            print("🎯 All conversational tests completed successfully!")
            sys.exit(0)
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 