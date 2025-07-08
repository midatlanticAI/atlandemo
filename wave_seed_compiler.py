"""wave_seed_compiler.py
Reads seed_knowledge.yaml and produces seed_store.json for runtime use.
Run once after editing YAML:
    python wave_seed_compiler.py
"""

import json
import hashlib
from pathlib import Path
import yaml
import math

YAML_PATH = Path("seed_knowledge.yaml")
OUTPUT_PATH = Path("seed_store.json")


def text_to_vector(text: str):
    """Convert text to 5-float wave signature using stable hash."""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    ints = [int.from_bytes(h[i : i + 4], "little") for i in range(0, 20, 4)]  # 5 chunks
    vec = []
    for val in ints:
        # Map to deterministic float range 0-2π for phase and 0-1 for amplitude
        freq = 1.0 + (val % 500) / 100.0  # 1.0 – 6.0
        amp = 0.5 + ((val >> 9) % 500) / 1000.0  # 0.5 – 1.0
        phase = ((val >> 19) % 628) / 100.0  # 0 – 6.28
        vec.extend([freq, amp, phase])
    return vec[:5]  # keep first 5 floats


def compile_yaml():
    data = yaml.safe_load(YAML_PATH.read_text("utf-8"))
    store = []
    for entry in data:
        vec = text_to_vector(entry["text"].lower())
        store.append({"id": entry["id"], "vec": vec, "text": entry["text"]})
    OUTPUT_PATH.write_text(json.dumps(store, ensure_ascii=False, indent=2))
    print(f"[+] Compiled {len(store)} seed items → {OUTPUT_PATH}")


if __name__ == "__main__":
    compile_yaml() 