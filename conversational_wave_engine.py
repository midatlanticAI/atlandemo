#!/usr/bin/env python3
"""
Conversational Wave Engine
Adds text I/O and conversational AI capabilities to the wave-based cognition system.
Enables natural language interaction while maintaining wave-based processing.
"""

import time
import re
import json
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from src.temporal_cognition import TemporalCognitionEngine

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class ConversationType(Enum):
    """Types of conversational interactions"""
    QUESTION = "question"
    STATEMENT = "statement" 
    COMMAND = "command"
    EXPLANATION = "explanation"
    GREETING = "greeting"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


@dataclass
class ConversationContext:
    """Maintains context for ongoing conversation"""
    user_id: str
    conversation_id: str
    turn_count: int
    conversation_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    active_topics: List[str]
    emotional_state: Dict[str, float]
    learning_context: Dict[str, Any]


class TextProcessor:
    """Advanced text processing with wave-based symbol extraction"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Common conversational patterns
        self.question_patterns = [
            r'what\s+(?:is|are|was|were|do|does|did|will|would|can|could|should|might)',
            r'how\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'why\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'when\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'where\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'who\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'which\s+(?:do|does|did|will|would|can|could|should|might|is|are|was|were)',
            r'can\s+you',
            r'do\s+you',
            r'are\s+you',
            r'is\s+it',
            r'\?'
        ]
        
        self.command_patterns = [
            r'^(?:please\s+)?(?:tell\s+me|explain|describe|show|demonstrate|help)',
            r'^(?:can\s+you\s+)?(?:create|generate|make|build|write|design)',
            r'^(?:let\'s|let\s+us)\s+',
            r'^(?:go\s+ahead|proceed|continue|start|begin)'
        ]
        
        self.greeting_patterns = [
            r'^(?:hi|hello|hey|greetings|good\s+(?:morning|afternoon|evening)|howdy)',
            r'^(?:how\s+are\s+you|how\'s\s+it\s+going|what\'s\s+up)'
        ]
        
        self.goodbye_patterns = [
            r'(?:goodbye|bye|farewell|see\s+you|talk\s+to\s+you|until\s+next|have\s+a\s+good)',
            r'(?:thanks?|thank\s+you).{0,20}(?:goodbye|bye|that\'s\s+all)'
        ]
    
    def extract_symbols_from_text(self, text: str) -> List[str]:
        """Extract meaningful symbols from text using wave-based processing"""
        # Basic tokenization and cleaning
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and punctuation
        meaningful_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                token.isalpha() and 
                len(token) > 1):
                meaningful_tokens.append(self.lemmatizer.lemmatize(token))
        
        # Extract phrases and compound concepts
        symbols = meaningful_tokens.copy()
        
        # Add bigrams for compound concepts
        for i in range(len(meaningful_tokens) - 1):
            bigram = f"{meaningful_tokens[i]}_{meaningful_tokens[i+1]}"
            symbols.append(bigram)
        
        # Add key phrases
        key_phrases = self._extract_key_phrases(text)
        symbols.extend(key_phrases)
        
        return symbols
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases and concepts from text"""
        phrases = []
        
        # Technical terms
        tech_patterns = [
            r'artificial\s+intelligence', r'machine\s+learning', r'deep\s+learning',
            r'neural\s+network', r'wave\s+engine', r'temporal\s+cognition',
            r'consciousness', r'cognition', r'reasoning', r'inference'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text.lower())
            phrases.extend([match.replace(' ', '_') for match in matches])
        
        # Emotional expressions
        emotion_patterns = [
            r'feel\s+(?:good|bad|happy|sad|excited|worried|confused|confident)',
            r'(?:love|hate|like|dislike|enjoy|appreciate)'
        ]
        
        for pattern in emotion_patterns:
            matches = re.findall(pattern, text.lower())
            phrases.extend([match.replace(' ', '_') for match in matches])
        
        return phrases
    
    def classify_conversation_type(self, text: str) -> ConversationType:
        """Classify the type of conversational input"""
        text_lower = text.lower().strip()
        
        # Check for questions
        for pattern in self.question_patterns:
            if re.search(pattern, text_lower):
                return ConversationType.QUESTION
        
        # Check for commands
        for pattern in self.command_patterns:
            if re.search(pattern, text_lower):
                return ConversationType.COMMAND
        
        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.search(pattern, text_lower):
                return ConversationType.GREETING
        
        # Check for goodbyes
        for pattern in self.goodbye_patterns:
            if re.search(pattern, text_lower):
                return ConversationType.GOODBYE
        
        # Check for explanations (contains "because", "due to", etc.)
        if re.search(r'because|due\s+to|reason|explain|since|as\s+a\s+result', text_lower):
            return ConversationType.EXPLANATION
        
        # Default to statement
        return ConversationType.STATEMENT
    
    def extract_intent_and_entities(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Extract intent and entities from text"""
        conv_type = self.classify_conversation_type(text)
        
        entities = {
            'topics': [],
            'emotions': [],
            'objects': [],
            'actions': [],
            'time_references': [],
            'quantities': []
        }
        
        # Extract topics
        topics = re.findall(r'(?:about|regarding|concerning)\s+(\w+)', text.lower())
        entities['topics'].extend(topics)
        
        # Extract emotions
        emotions = re.findall(r'(?:feel|feeling|emotion|mood)\s+(\w+)', text.lower())
        entities['emotions'].extend(emotions)
        
        # Extract actions
        actions = re.findall(r'(?:want\s+to|need\s+to|going\s+to|will)\s+(\w+)', text.lower())
        entities['actions'].extend(actions)
        
        # Extract time references
        time_refs = re.findall(r'(?:today|tomorrow|yesterday|now|later|soon|never)', text.lower())
        entities['time_references'].extend(time_refs)
        
        # Extract quantities
        quantities = re.findall(r'\d+|(?:few|many|some|all|most|several)', text.lower())
        entities['quantities'].extend(quantities)
        
        return conv_type.value, entities


class ResponseGenerator:
    """Generates natural language responses from wave activations"""
    
    def __init__(self):
        self.response_templates = {
            ConversationType.QUESTION: [
                "Based on the wave patterns, I think {answer}.",
                "The wave interference suggests {answer}.",
                "My wave-based analysis indicates {answer}.",
                "From the resonance patterns, {answer}.",
                "The wave dynamics show {answer}."
            ],
            ConversationType.STATEMENT: [
                "That's interesting. The wave patterns show {resonance}.",
                "I see. This creates wave interference with {concepts}.",
                "That resonates with {related_concepts}.",
                "This generates strong wave activity around {activated_concepts}.",
                "The wave field is now active with {concepts}."
            ],
            ConversationType.COMMAND: [
                "I'll process that through the wave engine. {explanation}",
                "Let me use wave interference to {action}. {explanation}",
                "Processing through wave dynamics... {explanation}",
                "Using temporal wave cognition to {action}. {explanation}"
            ],
            ConversationType.GREETING: [
                "Hello! My wave-based cognition is ready to interact.",
                "Hi there! The wave patterns are resonating nicely today.",
                "Greetings! My temporal cognition engine is active and ready.",
                "Hello! The wave field is stable and ready for conversation."
            ],
            ConversationType.GOODBYE: [
                "Goodbye! The wave patterns from our conversation will continue resonating.",
                "Farewell! Thanks for the interesting wave dynamics.",
                "See you later! The conversation waves are now part of my memory.",
                "Goodbye! The wave interference patterns were fascinating."
            ]
        }
    
    def generate_response(self, 
                         conv_type: ConversationType, 
                         wave_result: Dict[str, Any],
                         context: ConversationContext,
                         user_input: str) -> str:
        """Generate a natural language response from wave activations"""
        
        activation_field = wave_result.get('activation_field', {})
        
        # Select appropriate template
        templates = self.response_templates.get(conv_type, self.response_templates[ConversationType.STATEMENT])
        template = random.choice(templates)
        
        # Fill template based on wave activations
        if conv_type == ConversationType.QUESTION:
            answer = self._generate_answer_from_waves(activation_field, user_input)
            return template.format(answer=answer)
        
        elif conv_type == ConversationType.STATEMENT:
            resonance = self._describe_resonance(wave_result)
            concepts = self._get_active_concepts(activation_field, limit=3)
            related_concepts = self._get_related_concepts(activation_field, limit=2)
            activated_concepts = concepts
            
            return template.format(
                resonance=resonance,
                concepts=", ".join(concepts),
                related_concepts=", ".join(related_concepts),
                activated_concepts=", ".join(activated_concepts)
            )
        
        elif conv_type == ConversationType.COMMAND:
            action = self._extract_action_from_input(user_input)
            explanation = self._generate_wave_explanation(wave_result)
            return template.format(action=action, explanation=explanation)
        
        elif conv_type in [ConversationType.GREETING, ConversationType.GOODBYE]:
            return template
        
        else:
            return "I processed that through my wave engine. " + self._generate_wave_explanation(wave_result)
    
    def _generate_answer_from_waves(self, activation_field: Dict[str, float], question: str) -> str:
        """Generate an answer based on wave activations"""
        if not activation_field:
            return "I need more wave interference to answer that"
        
        # Find strongest activations
        sorted_activations = sorted(activation_field.items(), key=lambda x: abs(x[1]), reverse=True)
        
        # Generate answer based on strongest activation
        if sorted_activations:
            strongest_concept, strength = sorted_activations[0]
            
            # Simple heuristic responses
            if strength > 0.5:
                return f"there's strong resonance with '{strongest_concept}'"
            elif strength > 0.0:
                return f"there's positive wave activity around '{strongest_concept}'"
            elif strength < -0.5:
                return f"there's strong negative interference with '{strongest_concept}'"
            else:
                return f"there's some wave activity around '{strongest_concept}'"
        
        return "the wave patterns are still forming"
    
    def _describe_resonance(self, wave_result: Dict[str, Any]) -> str:
        """Describe the resonance patterns"""
        recent_resonance = wave_result.get('recent_resonance', [])
        
        if not recent_resonance:
            return "stable wave patterns"
        
        latest_resonance = recent_resonance[-1]
        resonance_type = latest_resonance.get('resonance_type', 'unknown')
        
        descriptions = {
            'constructive': 'strong constructive interference',
            'destructive': 'wave cancellation patterns',
            'harmonic': 'beautiful harmonic resonance',
            'dissonant': 'complex interference patterns'
        }
        
        return descriptions.get(resonance_type, 'interesting wave dynamics')
    
    def _get_active_concepts(self, activation_field: Dict[str, float], limit: int = 5) -> List[str]:
        """Get the most active concepts from the wave field"""
        if not activation_field:
            return []
        
        sorted_concepts = sorted(activation_field.items(), key=lambda x: abs(x[1]), reverse=True)
        return [concept for concept, _ in sorted_concepts[:limit]]
    
    def _get_related_concepts(self, activation_field: Dict[str, float], limit: int = 3) -> List[str]:
        """Get related concepts based on activation patterns"""
        active_concepts = self._get_active_concepts(activation_field, limit)
        
        # Simple related concept mapping
        related_map = {
            'thinking': ['mind', 'cognition', 'reasoning'],
            'wave': ['frequency', 'interference', 'resonance'],
            'consciousness': ['awareness', 'experience', 'perception'],
            'learning': ['knowledge', 'understanding', 'memory'],
            'emotion': ['feeling', 'mood', 'sentiment']
        }
        
        related = []
        for concept in active_concepts:
            if concept in related_map:
                related.extend(related_map[concept])
        
        return related[:limit]
    
    def _extract_action_from_input(self, text: str) -> str:
        """Extract the main action from user input"""
        actions = re.findall(r'(?:create|generate|make|build|write|design|explain|describe|show|demonstrate|help|analyze|process)', text.lower())
        return actions[0] if actions else "process"
    
    def _generate_wave_explanation(self, wave_result: Dict[str, Any]) -> str:
        """Generate an explanation of what the wave engine is doing"""
        active_waves = wave_result.get('active_waves', 0)
        activation_field = wave_result.get('activation_field', {})
        
        if active_waves == 0:
            return "No wave activity detected."
        
        strongest_activation = max(activation_field.values()) if activation_field else 0
        
        if strongest_activation > 0.5:
            return f"Strong wave interference detected with {active_waves} active patterns."
        elif strongest_activation > 0.0:
            return f"Moderate wave activity with {active_waves} resonating patterns."
        else:
            return f"Wave patterns are stabilizing with {active_waves} active frequencies."


class ConversationalWaveEngine:
    """Main conversational AI engine built on wave-based cognition"""
    
    def __init__(self):
        self.wave_engine = TemporalCognitionEngine()
        self.text_processor = TextProcessor()
        self.response_generator = ResponseGenerator()
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        self.learning_memory: Dict[str, Any] = {}
        self.global_knowledge: Dict[str, Any] = {}
        
        # Initialize conversation personality
        self.personality = {
            'curiosity': 0.7,
            'helpfulness': 0.9,
            'technical_depth': 0.8,
            'creativity': 0.6,
            'empathy': 0.5
        }
    
    def start_conversation(self, user_id: str, conversation_id: str = None) -> str:
        """Start a new conversation with a user"""
        if conversation_id is None:
            conversation_id = f"conv_{user_id}_{int(time.time())}"
        
        context = ConversationContext(
            user_id=user_id,
            conversation_id=conversation_id,
            turn_count=0,
            conversation_history=[],
            user_preferences={},
            active_topics=[],
            emotional_state={'mood': 0.0, 'arousal': 0.5, 'attention': 0.8},
            learning_context={}
        )
        
        self.conversation_contexts[conversation_id] = context
        
        # Generate a welcoming response
        wave_result = self.wave_engine.live_experience(
            visual=['greeting', 'conversation', 'start'],
            auditory=['welcome'],
            mood=0.3,
            arousal=0.6,
            attention=0.9,
            goals=['engage', 'help', 'learn'],
            satisfaction=0.8
        )
        
        response = self.response_generator.generate_response(
            ConversationType.GREETING,
            wave_result,
            context,
            "Hello"
        )
        
        # Add to conversation history
        context.conversation_history.append({
            'turn': 0,
            'user_input': "Hello",
            'wave_result': wave_result,
            'response': response,
            'timestamp': time.time()
        })
        
        return response
    
    def process_conversation_turn(self, 
                                 user_id: str, 
                                 conversation_id: str, 
                                 user_input: str) -> Dict[str, Any]:
        """Process a single turn in the conversation"""
        
        # Get or create conversation context
        context = self.conversation_contexts.get(conversation_id)
        if not context:
            # Create new context if it doesn't exist
            context = ConversationContext(
                user_id=user_id,
                conversation_id=conversation_id,
                turn_count=0,
                conversation_history=[],
                user_preferences={},
                active_topics=[],
                emotional_state={'mood': 0.0, 'arousal': 0.5, 'attention': 0.8},
                learning_context={}
            )
            self.conversation_contexts[conversation_id] = context
        
        # Update turn count
        context.turn_count += 1
        
        # Process the user input
        symbols = self.text_processor.extract_symbols_from_text(user_input)
        conv_type_str, entities = self.text_processor.extract_intent_and_entities(user_input)
        conv_type = ConversationType(conv_type_str)
        
        # Update context with new information
        context.active_topics.extend(entities.get('topics', []))
        context.active_topics = list(set(context.active_topics))  # Remove duplicates
        
        # Determine emotional state from conversation
        emotion_factors = self._analyze_emotional_context(user_input, context)
        
        # Process through wave engine
        wave_result = self.wave_engine.live_experience(
            visual=symbols,
            auditory=['conversation', 'dialogue'],
            mood=emotion_factors['mood'],
            arousal=emotion_factors['arousal'],
            attention=emotion_factors['attention'],
            goals=entities.get('actions', ['understand', 'respond']),
            context=context.active_topics,
            surprise=self._calculate_surprise(user_input, context),
            satisfaction=emotion_factors['satisfaction']
        )
        
        # Generate response
        response = self.response_generator.generate_response(
            conv_type,
            wave_result,
            context,
            user_input
        )
        
        # Learn from this interaction
        self._learn_from_interaction(user_input, response, wave_result, context)
        
        # Update conversation history
        turn_data = {
            'turn': context.turn_count,
            'user_input': user_input,
            'symbols': symbols,
            'conversation_type': conv_type.value,
            'entities': entities,
            'wave_result': wave_result,
            'response': response,
            'timestamp': time.time()
        }
        
        context.conversation_history.append(turn_data)
        
        return {
            'response': response,
            'conversation_type': conv_type.value,
            'wave_activations': wave_result.get('activation_field', {}),
            'active_concepts': list(wave_result.get('activation_field', {}).keys()),
            'resonance_patterns': wave_result.get('recent_resonance', []),
            'turn_count': context.turn_count,
            'conversation_id': conversation_id,
            'learning_occurred': True
        }
    
    def _analyze_emotional_context(self, user_input: str, context: ConversationContext) -> Dict[str, float]:
        """Analyze emotional context from user input and conversation history"""
        
        # Basic sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'excited', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'confused']
        
        input_lower = user_input.lower()
        
        mood = 0.0
        for word in positive_words:
            if word in input_lower:
                mood += 0.2
        
        for word in negative_words:
            if word in input_lower:
                mood -= 0.2
        
        # Arousal based on punctuation and capitalization
        arousal = 0.5
        if '!' in user_input:
            arousal += 0.2
        if '?' in user_input:
            arousal += 0.1
        if user_input.isupper():
            arousal += 0.3
        
        # Attention based on question words and complexity
        attention = 0.5
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        for word in question_words:
            if word in input_lower:
                attention += 0.1
        
        # Satisfaction based on context
        satisfaction = 0.5
        if context.turn_count > 1:
            # Look at previous interactions
            recent_turns = context.conversation_history[-3:]
            if any('thank' in turn.get('user_input', '').lower() for turn in recent_turns):
                satisfaction += 0.2
        
        return {
            'mood': max(-1.0, min(1.0, mood)),
            'arousal': max(0.0, min(1.0, arousal)),
            'attention': max(0.0, min(1.0, attention)),
            'satisfaction': max(-1.0, min(1.0, satisfaction))
        }
    
    def _calculate_surprise(self, user_input: str, context: ConversationContext) -> float:
        """Calculate surprise based on how unexpected the input is"""
        if context.turn_count == 1:
            return 0.1  # First turn is rarely surprising
        
        # Check for topic changes
        recent_topics = []
        for turn in context.conversation_history[-3:]:
            recent_topics.extend(turn.get('entities', {}).get('topics', []))
        
        current_symbols = self.text_processor.extract_symbols_from_text(user_input)
        
        # Calculate overlap with recent topics
        overlap = len(set(current_symbols) & set(recent_topics))
        total_symbols = len(current_symbols)
        
        if total_symbols == 0:
            return 0.0
        
        surprise = 1.0 - (overlap / total_symbols)
        return max(0.0, min(1.0, surprise))
    
    def _learn_from_interaction(self, 
                               user_input: str, 
                               response: str, 
                               wave_result: Dict[str, Any], 
                               context: ConversationContext):
        """Learn from the conversation interaction"""
        
        # Store patterns that led to responses
        activation_field = wave_result.get('activation_field', {})
        
        # Learn user preferences
        if user_input.lower().find('i like') != -1 or user_input.lower().find('i love') != -1:
            liked_concepts = self.text_processor.extract_symbols_from_text(user_input)
            for concept in liked_concepts:
                if concept not in context.user_preferences:
                    context.user_preferences[concept] = 0.0
                context.user_preferences[concept] += 0.1
        
        # Learn from strong wave activations
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.5:
                if symbol not in self.learning_memory:
                    self.learning_memory[symbol] = {
                        'activation_history': [],
                        'context_associations': [],
                        'response_patterns': []
                    }
                
                self.learning_memory[symbol]['activation_history'].append({
                    'activation': activation,
                    'timestamp': time.time(),
                    'context': context.active_topics.copy()
                })
        
        # Update global knowledge
        self.global_knowledge[f"conversation_{context.conversation_id}"] = {
            'user_id': context.user_id,
            'total_turns': context.turn_count,
            'topics_discussed': context.active_topics.copy(),
            'user_preferences': context.user_preferences.copy(),
            'last_interaction': time.time()
        }
    
    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        context = self.conversation_contexts.get(conversation_id)
        if not context:
            return {'error': 'Conversation not found'}
        
        # Analyze conversation patterns
        topics = context.active_topics
        turn_count = context.turn_count
        
        # Get wave pattern summary
        wave_state = self.wave_engine.get_cognitive_state()
        
        # Extract key moments
        key_moments = []
        for turn in context.conversation_history:
            wave_result = turn.get('wave_result', {})
            activations = wave_result.get('activation_field', {})
            
            if any(abs(activation) > 0.7 for activation in activations.values()):
                key_moments.append({
                    'turn': turn['turn'],
                    'input': turn['user_input'],
                    'response': turn['response'],
                    'strong_activations': [k for k, v in activations.items() if abs(v) > 0.7]
                })
        
        return {
            'conversation_id': conversation_id,
            'user_id': context.user_id,
            'total_turns': turn_count,
            'topics_discussed': topics,
            'user_preferences': context.user_preferences,
            'key_moments': key_moments,
            'wave_state': wave_state,
            'conversation_duration': time.time() - context.conversation_history[0]['timestamp'] if context.conversation_history else 0
        }
    
    def explain_wave_reasoning(self, conversation_id: str, turn_number: int) -> str:
        """Explain the wave-based reasoning for a specific turn"""
        context = self.conversation_contexts.get(conversation_id)
        if not context:
            return "Conversation not found"
        
        if turn_number >= len(context.conversation_history):
            return "Turn not found"
        
        turn = context.conversation_history[turn_number]
        wave_result = turn.get('wave_result', {})
        
        explanation = f"Wave Analysis for Turn {turn_number}:\n\n"
        
        # Explain input processing
        symbols = turn.get('symbols', [])
        explanation += f"Input Symbols: {', '.join(symbols)}\n\n"
        
        # Explain wave activations
        activations = wave_result.get('activation_field', {})
        explanation += "Wave Activations:\n"
        for symbol, activation in sorted(activations.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
            strength = "Strong" if abs(activation) > 0.5 else "Moderate" if abs(activation) > 0.2 else "Weak"
            direction = "Positive" if activation > 0 else "Negative"
            explanation += f"  • {symbol}: {activation:.3f} ({strength} {direction})\n"
        
        # Explain resonance patterns
        resonance = wave_result.get('recent_resonance', [])
        if resonance:
            explanation += f"\nResonance Patterns:\n"
            for pattern in resonance[-3:]:
                explanation += f"  • {pattern['symbols']} -> {pattern['resonance_type']} (strength: {pattern['interference']:.3f})\n"
        
        # Explain response generation
        explanation += f"\nResponse Generation:\n"
        explanation += f"  • Conversation Type: {turn.get('conversation_type', 'unknown')}\n"
        explanation += f"  • Active Wave Patterns: {wave_result.get('active_waves', 0)}\n"
        explanation += f"  • Generated Response: {turn.get('response', 'No response')}\n"
        
        return explanation
    
    def save_conversation_data(self, conversation_id: str, filename: str):
        """Save conversation data to a file"""
        context = self.conversation_contexts.get(conversation_id)
        if not context:
            return False
        
        data = {
            'conversation_summary': self.get_conversation_summary(conversation_id),
            'full_history': context.conversation_history,
            'learning_memory': self.learning_memory,
            'wave_state': self.wave_engine.get_cognitive_state(),
            'export_timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return True
    
    def chat(self, user_input: str, user_id: str = "default_user", conversation_id: str = None) -> str:
        """Simple chat interface - returns just the response text"""
        if conversation_id is None:
            conversation_id = f"chat_{user_id}_{int(time.time())}"
        
        if conversation_id not in self.conversation_contexts:
            # Start new conversation
            self.start_conversation(user_id, conversation_id)
        
        result = self.process_conversation_turn(user_id, conversation_id, user_input)
        return result['response']


# Demonstration and testing functions
def demo_conversational_wave_engine():
    """Demonstrate the conversational wave engine capabilities"""
    print("🌊 CONVERSATIONAL WAVE ENGINE DEMO 🌊")
    print("=" * 60)
    
    engine = ConversationalWaveEngine()
    
    # Test different conversation types
    test_conversations = [
        ("Hello there!", "greeting"),
        ("What is consciousness?", "question"),
        ("I love learning about AI", "statement"),
        ("Please explain how wave engines work", "command"),
        ("Why do waves interfere with each other?", "question"),
        ("This is fascinating!", "statement"),
        ("Thanks for the explanation, goodbye!", "goodbye")
    ]
    
    user_id = "demo_user"
    conversation_id = "demo_conv"
    
    print(f"\n🎯 Starting conversation with user: {user_id}")
    welcome = engine.start_conversation(user_id, conversation_id)
    print(f"Assistant: {welcome}")
    
    for i, (user_input, expected_type) in enumerate(test_conversations):
        print(f"\n--- Turn {i+1} ---")
        print(f"User: {user_input}")
        
        result = engine.process_conversation_turn(user_id, conversation_id, user_input)
        
        print(f"Assistant: {result['response']}")
        print(f"Detected Type: {result['conversation_type']} (expected: {expected_type})")
        print(f"Active Concepts: {result['active_concepts'][:3]}")
        
        if result['resonance_patterns']:
            print(f"Resonance: {result['resonance_patterns'][-1]['resonance_type']}")
    
    # Show conversation summary
    print(f"\n🔍 CONVERSATION SUMMARY")
    print("=" * 40)
    summary = engine.get_conversation_summary(conversation_id)
    print(f"Total turns: {summary['total_turns']}")
    print(f"Topics discussed: {summary['topics_discussed']}")
    print(f"Key moments: {len(summary['key_moments'])}")
    
    # Show wave reasoning for a specific turn
    print(f"\n🌊 WAVE REASONING EXPLANATION")
    print("=" * 40)
    explanation = engine.explain_wave_reasoning(conversation_id, 2)
    print(explanation)
    
    return engine


if __name__ == "__main__":
    demo_conversational_wave_engine() 