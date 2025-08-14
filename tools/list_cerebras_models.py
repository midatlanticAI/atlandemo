#!/usr/bin/env python3
"""
List available Cerebras models and optionally print a recommended match.

Usage:
  py tools/list_cerebras_models.py                 # print all model ids (one per line)
  py tools/list_cerebras_models.py --recommend qwen coder   # print best match only
"""

import sys
from pathlib import Path
from typing import List

# Ensure project root is on sys.path when run from tools/
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cerebras_client import CerebrasClient


def choose_best(models: List[str], includes: List[str]) -> str:
    lc = [m for m in models]
    # Rank by number of include substrings present, then by length (shorter first)
    def score(m: str) -> int:
        ml = m.lower()
        return sum(1 for inc in includes if inc.lower() in ml)
    ranked = sorted(lc, key=lambda m: (-score(m), len(m)))
    return ranked[0] if ranked else ""


def main():
    args = sys.argv[1:]
    client = CerebrasClient()
    models = client.list_models()
    if not args:
        for m in models:
            print(m)
        return
    if args and args[0] == "--recommend":
        includes = [a for a in args[1:]] or ["qwen", "qwen-3", "coder", "qwen-3-coder", "qwen2.5-coder"]
        best = choose_best(models, includes)
        if best:
            print(best)
        return


if __name__ == "__main__":
    main()


