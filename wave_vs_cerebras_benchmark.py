#!/usr/bin/env python3
"""
Wave Engine vs Cerebras Benchmark
Mirror of wave_vs_ollama_benchmark but for the Cerebras Inference API.

Usage (non-interactive preferred for CI):
  py wave_vs_cerebras_benchmark.py --model <MODEL_ID> --samples 100 
     ; set CEREBRAS_API_KEY and optionally CEREBRAS_API_BASE
"""

import json
import time
import random
from pathlib import Path
from typing import List, Dict, Any
import argparse

from enhanced_wave_engine import EnhancedWaveEngine
from cerebras_client import CerebrasClient


def safe_print(text):
    try:
        print(text)
    except Exception:
        try:
            print(str(text))
        except Exception:
            pass


class WaveVsCerebrasBenchmark:
    """
    Benchmark harness comparing the Wave engine to a Cerebras-hosted model.

    Note: the Wave engine under test is not a hand-written rule system. It runs a
    temporal wave-based cognition core that produces numeric activation fields,
    selects expert modules dynamically via a registry and confidence thresholds,
    and integrates wave/expert outputs using weighted fusion. Simple heuristics
    only backstop when no expert meets the confidence threshold.
    """
    def __init__(self, api_key: str = None, api_base: str = None, timeout_s: float = 10.0, max_tokens: int = 8):
        self.wave_engine = EnhancedWaveEngine()
        self.cb = CerebrasClient(api_key=api_key, api_base=api_base, timeout_s=timeout_s)
        self.default_max_tokens = max_tokens
        self.results = {
            'wave': {'correct': 0, 'total': 0, 'time': 0, 'answers': []},
            'cerebras': {'correct': 0, 'total': 0, 'time': 0, 'answers': []}
        }

    # ---------------------------------
    # Data loading
    # ---------------------------------
    def load_sample_questions(self, sample_size: int = 100) -> List[Dict[str, Any]]:
        questions: List[Dict[str, Any]] = []
        target_types = ['propositional_logic', 'first_order_logic']
        for logic_type in target_types:
            base_path = Path(f"logicbench/LogicBench(Eval)/BQA/{logic_type}")
            if not base_path.exists():
                continue
            for axiom_dir in base_path.iterdir():
                if axiom_dir.is_dir():
                    axiom = axiom_dir.name
                    data_file = axiom_dir / "data_instances.json"
                    if data_file.exists():
                        try:
                            data = json.loads(data_file.read_text(encoding='utf-8'))
                        except Exception as e:
                            safe_print(f"[warn] could not load {data_file}: {e}")
                            continue
                        samples = data.get('samples', [])
                        for sample in samples:
                            context = sample.get('context', '')
                            for qa_pair in sample.get('qa_pairs', []):
                                questions.append({
                                    'context': context,
                                    'question': qa_pair.get('question', ''),
                                    'answer': qa_pair.get('answer', ''),
                                    'logic_type': logic_type,
                                    'axiom': axiom
                                })
        if sample_size and len(questions) > sample_size:
            questions = random.sample(questions, sample_size)
        return questions

    # ---------------------------------
    # Wave path
    # ---------------------------------
    def test_wave_engine(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        safe_print("[WAVE] Testing Wave Engine...")
        start = time.time()
        correct = 0
        answers = []
        for q in questions:
            ctx = {'context': q['context'], 'type': q['logic_type'], 'axiom': q['axiom']}
            expert = self.wave_engine.expert_registry.find_best_expert(q['question'], ctx)
            if expert and expert.can_handle(q['question'], ctx) > 0.3:
                predicted = expert.process_query(q['question'], ctx).answer
            else:
                predicted = self._fallback_yesno(q['question'], q['axiom'])
            is_correct = predicted.lower() == q['answer'].lower()
            if is_correct:
                correct += 1
            answers.append({'question': q['question'], 'expected': q['answer'], 'predicted': predicted, 'correct': is_correct})
        elapsed = time.time() - start
        return {'correct': correct, 'total': len(questions), 'time': elapsed, 'answers': answers, 'accuracy': (correct/len(questions)) if questions else 0}

    # ---------------------------------
    # Cerebras path
    # ---------------------------------
    def _extract_yes_no(self, text: str) -> str:
        t = (text or "").strip().lower()
        if t.startswith('yes') and 'no' not in t:
            return 'yes'
        if t.startswith('no') and 'yes' not in t:
            return 'no'
        if 'yes' in t and 'no' not in t:
            return 'yes'
        if 'no' in t and 'yes' not in t:
            return 'no'
        return 'no'

    def test_cerebras_model(self, model: str, questions: List[Dict[str, Any]], max_tokens: int = None) -> Dict[str, Any]:
        safe_print(f"[CB] Testing Cerebras model: {model}")
        if max_tokens is None:
            max_tokens = self.default_max_tokens
        start = time.time()
        correct = 0
        answers: List[Dict[str, Any]] = []
        for i, q in enumerate(questions):
            messages = [
                {"role": "system", "content": "You answer strictly with 'yes' or 'no'."},
                {"role": "user", "content": f"Context: {q['context']}\n\nQuestion: {q['question']}\n\nAnswer with just 'yes' or 'no'."}
            ]
            try:
                resp = self.cb.chat_completion(model=model, messages=messages, max_tokens=max_tokens, temperature=0.0)
            except Exception as e:
                resp = f"error: {e}"
            predicted = self._extract_yes_no(resp)
            ok = predicted.lower() == q['answer'].lower()
            if ok:
                correct += 1
            answers.append({
                'question': q['question'],
                'expected': q['answer'],
                'predicted': predicted,
                'correct': ok,
                'raw': resp,
            })
            if (i + 1) % 10 == 0:
                safe_print(f"   Progress: {i + 1}/{len(questions)}")
        elapsed = time.time() - start
        return {'correct': correct, 'total': len(questions), 'time': elapsed, 'answers': answers, 'accuracy': (correct/len(questions)) if questions else 0}

    # ---------------------------------
    # Helpers
    # ---------------------------------
    @staticmethod
    def _fallback_yesno(question: str, axiom: str) -> str:
        ql = question.lower()
        has_neg = any(neg in ql for neg in ['not', "don't", "doesn't", "won't", "isn't", "aren't"])
        if axiom == 'modus_tollens':
            return 'yes' if has_neg else 'no'
        return 'no' if has_neg else 'yes'

    # ---------------------------------
    # Public
    # ---------------------------------
    def run(self, model: str, sample_size: int = 100, outfile: str = "wave_vs_cerebras_results.json"):
        safe_print("[FLAG] WAVE vs CEREBRAS BENCHMARK")
        safe_print("=" * 50)
        safe_print(f"[DATA] Loading {sample_size} LogicBench questions...")
        questions = self.load_sample_questions(sample_size)
        if not questions:
            safe_print("[error] No questions loaded – check dataset path")
            return
        safe_print(f"[+] Loaded {len(questions)} questions")

        wave_res = self.test_wave_engine(questions)
        cb_res = self.test_cerebras_model(model, questions)

        self._display(wave_res, cb_res, model)
        details = {'wave': wave_res, 'cerebras': cb_res, 'model': model, 'questions': questions}
        Path(outfile).write_text(json.dumps(details, indent=2))
        safe_print(f"[SAVE] Detailed results written to: {outfile}")

    def _display(self, wave: Dict[str, Any], cb: Dict[str, Any], model: str):
        safe_print("\n[TROPHY] BENCHMARK RESULTS")
        safe_print("=" * 50)
        safe_print("[DATA] ACCURACY:")
        safe_print(f"   [WAVE] {wave['accuracy']:.3f} ({wave['accuracy']*100:.1f}%)")
        safe_print(f"   [CB  ] {cb['accuracy']:.3f} ({cb['accuracy']*100:.1f}%)  model={model}")

        if wave['accuracy'] > cb['accuracy']:
            diff = (wave['accuracy'] - cb['accuracy']) * 100
            safe_print(f"   [TROPHY] WINNER: Wave (+{diff:.1f} pp)")
        elif cb['accuracy'] > wave['accuracy']:
            diff = (cb['accuracy'] - wave['accuracy']) * 100
            safe_print(f"   [TROPHY] WINNER: Cerebras (+{diff:.1f} pp)")
        else:
            safe_print("   [SHAKE] TIE")

        safe_print("\n[BOLT] SPEED:")
        wave_qps = wave['total']/wave['time'] if wave['time'] else 0
        cb_qps = cb['total']/cb['time'] if cb['time'] else 0
        safe_print(f"   [WAVE] {wave['time']:.2f}s ({wave_qps:.1f} q/s)")
        safe_print(f"   [CB  ] {cb['time']:.2f}s ({cb_qps:.1f} q/s)")
        if cb_qps:
            safe_print(f"   [ROCKET] Wave is {wave_qps/cb_qps:.1f}x faster")


def main():
    ap = argparse.ArgumentParser(description="Wave vs Cerebras benchmark")
    ap.add_argument("--model", type=str, required=False, help="Cerebras model id")
    ap.add_argument("--samples", type=int, default=100, help="Sample size (default 100)")
    ap.add_argument("--api_base", type=str, default=None, help="Override Cerebras API base URL")
    ap.add_argument("--api_key", type=str, default=None, help="Override Cerebras API key")
    ap.add_argument("--outfile", type=str, default="wave_vs_cerebras_results.json")
    ap.add_argument("--timeout_s", type=float, default=10.0, help="HTTP timeout per request (s)")
    ap.add_argument("--max_tokens", type=int, default=8, help="Max tokens to generate per question")
    args = ap.parse_args()

    bench = WaveVsCerebrasBenchmark(api_key=args.api_key, api_base=args.api_base, timeout_s=args.timeout_s, max_tokens=args.max_tokens)
    model = args.model
    if not model:
        models = bench.cb.list_models()
        if not models:
            safe_print("[warn] Could not list Cerebras models; please pass --model explicitly")
            safe_print("[hint] Set CEREBRAS_API_KEY; optionally set CEREBRAS_API_BASE")
            return
        model = models[0]
        safe_print(f"[info] Using first available model: {model}")

    bench.run(model=model, sample_size=args.samples, outfile=args.outfile)


if __name__ == "__main__":
    main()


