#!/usr/bin/env python3
"""
ATLAN BIOINTELLIGENCE - LANGUAGE REGION
[BRAIN] Language processing region that flows through central brain
"""

import re
from typing import Dict, Any, Optional, List
from core.agent import AtlanAgent

class LanguageRegion:
    """
    [BRAIN] Language specialized brain region
    ALL processing flows through central AtlanAgent - no bypassing allowed!
    """
    
    def __init__(self, central_brain: AtlanAgent):
        """
        Initialize language region with central brain
        
        Args:
            central_brain: The AtlanAgent central executive
        """
        self.central_brain = central_brain
        
    def process_through_brain(self, query: str, brain_result: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [BRAIN] Process language query through central brain
        
        Args:
            query: Language query to process
            brain_result: Central brain's initial processing
            context: Additional context
            
        Returns:
            Language processing result integrated with brain
        """
        # The central brain has already processed this - we build on that
        brain_confidence = brain_result.get("brain_state", {}).get("confidence_level", 0.5)
        
        # Let brain update its language domain expertise
        self.central_brain.domain_expertise["language"] += 0.02
        
        try:
            # Attempt language processing
            language_result = self._analyze_language_structure(query)
            
            if language_result["success"]:
                # Brain learns from successful language processing
                success_phrase = f"Successfully analyzed language: {query}"
                self.central_brain.process_input(success_phrase, domain="language")
                
                return {
                    "success": True,
                    "response": language_result["response"],
                    "confidence": min(1.0, brain_confidence + 0.2),
                    "language_details": language_result["details"],
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
            else:
                # Brain learns from language challenges
                challenge_phrase = f"Language challenge encountered: {query}"
                self.central_brain.process_input(challenge_phrase, domain="language")
                
                return {
                    "success": False,
                    "response": f"I need to analyze this language structure further: {query}",
                    "confidence": brain_confidence * 0.8,
                    "brain_integration": "complete",
                    "learning_occurred": True
                }
                
        except Exception as e:
            # Brain processes the error for learning
            error_phrase = f"Language processing error: {str(e)}"
            self.central_brain.process_input(error_phrase, domain="language")
            
            return {
                "success": False,
                "response": "I encountered a language processing challenge.",
                "confidence": brain_confidence * 0.5,
                "error": str(e),
                "brain_integration": "complete",
                "learning_occurred": True
            }
    
    def _analyze_language_structure(self, query: str) -> Dict[str, Any]:
        """
        [BRAIN] Analyze language structures and patterns
        
        Args:
            query: Language query
            
        Returns:
            Language analysis result
        """
        query_lower = query.lower().strip()
        
        # Check for different types of language analysis
        if any(keyword in query_lower for keyword in ['grammar', 'syntax', 'grammatical']):
            return self._analyze_grammar(query)
            
        elif any(keyword in query_lower for keyword in ['meaning', 'semantic', 'definition']):
            return self._analyze_semantics(query)
            
        elif any(keyword in query_lower for keyword in ['word', 'vocabulary', 'lexical']):
            return self._analyze_lexical(query)
            
        elif any(keyword in query_lower for keyword in ['sentence', 'structure', 'parse']):
            return self._analyze_sentence_structure(query)
            
        elif any(keyword in query_lower for keyword in ['translate', 'translation', 'language']):
            return self._handle_translation(query)
            
        else:
            return self._general_language_analysis(query)
    
    def _analyze_grammar(self, query: str) -> Dict[str, Any]:
        """Analyze grammatical structures"""
        return {
            "success": True,
            "response": "Grammar governs how words combine to form meaningful sentences. Key components include parts of speech, syntax rules, and morphology.",
            "details": {
                "parts_of_speech": ["noun", "verb", "adjective", "adverb", "pronoun", "preposition", "conjunction", "interjection"],
                "syntax_rules": "Subject-Verb-Object order in English",
                "morphology": "How words are formed and modified",
                "examples": {
                    "noun_phrase": "the big dog",
                    "verb_phrase": "is running quickly",
                    "sentence": "The big dog is running quickly."
                }
            }
        }
    
    def _analyze_semantics(self, query: str) -> Dict[str, Any]:
        """Analyze semantic meaning"""
        return {
            "success": True,
            "response": "Semantics deals with meaning in language - how words, phrases, and sentences convey information and concepts.",
            "details": {
                "lexical_semantics": "Word meanings and relationships",
                "compositional_semantics": "How phrase meaning builds from word meanings",
                "pragmatics": "Context-dependent meaning",
                "semantic_relations": ["synonymy", "antonymy", "hyponymy", "polysemy"],
                "example": "The word 'bank' has multiple meanings (financial institution, river edge)"
            }
        }
    
    def _analyze_lexical(self, query: str) -> Dict[str, Any]:
        """Analyze lexical properties"""
        words = query.split()
        word_count = len(words)
        unique_words = len(set(word.lower().strip('.,!?') for word in words))
        
        return {
            "success": True,
            "response": f"Lexical analysis: {word_count} total words, {unique_words} unique words. Lexical diversity: {unique_words/word_count:.2f}",
            "details": {
                "total_words": word_count,
                "unique_words": unique_words,
                "lexical_diversity": round(unique_words/word_count, 2) if word_count > 0 else 0,
                "word_types": ["content words (nouns, verbs, adjectives)", "function words (articles, prepositions)"],
                "analysis": "Higher lexical diversity suggests richer vocabulary usage"
            }
        }
    
    def _analyze_sentence_structure(self, query: str) -> Dict[str, Any]:
        """Analyze sentence structure"""
        sentences = query.split('.')
        sentence_count = len([s for s in sentences if s.strip()])
        avg_words_per_sentence = len(query.split()) / max(sentence_count, 1)
        
        return {
            "success": True,
            "response": f"Structural analysis: {sentence_count} sentences, average {avg_words_per_sentence:.1f} words per sentence.",
            "details": {
                "sentence_count": sentence_count,
                "avg_words_per_sentence": round(avg_words_per_sentence, 1),
                "sentence_types": ["simple", "compound", "complex", "compound-complex"],
                "complexity_indicators": ["sentence length", "subordinate clauses", "coordination"],
                "readability": "Shorter sentences generally easier to process"
            }
        }
    
    def _handle_translation(self, query: str) -> Dict[str, Any]:
        """Handle translation requests"""
        return {
            "success": True,
            "response": "Translation involves converting meaning between languages while preserving semantic content and cultural context.",
            "details": {
                "translation_types": ["literal", "free", "semantic", "pragmatic"],
                "challenges": ["idiomatic expressions", "cultural references", "grammatical differences"],
                "considerations": ["context", "register", "audience", "purpose"],
                "note": "I can help analyze translation concepts but don't perform actual translations"
            }
        }
    
    def _general_language_analysis(self, query: str) -> Dict[str, Any]:
        """General language analysis"""
        return {
            "success": True,
            "response": "I can analyze various aspects of language including grammar, semantics, lexical properties, and sentence structure.",
            "details": {
                "analysis_types": [
                    "Grammar and syntax",
                    "Semantic meaning",
                    "Lexical analysis",
                    "Sentence structure",
                    "Translation concepts"
                ],
                "query_examples": [
                    "Analyze the grammar of this sentence",
                    "What does this word mean?",
                    "Check the structure of this text",
                    "Explain translation principles"
                ]
            }
        } 