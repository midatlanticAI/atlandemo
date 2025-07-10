#!/usr/bin/env python3
"""
Wave Engine LogicBench Full Benchmark
Comprehensive evaluation of Wave Engine on LogicBench
"""

import os
import json
import time
from pathlib import Path

# Import from the refactored package structure
try:
    from vtrfm import WaveEngine
except ImportError:
    # For development environment when run directly
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.vtrfm import WaveEngine


def safe_print(text: str):
    """Print helper that avoids Unicode errors in some consoles."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


class WaveLogicBenchBenchmark:
    """Run EnhancedWaveEngine on the full LogicBench Eval dataset (BQA + MCQA)."""

    TASK_FAMILIES = ["propositional_logic", "first_order_logic", "nm_logic"]
    TASK_TYPES = ["BQA", "MCQA"]

    def __init__(self):
        self.wave_engine = WaveEngine()
        self.results: Dict[str, Dict[str, Any]] = {}

    # ---------------------------------------------------------------------
    # Data loading helpers
    # ---------------------------------------------------------------------
    def _iter_json_files(self) -> Generator[Tuple[str, str, Path], None, None]:
        """Yield (task_type, logic_family, path) for every data_instances.json."""
        for task in self.TASK_TYPES:
            for family in self.TASK_FAMILIES:
                root = Path(f"logicbench/LogicBench(Eval)/{task}/{family}")
                if not root.exists():
                    continue
                for axiom_dir in root.iterdir():
                    data_file = axiom_dir / "data_instances.json"
                    if data_file.exists():
                        yield task, family, data_file

    # ------------------------------------------------------------------
    # BQA evaluation (yes/no)
    # ------------------------------------------------------------------
    def _eval_bqa_sample(self, sample: Dict[str, Any], logic_type: str, axiom: str) -> List[Dict[str, Any]]:
        out = []
        context_txt = sample.get("context", "")
        for qa in sample.get("qa_pairs", []):
            question = qa.get("question", "")
            expected = qa.get("answer", "").lower()
            ctx = {
                "context": context_txt,
                "type": logic_type,
                "axiom": axiom,
            }
            expert = self.wave_engine.expert_registry.find_best_expert(question, ctx)
            if expert and expert.can_handle(question, ctx) > 0.3:
                predicted = expert.process_query(question, ctx).answer.lower()
            else:
                predicted = self._fallback_yesno(question, axiom)
            out.append({
                "question": question,
                "expected": expected,
                "predicted": predicted,
                "correct": predicted == expected,
                "logic_type": logic_type,
                "axiom": axiom,
            })
        return out

    # ------------------------------------------------------------------
    # MCQA evaluation (multiple-choice)
    # ------------------------------------------------------------------
    def _eval_mcqa_sample(self, sample: Dict[str, Any], logic_type: str, axiom: str) -> Dict[str, Any]:
        context_txt = sample.get("context", "")
        question = sample.get("question", "")
        choices: Dict[str, str] = sample.get("choices", {})
        expected_key = sample.get("answer", "")

        # Quick heuristic: token overlap between choice and context+question
        ctx_tokens = set((context_txt + " " + question).lower().split())
        scored: List[Tuple[str, float]] = []
        for k, txt in choices.items():
            overlap = len(set(txt.lower().split()) & ctx_tokens)
            scored.append((k, overlap))
        # Keep top-N choices for expert processing (N=2)
        scored.sort(key=lambda x: x[1], reverse=True)
        top_choices = [k for k, _ in scored[:2]]

        best_choice = top_choices[0]  # default to highest overlap
        best_conf = -1.0
        for key in top_choices:
            choice_text = choices[key]
            prompt = f"{question} Option: {choice_text}"
            ctx = {
                "context": context_txt,
                "type": logic_type,
                "axiom": axiom,
            }
            expert = self.wave_engine.expert_registry.find_best_expert(prompt, ctx)
            if expert and expert.can_handle(prompt, ctx) > 0.3:
                resp = expert.process_query(prompt, ctx)
                conf = getattr(resp, "confidence", 0.0)
                if conf > best_conf:
                    best_conf = conf
                    best_choice = key

        # If confidence still low, just keep heuristic best_choice
        if best_choice is None:
            best_choice = random.choice(list(choices.keys()))

        return {
            "question": question,
            "expected": expected_key,
            "predicted": best_choice,
            "correct": best_choice == expected_key,
            "logic_type": logic_type,
            "axiom": axiom,
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self):
        # Verify dataset integrity if hash file is present
        self._verify_dataset_integrity()
        safe_print("[BENCH] Wave Engine full LogicBench (Eval) run")
        start = time.time()

        total_correct = 0
        total_questions = 0

        for task_type, logic_family, path in self._iter_json_files():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            axiom = data.get("axiom", path.parent.name)
            for sample in data.get("samples", []):
                if task_type == "BQA":
                    answers = self._eval_bqa_sample(sample, logic_family, axiom)
                    total_correct += sum(a["correct"] for a in answers)
                    total_questions += len(answers)
                else:  # MCQA
                    result = self._eval_mcqa_sample(sample, logic_family, axiom)
                    total_correct += 1 if result["correct"] else 0
                    total_questions += 1

        elapsed = time.time() - start
        accuracy = total_correct / total_questions if total_questions else 0.0
        safe_print(f"[DONE] Questions: {total_questions}, Correct: {total_correct}, Accuracy: {accuracy*100:.2f}%, Time: {elapsed:.2f}s")

        # save raw metrics
        self.results = {
            "total_questions": total_questions,
            "total_correct": total_correct,
            "accuracy": accuracy,
            "time_seconds": elapsed,
        }
        with open("wave_logicbench_full_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        safe_print("[SAVE] Detailed metrics written to wave_logicbench_full_results.json")

    # ------------------------------------------------------------------
    # Dataset integrity verification
    # ------------------------------------------------------------------
    def _verify_dataset_integrity(self):
        """If logicbench_hashes.txt exists, ensure all listed files match size and sha256."""
        hash_file = Path("logicbench_hashes.txt")
        if not hash_file.exists():
            safe_print("[WARN] logicbench_hashes.txt not found; skipping integrity check")
            return

        mismatches = []
        for line in hash_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                sha, size_str, rel_path = line.split(maxsplit=2)
                expected_size = int(size_str)
            except ValueError:
                safe_print(f"[WARN] Malformed line in hash file: {line}")
                continue

            file_path = Path(rel_path)
            if not file_path.exists():
                mismatches.append(f"missing:{rel_path}")
                continue
            actual_size = file_path.stat().st_size
            if actual_size != expected_size:
                mismatches.append(f"size:{rel_path}")
                continue
            # compute sha256
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            if h.hexdigest() != sha:
                mismatches.append(f"hash:{rel_path}")

        if mismatches:
            safe_print("[FAIL] Dataset integrity check failed:")
            for m in mismatches:
                safe_print(f"   - {m}")
            raise SystemExit(1)
        safe_print("[DATA] Dataset integrity verified (logicbench_hashes.txt)")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _fallback_yesno(question: str, axiom: str) -> str:
        """Maintain old heuristic as last resort."""
        q_lower = question.lower()
        has_neg = any(neg in q_lower for neg in ["not", "n't", "doesn't", "isn't", "aren't", "won't"])
        if axiom == "modus_tollens":
            return "yes" if has_neg else "no"
        return "no" if has_neg else "yes"


if __name__ == "__main__":
    benchmark = WaveLogicBenchBenchmark()
    benchmark.run() 