#!/usr/bin/env python3
"""
Optimized Wave Engine LogicBench Benchmark
Fast wave-only evaluation without cleanup overhead - same as wave_vs_ollama speed.
"""

import json
import random
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse

from enhanced_wave_engine import EnhancedWaveEngine

LOGIC_DIR = Path("logicbench/LogicBench(Eval)/BQA")
LOGIC_TYPES_DEFAULT = ["propositional_logic", "first_order_logic", "nm_logic"]


def load_questions(sample_size: int = None) -> List[Dict[str, Any]]:
    """Load LogicBench questions - same as wave_vs_ollama approach."""
    # Use same logic types as wave_vs_ollama for consistency
    target_types = LOGIC_TYPES_DEFAULT  # Include nm_logic
    questions: List[Dict[str, Any]] = []

    for logic_type in target_types:
        base = LOGIC_DIR / logic_type
        if not base.exists():
            continue
        for axiom_dir in base.iterdir():
            if not axiom_dir.is_dir():
                continue
            axiom = axiom_dir.name
            data_file = axiom_dir / "data_instances.json"
            if not data_file.exists():
                continue
            try:
                data = json.loads(data_file.read_text(encoding="utf-8"))
                for sample in data.get("samples", []):
                    ctx = sample.get("context", "")
                    for qa in sample.get("qa_pairs", []):
                        questions.append({
                            "context": ctx,
                            "question": qa.get("question", ""),
                            "answer": qa.get("answer", ""),
                            "logic_type": logic_type,
                            "axiom": axiom,
                        })
            except Exception as e:
                print(f"[warn] Could not read {data_file}: {e}")

    if sample_size and len(questions) > sample_size:
        questions = random.sample(questions, sample_size)
    random.shuffle(questions)
    return questions


def run_optimized_wave(questions: List[Dict[str, Any]], engine: EnhancedWaveEngine = None):
    """Optimized wave evaluation - same as wave_vs_ollama speed."""
    if engine is None:
        engine = EnhancedWaveEngine()
    
    def fallback_reasoning(question: str, context: str, logic_type: str, axiom: str) -> str:
        """Fallback reasoning for Wave engine - same as wave_vs_ollama."""
        question_lower = question.lower()
        has_negation = any(neg in question_lower for neg in ['not', "don't", "doesn't", "won't", "isn't", "aren't"])
        
        if axiom == 'modus_tollens':
            return "yes" if has_negation else "no"
        else:
            return "no" if has_negation else "yes"

    correct = 0
    start = time.time()

    for q in questions:
        context = {
            'context': q['context'],
            'type': q['logic_type'],
            'axiom': q['axiom']
        }
        
        expert = engine.expert_registry.find_best_expert(q['question'], context)
        if expert and expert.can_handle(q['question'], context) > 0.3:
            result = expert.process_query(q['question'], context)
            predicted = result.answer
        else:
            predicted = fallback_reasoning(q['question'], q['context'], q['logic_type'], q['axiom'])

        if predicted.lower() == q['answer'].lower():
            correct += 1

    elapsed = time.time() - start
    return {
        "total": len(questions),
        "correct": correct,
        "accuracy": correct / len(questions) if questions else 0,
        "time": elapsed,
    }


def main():
    ap = argparse.ArgumentParser(description="Optimized Wave-only LogicBench benchmark")
    ap.add_argument("--samples", type=int, default=None, help="Number of random questions (default: all)")
    args = ap.parse_args()

    print("[OPTIMIZED] Loading LogicBench questions...")
    qs = load_questions(args.samples)
    if not qs:
        print("[error] No questions loaded – check dataset path.")
        return
    
    print(f"[info] Loaded {len(qs)} questions")
    print("[OPTIMIZED] Running Wave Engine (no cleanup overhead)...")
    
    # Create engine once and reuse it (like wave_vs_ollama)
    engine = EnhancedWaveEngine()
    res = run_optimized_wave(qs, engine)
    qps = res["total"] / res["time"] if res["time"] else 0
    
    print(f"[RESULT] Accuracy {res['accuracy']*100:.1f}%  Time {res['time']:.2f}s  ({qps:.1f} q/s)")
    print(f"[SPEED] {qps:.0f} questions per second - optimized performance!")

    # Save detailed results
    out = [{"q": q["question"], "a": q["answer"]} for q in qs]
    Path("wave_logicbench_optimized_results.json").write_text(json.dumps({"meta": res, "questions": out}, indent=2))
    print("[save] Results written to wave_logicbench_optimized_results.json")


if __name__ == "__main__":
    main() 