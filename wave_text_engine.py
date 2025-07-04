#!/usr/bin/env python3
"""
Wave-Based Text Processing Engine
Converts text to wave patterns and generates text responses
"""

import re
import time
import random
from typing import Dict, List, Any, Optional
from src.temporal_cognition import TemporalCognitionEngine

class WaveTextEngine:
    """Text processing engine using wave-based cognition"""
    
    def __init__(self):
        self.wave_engine = TemporalCognitionEngine()
        self.conversation_history = []
        self.user_context = {}
        
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'shall', 'ought',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'
        }
        
        # Response templates for different types of interactions
        self.response_templates = {
            'question': [
                "Based on the wave patterns, {answer}",
                "The wave interference suggests {answer}",
                "From the resonance patterns, I believe {answer}",
                "The wave dynamics indicate {answer}"
            ],
            'statement': [
                "That creates interesting wave patterns around {concepts}",
                "I see wave resonance with {concepts}",
                "This generates wave activity involving {concepts}",
                "The wave field shows activation in {concepts}"
            ],
            'greeting': [
                "Hello! My wave-based cognition is ready to chat.",
                "Hi there! The wave patterns are stable and ready for conversation.",
                "Greetings! My temporal cognition engine is active.",
                "Hello! Wave interference patterns are ready for interaction."
            ],
            'goodbye': [
                "Goodbye! The conversation waves will continue resonating.",
                "Farewell! Thanks for the interesting wave dynamics.",
                "See you later! The wave patterns from our chat are now in memory.",
                "Goodbye! The conversation created beautiful interference patterns."
            ]
        }
    
    def text_to_symbols(self, text: str) -> List[str]:
        """Convert text to meaningful symbols for wave processing"""
        # Basic tokenization - split into words and clean
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out stop words and short words
        symbols = []
        for word in words:
            if word not in self.stop_words and len(word) > 2:
                symbols.append(word)
        
        # Add some compound concepts (bigrams)
        for i in range(len(symbols) - 1):
            bigram = f"{symbols[i]}_{symbols[i+1]}"
            symbols.append(bigram)
        
        return symbols
    
    def detect_conversation_type(self, text: str) -> str:
        """Detect the type of conversation input"""
        text_lower = text.lower().strip()
        
        # Check for questions
        question_indicators = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can you', 'do you', 'are you', '?']
        if any(indicator in text_lower for indicator in question_indicators):
            return 'question'
        
        # Check for greetings
        greeting_words = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in text_lower for greeting in greeting_words):
            return 'greeting'
        
        # Check for goodbyes
        goodbye_words = ['goodbye', 'bye', 'farewell', 'see you', 'talk to you later', 'have a good']
        if any(goodbye in text_lower for goodbye in goodbye_words):
            return 'goodbye'
        
        # Default to statement
        return 'statement'
    
    def process_text_input(self, text: str, user_id: str = "default") -> Dict[str, Any]:
        """Process text input through wave cognition"""
        # Convert text to symbols
        symbols = self.text_to_symbols(text)
        
        # Detect conversation type
        conv_type = self.detect_conversation_type(text)
        
        # Analyze emotional context
        emotion_context = self.analyze_emotion(text)
        
        # Process through wave engine
        wave_result = self.wave_engine.live_experience(
            visual=symbols,
            auditory=['text', 'conversation'],
            mood=emotion_context['mood'],
            arousal=emotion_context['arousal'],
            attention=emotion_context['attention'],
            goals=['understand', 'respond', 'communicate'],
            satisfaction=emotion_context['satisfaction']
        )
        
        # Generate response
        response = self.generate_response(conv_type, wave_result, text)
        
        # Store interaction
        interaction = {
            'user_id': user_id,
            'input': text,
            'symbols': symbols,
            'conversation_type': conv_type,
            'wave_result': wave_result,
            'response': response,
            'timestamp': time.time()
        }
        
        self.conversation_history.append(interaction)
        
        return {
            'response': response,
            'conversation_type': conv_type,
            'wave_activations': wave_result.get('activation_field', {}),
            'symbols_processed': symbols,
            'wave_patterns': wave_result.get('recent_resonance', [])
        }
    
    def analyze_emotion(self, text: str) -> Dict[str, float]:
        """Analyze emotional context from text"""
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'excited', 'love', 'like', 'fantastic', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'confused', 'disappointed']
        
        text_lower = text.lower()
        
        # Calculate mood (-1 to 1)
        mood = 0.0
        for word in positive_words:
            if word in text_lower:
                mood += 0.3
        for word in negative_words:
            if word in text_lower:
                mood -= 0.3
        
        # Calculate arousal (0 to 1) based on intensity markers
        arousal = 0.5
        if '!' in text:
            arousal += 0.3
        if '?' in text:
            arousal += 0.1
        if text.isupper():
            arousal += 0.2
        
        # Calculate attention (0 to 1) based on question words and length
        attention = 0.5
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        for word in question_words:
            if word in text_lower:
                attention += 0.1
        
        # Longer texts get more attention
        if len(text) > 50:
            attention += 0.1
        
        # Calculate satisfaction (basic heuristic)
        satisfaction = 0.0
        if 'thank' in text_lower:
            satisfaction += 0.3
        if 'please' in text_lower:
            satisfaction += 0.2
        
        return {
            'mood': max(-1.0, min(1.0, mood)),
            'arousal': max(0.0, min(1.0, arousal)),
            'attention': max(0.0, min(1.0, attention)),
            'satisfaction': max(-1.0, min(1.0, satisfaction))
        }
    
    def generate_response(self, conv_type: str, wave_result: Dict[str, Any], original_text: str) -> str:
        """Generate natural language response from wave patterns"""
        activation_field = wave_result.get('activation_field', {})
        
        # Get response template
        templates = self.response_templates.get(conv_type, self.response_templates['statement'])
        template = random.choice(templates)
        
        if conv_type == 'question':
            # Generate answer based on strongest activations
            answer = self.generate_answer_from_activations(activation_field, original_text)
            return template.format(answer=answer)
        
        elif conv_type == 'statement':
            # Describe the concepts that are active
            concepts = self.get_active_concepts(activation_field)
            concepts_str = ", ".join(concepts[:3]) if concepts else "various topics"
            return template.format(concepts=concepts_str)
        
        elif conv_type in ['greeting', 'goodbye']:
            return template
        
        else:
            # Default response
            return "I processed that through my wave engine. " + self.describe_wave_activity(wave_result)
    
    def generate_answer_from_activations(self, activation_field: Dict[str, float], question: str) -> str:
        """Generate an answer based on wave activations"""
        if not activation_field:
            return "I need more information to answer that."
        
        # Find the strongest activation
        strongest_concept = max(activation_field.keys(), key=lambda k: abs(activation_field[k]))
        strongest_value = activation_field[strongest_concept]
        
        if strongest_value > 0.5:
            return f"there is strong positive resonance with '{strongest_concept}'"
        elif strongest_value > 0.0:
            return f"there is some positive wave activity around '{strongest_concept}'"
        elif strongest_value < -0.5:
            return f"there is strong negative interference with '{strongest_concept}'"
        else:
            return f"there is wave activity around '{strongest_concept}', but the patterns are still forming"
    
    def get_active_concepts(self, activation_field: Dict[str, float], limit: int = 5) -> List[str]:
        """Get the most active concepts from the activation field"""
        if not activation_field:
            return []
        
        # Sort by absolute activation strength
        sorted_concepts = sorted(activation_field.items(), key=lambda x: abs(x[1]), reverse=True)
        return [concept for concept, _ in sorted_concepts[:limit]]
    
    def describe_wave_activity(self, wave_result: Dict[str, Any]) -> str:
        """Describe the current wave activity"""
        active_waves = wave_result.get('active_waves', 0)
        activation_field = wave_result.get('activation_field', {})
        
        if not activation_field:
            return "No significant wave activity detected."
        
        max_activation = max(abs(v) for v in activation_field.values())
        
        if max_activation > 0.7:
            return f"Strong wave interference patterns detected with {active_waves} active frequencies."
        elif max_activation > 0.3:
            return f"Moderate wave resonance with {active_waves} active patterns."
        else:
            return f"Gentle wave activity with {active_waves} resonating frequencies."
    
    def chat(self, text: str, user_id: str = "default") -> str:
        """Simple chat interface"""
        result = self.process_text_input(text, user_id)
        return result['response']
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation so far"""
        if not self.conversation_history:
            return {"message": "No conversation history yet"}
        
        total_turns = len(self.conversation_history)
        conversation_types = [turn['conversation_type'] for turn in self.conversation_history]
        
        # Count types
        type_counts = {}
        for conv_type in conversation_types:
            type_counts[conv_type] = type_counts.get(conv_type, 0) + 1
        
        # Get all symbols that have been discussed
        all_symbols = []
        for turn in self.conversation_history:
            all_symbols.extend(turn['symbols'])
        
        # Count symbol frequencies
        symbol_counts = {}
        for symbol in all_symbols:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        # Get most discussed topics
        top_topics = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_turns': total_turns,
            'conversation_types': type_counts,
            'top_topics': top_topics,
            'recent_wave_state': self.wave_engine.get_cognitive_state()
        }
    
    def explain_last_response(self) -> str:
        """Explain the wave reasoning behind the last response"""
        if not self.conversation_history:
            return "No conversation history to explain."
        
        last_turn = self.conversation_history[-1]
        wave_result = last_turn['wave_result']
        
        explanation = "Wave Analysis of Last Response:\n\n"
        
        # Show input processing
        explanation += f"Input: '{last_turn['input']}'\n"
        explanation += f"Extracted Symbols: {', '.join(last_turn['symbols'])}\n"
        explanation += f"Conversation Type: {last_turn['conversation_type']}\n\n"
        
        # Show wave activations
        activations = wave_result.get('activation_field', {})
        explanation += "Wave Activations:\n"
        for symbol, activation in sorted(activations.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
            direction = "+" if activation > 0 else "-"
            strength = "Strong" if abs(activation) > 0.5 else "Moderate" if abs(activation) > 0.2 else "Weak"
            explanation += f"  {symbol}: {direction}{abs(activation):.3f} ({strength})\n"
        
        # Show resonance patterns
        resonance = wave_result.get('recent_resonance', [])
        if resonance:
            explanation += "\nResonance Patterns:\n"
            for pattern in resonance[-3:]:
                explanation += f"  {' + '.join(pattern['symbols'])} -> {pattern['resonance_type']}\n"
        
        explanation += f"\nGenerated Response: '{last_turn['response']}'"
        
        return explanation

def demo_wave_text_engine():
    """Demonstrate the wave text engine"""
    print("🌊 WAVE TEXT ENGINE DEMO 🌊")
    print("=" * 50)
    
    engine = WaveTextEngine()
    
    # Test conversations
    test_inputs = [
        "Hello! How are you today?",
        "What is consciousness?",
        "I love learning about artificial intelligence",
        "Can you explain how wave engines work?",
        "This is really fascinating stuff!",
        "Thank you for the explanation. Goodbye!"
    ]
    
    print("\n🎯 Testing different types of inputs:")
    
    for i, text in enumerate(test_inputs):
        print(f"\n--- Test {i+1} ---")
        print(f"Input: {text}")
        
        result = engine.process_text_input(text)
        
        print(f"Response: {result['response']}")
        print(f"Type: {result['conversation_type']}")
        print(f"Top Symbols: {result['symbols_processed'][:3]}")
        
        # Show wave activations
        activations = result['wave_activations']
        if activations:
            top_activation = max(activations.items(), key=lambda x: abs(x[1]))
            print(f"Strongest Wave: {top_activation[0]} ({top_activation[1]:.3f})")
    
    print(f"\n🔍 Conversation Summary:")
    summary = engine.get_conversation_summary()
    print(f"Total turns: {summary['total_turns']}")
    print(f"Conversation types: {summary['conversation_types']}")
    print(f"Top topics: {[topic for topic, _ in summary['top_topics'][:5]]}")
    
    print(f"\n🌊 Wave Reasoning Explanation:")
    explanation = engine.explain_last_response()
    print(explanation)
    
    return engine

if __name__ == "__main__":
    demo_wave_text_engine() 