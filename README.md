# Atlan Wave-Engine

[![CI](https://github.com/<ORG>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<ORG>/<REPO>/actions/workflows/ci.yml)
[![Coverage Status](https://img.shields.io/badge/coverage-auto-important)](./coverage.xml)

The Atlan Wave-Engine is a deterministic, cross-modal cognition core capable of logic reasoning, vision classification, acoustic event detection and EEG schema formation – all without gradient-based training.

## Quick-Start

```bash
# Clone and install
python -m pip install -r requirements.txt

# Run LogicBench slice (full corpus takes <3 s on CPU)
python simulations/wave_logicbench_full_benchmark.py --results wave_logicbench_results.json

# MNIST deterministic classifier
python simulations/mnist_pixel_classifier.py --k 170

# Dolphin click-train sanity check
python -m tools.acoustic_sanity --file samples/bottlenose.wav
```

Full architecture docs are in `ARCHITECTURE.md`. Benchmark tables live in `docs/benchmarks.md`.



