#!/usr/bin/env python3
"""
RAW WAVE LOGIC DEMO
Shows the exact mathematical expressions the wave engine uses
Output: Pure mathematical calculations - no translation or interpretation
"""

import time
import math
from typing import Dict, List

class RawWaveLogicDemo:
    """Demo showing raw mathematical expressions for logic processing"""
    
    def __init__(self):
        self.logic_questions = [
            {
                "id": "question_1",
                "type": "modus_tollens", 
                "question": "If Mason left his job, then he will not receive any salary. If he will receive any salary, does this mean that Mason didn't leave his job?",
                "answer": "yes"
            },
            {
                "id": "question_2",
                "type": "commutation",
                "question": "We know that at least one of the following is true: (1) Tom is an avid reader and (2) he devours books of all genres. If at least one of (1) and (2) is true, can we say at least one of the following must always be true? (a) he devours books of all genres or (b) Tom is an avid reader",
                "answer": "yes"
            },
            {
                "id": "question_3", 
                "type": "modus_tollens",
                "question": "If Jack won the lottery, then he will buy a house. If he won't buy a house, does this imply that Jack didn't win the lottery?",
                "answer": "yes"
            }
        ]
    
    def extract_symbols(self, text: str) -> List[str]:
        """Extract symbols from text for wave processing"""
        # Simple tokenization - split by spaces and filter short words
        symbols = [word.lower().strip('.,?!();:') for word in text.split()]
        return [symbol for symbol in symbols if len(symbol) > 2]
    
    def show_raw_wave_mathematics(self, symbols: List[str], question_id: str):
        """Show the exact mathematical expressions used by the wave engine"""
        print(f"\n{'='*80}")
        print(f"RAW WAVE MATHEMATICS FOR {question_id.upper()}")
        print(f"{'='*80}")
        
        print(f"INPUT SYMBOLS: {symbols}")
        print(f"SYMBOL COUNT: {len(symbols)}")
        
        print(f"\nWAVE GENERATION ALGORITHM:")
        print(f"frequency = 1.0 + (hash(symbol) % 100) / 100.0")
        print(f"amplitude = 0.5 + (len(symbol) % 10) / 20.0") 
        print(f"phase = (hash(symbol) % 628) / 100.0")
        print(f"wave_value = amplitude * sin(2 * π * frequency * time + phase)")
        
        # Record start time for wave calculation
        start_time = time.time()
        
        print(f"\nRAW MATHEMATICAL CALCULATIONS:")
        print(f"{'Symbol':<15} {'Hash':<12} {'Freq':<8} {'Amp':<8} {'Phase':<8} {'Wave_Value':<12}")
        print(f"{'-'*75}")
        
        activation_field = {}
        
        for symbol in symbols:
            # These are the EXACT mathematical expressions from the wave engine
            symbol_hash = hash(symbol)
            frequency = 1.0 + (symbol_hash % 100) / 100.0
            amplitude = 0.5 + (len(symbol) % 10) / 20.0
            phase = (symbol_hash % 628) / 100.0
            
            # Calculate wave value
            current_time = time.time()
            time_diff = current_time - start_time
            wave_value = amplitude * math.sin(2 * math.pi * frequency * time_diff + phase)
            
            activation_field[symbol] = wave_value
            
            print(f"{symbol:<15} {symbol_hash:<12} {frequency:<8.3f} {amplitude:<8.3f} {phase:<8.3f} {wave_value:<12.6f}")
        
        print(f"\nWAVE INTERFERENCE MATRIX:")
        print(f"Total symbols processed: {len(activation_field)}")
        print(f"Activation field size: {len(activation_field)} entries")
        
        # Show raw activation values
        print(f"\nRAW ACTIVATION VALUES:")
        for symbol, value in activation_field.items():
            print(f"  {symbol}: {value:.8f}")
        
        # Calculate wave statistics
        values = list(activation_field.values())
        mean_activation = sum(values) / len(values)
        max_activation = max(values)
        min_activation = min(values)
        
        print(f"\nWAVE STATISTICS:")
        print(f"  Mean activation: {mean_activation:.8f}")
        print(f"  Max activation:  {max_activation:.8f}")
        print(f"  Min activation:  {min_activation:.8f}")
        print(f"  Activation range: {max_activation - min_activation:.8f}")
        
        return activation_field
    
    def run_demo(self):
        """Run the raw wave logic demo"""
        print("RAW WAVE LOGIC DEMO - MATHEMATICAL EXPRESSIONS ONLY")
        print("="*80)
        print("This demo shows the EXACT mathematical calculations the wave engine performs")
        print("NO interpretation, NO translation - just pure mathematics")
        print("="*80)
        
        for i, question_data in enumerate(self.logic_questions, 1):
            print(f"\n\nLOGIC QUESTION {i}:")
            print(f"Type: {question_data['type']}")
            print(f"Question: {question_data['question']}")
            print(f"Expected Answer: {question_data['answer']}")
            
            # Extract symbols for wave processing
            symbols = self.extract_symbols(question_data['question'])
            
            # Show raw mathematical expressions
            activation_field = self.show_raw_wave_mathematics(symbols, question_data['id'])
            
            print(f"\nSYMBOL-TO-WAVE MAPPING (Raw Data):")
            for symbol, wave_val in activation_field.items():
                print(f"  '{symbol}' → {wave_val:.10f}")
        
        print(f"\n\n{'='*80}")
        print("DEMO COMPLETE - Raw mathematical expressions shown")
        print("The wave engine uses ONLY these sine wave calculations")
        print("No neural networks, no language models, no AI - just math")
        print("="*80)

def main():
    """Main function to run the demo"""
    demo = RawWaveLogicDemo()
    demo.run_demo()

if __name__ == "__main__":
    main() 