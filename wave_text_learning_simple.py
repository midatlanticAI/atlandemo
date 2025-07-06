#!/usr/bin/env python3
"""
Simple Wave Text Learning System
"""

import os
import re
import time
import random
from typing import Dict, List, Any
from wave_text_engine import WaveTextEngine

class SimpleWaveTextLearner:
    """Simple text learning using wave cognition"""
    
    def __init__(self):
        self.wave_engine = WaveTextEngine()
        self.knowledge_base = {}
        self.learned_documents = {}
        self.concept_connections = {}
        
    def learn_from_file(self, filename: str) -> Dict[str, Any]:
        """Learn from a text file"""
        if not os.path.exists(filename):
            return {'error': f'File not found: {filename}'}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.learn_from_text(content, filename)
        
        except Exception as e:
            return {'error': f'Error reading file: {e}'}
    
    def learn_from_text(self, text: str, source: str = "text_input") -> Dict[str, Any]:
        """Learn from text content"""
        # Split into sentences
        sentences = self._split_sentences(text)
        
        learned_concepts = []
        
        # Process each sentence
        for sentence in sentences:
            # Extract symbols
            symbols = self.wave_engine.text_to_symbols(sentence)
            
            # Process through wave engine
            result = self.wave_engine.process_text_input(sentence)
            
            # Store strong activations
            activations = result['wave_activations']
            for concept, activation in activations.items():
                if abs(activation) > 0.3:
                    learned_concepts.append({
                        'concept': concept,
                        'activation': activation,
                        'sentence': sentence,
                        'source': source
                    })
        
        # Update knowledge base
        self._update_knowledge(learned_concepts)
        
        # Store document
        self.learned_documents[source] = {
            'content': text,
            'sentences': sentences,
            'concepts': learned_concepts,
            'timestamp': time.time()
        }
        
        return {
            'success': True,
            'source': source,
            'sentences_processed': len(sentences),
            'concepts_learned': len(learned_concepts),
            'top_concepts': sorted(learned_concepts, key=lambda x: abs(x['activation']), reverse=True)[:5]
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
    
    def _update_knowledge(self, concepts: List[Dict[str, Any]]):
        """Update knowledge base with learned concepts"""
        for concept_info in concepts:
            concept = concept_info['concept']
            
            if concept not in self.knowledge_base:
                self.knowledge_base[concept] = {
                    'total_activations': 0,
                    'contexts': [],
                    'sources': set()
                }
            
            self.knowledge_base[concept]['total_activations'] += abs(concept_info['activation'])
            self.knowledge_base[concept]['contexts'].append(concept_info['sentence'])
            self.knowledge_base[concept]['sources'].add(concept_info['source'])
    
    def generate_text(self, prompt: str, length: int = 50) -> str:
        """Generate text based on learned knowledge"""
        # Get concepts from prompt
        prompt_symbols = self.wave_engine.text_to_symbols(prompt)
        
        # Find relevant concepts from knowledge base
        relevant_concepts = []
        for concept in prompt_symbols:
            if concept in self.knowledge_base:
                relevant_concepts.append(concept)
        
        # If no relevant concepts, use most frequent concepts
        if not relevant_concepts:
            sorted_concepts = sorted(
                self.knowledge_base.items(),
                key=lambda x: x[1]['total_activations'],
                reverse=True
            )
            relevant_concepts = [concept for concept, _ in sorted_concepts[:5]]
        
        # Generate sentences
        sentences = []
        target_words = length
        current_words = 0
        
        while current_words < target_words and len(sentences) < 5:
            sentence = self._generate_sentence(relevant_concepts)
            if sentence:
                sentences.append(sentence)
                current_words += len(sentence.split())
        
        return ' '.join(sentences)
    
    def _generate_sentence(self, concepts: List[str]) -> str:
        """Generate a sentence using given concepts"""
        if not concepts:
            return ""
        
        # Simple templates
        templates = [
            "The concept of {concept} is important for understanding {related}.",
            "When we consider {concept}, we find that {related} plays a key role.",
            "{concept} connects to {related} in meaningful ways.",
            "Understanding {concept} requires examining {related}.",
            "The relationship between {concept} and {related} is fascinating."
        ]
        
        # Pick random concepts
        main_concept = random.choice(concepts)
        related_concept = random.choice(concepts) if len(concepts) > 1 else main_concept
        
        # Choose template and fill
        template = random.choice(templates)
        sentence = template.format(concept=main_concept, related=related_concept)
        
        return sentence
    
    def query_knowledge(self, query: str) -> str:
        """Query the knowledge base"""
        query_symbols = self.wave_engine.text_to_symbols(query)
        
        # Find relevant concepts
        relevant_info = []
        for symbol in query_symbols:
            if symbol in self.knowledge_base:
                info = self.knowledge_base[symbol]
                relevant_info.append({
                    'concept': symbol,
                    'strength': info['total_activations'],
                    'contexts': info['contexts'][:2]  # First 2 contexts
                })
        
        # Sort by strength
        relevant_info.sort(key=lambda x: x['strength'], reverse=True)
        
        if not relevant_info:
            return "I don't have specific information about that topic."
        
        # Generate response
        top_concept = relevant_info[0]
        response = f"Based on my knowledge, {top_concept['concept']} is relevant to your query."
        
        if top_concept['contexts']:
            response += f" For example: {top_concept['contexts'][0]}"
        
        return response
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of learned knowledge"""
        sorted_concepts = sorted(
            self.knowledge_base.items(),
            key=lambda x: x[1]['total_activations'],
            reverse=True
        )
        
        return {
            'total_concepts': len(self.knowledge_base),
            'documents_learned': len(self.learned_documents),
            'top_concepts': [(concept, info['total_activations']) for concept, info in sorted_concepts[:10]],
            'sources': list(set().union(*[info['sources'] for info in self.knowledge_base.values()]))
        }

def demo_simple_wave_learning():
    """Demo the simple wave learning system"""
    print("[WAVE] SIMPLE WAVE TEXT LEARNING DEMO [WAVE]")
    print("=" * 50)
    
    learner = SimpleWaveTextLearner()
    
    # Sample text to learn from
    sample_text = """
    Artificial intelligence is transforming how we understand cognition and consciousness.
    Machine learning algorithms can process vast amounts of data to identify patterns.
    Neural networks are inspired by how the human brain processes information.
    Wave-based cognition offers a new perspective on how intelligence might emerge.
    Temporal dynamics in neural systems could explain consciousness and awareness.
    The future of AI might involve understanding these wave patterns better.
    """
    
    print("\n📚 Learning from sample text:")
    result = learner.learn_from_text(sample_text, "ai_sample")
    
    if result['success']:
        print(f"[+] Processed {result['sentences_processed']} sentences")
        print(f"📖 Learned {result['concepts_learned']} concepts")
        print("[TARGET] Top concepts:")
        for concept_info in result['top_concepts']:
            print(f"  - {concept_info['concept']}: {concept_info['activation']:.3f}")
    
    # Test knowledge query
    print(f"\n❓ Testing knowledge query:")
    query = "What is artificial intelligence?"
    response = learner.query_knowledge(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
    
    # Test text generation
    print(f"\n🎨 Testing text generation:")
    prompt = "Write about consciousness and AI"
    generated = learner.generate_text(prompt, length=60)
    print(f"Prompt: {prompt}")
    print(f"Generated: {generated}")
    
    # Show knowledge summary
    print(f"\n[SEARCH] Knowledge Summary:")
    summary = learner.get_knowledge_summary()
    print(f"Total concepts: {summary['total_concepts']}")
    print(f"Documents learned: {summary['documents_learned']}")
    print(f"Top concepts: {[concept for concept, _ in summary['top_concepts'][:5]]}")
    
    return learner

if __name__ == "__main__":
    demo_simple_wave_learning() 