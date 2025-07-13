"""
Temporal Schema Demo
====================
Run this script to see how the new schema consolidation layer works.

It feeds a short sequence of symbolic experiences to the 
TemporalCognitionEngine and then prints out:
  • Consolidated schemas
  • Activation field snapshot
  • Recent resonance events

To execute on Windows PowerShell (from project root):
  python simulations/temporal_schema_demo.py

No external packages are required beyond the project dependencies.
"""

from pprint import pprint
import sys
from pathlib import Path
import argparse

# ------------------------------------------------------------------
# Ensure project root on path
# ------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.cog_config import CogConfig
from src.temporal_cognition import TemporalCognitionEngine

# ------------------------------------------------------------------
# CLI parsing
# ------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Temporal Schema Demo")
parser.add_argument("--reset", action="store_true", help="Clear schema store before run")
parser.add_argument("--backend", choices=["json", "sqlite"], default="json")
args = parser.parse_args()

# Configure
store_path = "schemas_demo.db" if args.backend == "sqlite" else "schemas_demo.json"

cfg = CogConfig(
    deterministic=True,
    seed=42,
    store_backend=args.backend,
    store_path=store_path,
    save_frequency=10,
)

# Optional reset
if args.reset and Path(store_path).exists():
    Path(store_path).unlink()

engine = TemporalCognitionEngine(config=cfg)

# -------------------------------------------------------------
# 2. Feed a sequence of experiences
# -------------------------------------------------------------
sequence = [
    {"visual": ["dog"], "auditory": ["bark"]},
    {"visual": ["dog"], "auditory": ["bark"]},
    {"visual": ["dog"], "auditory": ["bark"]},
    {"visual": ["dog"], "auditory": ["bark"]},
    {"visual": ["dog"], "auditory": ["bark"]},  # 5th frame triggers dream replay
]

for i, kwargs in enumerate(sequence, 1):
    result = engine.live_experience(**kwargs)
    print(f"Frame {i}: active_waves={result['active_waves']}")

# -------------------------------------------------------------
# 3. Inspect cognitive state
# -------------------------------------------------------------
state = engine.get_cognitive_state()

print("\n=== Consolidated Schemas (top) ===")
pprint(state["schemas"])

print("\n=== Activation Field Snapshot (trimmed) ===")
# Show only strongest 10 activations for clarity
activation_sorted = sorted(state["activation_field"].items(), key=lambda kv: abs(kv[1]), reverse=True)[:10]
pprint(activation_sorted)

print("\n=== Recent Resonance Events ===")
pprint(state["recent_resonance"])

print("\nDemo complete. You should see ('bark', 'dog') emerge as a schema after it reoccurs at least 3 times.") 