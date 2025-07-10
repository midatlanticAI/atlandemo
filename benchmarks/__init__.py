"""
VTRFM Benchmarks Module
===============================================================================

This module contains benchmarking tools for the VTRFM Wave Engine:
- wave_vs_ollama_benchmark: Compares VTRFM against Ollama models on LogicBench
- wave_logicbench_full_benchmark: Full LogicBench evaluation suite

Author: Johnathan Scott Viruet
Patent Pending: Filed July 7, 2025 - All Rights Reserved
"""

import os
import sys
import argparse
from typing import List, Optional

# Make the benchmark script importable
from .wave_vs_ollama_benchmark import WaveVsOllamaBenchmark
from .wave_logicbench_full_benchmark import run_benchmark as run_full_benchmark


def main(args: Optional[List[str]] = None) -> int:
    """Entry point for the benchmarks CLI"""
    
    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(description='VTRFM Benchmark Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Ollama comparison benchmark
    ollama_parser = subparsers.add_parser('ollama', help='Compare against Ollama models')
    ollama_parser.add_argument('--model', type=str, help='Ollama model to test against')
    ollama_parser.add_argument('--samples', type=int, default=50, help='Number of samples')
    ollama_parser.add_argument('--url', type=str, default='http://localhost:11434', help='Ollama API URL')
    
    # Full LogicBench benchmark
    full_parser = subparsers.add_parser('full', help='Run full LogicBench benchmark')
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == 'ollama':
        benchmark = WaveVsOllamaBenchmark(ollama_url=parsed_args.url)
        if parsed_args.model:
            benchmark.run_comparison(parsed_args.model, sample_size=parsed_args.samples)
        else:
            # Get available models
            models = benchmark.get_available_ollama_models()
            if not models:
                print("[-] No Ollama models found! Make sure Ollama is running.")
                return 1
            
            # Interactive model selection
            print("[BOT] Available Ollama models:")
            for i, model in enumerate(models):
                print(f"   {i+1}. {model}")
            
            try:
                choice = input(f"\nChoose model (1-{len(models)}): ")
                model_index = int(choice) - 1
                
                if 0 <= model_index < len(models):
                    selected_model = models[model_index]
                else:
                    print("[-] Invalid choice, using first model")
                    selected_model = models[0]
            except:
                print("[-] Invalid input, using first model")
                selected_model = models[0]
            
            # Run the benchmark
            benchmark.run_comparison(selected_model, sample_size=parsed_args.samples)
        
        return 0
    
    elif parsed_args.command == 'full':
        run_full_benchmark()
        return 0
    
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
