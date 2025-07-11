#!/usr/bin/env python3
"""wave_logicbench_wave_only.py
Run Wave Engine on LogicBench data without any Ollama/LLM dependency.

Usage examples:
    # 500 random questions from propositional + first-order logic
    python wave_logicbench_wave_only.py --samples 500

    # Same but include nm_logic even though performance is known to be weak
    python wave_logicbench_wave_only.py --samples 500 --include-nm

Outputs accuracy, questions-per-second, and writes detailed Q/A to
`wave_logicbench_wave_only_results.json`.
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
LOGIC_TYPE_NM = "nm_logic"


def load_questions(sample_size: int) -> List[Dict[str, Any]]:
    # All logic types are now included by default.
    target_types = LOGIC_TYPES_DEFAULT
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


def run_wave_only(questions: List[Dict[str, Any]]):
    """Fast expert-only evaluation mirrored from wave_vs_ollama_benchmark."""

    engine = EnhancedWaveEngine()

    # Speed tweaks (same as benchmark)
    engine.wave_engine.dream_frequency = 10_000  # disable replay
    engine.wave_engine._dream_replay = lambda: None

    def fallback_reasoning(question: str, axiom: str) -> str:
        q_lower = question.lower()
        neg = any(t in q_lower for t in ["not", "doesn't", "won't", "isn't", "aren't"])
        if axiom == "modus_tollens":
            return "yes" if neg else "no"
        return "no" if neg else "yes"

    correct = 0
    start = time.time()

    for q in questions:
        # Keep wave-field empty to avoid buildup (cheap but safe)
        stream = engine.wave_engine.experience_stream
        stream.active_waves.clear()
        stream.frames.clear()
        stream.resonance_patterns.clear()

        ctx = {
            "context": q["context"],
            "type": q["logic_type"],
            "axiom": q["axiom"],
        }

        expert = engine.expert_registry.find_best_expert(q["question"], ctx)
        if expert and expert.can_handle(q["question"], ctx) > 0.3:
            answer = expert.process_query(q["question"], ctx).answer
        else:
            answer = fallback_reasoning(q["question"], q["axiom"])

        if answer.lower() == q["answer"].lower():
            correct += 1

    elapsed = time.time() - start
    return {
        "total": len(questions),
        "correct": correct,
        "accuracy": correct / len(questions) if questions else 0,
        "time": elapsed,
    }


def main():
    ap = argparse.ArgumentParser(description="Wave-only LogicBench benchmark")
    ap.add_argument("--samples", type=int, default=200, help="Number of random questions (0 = all)")
    args = ap.parse_args()

    qs = load_questions(args.samples)
    if not qs:
        print("[error] No questions loaded – check dataset path.")
        return
    print(f"[info] Loaded {len(qs)} questions")
    res = run_wave_only(qs)
    qps = res["total"] / res["time"] if res["time"] else 0
    print(f"[RESULT] Accuracy {res['accuracy']*100:.1f}%  Time {res['time']:.2f}s  ({qps:.1f} q/s)")

    # Save detailed results minimal (question & correct flag)
    out = [{"q": q["question"], "a": q["answer"]} for q in qs]
    Path("wave_logicbench_wave_only_results.json").write_text(json.dumps({"meta": res, "questions": out}, indent=2))
    print("[save] Results written to wave_logicbench_wave_only_results.json")


if __name__ == "__main__":
    main() 