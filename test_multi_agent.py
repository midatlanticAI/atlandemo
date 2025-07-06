#!/usr/bin/env python3
"""
Test Multi-Agent Collaboration
Testing the enhanced wave engine with expert modules
"""

from enhanced_wave_engine import EnhancedWaveEngine

def test_wave_plus_expert():
    """Test wave engine + expert module collaboration"""
    print("[TOOL] TESTING WAVE + EXPERT COLLABORATION")
    print("=" * 50)
    
    # Create enhanced engine
    engine = EnhancedWaveEngine()
    
    # Test a logic question
    question = "If all cats are animals and Fluffy is a cat, is Fluffy an animal?"
    print(f"Question: {question}")
    print()
    
    # Process with enhanced engine
    result = engine.process_query(question)
    
    print("[WAVE] MULTI-AGENT RESULT:")
    print(f"  Final Answer: {result.get('final_answer', 'Unknown')}")
    print(f"  Confidence: {result.get('confidence', 'Unknown')}")
    print()
    
    # Show different agent contributions
    if 'wave_response' in result and result['wave_response']:
        print("[WAVE] WAVE ENGINE CONTRIBUTION:")
        wave_resp = result['wave_response']
        print(f"  Wave Answer: {wave_resp.get('wave_answer', 'Unknown')}")
        print(f"  Wave Confidence: {wave_resp.get('confidence', 'Unknown')}")
        print(f"  Active Concepts: {len(wave_resp.get('activation_field', {}))}")
    
    if 'expert_response' in result and result['expert_response']:
        print("\n[BRAIN] EXPERT MODULE CONTRIBUTION:")
        expert_resp = result['expert_response']
        print(f"  Expert Answer: {expert_resp.answer}")
        print(f"  Expert Confidence: {expert_resp.confidence}")
        print(f"  Expert Type: {expert_resp.expert_type}")
        print(f"  Reasoning: {expert_resp.reasoning}")
    
    if 'integrated_response' in result and result['integrated_response']:
        print("\n[BOLT] INTEGRATED RESPONSE (3rd Agent):")
        integrated = result['integrated_response']
        print(f"  Integrated Answer: {integrated.get('answer', 'Unknown')}")
        print(f"  Integration Method: {integrated.get('method', 'Unknown')}")
        print(f"  Synergy Score: {result.get('synergy_score', 'Unknown')}")
    
    return result

def test_multiple_questions():
    """Test multiple questions to see consistency"""
    print("\n\n[TARGET] TESTING MULTIPLE QUESTIONS")
    print("=" * 50)
    
    engine = EnhancedWaveEngine()
    
    questions = [
        "All birds can fly. Penguins are birds. Can penguins fly?",
        "If A implies B and B implies C, does A imply C?",
        "All roses are flowers. Some flowers are red. Are all roses red?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📋 Question {i}: {question}")
        result = engine.process_query(question)
        print(f"   Answer: {result.get('final_answer', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 'Unknown')}")
        if 'synergy_score' in result:
            print(f"   Agent Synergy: {result['synergy_score']:.3f}")

if __name__ == "__main__":
    test_wave_plus_expert()
    test_multiple_questions() 