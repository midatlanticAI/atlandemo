"""wave_seed_runtime.py
Provides nearest_paragraph lookup from precompiled seed_store.json
"""

import json
import math
from pathlib import Path
import hashlib

STORE_PATH = Path("seed_store.json")

if STORE_PATH.exists():
    SEED_STORE = json.loads(STORE_PATH.read_text("utf-8"))
else:
    SEED_STORE = []


def _text_to_vector(text: str):
    h = hashlib.sha256(text.encode("utf-8")).digest()
    ints = [int.from_bytes(h[i : i + 4], "little") for i in range(0, 20, 4)]
    vec = []
    for val in ints:
        freq = 1.0 + (val % 500) / 100.0
        amp = 0.5 + ((val >> 9) % 500) / 1000.0
        phase = ((val >> 19) % 628) / 100.0
        vec.extend([freq, amp, phase])
    return vec[:5]


def _distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def nearest_paragraph(prompt: str, threshold: float = 0.25):
    if not SEED_STORE:
        return None
    vec = _text_to_vector(prompt.lower())
    best = min(SEED_STORE, key=lambda item: _distance(vec, item["vec"]))
    if _distance(vec, best["vec"]) < threshold:
        return best["text"]
    return None 