#!/usr/bin/env python3
"""
Wave-Based Text Learning System
Advanced text processing that learns from documents and generates creative content
"""

import os
import re
import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
from wave_text_engine import WaveTextEngine

class WaveTextLearningEngine:
    """Advanced text learning engine using wave-based cognition"""
    
    def __init__(self):
        self.base_engine = WaveTextEngine()
        self.knowledge_base = {}
        self.document_memories = {}
        self.concept_associations = defaultdict(list)
        self.text_patterns = {}
        self.creative_templates = {}
        self.learning_history = []
        
        # Advanced text processing patterns
        self.sentence_patterns = {
            'declarative': r'^[A-Z][^.!?]*\.$',
            'interrogative': r'^[A-Z][^.!?]*\?$',
            'exclamatory': r'^[A-Z][^.!?]*\!$',
            'imperative': r'^[A-Z][^.!?]*\.$'
        }
        
        self.phrase_patterns = {
            'technical': r'\b(?:algorithm|system|process|method|technique|approach|framework|model|architecture)\b',
            'emotional': r'\b(?:feel|emotion|happy|sad|excited|worried|confident|nervous|proud|ashamed)\b',
            'temporal': r'\b(?:now|then|before|after|during|while|when|until|since|always|never|often|sometimes)\b',
            'causal': r'\b(?:because|since|due to|as a result|therefore|thus|consequently|hence|so|caused by)\b',
            'comparative': r'\b(?:better|worse|more|less|than|compared to|similar to|different from|like|unlike)\b'
        }
    
    def learn_from_text_file(self, filename: str, learning_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Learn from a text file using wave-based processing"""
        if not os.path.exists(filename):
            return {'error': f'File not found: {filename}'}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.learn_from_text(content, source=filename, context=learning_context)
        
        except Exception as e:
            return {'error': f'Error reading file: {e}'}
    
    def learn_from_text(self, text: str, source: str = "direct_input", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Learn from raw text using wave-based cognition"""
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        # Process each sentence through wave engine
        learned_concepts = []
        sentence_patterns = []
        wave_memories = []
        
        for i, sentence in enumerate(sentences):
            # Extract symbols from sentence
            symbols = self.base_engine.text_to_symbols(sentence)
            
            # Analyze sentence patterns
            pattern_info = self._analyze_sentence_patterns(sentence)
            sentence_patterns.append(pattern_info)
            
            # Process through wave engine
            wave_result = self.base_engine.wave_engine.live_experience(
                visual=symbols,
                auditory=['learning', 'text', 'knowledge'],
                mood=self._calculate_learning_mood(sentence),
                arousal=0.7,
                attention=0.9,
                goals=['learn', 'understand', 'remember'],
                context=[source, 'learning_session'],
                satisfaction=0.8
            )
            
            # Store wave memory
            wave_memory = {
                'sentence': sentence,
                'symbols': symbols,
                'wave_activations': wave_result.get('activation_field', {}),
                'resonance_patterns': wave_result.get('recent_resonance', []),
                'pattern_info': pattern_info,
                'index': i
            }
            wave_memories.append(wave_memory)
            
            # Extract and store concepts
            activations = wave_result.get('activation_field', {})
            for symbol, activation in activations.items():
                if abs(activation) > 0.3:  # Strong activation threshold
                    learned_concepts.append({
                        'concept': symbol,
                        'activation': activation,
                        'context': sentence,
                        'source': source
                    })
        
        # Build concept associations
        self._build_concept_associations(wave_memories)
        
        # Extract text patterns for generation
        self._extract_text_patterns(sentences, sentence_patterns)
        
        # Store document memory
        document_memory = {
            'source': source,
            'content': text,
            'sentences': sentences,
            'wave_memories': wave_memories,
            'learned_concepts': learned_concepts,
            'sentence_patterns': sentence_patterns,
            'learning_timestamp': time.time(),
            'context': context or {}
        }
        
        self.document_memories[source] = document_memory
        
        # Update knowledge base
        self._update_knowledge_base(learned_concepts, source)
        
        # Record learning session
        learning_session = {
            'source': source,
            'sentences_processed': len(sentences),
            'concepts_learned': len(learned_concepts),
            'patterns_identified': len(set(p['primary_pattern'] for p in sentence_patterns)),
            'timestamp': time.time(),
            'context': context or {}
        }
        
        self.learning_history.append(learning_session)
        
        return {
            'success': True,
            'source': source,
            'sentences_processed': len(sentences),
            'concepts_learned': len(learned_concepts),
            'top_concepts': sorted(learned_concepts, key=lambda x: abs(x['activation']), reverse=True)[:10],
            'patterns_found': list(set(p['primary_pattern'] for p in sentence_patterns)),
            'learning_session': learning_session
        }
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    def _analyze_sentence_patterns(self, sentence: str) -> Dict[str, Any]:
        """Analyze patterns in a sentence"""
        pattern_info = {
            'primary_pattern': 'declarative',
            'phrase_types': [],
            'complexity': 'simple',
            'sentiment': 'neutral',
            'length_category': 'medium'
        }
        
        # Determine primary pattern
        if sentence.endswith('?'):
            pattern_info['primary_pattern'] = 'interrogative'
        elif sentence.endswith('!'):
            pattern_info['primary_pattern'] = 'exclamatory'
        elif sentence.lower().startswith(('please', 'let', 'go', 'come', 'do', 'don\'t')):
            pattern_info['primary_pattern'] = 'imperative'
        
        # Find phrase types
        for phrase_type, pattern in self.phrase_patterns.items():
            if re.search(pattern, sentence.lower()):
                pattern_info['phrase_types'].append(phrase_type)
        
        # Determine complexity
        word_count = len(sentence.split())
        if word_count > 20:
            pattern_info['complexity'] = 'complex'
        elif word_count > 10:
            pattern_info['complexity'] = 'medium'
        else:
            pattern_info['complexity'] = 'simple'
        
        # Determine length category
        if word_count > 25:
            pattern_info['length_category'] = 'long'
        elif word_count > 15:
            pattern_info['length_category'] = 'medium'
        else:
            pattern_info['length_category'] = 'short'
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'like', 'best', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'sad', 'angry', 'disappointed', 'wrong']
        
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in positive_words):
            pattern_info['sentiment'] = 'positive'
        elif any(word in sentence_lower for word in negative_words):
            pattern_info['sentiment'] = 'negative'
        
        return pattern_info
    
    def _calculate_learning_mood(self, sentence: str) -> float:
        """Calculate learning mood based on sentence content"""
        positive_indicators = ['learn', 'understand', 'discover', 'amazing', 'fascinating', 'wonderful', 'excellent']
        negative_indicators = ['difficult', 'hard', 'confusing', 'complex', 'challenging', 'impossible']
        
        sentence_lower = sentence.lower()
        mood = 0.0
        
        for indicator in positive_indicators:
            if indicator in sentence_lower:
                mood += 0.2
        
        for indicator in negative_indicators:
            if indicator in sentence_lower:
                mood -= 0.1
        
        return max(-1.0, min(1.0, mood))
    
    def _build_concept_associations(self, wave_memories: List[Dict[str, Any]]):
        """Build associations between concepts based on wave interference"""
        for i, memory in enumerate(wave_memories):
            activations = memory['wave_activations']
            strong_concepts = [concept for concept, activation in activations.items() if abs(activation) > 0.4]
            
            # Create associations between strong concepts
            for concept in strong_concepts:
                for other_concept in strong_concepts:
                    if concept != other_concept:
                        self.concept_associations[concept].append({
                            'associated_concept': other_concept,
                            'context': memory['sentence'],
                            'activation_strength': activations.get(other_concept, 0.0),
                            'timestamp': time.time()
                        })
    
    def _extract_text_patterns(self, sentences: List[str], sentence_patterns: List[Dict[str, Any]]):
        """Extract text patterns for later generation"""
        for sentence, pattern_info in zip(sentences, sentence_patterns):
            pattern_key = f"{pattern_info['primary_pattern']}_{pattern_info['complexity']}_{pattern_info['sentiment']}"
            
            if pattern_key not in self.text_patterns:
                self.text_patterns[pattern_key] = []
            
            self.text_patterns[pattern_key].append({
                'sentence': sentence,
                'pattern_info': pattern_info,
                'timestamp': time.time()
            })
    
    def _update_knowledge_base(self, learned_concepts: List[Dict[str, Any]], source: str):
        """Update the knowledge base with learned concepts"""
        for concept_info in learned_concepts:
            concept = concept_info['concept']
            
            if concept not in self.knowledge_base:
                self.knowledge_base[concept] = {
                    'activation_history': [],
                    'contexts': [],
                    'sources': set(),
                    'associations': [],
                    'first_learned': time.time()
                }
            
            self.knowledge_base[concept]['activation_history'].append({
                'activation': concept_info['activation'],
                'timestamp': time.time()
            })
            
            self.knowledge_base[concept]['contexts'].append(concept_info['context'])
            self.knowledge_base[concept]['sources'].add(source)
    
    def generate_creative_text(self, prompt: str, style: str = "creative", length: int = 100) -> Dict[str, Any]:
        """Generate creative text based on learned patterns and wave dynamics"""
        
        # Process prompt through wave engine
        prompt_symbols = self.base_engine.text_to_symbols(prompt)
        wave_result = self.base_engine.wave_engine.live_experience(
            visual=prompt_symbols,
            auditory=['creative', 'generation', 'writing'],
            mood=0.6,
            arousal=0.8,
            attention=0.9,
            goals=['create', 'generate', 'express'],
            satisfaction=0.7
        )
        
        # Get activated concepts
        activations = wave_result.get('activation_field', {})
        active_concepts = [concept for concept, activation in activations.items() if abs(activation) > 0.3]
        
        # Generate text based on active concepts and learned patterns
        generated_sentences = []
        target_sentences = max(1, length // 20)  # Rough estimate
        
        for _ in range(target_sentences):
            sentence = self._generate_sentence_from_concepts(active_concepts, style)
            if sentence:
                generated_sentences.append(sentence)
        
        generated_text = ' '.join(generated_sentences)
        
        # Analyze the generated text
        analysis = self._analyze_generated_text(generated_text, prompt)
        
        return {
            'generated_text': generated_text,
            'prompt': prompt,
            'style': style,
            'active_concepts': active_concepts,
            'sentences_generated': len(generated_sentences),
            'analysis': analysis,
            'wave_activations': activations,
            'generation_timestamp': time.time()
        }
    
    def _generate_sentence_from_concepts(self, concepts: List[str], style: str) -> str:
        """Generate a sentence using active concepts and learned patterns"""
        if not concepts:
            return ""
        
        # Choose a random concept as the focus
        focus_concept = random.choice(concepts)
        
        # Find associated concepts
        associated = self.concept_associations.get(focus_concept, [])
        related_concepts = [assoc['associated_concept'] for assoc in associated[:3]]
        
        # Choose a text pattern
        available_patterns = list(self.text_patterns.keys())
        if available_patterns:
            pattern_key = random.choice(available_patterns)
            pattern_examples = self.text_patterns[pattern_key]
            
            if pattern_examples:
                # Use an example as a template
                example = random.choice(pattern_examples)
                template_sentence = example['sentence']
                
                # Simple substitution (very basic)
                sentence = template_sentence
                
                # Replace some words with concepts
                words = sentence.split()
                for i, word in enumerate(words):
                    if word.lower() in ['thing', 'concept', 'idea', 'element', 'part']:
                        if concepts:
                            words[i] = random.choice(concepts)
                
                return ' '.join(words)
        
        # Fallback: simple sentence generation
        templates = [
            f"The {focus_concept} creates interesting possibilities.",
            f"Understanding {focus_concept} requires careful consideration.",
            f"The concept of {focus_concept} resonates with many ideas.",
            f"When we examine {focus_concept}, we find fascinating patterns."
        ]
        
        if related_concepts:
            templates.extend([
                f"The {focus_concept} connects to {random.choice(related_concepts)} in meaningful ways.",
                f"Both {focus_concept} and {random.choice(related_concepts)} share important characteristics."
            ])
        
        return random.choice(templates)
    
    def _analyze_generated_text(self, text: str, prompt: str) -> Dict[str, Any]:
        """Analyze the quality and characteristics of generated text"""
        words = text.split()
        sentences = self._split_into_sentences(text)
        
        analysis = {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'average_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(word.lower() for word in words)),
            'vocabulary_diversity': len(set(word.lower() for word in words)) / len(words) if words else 0,
            'prompt_relevance': self._calculate_prompt_relevance(text, prompt),
            'creativity_score': self._calculate_creativity_score(text),
            'readability': self._calculate_readability(text)
        }
        
        return analysis
    
    def _calculate_prompt_relevance(self, text: str, prompt: str) -> float:
        """Calculate how relevant the generated text is to the prompt"""
        prompt_words = set(self.base_engine.text_to_symbols(prompt))
        text_words = set(self.base_engine.text_to_symbols(text))
        
        if not prompt_words:
            return 0.0
        
        overlap = len(prompt_words & text_words)
        relevance = overlap / len(prompt_words)
        
        return min(1.0, relevance)
    
    def _calculate_creativity_score(self, text: str) -> float:
        """Calculate a creativity score based on unique word combinations"""
        words = text.lower().split()
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        
        # Check how many bigrams are novel (not seen in training)
        novel_bigrams = 0
        for bigram in bigrams:
            if bigram not in self.knowledge_base:
                novel_bigrams += 1
        
        creativity = novel_bigrams / len(bigrams) if bigrams else 0
        return min(1.0, creativity)
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate basic readability score"""
        words = text.split()
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability heuristic
        if avg_sentence_length > 25:
            return 0.3  # Too long
        elif avg_sentence_length > 15:
            return 0.7  # Good
        elif avg_sentence_length > 8:
            return 0.9  # Very good
        else:
            return 0.5  # Too short
    
    def query_knowledge(self, query: str) -> Dict[str, Any]:
        """Query the knowledge base using wave-based retrieval"""
        query_symbols = self.base_engine.text_to_symbols(query)
        
        # Find relevant concepts
        relevant_concepts = []
        for concept, info in self.knowledge_base.items():
            if concept in query_symbols:
                relevant_concepts.append({
                    'concept': concept,
                    'relevance': 1.0,
                    'info': info
                })
        
        # Find associated concepts
        for query_symbol in query_symbols:
            if query_symbol in self.concept_associations:
                for assoc in self.concept_associations[query_symbol]:
                    relevant_concepts.append({
                        'concept': assoc['associated_concept'],
                        'relevance': 0.7,
                        'info': self.knowledge_base.get(assoc['associated_concept'], {}),
                        'association_context': assoc['context']
                    })
        
        # Sort by relevance
        relevant_concepts.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Generate response
        response = self._generate_knowledge_response(query, relevant_concepts[:5])
        
        return {
            'query': query,
            'relevant_concepts': relevant_concepts[:10],
            'response': response,
            'sources': list(set(info['info'].get('sources', set()) for info in relevant_concepts[:5] if 'info' in info))
        }
    
    def _generate_knowledge_response(self, query: str, relevant_concepts: List[Dict[str, Any]]) -> str:
        """Generate a response based on relevant concepts"""
        if not relevant_concepts:
            return "I don't have specific information about that topic in my knowledge base."
        
        # Build response from relevant concepts
        response_parts = []
        
        # Start with the most relevant concept
        top_concept = relevant_concepts[0]
        response_parts.append(f"Based on my knowledge, {top_concept['concept']} is a key concept here.")
        
        # Add context from learned sources
        if 'info' in top_concept and 'contexts' in top_concept['info']:
            contexts = top_concept['info']['contexts']
            if contexts:
                context_example = random.choice(contexts[:3])
                response_parts.append(f"In context: {context_example}")
        
        # Add associated concepts
        associated_concepts = [concept['concept'] for concept in relevant_concepts[1:4]]
        if associated_concepts:
            response_parts.append(f"This relates to: {', '.join(associated_concepts)}")
        
        return ' '.join(response_parts)
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of what has been learned"""
        return {
            'total_documents': len(self.document_memories),
            'total_concepts': len(self.knowledge_base),
            'learning_sessions': len(self.learning_history),
            'concept_associations': len(self.concept_associations),
            'text_patterns': len(self.text_patterns),
            'top_concepts': sorted(
                [(concept, len(info['activation_history'])) for concept, info in self.knowledge_base.items()],
                key=lambda x: x[1], reverse=True
            )[:10],
            'recent_learning': self.learning_history[-5:] if self.learning_history else []
        }

def demo_wave_text_learning():
    """Demonstrate the wave text learning system"""
    print("[WAVE] WAVE TEXT LEARNING DEMO [WAVE]")
    print("=" * 50)
    
    engine = WaveTextLearningEngine()
    
    # Sample texts to learn from
    sample_texts = {
        'ai_overview': """
        Artificial intelligence is a fascinating field that combines computer science, mathematics, and cognitive science.
        Machine learning algorithms can identify patterns in data and make predictions.
        Deep learning uses neural networks to process complex information.
        The goal is to create systems that can think and learn like humans.
        Wave-based cognition represents a new approach to understanding intelligence.
        """,
        
        'consciousness_theory': """
        Consciousness is one of the most mysterious aspects of human experience.
        It involves awareness, perception, and the ability to reflect on one's own thoughts.
        Some theories suggest consciousness emerges from complex neural interactions.
        Wave patterns in the brain might be the key to understanding consciousness.
        Temporal dynamics could explain how awareness arises from physical processes.
        """,
        
        'creative_writing': """
        Creativity flows like water, finding new paths through the landscape of imagination.
        Writers sculpt words into stories that capture the essence of human experience.
        The dance between structure and freedom creates compelling narratives.
        Each sentence is a brushstroke on the canvas of meaning.
        Great writing resonates with readers across time and space.
        """
    }
    
    print("\n📚 Learning from sample texts:")
    
    # Learn from each text
    for topic, text in sample_texts.items():
        print(f"\n--- Learning from {topic} ---")
        result = engine.learn_from_text(text, source=topic)
        
        if result.get('success'):
            print(f"[+] Processed {result['sentences_processed']} sentences")
            print(f"📖 Learned {result['concepts_learned']} concepts")
            print(f"[TARGET] Top concepts: {[c['concept'] for c in result['top_concepts'][:3]]}")
            print(f"📝 Patterns: {result['patterns_found']}")
        else:
            print(f"[-] Error: {result.get('error')}")
    
    # Show learning summary
    print(f"\n[SEARCH] Learning Summary:")
    summary = engine.get_learning_summary()
    print(f"Documents learned: {summary['total_documents']}")
    print(f"Concepts in knowledge base: {summary['total_concepts']}")
    print(f"Top learned concepts: {[concept for concept, count in summary['top_concepts'][:5]]}")
    
    # Test knowledge query
    print(f"\n❓ Testing knowledge query:")
    query = "What is consciousness?"
    query_result = engine.query_knowledge(query)
    print(f"Query: {query}")
    print(f"Response: {query_result['response']}")
    print(f"Relevant concepts: {[c['concept'] for c in query_result['relevant_concepts'][:3]]}")
    
    # Test creative text generation
    print(f"\n🎨 Testing creative text generation:")
    prompts = [
        "Write about artificial intelligence",
        "Describe the nature of consciousness",
        "Create a story about waves"
    ]
    
    for prompt in prompts:
        print(f"\n--- Prompt: {prompt} ---")
        generation_result = engine.generate_creative_text(prompt, style="creative", length=80)
        print(f"Generated: {generation_result['generated_text']}")
        print(f"Active concepts: {generation_result['active_concepts'][:3]}")
        print(f"Creativity score: {generation_result['analysis']['creativity_score']:.2f}")
        print(f"Relevance score: {generation_result['analysis']['prompt_relevance']:.2f}")
    
    return engine

if __name__ == "__main__":
    demo_wave_text_learning() 